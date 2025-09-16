# utils/config_loader.py
import yaml

def load_config(cfg_path="configs/pipeline_v0.yaml"):
    with open(cfg_path) as f:
        return yaml.safe_load(f)
# utils/config_loader.py
import yaml

def load_config(cfg_path="configs/pipeline_v0.yaml"):
    with open(cfg_path) as f:
        return yaml.safe_load(f)
