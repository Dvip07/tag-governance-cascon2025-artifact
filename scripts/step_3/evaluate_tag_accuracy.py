import os
import json
import csv
import yaml
from collections import defaultdict

def score_tagsets(gold, pred):
    if not gold and not pred:
        return (1.0, 1.0, 1.0, 1.0)
    if not pred or not gold:
        return (0.0, 0.0, 0.0, 0.0)
    precision = sum(1 for t in pred if t in gold) / len(pred) if pred else 0
    recall = sum(1 for t in gold if t in pred) / len(gold) if gold else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    jacc = len(set(pred) & set(gold)) / len(set(pred) | set(gold)) if (set(pred) | set(gold)) else 1.0
    return precision, recall, f1, jacc

def main(config_path):
    # --- Load pipeline config ---
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    run_dir = cfg["globals"]["run_dir"]
    gold_ver = cfg["step11"]["gold_version"]

    meta_dir = os.path.join(run_dir, "step_9", "hlj_tag_metadata")
    out_dir = os.path.join(run_dir, "step_11")
    os.makedirs(out_dir, exist_ok=True)

    out_csv = os.path.join(out_dir, "tag_eval_stats.csv")
    out_md = os.path.join(out_dir, "tag_eval_report.md")
    out_domain_csv = os.path.join(out_dir, "tag_eval_stats_by_domain.csv")

    rows = []
    per_model_stats = defaultdict(lambda: {"n":0,"prec2":0,"rec2":0,"f12":0,"jac2":0,
                                           "prec3":0,"rec3":0,"f13":0,"jac3":0})
    per_domain_stats = defaultdict(lambda: {"n":0,"prec2":0,"rec2":0,"f12":0,"jac2":0,
                                            "prec3":0,"rec3":0,"f13":0,"jac3":0})

    # --- Iterate HLJ metadata files ---
    for fname in os.listdir(meta_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(meta_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        hlj_id = meta["hlj_id"]
        req_id = meta.get("req_id", hlj_id.split("-")[0])
        model = meta.get("model", "unknown")
        domain = meta.get("domain", "unknown")

        v1_tags = set(meta.get("tags_v1", []))
        v2_tags = set(meta.get("tags_v2", []))
        v3_tags = set(meta.get("tags_v3", []))

        if gold_ver == "v1":
            gold = v1_tags
            p2,r2,f2,j2 = score_tagsets(gold, v2_tags)
            p3,r3,f3,j3 = score_tagsets(gold, v3_tags)
        elif gold_ver == "v2":
            gold = v2_tags
            p2,r2,f2,j2 = score_tagsets(gold, v1_tags)
            p3,r3,f3,j3 = score_tagsets(gold, v3_tags)
        elif gold_ver == "v3":
            gold = v3_tags
            p2,r2,f2,j2 = score_tagsets(gold, v1_tags)
            p3,r3,f3,j3 = score_tagsets(gold, v2_tags)
        else:
            raise ValueError("gold_version must be one of 'v1','v2','v3'")

        row = {
            "hlj_id": hlj_id, "req_id": req_id, "model": model, "domain": domain,
            "v1_tags": "|".join(sorted(v1_tags)),
            "v2_tags": "|".join(sorted(v2_tags)),
            "v3_tags": "|".join(sorted(v3_tags)),
            "precision_v2": p2, "recall_v2": r2, "f1_v2": f2, "jaccard_v2": j2,
            "precision_v3": p3, "recall_v3": r3, "f1_v3": f3, "jaccard_v3": j3,
        }
        rows.append(row)

        # --- Aggregations ---
        for target, p,r,f,j in [("2",p2,r2,f2,j2),("3",p3,r3,f3,j3)]:
            per_model_stats[model][f"prec{target}"] += p
            per_model_stats[model][f"rec{target}"]  += r
            per_model_stats[model][f"f1{target}"]   += f
            per_model_stats[model][f"jac{target}"]  += j
            per_model_stats[model]["n"] += 1

            per_domain_stats[domain][f"prec{target}"] += p
            per_domain_stats[domain][f"rec{target}"]  += r
            per_domain_stats[domain][f"f1{target}"]   += f
            per_domain_stats[domain][f"jac{target}"]  += j
            per_domain_stats[domain]["n"] += 1

    # --- Write CSVs ---
    with open(out_csv, "w", newline='', encoding="utf-8") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader(); writer.writerows(rows)

    with open(out_domain_csv, "w", newline='', encoding="utf-8") as f:
        fieldnames = ["domain","n","precision_v2","recall_v2","f1_v2","jaccard_v2",
                      "precision_v3","recall_v3","f1_v3","jaccard_v3"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d,stats in per_domain_stats.items():
            n=stats["n"]
            writer.writerow({
                "domain":d,"n":n,
                "precision_v2": stats["prec2"]/n if n else 0,
                "recall_v2":    stats["rec2"]/n if n else 0,
                "f1_v2":        stats["f12"]/n if n else 0,
                "jaccard_v2":   stats["jac2"]/n if n else 0,
                "precision_v3": stats["prec3"]/n if n else 0,
                "recall_v3":    stats["rec3"]/n if n else 0,
                "f1_v3":        stats["f13"]/n if n else 0,
                "jaccard_v3":   stats["jac3"]/n if n else 0,
            })

    # --- Markdown report ---
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(f"# Tag Accuracy Evaluation Report (GOLD: {gold_ver})\n\n")
        f.write("| Model | #HLJs | Prec@v2 | Recall@v2 | F1@v2 | Jac@v2 | Prec@v3 | Recall@v3 | F1@v3 | Jac@v3 |\n")
        f.write("|-------|-------|---------|-----------|-------|--------|---------|-----------|-------|--------|\n")
        for model, stats in per_model_stats.items():
            n = stats["n"]
            f.write(f"| {model} | {n} | "
                    f"{stats['prec2']/n if n else 0:.3f} | "
                    f"{stats['rec2']/n if n else 0:.3f} | "
                    f"{stats['f12']/n if n else 0:.3f} | "
                    f"{stats['jac2']/n if n else 0:.3f} | "
                    f"{stats['prec3']/n if n else 0:.3f} | "
                    f"{stats['rec3']/n if n else 0:.3f} | "
                    f"{stats['f13']/n if n else 0:.3f} | "
                    f"{stats['jac3']/n if n else 0:.3f} |\n")

        f.write("\n## Per-domain Analysis\n")
        f.write("| Domain | #HLJs | Prec@v2 | Recall@v2 | F1@v2 | Jac@v2 | Prec@v3 | Recall@v3 | F1@v3 | Jac@v3 |\n")
        f.write("|--------|-------|---------|-----------|-------|--------|---------|-----------|-------|--------|\n")
        for domain, stats in per_domain_stats.items():
            n = stats["n"]
            f.write(f"| {domain} | {n} | "
                    f"{stats['prec2']/n if n else 0:.3f} | "
                    f"{stats['rec2']/n if n else 0:.3f} | "
                    f"{stats['f12']/n if n else 0:.3f} | "
                    f"{stats['jac2']/n if n else 0:.3f} | "
                    f"{stats['prec3']/n if n else 0:.3f} | "
                    f"{stats['rec3']/n if n else 0:.3f} | "
                    f"{stats['f13']/n if n else 0:.3f} | "
                    f"{stats['jac3']/n if n else 0:.3f} |\n")

        f.write("\n## Error Cases (Low F1/Jaccard HLJs)\n")
        f.write("| HLJ | Model | Prec@v2 | Rec@v2 | F1@v2 | Jac@v2 | Prec@v3 | Rec@v3 | F1@v3 | Jac@v3 | v1 | v2 | v3 |\n")
        f.write("|-----|-------|---------|--------|-------|--------|---------|--------|-------|--------|----|----|----|\n")
        for row in rows:
            if (row["f1_v2"] < 0.5 or row["f1_v3"] < 0.5) or (row["jaccard_v2"] < 0.5 or row["jaccard_v3"] < 0.5):
                f.write(f"| {row['hlj_id']} | {row['model']} | "
                        f"{row['precision_v2']:.2f} | {row['recall_v2']:.2f} | {row['f1_v2']:.2f} | {row['jaccard_v2']:.2f} | "
                        f"{row['precision_v3']:.2f} | {row['recall_v3']:.2f} | {row['f1_v3']:.2f} | {row['jaccard_v3']:.2f} | "
                        f"{row['v1_tags']} | {row['v2_tags']} | {row['v3_tags']} |\n")

        f.write("\n_This report was auto-generated by evaluate_tag_accuracy.py_\n")

    print(f"✅ Evaluation complete\n  CSV: {out_csv}\n  Domain CSV: {out_domain_csv}\n  MD: {out_md}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to pipeline config YAML")
    args = parser.parse_args()
    main(args.config)
