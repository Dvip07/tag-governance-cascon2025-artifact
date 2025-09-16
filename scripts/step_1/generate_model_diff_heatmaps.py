"""
Step 1 — Generate Model Diff Heatmaps
-------------------------------------
Plots heatmaps comparing model similarity scores vs a baseline model.
Also outputs leaderboards and bar charts.

All paths, models, and plotting options are loaded from a versioned config YAML.
"""

import os, argparse, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from scripts.step_1.config_resolver import ConfigResolver

sns.set(style="whitegrid")
plt.switch_backend("Agg")   # safe for headless environments

# ========= Helpers =========
def ensure_dir(p): os.makedirs(p, exist_ok=True)

def plot_model_diff_heatmap(df, value_col, index_col, columns_col,
                            baseline_model, out_path, title, aliases=None):
    """
    Create diff heatmaps + leaderboard plots for model comparison.
    """
    if index_col not in df or columns_col not in df or value_col not in df:
        print(f"[WARN] Missing required cols: {index_col}, {columns_col}, {value_col}")
        return

    pivot = df.pivot_table(
    index=index_col,
    columns=columns_col,
    values=value_col,
    aggfunc="mean"   # average similarity if duplicates exist
)

    models = sorted(pivot.columns)
    if len(models) < 2:
        print("[WARN] Need >=2 models to diff.")
        return

    # Normalize baseline
    if aliases and baseline_model in aliases:
        baseline_model = aliases[baseline_model]
    if baseline_model not in models:
        baseline_model = models[0]
        print(f"[INFO] Baseline not in data, falling back to {baseline_model}")

    # Leaderboard
    leaderboard = pivot.mean().sort_values(ascending=False)
    leaderboard.to_csv(out_path.replace(".png", "_leaderboard.csv"))

    plt.figure(figsize=(8, 4))
    sns.barplot(x=leaderboard.index, y=leaderboard.values)
    plt.title(f"Leaderboard by mean({value_col})")
    plt.tight_layout()
    plt.savefig(out_path.replace(".png", "_leaderboard.png"))
    plt.close()

    # Pairwise diffs vs baseline
    for m in models:
        if m == baseline_model: continue
        diff = pivot[m] - pivot[baseline_model]
        plt.figure(figsize=(12, 4))
        sns.heatmap(diff.to_frame().T, annot=True, cmap="coolwarm", center=0)
        plt.title(f"{title}: {m} vs {baseline_model}")
        plt.tight_layout()
        plt.savefig(out_path.replace(".png", f"_{m}_vs_{baseline_model}.png"))
        plt.close()


# ========= Main =========
def main(cfg_path="configs/pipeline_v0.yaml"):
    cfg = ConfigResolver(cfg_path)

    csv_path    = cfg.get("semantic_eval.csv_out")
    plots_dir   = cfg.get("plots.plots_dir")
    baseline    = cfg.get("models.baseline")
    value_col   = cfg.get("plots.value_col")
    index_col   = cfg.get("plots.index_col")
    columns_col = cfg.get("plots.columns_col")
    title       = cfg.get("plots.title")
    aliases     = cfg.get("plots.aliases", {})

    ensure_dir(plots_dir)

    if not os.path.exists(csv_path):
        print(f"[WARN] Missing CSV: {csv_path}")
        return

    df = pd.read_csv(csv_path)
    out_path = os.path.join(plots_dir, "model_diff_semantic_similarity.png")

    plot_model_diff_heatmap(
        df, value_col, index_col, columns_col,
        baseline_model=baseline,
        out_path=out_path,
        title=title,
        aliases=aliases
    )

    print(f"✅ Plots written to {plots_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pipeline_v0.yaml")
    args = parser.parse_args()
    main(args.config)
