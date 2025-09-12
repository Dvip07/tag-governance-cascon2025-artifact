# SBERT HLJ Audit Logger - Mega Forensic Edition (with LLM fallback and logging)
# Author: Dvip + ChatGPT, 2025-05-29

import os
import json
import csv
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
from collections import defaultdict
import pathlib
import sys
import re

ROOT_DIR = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT_DIR))

from services.llm_clients import call_gpt41_model

MODEL_FOLDERS = ["gpt41", "meta70b", "opus4"]
BASE_OUTPUT_DIR = "eval/output"
LOG_BASE = "eval/sbert_fix"
PROMPT_PATH = "eval/prompts/hlj_fallback_by_sbert_prompt.md"
THRESHOLD_CONFIDENCE = 0.75
THRESHOLD_SIMILARITY = 0.75
CLAMP_MIN = 0.70
CLAMP_MAX = 0.99
# LLM_FALLBACK_URL = "http://localhost:5002/call_gpt41_model"  # Update as needed


model = SentenceTransformer('all-MiniLM-L6-v2')

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def clamp_conf(val):
    reason = None
    if val < CLAMP_MIN:
        reason = f"clamped up to {CLAMP_MIN}"
        val = CLAMP_MIN
    elif val > CLAMP_MAX:
        reason = f"clamped down to {CLAMP_MAX}"
        val = CLAMP_MAX
    return round(val, 3), reason

def check_tag_integrity(tags, tag_metadata_reference):
    meta_tags = {t["tag"] for t in tag_metadata_reference}
    return set(tags) >= meta_tags, meta_tags - set(tags)

def call_llm_fallback(raw_text, summary, field_name, prompt_path=PROMPT_PATH):
    # Loads prompt template, fills in fields, calls LLM endpoint (returns only value)
    with open(prompt_path) as f:
        prompt_template = f.read()
    prompt = (
        prompt_template
        .replace("{raw_requirement}", raw_text)
        .replace("{summary}", summary)
        .replace("{field_name}", field_name)
    )
    try:
        # response = requests.post(
        #     LLM_FALLBACK_URL,
        #     json={"prompt": prompt}
        # )
        val = call_gpt41_model(prompt)
        return val.strip() if val else "unknown"
    except Exception as e:
        print(f"[LLM FALLBACK ERROR] {e}")
        return "unknown"
        return val
    except Exception as e:
        print(f"[LLM FALLBACK ERROR] {e}")
        return "unknown"

def auto_populate_field(field_value, raw_text, summary, field_name):
    # Call LLM fallback only if current value is missing or flagged
    new_value = call_llm_fallback(raw_text, summary, field_name)
    return new_value

def validate_hlj_item(hlj, raw_text, summary, model_name, req_id, hlj_id):
    errors, fixes, flagged = [], [], {}
    now_utc = datetime.utcnow().isoformat() + 'Z'
    status_by_field = {}
    for key in ["difficulty_confidence", "priority_confidence"]:
        if key in hlj:
            orig_val = hlj[key]
            new_val, reason = clamp_conf(orig_val)
            if new_val != orig_val:
                fixes.append({
                    "field": key,
                    "old_value": orig_val,
                    "new_value": new_val,
                    "fix_reason": f"clamped (was {orig_val}) - {reason}",
                    "fixed_by": "sbert_validator",
                    "timestamp": now_utc
                })
                status_by_field[key] = "changed"
            else:
                status_by_field[key] = "passed"
            hlj[key] = new_val
            if reason:
                hlj["low_confidence_reason"] = f"{key} {reason}"
    tags = set(hlj.get("tags", []))
    tag_meta = hlj.get("reasoning", {}).get("tag_metadata_reference", [])
    integrity, missing = check_tag_integrity(tags, tag_meta)
    if not integrity:
        errors.append({
            "id": hlj["id"],
            "issue": f"missing tag(s) in tags: {missing}",
            "severity": "critical",
            "tags_involved": list(missing)
        })
        status_by_field["tags"] = "error"
    else:
        status_by_field["tags"] = "passed"
    if len(tags) > 4:
        errors.append({
            "id": hlj["id"],
            "issue": f"too many tags ({len(tags)})",
            "severity": "critical",
            "tags_involved": list(tags)
        })
        status_by_field["tags"] = "error"
    for field in ["difficulty", "priority"]:
        conf_key = f"{field}_confidence"
        if conf_key in hlj and hlj[conf_key] < THRESHOLD_CONFIDENCE:
            value = hlj.get(field, "")
            emb_value = model.encode(str(value), convert_to_tensor=True)
            emb_raw = model.encode(str(raw_text), convert_to_tensor=True)
            emb_sum = model.encode(str(summary), convert_to_tensor=True)
            sim_raw = util.cos_sim(emb_value, emb_raw).item()
            sim_sum = util.cos_sim(emb_value, emb_sum).item()
            avg_sim = round((sim_raw + sim_sum) / 2, 3)
            flagged[field] = {
                "value": value,
                "confidence": round(hlj[conf_key], 3),
                "avg_similarity": avg_sim,
                "flag_reason": "Low confidence and low semantic alignment" if avg_sim < THRESHOLD_SIMILARITY else "Low confidence"
            }
            if not value or avg_sim < THRESHOLD_SIMILARITY:
                suggested = auto_populate_field(value, raw_text, summary, field)
                if suggested != value:
                    fixes.append({
                        "field": field,
                        "old_value": value,
                        "new_value": suggested,
                        "fix_reason": "Auto-populated by gpt-41 fallback due to low semantic alignment",
                        "fixed_by": "gpt41",
                        "timestamp": now_utc
                    })
                    status_by_field[field] = "changed"
                    hlj[field] = suggested
                else:
                    status_by_field[field] = "flagged"
            else:
                status_by_field[field] = "passed"
    notes = hlj.get("inference_notes", {})
    if "tag_added" in notes:
        if notes.get("confidence", 0) < 0.90:
            errors.append({
                "id": hlj["id"],
                "issue": f"[INFERRED] tag '{notes['tag_added']}' below 0.90 conf ({notes.get('confidence')})",
                "severity": "warning",
                "tags_involved": [notes["tag_added"]]
            })
            status_by_field["inferred_tag"] = "error"
        else:
            status_by_field["inferred_tag"] = "passed"
    if fixes:
        hlj.setdefault("fixes", []).extend(fixes)
    return errors, fixes, flagged, status_by_field

def write_per_hlj_csv(model, req, hlj_id, rows):
    hlj_dir = os.path.join(LOG_BASE, model, req)
    ensure_dir(hlj_dir)
    out_path = os.path.join(hlj_dir, f"{hlj_id}_status.csv")
    fieldnames = rows[0].keys() if rows else []
    with open(out_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def write_requirement_summary_csv(model, req, summary_rows):
    req_dir = os.path.join(LOG_BASE, model, req)
    ensure_dir(req_dir)
    out_path = os.path.join(req_dir, "requirement_summary.csv")
    fieldnames = summary_rows[0].keys() if summary_rows else []
    with open(out_path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

def write_missing_inputs(missing_rows):
    if not missing_rows:
        return
    path = os.path.join(LOG_BASE, "missing_inputs.csv")
    fieldnames = missing_rows[0].keys()
    with open(path, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(missing_rows)

def main():
    ensure_dir(LOG_BASE)
    master_rows = []
    error_rows = []
    tag_heatmap = defaultdict(int)
    field_heatmap = defaultdict(int)
    missing_inputs = []
    for model_folder in MODEL_FOLDERS:
        print(f"Validating model: {model_folder}")
        model_dir = os.path.join(BASE_OUTPUT_DIR, model_folder)
        req_folders = [f for f in os.listdir(model_dir) if f.startswith("req-")]
        for req in tqdm(req_folders, desc=model_folder):
            req_dir = os.path.join(model_dir, req)
            raw_path = os.path.join(req_dir, "summary", "step1_response.txt")
            sum_json_path = os.path.join(req_dir, "summary", "summary_clean.json")
            hlj_path = os.path.join(req_dir, "hlj", "merged", "all_chunks_full.json")
            if not (os.path.exists(raw_path) and os.path.exists(sum_json_path) and os.path.exists(hlj_path)):
                missing_inputs.append({
                    "model": model_folder,
                    "requirement_id": req,
                    "raw_path": raw_path,
                    "summary_path": sum_json_path,
                    "hlj_path": hlj_path
                })
                continue
            with open(raw_path) as f: raw_text = f.read()
            with open(sum_json_path) as f: summary = json.load(f).get("summary", "")
            with open(hlj_path) as f: hlj_data = json.load(f)
            per_req_summary = {
                "requirement_id": req, "total_hljs": 0,
                "hljs_changed": 0, "hljs_passed": 0,
                "hljs_with_errors": 0, "%changed": 0, "%error": 0
            }
            summary_rows = []
            for hlj in hlj_data:
                hlj_id = hlj.get("id", "unknown")
                errors, fixes, flagged, status_by_field = validate_hlj_item(
                    hlj, raw_text, summary, model_folder, req, hlj_id)
                per_hlj_rows = []
                hlj_status = "passed"
                if errors:
                    hlj_status = "error"
                    per_req_summary["hljs_with_errors"] += 1
                if fixes:
                    hlj_status = "changed"
                    per_req_summary["hljs_changed"] += 1
                if not errors and not fixes:
                    per_req_summary["hljs_passed"] += 1
                per_req_summary["total_hljs"] += 1
                for field, status in status_by_field.items():
                    row = {
                        "hlj_id": hlj_id, "model": model_folder, "requirement_id": req,
                        "field": field, "status": status,
                        "old_value": None, "new_value": None, "fix_reason": None, "timestamp": None
                    }
                    for fix in fixes:
                        if fix["field"] == field:
                            row["old_value"] = fix["old_value"]
                            row["new_value"] = fix["new_value"]
                            row["fix_reason"] = fix["fix_reason"]
                            row["timestamp"] = fix["timestamp"]
                    per_hlj_rows.append(row)
                    master_rows.append(dict(row))
                    if status == "error":
                        for err in errors:
                            if err["issue"]:
                                error_row = dict(row)
                                error_row.update({
                                    "error_type": err["severity"],
                                    "issue": err["issue"],
                                    "tags_involved": err.get("tags_involved", [])
                                })
                                error_rows.append(error_row)
                                if field == "tags":
                                    for tag in err.get("tags_involved", []):
                                        tag_heatmap[(model_folder, tag)] += 1
                                field_heatmap[(model_folder, field)] += 1
                write_per_hlj_csv(model_folder, req, hlj_id, per_hlj_rows)
            per_req_summary["%changed"] = round(100 * per_req_summary["hljs_changed"] / per_req_summary["total_hljs"], 2) if per_req_summary["total_hljs"] else 0
            per_req_summary["%error"] = round(100 * per_req_summary["hljs_with_errors"] / per_req_summary["total_hljs"], 2) if per_req_summary["total_hljs"] else 0
            summary_rows.append(per_req_summary)
            write_requirement_summary_csv(model_folder, req, summary_rows)
    ensure_dir(LOG_BASE)
    if master_rows:
        with open(os.path.join(LOG_BASE, "master_log.csv"), "w") as f:
            writer = csv.DictWriter(f, fieldnames=master_rows[0].keys())
            writer.writeheader()
            writer.writerows(master_rows)
    if error_rows:
        with open(os.path.join(LOG_BASE, "master_errors.csv"), "w") as f:
            writer = csv.DictWriter(f, fieldnames=error_rows[0].keys())
            writer.writeheader()
            writer.writerows(error_rows)
    with open(os.path.join(LOG_BASE, "tag_error_heatmap.csv"), "w") as f:
        writer = csv.writer(f)
        writer.writerow(["model", "tag", "error_count"])
        for (model, tag), count in tag_heatmap.items():
            writer.writerow([model, tag, count])
    with open(os.path.join(LOG_BASE, "field_error_heatmap.csv"), "w") as f:
        writer = csv.writer(f)
        writer.writerow(["model", "field", "error_count"])
        for (model, field), count in field_heatmap.items():
            writer.writerow([model, field, count])
    write_missing_inputs(missing_inputs)
    print("✅ All logs, errors, and audits written to eval/sbert_fix/.")

if __name__ == "__main__":
    main()
