#!/usr/bin/env bash
# eval_all.sh — run the evaluation pipeline
# Usage:
#   ./eval_all.sh
# Make sure to `chmod +x eval_all.sh` once.

set -e  # exit immediately on errors

# -------- config --------
# Path to the venv inside eval/
# VENV_PY="venv/Scripts/python.exe"   # Windows
# Use the active conda env's python
VENV_PY="python"


# If you want to use system python instead, just set:
# VENV_PY="python3"

# -------- pipeline --------
echo "================ PIPELINE START ================"

"$VENV_PY" scripts/step_1/sbert_confidence_score.py
"$VENV_PY" scripts/step_1/evaluate_hlj_fields.py
"$VENV_PY" scripts/step_1/semantic_eval.py --plot || "$VENV_PY" scripts/step_1/semantic_eval.py
"$VENV_PY" scripts/step_1/generate_model_diff_heatmaps.py
"$VENV_PY" scripts/step_1/generate_eval_heatmaps.py

echo "================  PIPELINE DONE  ================"
echo "✅  All evaluations done! Check CSVs and plots under eval/."
