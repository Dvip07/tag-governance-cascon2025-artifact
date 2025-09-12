# 🦾 Plantric HLJ Validation Pipeline – Scripts & Outputs

This repository contains a modular pipeline for validating and auditing High-Level JSON (HLJ) outputs from multiple LLMs (e.g., GPT-4.1, Meta-70B, Opus-4).  
Each script is responsible for one key step in the pipeline. Outputs are versioned and auditable for maximum research traceability.

---

## 📚 **Script Index**

| Script Name                 | Purpose                                                  | Input(s)                       | Output(s)                        | Outcome / Description                  |
|-----------------------------|---------------------------------------------------------|--------------------------------|-----------------------------------|----------------------------------------|
| `validate_hljs.py`          | Runs NLU/SBERT tag validation on HLJs                   | HLJ v1s, raw reqs              | HLJ v2s (validated), tag changes  | Produces versioned HLJ JSON with tags validated against requirement context; never mutates original |
| `generate_audits.py`        | Generates YAML audit logs for HLJ changes               | HLJ v1/v2                      | Audit YAML per req/HLJ            | Full audit trail of all tag/field changes, with reason, similarity, timestamp                     |
| `generate_changelog.py`     | Creates Markdown changelog tables per HLJ/requirement   | Audit YAML/JSON                | Markdown changelog per req/HLJ    | Table view of all tag changes (added, dropped, kept) with validation metadata                    |
| `generate_delta_summary.py` | Aggregates model/requirement-level delta summaries      | All audit logs/CSV             | Markdown/CSV delta summary        | For each model: HLJs processed, changed, % change, top tags dropped/added, top reasons           |
| `analyze_change_trends.py`  | Tracks pipeline change trends across multiple runs      | Delta summary logs (CSV)       | Markdown/CSV trend tables         | Shows trend lines over time (% changed, avg. similarity, etc.)                                   |
| `flagged_case_table.py`     | Lists most-changed HLJs for qualitative review          | Audit logs/changes CSV         | Markdown/CSV flagged cases        | Appendix-ready table of HLJs with most tag changes, for paper or debugging                       |
| `pipeline_run_all.py`       | Runs all pipeline steps sequentially                    | -                              | -                                 | Optional. Automates full pipeline from validation to trend summary                               |

---

## 📁 **Typical File Structure**

```plaintext
output/
  gpt41/req-001/hlj/merged/all_chunks_full.json
  ...
sbert_fix/
  gpt41/req-001/all_chunks_full_validated.json
  gpt41/req-001/audit.yaml
  gpt41/req-001/changelog.md
  delta_summary.csv
  delta_summary.md
  trends/change_trend_table.csv
  flagged_cases.csv
  ...
raw_requirement/
  FinTech/req-001.md
  SaaS/req-002.md



# Step 1: Validate HLJs
python scripts/step_1/validate_hljs.py

# Step 2: Generate audits from v1/v2 HLJs
python scripts/step_1/generate_audits.py

# Step 3: Generate Markdown changelogs
python scripts/step_1/generate_changelog.py

# Step 4: Aggregate delta summaries (per model)
python scripts/step_1/generate_delta_summary.py

# Step 5: Analyze trends across runs
python scripts/step_1/analyze_change_trends.py

# Step 6: Generate table of most-flagged HLJs
python scripts/step_1/flagged_case_table.py

# (Optional) Run all pipeline steps in order
python scripts/step_1/pipeline_run_all.py
