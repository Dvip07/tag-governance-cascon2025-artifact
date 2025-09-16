import os
import csv
import json
import argparse
from collections import defaultdict, Counter
from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run

def main(cfg_path="configs/pipeline_v2.yaml"):
    cfg = ConfigResolver(cfg_path)
    run_id = get_current_run(cfg_path)
    run_dir = cfg.get("globals.run_dir")

    # === Paths from YAML ===
        # === Paths from YAML ===
    deduped_csv = cfg.get("outputs.deduplicated_tags")
    token_filtered_csv = cfg.get("outputs.tags_token_filtered")
    dropped_csv = cfg.get("outputs.step2_dropped")
    out_json = os.path.join(run_dir, "step_6", "topk_tags_per_hlj.json")

    # sanity check deduped
    if not deduped_csv or not os.path.exists(deduped_csv):
        print("❌ Step 6 aborted: deduplicated_tags CSV missing. Did you run step_5?")
        return

    # --- robust handling for token_filtered ---
    use_step2_all = False
    if not token_filtered_csv or not os.path.exists(token_filtered_csv) or os.path.getsize(token_filtered_csv) == 0:
        # fallback to step2_all
        token_filtered_csv = cfg.get("outputs.step2_all")
        if not token_filtered_csv or not os.path.exists(token_filtered_csv):
            print("❌ Step 6 aborted: no usable tag CSV (neither token_filtered nor step2_all).")
            return
        use_step2_all = True

    if use_step2_all:
        print(f"⚠️ Using step2_all instead of token_filtered: {token_filtered_csv}")
    else:
        print(f"✅ Using token_filtered: {token_filtered_csv}")


    # if not deduped_csv or not os.path.exists(deduped_csv):
    #     print("❌ Step 6 aborted: deduplicated_tags CSV missing. Did you run step_5?")
    #     return
    # if not token_filtered_csv or not os.path.exists(token_filtered_csv):
    #     print("❌ Step 6 aborted: token_filtered CSV missing. Did you run step_2?")
    #     return

    os.makedirs(os.path.dirname(out_json), exist_ok=True)

    # === Params ===
    top_k = cfg.get("step6.top_k", 9)

    # Step 1: Load dropped tags
    dropped_set = set()
    if dropped_csv and os.path.exists(dropped_csv):
        with open(dropped_csv, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dropped_set.add((row['tag'], row['hlj_id']))

    # Step 2: Map HLJ to canonical tags
    hlj2tags = defaultdict(list)

    canon_alias_map = defaultdict(set)  # alias -> canonical_tag
    with open(deduped_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            alias = row['alias']
            canonical = row['canonical_tag']
            canon_alias_map[alias].add(canonical)

    # Step 3: Walk token-filtered tags
    with open(token_filtered_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hlj_id = row['hlj_id']
            tag = row['tag']
            if (tag, hlj_id) in dropped_set:
                continue
            version = row.get('version', 'v3')
            model = row.get('model', 'unknown')
            conf_val = row.get('confidence')
            try:
                confidence = float(conf_val)
            except (TypeError, ValueError):
                confidence = None

            canonicals = canon_alias_map.get(tag, set())
            for canonical in canonicals:
                detail = {
                    "tag": canonical,
                    "original_tag": tag,
                    "model": model,
                    "version": version,
                    "confidence": confidence,
                    "method": "dedup_canonical"
                }
                hlj2tags[hlj_id].append(detail)

    # Step 4: Frequency ranking
    hlj_outputs = []
    for hlj_id, taglist in hlj2tags.items():
        freq = Counter([d["tag"] for d in taglist])
        ranked = sorted(
            taglist,
            key=lambda x: (-freq[x["tag"]], -(x["confidence"] or 0))
        )
        topk_tags = []
        seen = set()
        for d in ranked:
            if d["tag"] in seen:
                continue
            score = freq[d["tag"]]
            topk_tags.append({
                "tag": d["tag"],
                "score": score,
                "method": d["method"],
                "model": d["model"],
                "version": d["version"],
                "confidence": d["confidence"],
                "original_tag": d["original_tag"]
            })
            seen.add(d["tag"])
            if len(topk_tags) == top_k:
                break
        hlj_outputs.append({"hlj_id": hlj_id, "tags": topk_tags})

    # Step 5: Save JSON
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(hlj_outputs, f, indent=2, ensure_ascii=False)

    print(f"✅ Top-K tag scoring complete for {len(hlj_outputs)} HLJs.")
    print(f"Output: {out_json}")

    # Update YAML
    cfg.set("outputs.topk_tags", out_json)
    cfg.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 6: Top-K scoring per HLJ")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml", help="Path to pipeline config YAML")
    args = parser.parse_args()
    main(args.config)
