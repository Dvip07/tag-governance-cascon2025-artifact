import os
import yaml
import argparse
from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def render_tag_changes(audit):
    lines = []
    lines.append("| Tag | Action   | Validation | Similarity | Context | Timestamp |")
    lines.append("|-----|----------|------------|------------|---------|-----------|")

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
        lines.append(
            f"| {tag} | {action} | {val.get('validation_status','')} | "
            f"{val.get('similarity','')} | {val.get('context','')} | {val.get('timestamp','')} |"
        )
    return "\n".join(lines)

def main(cfg, run_id=None):
    # resolve paths
    run_dir = cfg.get("globals.run_dir")
    sbert_fix_base = cfg.get("outputs.sbert_fix", "sbert_fix")
    out_dir = os.path.join(run_dir, "changelogs")
    ensure_dir(out_dir)

    if not os.path.exists(sbert_fix_base):
        print(f"❌ Base folder not found: {sbert_fix_base}")
        return

    for model in os.listdir(sbert_fix_base):
        model_dir = os.path.join(sbert_fix_base, model)
        if not os.path.isdir(model_dir):
            continue
        for req in os.listdir(model_dir):
            req_dir = os.path.join(model_dir, req)
            audit_path = os.path.join(req_dir, "tag_audit.yaml")
            out_path = os.path.join(out_dir, model, f"{req}.md")
            ensure_dir(os.path.dirname(out_path))

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
                    f.write(f"# 📝 Changelog for `{req}` — **{model}**\n\n⚠️ audit.yaml empty or malformed.\n")
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

    # update cfg outputs
    cfg.set("outputs.changelogs_dir", out_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate markdown changelogs from audits")
    parser.add_argument("--config", default="configs/pipeline_v1.yaml")
    args = parser.parse_args()

    cfg = ConfigResolver(args.config)
    run_id = get_current_run(args.config)
    main(cfg, run_id=run_id)
