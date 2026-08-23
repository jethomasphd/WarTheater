#!/usr/bin/env python3
"""
06 — Indirect mortality projection and WASH/environmental exposure summary.

The daily "estimated killed" series records DIRECT, reported deaths. The
conflict-epidemiology literature is unanimous that direct counts are the
floor, not the total: deaths from disrupted care, displacement, water
failure, and disease follow with a lag and rarely enter strike-day tallies
(Guha-Sapir & van Panhuis 2004; Geneva Declaration 2008; Checchi & Roberts
2008; Jawad et al. 2020).

This script therefore PROJECTS — it does not estimate from these data — the
plausible indirect-death burden implied by literature indirect:direct ratios,
applied to the documented direct toll, under explicit assumptions:
  R = 1:1  (very conservative floor)
  R = 3:1  (low end of the Geneva Declaration range)
  R = 4:1  (Geneva Declaration average across studied conflicts)
  R = 15:1 (upper end of the reported range; weak-health-system settings)
Each projection is computed on BOTH direct-toll bounds (daily-series sum =
lower bound; dashboard cumulative snapshot = upper bound), so the
presentation carries the dataset's own measurement uncertainty forward
rather than hiding it.

Also summarizes the WASH / environmental exposure events documented in the
register (population figures quoted verbatim from source events).

Outputs:
  output/tables/t06_direct_toll.csv
  output/tables/t06_projection.csv
  output/tables/t06_wash_exposure.csv
  output/figures/fig7_indirect_projection.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import util

# Indirect:direct death ratio scenarios (label, R, source note).
SCENARIOS = [
    ("floor_1to1", 1.0, "Very conservative floor"),
    ("low_3to1", 3.0, "Low end of Geneva Declaration (2008) range"),
    ("avg_4to1", 4.0, "Geneva Declaration (2008) cross-conflict average"),
    ("high_15to1", 15.0, "Upper end of reported range (weakest health systems)"),
]

# WASH / environmental exposure events with population-at-risk figures quoted
# in the dataset (event ids verified by the register build).
WASH_ROWS = [
    ("EVT-3311", 140, "Bonji (Jask) desalination plant intake station destroyed",
     "~10,000 people across 20 villages lost drinking water (Iran, Hormozgan)"),
    ("EVT-1019", 140, "Two Kuwaiti power-and-desalination plants struck, ablaze",
     "Kuwait relies on desalination for ~90% of potable water"),
    ("EVT-1769", 33, "Qeshm Island desalination plant struck (Days 33-34)",
     "Island population depends on desalinated supply"),
    ("EVT-0303", 31, "Kuwait water/electrical plant struck",
     "First strike on Gulf water infrastructure"),
    ("EVT-0060", 11, "ICRC: 30-40% of Iranian power generation degraded",
     "Nationwide power, water and fuel systems degraded (ICRC assessment)"),
]


def main():
    util.apply_style()
    p = util.load_panel()
    h = util.load_health_register()

    # ---------------- Direct toll bounds at Day 170 ----------------------- #
    civ_share_iran = p.iran_civ.sum() / (p.iran_civ.sum() + p.iran_mil.sum())
    rows = [
        {"population": "Iran (total)", "basis": "daily series (lower bound)",
         "direct_killed": int(p.cum_iran_daily.iloc[-1])},
        {"population": "Iran (total)", "basis": "dashboard snapshot (upper bound)",
         "direct_killed": int(p.snap_iranian_killed.iloc[-1])},
        {"population": "Iran (total)",
         "basis": "peak pre-re-anchoring snapshot (Day 56; see 07)",
         "direct_killed": int(p.snap_iranian_killed.max())},
        {"population": "Iran (civilian)", "basis": "daily series",
         "direct_killed": int(p.iran_civ.sum())},
        {"population": "Lebanon (all)", "basis": "daily series (lower bound)",
         "direct_killed": int(p.cum_leb_daily.iloc[-1])},
        {"population": "Lebanon (all)", "basis": "dashboard snapshot (upper bound)",
         "direct_killed": int(p.snap_lebanese_killed.iloc[-1])},
        {"population": "Children (Iran, snapshot)", "basis": "dashboard snapshot",
         "direct_killed": int(p.snap_children_killed.iloc[-1])},
    ]
    t_direct = pd.DataFrame(rows)
    t_direct.to_csv(util.TAB_DIR / "t06_direct_toll.csv", index=False)
    print("t06_direct_toll:")
    print(t_direct.to_string(index=False))
    print(f"  (Iranian civilian share of daily-series deaths: {civ_share_iran:.3f})")

    # ---------------- Projection table ------------------------------------ #
    bases = {
        "Iran": (int(p.cum_iran_daily.iloc[-1]), int(p.snap_iranian_killed.iloc[-1])),
        "Lebanon": (int(p.cum_leb_daily.iloc[-1]), int(p.snap_lebanese_killed.iloc[-1])),
    }
    proj = []
    for pop, (lo_base, hi_base) in bases.items():
        for label, R, note in SCENARIOS:
            proj.append({
                "population": pop, "scenario": label, "ratio_indirect_to_direct": R,
                "note": note,
                "direct_lower": lo_base, "direct_upper": hi_base,
                "indirect_lower": int(round(lo_base * R)),
                "indirect_upper": int(round(hi_base * R)),
                "total_lower": int(round(lo_base * (1 + R))),
                "total_upper": int(round(hi_base * (1 + R))),
            })
    t_proj = pd.DataFrame(proj)
    t_proj.to_csv(util.TAB_DIR / "t06_projection.csv", index=False)
    print("\nt06_projection (Iran):")
    print(t_proj[t_proj.population == "Iran"][
        ["scenario", "ratio_indirect_to_direct", "indirect_lower",
         "indirect_upper", "total_lower", "total_upper"]].to_string(index=False))

    # ---------------- WASH exposure table ---------------------------------- #
    df = util.load_events()
    idx = df.set_index("event_id")["event_description"].fillna("")
    wash = []
    for eid, day, event, exposure in WASH_ROWS:
        assert eid in idx.index, f"WASH anchor {eid} missing"
        wash.append({"event_id": eid, "day": day, "event": event,
                     "population_exposure": exposure,
                     "in_insult_register": bool(
                         (h.event_id == eid).any() and
                         h.loc[h.event_id == eid, "counted"].any())})
    t_wash = pd.DataFrame(wash)
    t_wash.to_csv(util.TAB_DIR / "t06_wash_exposure.csv", index=False)
    print("\nt06_wash_exposure written "
          f"({int(t_wash.in_insult_register.sum())}/{len(t_wash)} in insult register)")

    # ---------------- Figure 7 --------------------------------------------- #
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.4), sharey=False)
    for ax, pop in zip(axes, ("Iran", "Lebanon")):
        sub = t_proj[t_proj.population == pop]
        x = np.arange(len(sub))
        direct_hi = sub.direct_upper.iloc[0]
        ax.bar(x, sub.direct_upper, width=0.62, color=util.C_KILLED, alpha=0.85,
               label="Direct (documented, snapshot)")
        ax.bar(x, sub.indirect_upper, width=0.62, bottom=sub.direct_upper,
               color=util.C_GOLD, alpha=0.75, label="Projected indirect (upper)")
        # lower-bound whisker: total under the daily-series direct basis
        ax.errorbar(x, sub.total_upper, yerr=[sub.total_upper - sub.total_lower,
                                              np.zeros(len(sub))],
                    fmt="none", ecolor="0.3", elinewidth=1.2, capsize=4)
        ax.axhline(direct_hi, color="0.4", lw=0.8, ls=":")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{int(r)}:1" for r in sub.ratio_indirect_to_direct])
        ax.set_xlabel("Assumed indirect:direct ratio")
        ax.set_title(f"{pop}: projected total conflict deaths (Day 170)",
                     loc="left", fontweight="bold", fontsize=9.5)
        if ax is axes[0]:
            ax.set_ylabel("Deaths")
            ax.legend(fontsize=8, loc="upper left")
    fig.text(0.5, -0.02,
             "Projections apply literature indirect:direct mortality ratios to the documented direct toll; "
             "whiskers span the daily-series vs snapshot direct-toll bounds. These are scenario projections, not estimates from these data.",
             ha="center", fontsize=7.4, color="0.25")
    util.savefig(fig, "fig7_indirect_projection")
    plt.close(fig)

    print("\nwrote t06 tables + fig7")


if __name__ == "__main__":
    main()
