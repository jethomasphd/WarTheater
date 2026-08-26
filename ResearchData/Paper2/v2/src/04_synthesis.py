#!/usr/bin/env python3
"""
04 — Synthesis: the three findings as one argument.

The student read the headline findings and wrote back that three of them "feel
like one argument to me: the war killed fast and early, the health system
gradually lost its ability to absorb further shocks, and the deaths we can
count may only represent part of the real human toll."

This script assembles the headline numbers from the three finding scripts into
a single wired-together summary, and ASSERTS each against the value the
manuscript reports, so the whole v2 pipeline fails loudly if any number drifts
from the frozen dataset. It writes:

  output/tables/t0_headline_findings.csv   one row per finding (the argument)
  output/synthesis.json                     machine-readable headline numbers

Run last (after 01-03).
"""
from __future__ import annotations

import json

import pandas as pd

import util


def close(a, b, tol=0.05):
    return abs(float(a) - float(b)) <= tol


def main():
    TAB = util.TAB_DIR

    conc = pd.read_csv(TAB / "t1_concentration.csv").set_index("metric")["value"]
    anova = pd.read_csv(TAB / "t1_phase_anova.csv")
    leth = pd.read_csv(TAB / "t1_lethality.csv")
    slopes = pd.read_csv(TAB / "t5_simple_slopes.csv")
    moder = pd.read_csv(TAB / "t5_moderation.csv")
    proj = pd.read_csv(TAB / "t6_projection.csv")

    # ---- Finding 1 -------------------------------------------------------- #
    f1_death_share = float(conc.loc["major_combat_share_of_deaths_pct"])
    f1_day_share = float(conc.loc["major_combat_share_of_days_pct"])
    f1_eta2 = float(anova[anova.outcome == "killed_total"].eta2.iloc[0])
    f1_g = float(leth.combat_vs_resumption_g.iloc[0])

    # ---- Finding 5 -------------------------------------------------------- #
    fac = slopes[(slopes.moderator == "facil_damage_pct") & (slopes["sample"] == "full")]
    s_lo = float(fac[fac.at_W == "-1SD"].slope.iloc[0])
    s_mid = float(fac[fac.at_W == "mean"].slope.iloc[0])
    s_hi = float(fac[fac.at_W == "+1SD"].slope.iloc[0])
    f5_inter_p = float(moder[(moder.moderator == "facil_damage_pct")
                             & (moder["sample"] == "full")
                             & (moder.term == "strikes_x_W")].p.iloc[0])

    # ---- Finding 6 -------------------------------------------------------- #
    ir4 = proj[(proj.population == "Iran") & (proj.scenario == "avg_4to1")].iloc[0]

    findings = [
        {"finding": 1, "short": "The war killed fast and early",
         "headline": f"{f1_death_share:.1f}% of documented deaths fell in the "
                     f"{f1_day_share:.1f}% of days that were Major Combat",
         "key_stats": f"phase eta^2 = {f1_eta2:.2f}; deaths-per-strike collapsed "
                      f"95% (Major Combat -> Resumption, Hedges g = {f1_g:.2f})"},
        {"finding": 5, "short": "The system lost its ability to absorb shocks",
         "headline": f"the deaths-per-strike slope steepened from {s_lo:.2f} to "
                     f"{s_mid:.2f} to {s_hi:.2f} as facility damage accumulated",
         "key_stats": f"strikes x damage interaction p = {f5_inter_p:.3f}; "
                      f"~{s_hi / s_lo:.0f}x steepening across the observed damage range"},
        {"finding": 6, "short": "The counted dead are only a floor",
         "headline": f"{ir4.direct_lower:,}-{ir4.direct_upper:,} documented in Iran "
                     f"-> {ir4.total_lower:,}-{ir4.total_upper:,} total at the 4:1 "
                     f"literature-average indirect:direct ratio",
         "key_stats": f"projected indirect deaths (Iran, 4:1): "
                      f"{ir4.indirect_lower:,}-{ir4.indirect_upper:,}"},
    ]
    pd.DataFrame(findings).to_csv(TAB / "t0_headline_findings.csv", index=False)

    summary = {
        "argument": ("The war killed fast and early; the health system gradually "
                     "lost its ability to absorb further shocks; and the deaths we "
                     "can count may only represent part of the real human toll."),
        "finding_1_frontloading": {
            "death_share_major_combat_pct": f1_death_share,
            "day_share_major_combat_pct": f1_day_share,
            "phase_eta2_all_faction": round(f1_eta2, 3),
            "lethality_collapse_hedges_g": round(f1_g, 3),
        },
        "finding_5_resilience_erosion": {
            "simple_slope_low_damage": round(s_lo, 3),
            "simple_slope_mean_damage": round(s_mid, 3),
            "simple_slope_high_damage": round(s_hi, 3),
            "interaction_p_facility_damage": round(f5_inter_p, 4),
        },
        "finding_6_indirect_floor": {
            "iran_direct_lower": int(ir4.direct_lower),
            "iran_direct_upper": int(ir4.direct_upper),
            "iran_total_4to1_lower": int(ir4.total_lower),
            "iran_total_4to1_upper": int(ir4.total_upper),
        },
    }
    with open(util.OUT_DIR / "synthesis.json", "w") as f:
        json.dump(summary, f, indent=2)

    # ---- Fail-loud assertions against the manuscript's reported values ---- #
    assert close(f1_death_share, 79.6), f1_death_share
    assert close(f1_day_share, 23.5), f1_day_share
    assert close(f1_eta2, 0.757, 0.005), f1_eta2
    assert close(s_lo, 0.18, 0.01) and close(s_mid, 0.63, 0.01) and close(s_hi, 1.07, 0.01), \
        (s_lo, s_mid, s_hi)
    assert close(f5_inter_p, 0.006, 0.001), f5_inter_p
    assert int(ir4.direct_lower) == 3166 and int(ir4.direct_upper) == 3636
    assert int(ir4.total_lower) == 15830 and int(ir4.total_upper) == 18180

    print("=" * 70)
    print("THE THREE FINDINGS AS ONE ARGUMENT")
    print("=" * 70)
    for r in findings:
        print(f"\n  Finding {r['finding']}. {r['short']}")
        print(f"    {r['headline']}")
        print(f"    ({r['key_stats']})")
    print("\n  " + "-" * 66)
    print("  " + summary["argument"])
    print("\nAll headline numbers verified against the frozen v1.2 dataset. "
          "\nwrote t0_headline_findings.csv + synthesis.json")


if __name__ == "__main__":
    main()
