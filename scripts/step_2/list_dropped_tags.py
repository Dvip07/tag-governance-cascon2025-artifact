import os
import csv
import argparse
import yaml
from datetime import datetime
from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run


def ensure_run_id(cfg_path, cfg):
    """Ensure the YAML config has a unique run_id + run_dir set."""
    run_id = cfg.get("globals.run_id")
    run_dir = cfg.get("globals.run_dir")

    if not run_id or not run_dir:
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        run_id = f"run_{ts}"
        run_dir = os.path.join("runs", run_id)

        # Update YAML file in-place
        with open(cfg_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        raw.setdefault("globals", {})
        raw["globals"]["run_id"] = run_id
        raw["globals"]["run_dir"] = run_dir
        raw.setdefault("outputs", {})
        raw["outputs"]["dropped_tags"] = os.path.join(run_dir, "dropped_tags.csv")

        os.makedirs(run_dir, exist_ok=True)
        with open(cfg_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(raw, f, sort_keys=False)

        print(f"🆕 Created run_id: {run_id}, run_dir: {run_dir}")
    else:
        print(f"🔁 Using existing run_id: {run_id}")

    return run_id, run_dir, cfg.get("outputs.dropped_tags")


def list_dropped_tags_to_file(cfg, output_file):
    base_path = cfg.get("globals.sbert_fix_base", "sbert_fix")
    rows = []

    for req in os.listdir(base_path):
        path = os.path.join(base_path, req, "tag_audit.yaml")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            audits = yaml.safe_load(f)

        for audit in audits or []:
            for tag in audit.get("tags_dropped", []):
                rows.append({
                    "requirement": req,
                    "hlj_id": audit.get("hlj_id", "unknown"),
                    "dropped_tag": tag,
                })

    if not rows:
        print("😇 No dropped tags found.")
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["requirement", "hlj_id", "dropped_tag"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Dropped tags exported to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export dropped tags from audits")
    parser.add_argument("--config", default="configs/pipeline_v1.yaml", help="Path to config YAML")
    args = parser.parse_args()

    cfg = ConfigResolver(args.config)
    run_id, run_dir, out_file = ensure_run_id(args.config, cfg)
    run_id = get_current_run("configs/pipeline_v1.yaml")
    list_dropped_tags_to_file(cfg, out_file)
