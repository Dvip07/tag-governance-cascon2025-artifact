# Tag Governance & HLJ Pipeline

> Central README for the research repo tying together HLJ parsing, versioned tag governance, benchmarking, and the paper.

---

## Why this repo exists

We automate requirements engineering artifacts into **High‑Level JSON (HLJ)** and apply a **versioned tag‑governance pipeline** (v0 → v1 → v2). The design emphasizes **auditability**, **confidence scoring**, and **reproducibility** across multi‑model outputs (GPT‑4.1, Opus4, Meta‑70B, etc.).

---

## Repo map (what lives where)

* **`configs/`** – Versioned, YAML‑driven pipeline configs (`pipeline_v0.yaml`, `pipeline_v1.yaml`, `pipeline_v2.yaml`).
* **`scripts/`** – All runnable modules, grouped by step:

  * `step_1/` — v0 evaluation & plots (SBERT scoring, semantic eval, heatmaps, field‑level eval).
  * `step_2/` — v1 governance utilities (dropped tags export, flagged cases, alias mapping, audits, deltas/changelogs, trend tables).
  * `step_3/` — v2 governance (harvest → filter → cluster → canonicalize → dedupe → score → NLU validate → domain filter → persist metadata → drift detect → eval accuracy).
  * `utils/` — `config_resolver.py`, `pipeline_context.py`, helpers.
* **`raw_requirement/`** — Domain folders (e.g., `FinTech/`, `SaaS/`) with raw requirement markdown used for grounding.
* **`prompts/`** — Prompt templates (HLJ planning/expansion, SBERT fallback prompts).
* **`eval/`** — All evaluation artifacts.

  * `runs/<vX>/run_<timestamp>/step_*/*` — Per‑run outputs (see per‑pipeline sections below).
  * `logging/` — Audit JSON/YAML, missing‑inputs logs, etc.
* **`output/`** — Model outputs laid out as `output/<model>/req-XXX/...` for v1 utilities.
* **`docs/`** — In‑depth docs for each pipeline version (linked below).

---

## Dataset types (so you recognize paths)

* **Legacy dataset** — Single‑model, flat‑WBS available; used mainly by v1 utilities.
* **Testing dataset** — Multi‑model & multi‑version (v1=LLM, v2=SBERT, v3=Hybrid); no flat‑WBS; used by v2 pipeline.

---

## Pipelines at a glance

| Version | Focus                                              | Typical Inputs                | Key Outputs                                                                                         |
| ------- | -------------------------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------- |
| **v0**  | SBERT confidence + semantic eval + plots           | HLJs + summaries              | `eval/semantic_eval_results.csv`, heatmaps in `eval/plots/`, field‑eval CSV/MD                      |
| **v1**  | Canonicalization, alias mapping, audits, deltas    | `output/<model>/...` + audits | `eval/runs/v1/tag_alias_maps/*.json`, changelogs, delta summaries, trend tables                     |
| **v2**  | Full tag governance, multi‑stage validation, drift | `eval/runs/v2/.../step_*/*`   | `.../step_9/hlj_tag_metadata/*.json`, `.../step_10/tag_drift_report.yaml`, `.../step_11/tag_eval_*` |

### Deep dives (docs)

* **[docs/v0\_pipeline.md](docs/v0_pipeline.md)** — SBERT scoring, semantic eval, model‑diff heatmaps, field‑level metrics.
* **[docs/v1\_pipeline.md](docs/v1_pipeline.md)** — Alias maps, audits, flagged cases, deltas & changelogs, trend aggregation.
* **[docs/v2\_pipeline.md](docs/v2_pipeline.md)** — Multi‑version tag governance (harvest → NLU validate → domain filter), metadata persistence, drift detection, accuracy eval.

> Tip: the paper’s figures/tables map directly to v2 step outputs (see `eval/runs/v2/run_*/step_*`).

---

## Prerequisites

* **Python 3.11** recommended (tested on macOS/Linux).
* Install deps: `pip install -r requirements.txt`
* **Models**

  * SentenceTransformers (e.g., `all-MiniLM-L6-v2`, `hkunlp/instructor-xl`) download on first use.
  * spaCy (v1 validators): `python -m spacy download en_core_web_sm`
* (Optional) **FAISS** for clustering; CPU build is fine for most runs.

---

## The Runner (how to invoke anything)

All pipelines are driven by **`scripts/run_pipeline.py`**, which reads the config and runs the listed modules.

```
# List steps without executing
python -m scripts.run_pipeline --config configs/pipeline_v2.yaml --list

# Run entire pipeline
python -m scripts.run_pipeline --config configs/pipeline_v2.yaml

# Run a single step (suffix match on filename)
python -m scripts.run_pipeline --config configs/pipeline_v2.yaml --step detect_tag_drift.py
```

**Flags**

* `--config` — path to YAML (absolute or repo‑relative)
* `--list` — print a pretty table of runnable steps and exit
* `--step` — run only scripts whose `script` path **ends with** this string

> The runner prints ✅/❌ per step and stops on first failure, showing the exact module and arguments it invoked.

---

## Running each pipeline

### v0 — Evaluation & plots

```
python -m scripts.run_pipeline --config configs/pipeline_v0.yaml
```

**Outputs**

* `eval/semantic_eval_results.csv`
* `eval/plots/model_diff_semantic_similarity_*.png`
* `eval/output/meta_llama70b.yaml` (if configured)
* `eval/metrics/field_eval.{csv,md}`

### v1 — Governance utilities over legacy layout

```
python -m scripts.run_pipeline --config configs/pipeline_v1.yaml
```

**Outputs**

* `eval/runs/v1/tag_alias_maps/tag_alias_map_<run>.json`
* `eval/runs/v1/run_*/delta_summaries/delta_summary_*.{csv,md}`
* `eval/runs/v1/run_*/changelogs/<model>/<req>.md`
* `eval/runs/v1/run_*/dropped_tags.csv`, flagged‑cases tables, trend tables

### v2 — Research pipeline (HLJ‑centric, multi‑version)

```
python -m scripts.run_pipeline --config configs/pipeline_v2.yaml
```

**Key outputs by step** (under `eval/runs/v2/run_<id>/`)

* **step\_1–7**: harvesting, filtering, clustering, canonicalization, dedupe, scoring, NLU validation
* **step\_8**: `domain_filtered_tags_per_hlj.{json,csv}` + mismatch logs
* **step\_9**: `hlj_tag_metadata/<hlj_id>.json` (+ rejected & lookup‑gap logs)
* **step\_10**: `tag_drift_report.yaml`, `auto_pr_alias_update.yml`
* **step\_11**: `tag_eval_stats.csv`, `tag_eval_stats_by_domain.csv`, `tag_eval_report.md`

---

## Configuration anatomy (what the YAML controls)

Each `configs/pipeline_v*.yaml` includes:

* **`globals`** — run metadata, base dirs, model choices, previous run references.
* **`scripts`** — ordered list of modules to run; each has `script` path and optional `args`.
* **`stepN` blocks** — knobs per stage (thresholds, embedding models, paths).
* **`outputs`** — where artifacts should land; many steps update these paths for downstream steps.

> Pro tip: `globals.run_id` / `globals.run_dir` are set/updated by the pipeline context helpers so each run is isolated.

---

## Troubleshooting (quick fixes)

* **Drift detector wants old CTD**

  * Error mentions a missing file like `eval/runs/v1/<latest_run>/step_4/canonical_tags_with_domain.yaml`.
  * Fix by setting a valid path in `step10.prev_ctd_path` *or* ensure `globals.prev_run_dir`/`globals.prev_run_id` point to an existing v1 run.
* **`evaluate_tag_accuracy` couldn’t find `pipeline_v2.yaml`**

  * Use the config‑driven version (the script that reads `--config` rather than a hardcoded path). Ensure your config has `globals.run_dir` and `step11.*` outputs.
* **spaCy model not found**

  * `python -m spacy download en_core_web_sm`
* **SentenceTransformers model download issues**

  * First run fetches weights; ensure internet access or pre‑cache models.

---

## Reproducibility & logs

Every run writes a unique **`run_id`** folder under `eval/runs/<vX>/` with:

* Exact step outputs (`step_*`),
* Audit logs (rejects, lookup gaps, mismatches),
* Derived reports (metrics, plots),
* Drift and auto‑PR artifacts (v2).

This structure lets you diff runs, aggregate trend tables across runs (v1), and cite specific artifacts in the paper.

---

## Citing & paper tie‑in

This repo’s design mirrors the paper’s methodology and figures. Please cite the paper in any derivative work. (Links and BibTeX live in `docs/`.)

---

## FAQ (tiny)

* **Can I run only NLU validation?** Yes — use `--step validate_tags_nlu.py` with the v2 config.
* **Where do per‑HLJ facts live?** In v2: `step_9/hlj_tag_metadata/<hlj_id>.json`.
* **How do I inspect tag changes for a requirement?** v1 changelogs under `run_*/changelogs/<model>/<req>.md`.

---

## Next

* (Optional) `docs/v0_pipeline.md`, `docs/v1_pipeline.md`, and `docs/v2_pipeline.md` for line‑by‑line walkthroughs.
* Add a Dockerfile / dev‑container with the exact Python & system deps.
