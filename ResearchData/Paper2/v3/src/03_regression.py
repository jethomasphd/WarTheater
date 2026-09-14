#!/usr/bin/env python3
"""
03 — FINDING 2: as facility damage accumulated, each additional strike was
     associated with more civilian deaths. (Tool: regression with an
     interaction term.)

The question
------------
Did the relationship between strikes and same-day civilian deaths change as
the health system accumulated damage? In regression language: does facility
damage MODERATE the strike-death slope?

The models
----------
All models use Iranian civilian deaths per day as the outcome (Y) and all
170 days.

  Model 1   Y = b0 + b1*strikes
  Model 2   Y = b0 + b1*strikes + b2*damage
  Model 3   Y = b0 + b1*strikes_c + b2*damage_c + b3*(strikes_c x damage_c)

In Model 3 both predictors are mean-centered (the "_c"), which is standard
practice for interaction models: it makes b1 the strike slope at the average
damage level and keeps the predictors from being highly correlated with their
product. The interaction coefficient b3 answers the question: it is the change
in the strike slope for each one-point rise in damage (damage is on a 0-100
scale: percent of the final count of 309 damaged facilities).

Standard errors
---------------
Days in a war are not independent of one another (a bad day tends to follow a
bad day). Ordinary regression standard errors assume independence, so we
report two p-values for every coefficient: the ordinary one, and a
Newey-West (HAC) version that allows for correlation between neighbouring
days (7-day window). The HAC p-values are the ones we quote in the text; the
conclusion is the same under both.

Simple slopes
-------------
The interaction is easiest to read as "the strike slope at chosen levels of
damage". Version 2 of this paper probed at the mean +/- 1 SD, but +1 SD lies
ABOVE the observed maximum (mean 85%, SD 31% -> 116%), so v3 probes at
levels that actually occurred, expressed as facility counts: 31 (the Day-15
figure, 10% of the final count), 155 (half; reached about Day 26), 232
(three-quarters; about Day 33), and 307 (the Day-39 WHO figure, 99% of the
final count; the damage level for every day from Day 39 on). We also report the damage level above which the
slope is statistically significant (the Johnson-Neyman boundary, translated
into a facility count and a day).

Checks
------
  * Strike days only and kinetic days only (drops the quiet days).
  * Major Combat only (Days 1-40): does the pattern hold inside the one phase
    where strikes were sustained and damage was rising?
  * The coarser 21-event stress index (HSSI) as the damage measure.
  * A phase check: does the strike slope simply differ between Major Combat
    and the Resumption? (If the moderation were only "late war is different",
    this interaction would be significant.)

Outputs
-------
  output/tables/t3_models.csv
  output/tables/t3_simple_slopes.csv
  output/tables/t3_robustness.csv
  output/figures/fig3_regression_slopes.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import util

HAC_LAGS = 7
PROBE_COUNTS = [31, 155, 232, 307]   # damaged facilities: Day-15 figure, half, three-quarters, Day-39 WHO figure
PROBE_LEVELS = [100.0 * c / 309 for c in PROBE_COUNTS]   # as percent of the final count (309)


def star(pv):
    return "***" if pv < 0.001 else "**" if pv < 0.01 else "*" if pv < 0.05 else ""


def fit_both(y, X):
    """Fit OLS once with ordinary SEs and once with HAC SEs; return both."""
    Xc = sm.add_constant(X)
    m_ols = sm.OLS(y, Xc).fit()
    m_hac = sm.OLS(y, Xc).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    return m_ols, m_hac


def rows_for(model_name, sample, m_ols, m_hac):
    rows = []
    for term in m_ols.params.index:
        rows.append({"model": model_name, "sample": sample, "term": term,
                     "coef": m_ols.params[term],
                     "se_ols": m_ols.bse[term], "p_ols": m_ols.pvalues[term],
                     "se_hac": m_hac.bse[term], "p_hac": m_hac.pvalues[term],
                     "sig_hac": star(m_hac.pvalues[term])})
    rows.append({"model": model_name, "sample": sample, "term": "_R2",
                 "coef": m_ols.rsquared, "se_ols": np.nan, "p_ols": np.nan,
                 "se_hac": np.nan, "p_hac": np.nan, "sig_hac": ""})
    rows.append({"model": model_name, "sample": sample, "term": "_N",
                 "coef": int(m_ols.nobs), "se_ols": np.nan, "p_ols": np.nan,
                 "se_hac": np.nan, "p_hac": np.nan, "sig_hac": ""})
    return rows


def interaction_design(d, wcol):
    xc = d["strikes"].astype(float) - d["strikes"].astype(float).mean()
    wc = d[wcol].astype(float) - d[wcol].astype(float).mean()
    X = pd.DataFrame({"strikes_c": xc, "damage_c": wc, "strikes_x_damage": xc * wc})
    return X, d[wcol].astype(float).mean()


def slope_at(m, w0_centered):
    """Strike slope and its SE at a centered damage value (from the model's
    coefficient covariance, which is HAC when m is the HAC fit)."""
    V = m.cov_params()
    b1, b3 = m.params["strikes_c"], m.params["strikes_x_damage"]
    s = b1 + b3 * w0_centered
    se = np.sqrt(V.loc["strikes_c", "strikes_c"]
                 + 2 * w0_centered * V.loc["strikes_c", "strikes_x_damage"]
                 + w0_centered ** 2 * V.loc["strikes_x_damage", "strikes_x_damage"])
    t = s / se
    pv = 2 * stats.t.sf(abs(t), int(m.df_resid))
    return s, se, t, pv


def jn_boundary(m, wmin_c, wmax_c):
    """Lowest centered damage value (within the observed range) at which the
    strike slope is significant at alpha = .05 and stays so up to the max."""
    tcrit = stats.t.ppf(0.975, int(m.df_resid))
    ws = np.linspace(wmin_c, wmax_c, 20001)
    tv = np.array([slope_at(m, w)[2] for w in ws])
    sig = tv > tcrit
    if sig.all():
        return wmin_c
    if not sig.any():
        return np.nan
    # first index after which everything is significant
    last_nonsig = np.where(~sig)[0].max()
    return ws[last_nonsig + 1] if last_nonsig + 1 < len(ws) else np.nan


def first_day_at_level(p, level_pct):
    hit = p.index[p.facil_damage_pct >= level_pct - 1e-9]
    return int(hit.min()) if len(hit) else np.nan


def main():
    util.apply_style()
    p = util.load_panel()
    y = p["iran_civ"].astype(float).values
    wmean = p.facil_damage_pct.mean()
    wsd = p.facil_damage_pct.std(ddof=1)
    max_fac = float(p.facil_damage_bench.max())

    # ------------------------------------------------------------------ #
    # Models 1-3 on all days
    # ------------------------------------------------------------------ #
    rows = []
    X1 = pd.DataFrame({"strikes": p.strikes.astype(float)})
    m1o, m1h = fit_both(y, X1)
    rows += rows_for("M1 strikes only", "all days", m1o, m1h)
    X2 = pd.DataFrame({"strikes": p.strikes.astype(float), "damage_pct": p.facil_damage_pct})
    m2o, m2h = fit_both(y, X2)
    rows += rows_for("M2 strikes + damage", "all days", m2o, m2h)
    X3, _ = interaction_design(p, "facil_damage_pct")
    m3o, m3h = fit_both(y, X3)
    rows += rows_for("M3 strikes x damage (interaction)", "all days", m3o, m3h)
    t3 = pd.DataFrame(rows)
    t3.round(5).to_csv(util.TAB_DIR / "t3_models.csv", index=False)

    b3 = m3h.params["strikes_x_damage"]
    print("FINDING 2 — regression with an interaction term (Iranian civilian deaths/day)")
    print(f"  M1: deaths = {m1o.params['const']:.2f} + {m1o.params['strikes']:.2f} x strikes   "
          f"(R2 = {m1o.rsquared:.2f}; HAC p = {m1h.pvalues['strikes']:.4f})")
    print(f"  M2: + damage: strikes b = {m2o.params['strikes']:.2f}, damage b = {m2o.params['damage_pct']:.3f}  (R2 = {m2o.rsquared:.2f})")
    print(f"  M3: interaction b3 = {b3:+.4f} per damage point; ordinary p = {m3o.pvalues['strikes_x_damage']:.4f}, "
          f"HAC p = {m3h.pvalues['strikes_x_damage']:.4f}; R2 = {m3o.rsquared:.2f}; N = {int(m3o.nobs)}")

    # ------------------------------------------------------------------ #
    # Simple slopes at observed damage levels (+ the v2 convention, marked)
    # ------------------------------------------------------------------ #
    srows = []
    for lvl in PROBE_LEVELS:
        s, se, t, pv = slope_at(m3h, lvl - wmean)
        srows.append({"damage_level_pct": lvl,
                      "facilities_damaged": round(lvl / 100 * max_fac),
                      "first_day_at_level": first_day_at_level(p, lvl),
                      "basis": "observed level (v3)",
                      "slope": s, "se_hac": se, "t": t, "p_hac": pv, "sig": star(pv)})
    for label, lvl in (("mean - 1 SD (v2 convention)", wmean - wsd),
                       ("mean (v2 convention)", wmean),
                       ("mean + 1 SD (v2 convention; outside observed range)", wmean + wsd)):
        s, se, t, pv = slope_at(m3h, lvl - wmean)
        srows.append({"damage_level_pct": lvl, "facilities_damaged": round(lvl / 100 * max_fac),
                      "first_day_at_level": first_day_at_level(p, lvl) if lvl <= 100 else np.nan,
                      "basis": label, "slope": s, "se_hac": se, "t": t, "p_hac": pv, "sig": star(pv)})
    jn_c = jn_boundary(m3h, p.facil_damage_pct.min() - wmean, 100.0 - wmean)
    jn_pct = jn_c + wmean if pd.notna(jn_c) else np.nan
    srows.append({"damage_level_pct": jn_pct,
                  "facilities_damaged": round(jn_pct / 100 * max_fac) if pd.notna(jn_pct) else np.nan,
                  "first_day_at_level": first_day_at_level(p, jn_pct) if pd.notna(jn_pct) else np.nan,
                  "basis": "threshold: slope significant (p < .05) at and above this level",
                  "slope": slope_at(m3h, jn_c)[0] if pd.notna(jn_c) else np.nan,
                  "se_hac": np.nan, "t": np.nan, "p_hac": np.nan, "sig": ""})
    ts = pd.DataFrame(srows)
    ts.round(4).to_csv(util.TAB_DIR / "t3_simple_slopes.csv", index=False)
    print("  strike slope (extra civilian deaths per extra strike location) at observed damage levels:")
    for _, r in ts[ts.basis == "observed level (v3)"].iterrows():
        print(f"    damage {r.damage_level_pct:5.1f}% (~{int(r.facilities_damaged):3d} facilities, reached Day {int(r.first_day_at_level):3d}): "
              f"slope = {r.slope:+.2f}  (HAC p = {r.p_hac:.3f} {r.sig})")
    print(f"  slope is significant once damage reaches ~{jn_pct/100*max_fac:.0f} facilities ({jn_pct:.0f}%; Day {first_day_at_level(p, jn_pct)})")
    print(f"  (v2 convention: mean = {wmean:.1f}%, SD = {wsd:.1f}%; mean + 1 SD = {wmean + wsd:.0f}% is outside the observed 0-100 range)")

    # ------------------------------------------------------------------ #
    # Robustness: samples, the HSSI moderator, the phase check
    # ------------------------------------------------------------------ #
    rrows = []

    def add_check(label, d, wcol, note=""):
        Xd, wm = interaction_design(d, wcol)
        yd = d["iran_civ"].astype(float).values
        mo, mh = fit_both(yd, Xd)
        s100 = slope_at(mh, 100.0 - wm)
        s_lo = slope_at(mh, d[wcol].min() - wm)
        rrows.append({"check": label, "moderator": wcol, "n": int(mo.nobs),
                      "interaction_b": mh.params["strikes_x_damage"],
                      "interaction_p_ols": mo.pvalues["strikes_x_damage"],
                      "interaction_p_hac": mh.pvalues["strikes_x_damage"],
                      "slope_at_min_damage": s_lo[0], "slope_at_min_p_hac": s_lo[3],
                      "slope_at_100pct_damage": s100[0], "slope_at_100pct_p_hac": s100[3],
                      "r_squared": mo.rsquared, "note": note})

    add_check("primary: all days", p, "facil_damage_pct")
    add_check("strike days only", p[p.strike_day == 1], "facil_damage_pct")
    add_check("kinetic days only (strikes or retaliation)", p[p.kinetic_day == 1], "facil_damage_pct")
    add_check("Major Combat only (Days 1-40)", p.loc[1:40], "facil_damage_pct",
              "the one phase with sustained strikes and rising damage")
    add_check("Days 1-60", p.loc[1:60], "facil_damage_pct")
    add_check("HSSI (21-event index) as the damage measure", p, "hssi_pct",
              "coarser measure; same direction, interaction not significant")
    add_check("HSSI, strike days only", p[p.strike_day == 1], "hssi_pct")

    # Phase check: strikes x Resumption dummy, Major Combat + Resumption days.
    d = p[(p.phase == "Major Combat") | (p.phase == "Resumption")]
    yd = d["iran_civ"].astype(float).values
    res = (d.phase == "Resumption").astype(float)
    xc = d["strikes"].astype(float) - d["strikes"].astype(float).mean()
    Xp = pd.DataFrame({"strikes_c": xc, "resumption": res, "strikes_x_resumption": xc * res})
    po, ph = fit_both(yd, Xp)
    rrows.append({"check": "phase check: strikes x Resumption (Major Combat + Resumption days)",
                  "moderator": "phase (Resumption = 1)", "n": int(po.nobs),
                  "interaction_b": ph.params["strikes_x_resumption"],
                  "interaction_p_ols": po.pvalues["strikes_x_resumption"],
                  "interaction_p_hac": ph.pvalues["strikes_x_resumption"],
                  "slope_at_min_damage": ph.params["strikes_c"], "slope_at_min_p_hac": ph.pvalues["strikes_c"],
                  "slope_at_100pct_damage": ph.params["strikes_c"] + ph.params["strikes_x_resumption"],
                  "slope_at_100pct_p_hac": np.nan, "r_squared": po.rsquared,
                  "note": f"Resumption baseline lower by {ph.params['resumption']:.1f} deaths/day (HAC p = {ph.pvalues['resumption']:.4f}); "
                          "slope columns = Major Combat slope and Resumption slope"})
    tr = pd.DataFrame(rrows)
    tr.round(5).to_csv(util.TAB_DIR / "t3_robustness.csv", index=False)
    print("\n  checks (interaction coefficient; HAC p; ordinary p):")
    for _, r in tr.iterrows():
        print(f"    {r.check:66s} b = {r.interaction_b:+.4f}  HAC p = {r.interaction_p_hac:.3f}  OLS p = {r.interaction_p_ols:.3f}  n = {r.n}")

    # ------------------------------------------------------------------ #
    # Figure 3
    # ------------------------------------------------------------------ #
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    ax = axes[0]
    xs = np.linspace(0, p.strikes.max(), 100)
    xs_c = xs - p.strikes.mean()
    line_cols = dict(zip(PROBE_LEVELS, [util.C_SKY, util.C_STRIKE, util.C_ACCENT, util.C_RETAL]))
    for lvl in PROBE_LEVELS:
        w0 = lvl - wmean
        yhat = (m3h.params["const"] + m3h.params["strikes_c"] * xs_c
                + m3h.params["damage_c"] * w0 + m3h.params["strikes_x_damage"] * xs_c * w0)
        s = slope_at(m3h, w0)[0]
        ax.plot(xs, yhat, lw=2.1, color=line_cols[lvl],
                label=f"{lvl/100*max_fac:.0f} facilities damaged ({lvl:.0f}%): slope {s:+.2f}")
    per_col = np.where(p.index <= 15, util.C_SKY, np.where(p.index <= 39, util.C_STRIKE, util.C_RETAL))
    ax.scatter(p.strikes, p.iran_civ, s=13, alpha=0.4, c=per_col, linewidth=0)
    ax.axhline(0, color="0.5", lw=0.6)
    ax.set_xlabel("Strike locations per day")
    ax.set_ylabel("Iranian civilian deaths per day")
    ax.set_title("A. The strike–death slope at four levels of facility damage",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=7.4, title="Model 3 prediction with:", title_fontsize=7.6, loc="upper right")

    ax = axes[1]
    util.shade_phases(ax)
    ax.plot(p.index, p.facil_damage_pct, color=util.C_RETAL, lw=2.0,
            label="Facility damage (benchmark curve: 31 → 307 → 309)")
    ax.plot(p.index, p.hssi_pct, color=util.C_HEALTH, lw=1.5, ls="--",
            label="HSSI (21 audited health-system events)")
    for lvl in PROBE_LEVELS:
        dday = first_day_at_level(p, lvl)
        ax.scatter([dday], [lvl], s=42, zorder=6, color=line_cols[lvl], edgecolor="white", linewidth=0.8)
        ax.annotate(f"{lvl/100*max_fac:.0f} facilities by Day {dday}", (dday, lvl), textcoords="offset points",
                    xytext=(8, -3 if lvl < 90 else -13), fontsize=7.6, color="0.25")
    ax.set_xlabel("Day of the war")
    ax.set_ylabel("Accumulated damage (% of the Day-170 level)")
    ax.set_title("B. When each damage level was reached", loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=7.6, loc="lower right")
    ax.set_xlim(0, 171)
    ax.set_ylim(-3, 108)
    util.savefig(fig, "fig3_regression_slopes")
    plt.close(fig)
    print("\nwrote t3 tables + fig3_regression_slopes")


if __name__ == "__main__":
    main()
