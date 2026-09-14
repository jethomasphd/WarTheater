#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Paper 2 — v3 (plain-language, three-tool edition): reproduce the whole
# analysis from the frozen v1.2 dataset.
#
#   bash run_all.sh
#
# Regenerates data/panel_daily.csv, data/health_system_events.csv, every
# table in output/tables/, every figure in output/figures/, and
# output/numbers.json. The last step re-derives every headline number in the
# manuscript and checks it, so the pipeline fails loudly on any drift.
# Deterministic; no network access; about 30 seconds.
#
# Optional final step: rebuild the Word manuscript (needs Node.js and the
# `docx` npm package; see manuscript/make_docx.js). It is skipped, with a
# message, if Node or the package is not available.
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")"
export MPLBACKEND=Agg          # headless plotting
export PYTHONHASHSEED=0         # determinism

echo "==> Paper 2 v3 (three tools: means comparison, correlation, regression)"
echo "    dataset: ../../releases/v1.2/iranwar_event_dataset.csv (pinned, frozen)"
echo

STEPS=(
  "00_build_panel.py"          # daily panel + audited health-system register
  "01_means_comparison.py"     # Finding 1 — the war killed early
  "02_correlation.py"          # bridge — strikes and deaths, by damage period
  "03_regression.py"           # Finding 2 — the strike-death slope steepened with damage
  "04_floor.py"                # Finding 3 — the counted dead are a floor
  "05_check_numbers.py"        # every headline number re-derived and checked
  "06_manuscript_tables.py"    # manuscript tables rendered from the CSVs and checked verbatim
)

for step in "${STEPS[@]}"; do
  echo "==> python3 src/${step}"
  ( cd src && python3 "${step}" )
  echo
done

echo "==> DONE (analysis)."
echo "    Panel  : data/panel_daily.csv + data/health_system_events.csv"
echo "    Tables : output/tables/*.csv   ($(ls output/tables | wc -l | tr -d ' ') files)"
echo "    Figures: output/figures/*.png|pdf ($(ls output/figures | wc -l | tr -d ' ') files)"
echo "    Numbers: output/numbers.json  |  Tables for the paper: output/manuscript_tables.md"
echo

if command -v node >/dev/null 2>&1 && ( cd manuscript && node -e "require('docx')" >/dev/null 2>&1 ); then
  echo "==> node manuscript/make_docx.js"
  ( cd manuscript && node make_docx.js )
else
  echo "==> Word manuscript not rebuilt: Node.js and the 'docx' npm package are needed."
  echo "    Install with:  npm install docx   (inside manuscript/), then:  node manuscript/make_docx.js"
  echo "    The committed manuscript/paper2_v3.docx was built from these same outputs."
fi
