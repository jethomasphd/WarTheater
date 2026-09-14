#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Paper 1 — Major Revision 1: reproduce the entire analysis from the frozen
# v1.2 dataset, then (if Node and the `docx` package are available) rebuild the
# Word manuscript from the regenerated outputs.
#
#   bash run_all.sh            # analysis + manuscript
#   bash run_all.sh --no-docx  # analysis only
#
# Deterministic: every stochastic step is seeded (SEED = 42). The input file's
# MD5 is verified before anything runs. About three minutes.
# ---------------------------------------------------------------------------
set -euo pipefail

cd "$(dirname "$0")"
export MPLBACKEND=Agg          # headless plotting
export PYTHONHASHSEED=0        # determinism

echo "==> Paper 1 · Major Revision 1: reproducible pipeline"
echo "    dataset: ../../releases/v1.2/iranwar_event_dataset.csv (pinned; md5 verified)"
echo

STEPS=(
  "00_build_panel.py"            # dataset -> data/panel_daily.csv (identity-checked vs parent)
  "01_descriptives.py"           # Figure 1, Table 1
  "02_reciprocity_var.py"        # Finding 1 — same-day, not lagged
  "03_regime_coupling.py"        # Finding 2 — coupling switches with the regime
  "04_identification_fevd.py"    # Finding 3 — who set the tempo is not identified
  "05_asymmetry_spread.py"       # Finding 4 — ratio flip and geographic reach
  "06_diplomacy.py"              # Finding 5 — diplomacy moves at the regime level
  "07_breaks_placebo.py"         # regimes recovered from the data + placebo check
  "08_directional_scoping.py"    # resumption (n = 23) and regime-demeaned re-estimation
  "09_robustness.py"             # stationarity, operationalisations, count models, casualty caveat
  "10_synthesis.py"              # headline numbers verified against the manuscript
)

for step in "${STEPS[@]}"; do
  echo "==> python3 src/${step}"
  ( cd src && python3 "${step}" )
  echo
done

echo "==> Analysis DONE."
echo "    Panel   : data/panel_daily.csv"
echo "    Tables  : output/tables/*.csv   ($(ls output/tables | wc -l | tr -d ' ') files)"
echo "    Figures : output/figures/*.png|pdf ($(ls output/figures | wc -l | tr -d ' ') files)"
echo "    Summary : output/synthesis.json"

if [[ "${1:-}" == "--no-docx" ]]; then
  exit 0
fi

echo
if command -v node >/dev/null 2>&1 && ( cd manuscript && node -e "require('docx')" >/dev/null 2>&1 ); then
  echo "==> node manuscript/make_docx.js"
  ( cd manuscript && node make_docx.js )
else
  echo "==> [skip] Word build: Node.js and the 'docx' package are needed."
  echo "    cd manuscript && npm install && node make_docx.js"
fi
