import os
import json
import csv
import argparse
import yaml
from datetime import datetime
import uuid
import argparse

PIPELINE_V2 = os.path.join("configs", "pipeline_v2.yaml")

def update_prev_run_paths():
    with open(PIPELINE_V2, "r") as f:
        cfg = yaml.safe_load(f)

    v1_config_path = cfg["globals"]["prev_config"]
    with open(v1_config_path, "r") as f:
        v1_cfg = yaml.safe_load(f)

    # find most recent v1 run
    runs = v1_cfg.get("pipeline_runs", {})
    sorted_runs = sorted(runs.items(), key=lambda kv: kv[1]["timestamp"], reverse=True)
    latest_run_id, meta = sorted_runs[0]

    run_dir = os.path.join(v1_cfg["globals"]["base_eval_dir"], latest_run_id)

    # update v2 config
    cfg["globals"]["prev_run_id"] = latest_run_id
    cfg["globals"]["prev_run_dir"] = run_dir

    with open(PIPELINE_V2, "w") as f:
        yaml.safe_dump(cfg, f)

    print(f"🔗 Linked v1 run: {latest_run_id}")
    print(f"   prev_run_dir: {run_dir}")
    return run_dir

# === Load/Save Config ===
def load_config(cfg_path):
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(cfg, cfg_path):
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

def init_run(cfg, cfg_path):
    """Ensure run_id + run_dir is set in config."""
    if not cfg.get("globals"):
        cfg["globals"] = {}

    run_id = cfg["globals"].get("run_id")
    run_dir = cfg["globals"].get("run_dir")

    if not run_id or not run_dir:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        run_id = f"run_{ts}_{uuid.uuid4().hex[:6]}"
        run_dir = os.path.join(cfg["globals"]["base_eval_dir"], run_id)
        os.makedirs(run_dir, exist_ok=True)

        cfg["globals"]["run_id"] = run_id
        cfg["globals"]["run_dir"] = run_dir
        cfg["globals"]["current_run_id"] = run_id

        # register under pipeline_runs
        cfg.setdefault("pipeline_runs", {})
        cfg["pipeline_runs"][run_id] = {"timestamp": datetime.utcnow().isoformat()}

        print(f"🆕 New run initialized: {run_id} -> {run_dir}")
    else:
        print(f"🔁 Continuing with existing run: {run_id}")

    save_config(cfg, cfg_path)
    return run_id, run_dir


# === Tag Harvest Functions ===
def collect_all_json_files(base_dir, models):
    files = []
    for model in models:
        model_path = os.path.join(base_dir, model)
        if not os.path.isdir(model_path):
            continue
        for req_id in os.listdir(model_path):
            req_dir = os.path.join(model_path, req_id)
            hybrid_path = os.path.join(req_dir, "hybridv3", "all_chunks_full_validated.json")
            root_path = os.path.join(req_dir, "all_chunks_full_validated.json")
            for path, version in [(hybrid_path, "v3"), (root_path, "v2")]:
                if os.path.exists(path):
                    files.append((model, req_id, version, path))
    return files

def load_jsonl(path):
    with open(path, "r") as f:
        try:
            content = json.load(f)
            if not isinstance(content, list):
                print(f"⚠️ File is not a list: {path}")
                return []
            return content
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error in {path}: {e}")
            return []

def flatten_tag_entry(tag, hlj_id, model, version, confidence=None, context=None, status=None, req_id=None):
    is_flagged, reasons = False, []
    is_inferred = "[inferred]" in tag.lower()
    tag_cleaned = tag.lower().replace("[inferred]", "").strip()

    if confidence is None or (isinstance(confidence, (int, float)) and confidence < 0.70):
        is_flagged, reasons = True, reasons + ["low_confidence"]
    if not context or context.strip() == "":
        is_flagged, reasons = True, reasons + ["no_context"]
    if status is None or status == "none":
        is_flagged, reasons = True, reasons + ["unvalidated"]

    return {
        "tag": tag_cleaned,
        "hlj_id": hlj_id,
        "requirement_id": req_id,
        "model": model,
        "version": version,
        "confidence": confidence,
        "context": context.lower() if context else None,
        "validation_status": status.lower() if status else None,
        "inferred": "yes" if is_inferred else "no",
        "flagged": "yes" if is_flagged else "no",
        "reason_for_flagged": ", ".join(reasons) if reasons else ""
    }

def parse_tags_from_entry(entry, model, version, req_id):
    tags = []
    for tagver in ["tags_v1", "tags_v2"]:
        for tag in entry.get(tagver, []):
            confidence, context, status = None, None, None
            if "tag_validation" in entry:
                for detail in entry["tag_validation"]:
                    if detail.get("original_tag") == tag:
                        confidence = detail.get("original_confidence")
                        context = detail.get("context")
                        status = detail.get("validation_status")
                        break
            tags.append(flatten_tag_entry(
                tag, entry["id"], model, tagver,
                confidence=confidence, context=context, status=status,
                req_id=req_id
            ))
    return tags


# === Main ===
def main(cfg_path):
    prev_run_dir = update_prev_run_paths()
    cfg = load_config(cfg_path)
    run_id, run_dir = init_run(cfg, cfg_path)

    base_dir = cfg["globals"]["base_dir"]
    models = cfg["globals"]["models"]

    out_dir = os.path.join(run_dir, "step_1")
    os.makedirs(out_dir, exist_ok=True)
    output_csv = os.path.join(out_dir, "tags_all.csv")

    all_files = collect_all_json_files(base_dir, models)
    print(f"Total files collected: {len(all_files)}")

    out_rows = []
    for model, req_id, version, path in all_files:
        try:
            data = load_jsonl(path)
            for entry in data:
                out_rows.extend(parse_tags_from_entry(entry, model, version, req_id))
        except Exception as e:
            print(f"Failed to parse {path}: {e}")

    # Write CSV
    with open(output_csv, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "tag", "hlj_id", "requirement_id", "model", "version",
            "confidence", "context", "validation_status",
            "inferred", "flagged", "reason_for_flagged"
        ])
        writer.writeheader()
        writer.writerows(out_rows)

    print(f"✅ All tags extracted and saved to {output_csv} ({len(out_rows)} rows)")

    # update YAML outputs
    cfg["outputs"]["tags_all"] = output_csv
    save_config(cfg, cfg_path)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Step 1: Harvest all tags")
    parser.add_argument("--config", required=True, help="Path to pipeline config YAML")
    args = parser.parse_args()
    main(args.config)
