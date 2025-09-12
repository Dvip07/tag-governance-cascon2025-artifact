# HLJ Overlap/Agreement Analysis

## Top HLJs by Disagreement

| req_id | hlj_id | present_models | agreement_score | entropy | opus4_prec | opus4_rec | opus4_f1 | meta70b_prec | meta70b_rec | meta70b_f1 | stable_tags | unique_gpt41 | unique_opus4 | unique_meta70b |
|--------|--------|----------------|----------------|---------|------------|-----------|----------|--------------|-------------|------------|-------------|--------------|--------------|----------------|
| req-001 | req-001-hlj-chunk_1-item_10-v1.0 | gpt41|opus4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |  |  |  | [inferred] compliance|documentation|integration|support | api|availability|resilience |  |
| req-001 | req-001-hlj-chunk_1-item_3-v1.0 | gpt41|opus4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |  |  |  | compliance|openapi|spec | api|filtering|query |  |
| req-001 | req-001-hlj-chunk_1-item_4-v1.0 | gpt41|opus4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |  |  |  | data|deduplication|schema | api|openapi|standards |  |
| req-001 | req-001-hlj-chunk_1-item_6-v1.0 | gpt41|opus4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |  |  |  | authentication|oauth|security | data|normalization|timestamp |  |
| req-001 | req-001-hlj-chunk_1-item_7-v1.0 | gpt41|opus4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |  |  |  | audit|compliance|logging | authentication|oauth|security |  |
| req-001 | req-001-hlj-chunk_1-item_9-v1.0 | gpt41|opus4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |  |  |  | [inferred] compliance|latency|performance|scalability | data|edge-cases|normalization |  |
| req-001 | req-001-hlj-chunk_2-item_1-v1.0 | opus4|meta70b | 0.00 | 1.00 |  |  |  |  |  |  |  |  | api|optimization|performance | [inferred] compliance|oauth|security |
| req-001 | req-001-hlj-chunk_2-item_2-v1.0 | opus4|meta70b | 0.00 | 1.00 |  |  |  |  |  |  |  |  | api|documentation|support | [inferred] security|audit|logging |
| req-002 | req-002-hlj-chunk_1-item_1-v1.0 | gpt41|opus4|meta70b | 0.00 | 0.92 | 0.00 | 0.00 | 0.00 | 0.33 | 0.50 | 0.40 |  | usability | ux|workflow | minor |
| req-002 | req-002-hlj-chunk_1-item_10-v1.0 | gpt41|opus4 | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |  |  |  |  | maintainability|usability | compliance|encryption|security |  |

## Aggregate Stats
- **total_req_ids**: 30
- **total_hlj_items**: 514
- **num_all_models_agree**: 190
- **num_full_disagreement**: 280
- **avg_agreement**: 0.39191217342968315
- **avg_entropy**: 0.5831224124401073
- **opus4_macro_precision**: 0.1044349070100142
- **opus4_macro_recall**: 0.1294706723891272
- **opus4_macro_f1**: 0.11340690782750856
- **meta70b_macro_precision**: 0.0893617021276596
- **meta70b_macro_recall**: 0.09999999999999999
- **meta70b_macro_f1**: 0.09333333333333335
