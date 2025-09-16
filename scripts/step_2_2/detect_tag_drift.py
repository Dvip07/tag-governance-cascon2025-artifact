import yaml
import os
from datetime import datetime

# === CONFIG ===
CTD_NEW = "eval/sbert_fix/all_tags/step_4/canonical_tags_with_domain.yaml"
CTD_OLD = "eval/sbert_fix/all_tags/step_4/canonical_tags_prev.yaml"  # You must keep this backup!
TAG_DRIFT_OUT = "eval/sbert_fix/all_tags/step_10/tag_drift_report.yaml"
AUTO_PR_YML = "eval/sbert_fix/all_tags/step_10/auto_pr_alias_update.yml"
os.makedirs(os.path.dirname(TAG_DRIFT_OUT), exist_ok=True)

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

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
    # Changed aliases and domains
    for tag in sorted(new_keys & old_keys):
        old_aliases = set(ctd_old[tag].get("aliases", []))
        new_aliases = set(ctd_new[tag].get("aliases", []))
        if old_aliases != new_aliases:
            drift_report["changed_aliases"].append({
                "canonical": tag,
                "prev_aliases": sorted(old_aliases),
                "new_aliases": sorted(new_aliases),
            })
        old_domains = set(ctd_old[tag].get("domains", []))
        new_domains = set(ctd_new[tag].get("domains", []))
        if old_domains != new_domains:
            drift_report["domain_changes"].append({
                "canonical": tag,
                "prev_domains": sorted(old_domains),
                "new_domains": sorted(new_domains),
            })
        if old_aliases == new_aliases and old_domains == new_domains:
            drift_report["unchanged"].append(tag)
    return drift_report

def write_auto_pr_yaml(drift_report):
    # Summarize changes for a GitHub Action PR
    updates = []
    if drift_report["added_canonicals"]:
        updates.append(f"**Added canonicals:** {', '.join(drift_report['added_canonicals'])}")
    if drift_report["removed_canonicals"]:
        updates.append(f"**Removed canonicals:** {', '.join(drift_report['removed_canonicals'])}")
    if drift_report["changed_aliases"]:
        updates.append(f"**Changed aliases:** {[f'{x['canonical']}: {x['prev_aliases']} → {x['new_aliases']}' for x in drift_report['changed_aliases']]}")
    if drift_report["domain_changes"]:
        updates.append(f"**Domain changes:** {[f'{x['canonical']}: {x['prev_domains']} → {x['new_domains']}' for x in drift_report['domain_changes']]}")
    body = "\n".join(updates) or "No changes detected."
    # Output GitHub workflow YAML (simplified example)
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
                ]
            }
        }
    }
    with open(AUTO_PR_YML, "w", encoding="utf-8") as f:
        yaml.dump(auto_pr, f, sort_keys=False)
    print(f"🟢 Auto-PR workflow saved: {AUTO_PR_YML}")

def main():
    ctd_new = load_yaml(CTD_NEW)
    ctd_old = load_yaml(CTD_OLD)
    drift_report = compare_ctd(ctd_old, ctd_new)
    with open(TAG_DRIFT_OUT, "w", encoding="utf-8") as f:
        yaml.dump(drift_report, f, sort_keys=False)
    print(f"✅ Drift report saved: {TAG_DRIFT_OUT}")
    write_auto_pr_yaml(drift_report)
    print("✅ Drift PR YAML saved for GitHub Actions.")

if __name__ == "__main__":
    main()
