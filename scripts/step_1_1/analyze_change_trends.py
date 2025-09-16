import os
import pandas as pd
from glob import glob
from datetime import datetime

# Paths
TRENDS_DIR = "sbert_fix/"
OUTPUT_TREND_CSV = "sbert_fix/change_trend_table.csv"
OUTPUT_TREND_MD = "sbert_fix/change_trend_table.md"

def get_run_date_from_filename(fname):
    # Expect filenames like: delta_summary_2024-06-01.csv
    # Adjust as per your naming!
    base = os.path.basename(fname)
    date_part = base.replace("delta_summary_", "").replace(".csv", "")
    return date_part

def aggregate_trends():
    trend_files = sorted(glob(os.path.join(TRENDS_DIR, "delta_summary_*.csv")))
    if not trend_files:
        print("No trend files found.")
        return

    records = []
    for f in trend_files:
        run_date = get_run_date_from_filename(f)
        df = pd.read_csv(f)
        df["run_date"] = run_date
        records.append(df)

    all_trends = pd.concat(records, ignore_index=True)

    # Let's assume you want trends per model
    summary = []
    models = all_trends["model"].unique()
    for model in models:
        dfm = all_trends[all_trends["model"] == model]
        for _, row in dfm.iterrows():
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

    trend_df = pd.DataFrame(summary)
    trend_df = trend_df.sort_values(["model", "run_date"])

    # Write to CSV
    trend_df.to_csv(OUTPUT_TREND_CSV, index=False)
    print(f"Trend table written to {OUTPUT_TREND_CSV}")

    # Write Markdown (ready for paper)
    with open(OUTPUT_TREND_MD, "w") as f:
        f.write("| Date | Model | HLJs | Changed | % Changed | Tags Added | Tags Dropped | Top Added | Top Dropped | Top Reason | Avg Sim |\n")
        f.write("|------|-------|------|---------|-----------|------------|--------------|-----------|-------------|------------|---------|\n")
        for _, row in trend_df.iterrows():
            f.write(f"| {row['run_date']} | {row['model']} | {row['hljs']} | {row['changed']} | {row['% changed']} | "
                    f"{row['tags_added']} | {row['tags_dropped']} | {row['top_added']} | {row['top_dropped']} | "
                    f"{row['top_reason']} | {row['avg_similarity']} |\n")
    print(f"Trend table (Markdown) written to {OUTPUT_TREND_MD}")

if __name__ == "__main__":
    aggregate_trends()
