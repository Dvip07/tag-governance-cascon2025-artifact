# Plantric HLJ & Tag Governance Pipeline — README

> End‑to‑end, reproducible scripts for HLJ generation, validation, tag governance, audits, and evals.

---

## 0) TL;DR Quickstart

```bash
# 0. Create & activate a Python env (3.10–3.12 recommended)
python -m venv .venv && source .venv/bin/activate       # (macOS/Linux)
# .venv\Scripts\activate                                # (Windows PowerShell)

pip install -r requirements.txt

# 1. Generate HLJs (v0) from raw requirements
python scripts/step_1/scaffold_generation.py \
  --in 02_raw_requirements \
  --out 03_refined_json

python scripts/step_1/hlj_generation.py \
  --in 02_raw_requirements \
  --out 03_refined_json \
  --model gpt41 --batch 8 --seed 42

python scripts/step_1/hlj_preview_generation.py \
  --in 03_refined_json --out 06_by_id

# 2. Validate raw HLJ & v0
python scripts/step_2/sbert_confidence_score.py --in 03_refined_json --out analytics/step_2/sbert_scores.csv
python scripts/step_2/evaluate_hlj_field.py --in 03_refined_json --csv analytics/step_2/field_eval.csv
python scripts/step_2/semantic_eval.py --in 03_refined_json --out analytics/step_2/semantic_eval.csv
python scripts/step_2/generate_model_diff_heatmaps.py --csv analytics/step_2/model_diffs.csv --out analytics/figs/model_diffs
python scripts/step_2/generate_eval_heatmaps.py --csv analytics/step_2/semantic_eval.csv --out analytics/figs/eval_heatmaps

# 3. Run v1 pipeline (curation, audits, deltas)
python scripts/step_3/list_dropped_tags.py --in 03_refined_json --out 07_v1/changes/dropped_tags.csv
python scripts/step_3/flagged_case_table.py --in 03_refined_json --out 07_v1/flags/flagged_cases.csv
python scripts/step_3/tag_alias_mapping.py --in 03_refined_json --map configs/alias_tag.json --out 07_v1/alias_applied
python scripts/step_3/validate_hljs.py --in 07_v1/alias_applied --schema configs/hlj_schema.json --out 07_v1/validated
python scripts/step_3/analyze_change_trends.py --in 07_v1 --out analytics/step_3/change_trends.csv
python scripts/step_3/generate_delta_summary.py --old 03_refined_json --new 07_v1/validated --out 07_v1/deltas
python scripts/step_3/generate_changelog.py --in 07_v1/deltas --out 07_v1/CHANGELOG.md
python scripts/step_3/generate_audits.py --in 07_v1/validated --out 07_v1/audits

# 4. Run v2 pipeline (tag governance + clustering)
python scripts/step_4/harvest_tags.py --in 07_v1/validated --out 08_v2/tags_raw.csv
python scripts/step_4/generate_canonical_labels.py --in 08_v2/tags_raw.csv --dict configs/canonical_dict.json --out 08_v2/tags_canonical.csv
python scripts/step_4/deduplicate_tags.py --in 08_v2/tags_canonical.csv --out 08_v2/tags_dedup.csv
python scripts/step_4/filter_tags_by_token_length.py --in 08_v2/tags_dedup.csv --min 2 --max 5 --out 08_v2/tags_len.csv
python scripts/step_4/filter_tags_domain.py --in 08_v2/tags_len.csv --whitelist configs/domain_whitelist.yaml --out 08_v2/tags_domain.csv
python scripts/step_4/validate_tags_nlu.py --in 08_v2/tags_domain.csv --model sbert-mini --out 08_v2/tags_validated.csv
python scripts/step_4/score_tags.py --in 08_v2/tags_validated.csv --out 08_v2/tags_scored.csv
python scripts/step_4/cluster_tags_faiss_sbert.py --in 08_v2/tags_scored.csv --out 08_v2/clusters
python scripts/step_4/detect_tag_drift.py --old analytics/baselines/tags_scored_prev.csv --new 08_v2/tags_scored.csv --out 08_v2/drift
python scripts/step_4/persist_tag_metadata.py --in 08_v2 --out 08_v2/metadata
python scripts/step_4/evaluate_tag_accuracy.py --pred 08_v2/tags_scored.csv --gold analytics/gold/tags_gold.csv --out analytics/step_4/tag_eval.csv

# 5. Multi‑model tag concordance
python scripts/step_5/multi_model_tag_concordance.py \
  --runs analytics/model_runs/*/tags_scored.csv \
  --out analytics/step_5/tag_concordance.csv
```

---

## 1) Repository Layout & Data Contracts

```
.
├── scripts/
│   ├── step_1/ (HLJ Generation)
│   ├── step_2/ (HLJ Validation & Evals)
│   ├── step_3/ (v1 Pipeline: curation, audits)
│   ├── step_4/ (v2 Pipeline: tag governance)
│   └── step_5/ (Eval: multi‑model concordance)
├── configs/
│   ├── hlj_schema.json
│   ├── alias_tag.json
│   ├── canonical_dict.json
│   └── domain_whitelist.yaml
├── 02_raw_requirements/<domain>/<prompt_id>/<req_id>-raw.txt
├── 03_refined_json/<domain>/<prompt_id>/<req_id>-refined.json      # HLJ v0
├── 06_by_id/<domain>/<prompt_id>/<req_id>/step_1.5_preview.md       # previews
├── 07_v1/...                                                        # v1 outputs
├── 08_v2/...                                                        # v2 outputs
├── analytics/
│   ├── step_2/ step_3/ step_4/ step_5/
│   ├── figs/ (heatmaps, plots)
│   └── model_runs/<model_name>/<date>/
└── 05_pipeline_runs/phase_X/<timestamp>/logs.yaml
```

### HLJ JSON (v0/v1) — minimal example

```json
{
  "id": "REQ-001",
  "domain": "FinTech",
  "subdomain": "KYC",
  "summary": "Implement KYC verification for new accounts.",
  "tags": ["KYC", "IdentityVerification", "Compliance"],
  "semantic_confidence": 0.86,
  "tag_metadata": [
    {"tag": "KYC", "source": "LLM", "conf": 0.93},
    {"tag": "IdentityVerification", "source": "RAKE", "conf": 0.80}
  ],
  "source_mapping": {
    "raw_path": "02_raw_requirements/FinTech/p001/req_001-raw.txt",
    "generator": "gpt41",
    "timestamp": "2025-09-15T00:22:00-04:00"
  },
  "version": {"v0": {"tags": ["KYC","IdentityVerification","Compliance"]}}
}
```

> **Versioning**
>
> * **v0** = initial HLJ (LLM‑parsed)
> * **v1** = curated/validated HLJ (aliases applied, schema‑clean, audits)
> * **v2** = tag governance outputs (canonicalized, deduped, scored, clustered)

---

## 2) Installation & Requirements

* Python 3.10–3.12 (works on macOS, Linux, Windows)
* `pip install -r requirements.txt`
* For FAISS on Windows, use `faiss-cpu` wheel; on macOS (ARM) use `faiss-cpu` via conda or `pip` prebuilt wheel if available.
* If you run into Windows encoding errors, set UTF‑8 mode:

  * PowerShell: `setx PYTHONUTF8 1` (restart shell)
  * Or run scripts with `PYTHONIOENCODING=utf-8`

**Key deps** (indicative): `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `faiss-cpu`, `sentence-transformers`, `torch`, `pydantic`, `typer`/`argparse`, `pyyaml`.

---

## 3) Configuration

Most scripts accept CLI flags. Shared conventions:

* `--in / --out`  input & output paths
* `--csv`          CSV input or output
* `--model`        model name or encoder (e.g., `gpt41`, `sbert-mini`)
* `--batch`        batch size for model calls
* `--seed`         RNG seed for reproducibility
* `--limit`        limit #items for dry runs
* `--overwrite`    allow replacing existing outputs

Optional central config: `configs/config.yaml`

```yaml
paths:
  raw: 02_raw_requirements
  hlj_v0: 03_refined_json
  previews: 06_by_id
  v1_root: 07_v1
  v2_root: 08_v2
  analytics: analytics
models:
  hlj_generator: gpt41
  nlu_encoder: sentence-transformers/all-MiniLM-L6-v2
thresholds:
  min_tag_conf: 0.55
  token_len: {min: 2, max: 5}
```

> Scripts may accept `--config configs/config.yaml` to override defaults.

---

## 4) Step‑by‑Step Scripts & Expected Artifacts

### **Step 1 — HLJ Generation using LLM**

**Scripts:**

* `scaffold_generation.py` — create per‑requirement placeholders, IDs, and directory scaffolding.
* `hlj_generation.py` — parse raw requirement text → HLJ (v0). Supports batching, logging, retries.
* `hlj_preview_generation.py` — produce human‑readable previews (e.g., Markdown) for quick QA.

**Inputs:** `02_raw_requirements/**.txt`
**Outputs:** `03_refined_json/**.json` (v0), `06_by_id/**/step_1.5_preview.md`

**Example:**

```bash
python scripts/step_1/hlj_generation.py \
  --in 02_raw_requirements \
  --out 03_refined_json \
  --model gpt41 --batch 8 --seed 13 --overwrite
```

---

### **Step 2 — Validate the Raw HLJ & v0**

**Scripts:**

* `sbert_confidence_score.py` — embed HLJ summaries vs. raw; compute similarity/consistency scores.
* `evaluate_hlj_field.py` — field‑level checks (missing/invalid domain, tag shapes, enums).
* `semantic_eval.py` — alignment tests between `summary`/`tags`/`subdomain` using NLU.
* `generate_model_diff_heatmaps.py` — visualize diffs across multiple model runs.
* `generate_eval_heatmaps.py` — visualize semantic/field evals as heatmaps.

**Inputs:** `03_refined_json/**.json` + optional `analytics/model_runs/*/*.csv`
**Outputs:** CSVs under `analytics/step_2/`, figures under `analytics/figs/`

**Notes:** `generate_model_diff_heatmaps.py` expects ≥2 model runs; ensure you pass multiple inputs or a combined CSV with a `model` column.

---

### **Step 3 — v1 Pipeline (Curation & Audits)**

**Scripts:**

* `list_dropped_tags.py` — detect & record tags removed during curation.
* `flagged_case_table.py` — collect edge cases (low confidence, schema violations, ambiguous tags).
* `tag_alias_mapping.py` — apply alias/canonical mapping (from `configs/alias_tag.json`).
* `validate_hljs.py` — enforce `configs/hlj_schema.json` (Pydantic/JSONSchema checks).
* `analyze_change_trends.py` — summarize change stats across batches/cohorts.
* `generate_delta_summary.py` — diff **old (v0)** vs **new (v1)** HLJs.
* `generate_changelog.py` — produce human‑readable `CHANGELOG.md`.
* `generate_audits.py` — per‑HLJ audit reports (CSV/MD) for traceability.

**Inputs:** `03_refined_json/**.json`
**Outputs:** under `07_v1/` → `alias_applied/`, `validated/`, `deltas/`, `flags/`, `CHANGELOG.md`, `audits/`

---

### **Step 4 — v2 Pipeline (Tag Governance)**

**Scripts:**

* `harvest_tags.py` — unify tag sources (LLM, RAKE, KeyBERT, etc.).
* `generate_canonical_labels.py` — canonical dictionary application.
* `deduplicate_tags.py` — semantic & lexical dedup.
* `filter_tags_by_token_length.py` — length gating.
* `filter_tags_domain.py` — domain whitelist/bayesian filters.
* `validate_tags_nlu.py` — semantic grounding vs. HLJ/summary.
* `score_tags.py` — final confidence scoring.
* `cluster_tags_faiss_sbert.py` — cluster tags (FAISS + SBERT embeddings), emit cluster IDs.
* `detect_tag_drift.py` — compare to previous baseline (distribution & semantics).
* `persist_tag_metadata.py` — write versioned metadata per HLJ/tag.
* `evaluate_tag_accuracy.py` — evaluate against gold labels (if available).

**Inputs:** `07_v1/validated/**.json` or CSV pipelines
**Outputs:** under `08_v2/` → `tags_*.csv`, `clusters/`, `drift/`, `metadata/`, plus eval CSVs

---

### **Step 5 — Eval of Raw Tags**

**Scripts:**

* `multi_model_tag_concordance.py` — agreement metrics across model runs (Jaccard, F1, overlap).

**Inputs:** `analytics/model_runs/*/tags_scored.csv`
**Outputs:** `analytics/step_5/tag_concordance.csv` + optional plots

---

## 5) Logging, Reproducibility & Runs

* All scripts should log under `05_pipeline_runs/phase_<N>/<timestamp>/logs.yaml`.
* Use `--seed` to fix RNG where sampling occurs.
* Keep per‑model outputs under `analytics/model_runs/<model>/<date>/` to enable diffs & concordance.

**Naming conventions**

* `REQ-###` ID, zero‑padded; one HLJ per requirement unless otherwise documented.
* Paths mirror: `<domain>/<prompt_id>/<req_id>` for traceability.

---

## 6) Schema & Validation Notes

* `configs/hlj_schema.json` defines strict required fields (`id`, `domain`, `summary`, `tags`, etc.), enums, and value ranges.
* v1 validation enforces: ID format, domain/subdomain enums, non‑empty `summary`, tag style (`CamelCase` or `snake_case` per policy), and integrity of `tag_metadata`.
* v2 validation ensures tags are grounded (cosine sim ≥ threshold), pass length/domain filters, and preserve traceability.

---

## 7) Troubleshooting

* **Windows Unicode errors** (`'charmap' codec can't decode byte ...`):

  * Set `PYTHONUTF8=1`, or open files with `encoding='utf-8'`.
* **FAISS install**: prefer `faiss-cpu`; if issues persist on Apple Silicon, consider Conda (`conda install -c pytorch faiss-cpu`).
* **Heatmaps show empty/flat**: verify you have ≥2 models for diffs and non‑empty eval CSVs.
* **Long runs / memory**: use `--limit`, `--batch`, and disable figures during first pass.

---

## 8) Makefile (optional)

```makefile
.PHONY: venv step1 step2 step3 step4 step5

venv:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

step1:
	python scripts/step_1/scaffold_generation.py --in 02_raw_requirements --out 03_refined_json
	python scripts/step_1/hlj_generation.py --in 02_raw_requirements --out 03_refined_json --model gpt41 --batch 8
	python scripts/step_1/hlj_preview_generation.py --in 03_refined_json --out 06_by_id

step2:
	python scripts/step_2/sbert_confidence_score.py --in 03_refined_json --out analytics/step_2/sbert_scores.csv
	python scripts/step_2/evaluate_hlj_field.py --in 03_refined_json --csv analytics/step_2/field_eval.csv
	python scripts/step_2/semantic_eval.py --in 03_refined_json --out analytics/step_2/semantic_eval.csv
	python scripts/step_2/generate_eval_heatmaps.py --csv analytics/step_2/semantic_eval.csv --out analytics/figs/eval_heatmaps

step3:
	python scripts/step_3/tag_alias_mapping.py --in 03_refined_json --map configs/alias_tag.json --out 07_v1/alias_applied
	python scripts/step_3/validate_hljs.py --in 07_v1/alias_applied --schema configs/hlj_schema.json --out 07_v1/validated
	python scripts/step_3/generate_delta_summary.py --old 03_refined_json --new 07_v1/validated --out 07_v1/deltas
	python scripts/step_3/generate_changelog.py --in 07_v1/deltas --out 07_v1/CHANGELOG.md

step4:
	python scripts/step_4/harvest_tags.py --in 07_v1/validated --out 08_v2/tags_raw.csv
	python scripts/step_4/generate_canonical_labels.py --in 08_v2/tags_raw.csv --dict configs/canonical_dict.json --out 08_v2/tags_canonical.csv
	python scripts/step_4/deduplicate_tags.py --in 08_v2/tags_canonical.csv --out 08_v2/tags_dedup.csv
	python scripts/step_4/filter_tags_by_token_length.py --in 08_v2/tags_dedup.csv --out 08_v2/tags_len.csv
	python scripts/step_4/validate_tags_nlu.py --in 08_v2/tags_len.csv --model sbert-mini --out 08_v2/tags_validated.csv
	python scripts/step_4/score_tags.py --in 08_v2/tags_validated.csv --out 08_v2/tags_scored.csv
	python scripts/step_4/cluster_tags_faiss_sbert.py --in 08_v2/tags_scored.csv --out 08_v2/clusters

step5:
	python scripts/step_5/multi_model_tag_concordance.py --runs analytics/model_runs/*/tags_scored.csv --out analytics/step_5/tag_concordance.csv
```

---

## 9) Governance & Auditability

* Every transformation should write: input path, parameters, model versions, timestamps.
* Keep `alias_tag.json`, `canonical_dict.json`, and `domain_whitelist.yaml` versioned.
* For publication prep: export summary tables from `analytics/` plus Figures from `analytics/figs/`.

---

## 10) Roadmap

* [ ] Add `Taskfile.yaml` for cross‑platform commands
* [ ] Integrate drift dashboards (Plotly) for interactive review
* [ ] CLI `--report md|html` to auto‑emit run reports
* [ ] Export cluster exemplars & centroid embeddings

---

## 11) Citation & Licensing

If you use these pipelines in a paper, please cite your preferred reference (to be added). Code is © 2025 Dvip Patel et al., license TBD.

---

**Questions / PRs welcome** — Happy tagging & auditing! 🧭
