#!/usr/bin/env python3
"""
09 — Robustness.

(1) Stationarity: ADF and KPSS on levels, full sample and combat regime. The full-sample
    KPSS rejections reflect the regime mean shifts (step 07), not a unit root, which is why
    the primary reciprocity model is estimated within the combat regime.
(2) Operationalisation invariance: the same-day coupling under three intensity measures.
(3) Count models: negative-binomial distributed-lag model of daily retaliation on same-day
    and lagged strikes (guards against the Gaussian VAR approximation for over-dispersed
    counts).
(4) Casualty caveat: daily deaths do not track daily tempo; tempo is not a lethality proxy.

Outputs
  output/tables/t09_stationarity.csv
  output/tables/t09_operationalization.csv
  output/tables/t09_countmodel_retal.csv
  output/tables/t09_casualty_propagation.csv
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss

import util

warnings.filterwarnings("ignore")


def unit_root_tests(x):
    x = x.astype(float)
    adf_stat, adf_p = adfuller(x, autolag="AIC")[:2]
    kpss_stat, kpss_p = kpss(x, regression="c", nlags="auto")[:2]
    return {"adf_stat": round(adf_stat, 3), "adf_p": round(adf_p, 4),
            "adf_rejects_unit_root": adf_p < 0.05,
            "kpss_stat": round(kpss_stat, 3), "kpss_p": round(kpss_p, 4),
            "kpss_rejects_stationarity": kpss_p < 0.05}


def dl_matrix(df, ycol, xcols, lags):
    cols = {}
    for x in xcols:
        for L in range(0, lags + 1):
            cols[f"{x}_L{L}"] = df[x].shift(L)
    cols[f"{ycol}_L1"] = df[ycol].shift(1)
    X = pd.DataFrame(cols); y = df[ycol]
    keep = X.notna().all(axis=1) & y.notna()
    return y[keep], sm.add_constant(X[keep])


def fit_nb(y, X):
    try:
        return sm.GLM(y, X, family=sm.families.NegativeBinomial(alpha=1.0)).fit(), "NegBin(alpha=1)"
    except Exception:
        return sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1"), "Poisson-HC1"


def coef_rows(res, fam, sample, X):
    out = []
    for name in X.columns:
        if name == "const":
            continue
        out.append({"sample": sample, "family": fam, "term": name,
                    "coef": round(float(res.params[name]), 4),
                    "IRR": round(float(np.exp(res.params[name])), 3),
                    "p_value": round(float(res.pvalues[name]), 4)})
    return out


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 09 · Robustness")
    print("=" * 70)
    p = util.load_panel()
    combat = p[p.index <= util.KINETIC_END]

    rows = []
    for sample, seg in [("full (Days 1-170)", p), ("combat (Days 1-40)", combat)]:
        for col in ["strikes", "retal", "diplomatic"]:
            rows.append({"sample": sample, "series": col, **unit_root_tests(seg[col])})
    st = pd.DataFrame(rows)
    print("\n--- (1) Stationarity ---")
    print(st.to_string(index=False))
    util.write_table(st, "t09_stationarity.csv")

    ops = [("primary (distinct locations)", "strikes", "retal"),
           ("raw event rows", "strikes_rows", "retal_rows"),
           ("timeline-only discrete events", "strikes_tl", "retal_tl")]
    rows = []
    for label, sc, rc in ops:
        for sample, seg in [("combat (Days 1-40)", combat), ("full (Days 1-170)", p)]:
            x, y = seg[sc].astype(float), seg[rc].astype(float)
            r, pr = stats.pearsonr(x, y)
            rows.append({"measure": label, "sample": sample, "same_day_r": round(r, 3),
                         "p_value": float(f"{pr:.2e}"), "strike_total": int(x.sum()),
                         "retal_total": int(y.sum())})
    ot = pd.DataFrame(rows)
    print("\n--- (2) Same-day coupling across operationalisations ---")
    print(ot.to_string(index=False))
    util.write_table(ot, "t09_operationalization.csv")

    crows, prows = [], []
    for sample, seg in [("combat (Days 1-40)", combat), ("full (Days 1-170)", p)]:
        y, X = dl_matrix(seg, "retal", ["strikes"], lags=2)
        res, fam = fit_nb(y, X); crows += coef_rows(res, fam, sample, X)
        y, X = dl_matrix(seg, "killed", ["strikes", "retal"], lags=2)
        res, fam = fit_nb(y, X); prows += coef_rows(res, fam, sample, X)
    ct = pd.DataFrame(crows); pt = pd.DataFrame(prows)
    print("\n--- (3) Negative-binomial: retal_t ~ strikes(0..2) + retal_L1 ---")
    print(ct.to_string(index=False))
    util.write_table(ct, "t09_countmodel_retal.csv")
    print("\n--- (4) Casualty propagation: killed_t ~ strikes(0..2) + retal(0..2) + killed_L1 ---")
    print(pt.to_string(index=False))
    util.write_table(pt, "t09_casualty_propagation.csv")


if __name__ == "__main__":
    main()
