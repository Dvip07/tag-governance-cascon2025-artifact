import os
import json
import yaml
from datetime import datetime
import spacy
from sentence_transformers import SentenceTransformer, util

# === Trimmed HLJ path only ===
HLJ_INPUT_SUBPATH = "hlj/trim_merged/all_trimmed_hljs.json"
ALIAS_MAP_PATH = "tag_alias_maps/tag_alias_map.json"

# --- Load models
nlp = spacy.load("en_core_web_sm")
sbert = SentenceTransformer("all-MiniLM-L6-v2")

# --- Load alias map
if os.path.exists(ALIAS_MAP_PATH):
    with open(ALIAS_MAP_PATH) as f:
        TAG_ALIAS_MAP = json.load(f)
else:
    TAG_ALIAS_MAP = {}

# --- Tag normalization
def normalize_tag(tag):
    return tag.lower().replace("-", " ").strip()

# --- Build reverse cluster mapping (✨ fixed version)
REVERSE_CLUSTER_MAP = {}
for canonical_tag, cluster_info in TAG_ALIAS_MAP.items():
    aliases = cluster_info.get("aliases", [])
    all_names = [canonical_tag] + aliases
    for name in all_names:
        name_normalized = normalize_tag(name)
        REVERSE_CLUSTER_MAP[name_normalized] = {
            "canonical_tag": canonical_tag,
            "cluster_id": canonical_tag,
            "is_alias": name_normalized != normalize_tag(canonical_tag)
        }
        
print(f"\n🔬 Total normalized tags in REVERSE_CLUSTER_MAP: {len(REVERSE_CLUSTER_MAP)}")
print("🧪 Sample entries:")
for i, (k, v) in enumerate(REVERSE_CLUSTER_MAP.items()):
    print(f"  {k} → {v['canonical_tag']} (alias: {v['is_alias']})")
    if i > 5:
        break


def get_canonical_tag(tag):
    return REVERSE_CLUSTER_MAP.get(normalize_tag(tag), {}).get("canonical_tag", tag)

def get_cluster_id(tag):
    return REVERSE_CLUSTER_MAP.get(normalize_tag(tag), {}).get("cluster_id", None)

def was_alias(tag):
    return REVERSE_CLUSTER_MAP.get(normalize_tag(tag), {}).get("is_alias", False)

def validate_tag(original_tag, canonical_tag, contexts, sbert_threshold=0.68):
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

# def main():
#     BASE = "output"
#     RAW_REQ_BASE = "raw_requirement"
#     DOMAINS = ["FinTech", "SaaS"]
#     alias_debug_log = []  # 💥 Track all alias matches globally

#     for model in os.listdir(BASE):
#         model_dir = os.path.join(BASE, model)
#         if not os.path.isdir(model_dir):
#             continue
#         print(f"Validating model: {model}")
#         for req in os.listdir(model_dir):
#             req_dir = os.path.join(model_dir, req)
#             hlj_path = os.path.join(req_dir, HLJ_INPUT_SUBPATH)
#             if not os.path.exists(hlj_path):
#                 print(f"Missing: {hlj_path}")
#                 continue

#             # Detect raw requirement domain
#             domain = None
#             for dom in DOMAINS:
#                 raw_req_file = os.path.join(RAW_REQ_BASE, dom, f"{req}.md")
#                 if os.path.exists(raw_req_file):
#                     domain = dom
#                     break
#             if not domain:
#                 print(f"Raw requirement missing for {req}")
#                 continue

#             with open(os.path.join(RAW_REQ_BASE, domain, f"{req}.md")) as f:
#                 raw_req_text = f.read()

#             try:
#                 hlj_list = load_flat_hljs(hlj_path)
#             except Exception as e:
#                 print(f"Error loading HLJ: {hlj_path}: {e}")
#                 continue

#             validated_hljs = []
#             audit_logs = []
#             for hlj in hlj_list:
#                 contexts = {
#                     "title": hlj.get("title", ""),
#                     "summary": hlj.get("summary", ""),
#                     "source_fragment": hlj.get("reasoning", {}).get("source_summary_fragment", ""),
#                     "mapped_concepts": " ".join(hlj.get("reasoning", {}).get("mapped_concepts", [])),
#                     "raw_requirement": raw_req_text
#                 }
#                 tag_results = []
#                 new_tags = []
#                 for tag in hlj.get("tags", []):
#                     canonical = get_canonical_tag(tag)
#                     cluster_id = get_cluster_id(tag)
#                     # if alias_flag:
#                     #     print(f"[Alias Detected] {tag} → {canonical}")
#                     alias_flag = was_alias(tag)
#                     if alias_flag:
#                         print(f"🔁 Alias matched: '{tag}' → '{canonical}'")
#                         alias_debug_log.append({
#                         "hlj_id": hlj.get("id", ""),
#                         "original_tag": tag,
#                         "canonical_tag": canonical,
#                         "model": model,
#                         "req_id": req,
#                         "cluster_id": cluster_id
#                     })

#                     status, sim, ctx = validate_tag(tag, canonical, contexts)
#                     tag_result = {
#                         "original_tag": tag,
#                         "canonical_tag": canonical,
#                         "matched_tag": canonical,
#                         "tag_origin_cluster_id": cluster_id,
#                         "original_confidence": next((t.get("confidence", None)
#                             for t in hlj.get("reasoning", {}).get("tag_metadata_reference", [])
#                             if t["tag"] == tag), None),
#                         "validation_status": status,
#                         "similarity": sim,
#                         "context": ctx,
#                         "alias_used": alias_flag,
#                         "timestamp": datetime.utcnow().isoformat() + "Z"
#                     }
#                     tag_results.append(tag_result)
#                     if status != "none":
#                         new_tags.append(canonical)
#                 hlj_validated = hlj.copy()
#                 hlj_validated["tags_v1"] = hlj.get("tags", [])
#                 hlj_validated["tags_v2"] = new_tags
#                 hlj_validated["tag_validation"] = tag_results
#                 hlj_validated["validation_version"] = "v2"
#                 validated_hljs.append(hlj_validated)

#                 audit_logs.append({
#                     "hlj_id": hlj.get("id", ""),
#                     "original_tags": hlj.get("tags", []),
#                     "validated_tags": new_tags,
#                     "tag_results": tag_results,
#                     "validation_version": "v2",
#                     "timestamp": datetime.utcnow().isoformat() + "Z"
#                 })

#             out_dir = os.path.join("sbert_fix", model, req)
#             os.makedirs(out_dir, exist_ok=True)

#             validated_file = os.path.join(out_dir, "all_chunks_full_validated.json")
#             audit_file = os.path.join(out_dir, "tag_audit.yaml")
#             for file_path in [validated_file, audit_file]:
#                 if os.path.exists(file_path):
#                     os.remove(file_path)

#             with open(validated_file, "w") as f:
#                 json.dump(validated_hljs, f, indent=2)
#             with open(audit_file, "w") as f:
#                 yaml.dump(audit_logs, f, sort_keys=False)


#             print(f"✅ Validated HLJs & audit written to {out_dir}")

def main():
    BASE = "output"
    RAW_REQ_BASE = "raw_requirement"
    DOMAINS = ["FinTech", "SaaS"]
    alias_debug_log = []  # 💥 Track all alias matches globally

    for model in os.listdir(BASE):
        model_dir = os.path.join(BASE, model)
        if not os.path.isdir(model_dir):
            continue
        print(f"Validating model: {model}")
        for req in os.listdir(model_dir):
            req_dir = os.path.join(model_dir, req)
            hlj_path = os.path.join(req_dir, HLJ_INPUT_SUBPATH)
            if not os.path.exists(hlj_path):
                print(f"Missing: {hlj_path}")
                continue

            # Detect raw requirement domain
            domain = None
            for dom in DOMAINS:
                raw_req_file = os.path.join(RAW_REQ_BASE, dom, f"{req}.md")
                if os.path.exists(raw_req_file):
                    domain = dom
                    break
            if not domain:
                print(f"Raw requirement missing for {req}")
                continue

            with open(os.path.join(RAW_REQ_BASE, domain, f"{req}.md")) as f:
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
                    canonical = get_canonical_tag(tag)
                    cluster_id = get_cluster_id(tag)
                    alias_flag = was_alias(tag)
                    if alias_flag:
                        print(f"🔁 Alias matched: '{tag}' → '{canonical}'")
                        alias_debug_log.append({
                            "hlj_id": hlj.get("id", ""),
                            "original_tag": tag,
                            "canonical_tag": canonical,
                            "model": model,
                            "req_id": req,
                            "cluster_id": cluster_id
                        })

                    status, sim, ctx = validate_tag(tag, canonical, contexts)
                    tag_result = {
                        "original_tag": tag,
                        "canonical_tag": canonical,
                        "matched_tag": canonical,
                        "tag_origin_cluster_id": cluster_id,
                        "original_confidence": next((t.get("confidence", None)
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

            out_dir = os.path.join("sbert_fix", model, req)
            os.makedirs(out_dir, exist_ok=True)

            validated_file = os.path.join(out_dir, "all_chunks_full_validated.json")
            audit_file = os.path.join(out_dir, "tag_audit.yaml")
            for file_path in [validated_file, audit_file]:
                if os.path.exists(file_path):
                    os.remove(file_path)

            with open(validated_file, "w") as f:
                json.dump(validated_hljs, f, indent=2)
            with open(audit_file, "w") as f:
                yaml.dump(audit_logs, f, sort_keys=False)

            print(f"✅ Validated HLJs & audit written to {out_dir}")

    # === Final alias match summary ===
    if alias_debug_log:
        print(f"\n🎯 Total aliases matched: {len(alias_debug_log)}")
        print("🧾 Sample alias mappings:")
        for entry in alias_debug_log[:10]:
            print(f"  ↳ {entry['original_tag']} → {entry['canonical_tag']} (HLJ: {entry['hlj_id']}, Model: {entry['model']})")
        # Optionally save
        with open("sbert_fix/alias_debug_log.json", "w") as f:
            json.dump(alias_debug_log, f, indent=2)
    else:
        print("\n⚠️ No aliases detected during validation. Something might still be wrong with REVERSE_CLUSTER_MAP.")


if __name__ == "__main__":
    main()
