import os
import yaml
from datetime import datetime
import argparse

# import_path = os.path.join("configs", "pipeline_v2.yaml")

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# def load_yaml(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return yaml.safe_load(f)

def compare_ctd(ctd_old, ctd_new):
    drift_report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "added_canonicals": [],
        "removed_canonicals": [],
        "changed_aliases": [],
        "domain_changes": [],
        "unchanged": [],
    }
    # Added/removed canonicals
    old_keys, new_keys = set(ctd_old), set(ctd_new)
    drift_report["added_canonicals"] = sorted(list(new_keys - old_keys))
    drift_report["removed_canonicals"] = sorted(list(old_keys - new_keys))
    # Changed aliases/domains
    for tag in sorted(new_keys & old_keys):
        old_aliases = set(ctd_old[tag].get("aliases", []))
        new_aliases = set(ctd_new[tag].get("aliases", []))
        old_domains = set(ctd_old[tag].get("domains", []))
        new_domains = set(ctd_new[tag].get("domains", []))

        if old_aliases != new_aliases:
            drift_report["changed_aliases"].append({
                "canonical": tag,
                "prev_aliases": sorted(old_aliases),
                "new_aliases": sorted(new_aliases),
            })
        if old_domains != new_domains:
            drift_report["domain_changes"].append({
                "canonical": tag,
                "prev_domains": sorted(old_domains),
                "new_domains": sorted(new_domains),
            })
        if old_aliases == new_aliases and old_domains == new_domains:
            drift_report["unchanged"].append(tag)
    return drift_report

def write_auto_pr_yaml(drift_report, out_path):
    lines = []
    if drift_report["added_canonicals"]:
        lines.append(f"**Added canonicals:** {', '.join(drift_report['added_canonicals'])}")
    if drift_report["removed_canonicals"]:
        lines.append(f"**Removed canonicals:** {', '.join(drift_report['removed_canonicals'])}")
    if drift_report["changed_aliases"]:
        for x in drift_report["changed_aliases"]:
            lines.append(f"Changed aliases for {x['canonical']}: {x['prev_aliases']} → {x['new_aliases']}")
    if drift_report["domain_changes"]:
        for x in drift_report["domain_changes"]:
            lines.append(f"Domain change for {x['canonical']}: {x['prev_domains']} → {x['new_domains']}")
    body = "\n".join(lines) or "No changes detected."

    auto_pr = {
        "name": "CTD Drift Auto-PR",
        "on": {"workflow_dispatch": None},
        "jobs": {
            "create-pr": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"run": "git checkout -b ctd-drift-auto"},
                    {"run": "git add ."},
                    {"run": 'git commit -m "Auto-update CTD for drift"'},
                    {"run": "git push origin ctd-drift-auto"},
                    {"run": f'gh pr create --title "CTD Drift: Auto-update" --body "{body}"'},
                ],
            }
        },
    }
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(auto_pr, f, sort_keys=False)

def main(cfg_path):
    cfg = load_yaml(cfg_path)
    run_dir = cfg["globals"]["run_dir"]

    # Step10 paths
    ctd_new = os.path.join(run_dir, "step_4", "canonical_tags_with_domain.yaml")
    ctd_old = cfg["step10"]["prev_ctd_path"]
    drift_out = os.path.join(run_dir, "step_10", "tag_drift_report.yaml")
    auto_pr_yml = os.path.join(run_dir, "step_10", "auto_pr_alias_update.yml")
    os.makedirs(os.path.dirname(drift_out), exist_ok=True)

    ctd_new_data = load_yaml(ctd_new)
    ctd_old_data = load_yaml(ctd_old)

    drift_report = compare_ctd(ctd_old_data, ctd_new_data)
    with open(drift_out, "w", encoding="utf-8") as f:
        yaml.dump(drift_report, f, sort_keys=False)
    print(f"✅ Drift report saved: {drift_out}")

    write_auto_pr_yaml(drift_report, auto_pr_yml)
    print(f"✅ Auto-PR YAML saved: {auto_pr_yml}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 9: Detect tag drift across runs")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml", help="Path to pipeline config YAML")
    args = parser.parse_args()

    main(args.config)

