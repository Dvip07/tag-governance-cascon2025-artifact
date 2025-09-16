"""
Step 1 — Evaluation Heatmaps
----------------------------
Generates heatmaps from evaluation CSVs (semantic similarity, field-level F1, etc.)
using parameters defined in the versioned config YAML.
"""

import os, argparse, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from scripts.step_1.config_resolver import ConfigResolver

sns.set(style="whitegrid")
plt.switch_backend("Agg")   # safe for headless servers

# ========= Helpers =========
def ensure_dir(path): os.makedirs(path, exist_ok=True)

def plot_heatmap(csv_path, value_col, index_col, columns_col, out_path, title):
    if not os.path.exists(csv_path):
        print(f"[WARN] CSV not found: {csv_path}")
        return
    df = pd.read_csv(csv_path)

    if index_col not in df or columns_col not in df or value_col not in df:
        print(f"[WARN] Missing required cols in {csv_path}")
        return

    pivot = df.pivot(index=index_col, columns=columns_col, values=value_col)
    plt.figure(figsize=(12, max(6, int(pivot.shape[0]/2))))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=0.3)
    plt.title(title)
    plt.ylabel(index_col)
    plt.xlabel(columns_col)
    plt.tight_layout()

    ensure_dir(os.path.dirname(out_path))
    plt.savefig(out_path)
    plt.close()
    print(f"✅ Saved heatmap: {out_path}")


# ========= Main =========
def main(cfg_path="configs/pipeline_v0.yaml"):
    cfg = ConfigResolver(cfg_path)

    plots = cfg.get("eval_heatmaps.plots", [])
    if not plots:
        print("[WARN] No heatmap plots defined in config.")
        return

    for spec in plots:
        try:
            plot_heatmap(
                csv_path=spec["csv_path"],
                value_col=spec["value_col"],
                index_col=spec["index_col"],
                columns_col=spec["columns_col"],
                out_path=spec["out_path"],
                title=spec["title"],
            )
        except Exception as e:
            print(f"[WARN] Skipped plot {spec}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pipeline_v0.yaml")
    args = parser.parse_args()
    main(args.config)
