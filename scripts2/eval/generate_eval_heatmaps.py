import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_heatmap(csv_path, value_col, index_col, columns_col, out_path, title):
    df = pd.read_csv(csv_path)
    pivot = df.pivot(index=index_col, columns=columns_col, values=value_col)
    plt.figure(figsize=(12, max(6, int(pivot.shape[0]/2))))
    ax = sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=0.3)
    plt.title(title)
    plt.ylabel(index_col)
    plt.xlabel(columns_col)
    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close()
    print(f"Saved heatmap to {out_path}")

if __name__ == "__main__":
    # Semantic similarity
    plot_heatmap(
        csv_path="eval/semantic_eval_results.csv",
        value_col="similarity",
        index_col="requirement_id",
        columns_col="model",
        out_path="eval/plots/semantic_similarity_heatmap.png",
        title="Semantic Similarity Heatmap (SBERT)"
    )
    # Field-level F1 (if you have field-level CSVs)
    try:
        plot_heatmap(
            csv_path="eval/field_eval_results.csv",
            value_col="f1_score",
            index_col="field",
            columns_col="model",
            out_path="eval/plots/field_f1_heatmap.png",
            title="Field-Level F1 Heatmap"
        )
    except Exception as e:
        print("Field-level F1 heatmap skipped:", e)
