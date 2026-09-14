#!/usr/bin/env python3
"""
02 — BRIDGE TO FINDING 2: did strikes and deaths move together more closely
     as facility damage accumulated? (Tool: correlation.)

The question
------------
On a day with more strikes, were there more Iranian civilian deaths? And did
that relationship change as the health system accumulated damage?

What we correlate
-----------------
Strike tempo (distinct strike locations per day) and Iranian civilian deaths
per day. We compute the Pearson correlation r, and the slope of a simple
regression of deaths on strikes, separately within three periods defined by
the facility-damage curve (the curve is anchored to institutional reports:
31 damaged facilities by Day 15, 307 by Day 39, 309 by Day 170):

  Period A  Days 1-15    damage rising from 0 to 31 facilities (10% of final)
  Period B  Days 16-39   damage rising from 31 to 307 facilities (10% -> 99%)
  Period C  Days 40-170  damage at 307-309 facilities (about 100%)

We also report the Resumption (Days 130-152, inside Period C, the only late
period with sustained strikes), all 170 days, and a strike-days-only version
of every row. Spearman's rho is included as a rank-based check because daily
death counts are skewed. Fisher's r-to-z test compares the correlations
between periods.

Why this step exists
--------------------
It is the plain version of the regression in script 03. If the correlation
is near zero early and clearly positive later, then the interaction term in
script 03 is describing something you can already see in a scatter plot.

Outputs
-------
  output/tables/t2_correlation_by_period.csv
  output/tables/t2_correlation_comparison.csv
  output/figures/fig2_correlation_by_period.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import util

PERIODS = [
    ("A", "Days 1-15: damage 0 -> 31 facilities (<=10% of final)", 1, 15),
    ("B", "Days 16-39: damage 31 -> 307 facilities (10% -> 99%)", 16, 39),
    ("C", "Days 40-170: damage 307 -> 309 facilities (about 100%)", 40, 170),
    ("C-resumption", "Days 130-152 (Resumption; inside period C)", 130, 152),
    ("all", "All days 1-170", 1, 170),
]


def corr_row(d, period, label, sample):
    x = d.strikes.astype(float).values
    y = d.iran_civ.astype(float).values
    row = {"period": period, "label": label, "sample": sample, "n_days": len(d),
           "n_strike_days": int((d.strikes > 0).sum()),
           "strikes_per_day": x.mean(), "civ_deaths_per_day": y.mean(),
           "civ_deaths_per_strike_location": (y.sum() / x.sum()) if x.sum() else np.nan,
           "damage_pct_mean": d.facil_damage_pct.mean()}
    if len(d) < 3 or x.var() == 0 or y.var() == 0:
        row.update({"pearson_r": np.nan, "pearson_p": np.nan, "spearman_rho": np.nan,
                    "spearman_p": np.nan, "slope": np.nan, "slope_se": np.nan,
                    "slope_ci95_low": np.nan, "slope_ci95_high": np.nan, "slope_p": np.nan,
                    "intercept": np.nan, "r_squared": np.nan,
                    "note": "not defined: no variation in strikes or deaths"})
        return row
    r, pr = stats.pearsonr(x, y)
    rho, prho = stats.spearmanr(x, y)
    lr = stats.linregress(x, y)
    tcrit = stats.t.ppf(0.975, len(d) - 2)
    row.update({"pearson_r": r, "pearson_p": pr, "spearman_rho": rho, "spearman_p": prho,
                "slope": lr.slope, "slope_se": lr.stderr,
                "slope_ci95_low": lr.slope - tcrit * lr.stderr,
                "slope_ci95_high": lr.slope + tcrit * lr.stderr,
                "slope_p": lr.pvalue, "intercept": lr.intercept, "r_squared": r ** 2,
                "note": ""})
    return row


def fisher_z_compare(r1, n1, r2, n2):
    """Two-sided test that two independent correlations are equal."""
    z1, z2 = np.arctanh(r1), np.arctanh(r2)
    se = np.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
    z = (z1 - z2) / se
    return z, 2 * stats.norm.sf(abs(z))


def main():
    util.apply_style()
    p = util.load_panel()

    rows = []
    for period, label, lo, hi in PERIODS:
        d = p.loc[lo:hi]
        rows.append(corr_row(d, period, label, "all days in period"))
        rows.append(corr_row(d[d.strike_day == 1], period, label, "strike days only"))
    t2 = pd.DataFrame(rows)
    t2.round(4).to_csv(util.TAB_DIR / "t2_correlation_by_period.csv", index=False)

    print("BRIDGE — correlation of strikes with Iranian civilian deaths, by damage period")
    show = t2[t2["sample"] == "all days in period"]
    for _, r in show.iterrows():
        rs = f"r = {r.pearson_r:+.2f} (p = {r.pearson_p:.3f})" if pd.notna(r.pearson_r) else "r not defined"
        print(f"  {r.label:58s} n={r.n_days:3d}  {rs}  slope = {r.slope:+.2f}")

    # Compare correlations between periods (Fisher's z).
    comp_rows = []
    get = lambda per, samp: t2[(t2.period == per) & (t2["sample"] == samp)].iloc[0]
    for samp in ("all days in period", "strike days only"):
        for a, b in (("A", "C"), ("A", "B"), ("B", "C"), ("A", "C-resumption")):
            ra, rb = get(a, samp), get(b, samp)
            if pd.isna(ra.pearson_r) or pd.isna(rb.pearson_r):
                continue
            z, pz = fisher_z_compare(ra.pearson_r, ra.n_days, rb.pearson_r, rb.n_days)
            comp_rows.append({"sample": samp, "period_1": a, "r_1": ra.pearson_r, "n_1": ra.n_days,
                              "period_2": b, "r_2": rb.pearson_r, "n_2": rb.n_days,
                              "fisher_z": z, "p": pz})
    tc = pd.DataFrame(comp_rows)
    tc.round(4).to_csv(util.TAB_DIR / "t2_correlation_comparison.csv", index=False)
    print("\n  are the correlations different? (Fisher r-to-z, all days in period)")
    for _, r in tc[tc["sample"] == "all days in period"].iterrows():
        print(f"    {r.period_1} (r={r.r_1:+.2f}, n={r.n_1}) vs {r.period_2} (r={r.r_2:+.2f}, n={r.n_2}): "
              f"z = {r.fisher_z:.2f}, p = {r.p:.3f}")

    # ------------------------------------------------------------------ #
    # Figure 2 — three scatter panels
    # ------------------------------------------------------------------ #
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.0), sharey=True)
    colors = {"A": util.C_SKY, "B": util.C_STRIKE, "C": util.C_RETAL}
    titles = {"A": "A. Days 1–15 (damage ≤ 10% of final)",
              "B": "B. Days 16–39 (damage 10% → 99%)",
              "C": "C. Days 40–170 (damage ≈ 100%)"}
    for ax, per in zip(axes, ("A", "B", "C")):
        _, _, lo, hi = [x for x in PERIODS if x[0] == per][0]
        d = p.loc[lo:hi]
        r = get(per, "all days in period")
        ax.scatter(d.strikes, d.iran_civ, s=22, alpha=0.65, color=colors[per], linewidth=0)
        xs = np.linspace(0, max(d.strikes.max(), 1), 50)
        ax.plot(xs, r.intercept + r.slope * xs, color="0.2", lw=1.8)
        ax.set_title(titles[per] + f"\nr = {r.pearson_r:+.2f} (p = {r.pearson_p:.3f}); "
                     f"slope = {r.slope:+.2f}; n = {r.n_days} days",
                     loc="left", fontweight="bold", fontsize=8.6)
        ax.set_xlabel("Strike locations per day")
    axes[0].set_ylabel("Iranian civilian deaths per day")
    fig.text(0.5, -0.03,
             "Each dot is one day. The line is the simple regression of deaths on strikes within the period; its slope is extra deaths per extra strike location. "
             "Periods follow the benchmark facility-damage curve (31 facilities by Day 15; 307 by Day 39; 309 by Day 170).",
             ha="center", fontsize=7.4, color="0.25")
    util.savefig(fig, "fig2_correlation_by_period")
    plt.close(fig)
    print("\nwrote t2 tables + fig2_correlation_by_period")


if __name__ == "__main__":
    main()
