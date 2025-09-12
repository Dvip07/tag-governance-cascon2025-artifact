import pathlib
import logging
import re
import json
import sys

ROOT_DIR = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from services.llm_clients import call_claude_opus4_model

BASE_DIR = pathlib.Path("eval")
DOMAINS = ["SaaS"]
PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "hlj_structure_prompt.md"

# ── Logger ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("step1_hlj")

# ── Helper Functions ─────────────────────────────────────────────────────────
def load_file(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""

def extract_json_section(text, marker):
    # First, try to match with ```json fenced blocks
    pattern_fenced = rf"### === {re.escape(marker)} START ===\s*```json(.*?)```\s*### === {re.escape(marker)} END ==="
    match = re.search(pattern_fenced, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception as e:
            logger.error(f"JSON parsing error (fenced) in section {marker}: {e}")
            return {}

    # Fallback: match plain JSON between fences (your current format)
    pattern_plain = rf"### === {re.escape(marker)} START ===\s*\n(.*?)\n### === {re.escape(marker)} END ==="
    match = re.search(pattern_plain, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception as e:
            logger.error(f"JSON parsing error (plain) in section {marker}: {e}")
            return {}

    logger.warning(f"Section {marker} not found or not formatted as JSON.")
    return {}


# ── Main Pipeline ────────────────────────────────────────────────────────────
def process_requirement(domain, req_file):
    req_id = req_file.stem  # "req-001"
    logger.info(f"📦 Running HLJ Step 1 for {domain}/{req_id}")

    OUTPUT_DIR = BASE_DIR / "output" / "opus4" / req_id
    PREVIEW_DIR = OUTPUT_DIR / "hlj-preview"
    hlj_plan_json_path = PREVIEW_DIR / "hlj_plan.json"
    # ---- Skip if already generated ----
    if hlj_plan_json_path.exists():
        logger.info(f"⏩ Skipping {req_id} (already processed).")
        return

    requirement = load_file(req_file)
    prompt_template = load_file(PROMPT_TEMPLATE_PATH)
    req_id_upper = req_id.upper()
    prompt_filled = (
        prompt_template
        .replace("{{REQ-id}}", req_id_upper)
        .replace("{{RAW_REQUIREMENT}}", requirement)
    )

    SUMMARY_DIR = OUTPUT_DIR / "summary"
    for path in [SUMMARY_DIR, PREVIEW_DIR]:
        path.mkdir(parents=True, exist_ok=True)

    (SUMMARY_DIR / "step1_full_prompt.txt").write_text(prompt_filled, encoding="utf-8")

    logger.info("⏳ Calling Claude Opus 4...")
    result = call_claude_opus4_model(prompt_filled)
    (SUMMARY_DIR / "step1_response.txt").write_text(result, encoding="utf-8")

    summary_json = extract_json_section(result, "SUMMARY")
    meta_json = extract_json_section(result, "HLJ_META")
    plan_json = extract_json_section(result, "HLJ_PLAN")

    (SUMMARY_DIR / "summary_clean.json").write_text(json.dumps(summary_json, indent=2), encoding="utf-8")
    (PREVIEW_DIR / "hlj_meta.json").write_text(json.dumps(meta_json, indent=2), encoding="utf-8")
    (PREVIEW_DIR / "hlj_plan.json").write_text(json.dumps(plan_json, indent=2), encoding="utf-8")

    logger.info(f"✅ Done. Structured JSON saved under: {OUTPUT_DIR}")


def main():
    for domain in DOMAINS:
        domain_dir = BASE_DIR / "raw_requirement" / domain
        if not domain_dir.exists():
            logger.warning(f"Domain folder does not exist: {domain_dir}")
            continue

        for req_file in sorted(domain_dir.glob("req-*.md")):
            process_requirement(domain, req_file)

if __name__ == "__main__":
    main()
