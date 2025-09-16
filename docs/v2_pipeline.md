# 🚀 Tag Governance Pipeline v2 (HLJ-Centric, Multi-Version, Audit-First)

---

## 🌍 Dataset Types

### **1. Legacy Dataset**

* **Tags via:** GPT-4o + semi-automation
* **Features:** single-version, includes **flat-WBS**
* **Purpose:** baseline enrichment + audit

### **2. Testing Dataset**

* **Tags via:** Multi-model (gpt41, opus4, meta70b)
* **Versions:** v1 (LLM), v2 (SBERT), v3 (Hybrid)
* **Features:** no flat-WBS, **multi-HLJ per requirement**
* **Purpose:** research-grade, benchmarking, reproducibility

---

## 🛠️ Pipeline (Testing Dataset)

### **Step 1: Harvest Tags**

`harvest_tags.py`

* Extracts all tags per HLJ, across models & versions.
* Records `tag, hlj_id, req_id, model, version`.
* **Output:** `tags_all.csv`

### **Step 2: Token-Length Filter**

`filter_tags_by_token_length.py`

* Compute median token length → drop tags above median.
* **Output:** `tags_token_filtered.csv`

### **Step 3: Semantic Clustering**

`cluster_tags_faiss_sbert.py`

* Embeds tags (SBERT/InstructorXL) + clusters via FAISS.
* Assigns `cluster_id`.
* **Output:** `tag_clusters.csv`

### **Step 4: Canonical Labels & Aliases**

`generate_canonical_labels.py`

* Canonical label = shortest/highest-TFIDF tag.
* Maps aliases using `alias_tag.json`.
* **Output:** `canonical_tags.yaml`, `tag_alias_map.json`

### **Step 5: Deduplication (Hybrid)**

`deduplicate_tags.py`

* SBERT + FAISS nearest neighbor search.
* Merge/alias above threshold, log method.
* **Output:** `deduplicated_tags.csv`

### **Step 6: Top-K Scoring**

`score_tags.py`

* For each HLJ: select top-k tags by frequency, centrality.
* **Output:** `topk_tags_per_hlj.json`

### **Step 7: NLU Validation**

`validate_tags_nlu.py`

* Check semantic similarity tag ↔ HLJ summary/raw requirement.
* Attach confidence, drop/flag low scores.
* **Output:** `validated_tags_per_hlj.json`

### **Step 8: Domain Consistency**

`filter_tags_domain.py`

* Whitelist check (+ Bayesian optional).
* **Output:** `domain_filtered_tags_per_hlj.json`

### **Step 9: Metadata Persistence**

`persist_tag_metadata.py`

* Save full traceability (cluster, canonical, conf, model, drop reason).
* **Output:** `hlj_tag_metadata/{hlj_id}.json`

### **Step 10: Drift Detection**

`detect_tag_drift.py`

* Compare new vs old clusters/tags.
* Auto-generate governance PRs.
* **Output:** `tag_drift_report.yaml`, `auto_pr_alias_update.yml`

### **Step 11: Evaluation**

`evaluate_tag_accuracy.py`

* Compare v1 vs v2 vs v3.
* Compute **Precision, Recall, F1, Jaccard**.
* **Outputs:**

  * `tag_eval_stats.csv`
  * `tag_eval_report.md`

---

## 📊 Flow Diagram

```mermaid
graph TD
    A[HLJ JSONs (all models/versions)] --> B[Step 1: Harvest Tags]
    B --> C[Step 2: Token-Length Filter]
    C --> D[Step 3: Semantic Clustering]
    D --> E[Step 4: Canonical Labels & Aliases]
    E --> F[Step 5: Deduplication]
    F --> G[Step 6: Top-K Scoring]
    G --> H[Step 7: NLU Validation]
    H --> I[Step 8: Domain Consistency]
    I --> J[Step 9: Metadata Persistence]
    J --> K[Step 10: Drift Detection]
    J --> L[Step 11: Evaluation]
```

---

## 🎯 Research Hooks

* **Reproducibility:** every step yields deterministic, versioned outputs.
* **Metrics:** Precision/Recall/F1/Jaccard at HLJ + per-domain.
* **Governance:** drift reports auto-generate CTD PRs.
* **Traceability:** metadata per-HLJ includes cluster, alias, model provenance, confidence.

---

## 📜 Final Scripts

| #  | Script                           | Purpose                          | Output                                              |
| -- | -------------------------------- | -------------------------------- | --------------------------------------------------- |
| 1  | `harvest_tags.py`                | Collect raw tags                 | `tags_all.csv`                                      |
| 2  | `filter_tags_by_token_length.py` | Median token filter              | `tags_token_filtered.csv`                           |
| 3  | `cluster_tags_faiss_sbert.py`    | SBERT+FAISS clustering           | `tag_clusters.csv`                                  |
| 4  | `generate_canonical_labels.py`   | Canonical labels + aliases       | `canonical_tags.yaml`, `tag_alias_map.json`         |
| 5  | `deduplicate_tags.py`            | Deduplicate tags                 | `deduplicated_tags.csv`                             |
| 6  | `score_tags.py`                  | Top-k scoring                    | `topk_tags_per_hlj.json`                            |
| 7  | `validate_tags_nlu.py`           | NLU similarity validation        | `validated_tags_per_hlj.json`                       |
| 8  | `filter_tags_domain.py`          | Domain consistency               | `domain_filtered_tags_per_hlj.json`                 |
| 9  | `persist_tag_metadata.py`        | Full tag metadata                | `hlj_tag_metadata/{hlj_id}.json`                    |
| 10 | `detect_tag_drift.py`            | Drift detection + governance PRs | `tag_drift_report.yaml`, `auto_pr_alias_update.yml` |
| 11 | `evaluate_tag_accuracy.py`       | Compare v1/v2/v3                 | `tag_eval_stats.csv`, `tag_eval_report.md`          |
