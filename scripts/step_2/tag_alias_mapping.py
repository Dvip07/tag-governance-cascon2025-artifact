import os
import re
import json
import argparse
from collections import defaultdict
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

from scripts.utils.config_resolver import ConfigResolver
from scripts.utils.pipeline_context import get_current_run


# ========= Helpers =========
def normalize_tag(tag: str):
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


def get_all_tags(model_dirs, target_filename):
    all_tags = defaultdict(list)
    for model_dir in model_dirs:
        model_name = os.path.basename(model_dir)
        tag_set = []
        for root, _, files in os.walk(model_dir):
            if target_filename in files:
                tags = extract_tags_from_file(os.path.join(root, target_filename))
                tag_set.extend(tags)
        all_tags[model_name] = tag_set
        print(f"📦 {model_name}: {len(tag_set)} tags")
    return all_tags


def generate_embeddings(tag_list, model_name):
    model = SentenceTransformer(model_name)
    tag_texts = [t[0] for t in tag_list]
    embeddings = model.encode(tag_texts, convert_to_tensor=True)
    return tag_texts, embeddings


def cluster_tags(tag_texts, embeddings, sim_threshold):
    if len(tag_texts) <= 1:
        return {}
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=1 - sim_threshold,
        linkage="average",
        metric="cosine",
    )
    clustering.fit(embeddings.cpu())
    label_map = defaultdict(list)
    for tag, label in zip(tag_texts, clustering.labels_):
        label_map[label].append(tag)
    return label_map


def build_alias_map(label_map, original_tag_map):
    alias_map = {}
    for label, tags in label_map.items():
        if len(tags) < 2:
            continue
        root = min(tags, key=len)  # shortest = canonical
        alias_map[root] = {
            "aliases": sorted(set(tags) - {root}),
            "was_inferred": any(original_tag_map.get(t, False) for t in tags),
            "cluster_size": len(tags),
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


def save_alias_maps(alias_map, all_tags, out_dir, run_id):
    os.makedirs(out_dir, exist_ok=True)
    main_file = os.path.join(out_dir, f"tag_alias_map_{run_id}.json")
    with open(main_file, "w") as f:
        json.dump(alias_map, f, indent=2)

    for model_name, tags in all_tags.items():
        tag_list = [t[0] for t in tags]
        model_alias_map = {k: v for k, v in alias_map.items() if k in tag_list}
        with open(os.path.join(out_dir, f"{model_name}_tag_alias_map_{run_id}.json"), "w") as f:
            json.dump(model_alias_map, f, indent=2)

    print(f"💾 Alias maps saved under {out_dir}")
    return main_file


# ========= Main =========
def main(cfg, run_id, model_dirs=None, target_file=None, sim_threshold=None, out_dir=None, embed_model=None):
    # resolve from config
    model_dirs = model_dirs or cfg.get("step3.model_dirs", [])
    target_file = target_file or cfg.get("step3.target_filename", "all_trimmed_hljs.json")
    sim_threshold = sim_threshold or cfg.get("step3.sim_threshold", 0.85)
    out_dir = out_dir or cfg.get("outputs.tag_alias_maps", "eval/v1/tag_alias_maps")
    embed_model = embed_model or cfg.get("step3.embedding_model", "all-MiniLM-L6-v2")

    all_tags = get_all_tags(model_dirs, target_file)
    combined_tags, tag_was_inferred = merge_all_tags(all_tags)
    print(f"\n🌍 Total unique normalized tags: {len(combined_tags)}")

    tag_texts, embeddings = generate_embeddings(combined_tags, embed_model)
    label_map = cluster_tags(tag_texts, embeddings, sim_threshold)
    alias_map = build_alias_map(label_map, tag_was_inferred)

    print(f"\n✅ Final alias groups: {len(alias_map)}")
    main_file = save_alias_maps(alias_map, all_tags, out_dir, run_id)

    # update YAML so downstream knows which file to use
    cfg.set("outputs.tag_alias_map", main_file)  # ✅ persistent write
    cfg.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 3: Build tag alias maps")
    parser.add_argument("--config", default="configs/pipeline_v1.yaml", help="Path to config YAML")
    parser.add_argument("--out_dir", help="Override output directory")
    parser.add_argument("--sim_threshold", type=float, help="Override similarity threshold")
    parser.add_argument("--embed_model", help="Override embedding model")
    args = parser.parse_args()

    cfg = ConfigResolver(args.config)
    run_id = get_current_run(args.config)
    main(cfg, run_id, out_dir=args.out_dir, sim_threshold=args.sim_threshold, embed_model=args.embed_model)
