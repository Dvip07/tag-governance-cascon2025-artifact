import os
import json
import yaml
import csv
import argparse
from collections import defaultdict

from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run


def canonicalize_tag(tag: str, canonical_map: dict) -> str:
    """If tag is an alias, return canonical; else itself."""
    for can_tag, meta in canonical_map.items():
        aliases = meta.get("aliases", [])
        if tag == can_tag or tag in aliases:
            return can_tag
    return tag


def check_domain(tag: str, hlj_domain: str, canonical_map: dict):
    tag_meta = canonical_map.get(tag, {})
    domains = tag_meta.get("domains", [])
    if hlj_domain in domains:
        return True, "whitelist"
    elif not domains:
        return None, "unknown_domain_in_tag"
    else:
        return False, "domain_mismatch"


def main(cfg_path="configs/pipeline_v2.yaml"):
    cfg = ConfigResolver(cfg_path)
    run_id = get_current_run(cfg_path)
    run_dir = cfg.get("globals.run_dir")

    if not run_id or not run_dir:
        print("❌ Step 8 aborted: run_id/run_dir missing. Did you start the pipeline?")
        return

    # --- Inputs ---
    canonical_yaml = cfg.get("outputs.canonical_tags")
    hybrid_dir = cfg.get("outputs.hybrid_dir")
    if not canonical_yaml or not os.path.exists(canonical_yaml):
        print("❌ Step 8 aborted: canonical_tags YAML missing. Did you run step_4?")
        return
    if not hybrid_dir or not os.path.isdir(hybrid_dir):
        print("❌ Step 8 aborted: hybrid_dir missing. Did you run step_7?")
        return

    # --- Outputs (scoped to run) ---
    out_dir = os.path.join(run_dir, "step_8")
    os.makedirs(out_dir, exist_ok=True)
    out_json = os.path.join(out_dir, "domain_filtered_tags_per_hlj.json")
    out_csv = os.path.join(out_dir, "domain_filtered_tags_per_hlj.csv")
    warn_log = os.path.join(out_dir, "all_tag_mismatch_hljs.log")

    # --- Load canonical map ---
    with open(canonical_yaml, "r", encoding="utf-8") as f:
        canonical_map = yaml.safe_load(f)

    all_results = []
    flat_csv_rows = []
    total_tags, whitelist_tags, mismatch_tags, unknown_tags = 0, 0, 0, 0
    all_tag_mismatch_hljs = []

    # --- Iterate hybrid models/reqs ---
    for model in os.listdir(hybrid_dir):
        model_path = os.path.join(hybrid_dir, model)
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
                hlj_domain = (
                    chunk.get("domain")
                    or chunk.get("metadata", {}).get("domain")
                    or "unknown"
                )
                tags_v3 = [canonicalize_tag(tag, canonical_map) for tag in chunk.get("tags_v3", [])]
                tags_out = []
                whitelist_count = 0
                for tag in tags_v3:
                    valid, reason = check_domain(tag, hlj_domain, canonical_map)
                    tags_out.append({
                        "tag": tag,
                        "hlj_id": hlj_id,
                        "domain_valid": valid,
                        "validation_reason": reason,
                        "domain": hlj_domain,
                    })
                    total_tags += 1
                    if reason == "whitelist":
                        whitelist_tags += 1
                        whitelist_count += 1
                    elif reason == "domain_mismatch":
                        mismatch_tags += 1
                    elif reason == "unknown_domain_in_tag":
                        unknown_tags += 1

                    flat_csv_rows.append({
                        "hlj_id": hlj_id,
                        "domain": hlj_domain,
                        "tag": tag,
                        "domain_valid": valid,
                        "validation_reason": reason,
                        "model": model,
                        "req_id": req_id,
                    })

                if tags_out and whitelist_count == 0:
                    all_tag_mismatch_hljs.append({
                        "hlj_id": hlj_id,
                        "domain": hlj_domain,
                        "tags": tags_out,
                        "model": model,
                        "req_id": req_id,
                    })

                all_results.append({
                    "hlj_id": hlj_id,
                    "domain": hlj_domain,
                    "tags": tags_out,
                })

    # --- Write outputs ---
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    if flat_csv_rows:
        with open(out_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(flat_csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(flat_csv_rows)

    with open(warn_log, "w", encoding="utf-8") as f:
        for entry in all_tag_mismatch_hljs:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Domain filtering complete. JSON: {out_json}")
    print(f"   CSV: {out_csv}")
    print(f"   All-mismatch HLJs log: {warn_log}")
    print(f"   Total HLJs: {len(all_results)} | Tags: {total_tags}")
    print(f"     ✅ Whitelisted: {whitelist_tags}")
    print(f"     ❓ Unknown: {unknown_tags}")
    print(f"     ❌ Mismatched: {mismatch_tags}")
    print(f"   HLJs with ALL tags mismatched/unknown: {len(all_tag_mismatch_hljs)}")

    # Update YAML outputs
    cfg.set("outputs.domain_filtered_tags", out_json)
    cfg.set("outputs.domain_filtered_csv", out_csv)
    cfg.set("outputs.domain_filtered_warnlog", warn_log)
    cfg.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 8: Domain filtering of validated tags")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml")
    args = parser.parse_args()
    main(args.config)
