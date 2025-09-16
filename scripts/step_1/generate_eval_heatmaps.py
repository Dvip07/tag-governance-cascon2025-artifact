"""
Step 1 — Generate Evaluation Heatmaps (Config-Driven)
-----------------------------------------------------
Creates annotated heatmaps from CSV evaluation results.

Two common use cases:
  1) Semantic similarity heatmap
  2) Field-level F1 heatmap

All paths, CSVs, and plotting parameters are configured
via a versioned YAML (e.g., configs/pipeline_v0.yaml).
"""

# ========= Imports =========
import os
import argparse
import yaml
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scripts.utils.config_loader import load_config



# ========= Config Loader =========
# def load_config(cfg_path: str):
#     return load_config(cfg_path)


# ========= Helpers =========
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def plot_heatmap(csv_path, value_col, index_col, columns_col, out_path, title):
    """Generate and save a heatmap from a CSV table."""
    if not os.path.exists(csv_path):
        print(f"[WARN] CSV not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    if not set([value_col, index_col, columns_col]).issubset(df.columns):
        print(f"[WARN] Missing required columns in {csv_path}")
        return

    pivot = df.pivot_table(
    index=index_col,
    columns=columns_col,
    values=value_col,
    aggfunc="mean"
)

    plt.figure(figsize=(12, max(6, int(pivot.shape[0] / 2))))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=0.3)
    plt.title(title)
    plt.ylabel(index_col)
    plt.xlabel(columns_col)
    plt.tight_layout()

    ensure_dir(os.path.dirname(out_path))
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"[OK] Saved heatmap: {out_path}")


# ========= Main =========
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pipeline_v0.yaml",
                        help="Path to pipeline config (YAML).")
    args = parser.parse_args()

    cfg = load_config(args.config)
    plots_cfg = cfg.get("eval_heatmaps", {})

    for plot in plots_cfg.get("plots", []):
        try:
            plot_heatmap(
                csv_path=plot["csv_path"],
                value_col=plot["value_col"],
                index_col=plot["index_col"],
                columns_col=plot["columns_col"],
                out_path=plot["out_path"],
                title=plot["title"],
            )
        except Exception as e:
            print(f"[WARN] Skipped {plot['title']}: {e}")


if __name__ == "__main__":
    main()
