#!/usr/bin/env python3
"""
02 — FINDING 5: the health system gradually lost its ability to absorb shocks.

The student's second finding, in her words: "each strike became more deadly as
the health system absorbed more damage. That is resilience erosion in numbers.
A functioning hospital can absorb one bad night, but after enough bad nights,
it cannot absorb much more."

We translate that clinical intuition into an interaction model. If the same
kinetic dose converts to more deaths once trauma-care capacity has been
degraded (Kruk et al.'s resilience-erosion prediction), the slope of deaths on
strikes should STEEPEN as accumulated facility damage rises:

    Y = b0 + b1*X_c + b2*W_c + b3*(X_c * W_c) + e     (HAC/Newey-West SEs)
      Y = iran_civ ;  X = strikes (centered) ;  W = degradation (centered)

W is operationalized two ways, exactly as in the parent paper:
  * facil_damage_pct  — the benchmark-anchored facility-damage curve
                        (31 -> 307 -> 309 facilities; the primary moderator)
  * hssi_pct          — the 21-event audited insult index (coarser sensitivity)

Reported: the interaction term, simple slopes of Y on strikes at W = mean +/-
1 SD, the Johnson-Neyman boundary, a phase-interaction check (does the pattern
just track a generic late-war regime shift?), and a kinetic-days-only
sensitivity. All computations are identical to parent script 05.

Outputs:
  output/tables/t5_moderation.csv
  output/tables/t5_simple_slopes.csv
  output/figures/fig2_resilience_erosion.(png|pdf)
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
    for wcol in ("facil_damage_pct", "hssi_pct"):
        for sample, d in (("full", p), ("kinetic_days", kinetic)):
            m, X, rows = fit_interaction(d, wcol, sample)
            mod_rows.extend(rows)
            slope_rows.extend(simple_slopes(m, X, d, wcol, sample))
            models[(wcol, sample)] = (m, X, d)

    # Phase-interaction variant: does per-strike lethality differ at the
    # Resumption relative to Major Combat? If the moderation were just a
    # generic late-war regime shift, this interaction would be significant.
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

    t5 = pd.DataFrame(mod_rows)
    t5.round(5).to_csv(util.TAB_DIR / "t5_moderation.csv", index=False)
    t5s = pd.DataFrame(slope_rows)
    t5s.round(5).to_csv(util.TAB_DIR / "t5_simple_slopes.csv", index=False)

    # ---- console summary: the headline (facility-damage) moderator -------- #
    inter = t5[(t5.moderator == "facil_damage_pct") & (t5["sample"] == "full")
               & (t5.term == "strikes_x_W")].iloc[0]
    ss = t5s[(t5s.moderator == "facil_damage_pct") & (t5s["sample"] == "full")
             & (t5s.at_W != "JN_boundary")]
    print("FINDING 5 — resilience erosion (facility-damage moderator, full sample)")
    print(f"  strikes x damage interaction: b3 = {inter.coef:.4f}, "
          f"HAC p = {inter.p:.3f} {inter.sig}")
    print("  simple slope of deaths on strikes, by accumulated facility damage:")
    for _, r in ss.iterrows():
        print(f"    at {r.at_W:>4} damage:  slope = {r.slope:.2f}  (p = {r.p:.3f} {r.sig})")
    lo, hi = ss.iloc[0].slope, ss.iloc[-1].slope
    print(f"  -> a {hi / lo:.1f}x steepening across the observed damage range")
    hss = t5[(t5.moderator == "hssi_pct") & (t5["sample"] == "full")
             & (t5.term == "strikes_x_W")].iloc[0]
    print(f"  sensitivity (21-event HSSI moderator): same direction, "
          f"b3 = {hss.coef:.4f}, p = {hss.p:.2f} {hss.sig or '(n.s.)'}")

    # ==================================================================== #
    # Figure 2 — simple slopes (primary moderator) + the degradation curves
    # ==================================================================== #
    m, X, d = models[("facil_damage_pct", "full")]
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

    ax = axes[0]
    wvals = X["W_c"]
    sdw = wvals.std(ddof=1)
    xs = np.linspace(0, d["strikes"].max(), 100)
    xs_c = xs - d["strikes"].mean()
    labels = {"-1SD": "Low damage (early war)", "mean": "Mean damage",
              "+1SD": "High damage (late war)"}
    colors = {"-1SD": util.C_SKY, "mean": util.C_STRIKE, "+1SD": util.C_RETAL}
    for label, w0 in [("-1SD", -sdw), ("mean", 0.0), ("+1SD", sdw)]:
        yhat = (m.params["const"] + m.params["strikes_c"] * xs_c
                + m.params["W_c"] * w0 + m.params["strikes_x_W"] * xs_c * w0)
        ax.plot(xs, yhat, lw=2.2, color=colors[label], label=labels[label])
    terc = pd.qcut(d["facil_damage_pct"], 3, labels=["low", "mid", "high"],
                   duplicates="drop")
    cmap = {"low": util.C_SKY, "mid": util.C_STRIKE, "high": util.C_RETAL}
    for t_lab, grp in d.groupby(terc, observed=True):
        ax.scatter(grp.strikes, grp.iran_civ, s=13, alpha=0.4,
                   color=cmap[str(t_lab)], linewidth=0)
    ax.set_xlabel("Strike locations per day")
    ax.set_ylabel("Iranian civilian deaths per day")
    ax.set_title("A. The same strike, made deadlier by a degraded system",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=8, title="Slope of deaths on strikes at:",
              title_fontsize=8)

    ax = axes[1]
    util.shade_phases(ax)
    ax.plot(p.index, p.facil_damage_pct, color=util.C_RETAL, lw=2.0,
            label="Facility damage (WHO/ministry benchmarks)")
    ax.plot(p.index, p.hssi_pct, color=util.C_HEALTH, lw=1.6, ls="--",
            label="HSSI (21 audited insults)")
    ax.set_xlabel("Day of conflict")
    ax.set_ylabel("Accumulated degradation (% of Day-170 level)")
    ax.set_title("B. How far the buffer had eroded, day by day",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=8, loc="lower right")
    ax.set_xlim(0, 171)
    util.savefig(fig, "fig2_resilience_erosion")
    plt.close(fig)

    print("\nwrote t5 tables + fig2_resilience_erosion")


if __name__ == "__main__":
    main()
