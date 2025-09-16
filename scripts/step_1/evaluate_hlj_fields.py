"""
Step 1 — Field-Level HLJ Evaluation (Config-Driven)
---------------------------------------------------
Compares gold vs candidate HLJ fields, computes precision/recall/F1,
and saves results to both CSV and Markdown.

Config:
  field_eval:
    meta_yaml: "eval/output/meta_llama70b.yaml"
    out_csv:   "eval/metrics/field_eval.csv"
    out_md:    "eval/metrics/field_eval.md"
"""

# ========= Imports =========
import os
import argparse
import yaml
import json
import pandas as pd
from collections import defaultdict
from scripts.utils.config_loader import load_config



# ========= Config Loader =========
def load_config(cfg_path="configs/pipeline_v0.yaml"):
    return load_config(cfg_path)


# ========= Helpers =========
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_all_hljs_from_chunks(chunk_list):
    """Extract all HLJ items from CURRENT_CHUNK->DATA lists (robust to wrappers)."""
    all_hljs = []
    for chunk in chunk_list:
        try:
            data_items = chunk.get("CURRENT_CHUNK", {}).get("DATA", [])
            all_hljs.extend(data_items)
        except Exception as e:
            print(f"Error extracting HLJs from chunk: {e}")
    return all_hljs


# ========= Core Evaluation =========
def evaluate(meta_yaml, fields):
    """Compare HLJ fields between gold and candidate outputs."""
    with open(meta_yaml, "r", encoding="utf-8") as f:
        meta = yaml.safe_load(f)

    field_scores = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0, "gold": [], "cand": []})

    for pair in meta:
        gold = load_json(pair["gold_path"])
        cand = load_json(pair["candidate_path"])
        gold_hljs = extract_all_hljs_from_chunks(gold)
        cand_hljs = extract_all_hljs_from_chunks(cand)

        gold_map = {h["id"]: h for h in gold_hljs}
        cand_map = {h["id"]: h for h in cand_hljs}
        all_ids = set(gold_map) | set(cand_map)

        for hlj_id in all_ids:
            g, c = gold_map.get(hlj_id), cand_map.get(hlj_id)
            for field in fields:
                if g is None:
                    field_scores[field]["fp"] += 1
                elif c is None:
                    field_scores[field]["fn"] += 1
                else:
                    g_val, c_val = g.get(field), c.get(field)
                    if isinstance(g_val, list) and isinstance(c_val, list):
                        gold_set, cand_set = set(g_val), set(c_val)
                        tp = len(gold_set & cand_set)
                        fp = len(cand_set - gold_set)
                        fn = len(gold_set - cand_set)
                        field_scores[field]["tp"] += tp
                        field_scores[field]["fp"] += fp
                        field_scores[field]["fn"] += fn
                        field_scores[field]["gold"].extend(gold_set)
                        field_scores[field]["cand"].extend(cand_set)
                    else:
                        match = g_val == c_val
                        field_scores[field]["tp"] += int(match)
                        field_scores[field]["fp"] += int(not match)
                        field_scores[field]["fn"] += int(not match)
                        field_scores[field]["gold"].append(g_val)
                        field_scores[field]["cand"].append(c_val)

    return field_scores

# ========= Main =========
def main(cfg_path="configs/pipeline_v0.yaml"):
    cfg = load_config(cfg_path)
    eval_cfg = cfg["field_eval"]

    meta_yaml = eval_cfg["meta_yaml"]
    out_csv   = eval_cfg["out_csv"]
    out_md    = eval_cfg["out_md"]

    # 👇 NEW: pull fields list from config (fallback to default)
    fields = eval_cfg.get("fields", ["title", "difficulty", "priority", "tags"])

    # Run evaluation
    field_scores = evaluate(meta_yaml, fields)

    # Build results dataframe
    rows = []
    for field, scores in field_scores.items():
        tp, fp, fn = scores["tp"], scores["fp"], scores["fn"]
        precision = tp / (tp + fp) if (tp + fp) else 0
        recall    = tp / (tp + fn) if (tp + fn) else 0
        f1        = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
        rows.append({
            "field": field,
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1": round(f1, 3),
            "tp": tp,
            "fp": fp,
            "fn": fn,
        })

    df = pd.DataFrame(rows)

    # Ensure output dir exists
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    # Save CSV
    df.to_csv(out_csv, index=False)
    print(f"✅ Saved CSV metrics: {out_csv}")

    # Save Markdown
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("| Field | Precision | Recall | F1 | TP | FP | FN |\n")
        f.write("|-------|-----------|--------|----|----|----|----|\n")
        for _, row in df.iterrows():
            f.write(
                f"| {row['field']} | {row['precision']:.3f} | {row['recall']:.3f} "
                f"| {row['f1']:.3f} | {int(row['tp'])} | {int(row['fp'])} | {int(row['fn'])} |\n"
            )
    print(f"✅ Saved Markdown metrics: {out_md}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pipeline_v0.yaml")
    args = parser.parse_args()
    main(args.config)
