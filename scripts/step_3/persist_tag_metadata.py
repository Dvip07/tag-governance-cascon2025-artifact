import os
import json
import yaml
import argparse
from datetime import datetime

from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run


def get_canonical_info(tag, canonical_map, gap_warn_path):
    meta = canonical_map.get(tag)
    if meta is None:
        with open(gap_warn_path, "a", encoding="utf-8") as warnlog:
            warnlog.write(f"[WARN] Tag not found in canonical_tags.yaml: '{tag}'\n")
        return {"aliases": [], "cluster_id": None, "domains": []}
    return {
        "aliases": meta.get("aliases", []),
        "cluster_id": meta.get("cluster_id", None),
        "domains": meta.get("domains", []),
    }


def main(cfg_path="configs/pipeline_v2.yaml"):
    cfg = ConfigResolver(cfg_path)
    run_id = get_current_run(cfg_path)
    run_dir = cfg.get("globals.run_dir")

    if not run_id or not run_dir:
        print("❌ Step 9 aborted: run_id/run_dir missing. Did you start the pipeline?")
        return

    # Inputs
    hybrid_dir = cfg.get("outputs.hybrid_dir")
    canonical_yaml = cfg.get("outputs.canonical_tags")

    if not hybrid_dir or not os.path.isdir(hybrid_dir):
        print("❌ Step 9 aborted: hybrid_dir missing. Did you run step_7?")
        return
    if not canonical_yaml or not os.path.exists(canonical_yaml):
        print("❌ Step 9 aborted: canonical_tags YAML missing. Did you run step_4?")
        return

    with open(canonical_yaml, "r", encoding="utf-8") as f:
        canonical_map = yaml.safe_load(f)

    # Outputs
    out_dir = os.path.join(run_dir, "step_9")
    os.makedirs(out_dir, exist_ok=True)
    tag_meta_out = os.path.join(out_dir, "hlj_tag_metadata")
    os.makedirs(tag_meta_out, exist_ok=True)
    rejected_log = os.path.join(out_dir, "rejected_tags.log")
    gap_warn_log = os.path.join(out_dir, "canonical_lookup_warnings.log")

    count = 0
    rejected_all = []

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
                tags_meta = []
                rejected_tags = []

                for tmeta in chunk.get("tag_nlu_validation", []):
                    canonical = tmeta["tag"]
                    cinfo = get_canonical_info(canonical, canonical_map, gap_warn_log)
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
                        "method": tmeta.get("method"),
                    }
                    tags_meta.append(tag_entry)

                    if tmeta.get("validated") is False:
                        rejected_tags.append({
                            "hlj_id": hlj_id,
                            "tag": canonical,
                            "reason": tmeta.get("validation_reason"),
                            "model": model,
                            "req_id": req_id,
                        })

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
                    "all_tag_metadata": tags_meta,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }

                out_path = os.path.join(tag_meta_out, f"{hlj_id}.json")
                with open(out_path, "w", encoding="utf-8") as out_f:
                    json.dump(meta_out, out_f, indent=2, ensure_ascii=False)

                count += 1
                if count % 100 == 0:
                    print(f"✅ Processed {count} HLJs... latest: {hlj_id}")

    # Write rejected log
    with open(rejected_log, "w", encoding="utf-8") as rejlog:
        for rej in rejected_all:
            rejlog.write(json.dumps(rej, ensure_ascii=False) + "\n")

    print(f"✅ Saved metadata for {count} HLJs in {tag_meta_out}")
    print(f"📝 Rejected tags log: {rejected_log}")
    print(f"📝 Lookup gaps log: {gap_warn_log}")

    # Update YAML
    cfg.set("outputs.hlj_tag_metadata", tag_meta_out)
    cfg.set("outputs.rejected_tags_log", rejected_log)
    cfg.set("outputs.gap_warnings_log", gap_warn_log)
    cfg.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 9: Persist tag metadata for each HLJ")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml")
    args = parser.parse_args()
    main(args.config)
