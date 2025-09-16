import os
import json
import yaml
from datetime import datetime
import argparse
import spacy
from sentence_transformers import SentenceTransformer, util

from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run


# ========= Tag Utilities =========
def normalize_tag(tag: str):
    return tag.lower().replace("-", " ").strip()


def build_reverse_cluster_map(alias_map):
    reverse_map = {}
    for canonical_tag, cluster_info in alias_map.items():
        aliases = cluster_info.get("aliases", [])
        all_names = [canonical_tag] + aliases
        for name in all_names:
            name_normalized = normalize_tag(name)
            reverse_map[name_normalized] = {
                "canonical_tag": canonical_tag,
                "cluster_id": canonical_tag,
                "is_alias": name_normalized != normalize_tag(canonical_tag)
            }
    return reverse_map


def get_canonical_tag(tag, reverse_map):
    return reverse_map.get(normalize_tag(tag), {}).get("canonical_tag", tag)


def get_cluster_id(tag, reverse_map):
    return reverse_map.get(normalize_tag(tag), {}).get("cluster_id", None)


def was_alias(tag, reverse_map):
    return reverse_map.get(normalize_tag(tag), {}).get("is_alias", False)


def validate_tag(original_tag, canonical_tag, contexts, nlp, sbert, sbert_threshold=0.68):
    tag_lower = canonical_tag.lower()
    for ctx_name, ctx_text in contexts.items():
        doc = nlp(ctx_text)
        noun_chunks = [chunk.text.lower() for chunk in doc.noun_chunks]
        if tag_lower in noun_chunks or tag_lower in ctx_text.lower().split():
            return "direct", 1.0, ctx_name

    tag_emb = sbert.encode([canonical_tag])[0]
    for ctx_name, ctx_text in contexts.items():
        ctx_emb = sbert.encode([ctx_text])[0]
        sim = util.cos_sim([tag_emb], [ctx_emb]).item()
        if sim >= sbert_threshold:
            return "semantic", sim, ctx_name
    return "none", 0.0, None


def load_flat_hljs(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list) and all(isinstance(x, dict) and "id" in x and "tags" in x for x in data):
        return data
    else:
        raise ValueError("Expected trimmed HLJs (flat list). Bad structure in file: " + path)


# ========= Main =========
def main(cfg, run_id=None, **kwargs):
    # --- resolve paths from config
    base_dir = cfg.get("step4.base_output", "output")
    raw_req_base = cfg.get("step4.raw_requirements", "raw_requirement")
    domains = cfg.get("step4.domains", ["FinTech", "SaaS"])
    hlj_subpath = cfg.get("step4.hlj_subpath", "hlj/trim_merged/all_trimmed_hljs.json")
    alias_map_path = cfg.get("outputs.tag_alias_map")
    if not alias_map_path or not os.path.exists(alias_map_path):
        raise RuntimeError("❌ Alias map path not set or file missing. Did you run tag_alias_mapping first?")

    sbert_fix_base = cfg.get("outputs.sbert_fix", "sbert_fix")
    sbert_threshold = cfg.get("step4.sbert_threshold", 0.68)

    # --- load models
    nlp = spacy.load("en_core_web_sm")
    sbert = SentenceTransformer(cfg.get("step4.embedding_model", "all-MiniLM-L6-v2"))

    # --- load alias map
    if os.path.exists(alias_map_path):
        with open(alias_map_path) as f:
            tag_alias_map = json.load(f)
    else:
        tag_alias_map = {}
    reverse_map = build_reverse_cluster_map(tag_alias_map)

    alias_debug_log = []

    # --- per-run folder
    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    run_dir = cfg.get("globals.run_dir", os.path.join("eval/runs/v1/", run_id))
    out_root = os.path.join(run_dir, "validated")
    os.makedirs(out_root, exist_ok=True)
    os.makedirs(run_dir, exist_ok=True)

    for model in os.listdir(base_dir):
        model_dir = os.path.join(base_dir, model)
        if not os.path.isdir(model_dir):
            continue
        print(f"Validating model: {model}")
        for req in os.listdir(model_dir):
            req_dir = os.path.join(model_dir, req)
            hlj_path = os.path.join(req_dir, hlj_subpath)
            if not os.path.exists(hlj_path):
                print(f"Missing: {hlj_path}")
                continue

            # --- detect raw requirement domain
            domain = None
            for dom in domains:
                raw_req_file = os.path.join(raw_req_base, dom, f"{req}.md")
                if os.path.exists(raw_req_file):
                    domain = dom
                    break
            if not domain:
                print(f"Raw requirement missing for {req}")
                continue

            with open(os.path.join(raw_req_base, domain, f"{req}.md")) as f:
                raw_req_text = f.read()

            try:
                hlj_list = load_flat_hljs(hlj_path)
            except Exception as e:
                print(f"Error loading HLJ: {hlj_path}: {e}")
                continue

            validated_hljs = []
            audit_logs = []
            for hlj in hlj_list:
                contexts = {
                    "title": hlj.get("title", ""),
                    "summary": hlj.get("summary", ""),
                    "source_fragment": hlj.get("reasoning", {}).get("source_summary_fragment", ""),
                    "mapped_concepts": " ".join(hlj.get("reasoning", {}).get("mapped_concepts", [])),
                    "raw_requirement": raw_req_text
                }
                tag_results = []
                new_tags = []
                for tag in hlj.get("tags", []):
                    canonical = get_canonical_tag(tag, reverse_map)
                    cluster_id = get_cluster_id(tag, reverse_map)
                    alias_flag = was_alias(tag, reverse_map)
                    if alias_flag:
                        alias_debug_log.append({
                            "hlj_id": hlj.get("id", ""),
                            "original_tag": tag,
                            "canonical_tag": canonical,
                            "model": model,
                            "req_id": req,
                            "cluster_id": cluster_id
                        })

                    status, sim, ctx = validate_tag(tag, canonical, contexts, nlp, sbert, sbert_threshold)
                    tag_result = {
                        "original_tag": tag,
                        "canonical_tag": canonical,
                        "matched_tag": canonical,
                        "tag_origin_cluster_id": cluster_id,
                        "original_confidence": next(
                            (t.get("confidence", None)
                             for t in hlj.get("reasoning", {}).get("tag_metadata_reference", [])
                             if t["tag"] == tag), None),
                        "validation_status": status,
                        "similarity": sim,
                        "context": ctx,
                        "alias_used": alias_flag,
                        "timestamp": datetime.utcnow().isoformat() + "Z"
                    }
                    tag_results.append(tag_result)
                    if status != "none":
                        new_tags.append(canonical)

                hlj_validated = hlj.copy()
                hlj_validated["tags_v1"] = hlj.get("tags", [])
                hlj_validated["tags_v2"] = new_tags
                hlj_validated["tag_validation"] = tag_results
                hlj_validated["validation_version"] = "v2"
                validated_hljs.append(hlj_validated)

                audit_logs.append({
                    "hlj_id": hlj.get("id", ""),
                    "original_tags": hlj.get("tags", []),
                    "validated_tags": new_tags,
                    "tag_results": tag_results,
                    "validation_version": "v2",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })

            out_dir = os.path.join(run_dir, model, req)
            os.makedirs(out_dir, exist_ok=True)

            with open(os.path.join(out_dir, "all_chunks_full_validated.json"), "w") as f:
                json.dump(validated_hljs, f, indent=2)
            with open(os.path.join(out_dir, "tag_audit.yaml"), "w") as f:
                yaml.dump(audit_logs, f, sort_keys=False)

            print(f"✅ Validated HLJs & audit written to {out_dir}")

    # === Final alias match summary ===
    if alias_debug_log:
        alias_log_path = os.path.join(run_dir, "alias_debug_log.json")
        with open(alias_log_path, "w") as f:
            json.dump(alias_debug_log, f, indent=2)
        print(f"\n🎯 Total aliases matched: {len(alias_debug_log)} (log: {alias_log_path})")
    else:
        print("\n⚠️ No aliases detected during validation.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 4: Validate tags with alias maps")
    parser.add_argument("--config", default="configs/pipeline_v1.yaml")
    args = parser.parse_args()

    cfg = ConfigResolver(args.config)
    run_id = get_current_run("configs/pipeline_v1.yaml")
    main(cfg, run_id=run_id)
