import os
import argparse
import yaml
import pandas as pd
from datetime import datetime

from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run


def collect_flagged_cases(cfg, top_n=20, base_path=None, out_csv=None, out_md=None):
    # Resolve paths from YAML or args
    base_path = base_path or cfg.get("globals.sbert_fix_base", "sbert_fix")
    
    run_dir = cfg.get("globals.run_dir")
    if not run_dir:
        raise RuntimeError("⚠️ run_dir not set — did you forget init_run()?")
    
    out_csv = out_csv or os.path.join(run_dir, f"flagged_cases_{datetime.now().date()}.csv")
    out_md  = out_md  or os.path.join(run_dir, f"flagged_cases_{datetime.now().date()}.md")

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
                num_changes = len(tags_added) + len(tags_dropped)
                reasons = [t.get("validation_status") for t in audit.get("validation_details", [])]
                most_common_reason = max(set(reasons), key=reasons.count) if reasons else "-"
                records.append({
                    "model": model,
                    "requirement": req,
                    "hlj_id": audit.get("hlj_id", "unknown"),
                    "tags_added": list(tags_added),
                    "tags_dropped": list(tags_dropped),
                    "num_tags_added": len(tags_added),
                    "num_tags_dropped": len(tags_dropped),
                    "total_tag_changes": num_changes,
                    "top_reason": most_common_reason
                })

    if not records:
        print("No flagged cases found.")
        return

    df = pd.DataFrame(records)
    flagged = df.sort_values(['total_tag_changes'], ascending=False).groupby('model').head(top_n)

    # Write CSV
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    flagged.to_csv(out_csv, index=False)
    print(f"✅ Flagged cases table written to {out_csv}")

    # Write Markdown
    with open(out_md, "w") as f:
        f.write("| Model | Requirement | HLJ ID | # Tags Added | # Tags Dropped | Total Tag Changes | Top Reason | Tags Added | Tags Dropped |\n")
        f.write("|-------|-------------|--------|--------------|----------------|-------------------|------------|------------|--------------|\n")
        for _, row in flagged.iterrows():
            f.write(f"| {row['model']} | {row['requirement']} | {row['hlj_id']} | "
                    f"{row['num_tags_added']} | {row['num_tags_dropped']} | {row['total_tag_changes']} | "
                    f"{row['top_reason']} | {', '.join(row['tags_added'])} | {', '.join(row['tags_dropped'])} |\n")
    print(f"✅ Flagged cases table (Markdown) written to {out_md}")

    # Update YAML with the paths for this run
    cfg.update("outputs.flagged_csv", out_csv)
    cfg.update("outputs.flagged_md", out_md)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect flagged cases from audits")
    parser.add_argument("--config", default="configs/pipeline_v1.yaml", help="Path to config YAML")
    parser.add_argument("--top_n", type=int, default=20, help="Top N HLJs per model")
    parser.add_argument("--base", help="Override base path to audits")
    parser.add_argument("--out_csv", help="Override CSV output path")
    parser.add_argument("--out_md", help="Override Markdown output path")
    args = parser.parse_args()

    cfg = ConfigResolver(args.config)
    run_id = get_current_run("configs/pipeline_v1.yaml")
    collect_flagged_cases(cfg, top_n=args.top_n, base_path=args.base, out_csv=args.out_csv, out_md=args.out_md)
