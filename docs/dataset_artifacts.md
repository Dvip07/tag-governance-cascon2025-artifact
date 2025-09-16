**Dataset & Artifacts Guide**

- Scope: Explains what each script does, the inputs it consumes, and the artifacts it writes (where and in what shape).
- Core concepts: HLJ = structured units extracted from a raw requirement (with title/summary/tags/etc.). Artifacts live under `eval/`, `output/`, and `sbert_fix/` roots depending on step.

**High-Level Flow**
- Raw requirements → HLJ preview/plan → Full HLJs → Validated HLJs → Audits/Reports → Tag mining → Tag clustering/aliasing → Top‑K tags → NLU validation (v3) → Domain filter → Analytics/visuals.

**Inputs**
- `eval/raw_requirement/<Domain>/req-XXX.md`: Source requirements (by domain, e.g., `FinTech`, `SaaS`).
- Prompt templates: `eval/prompts/hlj_structure_prompt.md`, `eval/prompts/hlj_generator_prompt.md`.

**Step 0: Scaffolding**
- Script: `scripts/scaffold_generation.py`
- Purpose: Create stub requirement files by domain (`req-001`…)
- Writes: `eval/raw_requirement/<Domain>/req-XXX.md`

**Step 1A: HLJ Preview/Plan**
- Script: `scripts/hlj_preview_generation.py`
- Reads: raw requirement (`eval/raw_requirement/<Domain>/req-*.md`), prompt template.
- Calls: Claude Opus 4 via `services.llm_clients.call_claude_opus4_model`.
- Writes under `eval/output/opus4/<req-id>/`:
  - `summary/step1_full_prompt.txt`: Full prompt sent to LLM
  - `summary/step1_response.txt`: Raw LLM response
  - `summary/summary_clean.json`: Parsed requirement summary
  - `hlj-preview/hlj_meta.json`: HLJ meta/config
  - `hlj-preview/hlj_plan.json`: Chunk plan (chunk ids, items, focus)

**Step 1B: HLJ Generation (by chunks)**
- Script: `scripts/hlj_generation.py`
- Reads: `hlj-preview/hlj_plan.json`, `hlj-preview/hlj_meta.json`, `summary/summary_clean.json`, and `eval/prompts/hlj_generator_prompt.md`.
- Calls: Claude Opus 4 to generate each chunk.
- Writes under `eval/output/<model>/<req-id>/hlj/` (model folder varies; code shows `opus4` while main enumerates `meta70b`):
  - `chunks/<CHUNK_ID>.json`: Full per‑chunk LLM JSON
  - `trim/<CHUNK_ID>_trim.json`: Flat list of HLJ items for that chunk
  - `merged/all_chunks_full.json`: All chunk outputs merged (audit view)
  - `trim_merged/all_trimmed_hljs.json`: Flat list of HLJ items across all chunks (primary downstream input)

Notes:
- If `trim_merged/all_trimmed_hljs.json` exists, the script skips re‑generation.
- Paths may use `eval/output/opus4` or `eval/output/meta70b` — keep them consistent in your runs.

**Step 0.5: Multi‑model Tag Concordance (optional analysis)**
- Script: `scripts/step_0.5/multi_model_tag_concordance.py`
- Reads manifests: `output/meta_opus4.yaml`, `output/meta_llama70b.yaml` (pair gold and candidate files), where each YAML maps `req_id` to `gold_path` (gpt41) and `candidate_path`.
- Computes: tag overlaps, disagreement, macro PRF vs GPT‑4.1.
- Writes under `output/score/`:
  - `hlj_overlap_stats.csv`, `hlj_missingness.csv`, `aggregate_agreement.csv`, `hlj_overlap_report.md` (+ optional `venn_plots/*.png`)

Companion manifest builder:
- Script: `scripts/meta_generation.py`
- Reads: `eval/output/gpt41/**/hlj/merged/all_chunks_full.json` and candidate model dirs (e.g., `eval/output/opus4` or `eval/output/meta70b`).
- Writes: `eval/output/meta_opus4.yaml`, `eval/output/meta_llama70b.yaml` (req‑to‑file pairs).

**Step 1: HLJ Validation + Auditing**
- Script: `scripts/step_1/validate_hljs.py`
- Reads: `output/<model>/<req-id>/hlj/trim_merged/all_trimmed_hljs.json` and raw requirement text.
- Normalizes tags using `tag_alias_maps/tag_alias_map.json` and validates with spaCy+SBERT.
- Writes under `sbert_fix/<model>/<req-id>/`:
  - `all_chunks_full_validated.json`: HLJs with tag versions and validation details
  - `tag_audit.yaml`: Per‑HLJ audit (original vs validated tags)

Fields (validated HLJs):
- `tags_v1`: original tags, `tags_v2`: validated tags, `tag_validation`: entries like `{original_tag, canonical_tag, tag_origin_cluster_id, original_confidence, validation_status, similarity, context, alias_used, timestamp}`.

Audits/Reports:
- `scripts/step_1/generate_audits.py`: regenerates `tag_audit.yaml` from validated JSON (uses key `validation_details` when present)
- `scripts/step_1/generate_changelog.py`: writes `sbert_fix/<model>/<req>/changelog.md`
- `scripts/step_1/generate_delta_summary.py`: writes `sbert_fix/delta_summary.csv` and `sbert_fix/delta_summary.md`
- `scripts/step_1/flagged_case_table.py`: writes `sbert_fix/flagged_cases.csv` and `.md`
- `scripts/step_1/analyze_change_trends.py`: aggregates `sbert_fix/delta_summary_*.csv` → `sbert_fix/change_trend_table.csv` and `.md`
- `scripts/step_1/list_dropped_tags.py`: writes `sbert_fix/gpt41/dropped_tags.csv` (configurable base)
- `scripts/step_1/validate_hlj_v3.py`: SBERT re‑checks dropped tags vs requirement; updates `tag_audit.yaml` in place (v3 tweaks)

**Step 2: Tag Mining, Clustering, Canonicalization, and NLU Validation**
- `scripts/step_2/harvest_tags.py`
  - Reads: `sbert_fix/<model>/<req>/all_chunks_full_validated.json`
  - Writes: `sbert_fix/all_tags/step_1/tags_all.csv` with columns: `tag, hlj_id, requirement_id, model, version (tags_v1|tags_v2), confidence, context, validation_status, inferred, flagged, reason_for_flagged`.

- `scripts/step_2/filter_tags_by_token_length.py`
  - Reads: `sbert_fix/all_tags/step_1/tags_all.csv` and raw requirements
  - Writes: `sbert_fix/all_tags/step_2/{final_tags.csv, filtered_tags.csv, rescued_tags.csv, dropped_tags.csv}`; enriches rows with `token_length, filtered, filter_reason, rescue_score, rescue_notes`.

- `scripts/step_2/cluster_tags_faiss_sbert.py`
  - Reads: `sbert_fix/all_tags/step_2/final_tags.csv`
  - Clusters with SBERT + FAISS (cosine) by all/by model/by version
  - Writes: `sbert_fix/all_tags/step_3/{tag_clusters.csv, tag_clusters_by_model.csv, tag_clusters_by_version.csv}` and YAML logs (`*_log.yaml`).

- `scripts/step_2/generate_canonical_labels.py` (v2)
  - Harvests `tags_v1/v2` domains from validated HLJs → assigns domain lists to tags
  - Writes: `sbert_fix/all_tags/step_4/canonical_tags_with_domain.yaml`, summary CSV (`tag_domain_summary.csv`), and a log; also maintains no‑domain `canonical_tags.yaml`.

- `scripts/step_2/deduplicate_tags.py`
  - Reads: `sbert_fix/all_tags/step_3/tag_clusters.csv`, `sbert_fix/all_tags/step_4/tag_alias_map.json`
  - SBERT similarity within clusters to map aliases → canonicals
  - Writes: `sbert_fix/all_tags/step_5/{deduplicated_tags.csv, deduplicate_audit_log.json}`

- `scripts/step_2/score_tags.py`
  - Reads: `sbert_fix/all_tags/step_2/final_tags.csv`, `sbert_fix/all_tags/step_5/deduplicated_tags.csv`, and dropped set
  - Scores per‑HLJ tag votes across versions/models; keeps top‑K
  - Writes: `sbert_fix/all_tags/step_6/topk_tags_per_hlj.json` with `{hlj_id, tags:[{tag, score, method, model, version, confidence, original_tag}]}`

- `scripts/step_2/validate_tags_nlu.py`
  - Reads: `sbert_fix/all_tags/step_6/topk_tags_per_hlj.json`, raw requirements, and per‑model validated JSONs
  - Produces hybrid v3: copies each model’s `all_chunks_full_validated.json` into `sbert_fix/hybrid/<model>/<req>/all_chunks_full_validated.json` and appends:
    - `tags_v3`: NLU‑validated top‑K tags
    - `tag_nlu_validation`: detailed rows `{tag, score, model, version, method, confidence, validated, validation_reason, hlj_id, req_id}`
  - Writes stats: `sbert_fix/hybrid/nlu_validation_stats.csv` (+ `borderline_nlu_tags.csv`)

- `scripts/step_2/filter_tags_domain.py`
  - Reads: `sbert_fix/all_tags/step_4/canonical_tags_with_domain.yaml`, hybrid v3 JSONs
  - Domain‑whitelists tags per HLJ domain
  - Writes: `sbert_fix/hybrid/domain_filtered_tags_per_hlj.{json,csv}` and a log of HLJs with all tags mismatched.

- `scripts/step_2/evaluate_tag_accuracy.py`
  - Reads: `sbert_fix/hlj_tag_metadata/*.json` (expected per‑HLJ metadata with `tags_v1/v2/v3`, `model`, `domain`)
  - Scores precision/recall/F1/Jaccard across versions (configurable GOLD version)
  - Writes: `sbert_fix/{tag_eval_stats.csv, tag_eval_report.md, tag_eval_stats_by_domain.csv}`

**Visualization**
- Script: `scripts/visualize/count_hljs_bar_chart.py`
- Reads: `eval/output/<model>/<req>/hlj/trim_merged/all_trimmed_hljs.json`
- Writes: `eval/visualize/bar_chart/hlj_count_bar_chart.png`

**Key Artifact Schemas**
- `eval/output/**/hlj/trim_merged/all_trimmed_hljs.json` (list): HLJ items `{id, title, summary, domain, subdomain, tags, difficulty, priority, line_source, reasoning?}`
- `sbert_fix/<model>/<req>/all_chunks_full_validated.json` (list): HLJs with `tags_v1`, `tags_v2`, `tag_validation` (see Step 1 fields).
- `sbert_fix/<model>/<req>/tag_audit.yaml` (list of HLJ audits): `{hlj_id, requirement, model, timestamp, original_tags, validated_tags, tags_added, tags_dropped, tags_kept, validation_details[]}`
- `sbert_fix/all_tags/step_1/tags_all.csv`: harvested tags across versions
- `sbert_fix/all_tags/step_2/*.csv`: filtered/rescued/dropped logs with similarity and reasons
- `sbert_fix/all_tags/step_3/tag_clusters*.csv`: cluster assignments (`tag, hlj_id, requirement_id, model, version, cluster_id`)
- `sbert_fix/all_tags/step_4/canonical_tags_with_domain.yaml`: `tag: {aliases: [], cluster_id: <id>, domains: [..]}`
- `sbert_fix/all_tags/step_5/deduplicated_tags.csv`: `canonical_tag, alias, method, similarity, cluster_id, version`
- `sbert_fix/all_tags/step_6/topk_tags_per_hlj.json`: per‑HLJ top‑K tags with vote scores
- `sbert_fix/hybrid/**/all_chunks_full_validated.json`: hybrid v3 additions (`tags_v3`, `tag_nlu_validation`)
- `sbert_fix/hybrid/domain_filtered_tags_per_hlj.{json,csv}`: domain validation per tag (`domain_valid`, `validation_reason`)

**Running Order (typical)**
- HLJ preview/plan: `python scripts/hlj_preview_generation.py`
- HLJ chunks: `python scripts/hlj_generation.py`
- Validate HLJs: `python scripts/step_1/validate_hljs.py`
- Audits/changelogs/summaries: run scripts in `scripts/step_1/`
- Tag pipeline: run scripts in `scripts/step_2/` in numbered order shown above
- Optional multi‑model analysis: `python scripts/step_0.5/multi_model_tag_concordance.py`
- Visualization: `python scripts/visualize/count_hljs_bar_chart.py`

**Conventions & Notes**
- Model roots vary by step: some scripts use `eval/output/<model>` while others assume `output/<model>`. Align paths (or move/symlink) to keep scripts happy.
- Validation keys naming: older scripts use `tag_results`; newer ones expect `validation_details`. The YAML audit writer handles either when present.
- Dependencies: spaCy (`en_core_web_sm`), `sentence_transformers`, FAISS, PyTorch, pandas, PyYAML, matplotlib. Some steps require GPU/accelerated backends for speed.
- Utils: `scripts/utils/pipeline_audit.py` can write per‑step manifests and a grand manifest for reproducibility.

**At‑a‑Glance Map**
- Inputs: `eval/raw_requirement/**`
- Generated HLJ: `eval/output/<model>/<req>/hlj/**`
- Validated HLJ + audits: `sbert_fix/<model>/<req>/**`
- Tag pipeline: `sbert_fix/all_tags/step_{1..6}/**`
- Hybrid v3 + domain filtering: `sbert_fix/hybrid/**`
- Multi‑model analysis: `output/score/**` (via YAML manifests in `eval/output/meta_*.yaml`)
- Visuals: `eval/visualize/**`

