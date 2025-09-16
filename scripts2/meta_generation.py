import pathlib
import yaml

GOLD_DIR = pathlib.Path('eval/output/gpt41')
CANDIDATE_DIRS = {
    "llama70b": pathlib.Path('eval/output/meta70b'),
    "opus4": pathlib.Path('eval/output/opus4')
}
META_BASE = pathlib.Path('eval/output')

def find_all_json_files(root, pattern="all_chunks_full.json"):
    # Looks for files matching the pattern inside any subfolder of root
    return {p.parent.parent.parent.name: p for p in root.glob(f"*/hlj/merged/{pattern}")}

gold_files = find_all_json_files(GOLD_DIR)

for candidate_name, candidate_dir in CANDIDATE_DIRS.items():
    candidate_files = find_all_json_files(candidate_dir)
    meta = []
    for req_id in sorted(gold_files.keys()):
        if req_id in candidate_files:
            meta.append({
                'req_id': req_id,
                'gold_path': str(gold_files[req_id]),
                'candidate_path': str(candidate_files[req_id])
            })
    meta_path = META_BASE / f'meta_{candidate_name}.yaml'
    with open(meta_path, 'w') as f:
        yaml.dump(meta, f, sort_keys=False)
    print(f"✅ {meta_path} written with {len(meta)} pairs! (model: {candidate_name})")
