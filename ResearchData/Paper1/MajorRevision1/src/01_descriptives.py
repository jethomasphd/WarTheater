#!/usr/bin/env python3
"""
01 — Descriptive trajectory (context for every finding).

Outputs
  output/figures/fig1_trajectory.(png|pdf)     daily strike/retaliation tempo + diplomacy
  output/tables/t01_phase_intensity.csv        per-phase daily intensities (Table 1)
  output/tables/t01_summary_stats.csv          series summary statistics
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

import util


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 01 · Descriptives")
    print("=" * 70)
    util.apply_style()
    p = util.load_panel()
    days = p.index.values

    # ---------------- Figure 1 ------------------------------------------- #
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 6.0), sharex=True,
                             gridspec_kw={"height_ratios": [1.6, 1]})
    ax = axes[0]
    util.shade_phases(ax)
    ax.plot(days, p["strikes"], color=util.C_STRIKE, lw=1.5, label="US/Israeli strikes")
    ax.plot(days, p["retal"], color=util.C_RETAL, lw=1.5, label="Iranian/proxy retaliation")
    for d in util.DOCUMENTED_BREAKS:
        ax.axvline(d, color="0.4", lw=0.8, ls="--", zorder=1)
    ax.set_ylim(0, 26)
    util.label_phases(ax, 24.6, fontsize=7)
    ax.set_ylabel("Events per day\n(distinct locations)")
    ax.set_title("A. Daily strike and retaliation tempo", loc="left", fontweight="bold")
    ax.legend(loc="upper right", ncol=2, fontsize=9, bbox_to_anchor=(1.0, 0.90))

    ax = axes[1]
    util.shade_phases(ax)
    ax.bar(days, p["diplomatic"], color=util.C_DIPL, width=0.9, alpha=0.85)
    for d in util.DOCUMENTED_BREAKS:
        ax.axvline(d, color="0.4", lw=0.8, ls="--", zorder=1)
    ax.set_ylabel("Diplomatic events\nper day")
    ax.set_title("B. Daily diplomatic activity", loc="left", fontweight="bold")
    ax.set_xlabel("Day of conflict (Day 1 = 28 February 2026)")
    util.savefig(fig, "fig1_trajectory")
    plt.close(fig)

    # ---------------- Table 1 -------------------------------------------- #
    rows = []
    for name, lo, hi in util.PHASES:
        seg = p[(p.index >= lo) & (p.index <= hi)]
        rows.append({
            "phase": name, "days": f"{lo}-{hi}", "n_days": len(seg),
            "strikes_per_day": round(seg["strikes"].mean(), 2),
            "retal_per_day": round(seg["retal"].mean(), 2),
            "strike_retal_ratio": round(seg["strikes"].sum() / max(seg["retal"].sum(), 1), 2),
            "diplomatic_per_day": round(seg["diplomatic"].mean(), 2),
            "killed_per_day": round(seg["killed"].mean(), 1),
            "pct_days_with_strike": round(100 * (seg["strikes"] > 0).mean(), 1),
            "pct_days_with_retal": round(100 * (seg["retal"] > 0).mean(), 1),
        })
    t = pd.DataFrame(rows)
    print("\n--- Per-phase daily intensity (Table 1) ---")
    print(t.to_string(index=False))
    util.write_table(t, "t01_phase_intensity.csv")

    cols = ["strikes", "retal", "killed", "diplomatic", "naval"]
    desc = p[cols].agg(["sum", "mean", "std", "min", "max"]).round(2).T
    desc["nonzero_days"] = [(p[c] > 0).sum() for c in cols]
    desc.index.name = "series"
    print("\n--- Series summary ---")
    print(desc.to_string())
    util.write_table(desc.reset_index(), "t01_summary_stats.csv")


if __name__ == "__main__":
    main()
