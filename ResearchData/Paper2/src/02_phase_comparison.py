#!/usr/bin/env python3
"""
02 — Means comparison: mortality across conflict phases and strike conditions.

Classic behavioral-statistics workhorse of the paper:
  - One-way ANOVA + Welch ANOVA + Kruskal-Wallis across the four phases
  - Pairwise Welch t-tests with Holm correction + Hedges' g
  - Strike-day vs no-strike-day comparisons
  - Per-strike lethality by phase (Mann-Whitney)

Outputs:
  output/tables/t02_anova.csv
  output/tables/t02_pairwise.csv
  output/tables/t02_strikeday.csv
  output/tables/t02_lethality.csv
  output/figures/fig4_phase_comparison.(png|pdf)
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


def eta_omega(groups):
    """Classical effect sizes for one-way designs."""
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

    # ---------------- ANOVA family across phases ------------------------- #
    rows_a, rows_p = [], []
    for col, label in OUTCOMES:
        groups = [p.loc[lo:hi, col].values.astype(float)
                  for _, lo, hi in util.PHASES]
        F, p_f = stats.f_oneway(*groups)
        if any(np.var(g, ddof=1) == 0 for g in groups):
            # Welch weights are undefined when a phase has zero variance
            # (e.g. Iranian civilian deaths are uniformly 0 in two phases);
            # Kruskal-Wallis carries the robustness burden there.
            Fw = df2w = p_w = np.nan
            welch_note = "undefined (zero-variance phase); see Kruskal-Wallis"
        else:
            Fw, df2w, p_w = util.welch_anova(groups)
            welch_note = ""
        H, p_kw = stats.kruskal(*groups)
        eta2, omega2 = eta_omega(groups)
        rows_a.append({
            "outcome": col, "outcome_label": label,
            "anova_F": F, "anova_df1": len(groups) - 1,
            "anova_df2": len(p) - len(groups), "anova_p": p_f,
            "welch_F": Fw, "welch_df2": df2w, "welch_p": p_w,
            "welch_note": welch_note,
            "kruskal_H": H, "kruskal_p": p_kw,
            "eta2": eta2, "omega2": omega2,
        })

        # Pairwise Welch t-tests + Hedges' g, Holm-corrected within outcome.
        pair_p, pair_rows = [], []
        for (n1, lo1, hi1), (n2, lo2, hi2) in itertools.combinations(util.PHASES, 2):
            g1 = p.loc[lo1:hi1, col].values.astype(float)
            g2 = p.loc[lo2:hi2, col].values.astype(float)
            if g1.var(ddof=1) == 0 and g2.var(ddof=1) == 0:
                # Two zero-variance groups: identical constants -> no
                # difference (t = 0, p = 1); Welch is otherwise undefined.
                t, pv = (0.0, 1.0) if g1.mean() == g2.mean() else (np.inf, 0.0)
            else:
                t, pv = stats.ttest_ind(g1, g2, equal_var=False)
            pair_p.append(pv)
            pair_rows.append({
                "outcome": col, "phase_1": n1, "phase_2": n2,
                "mean_1": g1.mean(), "sd_1": g1.std(ddof=1),
                "mean_2": g2.mean(), "sd_2": g2.std(ddof=1),
                "welch_t": t, "p_raw": pv,
                "hedges_g": util.hedges_g(g1, g2),
            })
        adj = util.holm(pair_p)
        for r, a in zip(pair_rows, adj):
            r["p_holm"] = a
        rows_p.extend(pair_rows)

    t_anova = pd.DataFrame(rows_a)
    t_anova.to_csv(util.TAB_DIR / "t02_anova.csv", index=False)
    t_pair = pd.DataFrame(rows_p)
    t_pair.to_csv(util.TAB_DIR / "t02_pairwise.csv", index=False)
    print("t02_anova:")
    print(t_anova[["outcome", "anova_F", "anova_p", "welch_F", "welch_p",
                   "eta2", "omega2"]].round(4).to_string(index=False))

    # ---------------- Strike-day vs no-strike-day ------------------------- #
    rows_s = []
    for col, label in OUTCOMES:
        a = p.loc[p.strike_day == 1, col].values.astype(float)
        b = p.loc[p.strike_day == 0, col].values.astype(float)
        t, pv = stats.ttest_ind(a, b, equal_var=False)
        u, pu = stats.mannwhitneyu(a, b, alternative="two-sided")
        rows_s.append({
            "outcome": col, "outcome_label": label,
            "n_strike_days": len(a), "n_quiet_days": len(b),
            "mean_strike_days": a.mean(), "sd_strike_days": a.std(ddof=1),
            "mean_quiet_days": b.mean(), "sd_quiet_days": b.std(ddof=1),
            "welch_t": t, "welch_p": pv, "mannwhitney_U": u, "mannwhitney_p": pu,
            "hedges_g": util.hedges_g(a, b),
        })
    t_sd = pd.DataFrame(rows_s)
    t_sd.to_csv(util.TAB_DIR / "t02_strikeday.csv", index=False)
    print("\nt02_strikeday:")
    print(t_sd[["outcome", "mean_strike_days", "mean_quiet_days", "welch_t",
                "welch_p", "hedges_g"]].round(3).to_string(index=False))

    # ---------------- Per-strike lethality by phase ----------------------- #
    # On strike days only: deaths per distinct strike location that day.
    # Compares Major Combat vs Resumption (the two kinetic regimes on the
    # Iran front). Iranian deaths only, since the strike files target Iran.
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
    t_le.round(4).to_csv(util.TAB_DIR / "t02_lethality.csv", index=False)
    print("\nt02_lethality (deaths per strike location, strike days):")
    print(t_le[["phase", "n_strike_days", "lethality_mean",
                "lethality_median"]].round(2).to_string(index=False))
    print(f"  Major Combat vs Resumption: U={u:.1f}, p={pu:.4f}")

    # ---------------- Figure 4 ------------------------------------------- #
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.9))
    rng = np.random.default_rng(util.SEED)   # jitter only; seeded
    for ax, (col, label) in zip(axes, OUTCOMES):
        data = [p.loc[lo:hi, col].values.astype(float) for _, lo, hi in util.PHASES]
        bp = ax.boxplot(data, tick_labels=[n.replace(" ", "\n") for n in util.PHASE_ORDER],
                        showfliers=False, widths=0.55, patch_artist=True,
                        medianprops=dict(color="black", lw=1.4))
        for patch in bp["boxes"]:
            patch.set_facecolor("#DCE9F5")
            patch.set_edgecolor("0.35")
        for i, d in enumerate(data):
            x = rng.normal(i + 1, 0.055, size=len(d))
            ax.scatter(x, d, s=6, alpha=0.35, color=util.C_STRIKE, zorder=3,
                       linewidth=0)
        ax.set_title(label, loc="left", fontweight="bold", fontsize=9.5)
        ax.set_ylabel("Killed per day" if ax is axes[0] else "")
        ax.tick_params(axis="x", labelsize=7.5)
    util.savefig(fig, "fig4_phase_comparison")
    plt.close(fig)

    print("\nwrote t02 tables + fig4")


if __name__ == "__main__":
    main()
