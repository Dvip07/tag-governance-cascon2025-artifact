# semantic_eval.py — SBERT-Based HLJ Similarity

from sentence_transformers import SentenceTransformer, util
import yaml
import json
import pandas as pd
from tqdm import tqdm
import sys

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def safe_get_hljs(data):
    # Extract list of HLJs from various wrappers
    if isinstance(data, list):
        return data
    if "CURRENT_CHUNK" in data and "DATA" in data["CURRENT_CHUNK"]:
        return data["CURRENT_CHUNK"]["DATA"]
    if "DATA" in data:
        return data["DATA"]
    for v in data.values():
        if isinstance(v, list):
            return v
    raise ValueError("HLJ list not found in file.")

# Model can be changed if you want bigger embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

with open('eval/meta.yaml') as f:
    meta = yaml.safe_load(f)

results = []

for pair in tqdm(meta, desc="Evaluating HLJs"):
    gold = load_json(pair['gold_path'])
    cand = load_json(pair['candidate_path'])
    gold_hljs = safe_get_hljs(gold)
    cand_hljs = safe_get_hljs(cand)
    gold_map = {h['id']: h for h in gold_hljs}
    cand_map = {h['id']: h for h in cand_hljs}
    all_ids = set(gold_map) & set(cand_map)  # Only compare IDs found in both

    for hlj_id in all_ids:
        g = gold_map[hlj_id]
        c = cand_map[hlj_id]
        g_summary = g.get('summary', '')
        c_summary = c.get('summary', '')
        g_emb = model.encode(g_summary, convert_to_tensor=True)
        c_emb = model.encode(c_summary, convert_to_tensor=True)
        similarity = util.cos_sim(g_emb, c_emb).item()
        results.append({
            "req_id": pair['req_id'],
            "hlj_id": hlj_id,
            "gold_summary": g_summary,
            "cand_summary": c_summary,
            "similarity": similarity,
            "model": pair['model'],
        })

# Save to CSV
import os
os.makedirs('eval', exist_ok=True)
df = pd.DataFrame(results)
df.to_csv("eval/semantic_eval_results.csv", index=False)

# Print stats
print(df.groupby('model')['similarity'].describe())

# Optional: Visualize
if '--plot' in sys.argv:
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.histplot(df, x='similarity', hue='model', kde=True)
    plt.title("SBERT Cosine Similarity Distribution")
    plt.show()
