import pathlib

BASE_DIR = pathlib.Path("eval/raw_requirement")

# Define domain-specific ranges
domain_ranges = {
    "FinTech": range(1, 16),   # req-001 to req-015
    "SaaS": range(16, 31)      # req-016 to req-030
}

# Template placeholder text
def generate_stub(req_id: str, domain: str) -> str:
    return f"""# Requirement {req_id} ({domain})\n\nThis is a placeholder requirement document for `{req_id}` in the `{domain}` domain.\n\nReplace this text with actual stakeholder input or simulated raw requirement text.\n"""

# Scaffold files
for domain, req_range in domain_ranges.items():
    domain_dir = BASE_DIR / domain
    domain_dir.mkdir(parents=True, exist_ok=True)
    for i in req_range:
        req_id = f"req-{i:03d}"
        file_path = domain_dir / f"{req_id}.md"
        if not file_path.exists():
            file_path.write_text(generate_stub(req_id, domain), encoding="utf-8")
            print(f"✅ Created: {file_path}")
        else:
            print(f"⚠️  Skipped (already exists): {file_path}")
