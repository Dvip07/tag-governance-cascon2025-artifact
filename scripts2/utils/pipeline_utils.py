# scripts/utils/pipeline_utils.py
import os
import glob
import logging
import sys
from datetime import datetime

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def walk_nested(root, filename_pattern=None, max_depth=None):
    """
    Generator that yields (dirpath, filename) for files matching pattern, recursively.
    - filename_pattern: glob pattern or substring
    - max_depth: int or None
    """
    for dirpath, _, files in os.walk(root):
        rel_depth = dirpath[len(root):].count(os.sep)
        if max_depth is not None and rel_depth > max_depth:
            continue
        for fname in files:
            if not filename_pattern or glob.fnmatch.fnmatch(fname, filename_pattern):
                yield dirpath, fname

def setup_logging(log_dir, run_id, step_name):
    ensure_dir(log_dir)
    log_path = os.path.join(log_dir, f"{step_name}_{run_id}.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_path

def save_manifest(manifest, output_dir):
    ensure_dir(output_dir)
    path = os.path.join(output_dir, "run_manifest.json")
    with open(path, "w") as f:
        import json; json.dump(manifest, f, indent=2)
