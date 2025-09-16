# import os
# import csv
# import yaml
# import json
# from collections import defaultdict, Counter

# # === Config ===
# CLUSTER_CSV = "sbert_fix/all_tags/step_3/tag_clusters.csv"
# ALIAS_JSON = "sbert_fix/all_tags/step_4/tag_alias_map.json"
# CANONICAL_YAML = "sbert_fix/all_tags/step_4/canonical_tags.yaml"
# os.makedirs(os.path.dirname(ALIAS_JSON), exist_ok=True)

# # Load clusters
# clusters = defaultdict(list)  # cluster_id -> list of tags
# tag_freq = Counter()  # tag -> count (for tie-break)

# with open(CLUSTER_CSV, newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         tag = row['tag']
#         cluster_id = row['cluster_id']
#         clusters[cluster_id].append(tag)
#         tag_freq[tag] += 1

# # Canonical label selection
# canonical_map = {}
# yaml_out = {}

# for cid, tags in clusters.items():
#     tags = list(set(tags))  # remove accidental duplicates
#     # Sort by token length (shortest first), then by frequency (most frequent first)
#     tags_sorted = sorted(tags, key=lambda t: (len(t.split()), -tag_freq[t]))
#     canonical = tags_sorted[0]
#     aliases = [t for t in tags_sorted if t != canonical]
#     canonical_map[canonical] = {
#         "aliases": aliases,
#         "cluster_id": cid
#     }
#     yaml_out[canonical] = {"aliases": aliases, "cluster_id": cid}

# # Merge/update with existing alias_tag.json if present
# if os.path.exists(ALIAS_JSON):
#     with open(ALIAS_JSON, 'r', encoding='utf-8') as f:
#         prev_alias_map = json.load(f)
#     # Merge, prefer keeping any previous aliases not in current run
#     for canon, meta in prev_alias_map.items():
#         if canon in canonical_map:
#             # Merge unique aliases
#             old_aliases = set(meta.get("aliases", []))
#             new_aliases = set(canonical_map[canon]["aliases"])
#             canonical_map[canon]["aliases"] = list(sorted(old_aliases | new_aliases))
#         else:
#             canonical_map[canon] = meta
#         # YAML stays as new clusters only

# # Write canonical_tags.yaml (human readable)
# with open(CANONICAL_YAML, 'w', encoding='utf-8') as f:
#     yaml.safe_dump(yaml_out, f, sort_keys=False, allow_unicode=True)
# print(f"✅ Saved canonical tags to {CANONICAL_YAML}")

# # Write tag_alias_map.json (for pipeline)
# with open(ALIAS_JSON, 'w', encoding='utf-8') as f:
#     json.dump(canonical_map, f, indent=2, ensure_ascii=False)
# print(f"✅ Saved alias tag map to {ALIAS_JSON}")

# # Log summary
# print(f"🔎 Clusters processed: {len(clusters)}")
# print(f"🔑 Unique canonical tags: {len(canonical_map)}")
# print(f"🔁 (Aliases merged from prior: {os.path.exists(ALIAS_JSON)})")






# v2:

import os
import json
import yaml
import csv
from collections import defaultdict, Counter

# === CONFIG ===
HLJ_ROOT = "sbert_fix"
MODELS = ["meta70b", "gpt41", "opus4"]
CANONICAL_YAML_WITH_DOMAIN = "sbert_fix/all_tags/step_4/canonical_tags_with_domain.yaml"
CANONICAL_YAML_NO_DOMAIN = "sbert_fix/all_tags/step_4/canonical_tags.yaml"
LOG_PATH = "sbert_fix/all_tags/step_4/domain_autopopulate_with_domain.log"
CSV_PATH = "sbert_fix/all_tags/step_4/tag_domain_summary.csv"

# --- Ensure canonical YAMLs exist or start empty ---
def load_or_empty_yaml(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        return {}

canonical_map = load_or_empty_yaml(CANONICAL_YAML_WITH_DOMAIN)
canonical_map_no_domain = load_or_empty_yaml(CANONICAL_YAML_NO_DOMAIN)

# --- 1. Harvest tag-domain mappings from HLJs ---
tag_domains_v1 = defaultdict(set)
tag_domains_v2 = defaultdict(set)

for model in MODELS:
    model_path = os.path.join(HLJ_ROOT, model)
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
            hlj_domain = chunk.get("domain")
            for tag in chunk.get("tags_v1", []):
                tag_domains_v1[tag].add(hlj_domain)
            for tag in chunk.get("tags_v2", []):
                tag_domains_v2[tag].add(hlj_domain)

# --- 2. Find common tags and assign union of all their domains
all_tags = set(tag_domains_v1.keys()) | set(tag_domains_v2.keys())
tag_to_domains = {}
for tag in all_tags:
    v1_domains = tag_domains_v1.get(tag, set())
    v2_domains = tag_domains_v2.get(tag, set())
    union_domains = v1_domains | v2_domains
    tag_to_domains[tag] = sorted([d for d in union_domains if d])

# --- 3. Update canonical YAML WITH domain info
updated_map_with_domain = {}
for tag in all_tags:
    # Prefer existing metadata if present, else empty dict
    meta = canonical_map.get(tag, canonical_map_no_domain.get(tag, {}))
    updated_meta = dict(meta)
    updated_meta["domains"] = tag_to_domains.get(tag, [])
    updated_map_with_domain[tag] = updated_meta

with open(CANONICAL_YAML_WITH_DOMAIN, "w", encoding="utf-8") as f:
    yaml.safe_dump(updated_map_with_domain, f, sort_keys=False, allow_unicode=True)

# --- 4. Create CSV
with open(CSV_PATH, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["tag", "domains"])
    for tag, domains in tag_to_domains.items():
        writer.writerow([tag, ", ".join(domains)])

# --- 5. Create log
domain_counter = Counter()
tag_counter = Counter()
with open(LOG_PATH, "w", encoding="utf-8") as log:
    for tag, domains in tag_to_domains.items():
        log.write(f"Tag: {tag:30} → Domains: {', '.join(domains)}\n")
        for d in domains:
            domain_counter[d] += 1
        tag_counter[tag] = len(domains)
    log.write("\nDomain coverage summary:\n")
    for d, count in domain_counter.items():
        log.write(f"  {d}: {count} tags\n")
    log.write(f"\nTotal tags with domains: {sum(1 for v in tag_to_domains.values() if v)}\n")
    log.write(f"Total tags with NO domain: {sum(1 for v in tag_to_domains.values() if not v)}\n")

    # Subset/superset check
    log.write("\nSubset/superset checks:\n")
    for tag in tag_to_domains:
        v1 = tag_domains_v1.get(tag, set())
        v2 = tag_domains_v2.get(tag, set())
        if v1 and v2:
            if v1 < v2:
                log.write(f"  {tag:30}: v1 domains ⊂ v2 domains ({v1} < {v2})\n")
            elif v2 < v1:
                log.write(f"  {tag:30}: v2 domains ⊂ v1 domains ({v2} < {v1})\n")
            elif v1 == v2:
                log.write(f"  {tag:30}: v1 domains == v2 domains ({v1})\n")
            else:
                log.write(f"  {tag:30}: v1/v2 domains overlap but not subset ({v1} | {v2})\n")

print(f"✅ Updated {CANONICAL_YAML_WITH_DOMAIN} with v1/v2 domain union for each tag.")
print(f"📝 Log written to: {LOG_PATH}")
print(f"📑 CSV written to: {CSV_PATH}")

