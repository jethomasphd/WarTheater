#!/usr/bin/env python3
"""
03 — Correlation structure and OLS regression models of daily mortality.

  - Pearson (lower triangle) / Spearman (upper triangle) correlation matrix
  - Lagged cross-correlations: strikes(t-k) -> deaths(t), k = 0..7
  - Hierarchical OLS models with Newey-West (HAC) standard errors
  - Negative-binomial count-model robustness (same specifications)
  - Full-sample and Major-Combat-only estimates

Outputs:
  output/tables/t03_correlations.csv
  output/tables/t03_lagged.csv
  output/tables/t03_ols_models.csv
  output/tables/t03_negbin.csv
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import util

HAC_LAGS = 7   # Newey-West truncation (one week of serial dependence)

CORR_VARS = ["strikes", "retal", "strikes_civfac", "strikes_milfac",
             "health_insults", "hssi_pct", "iran_civ", "iran_mil",
             "leb_all", "killed_total"]


def star(pv):
    return "***" if pv < 0.001 else "**" if pv < 0.01 else "*" if pv < 0.05 else ""


def fit_ols(y, X, label, sample):
    X = sm.add_constant(X)
    m = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    out = []
    for name in m.params.index:
        out.append({
            "model": label, "sample": sample, "term": name,
            "coef": m.params[name], "se_hac": m.bse[name],
            "t": m.tvalues[name], "p": m.pvalues[name],
            "sig": star(m.pvalues[name]),
        })
    out.append({"model": label, "sample": sample, "term": "_R2",
                "coef": m.rsquared, "se_hac": np.nan, "t": np.nan,
                "p": np.nan, "sig": ""})
    out.append({"model": label, "sample": sample, "term": "_adjR2",
                "coef": m.rsquared_adj, "se_hac": np.nan, "t": np.nan,
                "p": np.nan, "sig": ""})
    out.append({"model": label, "sample": sample, "term": "_N",
                "coef": int(m.nobs), "se_hac": np.nan, "t": np.nan,
                "p": np.nan, "sig": ""})
    out.append({"model": label, "sample": sample, "term": "_AIC",
                "coef": m.aic, "se_hac": np.nan, "t": np.nan, "p": np.nan,
                "sig": ""})
    return m, out


def main():
    p = util.load_panel()

    # ---------------- Correlation matrix --------------------------------- #
    k = len(CORR_VARS)
    mat = pd.DataFrame(np.eye(k), index=CORR_VARS, columns=CORR_VARS)
    pmat = pd.DataFrame(np.zeros((k, k)), index=CORR_VARS, columns=CORR_VARS)
    for i, a in enumerate(CORR_VARS):
        for j, b in enumerate(CORR_VARS):
            if i == j:
                continue
            if i > j:      # lower triangle: Pearson
                r, pv = stats.pearsonr(p[a], p[b])
            else:          # upper triangle: Spearman
                r, pv = stats.spearmanr(p[a], p[b])
            mat.iloc[i, j] = r
            pmat.iloc[i, j] = pv
    disp = mat.round(3).astype(str)
    for i in range(k):
        for j in range(k):
            if i != j:
                disp.iloc[i, j] += star(pmat.iloc[i, j])
    disp.to_csv(util.TAB_DIR / "t03_correlations.csv")
    print("t03_correlations (lower=Pearson, upper=Spearman):")
    print(disp.iloc[:6, :6].to_string())

    # ---------------- Lagged cross-correlations --------------------------- #
    rows = []
    for outcome in ("killed_total", "iran_civ", "leb_all"):
        for lag in range(8):
            x = p["strikes"].shift(lag).dropna()
            y = p[outcome].loc[x.index]
            r, pv = stats.pearsonr(x, y)
            rows.append({"outcome": outcome, "lag_days": lag, "pearson_r": r,
                         "p": pv, "sig": star(pv), "n": len(x)})
    t_lag = pd.DataFrame(rows)
    t_lag.round(4).to_csv(util.TAB_DIR / "t03_lagged.csv", index=False)
    best = (t_lag[t_lag.outcome == "killed_total"]
            .sort_values("pearson_r", ascending=False).iloc[0])
    print(f"\nlagged corr (killed_total): peak r={best.pearson_r:.3f} at lag "
          f"{int(best.lag_days)}")

    # ---------------- Hierarchical OLS ------------------------------------ #
    phase_d = pd.get_dummies(p.phase, dtype=float)
    # Reference category: Major Combat.
    phase_cols = [c for c in ["First Ceasefire", "Resumption", "Diplomatic Pause"]
                  if c in phase_d.columns]

    samples = {
        "full": p.index,
        "major_combat": p.index[(p.index >= 1) & (p.index <= 40)],
    }
    all_rows = []
    for sample, idx in samples.items():
        d = p.loc[idx]
        pd_ = phase_d.loc[idx]
        for outcome in ("killed_total", "iran_civ"):
            y = d[outcome].astype(float)
            m1_X = d[["strikes"]].astype(float)
            _, r1 = fit_ols(y, m1_X, f"M1_{outcome}", sample)
            m2_X = d[["strikes", "retal"]].astype(float)
            _, r2 = fit_ols(y, m2_X, f"M2_{outcome}", sample)
            m3_X = d[["strikes_milfac", "strikes_civfac", "retal"]].astype(float)
            _, r3 = fit_ols(y, m3_X, f"M3_{outcome}", sample)
            all_rows.extend(r1 + r2 + r3)
            if sample == "full":
                m4_X = pd.concat([d[["strikes_milfac", "strikes_civfac", "retal"]]
                                  .astype(float), pd_[phase_cols]], axis=1)
                _, r4 = fit_ols(y, m4_X, f"M4_{outcome}", sample)
                all_rows.extend(r4)
    t_ols = pd.DataFrame(all_rows)
    t_ols.round(5).to_csv(util.TAB_DIR / "t03_ols_models.csv", index=False)
    show = t_ols[(t_ols.model == "M3_iran_civ")
                 & (~t_ols.term.str.startswith("_"))]
    print("\nM3 (iran_civ ~ milfac + civfac + retal), HAC SEs:")
    print(show[["sample", "term", "coef", "se_hac", "p", "sig"]]
          .round(4).to_string(index=False))

    # ---------------- Negative-binomial robustness ------------------------ #
    # Daily killed are counts; NB2 with the same specifications guards the
    # OLS results against distributional objections. alpha estimated by MLE.
    nb_rows = []
    for sample, idx in samples.items():
        d = p.loc[idx]
        for outcome in ("killed_total", "iran_civ"):
            y = d[outcome].astype(float)
            X = sm.add_constant(
                d[["strikes_milfac", "strikes_civfac", "retal"]].astype(float))
            try:
                nb = sm.NegativeBinomial(y, X).fit(disp=False, maxiter=200)
                converged = bool(nb.mle_retvals.get("converged", True))
                for name in nb.params.index:
                    nb_rows.append({
                        "sample": sample, "outcome": outcome, "term": name,
                        "coef": nb.params[name], "se": nb.bse[name],
                        "p": nb.pvalues[name], "sig": star(nb.pvalues[name]),
                        "irr": np.exp(nb.params[name]) if name not in ("const", "alpha") else np.nan,
                        "converged": converged, "n": int(nb.nobs),
                    })
            except Exception as e:   # keep the pipeline running; report failure
                nb_rows.append({"sample": sample, "outcome": outcome,
                                "term": f"FIT_FAILED: {e}", "coef": np.nan,
                                "se": np.nan, "p": np.nan, "sig": "",
                                "irr": np.nan, "converged": False, "n": len(y)})
    t_nb = pd.DataFrame(nb_rows)
    t_nb.round(5).to_csv(util.TAB_DIR / "t03_negbin.csv", index=False)
    shown = t_nb[(t_nb["sample"] == "full") & (t_nb.outcome == "iran_civ")]
    print("\nNB2 (full, iran_civ):")
    print(shown[["term", "coef", "p", "sig", "irr"]].round(4).to_string(index=False))

    print("\nwrote t03 tables")


if __name__ == "__main__":
    main()
