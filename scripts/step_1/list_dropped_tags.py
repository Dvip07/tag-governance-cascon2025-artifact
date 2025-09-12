import os
import yaml
import csv

SBERT_FIX_BASE = "sbert_fix/gpt41"  # Change this if needed
OUTPUT_FILE = "sbert_fix/gpt41/dropped_tags.csv"

def list_dropped_tags_to_file():
    rows = []
    for req in os.listdir(SBERT_FIX_BASE):
        path = os.path.join(SBERT_FIX_BASE, req, "tag_audit.yaml")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            audits = yaml.safe_load(f)

        for audit in audits:
            dropped = audit.get("tags_dropped", [])
            if dropped:
                for tag in dropped:
                    rows.append({
                        "requirement": req,
                        "hlj_id": audit["hlj_id"],
                        "dropped_tag": tag
                    })

    if not rows:
        print("😇 No dropped tags found.")
        return

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["requirement", "hlj_id", "dropped_tag"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Dropped tags exported to {OUTPUT_FILE}")

if __name__ == "__main__":
    list_dropped_tags_to_file()
