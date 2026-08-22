#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Paper 2 — reproduce the entire analysis from the frozen v1.2 dataset.
#
#   bash run_all.sh
#
# Runs every step in order; regenerates data/panel_daily.csv,
# data/health_system_events.csv, all tables in output/tables/, and all
# figures in output/figures/. Deterministic: all bootstraps are seeded
# (SEED=42). Takes ~1 minute.
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")"
export MPLBACKEND=Agg          # headless plotting
export PYTHONHASHSEED=0         # determinism

echo "==> Paper 2: reproducible analysis pipeline"
echo "    dataset: ../releases/v1.2/iranwar_event_dataset.csv (pinned)"
echo

STEPS=(
  "00_build_panel.py"
  "01_descriptives.py"
  "02_phase_comparison.py"
  "03_regression.py"
  "04_mediation.py"
  "05_moderation.py"
  "06_indirect_burden.py"
  "07_source_divergence.py"
)

for step in "${STEPS[@]}"; do
  echo "==> python3 src/${step}"
  ( cd src && python3 "${step}" )
  echo
done

echo "==> DONE."
echo "    Panel  : data/panel_daily.csv + data/health_system_events.csv"
echo "    Tables : output/tables/*.csv   ($(ls output/tables | wc -l | tr -d ' ') files)"
echo "    Figures: output/figures/*.png|pdf ($(ls output/figures | wc -l | tr -d ' ') files)"
