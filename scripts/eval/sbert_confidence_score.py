"""
Step 1 — SBERT Confidence Score Evaluation
------------------------------------------
Validates HLJ (High-Level JSON) items using SBERT embeddings.
- Clamps confidence values
- Checks tag integrity
- Flags low-confidence fields with semantic similarity fallback

All paths, models, and thresholds are loaded from a versioned config YAML.
"""

# ========= Imports =========
import json, yaml
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
from scripts.step_1.config_resolver import ConfigResolver


# ========= Helpers =========
def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def clamp_conf(val, clamp_min, clamp_max):
    """Clamp confidence values into [clamp_min, clamp_max]."""
    reason = None
    if val < clamp_min:
        val, reason = clamp_min, f"clamped up to {clamp_min}"
    elif val > clamp_max:
        val, reason = clamp_max, f"clamped down to {clamp_max}"
    return round(val, 3), reason

def check_tag_integrity(tags, tag_meta):
    """Verify all reference tags are included in HLJ tags."""
    ref_tags = {t["tag"] for t in tag_meta}
    return set(tags) >= ref_tags, ref_tags - set(tags)

def log_results(log_dir: Path, model: str, req: str, results: dict):
    """Append per-requirement validation results to JSON log."""
    ensure_dir(log_dir)
    out_file = log_dir / f"{model}_{req}_audit.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


# ========= Core Validation =========
def validate_hlj_item(hlj, raw_text, summary, model_name, req_id, cfg, sbert_model):
    errors, fixes, flagged = [], [], {}
    now_utc = datetime.utcnow().isoformat() + "Z"
    status_by_field = {}

    # Clamp difficulty/priority confidences
    for key in ["difficulty_confidence", "priority_confidence"]:
        if key in hlj:
            orig_val = hlj[key]
            new_val, reason = clamp_conf(
                orig_val,
                cfg.get("thresholds.clamp_min"),
                cfg.get("thresholds.clamp_max"),
            )
            if new_val != orig_val:
                fixes.append({
                    "field": key, "old_value": orig_val, "new_value": new_val,
                    "fix_reason": reason, "fixed_by": "sbert_validator",
                    "timestamp": now_utc
                })
                status_by_field[key] = "changed"
            else:
                status_by_field[key] = "passed"
            hlj[key] = new_val

    # Tag integrity check
    tags = set(hlj.get("tags", []))
    tag_meta = hlj.get("reasoning", {}).get("tag_metadata_reference", [])
    integrity, missing = check_tag_integrity(tags, tag_meta)
    if not integrity:
        errors.append({"id": hlj["id"], "issue": f"missing tags: {missing}", "severity": "critical"})
        status_by_field["tags"] = "error"
    elif len(tags) > 4:
        errors.append({"id": hlj["id"], "issue": f"too many tags ({len(tags)})", "severity": "critical"})
        status_by_field["tags"] = "error"
    else:
        status_by_field["tags"] = "passed"

    # Semantic similarity fallback (difficulty/priority)
    for field in ["difficulty", "priority"]:
        conf_key = f"{field}_confidence"
        if conf_key in hlj and hlj[conf_key] < cfg.get("thresholds.confidence"):
            value = hlj.get(field, "")
            emb_value = sbert_model.encode(str(value), convert_to_tensor=True)
            emb_raw   = sbert_model.encode(str(raw_text), convert_to_tensor=True)
            emb_sum   = sbert_model.encode(str(summary), convert_to_tensor=True)
            avg_sim   = ((util.cos_sim(emb_value, emb_raw) +
                          util.cos_sim(emb_value, emb_sum)) / 2).item()

            flagged[field] = {
                "value": value,
                "confidence": round(hlj[conf_key], 3),
                "avg_similarity": round(avg_sim, 3),
                "flag_reason": (
                    "Low confidence" if avg_sim >= cfg.get("thresholds.similarity")
                    else "Low confidence + misaligned"
                ),
            }
            status_by_field[field] = "flagged" if avg_sim < cfg.get("thresholds.similarity") else "passed"

    return {
        "hlj_id": hlj.get("id", "unknown"),
        "errors": errors,
        "fixes": fixes,
        "flagged": flagged,
        "status": status_by_field,
    }


# ========= Main =========
def main(cfg_path="configs/pipeline_v0.yaml"):
    cfg = ConfigResolver(cfg_path)

    sbert_model = SentenceTransformer(cfg.get("models.sbert"))
    logs_dir = Path(cfg.get("paths.logs_dir"))
    base_output = Path(cfg.get("paths.base_output"))

    missing_inputs = []

    for model_folder in cfg.get("models.folders"):
        print(f"Validating model: {model_folder}")
        model_dir = base_output / model_folder
        if not model_dir.exists():
            continue

        req_folders = [f for f in model_dir.iterdir() if f.name.startswith("req-")]
        for req in tqdm(req_folders, desc=model_folder):
            raw_path = req / "summary" / "step1_response.txt"
            sum_json = req / "summary" / "summary_clean.json"
            hlj_path = req / "hlj" / "merged" / "all_chunks_full.json"

            if not (raw_path.exists() and sum_json.exists() and hlj_path.exists()):
                missing_inputs.append({"model": model_folder, "req": req.name})
                continue

            raw_text = raw_path.read_text(encoding="utf-8")
            summary  = json.loads(sum_json.read_text()).get("summary", "")
            hljs     = json.loads(hlj_path.read_text())

            for hlj in hljs:
                results = validate_hlj_item(
                    hlj, raw_text, summary, model_folder, req.name, cfg, sbert_model
                )
                log_results(logs_dir, model_folder, req.name, results)

    # Save missing inputs summary
    if missing_inputs:
        out_missing = logs_dir / "missing_inputs.json"
        ensure_dir(logs_dir)
        with open(out_missing, "w", encoding="utf-8") as f:
            json.dump(missing_inputs, f, indent=2)
        print(f"⚠️ Missing inputs logged to {out_missing}")

    print("✅ Validation complete")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/pipeline_v0.yaml")
    args = parser.parse_args()
    main(args.config)
