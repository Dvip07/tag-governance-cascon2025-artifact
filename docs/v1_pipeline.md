# Pipeline v1: Tag Governance & Change Tracking

| Step | Script/Tool                 | Input Data                     | Processing & Reasoning                                                                                              | Output                          |
| ---- | --------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| 1    | `list_dropped_tags.py`      | Tag evaluation logs, HLJ data  | Identifies tags removed in v1 vs v0; reasons (e.g., low confidence, semantic drift) are logged for traceability.    | Dropped tags report             |
| 2    | `flagged_case_table.py`     | HLJ, tag metadata              | Flags edge/tag cases (ambiguous, risky, over-specific); tabulates for audit and feedback loops.                     | Flagged tag case table          |
| 3    | `tag_alias_mapping.py`      | Tags, Canonical Tag Dictionary | Maps aliases/synonyms to canonical tags using a controlled vocabulary; reasoning: reduces tag bloat, enforces norms | Canonicalized tags, alias logs  |
| 4    | `validate_hljs.py`          | HLJ JSONs, evaluation scripts  | Runs structural and semantic validation on HLJs; flags errors, mismatches, and logs reasons for failures.           | Validation report, error logs   |
| 5    | `analyze_change_trends.py`  | v0/v1 tag/field diffs          | Analyzes trends in tag changes (what’s commonly dropped, why, and impact); supports reasoning and continuous QA.    | Change trend summary, plots     |
| 6    | `generate_delta_summary.py` | Diffs, change logs             | Summarizes key differences between versions, highlighting meaningful deltas and stability metrics.                  | Delta summary table, highlights |
| 7    | `generate_changelog.py`     | Change logs, deltas            | Produces readable changelogs for audit and future reference (who/what/why changed per field/tag).                   | Changelog                       |
| 8    | `generate_audits.py`        | Full eval logs                 | Generates final audit trail of all decisions, flagged cases, corrections, and mapping steps.                        | Audit report, traceable logs    |

---

## Reasoning Layer

* **Why:** v1 introduces robust tag governance, using alias mapping, canonicalization, and explicit flagging of edge/tag-risk cases.
* **How:** Every change (drop, flag, alias, validation) is logged with reason codes, enabling complete traceability and justification.
* **What’s new:** This layer turns the process from *“fix and score”* (v0) to *“govern, explain, and track”* (v1), making the whole system more transparent and auditable.

---

## Key Value Statement

> Pipeline v1 establishes a formal, auditable system for tag and HLJ validation. By tracking changes, mapping aliases, and flagging edge cases, it enables higher-quality, reliable metadata—setting a strong foundation for scaling and external review.
