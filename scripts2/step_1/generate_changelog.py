import os
import yaml

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def render_tag_changes(audit):
    lines = []
    lines.append("| Tag | Action   | Validation | Similarity | Context           | Timestamp               |")
    lines.append("|-----|----------|------------|------------|-------------------|-------------------------|")

    orig = set(audit.get("original_tags", []))
    validated = set(audit.get("validated_tags", []))

    tag_meta = {}
    for t in audit.get("validation_details", []):
        tag_meta[t.get("original_tag", t.get("canonical_tag", ""))] = t
        tag_meta[t.get("canonical_tag", t.get("original_tag", ""))] = t

    for tag in sorted(orig | validated):
        if tag in orig and tag in validated:
            action = "kept"
        elif tag in orig:
            action = "dropped"
        else:
            action = "added"

        val = tag_meta.get(tag, {})
        lines.append(f"| {tag} | {action} | {val.get('validation_status','')} | {val.get('similarity','')} | "
                     f"{val.get('context','')} | {val.get('timestamp','')} |")
    return "\n".join(lines)

def main():
    SBERT_FIX_BASE = "sbert_fix"
    if not os.path.exists(SBERT_FIX_BASE):
        print(f"❌ Base folder not found: {SBERT_FIX_BASE}")
        return

    for model in os.listdir(SBERT_FIX_BASE):
        model_dir = os.path.join(SBERT_FIX_BASE, model)
        if not os.path.isdir(model_dir):
            continue
        for req in os.listdir(model_dir):
            req_dir = os.path.join(model_dir, req)
            audit_path = os.path.join(req_dir, "tag_audit.yaml")
            out_path = os.path.join(req_dir, "changelog.md")

            ensure_dir(req_dir)

            if not os.path.exists(audit_path):
                print(f"⚠️ Missing audit: {audit_path}")
                with open(out_path, "w") as f:
                    f.write(f"# 📝 Changelog for `{req}` — **{model}**\n\n❌ No audit.yaml found.\n")
                continue

            with open(audit_path) as f:
                try:
                    audits = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(f"❌ YAML error in {audit_path}: {e}")
                    continue

            if not audits or not isinstance(audits, list):
                with open(out_path, "w") as f:
                    f.write(f"# 📝 Changelog for `{req}` — **{model}**\n\n⚠️ audit.yaml is empty or malformed.\n")
                print(f"⚠️ Skipped: Empty or invalid audit in {req_dir}")
                continue

            lines = [f"# 📝 Changelog for `{req}` — **{model}**\n"]
            for audit in audits:
                lines.append(f"## 🔹 HLJ: `{audit.get('hlj_id', 'UNKNOWN')}`\n")
                lines.append(f"**Original tags:** `{audit.get('original_tags', [])}`")
                lines.append(f"**Validated tags:** `{audit.get('validated_tags', [])}`")
                lines.append(f"**Tags added:** `{audit.get('tags_added', [])}`")
                lines.append(f"**Tags dropped:** `{audit.get('tags_dropped', [])}`")
                lines.append(f"**Tags kept:** `{audit.get('tags_kept', [])}`\n")
                lines.append("### 🔍 Tag Changes")
                lines.append(render_tag_changes(audit))
                lines.append("")

            with open(out_path, "w") as f:
                f.write("\n".join(lines))
            print(f"✅ Changelog written to {out_path}")

if __name__ == "__main__":
    main()
