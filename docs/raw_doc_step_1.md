**Step 1: HLJ Generation using LLM**
- scaffold_generation.py
- hlj_preview_generation.py
- hlj_generation.py

**Step 2: Validate the raw hlj & v0**
- sbert_confidence_score.py
- evaluate_hlj_field.py
- semantic_eval.py
- generate_model_diff_heatmaps.py
- generate_eval_heatmaps.py

**Step 3: v1 Pipeline**
- list_dropped_tags.py
- flagged_case_table.py
- tag_alias_mapping.py
- validate_hljs.py
- analyze_change_trends.py
- generate_delta_summary.py
- generate_changelog.py
- generate_audits.py


**Step 4: v2 Pipeline**
- harvest_tags.py
- generate_canonical_labels.py
- deduplicate_tags.py
- filter_tags_by_token_length.py
- filter_tags_domain.py
- validate_tags_nlu.py
- score_tags.py
- cluster_tags_faiss_sbert.py
- detect_tag_drift.py
- persist_tag_metadata.py
- evaluate_tag_accuracy.py

**Step 5: eval of raw tags**
- multi_model_tag_concordance.py