import os
import csv
import json
from collections import defaultdict, Counter

# ==== CONFIG ====
DEDUPED_CSV = "sbert_fix/all_tags/step_5/deduplicated_tags.csv"
TOKEN_FILTERED_CSV = "sbert_fix/all_tags/step_2/final_tags.csv"
DROPPED_CSV = "sbert_fix/all_tags/step_2/dropped_tags.csv"
OUT_JSON = "sbert_fix/all_tags/step_6/topk_tags_per_hlj.json"
TOP_K = 9  # How many tags per HLJ? Tune as needed

os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)

# Step 1: Load dropped tags (set for fast exclusion)
dropped_set = set()
if os.path.exists(DROPPED_CSV):
    with open(DROPPED_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dropped_set.add((row['tag'], row['hlj_id']))

# Step 2: Map HLJ to canonical tags (with meta)
hlj2tags = defaultdict(list)
tag_detail_map = dict()

# Load deduplicated canonical mapping
canon_alias_map = defaultdict(set)  # alias -> canonical_tag
with open(DEDUPED_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        alias = row['alias']
        canonical = row['canonical_tag']
        canon_alias_map[alias].add(canonical)

# Step 3: Walk token-filtered tags for HLJ → canonical assignment
with open(TOKEN_FILTERED_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        hlj_id = row['hlj_id']
        tag = row['tag']
        # Skip if dropped
        if (tag, hlj_id) in dropped_set:
            continue
        version = row.get('version', 'v3')
        model = row.get('model', 'unknown')
        conf_val = row.get('confidence')
        try:
            confidence = float(conf_val)
        except (TypeError, ValueError):
            confidence = None
        # Map every alias to canonical (might be more than one, rare)
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
            tag_detail_map[(canonical, hlj_id)] = detail

# Step 4: Frequency count per HLJ (how many models/versions voted for each tag?)
hlj_outputs = []
for hlj_id, taglist in hlj2tags.items():
    freq = Counter([d["tag"] for d in taglist])
    ranked = sorted(taglist, key=lambda x: (-freq[x["tag"]], -(x["confidence"] or 0)))
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
        if len(topk_tags) == TOP_K:
            break
    hlj_outputs.append({
        "hlj_id": hlj_id,
        "tags": topk_tags
    })

# Step 5: Output as JSON
with open(OUT_JSON, "w", encoding='utf-8') as f:
    json.dump(hlj_outputs, f, indent=2, ensure_ascii=False)

print(f"✅ Top-K tag scoring complete for {len(hlj_outputs)} HLJs.")
print(f"Output: {OUT_JSON}")
