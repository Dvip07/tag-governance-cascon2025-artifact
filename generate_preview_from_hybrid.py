import os
import json
from pathlib import Path
from statistics import mean

# 🔍 Automatically find the latest run directory
v2_root = Path("eval/runs/v2")
runs = sorted(v2_root.glob("run_*"), key=os.path.getmtime, reverse=True)
if not runs:
    raise RuntimeError("No v2 runs found under eval/runs/v2/")
run_dir = runs[0]
print(f"🧭 Using latest run: {run_dir.name}")

# Define the hybrid root
ROOT = run_dir / "step_7" / "hybrid"
OUTPUT = Path("preview.jsonl")
preview_rows = []

# Recursive scan for all_chunks*.json under hybrid/
for model_dir in ROOT.iterdir():
    if not model_dir.is_dir():
        continue
    for req_dir in model_dir.iterdir():
        if not req_dir.is_dir():
            continue
        for file_path in req_dir.glob("all_chunks*_validated.json"):
            try:
                with open(file_path) as f:
                    data = json.load(f)
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
                continue

            for item in data:
                validations = item.get("tag_nlu_validation", [])
                confs = [v.get("confidence") for v in validations if v.get("confidence") is not None]
                validated_count = sum(1 for v in validations if v.get("validated"))
                avg_conf = round(mean(confs), 3) if confs else None

                row = {
                    "hlj_id": item.get("id"),
                    "req_id": item.get("source_hlj_id") or req_dir.name,
                    "model": model_dir.name,
                    "domain": item.get("domain", "unknown"),
                    "difficulty": item.get("difficulty", "unknown"),
                    "priority": item.get("priority", "unknown"),
                    "tags_v1": ", ".join(item.get("tags_v1", [])),
                    "tags_v2": ", ".join(item.get("tags_v2", [])),
                    "tags_v3": ", ".join(item.get("tags_v3", [])),
                    "validated_tags": validated_count,
                    "avg_confidence": avg_conf,
                }
                preview_rows.append(row)

print(f"✅ Extracted {len(preview_rows)} HLJ entries")

# Save as JSONL
with open(OUTPUT, "w") as f:
    for row in preview_rows:
        f.write(json.dumps(row) + "\n")

print(f"💾 Wrote preview file: {OUTPUT.resolve()}")
