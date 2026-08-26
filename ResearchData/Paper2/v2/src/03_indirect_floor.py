#!/usr/bin/env python3
"""
03 — FINDING 6: the deaths we can count are only a floor.

The student's third finding, and the one she said hit hardest, because she sees
it from the ward side: "The four who die indirectly are the patient whose
surgery gets postponed because the theatre is damaged, the mother who delivers
without skilled attendance because the midwife evacuated, or the dialysis
patient who misses several sessions in a row. They do not show up in the strike
count."

The daily "estimated killed" series records DIRECT, reported deaths. Conflict
epidemiology is unanimous that such counts are the floor, not the total: deaths
from disrupted care, displacement, water failure, and disease follow with a lag
and rarely enter strike-day tallies (Guha-Sapir & van Panhuis 2004; Geneva
Declaration 2008; Checchi & Roberts 2008; Jawad et al. 2020).

This script PROJECTS — it does not estimate from these data — the indirect
burden implied by literature indirect:direct ratios applied to the documented
direct toll, under explicit assumptions:
  R = 1:1  (very conservative floor)
  R = 3:1  (low end of the Geneva Declaration range)
  R = 4:1  (Geneva Declaration cross-conflict average)  <- headline
  R = 15:1 (upper end; weakest health systems)
Each projection is computed on BOTH direct-toll bounds (daily-series sum =
lower; dashboard cumulative snapshot = upper), carrying the dataset's own
measurement uncertainty forward. Computations are identical to parent 06.

Also summarizes the WASH / environmental exposure events that make the
mechanism concrete at household scale (population figures quoted verbatim from
source events).

Outputs:
  output/tables/t6_direct_toll.csv
  output/tables/t6_projection.csv
  output/tables/t6_wash_exposure.csv
  output/figures/fig3_indirect_floor.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import util

SCENARIOS = [
    ("floor_1to1", 1.0, "Very conservative floor"),
    ("low_3to1", 3.0, "Low end of Geneva Declaration (2008) range"),
    ("avg_4to1", 4.0, "Geneva Declaration (2008) cross-conflict average"),
    ("high_15to1", 15.0, "Upper end of reported range (weakest health systems)"),
]

# WASH / environmental exposure events with population-at-risk figures quoted
# in the dataset (event ids verified against the register at run time).
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
         "basis": "peak pre-re-anchoring snapshot (Day 56)",
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
    t_direct.to_csv(util.TAB_DIR / "t6_direct_toll.csv", index=False)

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
                "note": note, "direct_lower": lo_base, "direct_upper": hi_base,
                "indirect_lower": int(round(lo_base * R)),
                "indirect_upper": int(round(hi_base * R)),
                "total_lower": int(round(lo_base * (1 + R))),
                "total_upper": int(round(hi_base * (1 + R))),
            })
    t_proj = pd.DataFrame(proj)
    t_proj.to_csv(util.TAB_DIR / "t6_projection.csv", index=False)

    ir4 = t_proj[(t_proj.population == "Iran") & (t_proj.scenario == "avg_4to1")].iloc[0]
    lb4 = t_proj[(t_proj.population == "Lebanon") & (t_proj.scenario == "avg_4to1")].iloc[0]
    print("FINDING 6 — the direct toll is a floor")
    print(f"  documented direct deaths (Day 170):")
    print(f"    Iran    {ir4.direct_lower:,}-{ir4.direct_upper:,}   "
          f"(civilian share of Iranian deaths: {civ_share_iran:.1%})")
    print(f"    Lebanon {lb4.direct_lower:,}-{lb4.direct_upper:,}")
    print(f"  at the 4:1 literature average, projected TOTAL deaths:")
    print(f"    Iran    {ir4.total_lower:,}-{ir4.total_upper:,}  "
          f"(indirect {ir4.indirect_lower:,}-{ir4.indirect_upper:,})")
    print(f"    Lebanon {lb4.total_lower:,}-{lb4.total_upper:,}  "
          f"(indirect {lb4.indirect_lower:,}-{lb4.indirect_upper:,})")

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
    t_wash.to_csv(util.TAB_DIR / "t6_wash_exposure.csv", index=False)
    print(f"\n  WASH exposure rows written "
          f"({int(t_wash.in_insult_register.sum())}/{len(t_wash)} in the insult register)")

    # ==================================================================== #
    # Figure 3 — the floor and the tail
    # ==================================================================== #
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4), sharey=False)
    for ax, pop in zip(axes, ("Iran", "Lebanon")):
        sub = t_proj[t_proj.population == pop]
        x = np.arange(len(sub))
        direct_hi = sub.direct_upper.iloc[0]
        ax.bar(x, sub.direct_upper, width=0.62, color=util.C_KILLED, alpha=0.85,
               label="Direct (documented)")
        ax.bar(x, sub.indirect_upper, width=0.62, bottom=sub.direct_upper,
               color=util.C_GOLD, alpha=0.78, label="Projected indirect")
        ax.errorbar(x, sub.total_upper, yerr=[sub.total_upper - sub.total_lower,
                                              np.zeros(len(sub))],
                    fmt="none", ecolor="0.3", elinewidth=1.2, capsize=4)
        ax.axhline(direct_hi, color="0.4", lw=0.8, ls=":")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{int(r)}:1" for r in sub.ratio_indirect_to_direct])
        ax.set_xlabel("Assumed indirect:direct ratio")
        ax.set_title(f"{pop}: documented floor vs projected total (Day 170)",
                     loc="left", fontweight="bold", fontsize=9.5)
        if ax is axes[0]:
            ax.set_ylabel("Deaths")
            ax.legend(fontsize=8, loc="upper left")
    fig.text(0.5, -0.02,
             "Bars use the snapshot (upper) direct basis; whiskers span down to the daily-series (lower) basis. "
             "These are scenario projections under literature ratios, not estimates from these data.",
             ha="center", fontsize=7.4, color="0.25")
    util.savefig(fig, "fig3_indirect_floor")
    plt.close(fig)

    print("\nwrote t6 tables + fig3_indirect_floor")


if __name__ == "__main__":
    main()
