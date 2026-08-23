#!/usr/bin/env python3
"""
05 — Moderation: does accumulated health-system degradation change the
per-strike mortality relationship?

Competing hypotheses (both grounded in the conflict-health literature):
  H4a (resilience erosion, Kruk et al.): as the health system degrades,
      the same kinetic dose kills MORE (positive strikes x degradation
      interaction) — casualty survival depends on intact trauma care.
  H4b (harm front-loading / adaptation): early strikes are the deadliest
      (unprepared population, intact high-value target set); populations
      shelter, flee, and adapt, so per-strike DIRECT lethality falls
      (negative interaction). Indirect mortality is NOT observable in the
      daily direct-death series — see 06.

Model:  Y = b0 + b1*X_c + b2*W_c + b3*(X_c*W_c) + e     (HAC SEs)
  Y = iran_civ;  X = strikes (centered);  W = degradation (centered),
  operationalized two ways: hssi_pct (audited insult count) and
  facil_damage_pct (benchmark-anchored facility damage).

Simple slopes at W = mean ± 1 SD, Johnson-Neyman boundary, phase-interaction
variant (strikes x Resumption), and a kinetic-days-only sensitivity.

Outputs:
  output/tables/t05_moderation.csv
  output/tables/t05_simple_slopes.csv
  output/figures/fig6_moderation.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import util

HAC_LAGS = 7


def star(pv):
    return "***" if pv < 0.001 else "**" if pv < 0.01 else "*" if pv < 0.05 else ""


def fit_interaction(d, wcol, sample, outcome="iran_civ"):
    y = d[outcome].astype(float).values
    xc = d["strikes"].astype(float) - d["strikes"].astype(float).mean()
    wc = d[wcol].astype(float) - d[wcol].astype(float).mean()
    X = pd.DataFrame({"strikes_c": xc, "W_c": wc, "strikes_x_W": xc * wc})
    m = sm.OLS(y, sm.add_constant(X)).fit(cov_type="HAC",
                                          cov_kwds={"maxlags": HAC_LAGS})
    rows = []
    for name in m.params.index:
        rows.append({"moderator": wcol, "sample": sample, "outcome": outcome,
                     "term": name, "coef": m.params[name], "se_hac": m.bse[name],
                     "t": m.tvalues[name], "p": m.pvalues[name],
                     "sig": star(m.pvalues[name])})
    rows.append({"moderator": wcol, "sample": sample, "outcome": outcome,
                 "term": "_R2", "coef": m.rsquared, "se_hac": np.nan,
                 "t": np.nan, "p": np.nan, "sig": ""})
    rows.append({"moderator": wcol, "sample": sample, "outcome": outcome,
                 "term": "_N", "coef": int(m.nobs), "se_hac": np.nan,
                 "t": np.nan, "p": np.nan, "sig": ""})
    return m, X, rows


def simple_slopes(m, X, d, wcol, sample):
    """Slope of Y on strikes at W = mean -1SD / mean / mean +1SD (HAC vcov),
    plus the Johnson-Neyman boundary in centered-W units."""
    b1 = m.params["strikes_c"]
    b3 = m.params["strikes_x_W"]
    V = m.cov_params()
    sdw = X["W_c"].std(ddof=1)
    out = []
    for label, w0 in [("-1SD", -sdw), ("mean", 0.0), ("+1SD", sdw)]:
        slope = b1 + b3 * w0
        se = np.sqrt(V.loc["strikes_c", "strikes_c"]
                     + 2 * w0 * V.loc["strikes_c", "strikes_x_W"]
                     + w0 ** 2 * V.loc["strikes_x_W", "strikes_x_W"])
        t = slope / se
        pv = 2 * stats.t.sf(abs(t), int(m.df_resid))
        out.append({"moderator": wcol, "sample": sample, "at_W": label,
                    "W_centered": w0, "slope": slope, "se": se, "t": t,
                    "p": pv, "sig": star(pv)})

    # Johnson-Neyman: W where the strikes slope's |t| crosses the critical t.
    tcrit = stats.t.ppf(0.975, int(m.df_resid))
    ws = np.linspace(X["W_c"].min(), X["W_c"].max(), 4001)
    se_w = np.sqrt(V.loc["strikes_c", "strikes_c"]
                   + 2 * ws * V.loc["strikes_c", "strikes_x_W"]
                   + ws ** 2 * V.loc["strikes_x_W", "strikes_x_W"])
    tvals = (b1 + b3 * ws) / se_w
    sig_mask = np.abs(tvals) > tcrit
    jn = "none (significant everywhere)" if sig_mask.all() else \
         "none (significant nowhere)" if not sig_mask.any() else \
         f"crossing near W_c = {ws[np.where(np.diff(sig_mask))[0]].round(2).tolist()}"
    out.append({"moderator": wcol, "sample": sample, "at_W": "JN_boundary",
                "W_centered": np.nan, "slope": np.nan, "se": np.nan,
                "t": np.nan, "p": np.nan, "sig": jn})
    return out


def main():
    util.apply_style()
    p = util.load_panel()
    kinetic = p[p.kinetic_day == 1]

    mod_rows, slope_rows = [], []
    models = {}
    for wcol in ("hssi_pct", "facil_damage_pct"):
        for sample, d in (("full", p), ("kinetic_days", kinetic)):
            m, X, rows = fit_interaction(d, wcol, sample)
            mod_rows.extend(rows)
            slope_rows.extend(simple_slopes(m, X, d, wcol, sample))
            models[(wcol, sample)] = (m, X, d)

    # Phase-interaction variant: does per-strike lethality differ at the
    # Resumption relative to Major Combat? (kinetic Iran-front phases only)
    d = p[(p.phase == "Major Combat") | (p.phase == "Resumption")]
    y = d["iran_civ"].astype(float).values
    res = (d.phase == "Resumption").astype(float)
    xc = d["strikes"].astype(float) - d["strikes"].astype(float).mean()
    X = pd.DataFrame({"strikes_c": xc, "resumption": res,
                      "strikes_x_resumption": xc * res})
    m = sm.OLS(y, sm.add_constant(X)).fit(cov_type="HAC",
                                          cov_kwds={"maxlags": HAC_LAGS})
    for name in m.params.index:
        mod_rows.append({"moderator": "phase(Resumption)", "sample": "combat+resumption",
                         "outcome": "iran_civ", "term": name,
                         "coef": m.params[name], "se_hac": m.bse[name],
                         "t": m.tvalues[name], "p": m.pvalues[name],
                         "sig": star(m.pvalues[name])})
    mod_rows.append({"moderator": "phase(Resumption)", "sample": "combat+resumption",
                     "outcome": "iran_civ", "term": "_N", "coef": int(m.nobs),
                     "se_hac": np.nan, "t": np.nan, "p": np.nan, "sig": ""})

    t05 = pd.DataFrame(mod_rows)
    t05.round(5).to_csv(util.TAB_DIR / "t05_moderation.csv", index=False)
    t05s = pd.DataFrame(slope_rows)
    t05s.round(5).to_csv(util.TAB_DIR / "t05_simple_slopes.csv", index=False)

    hh = t05[(t05.moderator == "hssi_pct") & (t05["sample"] == "full")
             & (~t05.term.str.startswith("_"))]
    print("moderation (hssi_pct, full):")
    print(hh[["term", "coef", "se_hac", "p", "sig"]].round(4).to_string(index=False))
    ss = t05s[(t05s.moderator == "hssi_pct") & (t05s["sample"] == "full")]
    print("\nsimple slopes (hssi_pct, full):")
    print(ss[["at_W", "slope", "se", "p", "sig"]].to_string(index=False))

    # ---------------- Figure 6: simple-slopes plot ------------------------ #
    m, X, d = models[("hssi_pct", "full")]
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.3))

    ax = axes[0]
    wvals = X["W_c"]
    sdw = wvals.std(ddof=1)
    xs = np.linspace(0, d["strikes"].max(), 100)
    xs_c = xs - d["strikes"].mean()
    colors = {"-1SD": util.C_SKY, "mean": util.C_STRIKE, "+1SD": util.C_RETAL}
    for label, w0 in [("-1SD", -sdw), ("mean", 0.0), ("+1SD", sdw)]:
        yhat = (m.params["const"] + m.params["strikes_c"] * xs_c
                + m.params["W_c"] * w0 + m.params["strikes_x_W"] * xs_c * w0)
        ax.plot(xs, yhat, lw=2.0, color=colors[label],
                label=f"Degradation at {label}")
    # observed points, colored by degradation tercile
    terc = pd.qcut(d["hssi_pct"], 3, labels=["low", "mid", "high"], duplicates="drop")
    cmap = {"low": util.C_SKY, "mid": util.C_STRIKE, "high": util.C_RETAL}
    for t_lab, grp in d.groupby(terc, observed=True):
        ax.scatter(grp.strikes, grp.iran_civ, s=13, alpha=0.4,
                   color=cmap[str(t_lab)], linewidth=0)
    ax.set_xlabel("Strike locations per day")
    ax.set_ylabel("Iranian civilian killed per day")
    ax.set_title("A. Simple slopes: strikes × health-system degradation",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=8)

    ax = axes[1]
    util.shade_phases(ax)
    ax.plot(p.index, p.hssi_pct, color=util.C_HEALTH, lw=1.8,
            label="HSSI (audited insults, %)")
    ax.plot(p.index, p.facil_damage_pct, color=util.C_RETAL, lw=1.6, ls="--",
            label="Facility damage (benchmarks, %)")
    ax.set_xlabel("Day of conflict")
    ax.set_ylabel("Degradation (% of Day-170 level)")
    ax.set_title("B. The two degradation operationalizations",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_xlim(0, 171)
    util.savefig(fig, "fig6_moderation")
    plt.close(fig)

    print("\nwrote t05 tables + fig6")


if __name__ == "__main__":
    main()
