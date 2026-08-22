#!/usr/bin/env python3
"""
01 — Descriptives: mortality trajectories, health-system degradation timeline.

Outputs:
  output/tables/t01_phase_summary.csv        per-phase daily means/SD + totals
  output/tables/t01_series_summary.csv       summary statistics of key series
  output/tables/t01_health_register.csv      the 21 counted insult events (compact)
  output/figures/fig1_mortality_trajectory.(png|pdf)
  output/figures/fig2_cumulative_burden.(png|pdf)
  output/figures/fig3_health_system_timeline.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import util

TRANSITIONS = [41, 130, 153]

# Milestones annotated on the health-system timeline (day, short label).
# All are register events or benchmark reports; ids in data/health_system_events.csv.
MILESTONES = [
    (3,   "Gandhi Hospital damaged\n(IVF dept destroyed)"),
    (15,  "Ministry: 31 hospitals damaged,\n12 inactive"),
    (33,  "Pharma factory struck;\n10 nurses killed"),
    (39,  "WHO: 307 health\nfacilities damaged"),
    (45,  "WHO Dubai logistics\nhub on hold"),
    (69,  "WHO: 152 attacks on\nhealthcare in Lebanon"),
    (93,  "Lebanon MoPH: 127 health-\ncare workers killed"),
    (140, "Bonji desalination destroyed;\n~10,000 lose drinking water"),
]


def main():
    util.apply_style()
    p = util.load_panel()
    h = util.load_health_register()
    days = p.index.values

    # ------------------- Table 1: per-phase summary ---------------------- #
    rows = []
    for name, lo, hi in util.PHASES:
        seg = p.loc[lo:hi]
        rows.append({
            "phase": name, "days": f"{lo}-{hi}", "n_days": len(seg),
            "strikes_mean": seg.strikes.mean(), "strikes_sd": seg.strikes.std(),
            "civfac_strikes_mean": seg.strikes_civfac.mean(),
            "health_insults_total": int(seg.health_insults.sum()),
            "iran_civ_mean": seg.iran_civ.mean(), "iran_civ_sd": seg.iran_civ.std(),
            "iran_civ_total": int(seg.iran_civ.sum()),
            "iran_mil_total": int(seg.iran_mil.sum()),
            "leb_mean": seg.leb_all.mean(), "leb_sd": seg.leb_all.std(),
            "leb_total": int(seg.leb_all.sum()),
            "killed_total_mean": seg.killed_total.mean(),
            "killed_total_sd": seg.killed_total.std(),
            "killed_total_total": int(seg.killed_total.sum()),
        })
    seg = p
    rows.append({
        "phase": "Full war", "days": "1-170", "n_days": len(seg),
        "strikes_mean": seg.strikes.mean(), "strikes_sd": seg.strikes.std(),
        "civfac_strikes_mean": seg.strikes_civfac.mean(),
        "health_insults_total": int(seg.health_insults.sum()),
        "iran_civ_mean": seg.iran_civ.mean(), "iran_civ_sd": seg.iran_civ.std(),
        "iran_civ_total": int(seg.iran_civ.sum()),
        "iran_mil_total": int(seg.iran_mil.sum()),
        "leb_mean": seg.leb_all.mean(), "leb_sd": seg.leb_all.std(),
        "leb_total": int(seg.leb_all.sum()),
        "killed_total_mean": seg.killed_total.mean(),
        "killed_total_sd": seg.killed_total.std(),
        "killed_total_total": int(seg.killed_total.sum()),
    })
    t01 = pd.DataFrame(rows).round(2)
    t01.to_csv(util.TAB_DIR / "t01_phase_summary.csv", index=False)
    print("t01_phase_summary:")
    print(t01[["phase", "n_days", "strikes_mean", "iran_civ_total",
               "leb_total", "killed_total_total"]].to_string(index=False))

    # ------------------- Series summary ---------------------------------- #
    series = ["strikes", "retal", "strikes_civfac", "strikes_milfac",
              "health_insults", "iran_civ", "iran_mil", "us_mil", "leb_all",
              "isr_mil", "killed_total"]
    summ = p[series].agg(["mean", "std", "min", "median", "max", "sum"]).T.round(2)
    summ.to_csv(util.TAB_DIR / "t01_series_summary.csv")

    # Compact register table for the appendix.
    hc = h[h.counted][["event_id", "day_of_conflict", "date", "health_category",
                       "data_confidence", "event_description"]].copy()
    hc["event_description"] = hc.event_description.str.slice(0, 160)
    hc.to_csv(util.TAB_DIR / "t01_health_register.csv", index=False)

    # ------------------- Figure 1: mortality trajectory ------------------- #
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 8.4), sharex=True)

    ax = axes[0]
    util.shade_phases(ax)
    ax.plot(days, p.strikes, color=util.C_STRIKE, lw=1.5, label="Strike tempo (locations/day)")
    ax.plot(days, p.strikes_civfac, color=util.C_ACCENT, lw=1.3,
            label="Civilian-facing strike locations")
    ax.set_ylabel("Strike locations\nper day")
    ax.set_ylim(0, 23)
    ax.set_title("A. Kinetic exposure", loc="left", fontweight="bold")
    for d in TRANSITIONS:
        ax.axvline(d, color="0.4", lw=0.8, ls="--", zorder=1)
    util.phase_labels(ax, 21.4)
    ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.0, 0.88))

    ax = axes[1]
    util.shade_phases(ax)
    ax.fill_between(days, p.iran_civ + p.iran_mil, color=util.C_KILLED, alpha=0.18,
                    step="mid", label="Iran (military + civilian)")
    ax.plot(days, p.iran_civ + p.iran_mil, color=util.C_KILLED, lw=1.0)
    ax.plot(days, p.iran_civ, color=util.C_RETAL, lw=1.3, label="Iran (civilian)")
    ax.set_ylabel("Estimated killed\nper day")
    ax.set_title("B. Iranian daily estimated deaths", loc="left", fontweight="bold")
    ax.legend(fontsize=8, loc="upper right")

    ax = axes[2]
    util.shade_phases(ax)
    ax.fill_between(days, p.leb_all, color=util.C_SKY, alpha=0.35, step="mid")
    ax.plot(days, p.leb_all, color=util.C_STRIKE, lw=1.1)
    ax.set_ylabel("Estimated killed\nper day")
    ax.set_title("C. Lebanese daily estimated deaths (all categories)",
                 loc="left", fontweight="bold")
    ax.set_xlabel("Day of conflict")
    ax.set_xlim(0, 171)
    util.savefig(fig, "fig1_mortality_trajectory")
    plt.close(fig)

    # ------------------- Figure 2: cumulative burden ---------------------- #
    fig, axes = plt.subplots(2, 2, figsize=(10.2, 6.6))

    ax = axes[0, 0]
    util.shade_phases(ax)
    ax.plot(days, p.cum_iran_daily, color=util.C_KILLED, lw=1.6,
            label="Daily-series cumulative")
    ax.plot(days, p.snap_iranian_killed, color=util.C_RETAL, lw=1.4, ls="--",
            label="Dashboard snapshot")
    ax.set_title("A. Iran: cumulative killed", loc="left", fontweight="bold")
    ax.set_ylabel("Cumulative killed")
    ax.legend(fontsize=8, loc="lower right")

    ax = axes[0, 1]
    util.shade_phases(ax)
    ax.plot(days, p.cum_leb_daily, color=util.C_KILLED, lw=1.6,
            label="Daily-series cumulative")
    ax.plot(days, p.snap_lebanese_killed, color=util.C_RETAL, lw=1.4, ls="--",
            label="Dashboard snapshot")
    ax.set_title("B. Lebanon: cumulative killed", loc="left", fontweight="bold")
    ax.legend(fontsize=8, loc="lower right")

    ax = axes[1, 0]
    util.shade_phases(ax)
    ax.plot(days, p.snap_children_killed, color=util.C_ACCENT, lw=1.6)
    ax.set_title("C. Children killed (cumulative snapshot)", loc="left", fontweight="bold")
    ax.set_ylabel("Cumulative")
    ax.set_xlabel("Day of conflict")

    ax = axes[1, 1]
    util.shade_phases(ax)
    ax.plot(days, p.snap_displaced / 1e6, color=util.C_HEALTH, lw=1.6)
    ax.set_title("D. Displaced (cumulative snapshot, millions)", loc="left",
                 fontweight="bold")
    ax.set_xlabel("Day of conflict")
    for ax in axes.flat:
        ax.set_xlim(0, 171)
    util.savefig(fig, "fig2_cumulative_burden")
    plt.close(fig)

    # ------------------- Figure 3: health-system timeline ----------------- #
    fig, axes = plt.subplots(2, 1, figsize=(9.6, 7.2), sharex=True,
                             gridspec_kw={"height_ratios": [1.35, 1]})
    ax = axes[0]
    util.shade_phases(ax)
    ax.step(days, p.hssi, where="post", color=util.C_HEALTH, lw=1.8,
            label="Cumulative audited health-system insults (HSSI)")
    cat_marker = {"facility_attack": "o", "workforce_harm": "s",
                  "wash_disruption": "^", "supply_disruption": "D",
                  "access_disruption": "v"}
    hc2 = h[h.counted]
    for cat, mk in cat_marker.items():
        sub = hc2[hc2.health_category == cat]
        yvals = [p.loc[d, "hssi"] for d in sub.day_of_conflict]
        ax.scatter(sub.day_of_conflict, yvals, marker=mk, s=42, zorder=5,
                   color=util.C_HEALTH, edgecolor="white", linewidth=0.8,
                   label=cat.replace("_", " "))
    ax.set_ylabel("Cumulative insult events")
    ax.set_ylim(0, 24.5)
    ax.set_title("A. Health-system insult accumulation (21 audited events)",
                 loc="left", fontweight="bold")
    ax.legend(fontsize=7.5, loc="lower right", ncol=2)
    util.phase_labels(ax, 23.3)

    ax = axes[1]
    util.shade_phases(ax)
    ax.plot(days, p.facil_damage_bench, color=util.C_RETAL, lw=1.8)
    bx = [b[0] for b in util.FACILITY_BENCHMARKS]
    by = [b[1] for b in util.FACILITY_BENCHMARKS]
    ax.scatter(bx, by, s=52, zorder=5, color=util.C_RETAL, edgecolor="white")
    short = {"Iran Health Ministry / Red Crescent reporting": "Iran Health Ministry",
             "WHO": "WHO",
             "Iranian Red Crescent Society (IRCS)": "IRCS"}
    for d, v, _, _, src in util.FACILITY_BENCHMARKS:
        right_edge = d > 150
        ax.annotate(f"D{d}: {v} ({short.get(src, src)})", (d, v),
                    textcoords="offset points",
                    xytext=(-8 if right_edge else 8, -16),
                    ha="right" if right_edge else "left", fontsize=7.2)
    ax.set_ylabel("Health facilities damaged\n(Iran, cumulative)")
    ax.set_xlabel("Day of conflict")
    ax.set_title("B. Benchmark-anchored facility-damage curve",
                 loc="left", fontweight="bold")
    ax.set_xlim(0, 171)

    # Milestone annotations along the bottom panel are cluttered; put a
    # compact milestone strip between the panels instead.
    for d, label in MILESTONES:
        axes[0].axvline(d, color="0.55", lw=0.6, ls=":", zorder=1)
    util.savefig(fig, "fig3_health_system_timeline")
    plt.close(fig)

    print("wrote t01 tables + fig1-fig3")


if __name__ == "__main__":
    main()
