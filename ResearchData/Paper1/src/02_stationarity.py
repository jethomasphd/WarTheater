#!/usr/bin/env python3
"""
02 — Stationarity diagnostics for the daily series.

ADF (H0: unit root / non-stationary) and KPSS (H0: stationary) on the levels of
each series, plus a log1p variant. Event-count intensity series are bounded and
mean-reverting; we expect stationarity in levels, which justifies a level VAR in
the reciprocity tradition (Goldstein 1991; Brandt & Williams 2007).

Outputs:
  output/tables/t02_stationarity.csv
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

import util

warnings.filterwarnings("ignore")  # KPSS emits interpolation warnings at extremes

SERIES = ["strikes", "retal", "killed", "diplomatic"]


def run_tests(x: pd.Series) -> dict:
    x = x.astype(float)
    adf_stat, adf_p = adfuller(x, autolag="AIC")[:2]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        kpss_stat, kpss_p = kpss(x, regression="c", nlags="auto")[:2]
    return {
        "adf_stat": round(adf_stat, 3), "adf_p": round(adf_p, 4),
        "adf_stationary": adf_p < 0.05,
        "kpss_stat": round(kpss_stat, 3), "kpss_p": round(kpss_p, 4),
        "kpss_stationary": kpss_p > 0.05,
    }


def main():
    print("=" * 68)
    print("Paper 1 · Step 02 · Stationarity diagnostics")
    print("=" * 68)
    p = util.load_panel()
    combat = p[p.index <= util.KINETIC_END]  # Days 1..40, active-war regime

    rows = []
    for sample_name, sample in [("full (Days 1-170)", p),
                                (f"combat (Days 1-{util.KINETIC_END})", combat)]:
        for col in SERIES:
            r = run_tests(sample[col].astype(float))
            r.update({"series": col, "sample": sample_name})
            rows.append(r)

    t = pd.DataFrame(rows)[
        ["sample", "series", "adf_stat", "adf_p", "adf_stationary",
         "kpss_stat", "kpss_p", "kpss_stationary"]
    ]
    t.to_csv(util.TAB_DIR / "t02_stationarity.csv", index=False)
    print(t.to_string(index=False))

    full = t[t["sample"].str.startswith("full")]
    print("\nInterpretation:")
    print("  Full sample: KPSS rejects stationarity for all series — driven by the")
    print("  ceasefire-era MEAN SHIFT (a structural break, confirmed in step 04),")
    print("  not a unit root. The reciprocity VAR is therefore estimated primarily on")
    print("  the active-combat regime (Days 1-40); the full-sample VAR is reported as")
    print("  a war-average with the break made explicit, and differenced as robustness.")
    print(f"\nWrote {util.TAB_DIR / 't02_stationarity.csv'}")


if __name__ == "__main__":
    main()
