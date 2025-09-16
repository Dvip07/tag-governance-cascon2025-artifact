import os
import json
import matplotlib.pyplot as plt

# Configuration
base_dir = "eval/output"
models = ["gpt41", "opus4", "meta70b"]
chart_dir = "eval/visualize/bar_chart"
os.makedirs(chart_dir, exist_ok=True)
chart_path = os.path.join(chart_dir, "hlj_count_bar_chart.png")

# Data collection
req_ids = set()
model_counts = {model: {} for model in models}

for model in models:
    model_dir = os.path.join(base_dir, model)
    if not os.path.isdir(model_dir):
        print(f"Model dir not found: {model_dir}, skipping")
        continue

    for req_folder in os.listdir(model_dir):
        if not req_folder.startswith("req-"):
            continue
        req_id = req_folder
        req_ids.add(req_id)
        hlj_path = os.path.join(model_dir, req_folder, "hlj", "trim_merged", "all_trimmed_hljs.json")
        try:
            with open(hlj_path, "r") as f:
                hlj_data = json.load(f)
                model_counts[model][req_id] = len(hlj_data)
        except Exception as e:
            print(f"Failed to read {hlj_path}: {e}")
            model_counts[model][req_id] = 0

# Sort requirement IDs for x-axis
sorted_req_ids = sorted(list(req_ids))

# Prepare bar chart data
bar_width = 0.2
x = range(len(sorted_req_ids))
offsets = [-bar_width, 0, bar_width]  # for three models

plt.figure(figsize=(max(8, len(sorted_req_ids) * 0.5), 6))

for i, model in enumerate(models):
    y = [model_counts[model].get(req_id, 0) for req_id in sorted_req_ids]
    plt.bar([xi + offsets[i] for xi in x], y, width=bar_width, label=model)

plt.xlabel("Requirement ID")
plt.ylabel("Number of HLJs")
plt.title("Number of HLJs generated per requirement (by model)")
plt.xticks([xi for xi in x], [req_id for req_id in sorted_req_ids], rotation=90)
plt.legend()
plt.tight_layout()
plt.savefig(chart_path)
print(f"Chart saved to {chart_path}")
