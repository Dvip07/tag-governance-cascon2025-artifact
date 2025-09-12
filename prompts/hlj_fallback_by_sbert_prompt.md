# 🧩 GPT-4.1 Field Fallback Prompt for HLJ Auto-Population

---

## 🎯 **Prompt Goal:**

When an HLJ field fails both confidence and semantic similarity checks (flagged by SBERT), use this prompt to request GPT-4.1 (or another strong LLM) to auto-populate the correct field value. This ensures schema compliance and semantic grounding with minimal hallucination risk.

---

## 🔹 **Prompt Template:**

```
You are an expert requirements engineer.
Given the following software requirement and its summary, generate the most accurate value for the requested field.

- Only answer with the field value (no extra text, no explanation, no formatting).
- If the value cannot be determined, answer with "unknown".

--- Requirement (raw) ---
{raw_requirement}

--- HLJ Summary ---
{summary}

--- Field to populate ---
{field_name}
```

---

## 🔍 **Usage Example:**

**Raw Requirement:**

A payment gateway for multiple tenants is experiencing intermittent crashes during high-volume transactions. Need a solution for stability, must notify on-call engineers if a retry queue spikes, and prevent double-charging with idempotency keys. Immediate deploy required, status update every 1 hour.


**HLJ Summary:**


Implement robust payment gateway failover and retry queue with alerting for multi-tenant support; ensure idempotency for payment safety.


**Field to populate:**


priority


**Expected LLM Output:**


High


---

## 📝 **Instructions for Integration:**

* Replace `{raw_requirement}` with the full requirement text.
* Replace `{summary}` with the HLJ or LLM-generated summary for this requirement.
* Replace `{field_name}` with the field you want to auto-populate (e.g., "priority", "difficulty").

## 🚦 **Best Practices:**

* Always request a single value, not an explanation.
* If you want an explanation for audit, run a second prompt or log the LLM's reasoning separately.
* For enum fields, instruct the LLM to select only from allowed values (e.g., "priority": High, Medium, Low), if needed.

---

## 🏷️ **Prompt Version:** 2025-05-29
