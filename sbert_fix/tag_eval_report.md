# Tag Accuracy Evaluation Report (GOLD: v3)

| Model | #HLJs | Prec@v2 | Recall@v2 | F1@v2 | Jac@v2 | Prec@v3 | Recall@v3 | F1@v3 | Jac@v3 |
|-------|-------|---------|-----------|-------|--------|---------|-----------|-------|--------|
| gpt41 | 381 | 0.657 | 0.450 | 0.509 | 0.377 | 0.897 | 0.417 | 0.532 | 0.410 |
| opus4 | 88 | 0.771 | 0.871 | 0.797 | 0.704 | 0.949 | 0.799 | 0.847 | 0.773 |
| meta70b | 45 | 0.756 | 0.889 | 0.801 | 0.725 | 0.881 | 0.844 | 0.847 | 0.787 |

## Per-domain Analysis
| Domain | #HLJs | Prec@v2 | Recall@v2 | F1@v2 | Jac@v2 | Prec@v3 | Recall@v3 | F1@v3 | Jac@v3 |
|--------|-------|---------|-----------|-------|--------|---------|-----------|-------|--------|
| FinTech | 282 | 0.694 | 0.556 | 0.586 | 0.467 | 0.880 | 0.516 | 0.608 | 0.502 |
| SaaS | 217 | 0.679 | 0.569 | 0.584 | 0.462 | 0.936 | 0.526 | 0.623 | 0.511 |
| SaaS Analytics | 10 | 0.517 | 0.304 | 0.376 | 0.242 | 0.900 | 0.289 | 0.429 | 0.289 |
| Compliance and Security | 5 | 0.800 | 0.933 | 0.853 | 0.767 | 0.900 | 0.900 | 0.900 | 0.867 |

## Error Cases (Low F1/Jaccard HLJs)
| HLJ | Model | Prec@v2 | Rec@v2 | F1@v2 | Jac@v2 | Prec@v3 | Rec@v3 | F1@v3 | Jac@v3 | v1 | v2 | v3 |
|-----|-------|---------|--------|-------|--------|---------|--------|-------|--------|----|----|----|
| REQ-004-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | automation|right-to-erasure | automation|right-to-erasure | automation|compliance|gdpr|privacy|right-to-erasure |
| REQ-025-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] alerting|external|resilience | external|resilience | alert|compliance|external|performance|privacy|resilience|sla |
| REQ-007-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] compliance|encryption|security | encryption|security | compliance|dashboard|encryption|reporting|security |
| REQ-009-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 1.00 | 0.25 | 0.40 | 0.25 | 1.00 | 0.25 | 0.40 | 0.25 | audit|compliance | audit|compliance | api|audit|compliance|fx-rates|integration|notification|real-time|sms |
| REQ-002-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] compliance|usability |  | compliance|onboarding|security|session |
| REQ-017-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] audit|events|history | history | audit|billing|edge_cases|events|history|subscriptions|upgrade |
| REQ-021-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.25 | 0.40 | 0.25 | comments|ux | comments | comments|highlighting|pdf|ux |
| REQ-019-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.25 | 0.36 | 0.22 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] weighting|analytics|retention | analytics|retention | analytics|api|cohorts|events|metrics|retention|time_decay|weighting |
| REQ-024-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | documentation|training | documentation|training | automation|documentation|ml|segmentation|training |
| REQ-011-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] compliance|emi|usability | emi | compliance|creditworthiness|emi |
| REQ-018-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | documentation|onboarding | documentation|onboarding | automation|documentation|onboarding|status|workflow |
| REQ-006-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] audit|compliance|security | compliance|security | api|audit|authentication|compliance|sandbox environments|security|testing |
| REQ-003-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] maintainability|false-positive|logging | logs | alert|email|false-positive|logging |
| REQ-008-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] resilience|edge-case|error-handling |  | edge_cases|eligibility|income |
| REQ-005-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] security|frontend|usability | usability | design|freezeunfreeze|mobile|security|ui|usability|virtualcard |
| REQ-006-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.50 | 0.17 | 0.25 | 0.14 | 1.00 | 0.17 | 0.29 | 0.17 | abuse-detection|security | security | api|billing|compliance|rate-limiting|reporting|security |
| REQ-028-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] escalation|priority|routing | routing | ai|escalation|logic|priority|routing |
| REQ-026-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.33 | 0.50 | 0.40 | 0.25 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] embedded-ui|nps|usability | nps | churn_prevention|nps |
| REQ-010-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 1.00 | 0.60 | 0.75 | 0.60 | 1.00 | 0.40 | 0.57 | 0.40 | dual-ledger|operational|real-time | dual-ledger|operational | dual-ledger|operational|operational-ledger|real-time|real-time posting |
| REQ-020-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | duplicates|usability | duplicates | contacts|crm|duplicates |
| REQ-001-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 0.00 | 0.00 | 0.00 | 0.00 | availability|error|logging | error | compliance|logging|security |
| REQ-016-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | compliance|usability | compliance | 2fa|compliance|logging|security |
| REQ-018-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | email|notification | email|notification | assignment|edge_cases|email|manual|notification|workflow |
| REQ-014-HLJ-Chunk_2-Item_12-v1.0 | meta70b | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.33 | 0.40 | 0.25 | audit|fee query|logging | audit|logs | audit|fee query|logging |
| REQ-025-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] performance|alerting|sla | alert|sla | alert|analytics|dashboard|filter|performance|sla |
| REQ-004-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | access-control|retention | retention | access-control|compliance|gdpr|retention|security |
| REQ-013-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 1.00 | 0.80 | 0.67 | 0.50 | 0.50 | 0.50 | 0.33 | [INFERRED] traceability|exception|logging | exception|logs | exception|logging |
| REQ-023-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] progressive-rollout|deployment|feature-flags | deployment | deployment|feature-flags|geo-ip|geo-targeting|progressive-rollout|rollback |
| REQ-010-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] least-privilege|access-control|rbac | rbac | least-privilege|rbac|reconciliation|resolution-workflows |
| REQ-005-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] consistency|integration|synchronization | synchronization | api|backend|sync |
| REQ-006-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.50 | 0.20 | 0.29 | 0.17 | 1.00 | 0.20 | 0.33 | 0.20 | alerting|monitoring | monitoring | alert|api|dashboard|monitoring|rate-limiting |
| REQ-030-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.50 | 0.67 | 0.57 | 0.40 | 0.67 | 0.67 | 0.67 | 0.50 | [INFERRED] artifact-retention|logs|screenshots|video | logs|screenshots|video | logging|screenshots|video |
| REQ-008-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] anomaly-detection|detection|fraud | detection|fraud | compliance|consent|detection|fraud|privacy|ux |
| REQ-008-HLJ-Chunk_2-Item_9-v1.0 | meta70b | 0.67 | 1.00 | 0.80 | 0.67 | 0.50 | 0.50 | 0.50 | 0.33 | [INFERRED] tracking|audit|logging | audit|logs | audit|logging |
| REQ-014-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 1.00 | 0.25 | 0.40 | 0.25 | 1.00 | 0.25 | 0.40 | 0.25 | notification | notification | estimation|gas-fee|notification|transaction |
| REQ-022-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] alerting|anomaly|notification | anomaly | compliance|notification|privacy|security |
| REQ-006-HLJ-Chunk_2-Item_9-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] latency|performance | performance | infrastructure|latency|performance|upgrade |
| REQ-017-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|integration|tax | integration|tax | integration|notification|prorated upgrades|tax |
| REQ-007-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] onboarding|aml|performance | aml|performance | aml|api|compliance|onboarding|performance|regulation|risk |
| REQ-009-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.67 | 0.80 | 0.67 | [INFERRED] risk management|fx|locking | fx|lock | fx|fx-rates|lock |
| REQ-009-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] regulatory reporting|compliance|documentation | compliance|documentation | audit|beta|compliance|documentation |
| REQ-020-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | rollback|usability | rollback | conflict-resolution|crm|data-merge|rollback |
| REQ-012-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.67 | 0.67 | 0.50 | 0.50 | 0.33 | 0.40 | 0.25 | [INFERRED] compliance|audit|logging | audit|logs | audit|compliance|logging |
| REQ-006-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] fallback|availability|resilience |  | api|audit|availability|fallback|multi-factor approval|override|security |
| REQ-008-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] compliance|dashboard|monitoring | monitoring | compliance|dashboard|eligibility|income|monitoring|rules |
| REQ-020-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] onboarding|duplicates|import | duplicates|import | crm|dryrun|duplicates|hubspot|import|oauth|onboarding |
| REQ-024-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | compliance|logging | compliance | compliance|integration|messaging |
| REQ-023-HLJ-Chunk_2-Item_7-v1.0 | opus4 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | audit|backend|compliance | audit|compliance | alert|audit|compliance|monitoring|real-time-analytics |
| REQ-028-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] tone-analysis|edge-case|nlp | nlp | ai|nlp|trend |
| REQ-009-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] compliance|abuse prevention|fx | fx | beta|compliance|feature-toggle|fx|regulation |
| REQ-010-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 0.50 | 0.25 | 0.33 | 0.20 | [INFERRED] reconciliation|batch|phantom-balance | batch|phantom balance | batch|documentation|phantom-balance|reconciliation |
| REQ-026-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.50 | 0.50 | 0.50 | 0.33 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] synchronization|nps | nps | nps|user_experience |
| REQ-007-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] reporting|compliance|dashboard | compliance|dashboard | audit|compliance|dashboard|legal|reporting|security|support |
| REQ-008-HLJ-Chunk_3-Item_3-v1.0 | opus4 | 0.67 | 1.00 | 0.80 | 0.67 | 0.50 | 0.50 | 0.50 | 0.33 | display|earnings|ux | display|earnings | earnings|ux |
| REQ-002-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | usability |  | compliance|feedback|kyc|onboarding |
| REQ-023-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] data-protection|compliance|privacy | compliance|privacy | compliance|feature-flags|privacy|rollback |
| REQ-009-HLJ-Chunk_2-Item_7-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] reliability|compliance|sla | compliance|sla | compliance|fx-rates|payments|sla|validation |
| REQ-004-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 0.50 | 0.33 | 0.40 | 0.25 | classification|gdpr | classification|gdpr | compliance|gdpr|privacy |
| REQ-011-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] compliance|decisioning|emi | emi | compliance|creditworthiness|decisioning|emi |
| REQ-021-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 1.00 | 0.29 | 0.44 | 0.29 | 1.00 | 0.14 | 0.25 | 0.14 | comments|ux | comments | comments|deeplink|documentation|navigation|pdf|quickstart|ux |
| REQ-017-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] period-alignment|dates|plans | dates|plans | billing|dates|invoice|plans|support |
| REQ-005-HLJ-Chunk_2-Item_9-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | encryption|security | encryption|security | encryption|integration|monitoring|queue|security|virtualcard |
| REQ-019-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] trends|heatmap|visualization | visualization | cohort_analysis|decay|edge_cases|heatmap|metrics|trend|visualization |
| REQ-024-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] analytics|a/b testing|segmentation | a/b testing|segmentation | analytics|backend|messaging|optimization|segmentation |
| REQ-022-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] compliance|audit|logging | audit|logs | access_logs|audit|compliance|database|logging |
| REQ-014-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | coverage |  | estimation|gas-fee |
| REQ-001-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.33 | 0.50 | 0.33 | compliance|openapi|spec | compliance|openapi | api|compliance|filter|openapi|query|spec |
| REQ-007-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] resilience|aml|availability | aml | aml|availability|compliance|fallback|regulation|reporting |
| REQ-009-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] integrations|api|fx | api|fx | api|fx|fx-rates|integration|timer|ui |
| REQ-028-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] training|change-management|usability |  | compliance|constraints|dependencies|training |
| REQ-010-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] compliance|audit|workflow | audit | audit|compliance|sox|workflow |
| REQ-015-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | delivery|reliability | delivery|reliability | analytics|delivery|logging|monitoring|reliability |
| REQ-023-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] location-resolution|geo-ip|real-time | geo-ip | feature-flags|geo-ip|integration|location-resolution|real-time|rollback |
| REQ-026-HLJ-Chunk_2-Item_6-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] automation|kpi | kpi | analytics|automation|kpi|nps |
| REQ-010-HLJ-Chunk_2-Item_4-v1.0 | meta70b | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | conversion-logic|multi-currency | multi-currency | currency |
| REQ-025-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.25 | 0.36 | 0.22 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] analytics|metrics|visualization | metrics|visualization | analytics|dashboard|engineering|metrics|performance|privacy|telemetry|visualization |
| REQ-006-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] customization|configuration|rate-limiting |  | api|configuration|rate-limiting|tenant management |
| REQ-008-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] data-verification|gig-economy|integration | integration | api|api integration|data-verification|gig workers|gig-economy|integration|uber |
| REQ-019-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] deduplication|cohorts|edge-case | cohorts | analytics_data_store|cohorts|compatibility |
| REQ-024-HLJ-Chunk_2-Item_8-v1.0 | opus4 | 0.33 | 1.00 | 0.50 | 0.33 | 0.50 | 1.00 | 0.67 | 0.50 | compliance|messaging|ux | compliance|messaging | messaging |
| REQ-005-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] logging|audit|compliance | audit|compliance | api|audit|authorization|compliance|security |
| REQ-017-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] anomaly-detection|admin|alert | admin|alert | admin|alert|billing|invoice|refund |
| REQ-016-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | maintainability|usability |  |  |
| REQ-019-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | automation|cohorts | cohorts | api|cohort_updates|cohorts |
| REQ-024-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] compliance|deduplication|reliability | deduplication|reliability | analytics|compliance|deduplication|reliability|testing |
| REQ-027-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 0.67 | 0.67 | 0.50 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] QA|mirror|validation | validation | mirror|qa|validation |
| REQ-011-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] compliance|emi|revalidation | emi | compliance|emi|override|support |
| REQ-008-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] regulation|compliance|privacy | compliance|privacy | api|audit|compliance|privacy|regulation |
| REQ-004-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | deletion|gdpr | deletion|gdpr | compliance|datadeletion|deletion|gdpr|privacy |
| REQ-025-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] performance|prompt|usability | prompt|usability | automation|ci/cd|performance|prompt|usability |
| REQ-024-HLJ-Chunk_2-Item_10-v1.0 | opus4 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | audit|compliance|logging | audit|compliance | audit|compliance|notification|recipient_experience |
| REQ-002-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | compliance|security | compliance|security | compliance|guardian|kyc|onboarding|security |
| REQ-015-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] reliability|performance|rate-limiting |  | reliability |
| REQ-028-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] escalation|nlp|urgency | nlp|urgency | ai|detection|escalation|nlp|urgency |
| REQ-026-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] behavioral-intelligence|nps | nps | behavioral_intelligence|nps|user_experience |
| REQ-016-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | usability |  | 2fa|compliance|reporting|security |
| REQ-020-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.50 | 0.17 | 0.25 | 0.14 | 1.00 | 0.17 | 0.29 | 0.17 | conflict|usability | conflict | conflict|crm|duplicate-detection|email|matching|merge |
| REQ-001-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.50 | 0.50 | 0.50 | 0.33 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|latency|performance|scalability | latency|performance | compliance|data|latency|performance |
| REQ-018-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.50 | 0.17 | 0.25 | 0.14 | 1.00 | 0.17 | 0.29 | 0.17 | filtering|search | search | assignment|email|integration|search|status|workflow |
| REQ-006-HLJ-Chunk_2-Item_5-v1.0 | gpt41 | 0.33 | 0.11 | 0.17 | 0.09 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] safety|availability|rollout | rollout | access-control|api|audit|availability|documentation|mfa|rate-limiting|rollback|security |
| REQ-014-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 0.50 | 0.33 | audit|logging | audit|logs | audit|logging |
| REQ-029-HLJ-Chunk_2-Item_9-v1.0 | meta70b | 0.67 | 1.00 | 0.80 | 0.67 | 0.50 | 0.50 | 0.50 | 0.33 | kpi|performance|traceability | performance|traceability | kpi|traceability |
| REQ-003-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 0.00 | 0.00 | 0.00 | 0.00 | rate-limiting|usability |  | alert|compliance|rate-limiting|regulation |
| REQ-005-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] authorization|backend|security | backend|security | api|authorization|backend|real-time|security |
| REQ-006-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 0.50 | 0.20 | 0.29 | 0.17 | compliance|logging | compliance|logs | api|compliance|logging|monitoring|rate-limiting |
| REQ-008-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|aml|kyc | aml|kyc | aml|compliance|currency|kyc |
| REQ-019-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] education|docs|support | docs|support | database|docs|optimization|performance|support |
| REQ-013-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 1.00 | 0.50 | 0.33 | 0.50 | 1.00 | 0.67 | 0.50 | [INFERRED] recovery|partial|retry | partial|retry | retry |
| REQ-025-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] regression|alerting|diagnostics | alert|diagnostics | alert|analytics|dashboard|debugging|diagnostics|regression|visualization |
| REQ-004-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] multi-user|edge-case|redaction | redaction | audit|compliance|integrity|privacy|redaction|security |
| REQ-015-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] compliance|notifications|webhooks | notification|webhook | compliance|insurance|notification|real-time|webhook |
| REQ-023-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] portal|admin|feature-flags | admin | admin|edge_cases|feature-flags|geo-ip|portal |
| REQ-007-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] transparency|usability|ux |  | access|documentation|privacy|security|training |
| REQ-010-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] compliance|pci-dss|sox | pci-dss|sox | compliance|ledger-management|pci-dss|phantom-reversals|sox|transaction-management |
| REQ-007-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 1.00 | 0.25 | 0.40 | 0.25 | 1.00 | 0.25 | 0.40 | 0.25 | aml|integration | aml|integration | aml|audit|backend|integration|performance|privacy|security|sla |
| REQ-009-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] countdown|fx|ui | fx|ui | countdown|fx|fx-rates|payments|rate-lock|ui |
| REQ-020-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | conflict|sync | conflict|sync | conflict|crm|duplicate-resolution|rollback|sync |
| REQ-022-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] integrity|audit|historical | audit | audit|export|export_controls|filter|rate-limiting|security |
| REQ-008-HLJ-Chunk_2-Item_8-v1.0 | opus4 | 0.75 | 0.50 | 0.60 | 0.43 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] ml|fraud|income|security | fraud|income|security | compliance|fraud|income|monitoring|reporting|security |
| REQ-014-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | advanced|usability | advanced|usability | advanced|dynamic|estimation|gas-fee|usability |
| REQ-006-HLJ-Chunk_2-Item_8-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] legacy|compatibility|migration | compatibility|migration | compatibility|documentation|legacy|migration|self-service |
| REQ-022-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] data-protection|privacy|regulation | privacy | data-protection|monitoring|privacy|regulation |
| REQ-017-HLJ-Chunk_2-Item_1-v1.0 | opus4 | 0.33 | 0.50 | 0.40 | 0.25 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] analytics|monitoring|notifications | monitoring | monitoring|notification |
| REQ-024-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] notification|multi-language|template | multi-language|template | backend|messaging|multi-language|notification|personalization|template |
| REQ-020-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | configurable|duplicates | configurable|duplicates | authentication|configurable|crm|crm-sync|detection|duplicates |
| REQ-016-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | compliance|security | compliance|security | 2fa|compliance|rolebasedaccess|security|securitycompliance |
| REQ-025-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] compliance|privacy|transparency | privacy|transparency | compliance|monitoring|performance|privacy|resilience|transparency |
| REQ-018-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] UI|email|inbox | email|inbox | collaboration|design|email|inbox|shared inbox|ui |
| REQ-028-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] self-service|efficiency|routing | efficiency|routing | customer|efficiency|routing|satisfaction|self-service |
| REQ-009-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] cancellation|refund|scheduled payments | refund|scheduled payments | cancellation|compliance|payments|refund|scheduled payments |
| REQ-023-HLJ-Chunk_2-Item_6-v1.0 | opus4 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | developer|documentation|training | developer|documentation | dashboard|developer|documentation|metrics|real-time-analytics |
| REQ-026-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.50 | 0.50 | 0.50 | 0.33 | 1.00 | 0.50 | 0.67 | 0.50 | nps|usability | nps | nps|user_experience |
| REQ-007-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.25 | 0.36 | 0.22 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] immutability|audit|security | audit|security | audit|compliance|immutability|manual|privacy|regulation|security|workflow |
| REQ-010-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | ui|visibility | ui | monitoring|real-time-analytics|ui |
| REQ-005-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] security|operational|usability | operational|usability | mobile|notification|operational|security|ui|usability |
| REQ-030-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|artifacts|security | artifacts|security | artifacts|compliance|debugging|security |
| REQ-006-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.50 | 0.20 | 0.29 | 0.17 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] authentication|security | security | api|availability|fallback|security|tenant segment |
| REQ-009-HLJ-Chunk_3-Item_7-v1.0 | opus4 | 0.33 | 1.00 | 0.50 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 | automation|error-handling|payments | payments | payments |
| REQ-003-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] configurability|fraud|micro-transaction | fraud|micro-transaction | detection|fraud|micro-transaction|microtransactions|rules |
| REQ-008-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 0.50 | 0.17 | 0.25 | 0.14 | [INFERRED] compliance|audit|logging | audit|logs | admin|audit|compliance|logging|portal|rules |
| REQ-029-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 0.50 | 0.25 | 0.33 | 0.20 | [INFERRED] traceability|logging|security | logs|security | compliance|logging|security|traceability |
| REQ-006-HLJ-Chunk_2-Item_10-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] communication|compliance|legal | compliance|legal | communication|compatibility|compliance|legacy|legal|migration |
| REQ-017-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] transparency|invoice|tax | invoice | billing|history|invoice|notification|tax |
| REQ-021-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | comments|ux | comments | comments|notification|optimization|performance|ux |
| REQ-005-HLJ-Chunk_2-Item_8-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | authentication|security | authentication|security | api|authentication|encryption|logging|security|virtualcard |
| REQ-024-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] compliance|help-center|usability | usability | analytics|compliance|monitoring|ui|usability |
| REQ-019-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] configurability|settings|usability | settings | cohort_analysis|cohorts|data_visualization|settings|update |
| REQ-012-HLJ-Chunk_2-Item_6-v1.0 | meta70b | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.67 | 0.80 | 0.67 | [INFERRED] compliance|exemptions|gst | exemption|gst | compliance|exemption|gst |
| REQ-009-HLJ-Chunk_2-Item_6-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] integrations|api|fx | api|fx | api|availability|fx|fx-rates |
| REQ-002-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | compliance|security | compliance|security | api|compliance|integration|kyc|security |
| REQ-023-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] user-notification|communication|user-option |  | alert|monitoring|notification |
| REQ-004-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 1.00 | 0.29 | 0.44 | 0.29 | 1.00 | 0.29 | 0.44 | 0.29 | gdpr|traceability | gdpr|traceability | audit|auditlogs|compliance|gdpr|lineage|traceability|tracking |
| REQ-001-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.75 | 0.86 | 0.75 | api|filtering|pagination | api|filter|pagination | api|filter|pagination|performance |
| REQ-007-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] compliance|aml|notification | aml|notification | aml|compliance|notification|state|ui|workflow |
| REQ-009-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] fallback|fx|notifications | fx|notification | compliance|fx|fx-rates|lock|notification |
| REQ-028-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] kpi|analytics|reporting | reporting | analytics|kpi|reporting|tracking |
| REQ-024-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.25 | 0.40 | 0.25 | analytics|dashboard | analytics | analytics|dashboard|messaging|ml |
| REQ-014-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | ui|usability | ui|usability | estimation|gas-fee|real-time|ui|usability |
| REQ-027-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] compliance|update|vendor | update|vendor | compliance|localization|rtl|translation|update|vendor |
| REQ-030-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.67 | 0.80 | 0.67 | blocking|ci-cd|critical-path | blocking|ci/cd | blocking|ci/cd|deployment |
| REQ-025-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] analytics|compliance|privacy | compliance|privacy | analytics|compliance|performance|privacy |
| REQ-019-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] guidance|error-handling|usability |  | ux|validation|warnings |
| REQ-024-HLJ-Chunk_2-Item_9-v1.0 | opus4 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | compliance|legal|tracking | compliance|tracking | compliance|opt-out|tracking|unsubscribe |
| REQ-005-HLJ-Chunk_2-Item_5-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] user-notification|availability|resilience |  | availability|logging|security |
| REQ-017-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] enablement|documentation|support | documentation|support | documentation|downgrades|manual review|payments|support |
| REQ-023-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] fallback|fault-tolerance|geo-ip | geo-ip | admin portal|fallback|feature-flags|geo-ip |
| REQ-015-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.50 | 0.67 | 0.50 | notifications|reliability | notification|reliability | documentation|notification|reliability|webhook |
| REQ-010-HLJ-Chunk_2-Item_5-v1.0 | meta70b | 0.33 | 0.50 | 0.40 | 0.25 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] data-integrity|alerting|reconciliation | reconciliation | data-integrity|reconciliation |
| REQ-009-HLJ-Chunk_2-Item_10-v1.0 | gpt41 | 0.33 | 0.50 | 0.40 | 0.25 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] implementation|delivery|modularity | delivery | delivery|implementation |
| REQ-025-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] analytics|reporting|segmentation | reporting|segmentation | analytics|instrumentation|metrics|performance|reporting|segmentation |
| REQ-003-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] real-time|alert|notification | alert|notification | alert|audit|compliance|fraud|notification|real-time|reporting |
| REQ-022-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] enablement|compliance|docs | compliance|docs | audit|compliance|docs|documentation|roles|security |
| REQ-008-HLJ-Chunk_2-Item_6-v1.0 | opus4 | 0.67 | 0.50 | 0.57 | 0.40 | 0.67 | 0.50 | 0.57 | 0.40 | aml|compliance|kyc | aml|compliance|kyc | compliance|kyc|legal|regulations |
| REQ-006-HLJ-Chunk_2-Item_6-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] developer-experience|testing|usability | testing | deployment|developer-experience|testing |
| REQ-005-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.50 | 0.20 | 0.29 | 0.17 | 1.00 | 0.20 | 0.33 | 0.20 | error_handling|usability | usability | help|mobile|ui|usability|virtualcard |
| REQ-010-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | metadata|synchronization | metadata | metadata|phantom-balance|sync|transaction-management |
| REQ-028-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] sentiment|classification|nlp | classification|nlp | ai|analysis|classification|nlp|sentiment |
| REQ-015-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 1.00 | 0.80 | 0.67 | 0.50 | 0.50 | 0.50 | 0.33 | [INFERRED] auditing|compliance|logging | compliance|logs | compliance|logging |
| REQ-023-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|audit|changelog | audit|changelog | audit|changelog|compliance|geo-ip |
| REQ-018-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.25 | 0.40 | 0.25 | 1.00 | 0.25 | 0.40 | 0.25 | assignment|manually | assignment|manually | assignment|automation|collision|concurrency|lock|manually|routing|rules |
| REQ-016-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.50 | 0.20 | 0.29 | 0.17 | 1.00 | 0.20 | 0.33 | 0.20 | security|usability | security | 2fa|appspecificoverrides|exemption|mobile|security |
| REQ-013-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.67 | 0.67 | 0.50 | 0.50 | 0.33 | 0.40 | 0.25 | [INFERRED] compliance|audit|logging | audit|logs | audit|compliance|logging |
| REQ-004-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] auditability|redaction|right-to-erasure | redaction|right-to-erasure | audit|auditlogs|compliance|gdpr|privacy|redaction|right-to-erasure |
| REQ-009-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | compliance|dashboard | compliance | compliance|dashboard|fx|fx-rates|payments |
| REQ-002-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.50 | 0.20 | 0.29 | 0.17 | 1.00 | 0.20 | 0.33 | 0.20 | compliance|usability | compliance | compliance|minor|onboarding|ux|workflow |
| REQ-024-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] compliance|timezone|usability | timezone | messaging|personalization|timezone|usability |
| REQ-019-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] persistence|analytics|cohorts | analytics|cohorts | analytics|cohorts|database|persistence |
| REQ-012-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.50 | 0.67 | 0.57 | 0.40 | 1.00 | 0.67 | 0.80 | 0.67 | [INFERRED] compliance|gst|portal|usability | gst|portal | compliance|gst|portal |
| REQ-017-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] finance|billing|proration | billing | billing|calculations|prorated upgrades|proration |
| REQ-021-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 1.00 | 0.25 | 0.40 | 0.25 | 1.00 | 0.25 | 0.40 | 0.25 | comments | comments | backend|comments|filter|threading |
| REQ-006-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] self-service|monitoring|usability | monitoring | alert|api|monitoring|rate-limiting|self-service|usage metrics |
| REQ-005-HLJ-Chunk_2-Item_10-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | compliance|regulation | compliance | api|compliance|integration|virtualcard |
| REQ-029-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] advanced-filtering|compliance|usability | compliance | compliance|consistency|session |
| REQ-008-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] transparency|consent|user-experience | consent|user experience | api|consent|documentation|integration|user_experience |
| REQ-022-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] data-protection|masking|privacy | masking|privacy | csv|data-protection|export|privacy|security |
| REQ-024-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.22 | 0.33 | 0.20 | 1.00 | 0.11 | 0.20 | 0.11 | [INFERRED] notification|testing|usability | testing | backend|delivery|i18n|messaging|notification|scheduling|testing|timing|usability |
| REQ-001-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.33 | 0.50 | 0.33 | audit|compliance|logging | audit|compliance | audit|authentication|compliance|logging|oauth|security |
| REQ-018-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | assignment|edge-case | assignment | assignment|concurrency|notification|ui |
| REQ-004-HLJ-Chunk_2-Item_5-v1.0 | opus4 | 0.50 | 0.40 | 0.44 | 0.29 | 1.00 | 0.60 | 0.75 | 0.60 | [INFERRED] edge-cases|alerts|monitoring|testing | alert|monitoring|testing | alert|implementation|migration|monitoring|testing |
| REQ-003-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] data-minimization|privacy|security | privacy|security | alert|privacy|ratelimit|security |
| REQ-025-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] regression|automation|remediation | remediation | analytics|diagnostics|external services|fallback|performance|regression|remediation |
| REQ-013-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] consistency|atomicity|rollback | atomicity|rollback | atomicity|batch|consistency|rollback |
| REQ-015-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.50 | 0.50 | 0.50 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 | registration|webhooks | registration|webhook | registration|webhook |
| REQ-008-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] validation|edge-case|eligibility | eligibility | aggregation|data|earnings|eligibility|income|user_experience |
| REQ-006-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] API|feedback|usability | feedback | api|feedback|instant feedback|rate-limiting |
| REQ-027-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 0.50 | 0.33 | 0.40 | 0.25 | [INFERRED] traceability|auditing|logging | audit|logs | audit|auditlogs|logging |
| REQ-008-HLJ-Chunk_3-Item_1-v1.0 | opus4 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.33 | 0.50 | 0.33 | ui|ux|workflow | workflow | ui|ux|workflow |
| REQ-009-HLJ-Chunk_2-Item_5-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] retry|error handling|scheduled payments | scheduled payments | fx-rates|retry|scheduled payments |
| REQ-026-HLJ-Chunk_2-Item_9-v1.0 | meta70b | 0.67 | 1.00 | 0.80 | 0.67 | 0.50 | 0.50 | 0.50 | 0.33 | nps|opt_out|user_experience | nps|opt_out | nps|user_experience |
| REQ-015-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 1.00 | 0.67 | 0.80 | 0.67 | 1.00 | 0.33 | 0.50 | 0.33 | self-service|usability | usability | compliance|self-service|usability |
| REQ-029-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 0.50 | 0.17 | 0.25 | 0.14 | [INFERRED] session-tracking|compliance|logging | compliance|logs | access-control|compliance|logging|query|rbac|session-tracking |
| REQ-019-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] interoperability|export|reporting | export|reporting | cohort_analysis|export|reporting|settings|ui |
| REQ-024-HLJ-Chunk_2-Item_7-v1.0 | opus4 | 0.33 | 0.25 | 0.29 | 0.17 | 0.00 | 0.00 | 0.00 | 0.00 | automation|failover|reliability |  | alert|automation|deliverability|monitoring |
| REQ-021-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.17 | 0.29 | 0.17 | notifications | notification | browsers|compatibility|filter|notification|ui|ux |
| REQ-005-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] compliance|operational|usability | operational|usability | authentication|compliance|mobile|operational|security|usability|virtualcard |
| REQ-024-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | compliance|opt-out | compliance|opt-out | api|compliance|integration|messaging|opt-out |
| REQ-003-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] customization|fraud|rules | fraud|rules | alert|detection|fraud|notification|patterns|rules |
| REQ-018-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | email|tagging | email|tagging | automation|data|email|model|routing|tagging |
| REQ-025-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | analytics|self-service | analytics | analytics|dashboard|performance|self-service|ux |
| REQ-016-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 0.50 | 0.33 | 0.40 | 0.25 | security|usability | security|usability | 2fa|rolebasedaccess|security |
| REQ-010-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 1.00 | 0.67 | 0.80 | 0.67 | 0.50 | 0.33 | 0.40 | 0.25 | lifecycle|phantom-balance | lifecycle|phantom balance | lifecycle|phantom-balance|testing |
| REQ-026-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 | usability |  |  |
| REQ-028-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] latency|performance | performance | customer|documentation|guidelines|performance |
| REQ-009-HLJ-Chunk_2-Item_8-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] rollout|beta|usability | beta | beta|fx-rates|rollback|ui|workflow |
| REQ-023-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] kpi-tracking|dashboard|real-time-analytics | dashboard|real-time-analytics | analytics|dashboard|kpi-tracking|real-time-analytics |
| REQ-013-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] flexibility|batch|scheduling | batch | batch|failurehandling|rollback|scheduling |
| REQ-025-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] performance|instrumentation|timing | instrumentation|timing | analytics|instrumentation|optimization|performance|timing |
| REQ-004-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | integrity|security | integrity|security | analytics|audit|compliance|integrity|reporting|security |
| REQ-008-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.22 | 0.33 | 0.20 | 1.00 | 0.22 | 0.36 | 0.22 | [INFERRED] rules-engine|eligibility|risk | eligibility|risk | aml|api|compliance|eligibility|integration|kyc|risk|rules-engine|upwork |
| REQ-030-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | parallel|staging|ui-testing | parallel|staging | browser_coverage|parallel|staging|ui_testing |
| REQ-006-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] real-time|configuration|usability |  | api|configuration|rate-limiting|real-time|real-time updates |
| REQ-021-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.25 | 0.40 | 0.25 | support|usability | support | events|notification|support|usability |
| REQ-005-HLJ-Chunk_2-Item_6-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] rollback|consistency|error_handling |  | backend|queue|rest|rollback|security|virtualcard |
| REQ-024-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] notification|automation|multi-channel | multi-channel | automation|channel|messaging|multi-channel|notification|personalization|preferences |
| REQ-005-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | documentation|usability | documentation|usability | documentation|integration|mobile|notification|usability |
| REQ-026-HLJ-Chunk_2-Item_11-v1.0 | meta70b | 0.33 | 1.00 | 0.50 | 0.33 | 0.50 | 1.00 | 0.67 | 0.50 | edge_cases|nps|trigger_prioritization | nps|trigger_prioritization | nps |
| REQ-027-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] compliance|enablement|training | enablement | compliance|enablement|layout|preview|rtl |
| REQ-022-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 0.50 | 0.25 | 0.33 | 0.20 | [INFERRED] security|export|roles | export|roles | compliance|export|export_controls|security |
| REQ-014-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] coverage|integration|oracle | integration|oracle | blockchain|estimation|gas-fee|integration|oracle |
| REQ-001-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 0.50 | 0.25 | 0.33 | 0.20 | api|rest|spec | api|rest | api|compliance|endpoint|openbanking |
| REQ-004-HLJ-Chunk_2-Item_3-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] security|meta-log|real-time | meta-log | audit|compliance|meta-log|security |
| REQ-009-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] traceability|audit|fx | audit|fx | audit|fx|payments|processing|scheduling |
| REQ-023-HLJ-Chunk_2-Item_8-v1.0 | opus4 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | authentication|backend|infrastructure | authentication | authentication|infrastructure|rollback|user_experience |
| REQ-007-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.25 | 0.36 | 0.22 | 0.50 | 0.12 | 0.20 | 0.11 | [INFERRED] traceability|audit|logging | audit|logs | audit|compliance|logging|notification|screening|testing|traceability|workflow |
| REQ-010-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | exception|reporting | exception|reporting | audit-trails|exception|immutable logging|reporting|security |
| REQ-010-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] compliance|regulatory|reporting | reporting | compliance|dual-ledger|financial reporting|regulation|reporting|reporting-ledger |
| REQ-020-HLJ-Chunk_2-Item_11-v1.0 | opus4 | 0.25 | 1.00 | 0.40 | 0.25 | 0.50 | 1.00 | 0.67 | 0.50 | [INFERRED] compliance|audit|history|logging | audit|history | audit |
| REQ-023-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] enablement|documentation|training | documentation|training | compliance|documentation|enablement|gdpr|training |
| REQ-018-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.50 | 0.14 | 0.22 | 0.12 | 1.00 | 0.14 | 0.25 | 0.14 | concurrency|locking | lock | analytics|concurrency|lock|reporting|routing|rules|search |
| REQ-024-HLJ-Chunk_3-Item_1-v1.0 | opus4 | 0.50 | 0.67 | 0.57 | 0.40 | 1.00 | 0.67 | 0.80 | 0.67 | [INFERRED] automation|scheduling|timezone|ux | scheduling|timezone | automation|scheduling|timezone |
| REQ-016-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | compliance|security | compliance|security | 2fa|compliance|notification|security|ux |
| REQ-020-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | history|logging | history | crm|duplicate-detection|fuzzy-matching|webhook |
| REQ-003-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | alert|details | alert|details | alert|details|integration|privacy|security|slack |
| REQ-022-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] security|abuse|rate-limit | abuse | abuse|compliance|rate-limiting|security |
| REQ-006-HLJ-Chunk_2-Item_7-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] education|documentation | documentation | client-support|documentation|sandbox|testing |
| REQ-005-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] accessibility|feedback|usability | feedback|usability | design|feedback|mobile|ui|usability|virtualcard |
| REQ-021-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | comments|ux | comments | comments|pdf|replies|threaded_discussions|ux |
| REQ-006-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | compliance|reporting | compliance|reporting | api|compliance|metrics|rate-limiting|reporting|self-service |
| REQ-008-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] user-trust|dispute|user-interface | dispute | api|dispute|security |
| REQ-002-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | maintainability|usability |  | compliance|encryption|security |
| REQ-001-HLJ-Chunk_2-Item_5-v1.0 | opus4 | 0.50 | 0.67 | 0.57 | 0.40 | 0.67 | 0.67 | 0.67 | 0.50 | [INFERRED] security|compliance|deployment|review | compliance|deployment|review | compliance|review|security |
| REQ-004-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | audit|meta-log | audit|meta-log | audit|compliance|gdpr|logging|meta-log |
| REQ-009-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] messaging|notifications|usability | notification|usability | fx-rates|notification|rate-lock|reporting|usability |
| REQ-009-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] usability|scheduled payments|ui | scheduled payments|ui | payments|scheduled payments|scheduling|ui |
| REQ-007-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] integration|aml|screening | aml|screening | aml|compliance|integration|kyc|regulation|screening |
| REQ-016-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | compliance|security | compliance|security | 2fa|compliance|documentation|security|support |
| REQ-018-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.17 | 0.29 | 0.17 | analytics|reporting | reporting | analytics|concurrency|documentation|lock|onboarding|reporting |
| REQ-022-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] usability|export|filter | export|filter | compliance|export|export_controls|filter|security |
| REQ-003-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 0.50 | 0.20 | 0.29 | 0.17 | [INFERRED] auditability|audit|logging | audit|logs | alert|audit|data|logging|security |
| REQ-028-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] reporting|analytics|trend | trend | analytics|leadership|reporting|training|trend |
| REQ-024-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] personalization|scheduling|timezone | scheduling|timezone | messaging|personalization|preview|scheduling|timezone |
| REQ-012-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] automation|gst|rates | gst|rates | gst|provincial tax|rates|tax |
| REQ-008-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] configurability|admin|rule-management | admin | admin|api|data connection|fiverr|integration|rule-management|user_experience |
| REQ-006-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | enforcement|rate-limiting | enforcement | api|api-gateway|enforcement|infrastructure|rate-limiting |
| REQ-013-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] reliability|failure|rollback | failure|rollback | failure|reliability|reporting|rollback |
| REQ-025-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 0.17 | 0.22 | 0.12 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] performance|cicd|regression | regression | alert|analytics|ci/cd|optimization|performance|regression |
| REQ-010-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] immutable|audit|logging | audit | audit|compliance|immutability|logging|reconciliation |
| REQ-015-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] usability|customization|webhooks | webhook | customization|fault-tolerance|reliability|webhook |
| REQ-023-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] geo-segmentation|feature-flags|scalable | scalable | feature-flags|geo-segmentation|scalable|segmentation |
| REQ-011-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|creditworthiness|integration | creditworthiness|integration | checkout|compliance|creditworthiness|integration |
| REQ-022-HLJ-Chunk_2-Item_1-v1.0 | opus4 | 0.33 | 1.00 | 0.50 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 | performance|rate-limiting|security | security | security |
| REQ-029-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.33 | 0.20 | 0.25 | 0.14 | 1.00 | 0.20 | 0.33 | 0.20 | [INFERRED] query-interface|compliance|usability | compliance | compliance|data analysis|filter|query|query-interface |
| REQ-019-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] comparison|overlay|visualization | overlay|visualization | decay|decay_parameters|metrics|overlay|user_experience|visualization |
| REQ-024-HLJ-Chunk_2-Item_6-v1.0 | opus4 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.50 | 0.67 | 0.50 | alerts|monitoring|reliability | alert|monitoring | alert|analytics|dashboard|monitoring |
| REQ-017-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] fraud|abuse|review | abuse|review | abuse|payment processing|prorated upgrades|review|subscriptions |
| REQ-021-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.20 | 0.33 | 0.20 | comments|ux | comments | backend|comments|notification|status|ux |
| REQ-015-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | monitoring|usability | monitoring | monitoring|support|training |
| REQ-009-HLJ-Chunk_2-Item_4-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] outage-handling|availability|fx | fx | availability|fx|fx-rates|rollback |
| REQ-002-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | compliance|maintainability | compliance | compliance|guardian|kyc|workflow |
| REQ-020-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 0.50 | 0.25 | 0.33 | 0.20 | 1.00 | 0.25 | 0.40 | 0.25 | docs|usability | docs | auto-merge|crm|docs|sync |
| REQ-004-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] traceability|gdpr|metadata | gdpr|metadata | audit|auditlogs|compliance|gdpr|metadata|traceability |
| REQ-013-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] transparency|notification|status | notification|status | compliance|financialregulations|notification|status |
| REQ-018-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.17 | 0.29 | 0.17 | assignment|automation | assignment | assignment|assignment rules|automation|setup|tagging|workflow |
| REQ-020-HLJ-Chunk_1-Item_1-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] security|oauth|sync | oauth|sync | api|authentication|crm|oauth|salesforce|sync |
| REQ-016-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | maintainability|security | security | 2fa|rolebasedaccess|security |
| REQ-010-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 0.50 | 0.25 | 0.33 | 0.20 | phantom-balance|segregation | phantom balance|segregation | ledger-management|phantom-balance|reconciliation|segregation |
| REQ-015-HLJ-Chunk_2-Item_6-v1.0 | gpt41 | 0.33 | 0.50 | 0.40 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] reliability|availability|scalability |  | availability|reliability |
| REQ-028-HLJ-Chunk_1-Item_6-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] retraining|continuous-learning|feedback | feedback | audit|feedback|transparency |
| REQ-002-HLJ-Chunk_2-Item_8-v1.0 | meta70b | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.67 | 0.80 | 0.67 | auditing|compliance | audit|compliance | audit|auditlogs|compliance |
| REQ-005-HLJ-Chunk_1-Item_4-v1.0 | gpt41 | 1.00 | 0.33 | 0.50 | 0.33 | 1.00 | 0.33 | 0.50 | 0.33 | documentation|usability | documentation|usability | documentation|feedback|mobile|ui|usability|virtualcard |
| REQ-024-HLJ-Chunk_1-Item_8-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.17 | 0.29 | 0.17 | [INFERRED] notification|automation|reliability | reliability | api|automation|integration|messaging|notification|reliability |
| REQ-003-HLJ-Chunk_1-Item_3-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] analytics|detection|micro-transaction | detection|micro-transaction | analytics|detection|fraud|micro-transaction|rules |
| REQ-009-HLJ-Chunk_3-Item_5-v1.0 | opus4 | 0.33 | 0.50 | 0.40 | 0.25 | 1.00 | 1.00 | 1.00 | 1.00 | messaging|notifications|payments | notification|payments | notification|payments |
| REQ-008-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.67 | 0.29 | 0.40 | 0.25 | 1.00 | 0.29 | 0.44 | 0.29 | [INFERRED] compliance|encryption|rbac | encryption|rbac | analytics|compliance|eligibility|encryption|income|rbac|rules |
| REQ-005-HLJ-Chunk_1-Item_10-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | feedback|usability | feedback|usability | feedback|messaging|mobile|ui|usability |
| REQ-006-HLJ-Chunk_2-Item_1-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] audit|support|usability | support | abuse-detection|api|audit|monitoring|rate-limiting|security|support |
| REQ-008-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.33 | 0.12 | 0.18 | 0.10 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] reconciliation|aggregation|data-normalization | aggregation|normalization | aggregation|api|doordash|eligibility|gig income|income verification|integration|normalization |
| REQ-006-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] resilience|rate-limiting |  | api|burst limits|rate-limiting |
| REQ-021-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 0.50 | 0.67 | 0.50 | 1.00 | 0.25 | 0.40 | 0.25 | support|usability | support | migration|support|usability|versioning |
| REQ-005-HLJ-Chunk_2-Item_7-v1.0 | gpt41 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | [INFERRED] concurrency|consistency|error_handling |  | atomicity|backend|virtualcard |
| REQ-026-HLJ-Chunk_2-Item_5-v1.0 | gpt41 | 0.50 | 0.50 | 0.50 | 0.33 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] compliance|localization | localization | compliance|localization |
| REQ-023-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.33 | 0.33 | 0.33 | 0.20 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] automation|alerting|rollback | rollback | analytics|monitoring|rollback |
| REQ-015-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 0.50 | 0.33 | 0.40 | 0.25 | 1.00 | 0.33 | 0.50 | 0.33 | error-handling|validation | validation | ui|validation|webhook |
| REQ-013-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 0.50 | 0.25 | 0.33 | 0.20 | [INFERRED] traceability|audit|logging | audit|logs | audit|batch|logging|logic |
| REQ-004-HLJ-Chunk_2-Item_2-v1.0 | gpt41 | 0.67 | 0.50 | 0.57 | 0.40 | 1.00 | 0.50 | 0.67 | 0.50 | [INFERRED] reporting|dashboard|monitoring | dashboard|monitoring | dashboard|gdpr|monitoring|reporting |
| REQ-023-HLJ-Chunk_2-Item_9-v1.0 | meta70b | 0.33 | 0.50 | 0.40 | 0.25 | 0.50 | 0.50 | 0.50 | 0.33 | [INFERRED] data protection|compliance|privacy laws | compliance|privacy laws | compliance|privacy |
| REQ-009-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.67 | 0.40 | 0.50 | 0.33 | 1.00 | 0.40 | 0.57 | 0.40 | [INFERRED] user confirmation|fx|validation | fx|validation | cancellation|fx|payments|validation|workflow |
| REQ-010-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 0.33 | 0.25 | 0.29 | 0.17 | 1.00 | 0.25 | 0.40 | 0.25 | [INFERRED] reconciliation|mismatch|tooling | mismatch | mismatch|reconciliation|role-based access|security |
| REQ-007-HLJ-Chunk_1-Item_7-v1.0 | gpt41 | 0.33 | 0.14 | 0.20 | 0.11 | 1.00 | 0.14 | 0.25 | 0.14 | [INFERRED] exception|aml|manualreview | aml | alert|aml|compliance|matching|monitoring|security|workflow |
| REQ-026-HLJ-Chunk_2-Item_10-v1.0 | meta70b | 0.33 | 1.00 | 0.50 | 0.33 | 0.50 | 1.00 | 0.67 | 0.50 | device_coordination|edge_cases|nps | device_coordination|nps | nps |
| REQ-024-HLJ-Chunk_1-Item_5-v1.0 | gpt41 | 1.00 | 0.29 | 0.44 | 0.29 | 1.00 | 0.29 | 0.44 | 0.29 | integration|personalization | integration|personalization | backend|data|integration|messaging|personalization|scheduling|user profiling |
| REQ-005-HLJ-Chunk_1-Item_9-v1.0 | gpt41 | 1.00 | 0.40 | 0.57 | 0.40 | 1.00 | 0.40 | 0.57 | 0.40 | feedback|operational | feedback|operational | documentation|feedback|mobile|operational|support |
| REQ-022-HLJ-Chunk_1-Item_2-v1.0 | gpt41 | 0.67 | 0.33 | 0.44 | 0.29 | 1.00 | 0.33 | 0.50 | 0.33 | [INFERRED] policy|compliance|retention | compliance|retention | access_logs|compliance|logging|policy|retention|security |

_This report was auto-generated by evaluate_tag_accuracy.py_
