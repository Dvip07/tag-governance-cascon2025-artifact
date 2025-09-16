import os
import csv
import math
from statistics import median
from sentence_transformers import SentenceTransformer, util
import argparse
import yaml
from datetime import datetime

# === Config helpers ===
def load_config(cfg_path):
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(cfg, cfg_path):
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

def ensure_run(cfg, cfg_path):
    """Ensure we have a valid run_id/run_dir."""
    run_id = cfg.get("globals", {}).get("run_id")
    run_dir = cfg.get("globals", {}).get("run_dir")

    if not run_id or not run_dir:
        raise RuntimeError("⚠️ No run_id/run_dir found. Did you run Step 1 first?")

    return run_id, run_dir

# === Helpers ===
def get_token_length(tag):
    return len(tag.strip().split())

def get_domain_from_req_id(req_id, raw_req_base):
    for domain in ["FinTech", "SaaS"]:
        req_path = os.path.join(raw_req_base, domain, f"{req_id}.md")
        if os.path.exists(req_path):
            return domain
    return None

def load_raw_requirement(req_id, raw_req_base):
    domain = get_domain_from_req_id(req_id, raw_req_base)
    if not domain:
        return ""
    path = os.path.join(raw_req_base, domain, f"{req_id}.md")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def keyword_match(tag, text):
    return tag.lower() in text.lower()

def save_csv(path, data):
    if not data:
        print(f"⚠️ No data to write to {path}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

# === Main ===
def main(cfg_path):
    cfg = load_config(cfg_path)
    run_id, run_dir = ensure_run(cfg, cfg_path)

    # Inputs
    step1_csv = cfg["outputs"].get("tags_all")
    if not step1_csv or not os.path.exists(step1_csv):
        raise FileNotFoundError("❌ Step 1 output not found. Did you run harvest_tags.py?")

    raw_req_base = cfg["globals"].get("raw_req_base", "raw_requirement")

    # Parameters
    sbert_model = cfg.get("step2", {}).get("sbert_model", "all-MiniLM-L6-v2")
    th_strong = cfg.get("step2", {}).get("sbert_threshold_strong", 0.40)
    th_weak = cfg.get("step2", {}).get("sbert_threshold_weak", 0.20)

    # Outputs
    out_dir = os.path.join(run_dir, "step_2")
    os.makedirs(out_dir, exist_ok=True)
    out_all = os.path.join(out_dir, "final_tags.csv")
    out_filtered = os.path.join(out_dir, "filtered_tags.csv")
    out_rescued = os.path.join(out_dir, "rescued_tags.csv")
    out_dropped = os.path.join(out_dir, "dropped_tags.csv")

    # === Process ===
    print("🔎 Loading SBERT model...")
    sbert = SentenceTransformer(sbert_model)

    rows, token_lengths = [], []
    with open(step1_csv, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag = row['tag']
            tlen = get_token_length(tag)
            row['token_length'] = tlen
            token_lengths.append(tlen)
            rows.append(row)

    med = math.ceil(median(token_lengths))
    print(f"📏 Median token length: {med}")

    final_rows, filtered_rows, rescued_rows, dropped_rows = [], [], [], []
    req_cache = {}

    for row in rows:
        tag = row['tag']
        req_id = row['requirement_id']
        tlen = int(row['token_length'])
        flagged = row.get("flagged", "").lower() == "yes"
        inferred = row.get("inferred", "").lower() == "yes"

        needs_check = flagged or inferred or tlen > med
        row['rescue_score'] = ''
        row['rescue_notes'] = ''
        row['filtered'] = 'N'
        row['filter_reason'] = 'passed_all_filters'

        if not needs_check:
            final_rows.append(row)
            continue

        if req_id not in req_cache:
            req_text = load_raw_requirement(req_id, raw_req_base)
            req_cache[req_id] = req_text
        else:
            req_text = req_cache[req_id]

        if not req_text.strip():
            row['filtered'] = 'Y'
            row['filter_reason'] = 'suspicious_and_no_raw_requirement'
            filtered_rows.append(row)
            dropped_rows.append(row)
            print(f"🗑️ Dropped: '{tag}' for {req_id} | Reason: suspicious_and_no_raw_requirement")
            continue

        try:
            tag_emb = sbert.encode(tag, convert_to_tensor=True)
            req_emb = sbert.encode(req_text, convert_to_tensor=True)
            sim = util.cos_sim(tag_emb, req_emb).item()
            row['rescue_score'] = f"{sim:.3f}"
        except Exception as e:
            row['filtered'] = 'Y'
            row['filter_reason'] = 'sbert_encoding_failed'
            filtered_rows.append(row)
            dropped_rows.append(row)
            print(f"❌ SBERT failed on tag '{tag}' or req '{req_id}': {e}")
            continue

        if sim >= th_strong:
            row['filtered'] = 'N'
            row['filter_reason'] = 'rescued_by_strong_semantic_match'
            row['rescue_notes'] = 'strong semantic match with raw requirement'
            rescued_rows.append(row)
        elif sim >= th_weak:
            row['filtered'] = 'N'
            row['filter_reason'] = 'rescued_by_weak_semantic_match'
            row['rescue_notes'] = 'weak semantic match — low confidence'
            rescued_rows.append(row)
        elif keyword_match(tag, req_text):
            row['filtered'] = 'N'
            row['filter_reason'] = 'rescued_by_keyword_match'
            row['rescue_notes'] = 'tag appears in raw requirement text'
            rescued_rows.append(row)
        else:
            row['filtered'] = 'Y'
            row['filter_reason'] = f'suspicious_and_no_semantic_match:{sim:.3f}'
            dropped_rows.append(row)
            print(f"🗑️ Dropped: '{tag}' for {req_id} | Reason: suspicious_and_no_semantic_match:{sim:.3f}")

        final_rows.append(row)

    # === Save outputs ===
    save_csv(out_all, final_rows)
    save_csv(out_filtered, filtered_rows)
    save_csv(out_rescued, rescued_rows)
    save_csv(out_dropped, dropped_rows)

    print("✅ Step 2 complete. Outputs:")
    print(f"  - Full log:        {out_all} ({len(final_rows)} rows)")
    print(f"  - Filtered tags:   {out_filtered} ({len(filtered_rows)} rows)")
    print(f"  - Rescued tags:    {out_rescued} ({len(rescued_rows)} rows)")
    print(f"  - Dropped tags:    {out_dropped} ({len(dropped_rows)} rows)")

    # === Update YAML ===
    cfg["outputs"]["tags_token_filtered"] = out_filtered
    cfg["outputs"]["step2_all"] = out_all
    cfg["outputs"]["step2_rescued"] = out_rescued
    cfg["outputs"]["step2_dropped"] = out_dropped
    save_config(cfg, cfg_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 2: Filter tags by token length + semantic check")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml")
    args = parser.parse_args()
    main(args.config)
