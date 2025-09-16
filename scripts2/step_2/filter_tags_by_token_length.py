import os
import csv
import math
from statistics import median
from sentence_transformers import SentenceTransformer, util

# === CONFIG ===
STEP1_INPUT = "sbert_fix/all_tags/step_1/tags_all.csv"
STEP2_OUTPUT_ALL = "sbert_fix/all_tags/step_2/final_tags.csv"
STEP2_OUTPUT_FILTERED = "sbert_fix/all_tags/step_2/filtered_tags.csv"
STEP2_OUTPUT_RESCUED = "sbert_fix/all_tags/step_2/rescued_tags.csv"
STEP2_OUTPUT_DROPPED = "sbert_fix/all_tags/step_2/dropped_tags.csv"
RAW_REQ_BASE = "raw_requirement"
SBERT_MODEL = "all-MiniLM-L6-v2"
SBERT_THRESHOLD_STRONG = 0.40
SBERT_THRESHOLD_WEAK = 0.20

os.makedirs(os.path.dirname(STEP2_OUTPUT_ALL), exist_ok=True)

def get_token_length(tag):
    return len(tag.strip().split())

def get_domain_from_req_id(req_id):
    for domain in ["FinTech", "SaaS"]:
        req_path = os.path.join(RAW_REQ_BASE, domain, f"{req_id}.md")
        if os.path.exists(req_path):
            return domain
    return None

def load_raw_requirement(req_id):
    domain = get_domain_from_req_id(req_id)
    if not domain:
        return ""
    path = os.path.join(RAW_REQ_BASE, domain, f"{req_id}.md")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def keyword_match(tag, text):
    return tag.lower() in text.lower()

def main():
    print("\U0001f50e Loading SBERT model...")
    sbert = SentenceTransformer(SBERT_MODEL)

    rows = []
    token_lengths = []
    req_cache = {}

    with open(STEP1_INPUT, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag = row['tag']
            tlen = get_token_length(tag)
            row['token_length'] = tlen
            token_lengths.append(tlen)
            rows.append(row)

    med = math.ceil(median(token_lengths))
    print(f"\U0001f4cf Median token length: {med}")

    final_rows = []
    filtered_rows = []
    rescued_rows = []
    dropped_rows = []

    for row in rows:
        tag = row['tag']
        req_id = row['requirement_id']
        tlen = int(row['token_length'])
        flagged = row.get("flagged", "").lower() == "yes"
        inferred = row.get("inferred", "").lower() == "yes"

        needs_check = flagged or inferred or tlen > med
        row['rescue_score'] = ''
        row['rescue_notes'] = ''
        row['filtered'] = 'N'
        row['filter_reason'] = 'passed_all_filters'

        if not needs_check:
            final_rows.append(row)
            continue

        if req_id not in req_cache:
            req_text = load_raw_requirement(req_id)
            req_cache[req_id] = req_text
        else:
            req_text = req_cache[req_id]

        if not req_text.strip():
            row['filtered'] = 'Y'
            row['filter_reason'] = 'suspicious_and_no_raw_requirement'
            filtered_rows.append(row)
            dropped_rows.append(row)
            print(f"\U0001f5d1️ Dropped: '{tag}' for {req_id} | Reason: suspicious_and_no_raw_requirement")
            continue

        try:
            tag_emb = sbert.encode(tag, convert_to_tensor=True)
            req_emb = sbert.encode(req_text, convert_to_tensor=True)
            sim = util.cos_sim(tag_emb, req_emb).item()
            row['rescue_score'] = f"{sim:.3f}"
        except Exception as e:
            row['filtered'] = 'Y'
            row['filter_reason'] = 'sbert_encoding_failed'
            filtered_rows.append(row)
            dropped_rows.append(row)
            print(f"❌ SBERT failed on tag '{tag}' or req '{req_id}': {e}")
            continue

        if sim >= SBERT_THRESHOLD_STRONG:
            row['filtered'] = 'N'
            row['filter_reason'] = 'rescued_by_strong_semantic_match'
            row['rescue_notes'] = 'strong semantic match with raw requirement'
            if not row.get('context'):
                row['context'] = 'inferred_by_sbert'
            if not row.get('validation_status'):
                row['validation_status'] = 'semantically_inferred'
            if not row.get('confidence'):
                row['confidence'] = f"{sim:.2f}"
            rescued_rows.append(row)
        elif sim >= SBERT_THRESHOLD_WEAK:
            row['filtered'] = 'N'
            row['filter_reason'] = 'rescued_by_weak_semantic_match'
            row['rescue_notes'] = 'weak semantic match — flagged as low confidence'
            row['confidence'] = f"{sim:.2f}"
            row['context'] = 'low_confidence'
            rescued_rows.append(row)
        elif keyword_match(tag, req_text):
            row['filtered'] = 'N'
            row['filter_reason'] = 'rescued_by_keyword_match'
            row['rescue_notes'] = 'tag appears in raw requirement text'
            row['confidence'] = 'keyword_based'
            row['context'] = 'keyword_match'
            rescued_rows.append(row)
        else:
            row['filtered'] = 'Y'
            row['filter_reason'] = f'suspicious_and_no_semantic_match:{sim:.3f}'
            dropped_rows.append(row)
            print(f"\U0001f5d1️ Dropped: '{tag}' for {req_id} | Reason: suspicious_and_no_semantic_match:{sim:.3f}")

        final_rows.append(row)

    def save_csv(path, data):
        if not data:
            print(f"⚠️ No data to write to {path}")
            return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)

    save_csv(STEP2_OUTPUT_ALL, final_rows)
    save_csv(STEP2_OUTPUT_FILTERED, filtered_rows)
    save_csv(STEP2_OUTPUT_RESCUED, rescued_rows)
    save_csv(STEP2_OUTPUT_DROPPED, dropped_rows)

    print(f"✅ All done. Outputs:")
    print(f"  - Full log:        {STEP2_OUTPUT_ALL} ({len(final_rows)} rows)")
    print(f"  - Filtered tags:   {STEP2_OUTPUT_FILTERED} ({len(filtered_rows)} rows)")
    print(f"  - Rescued tags:    {STEP2_OUTPUT_RESCUED} ({len(rescued_rows)} rows)")
    print(f"  - Dropped tags:    {STEP2_OUTPUT_DROPPED} ({len(dropped_rows)} rows)")

if __name__ == '__main__':
    main()
