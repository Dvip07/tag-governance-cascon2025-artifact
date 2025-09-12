import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_model_diff_heatmap(csv_path, value_col, index_col, columns_col, baseline_model, out_path, title):
    df = pd.read_csv(csv_path)
    baseline_df = df[df[columns_col] == baseline_model].set_index(index_col)[value_col]
    pivot = df.pivot(index=index_col, columns=columns_col, values=value_col)
    for model in pivot.columns:
        if model == baseline_model:
            continue
        diff = pivot[model] - baseline_df
        plt.figure(figsize=(10, max(4, int(len(diff)/2))))
        sns.heatmap(diff.to_frame().T, annot=True, cmap="coolwarm", center=0, linewidths=0.3)
        plt.title(f"{title} ({model} - {baseline_model})")
        plt.xlabel(index_col)
        plt.ylabel("Difference")
        plt.tight_layout()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path.replace(".png", f"_{model}_vs_{baseline_model}.png"))
        plt.close()
        print(f"Saved model-vs-model diff heatmap for {model} to {out_path.replace('.png', f'_{model}_vs_{baseline_model}.png')}")

if __name__ == "__main__":
    # Semantic similarity diff
    plot_model_diff_heatmap(
        csv_path="eval/semantic_eval_results.csv",
        value_col="similarity",
        index_col="requirement_id",
        columns_col="model",
        baseline_model="GPT-4.1",
        out_path="eval/plots/model_diff_semantic_similarity.png",
        title="Semantic Similarity: Model Diff"
    )
    # Field-level F1 diff (if available)
    try:
        plot_model_diff_heatmap(
            csv_path="eval/field_eval_results.csv",
            value_col="f1_score",
            index_col="field",
            columns_col="model",
            baseline_model="GPT-4.1",
            out_path="eval/plots/model_diff_field_f1.png",
            title="Field-Level F1: Model Diff"
        )
    except Exception as e:
        print("Field-level F1 diff heatmap skipped:", e)
