import yaml
import json
from sklearn.metrics import precision_recall_fscore_support
from collections import defaultdict

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def extract_all_hljs_from_chunks(chunk_list):
    """Given a list of chunk dicts, extract all HLJ items from all CURRENT_CHUNK->DATA lists."""
    all_hljs = []
    for chunk in chunk_list:
        try:
            data_items = chunk.get("CURRENT_CHUNK", {}).get("DATA", [])
            all_hljs.extend(data_items)
        except Exception as e:
            print(f"Error extracting HLJs from chunk: {e}")
    return all_hljs


with open('eval/output/meta_llama70b.yaml') as f:
    meta = yaml.safe_load(f)

field_scores = defaultdict(lambda: {'tp':0, 'fp':0, 'fn':0, 'gold':[], 'cand':[]})

for pair in meta:
    gold = load_json(pair['gold_path'])
    cand = load_json(pair['candidate_path'])
    gold_hljs = extract_all_hljs_from_chunks(gold)
    cand_hljs = extract_all_hljs_from_chunks(cand)

    
    # Match by ID (robust); fallback to index if needed
    gold_map = {h['id']: h for h in gold_hljs}
    cand_map = {h['id']: h for h in cand_hljs}
    all_ids = set(gold_map) | set(cand_map)
    
    for hlj_id in all_ids:
        g = gold_map.get(hlj_id)
        c = cand_map.get(hlj_id)
        for field in ['title', 'difficulty', 'priority', 'tags']:  # Add more fields as needed
            if g is None:
                field_scores[field]['fp'] += 1
            elif c is None:
                field_scores[field]['fn'] += 1
            else:
                # For list fields (tags): compare as set
                if isinstance(g[field], list) and isinstance(c[field], list):
                    gold_set, cand_set = set(g[field]), set(c[field])
                    tp = len(gold_set & cand_set)
                    fp = len(cand_set - gold_set)
                    fn = len(gold_set - cand_set)
                    field_scores[field]['tp'] += tp
                    field_scores[field]['fp'] += fp
                    field_scores[field]['fn'] += fn
                    field_scores[field]['gold'].extend(list(gold_set))
                    field_scores[field]['cand'].extend(list(cand_set))
                else:
                    match = (g[field] == c[field])
                    field_scores[field]['tp'] += int(match)
                    field_scores[field]['fp'] += int(not match)
                    field_scores[field]['fn'] += int(not match)
                    field_scores[field]['gold'].append(g[field])
                    field_scores[field]['cand'].append(c[field])

# Calculate Precision/Recall/F1 per field
for field, scores in field_scores.items():
    tp, fp, fn = scores['tp'], scores['fp'], scores['fn']
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    print(f"\nField: {field}\nPrecision: {precision:.3f}\nRecall: {recall:.3f}\nF1: {f1:.3f}")

# (Optional) Save CSV/LaTeX table or plot
