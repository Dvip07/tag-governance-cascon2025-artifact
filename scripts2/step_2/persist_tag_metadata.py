import os
import json
import yaml

# ==== Config ====
HYBRID_DIR = "sbert_fix/hybrid"
TAG_META_OUT = "sbert_fix/hlj_tag_metadata"
CANONICAL_YAML = "sbert_fix/all_tags/step_4/canonical_tags_with_domain.yaml"
REJECTED_LOG = "sbert_fix/hlj_tag_metadata/rejected_tags.log"
GAP_WARNINGS = "sbert_fix/hlj_tag_metadata/canonical_lookup_warnings.log"

os.makedirs(TAG_META_OUT, exist_ok=True)

# --- Load canonical tags/alias/cluster info ---
with open(CANONICAL_YAML, "r", encoding="utf-8") as f:
    canonical_map = yaml.safe_load(f)

def get_canonical_info(tag):
    meta = canonical_map.get(tag)
    if meta is None:
        # Log missing tag for later gap analysis
        with open(GAP_WARNINGS, "a", encoding="utf-8") as warnlog:
            warnlog.write(f"[WARN] Tag not found in canonical_tags.yaml: '{tag}'\n")
        return {
            "aliases": [],
            "cluster_id": None,
            "domains": []
        }
    return {
        "aliases": meta.get("aliases", []),
        "cluster_id": meta.get("cluster_id", None),
        "domains": meta.get("domains", [])
    }

def main():
    count = 0
    rejected_all = []
    for model in os.listdir(HYBRID_DIR):
        model_path = os.path.join(HYBRID_DIR, model)
        if not os.path.isdir(model_path):
            continue
        for req_id in os.listdir(model_path):
            req_path = os.path.join(model_path, req_id)
            chunk_file = os.path.join(req_path, "all_chunks_full_validated.json")
            if not os.path.exists(chunk_file):
                continue
            with open(chunk_file, "r", encoding="utf-8") as f:
                hlj_chunks = json.load(f)
            for chunk in hlj_chunks:
                hlj_id = chunk.get("id", req_id)
                tags_meta = []
                tags_nlu = chunk.get("tag_nlu_validation", [])
                # Track rejected tags for central log
                rejected_tags = []
                for tmeta in tags_nlu:
                    canonical = tmeta["tag"]
                    cinfo = get_canonical_info(canonical)
                    tag_entry = {
                        "tag": canonical,
                        "aliases": cinfo["aliases"],
                        "cluster_id": cinfo["cluster_id"],
                        "domains": cinfo["domains"],
                        "model": tmeta.get("model"),
                        "version": tmeta.get("version"),
                        "score": tmeta.get("score"),
                        "confidence": tmeta.get("confidence"),
                        "validated": tmeta.get("validated"),
                        "validation_reason": tmeta.get("validation_reason"),
                        "original_tag": tmeta.get("original_tag"),
                        "method": tmeta.get("method")
                    }
                    tags_meta.append(tag_entry)
                    if tmeta.get("validated") is False:
                        # Add context so you can trace rejected tags back to HLJ
                        rejected_tags.append({
                            "hlj_id": hlj_id,
                            "tag": canonical,
                            "reason": tmeta.get("validation_reason"),
                            "model": model,
                            "req_id": req_id
                        })
                # Log all rejected tags for this HLJ
                if rejected_tags:
                    rejected_all.extend(rejected_tags)
                meta_out = {
                    "hlj_id": hlj_id,
                    "model": model,
                    "req_id": req_id,
                    "domain": chunk.get("domain"),
                    "title": chunk.get("title", ""),
                    "summary": chunk.get("summary", ""),
                    "tags_v1": chunk.get("tags_v1", []),
                    "tags_v2": chunk.get("tags_v2", []),
                    "tags_v3": chunk.get("tags_v3", []),
                    "all_tag_metadata": tags_meta
                }
                out_path = os.path.join(TAG_META_OUT, f"{hlj_id}.json")
                with open(out_path, "w", encoding="utf-8") as out_f:
                    json.dump(meta_out, out_f, indent=2, ensure_ascii=False)
                count += 1
                if count % 100 == 0:
                    print(f"✅ Processed {count} HLJs... latest: {hlj_id}")

    # Write rejected tags to central log
    with open(REJECTED_LOG, "w", encoding="utf-8") as rejlog:
        for rej in rejected_all:
            rejlog.write(json.dumps(rej, ensure_ascii=False) + "\n")
    print(f"✅ Saved metadata for {count} HLJs in {TAG_META_OUT}")
    print(f"📝 Central log of all rejected tags: {REJECTED_LOG}")
    print(f"📝 Any tag missing from canonical YAML was logged in: {GAP_WARNINGS}")

if __name__ == "__main__":
    main()
