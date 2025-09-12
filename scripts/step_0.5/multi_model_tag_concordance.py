import os
import json
import yaml
import csv
from collections import defaultdict, Counter
import numpy as np

try:
    from matplotlib_venn import venn3
    import matplotlib.pyplot as plt
    HAS_VENN = True
except ImportError:
    HAS_VENN = False

# ===== Config =====
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
OPUS4_YAML = os.path.join(ROOT_DIR, "output/meta_opus4.yaml")
META70B_YAML = os.path.join(ROOT_DIR, "output/meta_llama70b.yaml")
OUT_DIR = os.path.join(ROOT_DIR, "output/score")
os.makedirs(OUT_DIR, exist_ok=True)
VENN_TOP_N = 10
MODELS = ["gpt41", "opus4", "meta70b"]
GOLD_MODEL = "gpt41"

def load_yaml(yaml_path):
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)

def load_tags(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            obj = json.load(f)
            hlj_tags = {}
            for chunk in obj:
                for item in chunk.get("CURRENT_CHUNK", {}).get("DATA", []):
                    hlj_id = item["id"].lower()
                    tags = set([t.lower() for t in item.get("tags", [])])
                    hlj_tags[hlj_id] = tags
            return hlj_tags
    except Exception as e:
        print(f"Could not load {path}: {e}")
        return {}

# --- Load model YAML manifests ---
opus4_manifest = load_yaml(OPUS4_YAML)
meta70b_manifest = load_yaml(META70B_YAML)

# --- Build set of all req_ids across all manifests ---
all_req_ids = set([entry["req_id"].lower() for entry in opus4_manifest] +
                  [entry["req_id"].lower() for entry in meta70b_manifest])

# --- Map req_id -> model -> file path ---
req_model_paths = defaultdict(dict)
for entry in opus4_manifest:
    req = entry["req_id"].lower()
    req_model_paths[req]["gpt41"] = entry["gold_path"]
    req_model_paths[req]["opus4"] = entry["candidate_path"]
for entry in meta70b_manifest:
    req = entry["req_id"].lower()
    req_model_paths[req]["gpt41"] = entry["gold_path"]
    req_model_paths[req]["meta70b"] = entry["candidate_path"]

rows = []
missingness = []

# For macro PRF
prf_totals = {
    "opus4": {"prec": 0, "rec": 0, "f1": 0, "n": 0},
    "meta70b": {"prec": 0, "rec": 0, "f1": 0, "n": 0}
}

def tag_entropy(tagsets):
    all_tags = set().union(*tagsets)
    if not all_tags:
        return 0.0
    mat = np.zeros((len(tagsets), len(all_tags)))
    tag2idx = {t: i for i, t in enumerate(all_tags)}
    for i, tags in enumerate(tagsets):
        for t in tags:
            mat[i, tag2idx[t]] = 1
    entropies = []
    for j in range(mat.shape[1]):
        p = mat[:, j].sum() / mat.shape[0]
        if p == 0 or p == 1:
            entropies.append(0)
        else:
            entropies.append(-(p * np.log2(p) + (1-p)*np.log2(1-p)))
    return float(np.mean(entropies))

for req_id in sorted(all_req_ids):
    tags_by_model = {}
    present_models = []
    # Load HLJ dict for each model for this req
    for model in MODELS:
        path = req_model_paths[req_id].get(model)
        tags_by_model[model] = load_tags(path) if path and os.path.exists(path) else {}
        if tags_by_model[model]:
            present_models.append(model)
    all_hlj_ids = set().union(*[set(tags_by_model[m].keys()) for m in present_models])
    for hlj_id in sorted(all_hlj_ids):
        tags = {m: tags_by_model[m].get(hlj_id, set()) for m in MODELS}
        avail_models = [m for m in MODELS if tags[m]]
        missing_models = [m for m in MODELS if not tags[m]]
        union_tags = set().union(*tags.values())
        if avail_models:
            intersection_tags = set.intersection(*(tags[m] for m in avail_models))
        else:
            intersection_tags = set()
        tag_counts = Counter()
        for m in MODELS:
            for t in tags[m]:
                tag_counts[t] += 1
        majority_tags = set(t for t, c in tag_counts.items() if c >= 2)
        agreement_score = len(intersection_tags) / len(union_tags) if union_tags else 1.0
        disagreement_score = 1 - agreement_score
        entropy_val = tag_entropy([tags[m] for m in avail_models]) if union_tags else 0

        # Precision/Recall/F1 vs. GPT4.1
        prf_vals = {}
        for comp_model in ["opus4", "meta70b"]:
            if not tags[comp_model] or not tags[GOLD_MODEL]:
                prf = {"precision": "", "recall": "", "f1": ""}
            else:
                pred = tags[comp_model]
                gold = tags[GOLD_MODEL]
                tp = len(pred & gold)
                precision = tp / len(pred) if pred else 0
                recall = tp / len(gold) if gold else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
                prf = {"precision": precision, "recall": recall, "f1": f1}
                # For macro-average
                prf_totals[comp_model]["prec"] += precision
                prf_totals[comp_model]["rec"] += recall
                prf_totals[comp_model]["f1"]  += f1
                prf_totals[comp_model]["n"]   += 1
            prf_vals[comp_model] = prf

        row = {
            "req_id": req_id,
            "hlj_id": hlj_id,
            "present_models": "|".join(avail_models),
            "missing_models": "|".join(missing_models),
            "num_gpt41": len(tags["gpt41"]),
            "num_opus4": len(tags["opus4"]),
            "num_meta70b": len(tags["meta70b"]),
            "union_count": len(union_tags),
            "intersection_count": len(intersection_tags),
            "majority_count": len(majority_tags),
            "agreement_score": agreement_score,
            "disagreement_score": disagreement_score,
            "entropy": entropy_val,
            "stable_tags": "|".join(sorted(intersection_tags)),
            "majority_tags": "|".join(sorted(majority_tags)),
            "unique_gpt41": "|".join(sorted(tags["gpt41"] - tags["opus4"] - tags["meta70b"])),
            "unique_opus4": "|".join(sorted(tags["opus4"] - tags["gpt41"] - tags["meta70b"])),
            "unique_meta70b": "|".join(sorted(tags["meta70b"] - tags["gpt41"] - tags["opus4"])),
            "opus4_precision": prf_vals["opus4"]["precision"],
            "opus4_recall": prf_vals["opus4"]["recall"],
            "opus4_f1": prf_vals["opus4"]["f1"],
            "meta70b_precision": prf_vals["meta70b"]["precision"],
            "meta70b_recall": prf_vals["meta70b"]["recall"],
            "meta70b_f1": prf_vals["meta70b"]["f1"]
        }
        rows.append(row)
        for m in missing_models:
            missingness.append({
                "req_id": req_id,
                "hlj_id": hlj_id,
                "missing_model": m
            })

# --- Write CSV ---
if not rows:
    print("NO DATA FOUND! Check your YAML manifests and HLJ JSON file paths.")
    exit(1)

score_csv = os.path.join(OUT_DIR, "hlj_overlap_stats.csv")
with open(score_csv, "w", newline='', encoding="utf-8") as f:
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# --- Missingness CSV ---
missing_csv = os.path.join(OUT_DIR, "hlj_missingness.csv")
with open(missing_csv, "w", newline='', encoding="utf-8") as f:
    fieldnames = ["req_id", "hlj_id", "missing_model"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(missingness)

# --- Aggregate Stats (macro PRF) ---
aggregate = {
    "total_req_ids": len(all_req_ids),
    "total_hlj_items": len(rows),
    "num_all_models_agree": sum(1 for r in rows if r["agreement_score"] == 1.0),
    "num_full_disagreement": sum(1 for r in rows if r["agreement_score"] == 0.0),
    "avg_agreement": np.mean([r["agreement_score"] for r in rows]) if rows else 0,
    "avg_entropy": np.mean([r["entropy"] for r in rows]) if rows else 0,
    "opus4_macro_precision": prf_totals["opus4"]["prec"] / prf_totals["opus4"]["n"] if prf_totals["opus4"]["n"] else 0,
    "opus4_macro_recall": prf_totals["opus4"]["rec"] / prf_totals["opus4"]["n"] if prf_totals["opus4"]["n"] else 0,
    "opus4_macro_f1": prf_totals["opus4"]["f1"] / prf_totals["opus4"]["n"] if prf_totals["opus4"]["n"] else 0,
    "meta70b_macro_precision": prf_totals["meta70b"]["prec"] / prf_totals["meta70b"]["n"] if prf_totals["meta70b"]["n"] else 0,
    "meta70b_macro_recall": prf_totals["meta70b"]["rec"] / prf_totals["meta70b"]["n"] if prf_totals["meta70b"]["n"] else 0,
    "meta70b_macro_f1": prf_totals["meta70b"]["f1"] / prf_totals["meta70b"]["n"] if prf_totals["meta70b"]["n"] else 0,
}
agg_csv = os.path.join(OUT_DIR, "aggregate_agreement.csv")
with open(agg_csv, "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=aggregate.keys())
    writer.writeheader()
    writer.writerow(aggregate)

# --- Markdown Report (Top Disagreement/Entropy HLJs) ---
md_report = os.path.join(OUT_DIR, "hlj_overlap_report.md")
sorted_by_disagreement = sorted(rows, key=lambda r: -r["disagreement_score"])
top_disagreement = sorted_by_disagreement[:VENN_TOP_N]

def fmt(val):
    if val == "" or val is None:
        return ""
    return f"{val:.2f}"

with open(md_report, "w", encoding="utf-8") as f:
    f.write("# HLJ Overlap/Agreement Analysis\n\n")
    f.write("## Top HLJs by Disagreement\n\n")
    f.write("| req_id | hlj_id | present_models | agreement_score | entropy | opus4_prec | opus4_rec | opus4_f1 | meta70b_prec | meta70b_rec | meta70b_f1 | stable_tags | unique_gpt41 | unique_opus4 | unique_meta70b |\n")
    f.write("|--------|--------|----------------|----------------|---------|------------|-----------|----------|--------------|-------------|------------|-------------|--------------|--------------|----------------|\n")
    for row in top_disagreement:
        f.write(
            f"| {row['req_id']} | {row['hlj_id']} | {row['present_models']} | {fmt(row['agreement_score'])} | {fmt(row['entropy'])} | "
            f"{fmt(row['opus4_precision'])} | "
            f"{fmt(row['opus4_recall'])} | "
            f"{fmt(row['opus4_f1'])} | "
            f"{fmt(row['meta70b_precision'])} | "
            f"{fmt(row['meta70b_recall'])} | "
            f"{fmt(row['meta70b_f1'])} | "
            f"{row['stable_tags']} | {row['unique_gpt41']} | {row['unique_opus4']} | {row['unique_meta70b']} |\n"
        )
    f.write("\n## Aggregate Stats\n")
    for k, v in aggregate.items():
        f.write(f"- **{k}**: {v}\n")

# --- Venn Diagrams (optional) ---
if HAS_VENN:
    venn_dir = os.path.join(OUT_DIR, "venn_plots")
    os.makedirs(venn_dir, exist_ok=True)
    for row in top_disagreement:
        sets = [
            set(row["stable_tags"].split("|")) | set(row["unique_gpt41"].split("|")) if row["unique_gpt41"] else set(row["stable_tags"].split("|")),
            set(row["stable_tags"].split("|")) | set(row["unique_opus4"].split("|")) if row["unique_opus4"] else set(row["stable_tags"].split("|")),
            set(row["stable_tags"].split("|")) | set(row["unique_meta70b"].split("|")) if row["unique_meta70b"] else set(row["stable_tags"].split("|"))
        ]
        labels = ["gpt41", "opus4", "meta70b"]
        plt.figure(figsize=(6, 6))
        venn3(subsets=sets, set_labels=labels)
        plt.title(f"{row['req_id']} / {row['hlj_id']}")
        plt.tight_layout()
        plt.savefig(os.path.join(venn_dir, f"{row['req_id']}_{row['hlj_id']}_venn.png"))
        plt.close()

print(f"✅ HLJ overlap & PRF analysis complete. CSVs and markdown written to {OUT_DIR}")
if HAS_VENN:
    print(f"✅ Venn diagrams saved to {venn_dir}")
