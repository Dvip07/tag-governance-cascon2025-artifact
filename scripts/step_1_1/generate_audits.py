import os
import json
import yaml
from datetime import datetime

SBERT_FIX_BASE = "sbert_fix"
HLJ_INPUT_SUBPATH = "hlj/trim_merged/all_trimmed_hljs.json"
VALIDATED_FILE_NAME = "all_chunks_full_validated.json"
AUDIT_FILE_NAME = "tag_audit.yaml"


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def load_json_safe(path):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load {path}: {e}")
        return None

def main():
    for model in os.listdir(SBERT_FIX_BASE):
        model_dir = os.path.join(SBERT_FIX_BASE, model)
        if not os.path.isdir(model_dir):
            continue

        for req in os.listdir(model_dir):
            req_dir = os.path.join(model_dir, req)
            validated_path = os.path.join(req_dir, VALIDATED_FILE_NAME)
            if not os.path.exists(validated_path):
                print(f"Missing validated HLJs for {model}/{req}")
                continue

            hlj_validated = load_json_safe(validated_path)
            if hlj_validated is None:
                continue

            # Build audit logs per HLJ
            audits = []
            for hlj in hlj_validated:
                orig_tags = hlj.get("tags_v1", [])
                new_tags = hlj.get("tags_v2", hlj.get("tags", []))
                tag_validations = hlj.get("tag_validation", [])

                tags_added = [t for t in new_tags if t not in orig_tags]
                tags_dropped = [t for t in orig_tags if t not in new_tags]
                tags_kept = [t for t in orig_tags if t in new_tags]

                audit = {
                    "hlj_id": hlj.get("id", "unknown_id"),
                    "requirement": req,
                    "model": model,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "original_tags": orig_tags,
                    "validated_tags": new_tags,
                    "tags_added": tags_added,
                    "tags_dropped": tags_dropped,
                    "tags_kept": tags_kept,
                    "validation_details": tag_validations,
                }
                audits.append(audit)

            # Output audit YAML per requirement
            out_path = os.path.join(model_dir, req, AUDIT_FILE_NAME)
            with open(out_path, "w") as f:
                yaml.dump(audits, f, sort_keys=False)
            print(f"✅ Audit log written to {out_path}")

if __name__ == "__main__":
    main()
