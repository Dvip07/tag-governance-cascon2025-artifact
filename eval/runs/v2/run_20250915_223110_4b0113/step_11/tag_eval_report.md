# Tag Accuracy Evaluation Report (GOLD: v3)

| Model | #HLJs | Prec@v2 | Recall@v2 | F1@v2 | Jac@v2 | Prec@v3 | Recall@v3 | F1@v3 | Jac@v3 |
|-------|-------|---------|-----------|-------|--------|---------|-----------|-------|--------|
| gpt41 | 346 | 0.321 | 0.221 | 0.250 | 0.183 | 0.453 | 0.209 | 0.266 | 0.203 |
| opus4 | 98 | 0.000 | 0.000 | 0.000 | 0.000 | 0.010 | 0.010 | 0.010 | 0.010 |
| meta70b | 60 | 0.000 | 0.000 | 0.000 | 0.000 | 0.017 | 0.017 | 0.017 | 0.017 |

## Per-domain Analysis
| Domain | #HLJs | Prec@v2 | Recall@v2 | F1@v2 | Jac@v2 | Prec@v3 | Recall@v3 | F1@v3 | Jac@v3 |
|--------|-------|---------|-----------|-------|--------|---------|-----------|-------|--------|
| SaaS | 170 | 0.228 | 0.156 | 0.179 | 0.132 | 0.336 | 0.147 | 0.190 | 0.142 |
| FinTech | 334 | 0.216 | 0.150 | 0.168 | 0.123 | 0.304 | 0.147 | 0.185 | 0.144 |

## Error Cases (Low F1/Jaccard HLJs)
| HLJ | Model | Prec@v2 | Rec@v2 | F1@v2 | Jac@v2 | Prec@v3 | Rec@v3 | F1@v3 | Jac@v3 | v1 | v2 | v3 |
|-----|-------|---------|--------|-------|--------|---------|--------|-------|--------|----|----|----|
| REQ-025-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] alerting|external|resilience | external|resilience | alert|compliance|external|performance|privacy|resilience|sla |
| REQ-007-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] compliance|encryption|security | encryption|security | compliance|dashboard|encryption|reporting|security |
| REQ-009-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 1.00 | 0.25 | 0.40 | 0.25 | 1.00 | 0.25 | 0.40 | 0.25 | audit|compliance | audit|compliance | api|audit|compliance|fx-rates|integration|notification|real-time|sms |
| REQ-008-HLJ-Chunk_3-Item_5-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] lending|audit|compliance|dashboard | audit|compliance|dashboard |  |
| REQ-024-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | documentation|training | documentation|training | automation|documentation|ml|segmentation|training |
| REQ-014-HLJ-Chunk_2-Item_6-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | display|estimation|gas-fee | display|estimation|gas-fee |  |
| REQ-006-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] audit|compliance|security | compliance|security | api|audit|authentication|compliance|sandbox environments|security|testing |
| REQ-008-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | [INFERRED] resilience|edge-case|error-handling |  |  |
| REQ-006-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.50 | 0.17 | 0.25 | 0.14 | 1.00 | 0.17 | 0.29 | 0.17 | abuse-detection|security | security | api|billing|compliance|rate-limiting|reporting|security |
| REQ-001-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 0.00 | 0.00 | 0.00 | 0.00 | availability|error|logging | error | compliance|logging|security |
| REQ-024-HLJ-Chunk_3-Item_2-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | backend|deduplication|reliability | deduplication|reliability |  |
| REQ-014-HLJ-Chunk_2-Item_12-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | audit|fee query|logging | audit|logs |  |
| REQ-025-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] performance|alerting|sla | alert|sla | alert|analytics|dashboard|filter|performance|sla |
| REQ-013-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 1.00 | 0.80 | 0.67 | 0.50 | 0.50 | 0.50 | 0.33 | [INFERRED] traceability|exception|logging | exception|logs | exception|logging |
| REQ-023-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] progressive-rollout|deployment|feature-flags | deployment | deployment|feature-flags|geo-ip|geo-targeting|progressive-rollout|rollback |
| REQ-006-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.50 | 0.20 | 0.29 | 0.17 | 1.00 | 0.20 | 0.33 | 0.20 | alerting|monitoring | monitoring | alert|api|dashboard|monitoring|rate-limiting |
| REQ-030-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.50 | 0.67 | 0.57 | 0.40 | 0.67 | 0.67 | 0.67 | 0.50 | [INFERRED] artifact-retention|logs|screenshots|video | logs|screenshots|video | logging|screenshots|video |
| REQ-008-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] anomaly-detection|detection|fraud | detection|fraud | compliance|consent|detection|fraud|privacy|ux |
| REQ-008-HLJ-Chunk_2-Item_9-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] tracking|audit|logging | audit|logs |  |
| REQ-014-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 1.00 | 0.25 | 0.40 | 0.25 | 1.00 | 0.25 | 0.40 | 0.25 | notification | notification | estimation|gas-fee|notification|transaction |
| REQ-022-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] alerting|anomaly|notification | anomaly | compliance|notification|privacy|security |
| REQ-006-HLJ-Chunk_2-Item_9-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] latency|performance | performance | infrastructure|latency|performance|upgrade |
| REQ-007-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] onboarding|aml|performance | aml|performance | aml|api|compliance|onboarding|performance|regulation|risk |
| REQ-009-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.67 | 0.80 | 0.67 | [INFERRED] risk management|fx|locking | fx|lock | fx|fx-rates|lock |
| REQ-009-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] regulatory reporting|compliance|documentation | compliance|documentation | audit|beta|compliance|documentation |
| REQ-012-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.67 | 0.67 | 0.50 | 0.50 | 0.33 | 0.40 | 0.25 | [INFERRED] compliance|audit|logging | audit|logs | audit|compliance|logging |
| REQ-006-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] fallback|availability|resilience |  | api|audit|availability|fallback|multi-factor approval|override|security |
| REQ-008-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] compliance|dashboard|monitoring | monitoring | compliance|dashboard|eligibility|income|monitoring|rules |
| REQ-009-HLJ-Chunk_3-Item_6-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | dashboard|monitoring|reporting | dashboard|monitoring|reporting |  |
| REQ-023-HLJ-Chunk_2-Item_11-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] version control|change log|documentation | change log|documentation |  |
| REQ-024-HLJ-Chunk_3-Item_4-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | api|documentation|integration | api|documentation|integration |  |
| REQ-024-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | compliance|logging | compliance | compliance|integration|messaging |
| REQ-023-HLJ-Chunk_2-Item_7-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | audit|backend|compliance | audit|compliance |  |
| REQ-009-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] compliance|abuse prevention|fx | fx | beta|compliance|feature-toggle|fx|regulation |
| REQ-007-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] reporting|compliance|dashboard | compliance|dashboard | audit|compliance|dashboard|legal|reporting|security|support |
| REQ-007-HLJ-Chunk_2-Item_7-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|qa|testing | compliance|testing |  |
| REQ-008-HLJ-Chunk_3-Item_3-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | display|earnings|ux | display|earnings |  |
| REQ-023-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] data-protection|compliance|privacy | compliance|privacy | compliance|feature-flags|privacy|rollback |
| REQ-009-HLJ-Chunk_2-Item_7-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] reliability|compliance|sla | compliance|sla | compliance|fx-rates|payments|sla|validation |
| REQ-022-HLJ-Chunk_2-Item_2-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | admin|compliance|documentation | admin|compliance|documentation |  |
| REQ-012-HLJ-Chunk_2-Item_7-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | fallback|gst | fallback|gst |  |
| REQ-024-HLJ-Chunk_2-Item_5-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | analytics|metrics|tracking | analytics|metrics|tracking |  |
| REQ-024-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] analytics|a/b testing|segmentation | a/b testing|segmentation | analytics|backend|messaging|optimization|segmentation |
| REQ-022-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] compliance|audit|logging | audit|logs | access_logs|audit|compliance|database|logging |
| REQ-014-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | coverage |  |  |
| REQ-001-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.33 | 0.50 | 0.33 | compliance|openapi|spec | compliance|openapi | api|compliance|filter|openapi|query|spec |
| REQ-007-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] resilience|aml|availability | aml | aml|availability|compliance|fallback|regulation|reporting |
| REQ-009-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] integrations|api|fx | api|fx | api|fx|fx-rates|integration|timer|ui |
| REQ-015-HLJ-Chunk_1-Item_6-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] analytics|logging|monitoring | logs|monitoring |  |
| REQ-023-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] location-resolution|geo-ip|real-time | geo-ip | feature-flags|geo-ip|integration|location-resolution|real-time|rollback |
| REQ-025-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.25 | 0.36 | 0.22 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] analytics|metrics|visualization | metrics|visualization | analytics|dashboard|engineering|metrics|performance|privacy|telemetry|visualization |
| REQ-006-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] customization|configuration|rate-limiting |  | api|configuration|rate-limiting|tenant management |
| REQ-008-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] data-verification|gig-economy|integration | integration | api|api integration|data-verification|gig workers|gig-economy|integration|uber |
| REQ-024-HLJ-Chunk_2-Item_8-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|messaging|ux | compliance|messaging |  |
| REQ-024-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] compliance|deduplication|reliability | deduplication|reliability | analytics|compliance|deduplication|reliability|testing |
| REQ-014-HLJ-Chunk_2-Item_7-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | adjust|customization|gas-fee | adjust|gas-fee |  |
| REQ-008-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] regulation|compliance|privacy | compliance|privacy | api|audit|compliance|privacy|regulation |
| REQ-025-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] performance|prompt|usability | prompt|usability | automation|ci/cd|performance|prompt|usability |
| REQ-024-HLJ-Chunk_2-Item_10-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | audit|compliance|logging | audit|compliance |  |
| REQ-008-HLJ-Chunk_3-Item_4-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | dashboard|monitoring|operations | dashboard|monitoring|operations |  |
| REQ-001-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.50 | 0.50 | 0.50 | 0.33 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|latency|performance|scalability | latency|performance | compliance|data|latency|performance |
| REQ-024-HLJ-Chunk_3-Item_3-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | documentation|training|ux | documentation|training |  |
| REQ-013-HLJ-Chunk_2-Item_5-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|dataretention | compliance |  |
| REQ-006-HLJ-Chunk_2-Item_5-v1.0 | gpt41 | 0.33 | 0.11 | 0.17 | 0.09 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] safety|availability|rollout | rollout | access-control|api|audit|availability|documentation|mfa|rate-limiting|rollback|security |
| REQ-014-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 0.50 | 0.33 | audit|logging | audit|logs | audit|logging |
| REQ-008-HLJ-Chunk_2-Item_5-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | currency|edge-case|income | currency|income |  |
| REQ-009-HLJ-Chunk_3-Item_1-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|fx-rates|risk | compliance|risk |  |
| REQ-006-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 0.50 | 0.20 | 0.29 | 0.17 | compliance|logging | compliance|logs | api|compliance|logging|monitoring|rate-limiting |
| REQ-008-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|aml|kyc | aml|kyc | aml|compliance|currency|kyc |
| REQ-013-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 1.00 | 0.50 | 0.33 | 0.50 | 1.00 | 0.67 | 0.50 | [INFERRED] recovery|partial|retry | partial|retry | retry |
| REQ-025-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] regression|alerting|diagnostics | alert|diagnostics | alert|analytics|dashboard|debugging|diagnostics|regression|visualization |
| REQ-015-HLJ-Chunk_1-Item_1-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] real-time|insurance|webhook | insurance|webhook |  |
| REQ-023-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] portal|admin|feature-flags | admin | admin|edge_cases|feature-flags|geo-ip|portal |
| REQ-007-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | [INFERRED] transparency|usability|ux |  |  |
| REQ-007-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 1.00 | 0.25 | 0.40 | 0.25 | 1.00 | 0.25 | 0.40 | 0.25 | aml|integration | aml|integration | aml|audit|backend|integration|performance|privacy|security|sla |
| REQ-009-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] countdown|fx|ui | fx|ui | countdown|fx|fx-rates|payments|rate-lock|ui |
| REQ-022-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] integrity|audit|historical | audit | audit|export|export_controls|filter|rate-limiting|security |
| REQ-008-HLJ-Chunk_2-Item_8-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] ml|fraud|income|security | fraud|income|security |  |
| REQ-014-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | advanced|usability | advanced|usability | advanced|dynamic|estimation|gas-fee|usability |
| REQ-006-HLJ-Chunk_2-Item_8-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] legacy|compatibility|migration | compatibility|migration | compatibility|documentation|legacy|migration|self-service |
| REQ-022-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] data-protection|privacy|regulation | privacy | data-protection|monitoring|privacy|regulation |
| REQ-024-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] notification|multi-language|template | multi-language|template | backend|messaging|multi-language|notification|personalization|template |
| REQ-023-HLJ-Chunk_2-Item_10-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] training|documentation|onboarding | documentation|onboarding |  |
| REQ-025-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] compliance|privacy|transparency | privacy|transparency | compliance|monitoring|performance|privacy|resilience|transparency |
| REQ-009-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] cancellation|refund|scheduled payments | refund|scheduled payments | cancellation|compliance|payments|refund|scheduled payments |
| REQ-023-HLJ-Chunk_2-Item_6-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | developer|documentation|training | developer|documentation |  |
| REQ-007-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.25 | 0.36 | 0.22 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] immutability|audit|security | audit|security | audit|compliance|immutable|manual|privacy|regulation|security|workflow |
| REQ-030-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|artifacts|security | artifacts|security | artifacts|compliance|debugging|security |
| REQ-006-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.50 | 0.20 | 0.29 | 0.17 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] authentication|security | security | api|availability|fallback|security|tenant segment |
| REQ-009-HLJ-Chunk_3-Item_7-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | automation|error-handling|payments | payments |  |
| REQ-008-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 0.50 | 0.17 | 0.25 | 0.14 | [INFERRED] compliance|audit|logging | audit|logs | admin|audit|compliance|logging|portal|rules |
| REQ-006-HLJ-Chunk_2-Item_10-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] communication|compliance|legal | compliance|legal | communication|compatibility|compliance|legacy|legal|migration |
| REQ-024-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] compliance|help-center|usability | usability | analytics|compliance|monitoring|ui|usability |
| REQ-012-HLJ-Chunk_2-Item_6-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] compliance|exemptions|gst | exemption|gst |  |
| REQ-007-HLJ-Chunk_2-Item_6-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] gdpr|compliance|data|privacy | compliance|data|privacy |  |
| REQ-009-HLJ-Chunk_2-Item_6-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] integrations|api|fx | api|fx | api|availability|fx|fx-rates |
| REQ-008-HLJ-Chunk_3-Item_2-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] api|connection|feedback|ux | connection|feedback |  |
| REQ-023-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] user-notification|communication|user-option |  | alert|monitoring|notification |
| REQ-001-HLJ-Chunk_2-Item_1-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | api|optimization|performance | api|optimization|performance |  |
| REQ-001-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.75 | 0.86 | 0.75 | api|filtering|pagination | api|filter|pagination | api|filter|pagination|performance |
| REQ-007-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] compliance|aml|notification | aml|notification | aml|compliance|notification|state|ui|workflow |
| REQ-009-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] fallback|fx|notifications | fx|notification | compliance|fx|fx-rates|lock|notification |
| REQ-024-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.25 | 0.40 | 0.25 | analytics|dashboard | analytics | analytics|dashboard|messaging|ml |
| REQ-014-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | ui|usability | ui|usability | estimation|gas-fee|real-time|ui|usability |
| REQ-030-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.67 | 0.80 | 0.67 | blocking|ci-cd|critical-path | blocking|ci/cd | blocking|ci/cd|deployment |
| REQ-025-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] analytics|compliance|privacy | compliance|privacy | analytics|compliance|performance|privacy |
| REQ-024-HLJ-Chunk_2-Item_9-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|legal|tracking | compliance|tracking |  |
| REQ-023-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] fallback|fault-tolerance|geo-ip | geo-ip | admin portal|fallback|feature-flags|geo-ip |
| REQ-015-HLJ-Chunk_1-Item_7-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] onboarding|documentation|webhook | documentation|webhook |  |
| REQ-009-HLJ-Chunk_2-Item_10-v1.0 | gpt41 | 0.33 | 0.50 | 0.40 | 0.25 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] implementation|delivery|modularity | delivery | delivery|implementation |
| REQ-025-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] analytics|reporting|segmentation | reporting|segmentation | analytics|instrumentation|metrics|performance|reporting|segmentation |
| REQ-009-HLJ-Chunk_3-Item_2-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|payments|regulation | compliance|payments |  |
| REQ-022-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] enablement|compliance|docs | compliance|docs | audit|compliance|docs|documentation|roles|security |
| REQ-008-HLJ-Chunk_2-Item_6-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | aml|compliance|kyc | aml|compliance|kyc |  |
| REQ-006-HLJ-Chunk_2-Item_6-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] developer-experience|testing|usability | testing | deployment|developer-experience|testing |
| REQ-023-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|audit|changelog | audit|changelog | audit|changelog|compliance|geo-ip |
| REQ-013-HLJ-Chunk_2-Item_6-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | documentation|training | documentation|training |  |
| REQ-025-HLJ-Chunk_2-Item_4-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|privacy|ux | compliance|privacy|ux |  |
| REQ-001-HLJ-Chunk_2-Item_4-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | caching|data|performance | caching|data|performance |  |
| REQ-013-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.67 | 0.67 | 0.50 | 0.50 | 0.33 | 0.40 | 0.25 | [INFERRED] compliance|audit|logging | audit|logs | audit|compliance|logging |
| REQ-009-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | compliance|dashboard | compliance | compliance|dashboard|fx|fx-rates|payments |
| REQ-007-HLJ-Chunk_2-Item_3-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | communication|ui|ux | communication|ui |  |
| REQ-024-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] compliance|timezone|usability | timezone | messaging|personalization|timezone|usability |
| REQ-012-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.50 | 0.67 | 0.57 | 0.40 | 1.00 | 0.67 | 0.80 | 0.67 | [INFERRED] compliance|gst|portal|usability | gst|portal | compliance|gst|portal |
| REQ-006-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] self-service|monitoring|usability | monitoring | alert|api|monitoring|rate-limiting|self-service|usage metrics |
| REQ-008-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] transparency|consent|user-experience | consent|user experience | api|consent|documentation|integration|user_experience |
| REQ-022-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] data-protection|masking|privacy | masking|privacy | csv|data-protection|export|privacy|security |
| REQ-024-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.22 | 0.33 | 0.20 | 1.00 | 0.11 | 0.20 | 0.11 | [INFERRED] notification|testing|usability | testing | backend|delivery|i18n|messaging|notification|scheduling|testing|timing|usability |
| REQ-001-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.33 | 0.50 | 0.33 | audit|compliance|logging | audit|compliance | audit|authentication|compliance|logging|oauth|security |
| REQ-025-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] regression|automation|remediation | remediation | analytics|diagnostics|external services|fallback|performance|regression|remediation |
| REQ-013-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] consistency|atomicity|rollback | atomicity|rollback | atomicity|batch|consistency|rollback |
| REQ-014-HLJ-Chunk_2-Item_10-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | confirmation|gas-fee|resolution | confirmation|gas-fee|resolution |  |
| REQ-015-HLJ-Chunk_1-Item_2-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] flexibility|customfield|webhook | webhook |  |
| REQ-008-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] validation|edge-case|eligibility | eligibility | aggregation|data|earnings|eligibility|income|user_experience |
| REQ-014-HLJ-Chunk_2-Item_9-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | gas-fee|inaccuracy|retry | gas-fee|inaccuracy|retry |  |
| REQ-006-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] API|feedback|usability | feedback | api|feedback|instant feedback|rate-limiting |
| REQ-008-HLJ-Chunk_3-Item_1-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | ui|ux|workflow | workflow |  |
| REQ-015-HLJ-Chunk_1-Item_9-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | [INFERRED] architecture|performance|scalability |  |  |
| REQ-009-HLJ-Chunk_2-Item_5-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] retry|error handling|scheduled payments | scheduled payments | fx-rates|retry|scheduled payments |
| REQ-007-HLJ-Chunk_2-Item_5-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|encryption|security | compliance|encryption|security |  |
| REQ-001-HLJ-Chunk_2-Item_2-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | api|documentation|support | api|documentation|support |  |
| REQ-015-HLJ-Chunk_1-Item_10-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] risk-management|compliance|regulation | compliance |  |
| REQ-024-HLJ-Chunk_2-Item_7-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | automation|failover|reliability |  |  |
| REQ-024-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | compliance|opt-out | compliance|opt-out | api|compliance|integration|messaging|opt-out |
| REQ-009-HLJ-Chunk_3-Item_4-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | audit|compliance|logging | audit|compliance|logs |  |
| REQ-025-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | analytics|self-service | analytics | analytics|dashboard|performance|self-service|ux |
| REQ-023-HLJ-Chunk_2-Item_5-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | documentation|product|training | documentation|product |  |
| REQ-007-HLJ-Chunk_2-Item_8-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | alerting|compliance|monitoring | compliance|monitoring |  |
| REQ-009-HLJ-Chunk_2-Item_8-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] rollout|beta|usability | beta | beta|fx-rates|rollback|ui|workflow |
| REQ-015-HLJ-Chunk_1-Item_4-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] authentication|security|webhook | security|webhook |  |
| REQ-023-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] kpi-tracking|dashboard|real-time-analytics | dashboard|real-time-analytics | analytics|dashboard|kpi-tracking|real-time-analytics |
| REQ-013-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] flexibility|batch|scheduling | batch | batch|failurehandling|rollback|scheduling |
| REQ-025-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] performance|instrumentation|timing | instrumentation|timing | analytics|instrumentation|optimization|performance|timing |
| REQ-008-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.22 | 0.33 | 0.20 | 1.00 | 0.22 | 0.36 | 0.22 | [INFERRED] rules-engine|eligibility|risk | eligibility|risk | aml|api|compliance|eligibility|integration|kyc|risk|rules-engine|upwork |
| REQ-030-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | parallel|staging|ui-testing | parallel|staging | browser_coverage|parallel|staging|ui_testing |
| REQ-006-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] real-time|configuration|usability |  | api|configuration|rate-limiting|real-time|real-time updates |
| REQ-012-HLJ-Chunk_2-Item_8-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | gst|reporting | gst|reporting |  |
| REQ-024-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] notification|automation|multi-channel | multi-channel | automation|channel|messaging|multi-channel|notification|personalization|preferences |
| REQ-022-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 0.50 | 0.25 | 0.33 | 0.20 | [INFERRED] security|export|roles | export|roles | compliance|export|export_controls|security |
| REQ-014-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] coverage|integration|oracle | integration|oracle | blockchain|estimation|gas-fee|integration|oracle |
| REQ-001-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 0.50 | 0.25 | 0.33 | 0.20 | api|rest|spec | api|rest | api|compliance|endpoint|openbanking |
| REQ-009-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] traceability|audit|fx | audit|fx | audit|fx|payments|processing|scheduling |
| REQ-023-HLJ-Chunk_2-Item_8-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | authentication|backend|infrastructure | authentication |  |
| REQ-007-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.25 | 0.36 | 0.22 | 0.50 | 0.12 | 0.20 | 0.11 | [INFERRED] traceability|audit|logging | audit|logs | audit|compliance|logging|notification|screening|testing|traceability|workflow |
| REQ-023-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] enablement|documentation|training | documentation|training | compliance|documentation|enablement|gdpr|training |
| REQ-025-HLJ-Chunk_2-Item_5-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | analytics|dashboard|self-service | analytics|dashboard |  |
| REQ-013-HLJ-Chunk_2-Item_7-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | qualityassurance|testing | testing |  |
| REQ-024-HLJ-Chunk_3-Item_1-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] automation|scheduling|timezone|ux | scheduling|timezone |  |
| REQ-008-HLJ-Chunk_2-Item_7-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|identity|verification | compliance|identity|verification |  |
| REQ-009-HLJ-Chunk_3-Item_3-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|documentation|payments | compliance|documentation|payments |  |
| REQ-022-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] security|abuse|rate-limit | abuse | abuse|compliance|rate-limiting|security |
| REQ-006-HLJ-Chunk_2-Item_7-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] education|documentation | documentation | client-support|documentation|sandbox|testing |
| REQ-006-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | compliance|reporting | compliance|reporting | api|compliance|metrics|rate-limiting|reporting|self-service |
| REQ-008-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] user-trust|dispute|user-interface | dispute | api|dispute|security |
| REQ-001-HLJ-Chunk_2-Item_5-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] security|compliance|deployment|review | compliance|deployment|review |  |
| REQ-008-HLJ-Chunk_3-Item_6-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | alternative|edge-case|workflow | alternative|workflow |  |
| REQ-009-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] messaging|notifications|usability | notification|usability | fx-rates|notification|rate-lock|reporting|usability |
| REQ-007-HLJ-Chunk_2-Item_2-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | analytics|compliance|reporting | compliance|reporting |  |
| REQ-009-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] usability|scheduled payments|ui | scheduled payments|ui | payments|scheduled payments|scheduling|ui |
| REQ-007-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] integration|aml|screening | aml|screening | aml|compliance|integration|kyc|regulation|screening |
| REQ-022-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] usability|export|filter | export|filter | compliance|export|export_controls|filter|security |
| REQ-024-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] personalization|scheduling|timezone | scheduling|timezone | messaging|personalization|preview|scheduling|timezone |
| REQ-012-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] automation|gst|rates | gst|rates | gst|provincial tax|rates|tax |
| REQ-008-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] configurability|admin|rule-management | admin | admin|api|data connection|fiverr|integration|rule-management|user_experience |
| REQ-014-HLJ-Chunk_2-Item_8-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | congestion|fee spike|gas-fee | congestion|fee spike|gas-fee |  |
| REQ-006-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | enforcement|rate-limiting | enforcement | api|api-gateway|enforcement|infrastructure|rate-limiting |
| REQ-013-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] reliability|failure|rollback | failure|rollback | failure|reliability|reporting|rollback |
| REQ-025-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] performance|cicd|regression | regression | alert|analytics|ci/cd|optimization|performance|regression |
| REQ-014-HLJ-Chunk_2-Item_11-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|security|user data | compliance|security |  |
| REQ-015-HLJ-Chunk_1-Item_3-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] fault-tolerance|reliability|webhook | reliability|webhook |  |
| REQ-023-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] geo-segmentation|feature-flags|scalable | scalable | feature-flags|geo-segmentation|scalable|segmentation |
| REQ-022-HLJ-Chunk_2-Item_1-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | performance|rate-limiting|security | security |  |
| REQ-012-HLJ-Chunk_2-Item_10-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | privacy|security | privacy|security |  |
| REQ-024-HLJ-Chunk_2-Item_6-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | alerts|monitoring|reliability | alert|monitoring |  |
| REQ-015-HLJ-Chunk_1-Item_8-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] knowledge-base|support|training | support|training |  |
| REQ-009-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] outage-handling|availability|fx | fx | availability|fx|fx-rates|rollback |
| REQ-007-HLJ-Chunk_2-Item_4-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | ui|ux|workflow | ui|workflow |  |
| REQ-001-HLJ-Chunk_2-Item_3-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | api|integration|partners | api|integration|partners |  |
| REQ-013-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] transparency|notification|status | notification|status | compliance|financialregulations|notification|status |
| REQ-025-HLJ-Chunk_2-Item_3-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] GDPR|compliance|privacy|security | compliance|privacy |  |
| REQ-023-HLJ-Chunk_2-Item_12-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] geolocation|infrastructure|location awareness | infrastructure|location awareness |  |
| REQ-023-HLJ-Chunk_2-Item_4-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | audit|backend|rollback | audit|rollback |  |
| REQ-024-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] notification|automation|reliability | reliability | api|automation|integration|messaging|notification|reliability |
| REQ-009-HLJ-Chunk_3-Item_5-v1.0 | opus4 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | messaging|notifications|payments | notification|payments |  |
| REQ-008-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] compliance|encryption|rbac | encryption|rbac | analytics|compliance|eligibility|encryption|income|rbac|rules |
| REQ-006-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] audit|support|usability | support | abuse-detection|api|audit|monitoring|rate-limiting|security|support |
| REQ-008-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.33 | 0.12 | 0.18 | 0.10 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] reconciliation|aggregation|data-normalization | aggregation|normalization | aggregation|api|doordash|eligibility|gig income|income verification|integration|normalization |
| REQ-006-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] resilience|rate-limiting |  | api|burst limits|rate-limiting |
| REQ-012-HLJ-Chunk_2-Item_9-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | compliance|gst | compliance|gst |  |
| REQ-023-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] automation|alerting|rollback | rollback | analytics|monitoring|rollback |
| REQ-015-HLJ-Chunk_1-Item_5-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] user-experience|ui|webhook | ui|webhook |  |
| REQ-013-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 0.50 | 0.25 | 0.33 | 0.20 | [INFERRED] traceability|audit|logging | audit|logs | audit|batch|logging|logic |
| REQ-023-HLJ-Chunk_2-Item_9-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] data protection|compliance|privacy laws | compliance|privacy laws |  |
| REQ-009-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] user confirmation|fx|validation | fx|validation | cancellation|fx|payments|validation|workflow |
| REQ-007-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] exception|aml|manualreview | aml | alert|aml|compliance|matching|monitoring|security|workflow |
| REQ-024-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 1.00 | 0.29 | 0.44 | 0.29 | 1.00 | 0.29 | 0.44 | 0.29 | integration|personalization | integration|personalization | backend|data|integration|messaging|personalization|scheduling|user profiling |
| REQ-022-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] policy|compliance|retention | compliance|retention | access_logs|compliance|logging|policy|retention|security |

_This report was auto-generated by evaluate_tag_accuracy.py_
