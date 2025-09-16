# 📘 Pipeline v0 — SBERT-Based HLJ Evaluation & Confidence Scoring

This pipeline implements the **first structured evaluation flow (v0)** for HLJ (High-Level JSON) parsing and tag governance.
It focuses on **confidence scoring, semantic alignment, and visualization** using SBERT, with config-driven automation.

---

## 📂 Repo Structure (v0)

```
configs/
  pipeline_v0.yaml         # Master config (paths, models, thresholds, plots)

scripts/
  step_1/
    sbert_confidence_score.py    # Confidence scoring & fixes (low-conf HLJs)
    semantic_eval.py             # SBERT semantic similarity eval
    generate_model_diff_heatmaps.py
    generate_eval_heatmaps.py
    field_eval.py (optional)     # Field-level evaluation

  utils/
    config_loader.py             # YAML loader
    config_resolver.py           # Dot-notation config fetcher

output/
  base_output/                   # Model outputs (per folder: gpt41, meta70b, opus4)
  run/v0/plots/                  # Heatmaps & diff plots
  meta_70b.yaml                  # Meta file with gold/candidate HLJ pairs

eval/
  semantic_eval_results.csv      # SBERT similarity scores
  metrics/field_eval.csv         # Field-level CSV metrics
  metrics/field_eval.md          # Field-level Markdown report
  plots/                         # Generated heatmaps
  logging/runs/v0/sbert_fix/     # SBERT validator logs
```

---

## ⚙️ Config (v0)

All paths, models, thresholds, and plotting options are **centralized in YAML**:

```yaml
paths:
  base_output: "output"
  logs_dir: "eval/logging/runs/v0/sbert_fix"
  prompt_path: "prompts/hlj_fallback_by_sbert_prompt.md"
  meta_yaml: "output/meta_70b.yaml"

models:
  sbert: "all-MiniLM-L6-v2"
  folders: ["gpt41", "meta70b", "opus4"]
  baseline: "gpt41"

thresholds:
  confidence: 0.75
  similarity: 0.75
  clamp_min: 0.70
  clamp_max: 0.99
```

Run everything with:

```bash
python scripts/run_pipeline.py --config configs/pipeline_v0.yaml
```

---

## 🔄 Step-by-Step Flow

| Step | Script/Tool                       | Input                        | Processing                                                                                   | Output                                   |
| ---- | --------------------------------- | ---------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------- |
| 1    | `sbert_confidence_score.py`       | HLJ JSONs + SBERT embeddings | Clamps confidence, fixes low-confidence fields, validates tags. Logs rationale for each fix. | Confidence scores, fix logs, audit JSONs |
| 2    | `field_eval.py` *(optional)*      | HLJ JSONs + meta YAML        | Field-wise precision/recall/F1 vs gold HLJs.                                                 | Field metrics (CSV/MD)                   |
| 3    | `semantic_eval.py`                | Gold/candidate HLJ pairs     | SBERT cosine similarity of summaries; tag-set semantic agreement.                            | `semantic_eval_results.csv`              |
| 4    | `generate_model_diff_heatmaps.py` | Semantic eval CSV            | Visualizes model performance vs baseline; leaderboards + pairwise diffs.                     | Diff plots, leaderboards                 |
| 5    | `generate_eval_heatmaps.py`       | Field-level/semantic CSVs    | Heatmaps for per-field precision/recall/F1 or similarity.                                    | Annotated heatmaps                       |

---

## 🧠 Core Reasoning

* **SBERT Confidence Scoring**

  * Tags, difficulty, and priority are scored via SBERT.
  * Low confidence triggers fallback semantic checks against raw + summary text.
  * All fixes are logged with reasons (traceable audit trail).

* **Evaluation**

  * Field-wise (title, priority, difficulty, tags).
  * Tag-set semantic similarity (precision, recall, F1, Jaccard).
  * Gold version controlled via config (`v1`, `v2`, or `v3`).

* **Visualization**

  * Heatmaps & diff plots highlight systematic errors, model disagreements, and error clusters.

---

## 📊 Example Outputs

* `eval/semantic_eval_results.csv` — per-HLJ cosine similarity
* `eval/metrics/field_eval.csv` — per-field P/R/F1 metrics
* `eval/plots/semantic_similarity_heatmap.png` — annotated heatmap
* `eval/logging/runs/v0/sbert_fix/…` — per-HLJ audit logs

---

## 📌 Key Statement

**Pipeline v0 delivers a reproducible, semi-automated evaluation system for HLJ and tag quality.**
It blends statistical scoring, semantic validation, and visualization to justify all major fixes and scores—supporting evidence-backed refinement at the MVP stage.
