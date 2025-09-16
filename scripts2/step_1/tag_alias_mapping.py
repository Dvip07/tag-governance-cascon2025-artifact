import os
import json
from collections import defaultdict, Counter
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import re

# --- Config ---
MODEL_DIRS = ["output/meta70b", "output/opus4", "output/gpt41"]
TARGET_FILENAME = "all_trimmed_hljs.json"
SIM_THRESHOLD = 0.85

def normalize_tag(tag):
    tag = tag.strip().lower()
    tag = re.sub(r"\[inferred\]\s*", "", tag)
    tag = re.sub(r"[_\-]", " ", tag)
    return tag.strip()

def extract_tags_from_file(file_path):
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []

    tags = []
    for item in data:
        raw_tags = item.get("tags", [])
        for tag in raw_tags:
            clean_tag = normalize_tag(tag)
            was_inferred = "[inferred]" in tag.lower()
            tags.append((clean_tag, was_inferred))
    return tags

def get_all_tags():
    all_tags = defaultdict(list)  # model_name -> list of tags
    for model_dir in MODEL_DIRS:
        model_name = os.path.basename(model_dir)
        tag_set = []
        for root, _, files in os.walk(model_dir):
            if TARGET_FILENAME in files:
                tags = extract_tags_from_file(os.path.join(root, TARGET_FILENAME))
                tag_set.extend(tags)
        all_tags[model_name] = tag_set
        print(f"\U0001F4E6 {model_name}: {len(tag_set)} tags")
    return all_tags

def generate_embeddings(tag_list):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    tag_texts = [t[0] for t in tag_list]
    embeddings = model.encode(tag_texts, convert_to_tensor=True)
    return tag_texts, embeddings

def cluster_tags(tag_texts, embeddings):
    if len(tag_texts) <= 1:
        return {}
    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=1-SIM_THRESHOLD, linkage="average", metric="cosine")
    clustering.fit(embeddings.cpu())
    label_map = defaultdict(list)
    for tag, label in zip(tag_texts, clustering.labels_):
        label_map[label].append(tag)
    return label_map

def build_alias_map(label_map, original_tag_map):
    alias_map = {}
    for label, tags in label_map.items():
        if len(tags) < 2:
            continue  # skip singletons
        root = min(tags, key=len)  # shortest as canonical
        alias_map[root] = {
            "aliases": sorted(set(tags) - {root}),
            "was_inferred": any(original_tag_map[t] for t in tags),
            "cluster_size": len(tags)
        }
    return alias_map

def merge_all_tags(all_tags):
    combined = []
    tag_was_inferred = {}
    for model_tags in all_tags.values():
        for tag, inferred in model_tags:
            combined.append((tag, inferred))
            tag_was_inferred[tag] = tag_was_inferred.get(tag, False) or inferred
    return list(set(combined)), tag_was_inferred

def save_alias_maps(alias_map, all_tags):
    os.makedirs("output/tag_alias_maps", exist_ok=True)
    with open("output/tag_alias_maps/tag_alias_map.json", "w") as f:
        json.dump(alias_map, f, indent=2)
    for model_name, tags in all_tags.items():
        tag_list = [t[0] for t in tags]
        model_alias_map = {k: v for k, v in alias_map.items() if k in tag_list}
        with open(f"output/tag_alias_maps/{model_name}_tag_alias_map.json", "w") as f:
            json.dump(model_alias_map, f, indent=2)

if __name__ == "__main__":
    all_tags = get_all_tags()
    combined_tags, tag_was_inferred = merge_all_tags(all_tags)
    print(f"\n\U0001F310 Total unique normalized tags: {len(combined_tags)}")

    tag_texts, embeddings = generate_embeddings(combined_tags)
    label_map = cluster_tags(tag_texts, embeddings)
    alias_map = build_alias_map(label_map, tag_was_inferred)

    print(f"\n✅ Final alias groups: {len(alias_map)}")
    save_alias_maps(alias_map, all_tags)
    print("\n\U0001F4BE Alias maps saved under /output/tag_alias_maps/")
