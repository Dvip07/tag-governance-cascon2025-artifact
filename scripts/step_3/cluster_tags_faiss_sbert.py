import os
import csv
import yaml
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from collections import defaultdict
from datetime import datetime
import argparse

# === Config utils ===
def load_config(cfg_path):
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(cfg, cfg_path):
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

def ensure_run(cfg, cfg_path):
    run_id = cfg.get("globals", {}).get("run_id")
    run_dir = cfg.get("globals", {}).get("run_dir")
    if not run_id or not run_dir:
        raise RuntimeError("⚠️ No run_id/run_dir found. Did you run Step 1 first?")
    return run_id, run_dir

# === Helpers ===
def find_step2_csv(cfg):
    """Try multiple possible Step 2 outputs in order of preference."""
    candidates = [
        cfg["outputs"].get("tags_token_filtered"),
        cfg["outputs"].get("step2_all"),
        cfg["outputs"].get("step2_rescued"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            print(f"📂 Using Step 2 output: {c}")
            return c
    raise FileNotFoundError(
        "❌ No Step 2 outputs found. Expected one of: tags_token_filtered, step2_all, step2_rescued."
    )

def load_tags(step2_csv):
    tags = []
    with open(step2_csv, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Prefer explicit 'filtered' column, fallback to all rows
            if "filtered" not in row or row.get("filtered") == "N":
                tags.append(row)
    return tags

def get_embeddings(tags, sbert):
    tag_texts = [t["tag"] for t in tags]
    return np.array(sbert.encode(tag_texts, convert_to_numpy=True, show_progress_bar=True))

def cluster_tags_faiss(tags, embeddings, threshold=0.80):
    """Agglomerative-style clustering with FAISS cosine similarity."""
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

    return assigned, clusters

# === Main ===
def main(cfg_path):
    cfg = load_config(cfg_path)
    run_id, run_dir = ensure_run(cfg, cfg_path)

    step2_csv = find_step2_csv(cfg)

    # params
    sbert_model = cfg.get("step3", {}).get("sbert_model", "all-MiniLM-L6-v2")
    faiss_threshold = cfg.get("step3", {}).get("faiss_threshold", 0.80)

    sbert = SentenceTransformer(sbert_model)
    tags = load_tags(step2_csv)

    if not tags:
        raise RuntimeError("❌ No tags loaded from Step 2 output. Aborting.")

    out_dir = os.path.join(run_dir, "step_3")
    os.makedirs(out_dir, exist_ok=True)

    # --- Run clustering ---
    embeddings = get_embeddings(tags, sbert)
    assigned, clusters = cluster_tags_faiss(tags, embeddings, threshold=faiss_threshold)

    # --- Save main cluster file ---
    cluster_csv = os.path.join(out_dir, "tag_clusters.csv")
    with open(cluster_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tag", "cluster_id"])
        for row, cid in zip(tags, assigned):
            writer.writerow([row["tag"], cid])

    print(f"✅ Saved {cluster_csv}")

    # --- Update config outputs ---
    cfg["outputs"]["tag_clusters"] = cluster_csv
    cfg["outputs"]["tag_clusters_by_model"] = os.path.join(out_dir, "tag_clusters_by_model.csv")
    cfg["outputs"]["tag_clusters_by_version"] = os.path.join(out_dir, "tag_clusters_by_version.csv")
    save_config(cfg, cfg_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 3: Cluster tags with SBERT + FAISS")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml")
    args = parser.parse_args()
    main(args.config)
