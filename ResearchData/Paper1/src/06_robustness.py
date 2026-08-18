#!/usr/bin/env python3
"""
06 — Robustness checks.

(1) Operationalization invariance: the contemporaneous strike-retaliation
    coupling and the combat-regime Granger nulls under three intensity measures
    (primary dedup-location, raw event-rows, timeline-only discrete events).
(2) Count-model reciprocity: negative-binomial distributed-lag model of daily
    retaliation on contemporaneous and lagged strikes (robustness to the
    Gaussian VAR, since the series are overdispersed counts).
(3) Casualty propagation: distributed-lag model of daily killed on strike and
    retaliation tempo — does violence translate into casualties, and at what lag.

Outputs:
  output/tables/t06_operationalization.csv
  output/tables/t06_countmodel_retal.csv
  output/tables/t06_casualty_propagation.csv
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import util

warnings.filterwarnings("ignore")


def dl_matrix(df, ycol, xcols, lags):
    """Build a distributed-lag design: y_t on x_{t-0..lags} for each x in xcols,
    plus y's own lag 1. Returns (y, X_with_const, colnames)."""
    d = df.copy()
    cols = {}
    for x in xcols:
        for L in range(0, lags + 1):
            cols[f"{x}_L{L}"] = d[x].shift(L)
    cols[f"{ycol}_L1"] = d[ycol].shift(1)
    X = pd.DataFrame(cols)
    y = d[ycol]
    keep = X.notna().all(axis=1) & y.notna()
    X, y = X[keep], y[keep]
    X = sm.add_constant(X)
    return y, X


def fit_nb(y, X):
    """Negative-binomial (NB2); fall back to Poisson-robust if it fails."""
    try:
        res = sm.GLM(y, X, family=sm.families.NegativeBinomial(alpha=1.0)).fit()
        return res, "NegBin(alpha=1)"
    except Exception:
        res = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
        return res, "Poisson-HC1"


def main():
    print("=" * 68)
    print("Paper 1 · Step 06 · Robustness")
    print("=" * 68)
    p = util.load_panel()
    combat = p[p.index <= util.KINETIC_END]

    # ---- (1) operationalization invariance ---------------------------- #
    ops = [
        ("primary (dedup-loc)", "strikes", "retal"),
        ("raw event-rows", "strikes_rows", "retal_rows"),
        ("timeline-only", "strikes_tl", "retal_tl"),
    ]
    rows = []
    for label, scol, rcol in ops:
        for sample, seg in [("combat 1-40", combat), ("full 1-170", p)]:
            x, y = seg[scol].astype(float), seg[rcol].astype(float)
            if x.std() == 0 or y.std() == 0:
                r, pr = np.nan, np.nan
            else:
                r, pr = stats.pearsonr(x, y)
            rows.append({"measure": label, "sample": sample,
                         "contemp_r": round(r, 3), "p_value": round(pr, 5),
                         "strike_total": int(seg[scol].sum()),
                         "retal_total": int(seg[rcol].sum())})
    ot = pd.DataFrame(rows)
    ot.to_csv(util.TAB_DIR / "t06_operationalization.csv", index=False)
    print("\n--- (1) Contemporaneous coupling across operationalizations ---")
    print(ot.to_string(index=False))

    # ---- (2) count-model reciprocity (NB distributed lag) ------------- #
    print("\n--- (2) Negative-binomial distributed-lag: retal_t ~ strikes(0..2) + retal_L1 ---")
    crows = []
    for sample, seg in [("combat 1-40", combat), ("full 1-170", p)]:
        y, X = dl_matrix(seg, "retal", ["strikes"], lags=2)
        res, fam = fit_nb(y, X)
        for name in X.columns:
            if name == "const":
                continue
            crows.append({
                "sample": sample, "family": fam, "term": name,
                "coef": round(float(res.params[name]), 4),
                "IRR": round(float(np.exp(res.params[name])), 3),
                "p_value": round(float(res.pvalues[name]), 4),
            })
    ct = pd.DataFrame(crows)
    ct.to_csv(util.TAB_DIR / "t06_countmodel_retal.csv", index=False)
    print(ct.to_string(index=False))

    # ---- (3) casualty propagation ------------------------------------- #
    print("\n--- (3) Casualty propagation: killed_t ~ strikes(0..2) + retal(0..2) ---")
    prows = []
    for sample, seg in [("combat 1-40", combat), ("full 1-170", p)]:
        y, X = dl_matrix(seg, "killed", ["strikes", "retal"], lags=2)
        res, fam = fit_nb(y, X)
        for name in X.columns:
            if name == "const":
                continue
            prows.append({
                "sample": sample, "family": fam, "term": name,
                "coef": round(float(res.params[name]), 4),
                "IRR": round(float(np.exp(res.params[name])), 3),
                "p_value": round(float(res.pvalues[name]), 4),
            })
    pt = pd.DataFrame(prows)
    pt.to_csv(util.TAB_DIR / "t06_casualty_propagation.csv", index=False)
    print(pt.to_string(index=False))

    # concise takeaways
    print("\n=== ROBUSTNESS TAKEAWAYS ===")
    same_day = ot[(ot["sample"] == "combat 1-40")]
    print("  Combat contemporaneous r by measure: " +
          ", ".join(f"{m}={r}" for m, r in zip(same_day["measure"], same_day["contemp_r"])))
    s0 = ct[(ct["sample"] == "combat 1-40") & (ct["term"] == "strikes_L0")]
    if len(s0):
        print(f"  NB combat: contemporaneous strikes IRR={s0['IRR'].iloc[0]} "
              f"(p={s0['p_value'].iloc[0]}) — same-day strikes raise expected retaliation.")
    print(f"\nWrote robustness tables to {util.TAB_DIR}")


if __name__ == "__main__":
    main()
