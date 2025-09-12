import pathlib
import logging
import json
import math
import sys
import re

ROOT_DIR = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from services.llm_clients import call_claude_opus4_model

BASE_DIR = pathlib.Path("eval")
DOMAINS = ["FinTech", "SaaS"]

CHUNK_SIZE = 10
CHUNK_PROMPT_PATH = BASE_DIR / "prompts" / "hlj_generator_prompt.md"
SCHEMA_VERSION = "2025-05-28"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("step2_hlj_chunk")

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    
def clean_llm_response(raw_response):
    """
    Strips markdown code fences and leading/trailing whitespace from LLM output.
    Handles both ```json ... ``` and plain ```
    """
    # Remove leading/trailing whitespace
    resp = raw_response.strip()

    # Remove ```json or ``` at start, and closing ```
    if resp.startswith("```json"):
        resp = resp[len("```json"):].strip()
    elif resp.startswith("```"):
        resp = resp[len("```"):].strip()

    # Remove ending ```
    if resp.endswith("```"):
        resp = resp[:-3].strip()

    # Remove any stray code fences inside the string (rare)
    resp = re.sub(r"```[a-zA-Z]*\n?", '', resp)
    resp = re.sub(r"\n```", '', resp)

    return resp

def run_chunks_for_requirement(req_id, domain):
    output_dir = BASE_DIR / "output" / "opus4" / req_id
    preview_dir = output_dir / "hlj-preview"
    hlj_dir = output_dir / "hlj"
    chunks_dir = hlj_dir / "chunks"
    merged_dir = hlj_dir / "merged"
    trim_dir = hlj_dir / "trim"
    trim_merged_dir = hlj_dir / "trim_merged"

    # -------- SKIP IF EXISTS --------
    trim_merged_file = trim_merged_dir / "all_trimmed_hljs.json"
    if trim_merged_file.exists():
        logger.warning(f"⏩ Skipping {req_id} — Trimmed HLJ already exists at {trim_merged_file}")
        return
    # --------------------------------

    for d in [chunks_dir, merged_dir, trim_dir, trim_merged_dir]:
        d.mkdir(parents=True, exist_ok=True)
    # ... rest of your function as before ...


# def run_chunks_for_requirement(req_id, domain):
#     output_dir = BASE_DIR / "output" / "meta70b" / req_id
#     preview_dir = output_dir / "hlj-preview"
#     hlj_dir = output_dir / "hlj"
#     chunks_dir = hlj_dir / "chunks"
#     merged_dir = hlj_dir / "merged"
#     trim_dir = hlj_dir / "trim"
#     trim_merged_dir = hlj_dir / "trim_merged"

#     for d in [chunks_dir, merged_dir, trim_dir, trim_merged_dir]:
        # d.mkdir(parents=True, exist_ok=True)

    # Load plan/meta/summary from Step 1 output (JSON)
    plan_path = preview_dir / "hlj_plan.json"
    meta_path = preview_dir / "hlj_meta.json"
    summary_path = output_dir / "summary" / "summary_clean.json"
    if not plan_path.exists() or not meta_path.exists() or not summary_path.exists():
        logger.warning(f"Missing required HLJ plan/meta/summary for {req_id}, skipping.")
        return

    hlj_plan = load_json(plan_path)
    hlj_meta = load_json(meta_path)
    hlj_summary = load_json(summary_path)
    all_chunks_data = hlj_plan.get("chunks", [])

    logger.info(f"➡️  Processing {req_id}: {len(all_chunks_data)} chunk(s) found")
    previous_chunks = []
    all_chunks = []
    all_trimmed = []
    seq_no = 1

    for chunk in all_chunks_data:
        chunk_id = chunk.get("chunk_id")
        chunk_items = chunk.get("items", [])
        focus = chunk.get("focus", "unknown")
        is_final_chunk = chunk == all_chunks_data[-1]

        # Assemble per-chunk payload for LLM
        items_for_llm = []
        for item in chunk_items:
            # Script generates/assigns the seq_no, schema_version, etc.
            item_out = {
                "seq_no": seq_no,
                "schema_version": SCHEMA_VERSION,
                "id": item["id"],
                "title": item["title"],
                "domain": item["domain"],
                "subdomain": item["subdomain"],
                "tags": item["tags"],
                "difficulty": item["difficulty"],
                "priority": item["priority"],
                "line_source": item["line_source"]
            }
            items_for_llm.append(item_out)
            seq_no += 1

        prompt_payload = {
            "requirement_id": req_id.upper(),
            "summary": hlj_summary.get("summary", ""),
            "hlj_meta": hlj_meta,
            "chunk_to_generate": chunk_id,
            "preview_items": items_for_llm,
            "previous_chunks": previous_chunks
        }

        # Load and fill chunk prompt template
        chunk_prompt_template = CHUNK_PROMPT_PATH.read_text(encoding="utf-8")
        # Inject actual preview, summary, and meta fields into placeholders
        pretty_preview = json.dumps(items_for_llm, indent=2)
        pretty_req = json.dumps({"requirement_id": req_id.upper(), "summary": hlj_summary.get("summary", "")}, indent=2)
        pretty_meta = json.dumps(hlj_meta, indent=2)

        full_prompt = (
            chunk_prompt_template
            .replace("{{ INPUT_HLJ_PREVIEW }}", pretty_preview)
            .replace("{{ INPUT_REQ }}", pretty_req)
            .replace("{{ INPUT_HLJ_META }}", pretty_meta)
        )
        # Logging the prompt for debugging
        logger.debug(f"Full prompt for {chunk_id}:\n{full_prompt}")


        # Call LLM
        logger.info(f"  ⏳ Generating {chunk_id} ...")
                # --- Debug preview_items ---
        logger.info(f"[DEBUG] items_for_llm count for {chunk_id}: {len(items_for_llm)}")
        logger.info(f"[DEBUG] preview_items titles: {[item['title'] for item in items_for_llm]}")
        logger.debug(f"[DEBUG] preview_items sample: {json.dumps(items_for_llm[:2], indent=2)}")  # First 2

        # --- Debug prompt ---
        logger.debug(f"[PROMPT SENT TO LLM - {chunk_id}]\n{full_prompt[:1000]}... [truncated] ...")

        response = call_claude_opus4_model(full_prompt)
        logger.error(f"[RAW LLM RESPONSE] {response}")
        clean_response = clean_llm_response(response)
        response_json = json.loads(clean_response)

        # Store the full wrapper output
        chunk_file = chunks_dir / f"{chunk_id}.json"
        save_json(chunk_file, response_json)
        all_chunks.append(response_json)

        # Trimmed HLJs only for this chunk
        trimmed = response_json.get("CURRENT_CHUNK", {}).get("DATA", [])
        trim_file = trim_dir / f"{chunk_id}_trim.json"
        save_json(trim_file, trimmed)
        all_trimmed.extend(trimmed)

        # Update previous_chunks for the next call
        previous_chunks.append({
            "CHUNK_ID": chunk_id,
            "DATA": trimmed
        })

    # Merged full chunks (audit)
    merged_file = merged_dir / "all_chunks_full.json"
    save_json(merged_file, all_chunks)

    # Trim-merged, only HLJs, flat array
    trim_merged_file = trim_merged_dir / "all_trimmed_hljs.json"
    save_json(trim_merged_file, all_trimmed)

    logger.info(f"✅ Finished all chunks for {req_id}: {len(all_trimmed)} HLJs")

def main():
    for domain in DOMAINS:
        domain_dir = BASE_DIR / "output" / "meta70b"
        for req_folder in sorted(domain_dir.iterdir()):
            if not req_folder.is_dir():
                continue
            req_id = req_folder.name
            preview_dir = req_folder / "hlj-preview"
            summary_dir = req_folder / "summary"
            if not (preview_dir / "hlj_plan.json").exists():
                continue
            if not (preview_dir / "hlj_meta.json").exists():
                continue
            if not (summary_dir / "summary_clean.json").exists():
                continue
            run_chunks_for_requirement(req_id, domain)

if __name__ == "__main__":
    main()
