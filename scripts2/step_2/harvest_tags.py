import os
import json
import csv

# === CONFIG ===
BASE_DIR = "sbert_fix"
OUTPUT_DIR = "sbert_fix/all_tags/step_1"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODELS = ["gpt41", "opus4", "meta70b"]

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
                print(f"⚠️ File is not a list: {path} (got {type(content).__name__})")
                return []
            return content
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error in {path}: {e}")
            return []

def flatten_tag_entry(tag, hlj_id, model, version, confidence=None, context=None, status=None, req_id=None):
    is_flagged = False
    reasons = []

    # Check for inference
    is_inferred = "[inferred]" in tag.lower()
    tag_cleaned = tag.lower().replace("[inferred]", "").strip()

    # Flagging logic
    if confidence is None or confidence < 0.70:
        is_flagged = True
        reasons.append("low_confidence")
    if not context or context.strip() == "":
        is_flagged = True
        reasons.append("no_context")
    if status is None or status == "none":
        is_flagged = True
        reasons.append("unvalidated")

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

def main():
    all_files = collect_all_json_files(BASE_DIR, MODELS)
    print(f"Total files collected: {len(all_files)}")
    out_rows = []
    for model, req_id, version, path in all_files:
        print(f"Reading: {path}")
        try:
            data = load_jsonl(path)
            for entry in data:
                out_rows.extend(parse_tags_from_entry(entry, model, version, req_id))
        except Exception as e:
            print(f"Failed to parse {path}: {e}")
    # Write to CSV
    output_csv = os.path.join(OUTPUT_DIR, "tags_all.csv")
    with open(output_csv, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "tag", "hlj_id", "requirement_id", "model", "version",
            "confidence", "context", "validation_status",
            "inferred", "flagged", "reason_for_flagged"
        ])
        writer.writeheader()
        writer.writerows(out_rows)
    print(f"✅ All tags extracted and saved to {output_csv} ({len(out_rows)} rows)")

if __name__ == "__main__":
    main()



# python extract_candidates_batch.py \
#   --base_dir sbert_fix \
#   --output_root keyword_extraction \
#   --pipeline_version v0 \
#   --log_dir pipeline_runs/logs/keyword_extract/v0/step_01_candidates \
#   --models gpt41 opus4 meta70b
