import os
import yaml
import pandas as pd

SBERT_FIX_BASE = "sbert_fix"
OUTPUT_FLAGGED_CSV = "sbert_fix/flagged_cases.csv"
OUTPUT_FLAGGED_MD = "sbert_fix/flagged_cases.md"

def collect_flagged_cases(top_n=20):
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
                num_changes = len(tags_added) + len(tags_dropped)
                reasons = [t["validation_status"] for t in audit["validation_details"]]
                most_common_reason = max(set(reasons), key=reasons.count) if reasons else "-"
                records.append({
                    "model": model,
                    "requirement": req,
                    "hlj_id": audit["hlj_id"],
                    "tags_added": list(tags_added),
                    "tags_dropped": list(tags_dropped),
                    "num_tags_added": len(tags_added),
                    "num_tags_dropped": len(tags_dropped),
                    "total_tag_changes": num_changes,
                    "top_reason": most_common_reason
                })

    # Find top changed HLJs per model
    df = pd.DataFrame(records)
    if df.empty:
        print("No flagged cases found.")
        return

    flagged = df.sort_values(['total_tag_changes'], ascending=False).groupby('model').head(top_n)
    flagged.to_csv(OUTPUT_FLAGGED_CSV, index=False)
    print(f"Flagged cases table written to {OUTPUT_FLAGGED_CSV}")

    # Write as Markdown
    with open(OUTPUT_FLAGGED_MD, "w") as f:
        f.write("| Model | Requirement | HLJ ID | # Tags Added | # Tags Dropped | Total Tag Changes | Top Reason | Tags Added | Tags Dropped |\n")
        f.write("|-------|-------------|--------|--------------|----------------|-------------------|------------|------------|--------------|\n")
        for _, row in flagged.iterrows():
            f.write(f"| {row['model']} | {row['requirement']} | {row['hlj_id']} | "
                    f"{row['num_tags_added']} | {row['num_tags_dropped']} | {row['total_tag_changes']} | "
                    f"{row['top_reason']} | {', '.join(row['tags_added'])} | {', '.join(row['tags_dropped'])} |\n")
    print(f"Flagged cases table (Markdown) written to {OUTPUT_FLAGGED_MD}")

if __name__ == "__main__":
    collect_flagged_cases()
