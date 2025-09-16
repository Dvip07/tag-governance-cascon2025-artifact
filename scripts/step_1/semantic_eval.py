"""
Step 1 — Semantic Evaluation with SBERT
---------------------------------------
Compares candidate HLJ summaries to gold summaries using SBERT cosine similarity.
Outputs a CSV of similarity scores for analysis and plotting.

All paths, models, and output locations are loaded from a versioned config YAML.
"""

# ========= Imports =========
import os, json, argparse
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util
from scripts.step_1.config_resolver import ConfigResolver


# ========= Helpers =========
def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_get_hljs(data):
    """Extract HLJs regardless of wrapping structure (CURRENT_CHUNK, DATA, etc.)."""
    if isinstance(data, dict):
        if "CURRENT_CHUNK" in data:
            return data["CURRENT_CHUNK"].get("DATA", [])
        if "DATA" in data:
            return data["DATA"]
    if isinstance(data, list):
        hljs = []
        for item in data:
            if isinstance(item, dict):
                if "CURRENT_CHUNK" in item:
                    hljs.extend(item["CURRENT_CHUNK"].get("DATA", []))
                elif "DATA" in item:
                    hljs.extend(item["DATA"])
                elif "id" in item:
                    hljs.append(item)
        return hljs
    return []


# ========= Main =========
def main(cfg_path="configs/pipeline_v0.yaml"):
    cfg = ConfigResolver(cfg_path)

    meta_path  = cfg.get("paths.meta_yaml")
    output_csv = cfg.get("semantic_eval.csv_out")
    model_name = cfg.get("models.sbert")

    # Load SBERT model
    sbert_model = SentenceTransformer(model_name)

    # Load meta file (list of gold/candidate pairs)
    meta = load_json(meta_path) if meta_path.endswith(".json") else __import__("yaml").safe_load(open(meta_path))

    results = []
    for pair in tqdm(meta, desc="Evaluating HLJs"):
        gold = load_json(pair["gold_path"])
        cand = load_json(pair["candidate_path"])
        gold_map = {h["id"]: h for h in safe_get_hljs(gold)}
        cand_map = {h["id"]: h for h in safe_get_hljs(cand)}

        for hlj_id in set(gold_map) & set(cand_map):
            g, c = gold_map[hlj_id], cand_map[hlj_id]
            g_sum, c_sum = g.get("summary", ""), c.get("summary", "")
            if not g_sum or not c_sum:
                continue
            g_emb = sbert_model.encode(g_sum, convert_to_tensor=True)
            c_emb = sbert_model.encode(c_sum, convert_to_tensor=True)
            similarity = util.cos_sim(g_emb, c_emb).item()
            results.append({
                "req_id": pair.get("req_id", "unknown"),
                "hlj_id": hlj_id,
                "similarity": similarity,
                "model": Path(pair["candidate_path"]).parent.name
            })

    # Save results
    out_csv_path = Path(output_csv)
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(results).to_csv(out_csv_path, index=False)
    print(f"✅ Saved results to {out_csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pipeline_v0.yaml")
    args = parser.parse_args()
    main(args.config)
