"""
ConfigResolver
--------------
Utility to load and query the pipeline YAML config.
Lets you fetch nested values with dot notation, e.g.:

    cfg = ConfigResolver("configs/pipeline_v0.yaml")
    print(cfg["paths"]["base_output"])
    print(cfg.get("plots.aliases.GPT-4.1"))
"""

import yaml

class ConfigResolver:
    def __init__(self, yaml_path: str):
        with open(yaml_path, "r", encoding="utf-8") as f:
            self._cfg = yaml.safe_load(f)

    def __getitem__(self, key):
        return self._cfg[key]

    def get(self, dotted_key: str, default=None):
        """
        Retrieve nested config values using dot notation.
        Example: get("plots.aliases.GPT-4.1")
        """
        parts = dotted_key.split(".")
        node = self._cfg
        for p in parts:
            if isinstance(node, dict) and p in node:
                node = node[p]
            else:
                return default
        return node

    def as_dict(self):
        """Return full config dict."""
        return self._cfg
