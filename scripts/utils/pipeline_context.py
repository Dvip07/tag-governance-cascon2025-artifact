# scripts/utils/pipeline_context.py
import os
import uuid
from datetime import datetime
import yaml

CONFIG_FILE = "configs/pipeline_v1.yaml"  # adjust if needed


def new_run_id() -> str:
    """Generate a unique run ID like pipeline_20250915_123456_ab12cd."""
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    return f"pipeline_{ts}_{uuid.uuid4().hex[:6]}"


def load_config(path=CONFIG_FILE):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(cfg, path=CONFIG_FILE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)


def init_run(config_path=CONFIG_FILE) -> str:
    """
    Create and register a new pipeline run ID in the global YAML.
    Returns the run_id string.
    """
    cfg = load_config(config_path)

    run_id = new_run_id()
    cfg.setdefault("globals", {})
    cfg["globals"]["current_run_id"] = run_id

    cfg.setdefault("pipeline_runs", {})
    cfg["pipeline_runs"][run_id] = {"timestamp": datetime.utcnow().isoformat()}

    save_config(cfg, config_path)
    return run_id


def get_current_run(config_path=CONFIG_FILE) -> str:
    """Fetch the currently active run_id from YAML."""
    cfg = load_config(config_path)
    return cfg.get("globals", {}).get("current_run_id")
