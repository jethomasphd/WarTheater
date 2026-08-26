#!/usr/bin/env python3
"""
01 — FINDING 1: The war killed fast and early (front-loading).

The student's first finding: 79.6% of the war's documented deaths fell in the
40 days of Major Combat — 23.5% of the war's duration. The killing was not a
smooth function of how long the war lasted; it was concentrated at the front,
before the health system had any chance to adapt. Everything the two later
findings describe (a system losing its ability to absorb shocks; a documented
toll that is only a floor) happens in the long aftermath of that concentrated
opening blow.

This script quantifies the front-loading three complementary ways, reusing the
exact computations of the parent paper (scripts 01 and 02) so every number is
identical:

  (a) Per-phase mortality shares  -> t1_phase_summary.csv
  (b) A temporal-concentration curve (what fraction of deaths had accrued by
      each fraction of elapsed war-time) + the headline 79.6% / 23.5% point,
      a concentration ratio, and the day on which the cumulative toll crossed
      half -> t1_concentration.csv
  (c) That the phase differences are enormous, not noise: one-way ANOVA family
      with effect sizes and Holm-corrected pairwise contrasts, plus the
      collapse of deaths-per-strike from the opening campaign to the July
      resumption -> t1_phase_anova.csv, t1_phase_pairwise.csv, t1_lethality.csv

Figure:
  fig1_frontloading.(png|pdf) — the daily-death trajectory and the temporal
  concentration curve with the Major-Combat cut-point marked.
"""
from __future__ import annotations

import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import util

OUTCOMES = [("killed_total", "All-faction daily killed"),
            ("iran_civ", "Iranian civilian daily killed"),
            ("leb_all", "Lebanese daily killed")]


# ---- effect size for one-way designs (identical to parent 02) ------------- #
def eta_omega(groups):
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


def main():
    util.apply_style()
    p = util.load_panel()
    days = p.index.values

    # ==================================================================== #
    # (a) Per-phase summary (from parent 01) — the raw material of the share
    # ==================================================================== #
    rows = []
    for name, lo, hi in util.PHASES + [("Full war", 1, util.LAST_DAY)]:
        seg = p.loc[lo:hi]
        rows.append({
            "phase": name, "days": f"{lo}-{hi}", "n_days": len(seg),
            "strikes_mean": seg.strikes.mean(),
            "civfac_strikes_mean": seg.strikes_civfac.mean(),
            "health_insults_total": int(seg.health_insults.sum()),
            "iran_civ_mean": seg.iran_civ.mean(), "iran_civ_total": int(seg.iran_civ.sum()),
            "iran_mil_total": int(seg.iran_mil.sum()),
            "leb_mean": seg.leb_all.mean(), "leb_total": int(seg.leb_all.sum()),
            "killed_total_mean": seg.killed_total.mean(),
            "killed_total_sd": seg.killed_total.std(),
            "killed_total_total": int(seg.killed_total.sum()),
        })
    t1 = pd.DataFrame(rows).round(2)
    t1.to_csv(util.TAB_DIR / "t1_phase_summary.csv", index=False)

    total_deaths = int(p.killed_total.sum())
    mc_deaths = int(p.loc[1:40, "killed_total"].sum())
    mc_share = 100.0 * mc_deaths / total_deaths
    mc_day_share = 100.0 * 40 / util.LAST_DAY

    # ==================================================================== #
    # (b) Temporal concentration of mortality
    #     Order days chronologically; at each elapsed-time fraction record the
    #     fraction of the war's total deaths that had already accrued. The
    #     Major-Combat cut-point (Day 40) is the headline: 23.5% of the days,
    #     ~80% of the deaths.
    # ==================================================================== #
    cum = p.killed_total.cumsum().values
    frac_days = days / util.LAST_DAY
    frac_deaths = cum / total_deaths

    # Day on which the cumulative toll first crossed 50% / 80% of the war total.
    day_half = int(days[np.searchsorted(cum, 0.50 * total_deaths)])
    day_80 = int(days[np.searchsorted(cum, 0.80 * total_deaths)])

    # Concentration ratio: area under the temporal-concentration curve vs the
    # 45-degree line of a perfectly even war (2*area - 1; 0 = even, ->1 = all
    # deaths on Day 1). Chronological order, so this measures front-loading in
    # time, not inequality across an unordered set.
    area = np.trapezoid(frac_deaths, frac_days)
    conc_ratio = 2 * area - 1

    conc_rows = [
        {"metric": "total_documented_deaths", "value": total_deaths},
        {"metric": "major_combat_deaths", "value": mc_deaths},
        {"metric": "major_combat_share_of_deaths_pct", "value": round(mc_share, 1)},
        {"metric": "major_combat_share_of_days_pct", "value": round(mc_day_share, 1)},
        {"metric": "day_cumulative_toll_crossed_50pct", "value": day_half},
        {"metric": "day_cumulative_toll_crossed_80pct", "value": day_80},
        {"metric": "temporal_concentration_ratio", "value": round(conc_ratio, 3)},
    ]
    # Per-phase cumulative-share ladder.
    running = 0
    for name, lo, hi in util.PHASES:
        d = int(p.loc[lo:hi, "killed_total"].sum())
        running += d
        conc_rows.append({"metric": f"cum_share_through_{name.replace(' ', '_')}_pct",
                          "value": round(100.0 * running / total_deaths, 1)})
    pd.DataFrame(conc_rows).to_csv(util.TAB_DIR / "t1_concentration.csv", index=False)

    print("FINDING 1 — front-loading")
    print(f"  Major Combat carried {mc_deaths}/{total_deaths} deaths = {mc_share:.1f}% "
          f"in {mc_day_share:.1f}% of the days")
    print(f"  cumulative toll crossed 50% by Day {day_half}, 80% by Day {day_80}")
    print(f"  temporal concentration ratio = {conc_ratio:.3f} (0 = even, 1 = all on Day 1)")

    # ==================================================================== #
    # (c) The phase differences are enormous — ANOVA family + pairwise + g
    #     (identical to parent 02).
    # ==================================================================== #
    rows_a, rows_p = [], []
    for col, label in OUTCOMES:
        groups = [p.loc[lo:hi, col].values.astype(float) for _, lo, hi in util.PHASES]
        F, p_f = stats.f_oneway(*groups)
        if any(np.var(g, ddof=1) == 0 for g in groups):
            Fw = df2w = p_w = np.nan
            welch_note = "undefined (zero-variance phase); see Kruskal-Wallis"
        else:
            Fw, df2w, p_w = util.welch_anova(groups)
            welch_note = ""
        H, p_kw = stats.kruskal(*groups)
        eta2, omega2 = eta_omega(groups)
        rows_a.append({
            "outcome": col, "outcome_label": label, "anova_F": F,
            "anova_df1": len(groups) - 1, "anova_df2": len(p) - len(groups),
            "anova_p": p_f, "welch_F": Fw, "welch_df2": df2w, "welch_p": p_w,
            "welch_note": welch_note, "kruskal_H": H, "kruskal_p": p_kw,
            "eta2": eta2, "omega2": omega2,
        })
        pair_p, pair_rows = [], []
        for (n1, lo1, hi1), (n2, lo2, hi2) in itertools.combinations(util.PHASES, 2):
            g1 = p.loc[lo1:hi1, col].values.astype(float)
            g2 = p.loc[lo2:hi2, col].values.astype(float)
            if g1.var(ddof=1) == 0 and g2.var(ddof=1) == 0:
                t, pv = (0.0, 1.0) if g1.mean() == g2.mean() else (np.inf, 0.0)
            else:
                t, pv = stats.ttest_ind(g1, g2, equal_var=False)
            pair_p.append(pv)
            pair_rows.append({
                "outcome": col, "phase_1": n1, "phase_2": n2,
                "mean_1": g1.mean(), "sd_1": g1.std(ddof=1),
                "mean_2": g2.mean(), "sd_2": g2.std(ddof=1),
                "welch_t": t, "p_raw": pv, "hedges_g": util.hedges_g(g1, g2),
            })
        for r, a in zip(pair_rows, util.holm(pair_p)):
            r["p_holm"] = a
        rows_p.extend(pair_rows)

    pd.DataFrame(rows_a).to_csv(util.TAB_DIR / "t1_phase_anova.csv", index=False)
    pd.DataFrame(rows_p).to_csv(util.TAB_DIR / "t1_phase_pairwise.csv", index=False)
    ta = pd.DataFrame(rows_a)
    print("\n  phase ANOVA (variance explained by phase):")
    print(ta[["outcome_label", "anova_F", "eta2", "omega2"]].round(3).to_string(index=False))

    # Per-strike lethality collapse (identical to parent 02): supporting
    # context — average yield per strike fell 95% from Major Combat to the
    # July Resumption. (This is the "front-loaded averages" half of the story
    # the resilience finding reconciles with; see 02_resilience_erosion.py.)
    sd = p[p.strike_day == 1].copy()
    sd["iran_killed"] = sd.iran_civ + sd.iran_mil
    sd["lethality"] = sd.iran_killed / sd.strikes
    rows_l = []
    for name, lo, hi in util.PHASES:
        seg = sd.loc[(sd.index >= lo) & (sd.index <= hi)]
        if not len(seg):
            rows_l.append({"phase": name, "n_strike_days": 0})
            continue
        rows_l.append({
            "phase": name, "n_strike_days": len(seg),
            "strikes_per_day": seg.strikes.mean(),
            "iran_killed_per_day": seg.iran_killed.mean(),
            "lethality_mean": seg.lethality.mean(),
            "lethality_median": seg.lethality.median(),
            "lethality_sd": seg.lethality.std(ddof=1),
        })
    mc = sd.loc[(sd.index >= 1) & (sd.index <= 40), "lethality"]
    rs = sd.loc[(sd.index >= 130) & (sd.index <= 152), "lethality"]
    u, pu = stats.mannwhitneyu(mc, rs, alternative="two-sided")
    t_le = pd.DataFrame(rows_l)
    t_le["combat_vs_resumption_U"] = u
    t_le["combat_vs_resumption_p"] = pu
    t_le["combat_vs_resumption_g"] = util.hedges_g(mc.values, rs.values)
    t_le.round(4).to_csv(util.TAB_DIR / "t1_lethality.csv", index=False)
    leth_decline = 100 * (1 - rs.mean() / mc.mean())
    print(f"\n  deaths per strike location: {mc.mean():.1f} (Major Combat) -> "
          f"{rs.mean():.1f} (Resumption) = {leth_decline:.0f}% decline "
          f"(Mann-Whitney U={u:.0f}, p<.0001, g={util.hedges_g(mc.values, rs.values):.2f})")

    # ==================================================================== #
    # Figure 1 — trajectory + temporal concentration
    # ==================================================================== #
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))

    # Panel A: daily all-faction deaths, phases shaded, Major Combat filled.
    ax = axes[0]
    util.shade_phases(ax)
    ax.fill_between(days, p.killed_total, where=(days <= 40), color=util.C_RETAL,
                    alpha=0.30, step="mid", label="Major Combat (Days 1–40)")
    ax.plot(days, p.killed_total, color=util.C_KILLED, lw=1.1)
    ax.axvline(40, color=util.C_RETAL, lw=1.0, ls="--")
    ax.set_xlabel("Day of conflict")
    ax.set_ylabel("All-faction deaths per day")
    ax.set_xlim(0, 171)
    ax.set_title("A. Daily deaths: the killing is at the front",
                 loc="left", fontweight="bold", fontsize=9.5)
    # Label phases without overlap: wide phases get a horizontal label near the
    # top; the two narrow late phases get a short rotated label near the floor.
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

    # Panel B: temporal concentration curve with the headline cut-point.
    ax = axes[1]
    ax.plot([0, 1], [0, 1], color="0.6", lw=1.0, ls=":",
            label="An evenly-paced war")
    ax.plot(np.concatenate([[0], frac_days]) * 100,
            np.concatenate([[0], frac_deaths]) * 100,
            color=util.C_STRIKE, lw=2.2, label="Observed accumulation")
    ax.scatter([mc_day_share], [mc_share], s=70, zorder=6, color=util.C_RETAL,
               edgecolor="white", linewidth=1.0)
    ax.annotate(f"End of Major Combat:\n{mc_share:.1f}% of deaths in\n{mc_day_share:.1f}% of the war",
                (mc_day_share, mc_share), textcoords="offset points",
                xytext=(14, -6), fontsize=8.4, color=util.C_RETAL,
                fontweight="bold", va="top")
    ax.axhline(mc_share, color=util.C_RETAL, lw=0.6, ls="--", alpha=0.6)
    ax.axvline(mc_day_share, color=util.C_RETAL, lw=0.6, ls="--", alpha=0.6)
    ax.set_xlabel("Cumulative share of elapsed war-time (%)")
    ax.set_ylabel("Cumulative share of documented deaths (%)")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_title("B. Temporal concentration of mortality",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=8, loc="lower right")
    util.savefig(fig, "fig1_frontloading")
    plt.close(fig)

    print("\nwrote t1 tables + fig1_frontloading")


if __name__ == "__main__":
    main()
