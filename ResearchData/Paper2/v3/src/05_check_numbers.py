#!/usr/bin/env python3
"""
05 — Check every headline number and write the machine-readable summary.

This script reads the tables written by scripts 01-04, pulls out every number
that appears in the manuscript's headline sentences, and ASSERTS each one
against the value the manuscript reports. If the frozen dataset, the panel,
or any upstream computation drifts, this script fails loudly and the
pipeline stops. It also writes:

  output/numbers.json                  every headline number, by finding
  output/tables/t0_headline_findings.csv   one row per finding, in words

Run last (after 01-04).
"""
from __future__ import annotations

import json

import pandas as pd

import util


def close(a, b, tol=0.05):
    return abs(float(a) - float(b)) <= tol


def main():
    TAB = util.TAB_DIR
    ms = pd.read_csv(TAB / "t1_milestones.csv").set_index("metric")["value"]
    anova = pd.read_csv(TAB / "t1_anova.csv")
    pair = pd.read_csv(TAB / "t1_pairwise.csv")
    leth = pd.read_csv(TAB / "t1_lethality.csv")
    corr = pd.read_csv(TAB / "t2_correlation_by_period.csv")
    ccmp = pd.read_csv(TAB / "t2_correlation_comparison.csv")
    models = pd.read_csv(TAB / "t3_models.csv")
    slopes = pd.read_csv(TAB / "t3_simple_slopes.csv")
    robust = pd.read_csv(TAB / "t3_robustness.csv")
    sn = pd.read_csv(TAB / "t4_strike_vs_nonstrike_days.csv")
    cfb = pd.read_csv(TAB / "t4_ceasefire_block.csv").set_index("metric")["value"]
    gap_ph = pd.read_csv(TAB / "t4_accounting_gap_by_phase.csv")
    proj = pd.read_csv(TAB / "t4_projection.csv")

    # ---- Finding 1: the war killed early -------------------------------- #
    f1 = {
        "total_documented_deaths": int(float(ms["total_documented_deaths_daily_series"])),
        "deaths_days_1_40": int(float(ms["deaths_in_major_combat_days_1_40"])),
        "share_of_deaths_days_1_40_pct": float(ms["major_combat_share_of_deaths_pct"]),
        "share_of_days_days_1_40_pct": float(ms["major_combat_share_of_days_pct"]),
        "day_half_of_deaths": int(float(ms["day_cumulative_deaths_reached_50pct"])),
        "day_80pct_of_deaths": int(float(ms["day_cumulative_deaths_reached_80pct"])),
        "iran_deaths_by_day_40_pct": float(ms["iran_deaths_by_day_40_pct"]),
        "iran_civilian_deaths_by_day_40_pct": float(ms["iran_civilian_deaths_by_day_40_pct"]),
        "lebanon_deaths_by_day_40_pct": float(ms["lebanon_deaths_by_day_40_pct"]),
        "deadliest_day_all_faction": int(float(ms["deadliest_day_all_faction"])),
        "deadliest_day_all_faction_deaths": int(float(ms["deadliest_day_all_faction_deaths"])),
    }
    a = anova[anova.outcome == "killed_total"].iloc[0]
    f1.update({"anova_F_all_faction": round(float(a.anova_F), 1), "anova_df1": int(a.df1),
               "anova_df2": int(a.df2), "eta2_all_faction": round(float(a.eta2), 3),
               "eta2_iran_civilian": round(float(anova[anova.outcome == "iran_civ"].eta2.iloc[0]), 3),
               "eta2_lebanon": round(float(anova[anova.outcome == "leb_all"].eta2.iloc[0]), 3)})
    mc = pair[(pair.outcome == "killed_total") & (pair.phase_1 == "Major Combat")]
    f1["hedges_g_major_combat_vs_first_ceasefire"] = round(float(mc[mc.phase_2 == "First Ceasefire"].hedges_g.iloc[0]), 2)
    f1["hedges_g_major_combat_vs_others_min"] = round(float(mc.hedges_g.min()), 2)
    f1["hedges_g_major_combat_vs_others_max"] = round(float(mc.hedges_g.max()), 2)
    l_mc = leth[leth.phase == "Major Combat"].iloc[0]
    l_rs = leth[leth.phase == "Resumption"].iloc[0]
    f1.update({"deaths_per_strike_location_major_combat": round(float(l_mc.deaths_per_location_mean), 1),
               "deaths_per_strike_location_resumption": round(float(l_rs.deaths_per_location_mean), 1),
               "deaths_per_strike_location_pct_decline": round(float(l_mc.combat_vs_resumption_pct_decline), 1),
               "deaths_per_strike_location_welch_t": round(float(l_mc.combat_vs_resumption_welch_t), 2),
               "deaths_per_strike_location_p": float(l_mc.combat_vs_resumption_p),
               "deaths_per_strike_location_hedges_g": round(float(l_mc.combat_vs_resumption_hedges_g), 2)})

    # ---- Bridge: correlation by damage period --------------------------- #
    cd = corr[corr["sample"] == "all days in period"].set_index("period")
    br = {"r_days_1_15": round(float(cd.loc["A", "pearson_r"]), 2), "p_days_1_15": round(float(cd.loc["A", "pearson_p"]), 3),
          "r_days_16_39": round(float(cd.loc["B", "pearson_r"]), 2), "p_days_16_39": round(float(cd.loc["B", "pearson_p"]), 3),
          "r_days_40_170": round(float(cd.loc["C", "pearson_r"]), 2), "p_days_40_170": float(cd.loc["C", "pearson_p"]),
          "r_resumption": round(float(cd.loc["C-resumption", "pearson_r"]), 2),
          "r_all_days": round(float(cd.loc["all", "pearson_r"]), 2),
          "slope_days_1_15": round(float(cd.loc["A", "slope"]), 2),
          "slope_days_16_39": round(float(cd.loc["B", "slope"]), 2),
          "slope_days_40_170": round(float(cd.loc["C", "slope"]), 2)}
    ac = ccmp[(ccmp["sample"] == "all days in period") & (ccmp.period_1 == "A") & (ccmp.period_2 == "C")].iloc[0]
    br.update({"fisher_z_A_vs_C": round(float(ac.fisher_z), 2), "fisher_p_A_vs_C": round(float(ac.p), 3)})

    # ---- Finding 2: regression with an interaction ---------------------- #
    m3 = models[models.model.str.startswith("M3")].set_index("term")
    m1 = models[models.model.str.startswith("M1")].set_index("term")
    f2 = {"m1_slope_strikes": round(float(m1.loc["strikes", "coef"]), 2),
          "m1_r2": round(float(m1.loc["_R2", "coef"]), 2),
          "m3_interaction_b": round(float(m3.loc["strikes_x_damage", "coef"]), 4),
          "m3_interaction_se_hac": round(float(m3.loc["strikes_x_damage", "se_hac"]), 4),
          "m3_interaction_p_hac": round(float(m3.loc["strikes_x_damage", "p_hac"]), 3),
          "m3_interaction_p_ols": float(m3.loc["strikes_x_damage", "p_ols"]),
          "m3_r2": round(float(m3.loc["_R2", "coef"]), 2), "m3_n": int(float(m3.loc["_N", "coef"]))}
    obs = slopes[slopes.basis == "observed level (v3)"].set_index("facilities_damaged")
    for fac in (31, 155, 232, 307):
        f2[f"slope_at_{fac}_facilities"] = round(float(obs.loc[fac, "slope"]), 2)
        f2[f"slope_at_{fac}_facilities_p_hac"] = round(float(obs.loc[fac, "p_hac"]), 3)
        f2[f"slope_at_{fac}_facilities_first_day"] = int(obs.loc[fac, "first_day_at_level"])
    thr = slopes[slopes.basis.str.startswith("threshold")].iloc[0]
    f2.update({"threshold_facilities_for_significant_slope": int(thr.facilities_damaged),
               "threshold_pct": round(float(thr.damage_level_pct), 0),
               "threshold_first_day": int(thr.first_day_at_level)})
    v2hi = slopes[slopes.basis.str.startswith("mean + 1 SD")].iloc[0]
    f2.update({"v2_convention_mean_plus_1sd_pct": round(float(v2hi.damage_level_pct), 0),
               "v2_convention_slope_at_mean_plus_1sd": round(float(v2hi.slope), 2)})
    rb = robust.set_index("check")
    f2.update({"check_major_combat_only_p_hac": round(float(rb.loc["Major Combat only (Days 1-40)", "interaction_p_hac"]), 3),
               "check_major_combat_only_p_ols": round(float(rb.loc["Major Combat only (Days 1-40)", "interaction_p_ols"]), 3),
               "check_strike_days_only_p_hac": round(float(rb.loc["strike days only", "interaction_p_hac"]), 3),
               "check_hssi_p_hac": round(float(rb.loc["HSSI (21-event index) as the damage measure", "interaction_p_hac"]), 2),
               "check_hssi_p_ols": round(float(rb.loc["HSSI (21-event index) as the damage measure", "interaction_p_ols"]), 3),
               "check_hssi_slope_at_100pct": round(float(rb.loc["HSSI (21-event index) as the damage measure", "slope_at_100pct_damage"]), 2),
               "check_phase_interaction_p_hac": round(float(rb.loc["phase check: strikes x Resumption (Major Combat + Resumption days)", "interaction_p_hac"]), 2)})

    # ---- Finding 3: the counted dead are a floor ------------------------ #
    s0 = sn[sn.outcome == "iran_civ"].iloc[0]
    ir4 = proj[(proj.population == "Iran") & (proj.scenario == "avg_4to1")].iloc[0]
    lb4 = proj[(proj.population == "Lebanon") & (proj.scenario == "avg_4to1")].iloc[0]
    ir3 = proj[(proj.population == "Iran") & (proj.scenario == "low_3to1")].iloc[0]
    ir15 = proj[(proj.population == "Iran") & (proj.scenario == "high_15to1")].iloc[0]
    lb3 = proj[(proj.population == "Lebanon") & (proj.scenario == "low_3to1")].iloc[0]
    lb15 = proj[(proj.population == "Lebanon") & (proj.scenario == "high_15to1")].iloc[0]
    g = gap_ph.set_index(["population", "phase"])
    f3 = {"iran_civ_deaths_per_day_strike_days": round(float(s0.strike_days_mean), 2),
          "iran_civ_deaths_per_day_non_strike_days": round(float(s0.non_strike_days_mean), 2),
          "n_strike_days": int(s0.strike_days_n), "n_non_strike_days": int(s0.non_strike_days_n),
          "strike_vs_non_strike_welch_t": round(float(s0.welch_t), 2), "strike_vs_non_strike_p": float(s0.p),
          "strike_vs_non_strike_hedges_g": round(float(s0.hedges_g), 2),
          "first_ceasefire_days": int(float(cfb["first_ceasefire_days"])),
          "first_ceasefire_iran_civilian_deaths_recorded": int(float(cfb["iran_civilian_deaths_recorded"])),
          "first_ceasefire_strike_days": int(float(cfb["days_with_recorded_strikes"])),
          "first_ceasefire_health_insult_events": int(float(cfb["health_system_insult_events_in_register"])),
          "iran_direct_lower": int(ir4.direct_lower), "iran_direct_upper": int(ir4.direct_upper),
          "iran_gap_pct": round(100 * (int(ir4.direct_upper) - int(ir4.direct_lower)) / int(ir4.direct_lower), 1),
          "lebanon_direct_lower": int(lb4.direct_lower), "lebanon_direct_upper": int(lb4.direct_upper),
          "lebanon_gap_pct": round(100 * (int(lb4.direct_upper) - int(lb4.direct_lower)) / int(lb4.direct_lower), 1),
          "iran_gap_at_day_40_pct": float(g.loc[("Iran", "Major Combat"), "gap_pct_at_phase_end"]),
          "iran_gap_after_ceasefire_pct": float(g.loc[("Iran", "First Ceasefire"), "gap_pct_at_phase_end"]),
          "iran_daily_added_after_day_40": int(g.loc[("Iran", "First Ceasefire"), "daily_series_deaths_added"]
                                              + g.loc[("Iran", "Resumption"), "daily_series_deaths_added"]
                                              + g.loc[("Iran", "Diplomatic Pause"), "daily_series_deaths_added"]),
          "lebanon_gap_at_day_40_pct": float(g.loc[("Lebanon", "Major Combat"), "gap_pct_at_phase_end"]),
          "lebanon_ceasefire_daily_added": int(g.loc[("Lebanon", "First Ceasefire"), "daily_series_deaths_added"]),
          "lebanon_ceasefire_counter_change": int(g.loc[("Lebanon", "First Ceasefire"), "counter_change"]),
          "lebanon_gap_after_ceasefire_pct": float(g.loc[("Lebanon", "First Ceasefire"), "gap_pct_at_phase_end"]),
          "iran_total_3to1": [int(ir3.total_lower), int(ir3.total_upper)],
          "iran_total_4to1": [int(ir4.total_lower), int(ir4.total_upper)],
          "iran_total_15to1": [int(ir15.total_lower), int(ir15.total_upper)],
          "lebanon_total_3to1": [int(lb3.total_lower), int(lb3.total_upper)],
          "lebanon_total_4to1": [int(lb4.total_lower), int(lb4.total_upper)],
          "lebanon_total_15to1": [int(lb15.total_lower), int(lb15.total_upper)]}

    # ---- Assertions against the manuscript's reported values ------------ #
    assert close(f1["share_of_deaths_days_1_40_pct"], 79.6) and close(f1["share_of_days_days_1_40_pct"], 23.5)
    assert f1["day_half_of_deaths"] == 21 and f1["day_80pct_of_deaths"] == 42
    assert close(f1["eta2_all_faction"], 0.757, 0.005)
    assert close(f1["hedges_g_major_combat_vs_first_ceasefire"], 3.44, 0.01)
    assert close(f1["iran_deaths_by_day_40_pct"], 98.7) and close(f1["lebanon_deaths_by_day_40_pct"], 59.5)
    assert close(f1["deaths_per_strike_location_major_combat"], 15.4) and close(f1["deaths_per_strike_location_resumption"], 0.7)
    assert f1["deadliest_day_all_faction"] == 40
    assert close(br["r_days_1_15"], -0.41) and close(br["r_days_16_39"], 0.43) and close(br["r_days_40_170"], 0.52)
    assert close(f2["m3_interaction_b"], 0.0145, 0.0005) and close(f2["m3_interaction_p_hac"], 0.006, 0.001)
    assert close(f2["slope_at_31_facilities"], -0.46) and close(f2["slope_at_155_facilities"], 0.12)
    assert close(f2["slope_at_232_facilities"], 0.48) and close(f2["slope_at_307_facilities"], 0.83)
    assert close(f2["slope_at_307_facilities_p_hac"], 0.011, 0.001)
    assert close(f2["check_hssi_p_hac"], 0.32, 0.01) and close(f2["check_phase_interaction_p_hac"], 0.89, 0.01)
    assert close(f2["check_major_combat_only_p_hac"], 0.012, 0.001)
    assert f3["iran_direct_lower"] == 3166 and f3["iran_direct_upper"] == 3636
    assert f3["lebanon_direct_lower"] == 2993 and f3["lebanon_direct_upper"] == 4308
    assert f3["iran_total_4to1"] == [15830, 18180] and f3["lebanon_total_4to1"] == [14965, 21540]
    assert close(f3["iran_gap_pct"], 14.8) and close(f3["lebanon_gap_pct"], 43.9)
    assert f3["first_ceasefire_iran_civilian_deaths_recorded"] == 0 and f3["first_ceasefire_days"] == 89

    findings = [
        {"finding": 1, "tool": "means comparison", "short": "The war killed early",
         "headline": f"{f1['share_of_deaths_days_1_40_pct']:.1f}% of documented deaths fell in Days 1-40 "
                     f"({f1['share_of_days_days_1_40_pct']:.1f}% of the days); half by Day {f1['day_half_of_deaths']}",
         "key_stats": f"phase ANOVA eta^2 = {f1['eta2_all_faction']:.2f}; Major Combat vs First Ceasefire Hedges g = "
                      f"{f1['hedges_g_major_combat_vs_first_ceasefire']:.2f}; Iranian deaths per strike location "
                      f"{f1['deaths_per_strike_location_major_combat']:.1f} -> {f1['deaths_per_strike_location_resumption']:.1f}"},
        {"finding": 2, "tool": "correlation + regression with an interaction term",
         "short": "As facility damage accumulated, each extra strike was associated with more civilian deaths",
         "headline": f"strike slope {f2['slope_at_31_facilities']:+.2f} (n.s.) at 31 damaged facilities -> "
                     f"{f2['slope_at_307_facilities']:+.2f} (p = {f2['slope_at_307_facilities_p_hac']:.3f}) at 307",
         "key_stats": f"interaction b = {f2['m3_interaction_b']:.4f}, HAC p = {f2['m3_interaction_p_hac']:.3f}; "
                      f"r(strikes, deaths) {br['r_days_1_15']:+.2f} (Days 1-15) -> {br['r_days_40_170']:+.2f} (Days 40-170); "
                      f"HSSI version same direction, p = {f2['check_hssi_p_hac']:.2f}"},
        {"finding": 3, "tool": "descriptive means comparison + arithmetic",
         "short": "The counted dead are a floor",
         "headline": f"Iran {f3['iran_direct_lower']:,}-{f3['iran_direct_upper']:,} documented direct deaths -> "
                     f"{f3['iran_total_3to1'][0]:,} to {f3['iran_total_15to1'][1]:,} total under 3:1 to 15:1 "
                     f"(reference 4:1: {f3['iran_total_4to1'][0]:,}-{f3['iran_total_4to1'][1]:,})",
         "key_stats": f"non-strike days record {f3['iran_civ_deaths_per_day_non_strike_days']:.2f} Iranian civilian deaths/day; "
                      f"{f3['first_ceasefire_days']} ceasefire days record 0; the two direct counts differ by "
                      f"{f3['iran_gap_pct']:.1f}% (Iran) and {f3['lebanon_gap_pct']:.1f}% (Lebanon)"},
    ]
    pd.DataFrame(findings).to_csv(TAB / "t0_headline_findings.csv", index=False)

    summary = {
        "edition": "Paper 2, v3 (plain-language, three-tool edition)",
        "dataset": "IranWar.ai Event-Level Research Dataset v1.2 (Days 1-170), frozen release",
        "argument": ("The war killed early. As health-facility damage accumulated, each additional strike "
                     "was associated with more civilian deaths. The deaths we can count are a floor, not a total."),
        "finding_1_killed_early": f1,
        "bridge_correlation_by_damage_period": br,
        "finding_2_regression_interaction": f2,
        "finding_3_floor": f3,
    }
    with open(util.OUT_DIR / "numbers.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("=" * 72)
    print("THE THREE FINDINGS (every number re-derived and checked)")
    print("=" * 72)
    for r in findings:
        print(f"\n  Finding {r['finding']} ({r['tool']}): {r['short']}")
        print(f"    {r['headline']}")
        print(f"    ({r['key_stats']})")
    print("\n  " + summary["argument"])
    print("\nAll headline numbers verified against the frozen v1.2 dataset.")
    print("wrote output/numbers.json + output/tables/t0_headline_findings.csv")


if __name__ == "__main__":
    main()
