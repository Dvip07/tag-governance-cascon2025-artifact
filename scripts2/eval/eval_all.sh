#!/bin/bash
set -e

python eval/sbert_low_confidence_fix.py
python eval/evaluate_hlj_fields.py
python eval/semantic_eval.py
python eval/generate_model_diff_heatmaps.py

echo "✅  All evaluations done! Check your plots and CSVs."


# Add any additional evaluation scripts here
# chmod +x eval_all.sh

# Command
# ./eval_all.sh


