#!/usr/bin/env python3
"""
01 — FINDING 1: the war killed early. (Tool: means comparison.)

The question
------------
When did people die? Were deaths spread evenly across the 170 days, or were
they concentrated at the start?

What we compare
---------------
Average daily deaths across the four phases of the war (Major Combat, First
Ceasefire, Resumption, Diplomatic Pause). Three outcome series are used:
all-faction deaths per day, Iranian civilian deaths per day, and Lebanese
deaths per day.

The tools (all standard means comparison)
-----------------------------------------
* Descriptive shares: what percentage of all documented deaths fell in each
  phase, compared with what percentage of the days each phase covers.
* One-way ANOVA across the four phases, with eta-squared (the share of the
  day-to-day variance in deaths that phase explains). Welch's ANOVA, which
  does not assume equal variances, is reported alongside as a check.
* Pairwise Welch t-tests between phases, with Holm-adjusted p-values (a
  correction for running six comparisons) and Hedges' g (a standardized
  difference between two means; Cohen's d with a small-sample correction).
* "Deaths per strike location" on strike days, Major Combat vs Resumption:
  Welch t-test and Hedges' g (a Mann-Whitney test is included in the table
  as a rank-based check, because the per-strike values are skewed).
* A cumulative curve: on which day had half, then 80%, of all the deaths in
  the daily series already happened?

Outputs
-------
  output/tables/t1_phase_summary.csv
  output/tables/t1_milestones.csv
  output/tables/t1_anova.csv
  output/tables/t1_pairwise.csv
  output/tables/t1_lethality.csv
  output/figures/fig1_front_loading.(png|pdf)
"""
from __future__ import annotations

import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import util

OUTCOMES = [("killed_total", "All-faction deaths per day"),
            ("iran_civ", "Iranian civilian deaths per day"),
            ("leb_all", "Lebanese deaths per day")]


def eta_omega(groups):
    """Eta-squared and omega-squared for a one-way design."""
    k = len(groups)
    allv = np.concatenate(groups)
    n = len(allv)
    grand = allv.mean()
    ss_b = sum(len(g) * (np.mean(g) - grand) ** 2 for g in groups)
    ss_w = sum(((g - np.mean(g)) ** 2).sum() for g in groups)
    ss_t = ss_b + ss_w
    ms_w = ss_w / (n - k)
    eta2 = ss_b / ss_t if ss_t else 0.0
    omega2 = (ss_b - (k - 1) * ms_w) / (ss_t + ms_w) if (ss_t + ms_w) else 0.0
    return eta2, max(omega2, 0.0)


def welch_df(a, b):
    """Welch-Satterthwaite degrees of freedom for two samples."""
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    if va + vb == 0:
        return np.nan
    return (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))


def mean_diff_ci(a, b):
    """Difference in means with a 95% confidence interval (Welch)."""
    diff = a.mean() - b.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    df = welch_df(a, b)
    if se == 0 or np.isnan(df):
        return diff, diff, diff
    t = stats.t.ppf(0.975, df)
    return diff, diff - t * se, diff + t * se


def main():
    util.apply_style()
    p = util.load_panel()
    days = p.index.values
    total_deaths = int(p.killed_total.sum())

    # ------------------------------------------------------------------ #
    # Table 1 — per-phase summary: shares of days and of deaths
    # ------------------------------------------------------------------ #
    rows = []
    for name, lo, hi in util.PHASES + [("Full war", 1, util.LAST_DAY)]:
        seg = p.loc[lo:hi]
        rows.append({
            "phase": name, "days": f"{lo}-{hi}", "n_days": len(seg),
            "share_of_days_pct": 100.0 * len(seg) / util.LAST_DAY,
            "strikes_mean": seg.strikes.mean(),
            "iran_civ_mean": seg.iran_civ.mean(), "iran_civ_sd": seg.iran_civ.std(ddof=1),
            "iran_civ_total": int(seg.iran_civ.sum()),
            "iran_mil_total": int(seg.iran_mil.sum()),
            "leb_mean": seg.leb_all.mean(), "leb_sd": seg.leb_all.std(ddof=1),
            "leb_total": int(seg.leb_all.sum()),
            "killed_total_mean": seg.killed_total.mean(),
            "killed_total_sd": seg.killed_total.std(ddof=1),
            "killed_total_total": int(seg.killed_total.sum()),
            "share_of_deaths_pct": 100.0 * seg.killed_total.sum() / total_deaths,
        })
    t1 = pd.DataFrame(rows)
    t1.round(2).to_csv(util.TAB_DIR / "t1_phase_summary.csv", index=False)

    # ------------------------------------------------------------------ #
    # Milestones — the cumulative curve and the "policy window" numbers
    # ------------------------------------------------------------------ #
    cum = p.killed_total.cumsum().values
    mc_deaths = int(p.loc[1:40, "killed_total"].sum())
    mc_share = 100.0 * mc_deaths / total_deaths
    mc_day_share = 100.0 * 40 / util.LAST_DAY
    day_50 = int(days[np.searchsorted(cum, 0.50 * total_deaths)])
    day_80 = int(days[np.searchsorted(cum, 0.80 * total_deaths)])
    day_90 = int(days[np.searchsorted(cum, 0.90 * total_deaths)])
    iran_total = int(p.cum_iran_daily.iloc[-1])
    iran_by_40 = int(p.cum_iran_daily.loc[40])
    iranciv_total = int(p.iran_civ.sum())
    iranciv_by_40 = int(p.iran_civ.loc[:40].sum())
    leb_total = int(p.cum_leb_daily.iloc[-1])
    leb_by_40 = int(p.cum_leb_daily.loc[40])
    top = p.killed_total.sort_values(ascending=False).head(5)
    top_civ = p.iran_civ.sort_values(ascending=False).head(5)

    ms = [
        ("total_documented_deaths_daily_series", total_deaths),
        ("deaths_in_major_combat_days_1_40", mc_deaths),
        ("major_combat_share_of_deaths_pct", round(mc_share, 1)),
        ("major_combat_share_of_days_pct", round(mc_day_share, 1)),
        ("day_cumulative_deaths_reached_50pct", day_50),
        ("day_cumulative_deaths_reached_80pct", day_80),
        ("day_cumulative_deaths_reached_90pct", day_90),
        ("iran_deaths_daily_series_total", iran_total),
        ("iran_deaths_by_day_40", iran_by_40),
        ("iran_deaths_by_day_40_pct", round(100.0 * iran_by_40 / iran_total, 1)),
        ("iran_civilian_deaths_total", iranciv_total),
        ("iran_civilian_deaths_by_day_40", iranciv_by_40),
        ("iran_civilian_deaths_by_day_40_pct", round(100.0 * iranciv_by_40 / iranciv_total, 1)),
        ("lebanon_deaths_daily_series_total", leb_total),
        ("lebanon_deaths_by_day_40", leb_by_40),
        ("lebanon_deaths_by_day_40_pct", round(100.0 * leb_by_40 / leb_total, 1)),
        ("iran_civilian_deaths_first_ceasefire_days_41_129", int(p.loc[41:129, "iran_civ"].sum())),
        ("deadliest_day_all_faction", int(top.index[0])),
        ("deadliest_day_all_faction_deaths", int(top.iloc[0])),
        ("deadliest_day_iran_civilian", int(top_civ.index[0])),
        ("deadliest_day_iran_civilian_deaths", int(top_civ.iloc[0])),
        ("top5_days_all_faction", "; ".join(f"Day {int(d)}: {int(v)}" for d, v in top.items())),
    ]
    pd.DataFrame(ms, columns=["metric", "value"]).to_csv(
        util.TAB_DIR / "t1_milestones.csv", index=False)

    print("FINDING 1 — the war killed early (means comparison)")
    print(f"  {mc_deaths:,} of {total_deaths:,} documented deaths ({mc_share:.1f}%) "
          f"fell in Days 1-40 ({mc_day_share:.1f}% of the days)")
    print(f"  half of all deaths by Day {day_50}; 80% by Day {day_80}; 90% by Day {day_90}")
    print(f"  Iran: {iran_by_40:,} of {iran_total:,} deaths ({100*iran_by_40/iran_total:.1f}%) by Day 40; "
          f"Lebanon: {leb_by_40:,} of {leb_total:,} ({100*leb_by_40/leb_total:.1f}%)")
    print(f"  deadliest day (all factions): Day {int(top.index[0])} ({int(top.iloc[0])} deaths); "
          f"deadliest day for Iranian civilians: Day {int(top_civ.index[0])} ({int(top_civ.iloc[0])})")

    # ------------------------------------------------------------------ #
    # ANOVA across phases + pairwise contrasts
    # ------------------------------------------------------------------ #
    rows_a, rows_p = [], []
    for col, label in OUTCOMES:
        groups = [p.loc[lo:hi, col].values.astype(float) for _, lo, hi in util.PHASES]
        F, p_f = stats.f_oneway(*groups)
        if any(np.var(g, ddof=1) == 0 for g in groups):
            Fw = df2w = p_w = np.nan
            welch_note = "not defined: one phase has zero variance (all values 0)"
        else:
            Fw, df2w, p_w = util.welch_anova(groups)
            welch_note = ""
        eta2, omega2 = eta_omega(groups)
        rows_a.append({
            "outcome": col, "outcome_label": label,
            "anova_F": F, "df1": len(groups) - 1, "df2": len(p) - len(groups), "anova_p": p_f,
            "eta2": eta2, "omega2": omega2,
            "welch_F": Fw, "welch_df2": df2w, "welch_p": p_w, "welch_note": welch_note,
        })
        pair_p, pair_rows = [], []
        for (n1, lo1, hi1), (n2, lo2, hi2) in itertools.combinations(util.PHASES, 2):
            g1 = p.loc[lo1:hi1, col].values.astype(float)
            g2 = p.loc[lo2:hi2, col].values.astype(float)
            if g1.var(ddof=1) == 0 and g2.var(ddof=1) == 0:
                t, pv = (0.0, 1.0) if g1.mean() == g2.mean() else (np.inf, 0.0)
            else:
                t, pv = stats.ttest_ind(g1, g2, equal_var=False)
            diff, lo_ci, hi_ci = mean_diff_ci(g1, g2)
            pair_p.append(pv)
            pair_rows.append({
                "outcome": col, "phase_1": n1, "phase_2": n2,
                "n_1": len(g1), "mean_1": g1.mean(), "sd_1": g1.std(ddof=1),
                "n_2": len(g2), "mean_2": g2.mean(), "sd_2": g2.std(ddof=1),
                "mean_diff": diff, "diff_ci95_low": lo_ci, "diff_ci95_high": hi_ci,
                "welch_t": t, "welch_df": welch_df(g1, g2), "p_raw": pv,
                "hedges_g": util.hedges_g(g1, g2),
            })
        for r, a in zip(pair_rows, util.holm(pair_p)):
            r["p_holm"] = a
        rows_p.extend(pair_rows)
    ta = pd.DataFrame(rows_a)
    ta.to_csv(util.TAB_DIR / "t1_anova.csv", index=False)
    tp = pd.DataFrame(rows_p)
    tp.to_csv(util.TAB_DIR / "t1_pairwise.csv", index=False)
    print("\n  one-way ANOVA across the four phases:")
    print(ta[["outcome_label", "anova_F", "df1", "df2", "anova_p", "eta2"]].round(3).to_string(index=False))
    mc = tp[(tp.outcome == "killed_total") & (tp.phase_1 == "Major Combat")]
    print("  Major Combat vs each later phase (all-faction deaths/day):")
    for _, r in mc.iterrows():
        print(f"    vs {r.phase_2:17s} diff = {r.mean_diff:6.1f}/day  g = {r.hedges_g:.2f}  Holm p = {r.p_holm:.2e}")

    # ------------------------------------------------------------------ #
    # Deaths per strike location on strike days — Major Combat vs Resumption
    # ------------------------------------------------------------------ #
    sd = p[p.strike_day == 1].copy()
    sd["iran_killed"] = sd.iran_civ + sd.iran_mil
    sd["per_location"] = sd.iran_killed / sd.strikes
    rows_l = []
    for name, lo, hi in util.PHASES:
        seg = sd.loc[(sd.index >= lo) & (sd.index <= hi)]
        if not len(seg):
            rows_l.append({"phase": name, "n_strike_days": 0})
            continue
        rows_l.append({
            "phase": name, "n_strike_days": len(seg),
            "strike_locations_per_day": seg.strikes.mean(),
            "iran_deaths_per_day": seg.iran_killed.mean(),
            "deaths_per_location_mean": seg.per_location.mean(),
            "deaths_per_location_median": seg.per_location.median(),
            "deaths_per_location_sd": seg.per_location.std(ddof=1),
        })
    mc_v = sd.loc[(sd.index >= 1) & (sd.index <= 40), "per_location"].values
    rs_v = sd.loc[(sd.index >= 130) & (sd.index <= 152), "per_location"].values
    t, pv = stats.ttest_ind(mc_v, rs_v, equal_var=False)
    u, pu = stats.mannwhitneyu(mc_v, rs_v, alternative="two-sided")
    diff, lo_ci, hi_ci = mean_diff_ci(mc_v, rs_v)
    tl = pd.DataFrame(rows_l)
    tl["combat_vs_resumption_mean_diff"] = diff
    tl["combat_vs_resumption_diff_ci95_low"] = lo_ci
    tl["combat_vs_resumption_diff_ci95_high"] = hi_ci
    tl["combat_vs_resumption_welch_t"] = t
    tl["combat_vs_resumption_welch_df"] = welch_df(mc_v, rs_v)
    tl["combat_vs_resumption_p"] = pv
    tl["combat_vs_resumption_hedges_g"] = util.hedges_g(mc_v, rs_v)
    tl["combat_vs_resumption_pct_decline"] = 100 * (1 - rs_v.mean() / mc_v.mean())
    tl["mann_whitney_U_check"] = u
    tl["mann_whitney_p_check"] = pu
    tl.round(4).to_csv(util.TAB_DIR / "t1_lethality.csv", index=False)
    print(f"\n  Iranian deaths per strike location on strike days: {mc_v.mean():.1f} (Major Combat, "
          f"n={len(mc_v)}) vs {rs_v.mean():.1f} (Resumption, n={len(rs_v)}) = "
          f"{100*(1-rs_v.mean()/mc_v.mean()):.0f}% lower; Welch t = {t:.2f}, p = {pv:.4f}, "
          f"g = {util.hedges_g(mc_v, rs_v):.2f} (Mann-Whitney p = {pu:.4f})")

    # ------------------------------------------------------------------ #
    # Figure 1
    # ------------------------------------------------------------------ #
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    ax = axes[0]
    util.shade_phases(ax)
    ax.fill_between(days, p.killed_total, where=(days <= 40), color=util.C_RETAL,
                    alpha=0.30, step="mid", label="Major Combat (Days 1–40)")
    ax.plot(days, p.killed_total, color=util.C_KILLED, lw=1.1)
    ax.axvline(40.5, color=util.C_RETAL, lw=1.0, ls="--")
    ax.set_xlabel("Day of the war")
    ax.set_ylabel("Documented deaths per day (all factions)")
    ax.set_xlim(0, 171)
    ax.set_title("A. Deaths per day: most of them came early",
                 loc="left", fontweight="bold", fontsize=9.5)
    ylab = ax.get_ylim()[1]
    abbr = {"Major Combat": "MAJOR COMBAT", "First Ceasefire": "FIRST CEASEFIRE",
            "Resumption": "RESUMPTION", "Diplomatic Pause": "DIPL. PAUSE"}
    for name, lo, hi in util.PHASES:
        if hi - lo >= 25:
            ax.text((lo + hi) / 2, ylab * 0.9, abbr[name], fontsize=7.0,
                    color="0.35", ha="center", va="center")
        else:
            ax.text((lo + hi) / 2, ylab * 0.14, abbr[name], fontsize=6.6,
                    color="0.4", ha="center", va="bottom", rotation=90)
    ax.legend(fontsize=8, loc="upper right")

    ax = axes[1]
    frac_days = np.concatenate([[0], days]) / util.LAST_DAY * 100
    frac_deaths = np.concatenate([[0], cum]) / total_deaths * 100
    ax.plot([0, 100], [0, 100], color="0.6", lw=1.0, ls=":",
            label="If deaths were spread evenly")
    ax.plot(frac_days, frac_deaths, color=util.C_STRIKE, lw=2.2, label="What happened")
    ax.scatter([mc_day_share], [mc_share], s=70, zorder=6, color=util.C_RETAL,
               edgecolor="white", linewidth=1.0)
    ax.annotate(f"Day 40 (end of Major Combat):\n{mc_share:.1f}% of deaths in\n{mc_day_share:.1f}% of the days",
                (mc_day_share, mc_share), textcoords="offset points",
                xytext=(14, -6), fontsize=8.4, color=util.C_RETAL,
                fontweight="bold", va="top")
    d50 = 100 * day_50 / util.LAST_DAY
    ax.scatter([d50], [100 * cum[day_50 - 1] / total_deaths], s=40, zorder=6,
               color=util.C_STRIKE, edgecolor="white", linewidth=1.0)
    ax.annotate(f"Day {day_50}: half of all deaths", (d50, 100 * cum[day_50 - 1] / total_deaths),
                textcoords="offset points", xytext=(10, -14), fontsize=8.0, color=util.C_STRIKE)
    ax.axhline(mc_share, color=util.C_RETAL, lw=0.6, ls="--", alpha=0.6)
    ax.axvline(mc_day_share, color=util.C_RETAL, lw=0.6, ls="--", alpha=0.6)
    ax.set_xlabel("Share of the 170 days that had passed (%)")
    ax.set_ylabel("Share of all documented deaths that had happened (%)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title("B. How quickly the deaths added up",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=8, loc="lower right")
    util.savefig(fig, "fig1_front_loading")
    plt.close(fig)
    print("\nwrote t1 tables + fig1_front_loading")


if __name__ == "__main__":
    main()
