import os
import pandas as pd
from glob import glob
import argparse
from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run  # ✅ use current run

def get_run_date_from_filename(fname: str) -> str:
    base = os.path.basename(fname)
    if base.startswith("delta_summary_"):
        return base[len("delta_summary_") : -4]  # strip prefix and ".csv"
    return base


def aggregate_trends(cfg, delta_dir=None, out_csv=None, out_md=None):
    delta_dir = delta_dir or cfg.get("outputs.delta_dir") or "eval/runs/delta_summaries"

    out_csv = out_csv or cfg.get("outputs.trends_csv") or os.path.join(delta_dir, "change_trend_table.csv")
    out_md  = out_md  or cfg.get("outputs.trends_md")  or os.path.join(delta_dir, "change_trend_table.md")

    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    # os.makedirs(os.path.dirname(out_md), exist_ok=True)

    # Find all delta summaries from all runs
    trend_files = sorted(glob(os.path.join(delta_dir, "delta_summary_*.csv")))
    if not trend_files:
        print(f"⚠️ No delta summary files found under {delta_dir}")
        return

    records = []
    for f in trend_files:
        run_date = get_run_date_from_filename(f)
        df = pd.read_csv(f)
        df["run_date"] = run_date
        records.append(df)

    all_trends = pd.concat(records, ignore_index=True)

    # Build per-model trend summary (flatten all runs)
    summary = []
    for _, row in all_trends.iterrows():
        summary.append({
            "run_date": row["run_date"],
            "model": row["model"],
            "hljs": row["total_hljs"],
            "changed": row["changed_hljs"],
            "% changed": row["% changed"],
            "tags_added": row["tags_added"],
            "tags_dropped": row["tags_dropped"],
            "top_added": row["top_added"],
            "top_dropped": row["top_dropped"],
            "top_reason": row["top_reason"],
            "avg_similarity": row["avg_similarity"]
        })

    trend_df = pd.DataFrame(summary).sort_values(["model", "run_date"])

    # Write CSV
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    trend_df.to_csv(out_csv, index=False)
    print(f"✅ Trend table written to {out_csv}")

    # Write Markdown
    with open(out_md, "w") as f:
        f.write("| Date | Model | HLJs | Changed | % Changed | Tags Added | Tags Dropped | Top Added | Top Dropped | Top Reason | Avg Sim |\n")
        f.write("|------|-------|------|---------|-----------|------------|--------------|-----------|-------------|------------|---------|\n")
        for _, row in trend_df.iterrows():
            f.write(f"| {row['run_date']} | {row['model']} | {row['hljs']} | {row['changed']} | {row['% changed']} | "
                    f"{row['tags_added']} | {row['tags_dropped']} | {row['top_added']} | {row['top_dropped']} | "
                    f"{row['top_reason']} | {row['avg_similarity']} |\n")
    print(f"✅ Trend table (Markdown) written to {out_md}")

    # Update config so downstream knows where results live
    cfg.set("outputs.trends_csv", out_csv)
    cfg.set("outputs.trends_md", out_md)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate trends across multiple runs")
    parser.add_argument("--config", default="configs/pipeline_v1.yaml", help="Path to config YAML")
    parser.add_argument("--dir", help="Override delta summaries directory")
    parser.add_argument("--out_csv", help="Override CSV output path")
    parser.add_argument("--out_md", help="Override Markdown output path")
    args = parser.parse_args()

    cfg = ConfigResolver(args.config)
    run = get_current_run(args.config)  # ✅ no new run, attach to existing one
    aggregate_trends(cfg, delta_dir=args.dir, out_csv=args.out_csv, out_md=args.out_md)
