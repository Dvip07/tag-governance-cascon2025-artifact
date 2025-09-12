import os
import csv
import json
from sentence_transformers import SentenceTransformer, util

# ===== Config =====
CLUSTER_CSV = "sbert_fix/all_tags/step_3/tag_clusters.csv"
ALIAS_JSON = "sbert_fix/all_tags/step_4/tag_alias_map.json"
DEDUPE_OUT = "sbert_fix/all_tags/step_5/deduplicated_tags.csv"
DEDUPE_LOG = "sbert_fix/all_tags/step_5/deduplicate_audit_log.json"
os.makedirs(os.path.dirname(DEDUPE_OUT), exist_ok=True)
SBERT_MODEL = "all-MiniLM-L6-v2"
DEDUPLICATION_THRESHOLD = 0.83  # You can tune this as needed

# ==== Load tag clusters ====
clusters = {}
with open(CLUSTER_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cid = row['cluster_id']
        tag = row['tag']
        if cid not in clusters:
            clusters[cid] = []
        clusters[cid].append(tag)

# ==== Load alias map (from canonical labels step) ====
with open(ALIAS_JSON, encoding='utf-8') as f:
    alias_map = json.load(f)

# ==== Load SBERT ====
sbert = SentenceTransformer(SBERT_MODEL)

def sbert_sim(a, b):
    # Cosine similarity between two strings
    emb_a = sbert.encode(a, convert_to_tensor=True)
    emb_b = sbert.encode(b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b).item())

deduped_rows = []
audit_log = []

for canonical, meta in alias_map.items():
    cid = meta['cluster_id']
    version = meta.get('version', 'v3')
    aliases = meta['aliases']
    seen = set()
    for alias in aliases:
        # Compute SBERT similarity between canonical and alias
        sim = sbert_sim(canonical, alias)
        method = []
        if alias in clusters.get(cid, []):
            method.append("cluster")
        if sim >= DEDUPLICATION_THRESHOLD:
            method.append("sbert")
        method = "+".join(method) if method else "manual"
        deduped_rows.append({
            "canonical_tag": canonical,
            "alias": alias,
            "method": method,
            "similarity": f"{sim:.3f}",
            "cluster_id": cid,
            "version": version
        })
        audit_log.append({
            "canonical": canonical,
            "alias": alias,
            "cluster_id": cid,
            "similarity": sim,
            "method": method,
            "version": version
        })
        seen.add(alias)
    # Canonical tags themselves, for completeness
    deduped_rows.append({
        "canonical_tag": canonical,
        "alias": canonical,
        "method": "self",
        "similarity": "1.000",
        "cluster_id": cid,
        "version": version
    })

# ==== Save deduplicated tags CSV ====
with open(DEDUPE_OUT, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ["canonical_tag", "alias", "method", "similarity", "cluster_id", "version"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(deduped_rows)
print(f"✅ Saved deduplicated tags to {DEDUPE_OUT}")

# ==== Save audit log ====
with open(DEDUPE_LOG, 'w', encoding='utf-8') as f:
    json.dump(audit_log, f, indent=2, ensure_ascii=False)
print(f"📝 Audit log saved to {DEDUPE_LOG}")

print(f"🔎 Total deduplication decisions: {len(deduped_rows)}")
print(f"🔎 Unique canonicals: {len(alias_map)}")
