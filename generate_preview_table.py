import json
from pathlib import Path

PREVIEW_PATH = Path("preview.jsonl")
OUTPUT_PATH = Path("README_preview.md")

def load_preview(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]

def to_markdown_table(rows, max_rows=5):
    header = "| hlj_id | domain | num_tags | example_tags |\n"
    header += "|--------|----------|----------|---------------|\n"
    body = ""
    for row in rows[:max_rows]:
        body += f"| {row.get('hlj_id','-')} | {row.get('domain','-')} | {row.get('num_tags','-')} | {row.get('example_tags','-')} |\n"
    return header + body

def main():
    rows = load_preview(PREVIEW_PATH)
    md_table = to_markdown_table(rows)

    section = (
        "## Quick Preview Example\n\n"
        "Below is a small representative sample (50 HLJ entries across FinTech and SaaS) "
        "generated automatically from `preview.jsonl`.\n\n"
        f"{md_table}\n"
        "> **Full preview:** [View 50-entry sample →](./preview.jsonl)\n\n---\n"
    )

    OUTPUT_PATH.write_text(section)
    print(f"✅ Wrote markdown preview to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
