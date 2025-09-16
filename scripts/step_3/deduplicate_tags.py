import os
import csv
import json
import argparse
from sentence_transformers import SentenceTransformer, util
from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run

def sbert_sim(a, b, sbert):
    emb_a = sbert.encode(a, convert_to_tensor=True)
    emb_b = sbert.encode(b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b).item())

def main(cfg_path="configs/pipeline_v2.yaml"):
    cfg = ConfigResolver(cfg_path)
    run_id = get_current_run(cfg_path)
    run_dir = cfg.get("globals.run_dir")

    # === Paths from YAML ===
    cluster_csv = cfg.get("outputs.tag_clusters")
    alias_json = cfg.get("outputs.tag_alias_map")

    if not cluster_csv or not os.path.exists(cluster_csv):
        print("❌ Step 5 aborted: tag_clusters CSV missing. Did you run step_3 (clustering)?")
        return
    if not alias_json or not os.path.exists(alias_json):
        print("❌ Step 5 aborted: tag_alias_map JSON missing. Did you run step_4 (canonical labels)?")
        return

    out_dir = os.path.join(run_dir, "step_5")
    os.makedirs(out_dir, exist_ok=True)
    dedupe_out = os.path.join(out_dir, "deduplicated_tags.csv")
    dedupe_log = os.path.join(out_dir, "deduplicate_audit_log.json")

    # === Params ===
    sbert_model = cfg.get("step5.sbert_model", "all-MiniLM-L6-v2")
    threshold = cfg.get("step5.deduplication_threshold", 0.83)

    # === Load tag clusters ===
    clusters = {}
    with open(cluster_csv, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row['cluster_id']
            tag = row['tag']
            clusters.setdefault(cid, []).append(tag)

    # === Load alias map (from canonical labels step) ===
    with open(alias_json, encoding='utf-8') as f:
        alias_map = json.load(f)

    # === Load SBERT ===
    sbert = SentenceTransformer(sbert_model)

    deduped_rows = []
    audit_log = []

    for canonical, meta in alias_map.items():
        cid = meta['cluster_id']
        version = meta.get('version', 'v3')
        aliases = meta.get('aliases', [])
        for alias in aliases:
            sim = sbert_sim(canonical, alias, sbert)
            method = []
            if alias in clusters.get(cid, []):
                method.append("cluster")
            if sim >= threshold:
                method.append("sbert")
            method = "+".join(method) if method else "manual"

            deduped_rows.append({
                "canonical_tag": canonical,
                "alias": alias,
                "method": method,
                "similarity": f"{sim:.3f}",
                "cluster_id": cid,
                "version": version
            })
            audit_log.append({
                "canonical": canonical,
                "alias": alias,
                "cluster_id": cid,
                "similarity": sim,
                "method": method,
                "version": version
            })

        # Canonical tag itself
        deduped_rows.append({
            "canonical_tag": canonical,
            "alias": canonical,
            "method": "self",
            "similarity": "1.000",
            "cluster_id": cid,
            "version": version
        })

    # ==== Save deduplicated tags CSV ====
    with open(dedupe_out, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["canonical_tag", "alias", "method", "similarity", "cluster_id", "version"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduped_rows)
    print(f"✅ Saved deduplicated tags to {dedupe_out}")

    # ==== Save audit log ====
    with open(dedupe_log, 'w', encoding='utf-8') as f:
        json.dump(audit_log, f, indent=2, ensure_ascii=False)
    print(f"📝 Audit log saved to {dedupe_log}")

    print(f"🔎 Total deduplication decisions: {len(deduped_rows)}")
    print(f"🔎 Unique canonicals: {len(alias_map)}")

    # Update YAML
    cfg.set("outputs.deduplicated_tags", dedupe_out)
    cfg.set("outputs.deduplication_audit_log", dedupe_log)
    cfg.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 5: Deduplicate tags with SBERT + cluster checks")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml", help="Path to pipeline config YAML")
    args = parser.parse_args()
    main(args.config)
