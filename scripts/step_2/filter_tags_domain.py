import os
import json
import yaml
import csv

# ==== Config ====
HYBRID_DIR = "sbert_fix/hybrid"
CANONICAL_YAML = "sbert_fix/all_tags/step_4/canonical_tags_with_domain.yaml"
OUT_JSON = os.path.join(HYBRID_DIR, "domain_filtered_tags_per_hlj.json")
OUT_CSV = os.path.join(HYBRID_DIR, "domain_filtered_tags_per_hlj.csv")
WARN_LOG = os.path.join(HYBRID_DIR, "all_tag_mismatch_hljs.log")

# --- Load canonical tag domain mapping ---
with open(CANONICAL_YAML, "r", encoding="utf-8") as f:
    canonical_map = yaml.safe_load(f)
# canonical_map: tag -> {aliases: [...], cluster_id: ..., domains: [...]}

def canonicalize_tag(tag):
    """If tag is an alias, return canonical; else itself."""
    for can_tag, meta in canonical_map.items():
        aliases = meta.get("aliases", [])
        if tag == can_tag or tag in aliases:
            return can_tag
    return tag

def check_domain(tag, hlj_domain):
    tag_meta = canonical_map.get(tag, {})
    domains = tag_meta.get("domains", [])
    if hlj_domain in domains:
        return True, "whitelist"
    elif not domains:
        return None, "unknown_domain_in_tag"
    else:
        return False, "domain_mismatch"

def main():
    all_results = []
    flat_csv_rows = []
    total_tags, whitelist_tags, mismatch_tags, unknown_tags = 0, 0, 0, 0
    all_tag_mismatch_hljs = []

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
                # ---- FIELD MISMATCH CHECK ----
                # Try a few fallback locations for domain
                hlj_domain = (
                    chunk.get("domain")
                    or chunk.get("metadata", {}).get("domain")
                    or "unknown"
                )
                tags_v3 = [canonicalize_tag(tag) for tag in chunk.get("tags_v3", [])]
                tag_nlu_validation = chunk.get("tag_nlu_validation", [])
                tags_out = []
                mismatch_count, unknown_count, whitelist_count = 0, 0, 0
                for tag in tags_v3:
                    valid, reason = check_domain(tag, hlj_domain)
                    # --- BAYESIAN STUB ---
                    # if reason == "whitelist": do_bayesian_check(tag, hlj_id, hlj_domain)
                    tags_out.append({
                        "tag": tag,
                        "hlj_id": hlj_id,
                        "domain_valid": valid,
                        "validation_reason": reason,
                        "domain": hlj_domain,
                    })
                    total_tags += 1
                    if reason == "whitelist":
                        whitelist_count += 1
                        whitelist_tags += 1
                    elif reason == "domain_mismatch":
                        mismatch_count += 1
                        mismatch_tags += 1
                    elif reason == "unknown_domain_in_tag":
                        unknown_count += 1
                        unknown_tags += 1

                    # CSV row for every tag
                    flat_csv_rows.append({
                        "hlj_id": hlj_id,
                        "domain": hlj_domain,
                        "tag": tag,
                        "domain_valid": valid,
                        "validation_reason": reason,
                        "model": model,
                        "req_id": req_id
                    })
                # ---- Log HLJs with all tags mismatched/unknown ----
                if len(tags_out) > 0 and whitelist_count == 0:
                    all_tag_mismatch_hljs.append({
                        "hlj_id": hlj_id,
                        "domain": hlj_domain,
                        "tags": tags_out,
                        "model": model,
                        "req_id": req_id
                    })

                all_results.append({
                    "hlj_id": hlj_id,
                    "domain": hlj_domain,
                    "tags": tags_out
                })

    # Write output
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    # Write CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=flat_csv_rows[0].keys())
        writer.writeheader()
        writer.writerows(flat_csv_rows)
    # Write warning log
    with open(WARN_LOG, "w", encoding="utf-8") as f:
        for entry in all_tag_mismatch_hljs:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Domain filtering complete. Output: {OUT_JSON}")
    print(f"   Flat CSV written: {OUT_CSV}")
    print(f"   All-mismatch HLJs logged to: {WARN_LOG}")
    print(f"   Total HLJs processed: {len(all_results)}")
    print(f"   Total tags: {total_tags}")
    print(f"     ✅ Whitelisted: {whitelist_tags}")
    print(f"     ❓ Unknown: {unknown_tags}")
    print(f"     ❌ Domain mismatch: {mismatch_tags}")
    print(f"   HLJs with ALL tags mismatched/unknown: {len(all_tag_mismatch_hljs)}")

if __name__ == "__main__":
    main()
