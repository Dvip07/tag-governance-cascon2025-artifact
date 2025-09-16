import os
import csv
import yaml
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from collections import defaultdict
from datetime import datetime

# ===== Config =====
STEP2_INPUT = "sbert_fix/all_tags/step_2/final_tags.csv"
OUT_DIR = "sbert_fix/all_tags/step_3"
os.makedirs(OUT_DIR, exist_ok=True)
SBERT_MODEL = "all-MiniLM-L6-v2"  # plug-and-play!
FAISS_THRESHOLD = 0.80  # cosine similarity threshold (tune as desired)

def load_tags():
    tags = []
    with open(STEP2_INPUT, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('filtered') == 'N':
                tags.append(row)
    return tags

def get_embeddings(tags, sbert):
    tag_texts = [t['tag'] for t in tags]
    return np.array(sbert.encode(tag_texts, convert_to_numpy=True, show_progress_bar=True))

def cluster_tags_faiss(tags, embeddings, threshold=FAISS_THRESHOLD):
    """Agglomerative style clustering with FAISS (cosine sim > threshold)"""
    dim = embeddings.shape[1]
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    n = len(tags)
    assigned = np.full(n, -1, dtype=int)
    clusters = []
    next_cluster_id = 0

    for i in range(n):
        if assigned[i] != -1:
            continue
        D, I = index.search(embeddings[i:i+1], n)
        members = [j for j, sim in zip(I[0], D[0]) if sim > threshold]
        for m in members:
            assigned[m] = next_cluster_id
        clusters.append(members)
        next_cluster_id += 1

    tag2cluster = {i: assigned[i] for i in range(n)}
    cluster2tags = {cid: members for cid, members in enumerate(clusters)}
    return tag2cluster, cluster2tags

def cluster_and_save(tags, mode="all"):
    # tags: list of dicts; mode: "all", "by_model", "by_version"
    sbert = SentenceTransformer(SBERT_MODEL)
    outputs = []
    yaml_log = {
        "timestamp": datetime.utcnow().isoformat(),
        "sbert_model": SBERT_MODEL,
        "faiss_threshold": FAISS_THRESHOLD,
        "mode": mode,
        "clusters": [],
        "meta": {}
    }
    if mode == "all":
        partitions = {"all": tags}
    elif mode == "by_model":
        partitions = defaultdict(list)
        for t in tags:
            partitions[t['model']].append(t)
    elif mode == "by_version":
        partitions = defaultdict(list)
        for t in tags:
            partitions[t['version']].append(t)
    else:
        raise ValueError("Unknown clustering mode")

    for part, taglist in partitions.items():
        if not taglist:
            continue
        embeddings = get_embeddings(taglist, sbert)
        tag2cluster, cluster2tags = cluster_tags_faiss(taglist, embeddings)
        # Save output for CSV
        for i, t in enumerate(taglist):
            outputs.append({
                "tag": t['tag'],
                "hlj_id": t['hlj_id'],
                "requirement_id": t['requirement_id'],
                "model": t['model'],
                "version": t['version'],
                "cluster_id": f"{part}_{tag2cluster[i]}"
            })
        # For YAML log: store samples, size, models/versions in cluster, sample tags, etc.
        for cid, members in cluster2tags.items():
            sample_tags = [taglist[m]['tag'] for m in members[:5]]
            cluster_models = sorted(set(taglist[m]['model'] for m in members))
            cluster_versions = sorted(set(taglist[m]['version'] for m in members))
            yaml_log["clusters"].append({
                "partition": part,
                "cluster_id": f"{part}_{cid}",
                "size": len(members),
                "sample_tags": sample_tags,
                "models": cluster_models,
                "versions": cluster_versions,
            })
        yaml_log["meta"][part] = {
            "total_clusters": len(cluster2tags),
            "total_tags": len(taglist),
            "avg_cluster_size": float(np.mean([len(v) for v in cluster2tags.values()])) if cluster2tags else 0
        }
    return outputs, yaml_log

def save_csv(rows, fname):
    with open(fname, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = [
            "tag", "hlj_id", "requirement_id", "model", "version", "cluster_id"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Saved clusters: {fname}")

def save_yaml(obj, fname):
    with open(fname, "w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f)
    print(f"✅ Saved YAML log: {fname}")

def main():
    tags = load_tags()
    # Cluster ALL
    all_rows, all_yaml = cluster_and_save(tags, mode="all")
    save_csv(all_rows, os.path.join(OUT_DIR, "tag_clusters.csv"))
    save_yaml(all_yaml, os.path.join(OUT_DIR, "tag_clusters_log.yaml"))
    # Cluster BY MODEL
    bymodel_rows, bymodel_yaml = cluster_and_save(tags, mode="by_model")
    save_csv(bymodel_rows, os.path.join(OUT_DIR, "tag_clusters_by_model.csv"))
    save_yaml(bymodel_yaml, os.path.join(OUT_DIR, "tag_clusters_by_model_log.yaml"))
    # Cluster BY VERSION
    byver_rows, byver_yaml = cluster_and_save(tags, mode="by_version")
    save_csv(byver_rows, os.path.join(OUT_DIR, "tag_clusters_by_version.csv"))
    save_yaml(byver_yaml, os.path.join(OUT_DIR, "tag_clusters_by_version_log.yaml"))

if __name__ == "__main__":
    main()
