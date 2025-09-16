import os
import json
import yaml
import csv
from collections import defaultdict, Counter
import argparse
from datetime import datetime
import glob

# === Config helpers ===
def load_config(cfg_path):
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(cfg, cfg_path):
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

def ensure_run(cfg):
    run_id = cfg.get("globals", {}).get("run_id")
    run_dir = cfg.get("globals", {}).get("run_dir")
    if not run_id or not run_dir:
        raise RuntimeError("⚠️ No run_id/run_dir found. Did you run Step 1–3 first?")
    return run_id, run_dir


def find_cluster_csv(cfg):
    candidates = [
        cfg["outputs"].get("tag_clusters"),
        os.path.join(cfg["globals"]["run_dir"], "step_2", "tag_clusters.csv"),
    ]
    prev_run_dir = cfg["globals"].get("prev_run_dir")
    if prev_run_dir:
        candidates.append(os.path.join(prev_run_dir, "step_2", "tag_clusters.csv"))

    # NEW fallback: glob search in step_3
    run_dir = cfg["globals"].get("run_dir")
    if run_dir:
        globbed = glob.glob(os.path.join(run_dir, "step_2", "tag_clusters*.csv"))
        candidates.extend(globbed)

    for c in candidates:
        if c and os.path.exists(c):
            print(f"📂 Using Step 3 clusters: {c}")
            return c

    raise FileNotFoundError(f"❌ No Step 3 outputs found. Tried: {candidates}")
    

# === Main ===
def main(cfg_path):
    cfg = load_config(cfg_path)
    run_id, run_dir = ensure_run(cfg)

    cluster_csv = find_cluster_csv(cfg)
    if not cluster_csv or not os.path.exists(cluster_csv):
        raise FileNotFoundError("❌ Step 2 output not found. Did you run cluster_tags_faiss_sbert.py?")


    hlj_root = cfg["globals"]["base_dir"]
    models = cfg["globals"]["models"]

    out_dir = os.path.join(run_dir, "step_4")
    os.makedirs(out_dir, exist_ok=True)
    alias_json = os.path.join(out_dir, "tag_alias_map.json")
    canonical_yaml = os.path.join(out_dir, "canonical_tags.yaml")
    canonical_yaml_with_domain = os.path.join(out_dir, "canonical_tags_with_domain.yaml")
    log_path = os.path.join(out_dir, "domain_autopopulate_with_domain.log")
    csv_path = os.path.join(out_dir, "tag_domain_summary.csv")

    # --- 1. Load clusters ---
    clusters = defaultdict(list)
    tag_freq = Counter()
    with open(cluster_csv, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag = row["tag"]
            cluster_id = row["cluster_id"]
            clusters[cluster_id].append(tag)
            tag_freq[tag] += 1

    # --- 2. Canonical label selection ---
    canonical_map = {}
    yaml_out = {}
    for cid, tags in clusters.items():
        tags = list(set(tags))
        tags_sorted = sorted(tags, key=lambda t: (len(t.split()), -tag_freq[t]))
        canonical = tags_sorted[0]
        aliases = [t for t in tags_sorted if t != canonical]
        canonical_map[canonical] = {"aliases": aliases, "cluster_id": cid}
        yaml_out[canonical] = {"aliases": aliases, "cluster_id": cid}

    # --- 3. Harvest tag-domain mappings from HLJs ---
    tag_domains_v1, tag_domains_v2 = defaultdict(set), defaultdict(set)
    for model in models:
        model_path = os.path.join(hlj_root, model)
        if not os.path.isdir(model_path):
            continue
        for req_id in os.listdir(model_path):
            req_path = os.path.join(model_path, req_id)
            chunk_file = os.path.join(req_path, "all_chunks_full_validated.json")
            if not os.path.exists(chunk_file):
                continue
            with open(chunk_file, "r", encoding="utf-8") as f:
                hlj_chunks = json.load(f)
            for chunk in hlj_chunks:
                hlj_domain = chunk.get("domain")
                for tag in chunk.get("tags_v1", []):
                    tag_domains_v1[tag].add(hlj_domain)
                for tag in chunk.get("tags_v2", []):
                    tag_domains_v2[tag].add(hlj_domain)

    tag_to_domains = {}
    all_tags = set(tag_domains_v1.keys()) | set(tag_domains_v2.keys())
    for tag in all_tags:
        union_domains = tag_domains_v1.get(tag, set()) | tag_domains_v2.get(tag, set())
        tag_to_domains[tag] = sorted([d for d in union_domains if d])

    # --- 4. Update canonical with domain info ---
    updated_map_with_domain = {}
    for canon, meta in canonical_map.items():
        updated_meta = dict(meta)
        updated_meta["domains"] = tag_to_domains.get(canon, [])
        updated_map_with_domain[canon] = updated_meta

    # --- 5. Write outputs ---
    with open(alias_json, "w", encoding="utf-8") as f:
        json.dump(canonical_map, f, indent=2, ensure_ascii=False)
    with open(canonical_yaml, "w", encoding="utf-8") as f:
        yaml.safe_dump(yaml_out, f, sort_keys=False, allow_unicode=True)
    with open(canonical_yaml_with_domain, "w", encoding="utf-8") as f:
        yaml.safe_dump(updated_map_with_domain, f, sort_keys=False, allow_unicode=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["tag", "domains"])
        for tag, domains in tag_to_domains.items():
            writer.writerow([tag, ", ".join(domains)])

    with open(log_path, "w", encoding="utf-8") as log:
        domain_counter, tag_counter = Counter(), Counter()
        for tag, domains in tag_to_domains.items():
            log.write(f"Tag: {tag:30} → Domains: {', '.join(domains)}\n")
            for d in domains:
                domain_counter[d] += 1
            tag_counter[tag] = len(domains)
        log.write("\nDomain coverage summary:\n")
        for d, count in domain_counter.items():
            log.write(f"  {d}: {count} tags\n")
        log.write(f"\nTotal tags with domains: {sum(1 for v in tag_to_domains.values() if v)}\n")
        log.write(f"Total tags with NO domain: {sum(1 for v in tag_to_domains.values() if not v)}\n")

    print(f"✅ Canonical tags saved to {canonical_yaml}")
    print(f"✅ Alias map saved to {alias_json}")
    print(f"✅ Enriched canonical tags with domains saved to {canonical_yaml_with_domain}")

    # --- 6. Update YAML ---
    cfg["outputs"]["canonical_tags"] = canonical_yaml
    cfg["outputs"]["tag_alias_map"] = alias_json
    save_config(cfg, cfg_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 4: Generate canonical tags + alias map + domain enrichment")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml")
    args = parser.parse_args()
    main(args.config)
