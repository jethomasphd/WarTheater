#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Paper 2 — v2 (student-findings edition): reproduce the whole focused
# analysis from the frozen v1.2 dataset.
#
#   bash run_all.sh
#
# Regenerates data/panel_daily.csv, data/health_system_events.csv, the focused
# tables in output/tables/, and the three finding figures in output/figures/.
# Reads the SAME frozen release the parent paper uses, so every number here is
# identical to the parent's — this edition re-narrates the same evidence around
# the three findings the first author chose to develop. Deterministic
# (SEED = 42); ~30 seconds.
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")"
export MPLBACKEND=Agg          # headless plotting
export PYTHONHASHSEED=0         # determinism

echo "==> Paper 2 v2 (three findings): reproducible analysis pipeline"
echo "    dataset: ../../releases/v1.2/iranwar_event_dataset.csv (pinned, shared)"
echo

STEPS=(
  "00_build_panel.py"          # panel + audited health-system register
  "01_frontloading.py"         # Finding 1 — the war killed fast and early
  "02_resilience_erosion.py"   # Finding 5 — the system stopped absorbing shocks
  "03_indirect_floor.py"       # Finding 6 — the counted dead are a floor
  "04_synthesis.py"            # the three findings, wired into one argument
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
echo "    Summary: output/synthesis.json"
