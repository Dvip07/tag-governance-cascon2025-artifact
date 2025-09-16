import os
import json
import shutil
import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import re

# === CONFIG ===
TOPK_TAGS_JSON = "sbert_fix/all_tags/step_6/topk_tags_per_hlj.json"
RAW_REQ_BASE = "raw_requirement"  # Check your directory!
HLJ_ROOT = "sbert_fix"
HYBRID_DIR = "sbert_fix/hybrid"
EMBED_MODEL = "hkunlp/instructor-xl"
SIM_THRESHOLD = 0.68  # Can tune lower/higher
BORDERLINE_MIN = 0.60  # Tags between here and SIM_THRESHOLD will be logged as "borderline"

# ---- Device selection ----
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"🔌 Using device: {device}")

os.makedirs(HYBRID_DIR, exist_ok=True)

# ==== UTILS ====
def load_raw_requirement(req_id):
    found = False
    for domain in ["FinTech", "SaaS"]:
        path = os.path.join(RAW_REQ_BASE, domain, f"{req_id}.md")
        if os.path.exists(path):
            found = True
            with open(path, "r", encoding="utf-8") as f:
                print(f"    [FOUND] Raw requirement: {path}")
                return f.read()
    if not found:
        print(f"    [WARN] Raw requirement NOT found for {req_id} in {RAW_REQ_BASE}")
    return ""

def extract_req_id(hlj_id):
    m = re.search(r'(req-\d+)', hlj_id, re.IGNORECASE)
    if m:
        return m.group(1)
    # Fallback: maybe older pattern? (add more cases if you use other formats)
    return hlj_id

def build_nlu_context(chunk, raw_req):
    context_parts = []
    if chunk.get("summary"):
        context_parts.extend([chunk["summary"]] * 2)
    if chunk.get("title"):
        context_parts.append(chunk["title"])
    if chunk.get("reasoning", {}).get("source_summary_fragment"):
        context_parts.append(chunk["reasoning"]["source_summary_fragment"])
    if chunk.get("reasoning", {}).get("mapped_concepts"):
        context_parts.append(" ".join(chunk["reasoning"]["mapped_concepts"]))
    context_parts.append(raw_req)
    return "\n".join([p for p in context_parts if p and p != "None"])

def find_matching_chunk(hlj_chunks, hlj_id, req_id):
    # First, direct matches
    for chunk in hlj_chunks:
        if (
            chunk.get("id") == hlj_id or
            chunk.get("source_hlj_id") == hlj_id or
            (req_id in chunk.get("id", ""))
        ):
            print(f"    [MATCH] HLJ chunk matched by ID/source for {hlj_id}")
            return chunk
    # Fuzzy match fallback
    for chunk in hlj_chunks:
        if hlj_id.lower() in chunk.get("id", "").lower():
            print(f"    [FUZZY MATCH] HLJ chunk matched by fuzzy for {hlj_id}")
            return chunk
    print(f"    [NO MATCH] No HLJ chunk match for {hlj_id} (req: {req_id})")
    return None

# ==== MAIN ====
def main():
    print(f"🔎 Loading InstructorXL model: {EMBED_MODEL}")
    model = SentenceTransformer(EMBED_MODEL, device=device)

    if not os.path.exists(TOPK_TAGS_JSON):
        print(f"[ERROR] Cannot find TOPK_TAGS_JSON at {TOPK_TAGS_JSON}")
        return

    with open(TOPK_TAGS_JSON, "r", encoding="utf-8") as f:
        hlj_tags = json.load(f)
    
    print(f"💡 Found {len(hlj_tags)} HLJ entries in {TOPK_TAGS_JSON}")

    processed = 0
    validation_stats = []
    borderline_tags = []

    print(f"💡 Listing models in {HLJ_ROOT}...")
    root_models = [m for m in os.listdir(HLJ_ROOT) if os.path.isdir(os.path.join(HLJ_ROOT, m))]
    print(f"   Models found: {root_models}")

    for hlj in hlj_tags:
        hlj_id = hlj["hlj_id"]
        tags = hlj["tags"]
        req_id = extract_req_id(hlj_id)
        req_id = req_id.lower()

        print(f"\n==> HLJ: {hlj_id} | req_id: {req_id} | {len(tags)} tags")
        found_model = False
        for model_name in root_models:
            if model_name == "hybrid":
                continue
            model_path = os.path.join(HLJ_ROOT, model_name)
            req_dirs = os.listdir(model_path)
            print(f"  - [MODEL] {model_name}: dir contains {len(req_dirs)} entries")
            if req_id not in req_dirs:
                print(f"    [SKIP] {req_id} not in {model_path} dirs")
                continue
            found_model = True
            hlj_dir = os.path.join(HLJ_ROOT, model_name, req_id)
            hybrid_dir = os.path.join(HYBRID_DIR, model_name, req_id)
            os.makedirs(hybrid_dir, exist_ok=True)
            validated_json = os.path.join(hlj_dir, "all_chunks_full_validated.json")
            hybrid_json = os.path.join(hybrid_dir, "all_chunks_full_validated.json")
            if os.path.exists(validated_json) and not os.path.exists(hybrid_json):
                shutil.copy(validated_json, hybrid_json)
                print(f"    [COPY] {validated_json} → {hybrid_json}")
            if not os.path.exists(hybrid_json):
                print(f"    [SKIP] Hybrid json not found at {hybrid_json}")
                continue

            with open(hybrid_json, "r+", encoding="utf-8") as f:
                hlj_chunks = json.load(f)
                chunk = find_matching_chunk(hlj_chunks, hlj_id, req_id)
                if not chunk:
                    print(f"    [SKIP] No matching chunk for HLJ {hlj_id} in {req_id}")
                    continue
                raw_req = load_raw_requirement(req_id)
                nlu_context = build_nlu_context(chunk, raw_req)
                chunk["tags_v3"] = []
                chunk["tag_nlu_validation"] = []
                for tagobj in tags:
                    tag = tagobj["tag"]
                    print(f"      [VALIDATE] Tag: {tag}")
                    emb_tag = model.encode([["Represent the concept as a tag.", tag]], convert_to_tensor=True)
                    emb_ctx = model.encode([["Represent the document for tag matching.", nlu_context]], convert_to_tensor=True)
                    sim = float(util.cos_sim(emb_tag, emb_ctx).item())
                    is_valid = sim >= SIM_THRESHOLD
                    is_borderline = BORDERLINE_MIN <= sim < SIM_THRESHOLD
                    reason = (
                        "similarity_above_threshold" if is_valid
                        else "borderline_similarity" if is_borderline
                        else "similarity_below_threshold"
                    )
                    print(f"        [SIMILARITY] {sim:.3f} ({reason})")
                    tag_entry = {
                        "tag": tag,
                        "original_tag": tagobj.get("original_tag", tag),
                        "score": tagobj.get("score"),
                        "model": tagobj.get("model"),
                        "version": tagobj.get("version", "v3"),
                        "method": tagobj.get("method", "hybrid"),
                        "confidence": sim,
                        "validated": is_valid,
                        "validation_reason": reason,
                        "hlj_id": hlj_id,
                        "req_id": req_id
                    }
                    validation_stats.append(tag_entry)
                    if is_valid:
                        chunk["tags_v3"].append(tag)
                    if is_borderline:
                        borderline_tags.append(tag_entry)
                    chunk["tag_nlu_validation"].append(tag_entry)
                f.seek(0)
                f.truncate()
                json.dump(hlj_chunks, f, indent=2, ensure_ascii=False)
            processed += 1
        if not found_model:
            print(f"  [WARN] No model found for req_id: {req_id}")

    print(f"\n✅ NLU tag validation with InstructorXL complete for {processed} HLJs.")
    print("v1/v2 preserved, v3/validation reasons logged to hybrid folders.")

    # === Write validation stats ===
    if validation_stats:
        stats_df = pd.DataFrame(validation_stats)
        out_csv = os.path.join(HYBRID_DIR, "nlu_validation_stats.csv")
        stats_df.to_csv(out_csv, index=False)
        print(f"📊 Validation stats CSV saved: {out_csv}")

    # === Write borderline tags if any ===
    if borderline_tags:
        borderline_df = pd.DataFrame(borderline_tags)
        borderline_csv = os.path.join(HYBRID_DIR, "borderline_nlu_tags.csv")
        borderline_df.to_csv(borderline_csv, index=False)
        print(f"⚠️ Borderline similarity tags saved: {borderline_csv}")
    else:
        print("😴 No borderline tags found. Everything was clean (or useless).")

if __name__ == '__main__':
    main()
