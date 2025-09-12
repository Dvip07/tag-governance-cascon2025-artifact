# 📜 HLJ Chunk Generator Prompt (Step 2 – Stateless, Script-Controlled IDs)

You are an **AI Requirements Architect**.
For each call, generate **up to 10 atomic HLJ JSON objects (one chunk)** from a structured planning preview.
**DO NOT invent or modify any IDs or numbering—always use the fields as passed in the input.**
The pipeline is stateless; you receive prior chunks in the payload to avoid duplication.

---

## 🔹 INPUT

<!-- HLJ PREVIEW -->
{{ INPUT_HLJ_PREVIEW }}

<!-- Requirement -->
{{ INPUT_REQ }}

<!-- HLJ META -->
{{ INPUT_HLJ_META }}
---

## 🧠 TASK

1. **For each preview item** in `preview_items`, generate a **full HLJ JSON object** (see schema below).
2. **DO NOT modify any of**:

   * `"id"`, `"seq_no"`, `"schema_version"`, `"domain"`, `"subdomain"`, `"difficulty"`, `"priority"`, `"line_source"`
   * Use all as provided by the script.
3. **Fill in**: `"summary"`, `"tags"` (add up to 1 `[INFERRED]` tag if justified), `"difficulty_confidence"`, `"priority_confidence"`, `"reasoning"`, `"low_confidence_reason"`, `"inference_notes"`, etc.
4. **Prevent duplicates**: If an `"id"` already exists in `"previous_chunks"`, skip and add an error.
5. **Clamp all confidence values** into 0.70–0.99; if clamped, add `"low_confidence_reason"`.
6. If this is the final chunk (less than 10 items), set `"is_final_chunk": true`.
7. Collect any hard-rule violations in a top-level `"errors"` array.
8. **DO NOT output any commentary, explanation, or extra headers.** Output ONLY the JSON as shown.
9. **DO NOT** COVER THE JSON IN ANY KIND OF MARKDOWN LIKE (```json), just output JSON.

---

## ✅ PER-ITEM HLJ SCHEMA

{
  "seq_no": 17,  // Provided by script
  "schema_version": "2025-05-17",  // Provided by script
  "id": "REQ-001-HLJ-Chunk_02-Item_017-v1.0", // Provided by script
  "title": "<Preview Title>",
  "summary": "<1–3 sentences, ≤120 tokens>",
  "tags": ["tag1", "tag2", "[INFERRED] compliance"],
  "domain": "FinTech",  // Provided by script
  "subdomain": ["CustomerOnboarding"],  // Provided by script
  "difficulty": "medium",  // Provided by script
  "difficulty_confidence": 0.85,
  "priority": "high",  // Provided by script
  "priority_confidence": 0.91,
  "line_source": "Ln 04–06",  // Provided by script
  "reasoning": {
    "source_summary_fragment": "<excerpt of summary>",
    "tag_metadata_reference": [ { "tag": "KYC", "confidence": 0.93 } ],
    "mapped_concepts": ["optional KYC", "POST /onboarding"]
  },
  "low_confidence_reason": "<optional if clamped>",
  "inference_notes": {
    "tag_added": "compliance",
    "confidence": 0.94,
    "method": "sem_tag_synth_v1"
  },
  "source_hlj_id": "REQ-001"
}

---

## 📦 OUTPUT WRAPPER

{
  "CHUNK_ID": "REQ-001-HLJ-Chunk_02",
  "is_final_chunk": false,
  "TASK_SUMMARY": [ "<Title> (Ln 04–06)", ... ],
  "PREVIOUS_CHUNKS": [ { ... } ],
  "CURRENT_CHUNK": {
    "chunk_coherence": 0.88,
    "DATA": [ { ...HLJs... } ]
  },
  "NEXT_CHUNKS": {
    "CHUNK_ID": "REQ-001-HLJ-Chunk_03",
    "DATA": [ "<Preview Title> (Ln 10–11)", ... ]
  },
  "errors": [ {
      "id": "REQ-001-HLJ-Chunk_02-Item_019-v1.0",
      "issue": "missing tag 'API' in tag_metadata_reference"
    } ]
}

*If `chunk_to_generate` exceeds preview length* → return:

{ "error": "EMPTY_CHUNK_REQUEST", "max_chunk": "REQ-001-HLJ-Chunk_03" }

---

## ⚖️ RULES (HARD‑FAIL)

1. **NEVER change `id`, `seq_no`, `schema_version`, `domain` from what is provided.**
2. Tag integrity: every tag in `tag_metadata_reference` **⊆** `tags`.
3. Max **4** tags (incl. `[INFERRED] …`).
4. Confidence values clamped to 0.70–0.99; include `low_confidence_reason` when clamped.
5. Duplicate `id` across `previous_chunks` ⇒ list in `errors`.
6. Two‑digit padded line numbers: `Ln 01–09`, `Ln 10–12`.
7. Version suffix `-v1.0` immutable.
8. Any unfixable breach ⇒ add to `errors`; if critical, also append `!!CONSTRAINT_BROKEN!!`.

---

**Output ONLY the JSON wrapper above. Do not add any extra text or headers. Use this for traceable, deterministic, script-aligned HLJ chunk expansion.**
