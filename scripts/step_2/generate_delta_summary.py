import os
import argparse
import yaml
import pandas as pd
from collections import Counter
from datetime import datetime
from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run


def summarize_audits(cfg, base_path=None, out_dir=None):
    # Resolve paths from config
    base_path = base_path or cfg.get("globals.sbert_fix_base", "sbert_fix")
    out_dir = out_dir or cfg.get("outputs.delta_dir", "sbert_fix")

    run = get_current_run()
    # run_id = run["run_id"]
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    out_csv = os.path.join(out_dir, f"delta_summary_{run_id}_{ts}.csv")
    out_md = os.path.join(out_dir, f"delta_summary_{run_id}_{ts}.md")
    os.makedirs(out_dir, exist_ok=True)

    records = []

    for model in os.listdir(base_path):
        model_dir = os.path.join(base_path, model)
        if not os.path.isdir(model_dir):
            continue
        for req in os.listdir(model_dir):
            audit_path = os.path.join(model_dir, req, "tag_audit.yaml")
            if not os.path.exists(audit_path):
                continue
            with open(audit_path) as f:
                audits = yaml.safe_load(f) or []

            for audit in audits:
                orig = set(audit.get("original_tags", []))
                validated = set(audit.get("validated_tags", []))
                tags_added = validated - orig
                tags_dropped = orig - validated
                tags_kept = orig & validated

                details = audit.get("validation_details", [])
                reasons = [d.get("validation_status", "n/a") for d in details]
                sims = [d["similarity"] for d in details if d.get("similarity") is not None]

                records.append({
                    "model": model,
                    "requirement": req,
                    "hlj_id": audit.get("hlj_id", "unknown"),
                    "orig_tag_count": len(orig),
                    "validated_tag_count": len(validated),
                    "tags_added": list(tags_added),
                    "tags_dropped": list(tags_dropped),
                    "tags_kept": list(tags_kept),
                    "n_added": len(tags_added),
                    "n_dropped": len(tags_dropped),
                    "n_kept": len(tags_kept),
                    "reasons": reasons,
                    "avg_similarity": round(sum(sims)/len(sims), 3) if sims else None
                })

    df = pd.DataFrame(records)
    if df.empty:
        print("⚠️ No records found.")
        return

    summary_rows = []
    for model, group in df.groupby("model"):
        total = len(group)
        n_changed = (group["n_added"] + group["n_dropped"]).astype(bool).sum()
        percent_changed = 100 * n_changed / total if total else 0
        tags_added = Counter(tag for tags in group["tags_added"] for tag in tags)
        tags_dropped = Counter(tag for tags in group["tags_dropped"] for tag in tags)
        top_added = ", ".join([f"{t}({c})" for t, c in tags_added.most_common(3)])
        top_dropped = ", ".join([f"{t}({c})" for t, c in tags_dropped.most_common(3)])
        all_reasons = [r for reasons in group["reasons"] for r in reasons]
        top_reason = Counter(all_reasons).most_common(1)
        avg_sim_before = group["avg_similarity"].mean()
        summary_rows.append({
            "model": model,
            "total_hljs": total,
            "changed_hljs": n_changed,
            "% changed": round(percent_changed, 1),
            "tags_added": tags_added.total(),
            "tags_dropped": tags_dropped.total(),
            "top_added": top_added,
            "top_dropped": top_dropped,
            "top_reason": top_reason[0][0] if top_reason else "-",
            "avg_similarity": round(avg_sim_before, 3) if avg_sim_before else None,
        })

    # Save CSV
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(out_csv, index=False)
    print(f"✅ Delta summary table written to {out_csv}")

    # Save Markdown
    with open(out_md, "w") as f:
        f.write("| Model | HLJs | Changed | % Changed | Tags Added | Tags Dropped | Top Added | Top Dropped | Top Reason | Avg Sim |\n")
        f.write("|-------|------|---------|-----------|------------|--------------|-----------|-------------|------------|---------|\n")
        for row in summary_rows:
            f.write(f"| {row['model']} | {row['total_hljs']} | {row['changed_hljs']} | {row['% changed']} | "
                    f"{row['tags_added']} | {row['tags_dropped']} | {row['top_added']} | {row['top_dropped']} | "
                    f"{row['top_reason']} | {row['avg_similarity']} |\n")
    print(f"📝 Markdown summary written to {out_md}")

    # Update YAML for downstream steps
    cfg.set("outputs.delta_summary_csv", out_csv)
    cfg.set("outputs.delta_summary_md", out_md)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize audits into delta summary")
    parser.add_argument("--config", default="configs/pipeline_v1.yaml", help="Path to config YAML")
    parser.add_argument("--base", help="Override base path")
    parser.add_argument("--out_dir", help="Override output directory")
    args = parser.parse_args()

    cfg = ConfigResolver(args.config)
    run_id = get_current_run(args.config)
    summarize_audits(cfg, base_path=args.base, out_dir=args.out_dir)
