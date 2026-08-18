#!/usr/bin/env python3
"""
01 — Descriptive escalation trajectory.

Outputs:
  output/figures/fig1_escalation_trajectory.(png|pdf)   headline 3-panel time series
  output/figures/fig2_intensity_and_spread.(png|pdf)    ratio + horizontal spread
  output/tables/t01_phase_intensity.csv                 per-phase daily intensities
  output/tables/t01_summary_stats.csv                   series summary statistics
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import util

# Phase-transition day markers (dashed verticals on panel A).
TRANSITIONS = [41, 130, 153]


def main():
    util.apply_style()
    p = util.load_panel()
    days = p.index.values

    # ---------------- Figure 1: headline trajectory --------------------- #
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 8.4), sharex=True)

    ax = axes[0]
    util.shade_phases(ax)
    ax.plot(days, p["strikes"], color=util.C_STRIKE, lw=1.6, label="US/Israeli strikes")
    ax.plot(days, p["retal"], color=util.C_RETAL, lw=1.6, label="Iranian/proxy retaliation")
    ax.set_ylabel("Events per day\n(distinct locations)")
    ax.set_ylim(0, 23)
    ax.set_title("A. Offensive strike and retaliation tempo", loc="left", fontweight="bold")
    for d in TRANSITIONS:
        ax.axvline(d, color="0.4", lw=0.8, ls="--", zorder=1)
    # phase-band labels along the top (muted, uppercase)
    for name, lo, hi in util.PHASES:
        ax.text((lo + hi) / 2, 21.4, name.upper(), fontsize=7.0, color="0.35",
                ha="center", va="center")
    # legend above the panel row (figure-level) to avoid collisions
    h, l = ax.get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", bbox_to_anchor=(0.5, 0.99),
               ncol=2, fontsize=9)

    ax = axes[1]
    util.shade_phases(ax)
    ax.fill_between(days, p["killed"], color=util.C_KILLED, alpha=0.20, step="mid")
    ax.plot(days, p["killed"], color=util.C_KILLED, lw=1.1)
    ax.set_ylabel("Estimated killed\nper day (all factions)")
    ax.set_title("B. Daily casualties", loc="left", fontweight="bold")

    ax = axes[2]
    util.shade_phases(ax)
    ax.bar(days, p["diplomatic"], color=util.C_DIPL, width=0.9, alpha=0.85)
    ax.set_ylabel("Diplomatic events\nper day")
    ax.set_title("C. Diplomatic activity", loc="left", fontweight="bold")
    ax.set_xlabel("Day of conflict (Day 1 = 2026-02-28)")

    fig.suptitle("Escalation trajectory of the 2026 US–Iran War (Days 1–170)",
                 fontweight="bold", y=1.02)
    util.savefig(fig, "fig1_escalation_trajectory")
    plt.close(fig)

    # ---------------- Figure 2: intensity ratio + spread ---------------- #
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 5.8), sharex=True)

    # 7-day rolling strike & retaliation, plus rolling ratio
    roll = 7
    sm_s = p["strikes"].rolling(roll, min_periods=1).mean()
    sm_r = p["retal"].rolling(roll, min_periods=1).mean()
    ax = axes[0]
    util.shade_phases(ax)
    ax.plot(days, sm_s, color=util.C_STRIKE, lw=1.8, label="strikes (7-day mean)")
    ax.plot(days, sm_r, color=util.C_RETAL, lw=1.8, label="retaliation (7-day mean)")
    ax.set_ylabel("7-day mean\nevents/day")
    ax.legend(loc="upper right", ncol=2)
    ax.set_title("A. Smoothed strike vs. retaliation tempo", loc="left", fontweight="bold")

    ax = axes[1]
    util.shade_phases(ax)
    ax.plot(days, p["cum_countries"], color=util.C_ACCENT, lw=2.0)
    ax.set_ylabel("Cumulative distinct\ncountries hit by retaliation")
    ax.set_title("B. Horizontal spread of retaliation (geographic diffusion)",
                 loc="left", fontweight="bold")
    ax.set_xlabel("Day of conflict (Day 1 = 2026-02-28)")
    util.savefig(fig, "fig2_intensity_and_spread")
    plt.close(fig)

    # ---------------- Tables -------------------------------------------- #
    rows = []
    for name, lo, hi in util.PHASES:
        seg = p[(p.index >= lo) & (p.index <= hi)]
        n = len(seg)
        rows.append({
            "phase": name, "days": f"{lo}-{hi}", "n_days": n,
            "strikes_per_day": round(seg["strikes"].mean(), 2),
            "retal_per_day": round(seg["retal"].mean(), 2),
            "killed_per_day": round(seg["killed"].mean(), 1),
            "diplomatic_per_day": round(seg["diplomatic"].mean(), 2),
            "strike_retal_ratio": round(seg["strikes"].sum() / max(seg["retal"].sum(), 1), 2),
            "pct_days_with_strike": round(100 * (seg["strikes"] > 0).mean(), 1),
        })
    t = pd.DataFrame(rows)
    t.to_csv(util.TAB_DIR / "t01_phase_intensity.csv", index=False)
    print("\n--- Per-phase daily intensity ---")
    print(t.to_string(index=False))

    stat_cols = ["strikes", "retal", "killed", "diplomatic", "naval"]
    desc = p[stat_cols].agg(["sum", "mean", "std", "min", "max"]).round(2).T
    desc["nonzero_days"] = [(p[c] > 0).sum() for c in stat_cols]
    desc.to_csv(util.TAB_DIR / "t01_summary_stats.csv")
    print("\n--- Series summary ---")
    print(desc.to_string())
    print(f"\nWrote tables to {util.TAB_DIR}")


if __name__ == "__main__":
    main()
