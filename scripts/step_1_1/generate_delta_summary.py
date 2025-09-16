import os
import yaml
import pandas as pd
from collections import Counter

# Paths
SBERT_FIX_BASE = "sbert_fix"
OUTPUT_CSV = "sbert_fix/delta_summary.csv"
OUTPUT_MD = "sbert_fix/delta_summary.md"

def summarize_audits():
    records = []

    for model in os.listdir(SBERT_FIX_BASE):
        model_dir = os.path.join(SBERT_FIX_BASE, model)
        if not os.path.isdir(model_dir):
            continue
        for req in os.listdir(model_dir):
            req_dir = os.path.join(model_dir, req)
            audit_path = os.path.join(req_dir, "tag_audit.yaml")
            if not os.path.exists(audit_path):
                continue
            with open(audit_path) as f:
                audits = yaml.safe_load(f)

            for audit in audits:
                orig = set(audit.get("original_tags", []))
                validated = set(audit.get("validated_tags", []))
                tags_added = validated - orig
                tags_dropped = orig - validated
                tags_kept = orig & validated

                # updated: changed tag_results → validation_details
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

    # === Summary logic stays the same ===
    df = pd.DataFrame(records)
    if df.empty:
        print("No records found.")
        return

    model_groups = df.groupby("model")
    summary_rows = []
    for model, group in model_groups:
        total = len(group)
        n_changed = (group['n_added'] + group['n_dropped']).astype(bool).sum()
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

    # CSV
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Delta summary table written to `{OUTPUT_CSV}`")

    # Markdown
    with open(OUTPUT_MD, "w") as f:
        f.write("| Model | HLJs | Changed | % Changed | Tags Added | Tags Dropped | Top Added | Top Dropped | Top Reason | Avg Sim |\n")
        f.write("|-------|------|---------|-----------|------------|--------------|-----------|-------------|------------|---------|\n")
        for row in summary_rows:
            f.write(f"| {row['model']} | {row['total_hljs']} | {row['changed_hljs']} | {row['% changed']} | "
                    f"{row['tags_added']} | {row['tags_dropped']} | {row['top_added']} | {row['top_dropped']} | "
                    f"{row['top_reason']} | {row['avg_similarity']} |\n")
    print(f"📝 Markdown summary written to `{OUTPUT_MD}`")

if __name__ == "__main__":
    summarize_audits()
