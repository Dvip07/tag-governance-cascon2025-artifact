import os
import re
import json
import shutil
import argparse
import subprocess
from datetime import datetime
from collections import defaultdict

import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util

from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run


def choose_device(pref: str = "auto") -> str:
    pref = (pref or "auto").lower()
    if pref == "cuda" and torch.cuda.is_available():
        return "cuda"
    if pref == "mps" and torch.backends.mps.is_available():
        return "mps"
    if pref == "cpu":
        return "cpu"
    # auto
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def try_load_model(model_name: str, device: str):
    """
    Try to load a SentenceTransformer model.
    If it fails, attempt to install deps and retry once.
    Fallback to all-MiniLM-L6-v2 if it still fails.
    """
    def _load(name):
        return SentenceTransformer(name, device=device)

    try:
        return _load(model_name), model_name
    except Exception as e:
        print(f"⚠️ First attempt to load '{model_name}' failed: {e}")
        # best-effort dependency install (quiet)
        try:
            print("🔧 Attempting to install/upgrade transformers/sentence-transformers/accelerate...")
            subprocess.run(
                ["python", "-m", "pip", "install", "-q", "--upgrade",
                 "transformers", "sentence-transformers", "accelerate"],
                check=False
            )
            return _load(model_name), model_name
        except Exception as e2:
            print(f"❌ Retry failed for '{model_name}': {e2}")
            # final fallback
            fallback = "all-MiniLM-L6-v2"
            print(f"↩️ Falling back to '{fallback}'")
            return _load(fallback), fallback


def encode_with_instructor_guard(model, model_name: str, instr: str, text: str):
    """
    Use Instructor-style encoding if the model is an INSTRUCTOR model,
    otherwise standard ST encode.
    """
    if "instructor" in (model_name or "").lower():
        return model.encode([[instr, text]], convert_to_tensor=True)
    return model.encode(text, convert_to_tensor=True)


def extract_req_id(hlj_id: str) -> str:
    m = re.search(r'(req-\d+)', hlj_id, re.IGNORECASE)
    return m.group(1).lower() if m else hlj_id.lower()


def build_nlu_context(chunk: dict, raw_req: str) -> str:
    parts = []
    if chunk.get("summary"):
        parts.extend([chunk["summary"]] * 2)
    if chunk.get("title"):
        parts.append(chunk["title"])
    src = chunk.get("reasoning", {}).get("source_summary_fragment")
    if src:
        parts.append(src)
    mapped = chunk.get("reasoning", {}).get("mapped_concepts")
    if mapped:
        parts.append(" ".join(mapped))
    parts.append(raw_req or "")
    return "\n".join([p for p in parts if p and p != "None"])


def find_matching_chunk(hlj_chunks: list, hlj_id: str, req_id: str) -> dict | None:
    # direct
    for ch in hlj_chunks:
        if ch.get("id") == hlj_id or ch.get("source_hlj_id") == hlj_id or (req_id in ch.get("id", "")):
            return ch
    # fuzzy
    for ch in hlj_chunks:
        if hlj_id.lower() in ch.get("id", "").lower():
            return ch
    return None


def load_raw_requirement(req_base: str, req_id: str) -> str:
    for domain in ["FinTech", "SaaS"]:
        path = os.path.join(req_base, domain, f"{req_id}.md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    return ""


def main(cfg_path="configs/pipeline_v2.yaml"):
    cfg = ConfigResolver(cfg_path)
    run_id = get_current_run(cfg_path)
    run_dir = cfg.get("globals.run_dir")
    if not run_id or not run_dir:
        print("❌ Step 7 aborted: run_id/run_dir missing. Did you start the pipeline and run earlier steps?")
        return

    # === Inputs from YAML ===
    topk_path = cfg.get("outputs.topk_tags")
    if not topk_path or not os.path.exists(topk_path):
        print("❌ Step 7 aborted: topk_tags JSON missing. Did you run step_6 (score_tags.py)?")
        return

    hlj_root = cfg.get("globals.base_dir", "sbert_fix")
    raw_req_base = cfg.get("globals.raw_req_base", "raw_requirement")
    models = cfg.get("globals.models", [])

    # === Params ===
    step7 = cfg.get("step7", {}) or {}
    embed_model = step7.get("embedding_model", "hkunlp/instructor-xl")
    sim_threshold = float(step7.get("sim_threshold", 0.68))
    borderline_min = float(step7.get("borderline_min", 0.60))
    device_pref = step7.get("device_preference", "auto")
    hybrid_copy = bool(step7.get("hybrid_copy", True))
    match_strategy = step7.get("match_strategy", "id_then_source_then_fuzzy")
    prompt_tag = step7.get("prompt_tag", "Represent the concept as a tag.")
    prompt_doc = step7.get("prompt_doc", "Represent the document for tag matching.")

    # === Outputs (run-scoped) ===
    out_dir = os.path.join(run_dir, "step_7")
    hybrid_dir = os.path.join(out_dir, "hybrid")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(hybrid_dir, exist_ok=True)
    stats_csv = os.path.join(out_dir, "nlu_validation_stats.csv")
    borderline_csv = os.path.join(out_dir, "borderline_nlu_tags.csv")
    validated_json = os.path.join(out_dir, "validated_tags_per_hlj.json")

    # === Device and model ===
    device = choose_device(device_pref)
    print(f"🔌 Using device: {device}")
    model, actual_model_name = try_load_model(embed_model, device=device)
    print(f"🧠 Model in use: {actual_model_name}")

    # === Load inputs ===
    with open(topk_path, "r", encoding="utf-8") as f:
        hlj_tags = json.load(f)
    print(f"💡 Found {len(hlj_tags)} HLJ entries in {topk_path}")

    # List available model dirs under HLJ root
    root_models = [m for m in os.listdir(hlj_root) if os.path.isdir(os.path.join(hlj_root, m))]
    print(f"🗂️ HLJ root models: {root_models}")

    validation_stats = []
    borderline_tags = []
    validated_per_hlj = []

    processed = 0
    for hlj in hlj_tags:
        hlj_id = hlj.get("hlj_id")
        tag_objs = hlj.get("tags", [])
        req_id = extract_req_id(hlj_id)

        print(f"\n==> HLJ: {hlj_id} | req_id: {req_id} | tags: {len(tag_objs)}")
        found_any_model = False

        for model_name in root_models:
            if model_name == "hybrid":  # skip any existing hybrid dir in source root
                continue

            model_path = os.path.join(hlj_root, model_name)
            if not os.path.isdir(model_path) or req_id not in os.listdir(model_path):
                continue

            found_any_model = True
            src_dir = os.path.join(model_path, req_id)
            src_json = os.path.join(src_dir, "all_chunks_full_validated.json")

            # prepare hybrid working file
            dst_dir = os.path.join(hybrid_dir, model_name, req_id)
            os.makedirs(dst_dir, exist_ok=True)
            dst_json = os.path.join(dst_dir, "all_chunks_full_validated.json")

            if os.path.exists(src_json) and (hybrid_copy and not os.path.exists(dst_json)):
                shutil.copy(src_json, dst_json)
                print(f"    [COPY] {src_json} → {dst_json}")
            elif not os.path.exists(dst_json):
                # fall back: if no src, but maybe previous hybrid exists?
                if os.path.exists(dst_json):
                    pass
                else:
                    print(f"    [SKIP] No source JSON and no hybrid at {dst_json}")
                    continue

            # open and mutate hybrid json
            try:
                with open(dst_json, "r+", encoding="utf-8") as fh:
                    chunks = json.load(fh)
                    chunk = find_matching_chunk(chunks, hlj_id, req_id) if "fuzzy" in match_strategy or "id_then" in match_strategy else None
                    if not chunk:
                        print(f"    [NO MATCH] Could not locate matching chunk for {hlj_id}")
                        continue

                    raw_req = load_raw_requirement(raw_req_base, req_id)
                    if not raw_req:
                        print(f"    [WARN] Raw requirement not found for {req_id}")

                    ctx = build_nlu_context(chunk, raw_req)

                    # reset v3 for rebuild
                    chunk["tags_v3"] = []
                    chunk["tag_nlu_validation"] = []

                    for tagobj in tag_objs:
                        tag = tagobj.get("tag")
                        if not tag:
                            continue
                        emb_tag = encode_with_instructor_guard(model, actual_model_name, prompt_tag, tag)
                        emb_ctx = encode_with_instructor_guard(model, actual_model_name, prompt_doc, ctx)
                        sim = float(util.cos_sim(emb_tag, emb_ctx).item())
                        is_valid = sim >= sim_threshold
                        is_borderline = (borderline_min <= sim < sim_threshold)

                        reason = (
                            "similarity_above_threshold" if is_valid
                            else "borderline_similarity" if is_borderline
                            else "similarity_below_threshold"
                        )

                        entry = {
                            "tag": tag,
                            "original_tag": tagobj.get("original_tag", tag),
                            "score": tagobj.get("score"),
                            "model": tagobj.get("model"),
                            "version": tagobj.get("version", "v3"),
                            "method": tagobj.get("method", "hybrid"),
                            "confidence": round(sim, 6),
                            "validated": bool(is_valid),
                            "validation_reason": reason,
                            "hlj_id": hlj_id,
                            "req_id": req_id,
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                        }

                        validation_stats.append(entry)
                        if is_valid:
                            chunk["tags_v3"].append(tag)
                        if is_borderline:
                            borderline_tags.append(entry)
                        chunk["tag_nlu_validation"].append(entry)

                    # persist updated hybrid
                    fh.seek(0)
                    fh.truncate()
                    json.dump(chunks, fh, indent=2, ensure_ascii=False)
                    processed += 1

                    # capture per-HLJ rollup (from this model’s chunk)
                    validated_per_hlj.append({
                        "hlj_id": hlj_id,
                        "req_id": req_id,
                        "model": model_name,
                        "tags_v3": chunk.get("tags_v3", []),
                    })

            except Exception as e:
                print(f"    ❌ Error processing {dst_json}: {e}")
                continue

        if not found_any_model:
            print(f"  [WARN] No model directory found for req_id: {req_id}")

    print(f"\n✅ NLU tag validation complete for ~{processed} chunk(s). Hybrid copies live under: {hybrid_dir}")

    # === Write aggregate artifacts ===
    if validation_stats:
        pd.DataFrame(validation_stats).to_csv(stats_csv, index=False)
        print(f"📊 Validation stats CSV: {stats_csv}")
    else:
        print("😶 No validation stats to write.")

    if borderline_tags:
        pd.DataFrame(borderline_tags).to_csv(borderline_csv, index=False)
        print(f"⚠️ Borderline tags CSV: {borderline_csv}")
    else:
        print("👌 No borderline tags.")

    with open(validated_json, "w", encoding="utf-8") as f:
        json.dump(validated_per_hlj, f, indent=2, ensure_ascii=False)
    print(f"🧾 Validated tags per HLJ JSON: {validated_json}")

    # === Update YAML outputs ===
    cfg.set("outputs.validated_tags", validated_json)
    cfg.set("outputs.nlu_stats_csv", stats_csv)
    cfg.set("outputs.borderline_csv", borderline_csv)
    cfg.set("outputs.hybrid_dir", hybrid_dir)
    cfg.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 7: NLU validation of top-K tags and tags_v3 writeback")
    parser.add_argument("--config", default="configs/pipeline_v2.yaml")
    args = parser.parse_args()
    main(args.config)
