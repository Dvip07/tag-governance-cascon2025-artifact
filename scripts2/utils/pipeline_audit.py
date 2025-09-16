import os
import json
import hashlib
from datetime import datetime

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def hash_script(script_path):
    try:
        with open(script_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return "NA"

def log_pipeline_step(
    step_name,
    input_paths,
    output_paths,
    configs,
    model_versions,
    stats,
    log_dir,
    script_path
):
    run_id = datetime.now().strftime("%Y%m%dT%H%M%S")
    ensure_dir(log_dir)
    manifest = {
        "run_id": run_id,
        "step_name": step_name,
        "input_paths": input_paths,
        "output_paths": output_paths,
        "configs": configs,
        "model_versions": model_versions,
        "script_hash": hash_script(script_path),
        "stats": stats,
        "timestamp": run_id,
    }
    mpath = os.path.join(log_dir, f"{step_name}_manifest_{run_id}.json")
    with open(mpath, "w") as f: json.dump(manifest, f, indent=2)
    print(f"[{step_name}] Manifest written: {mpath}")
    return mpath

def append_audit_trail(hlj_id, record, audit_dir):
    ensure_dir(audit_dir)
    path = os.path.join(audit_dir, f"{hlj_id}_audit.jsonl")
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")

def assemble_grand_manifest(log_dir, output_path):
    step_manifests = []
    for fname in sorted(os.listdir(log_dir)):
        if "_manifest_" in fname and fname.endswith(".json"):
            with open(os.path.join(log_dir, fname)) as f:
                step_manifests.append(json.load(f))
    grand = {
        "pipeline_version": "v2",
        "run_id": step_manifests[0]["run_id"] if step_manifests else "unknown",
        "timestamp": datetime.now().isoformat(),
        "steps": step_manifests,
    }
    with open(output_path, "w") as f: json.dump(grand, f, indent=2)
    print(f"Grand pipeline manifest saved: {output_path}")
    return output_path

def save_markdown_report(md_str, output_path):
    with open(output_path, "w") as f:
        f.write(md_str)
    print(f"Markdown report saved: {output_path}")
