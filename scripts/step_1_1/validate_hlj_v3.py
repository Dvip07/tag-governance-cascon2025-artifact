import os
import yaml
import json
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
from datetime import datetime

# === Constants ===
MODEL_FOLDERS = ["gpt41", "meta70b", "opus4"]
BASE_DIR = "sbert_fix"
SIM_THRESHOLD = 0.72

print("\n\U0001F680 Loading SBERT model...")
sbert = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ SBERT loaded.\n")
print("\U0001F50D Starting HLJ v3 validation...")

def validate_against_requirement():
    for model in MODEL_FOLDERS:
        model_path = os.path.join(BASE_DIR, model)
        print(f"\n📁 Validating model folder: {model}")

        if not os.path.exists(model_path):
            print(f"⚠️ Skipping missing model folder: {model_path}")
            continue

        reqs = os.listdir(model_path)
        for req in tqdm(reqs, desc=f"📂 Scanning {model}"):
            if not req.lower().startswith("req-"):
                continue

            audit_path = os.path.join(model_path, req, "tag_audit.yaml")
            chunk_file_path = os.path.join(model_path, req, "all_chunks_full_validated.json")

            if not os.path.exists(audit_path):
                print(f"⚠️ Missing audit file: {audit_path}")
                continue
            if not os.path.exists(chunk_file_path):
                print(f"❌ Missing chunk file: {chunk_file_path}")
                continue

            with open(audit_path) as f:
                audits = yaml.safe_load(f)
            if not audits:
                print(f"⚠️ No audits found in: {audit_path}")
                continue

            with open(chunk_file_path) as f:
                all_chunks = json.load(f)

            chunk_map = {chunk["id"]: chunk for chunk in all_chunks if "id" in chunk}

            # Filter relevant chunks from chunk_map
            local_chunk_map = {
                audit["hlj_id"]: chunk_map[audit["hlj_id"]]
                for audit in audits if audit.get("hlj_id") in chunk_map
            }

            if not local_chunk_map:
                missing_ids = [a["hlj_id"] for a in audits if a["hlj_id"] not in chunk_map]
                print(f"⚠️ No chunks found for {req} — Missing HLJ IDs: {missing_ids[:3]}")
                continue

            print(f"\n🔧 Processing {model}/{req} — {len(audits)} audits, {len(local_chunk_map)} chunks")
            updated = False

            for audit in audits:
                dropped_tags = audit.get("tags_dropped", [])
                chunk_id = audit.get("hlj_id")
                chunk_obj = local_chunk_map.get(chunk_id)

                if not chunk_obj:
                    print(f"❓ Chunk not found: {chunk_id}")
                    continue

                req_text = chunk_obj.get("summary", "") + ". " + chunk_obj.get("title", "")
                if not req_text.strip():
                    print(f"⚠️ Empty chunk text for: {chunk_id}")
                    continue

                req_emb = sbert.encode(req_text, convert_to_tensor=True)
                new_dropped = []
                revalidated = []

                for tag in dropped_tags:
                    tag_emb = sbert.encode(tag, convert_to_tensor=True)
                    sim = util.cos_sim(req_emb, tag_emb).item()

                    if sim >= SIM_THRESHOLD:
                        revalidated.append({
                            "reinstated_tag": tag,
                            "similarity": round(sim, 4),
                            "reason": "Detected in requirement",
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        new_dropped.append(tag)

                if revalidated:
                    audit.setdefault("v3_updates", {})["reinstated_tags"] = revalidated
                    audit["tags_dropped"] = new_dropped
                    audit.setdefault("validated_tags", []).extend(
                        [t["reinstated_tag"] for t in revalidated]
                    )
                    updated = True

            if updated:
                with open(audit_path, "w") as f:
                    yaml.dump(audits, f, sort_keys=False)
                print(f"🔁 v3 updated: {model}/{req}")


if __name__ == "__main__":
    validate_against_requirement()