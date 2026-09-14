#!/usr/bin/env python3
"""
10 — Synthesis: the five statistics, wired together and verified.

Reads the regenerated tables, assembles the headline numbers the manuscript is written
towards, ASSERTS each against the value the manuscript reports (so the pipeline fails
loudly if any number drifts from the frozen dataset), and then checks that each headline
value appears verbatim in the manuscript text.

Writes
  output/synthesis.json                    machine-readable headline numbers
  output/tables/t0_headline_findings.csv   one row per finding

Run last.
"""
from __future__ import annotations

import json
import sys

import pandas as pd

import util

TAB = util.TAB_DIR
MANUSCRIPT = util.PAPER_DIR / "manuscript" / "paper1_major_revision1.md"


def close(a, b, tol):
    return abs(float(a) - float(b)) <= tol


def check(label, got, expected, tol=0.0):
    ok = close(got, expected, tol) if isinstance(expected, (int, float)) else (got == expected)
    print(f"  [{'OK' if ok else 'FAIL'}] {label}: {got} (expected {expected})")
    if not ok:
        raise AssertionError(f"{label}: got {got}, expected {expected}")


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 10 · Synthesis and verification")
    print("=" * 70)

    sd = pd.read_csv(TAB / "t02_same_day.csv")
    ls = pd.read_csv(TAB / "t02_lag_selection.csv")
    gr = pd.read_csv(TAB / "t02_granger.csv")
    irf = pd.read_csv(TAB / "t02_irf_summary.csv")
    rc = pd.read_csv(TAB / "t03_regime_coupling.csv")
    fz = pd.read_csv(TAB / "t03_fisher_pairwise.csv")
    fe = pd.read_csv(TAB / "t04_fevd_orderings.csv")
    rr = pd.read_csv(TAB / "t04_residual_corr.csv")
    ra = pd.read_csv(TAB / "t05_ratio_by_phase.csv")
    sp = pd.read_csv(TAB / "t05_spread.csv")
    wk = pd.read_csv(TAB / "t06_weekly.csv")
    gd = pd.read_csv(TAB / "t06_granger.csv")
    kw = pd.read_csv(TAB / "t06_regime_test.csv")
    dp = pd.read_csv(TAB / "t06_diplomacy_phase.csv")
    bp = pd.read_csv(TAB / "t07_breakpoints.csv")
    bs = pd.read_csv(TAB / "t07_break_selection.csv")
    pl = pd.read_csv(TAB / "t07_placebo_summary.csv")
    se = pd.read_csv(TAB / "t07_sensitivity.csv")
    rs = pd.read_csv(TAB / "t08_resumption.csv")
    fs = pd.read_csv(TAB / "t08_full_sample.csv")
    op = pd.read_csv(TAB / "t09_operationalization.csv")
    cm = pd.read_csv(TAB / "t09_countmodel_retal.csv")
    cp = pd.read_csv(TAB / "t09_casualty_propagation.csv")

    def fevd(order_starts, variable, shock):
        r = fe[fe.ordering.str.startswith(order_starts) & (fe.variable == variable) & (fe.shock_source == shock)]
        return float(r.share_h12.iloc[0])

    def rs_p(measure_starts, direction):
        r = rs[rs.measure.str.startswith(measure_starts) & (rs.direction == direction)]
        return float(r.p_value.iloc[0])

    def fs_p(sample_starts, crit_starts, direction):
        r = fs[fs["sample"].str.startswith(sample_starts) & fs.lag_criterion.str.startswith(crit_starts)
               & (fs.direction == direction)]
        return float(r.p_value.iloc[0])

    S = {
        "argument": ("Strikes and retaliation moved together within the day, not across days; "
                     "the coupling switched on in combat, off in the ceasefire, and on again at the "
                     "resumption; which side set the tempo cannot be identified from daily data; the "
                     "balance of the exchange flipped and retaliation's reach saturated by Day 22; and "
                     "diplomacy tracked the regime, not the week."),
        "finding_1_same_day": {
            "same_day_r_combat": float(sd.pearson_r[0]), "ci95_combat": [float(sd.ci95_low[0]), float(sd.ci95_high[0])],
            "same_day_r_full": float(sd.pearson_r[1]),
            "lag_selected_combat": {k: int(ls.loc[0, k]) for k in ["aic", "bic", "hqic", "fpe"]},
            "granger_p_strikes_to_retal_combat": float(gr.p_value[0]),
            "granger_p_retal_to_strikes_combat": float(gr.p_value[1]),
            "irf_impact_retal_to_strike_shock": float(irf.impact_response_h0[0]),
            "irf_impact_ci95": [float(irf.impact_ci95_low[0]), float(irf.impact_ci95_high[0])],
            "irf_cumulative_7day": float(irf.cumulative_7day[0]),
            "irf_first_horizon_band_includes_zero": int(irf.first_horizon_band_includes_zero[0]),
        },
        "finding_2_regime_switch": {
            "r_combat": float(rc.pearson_r[0]), "r_ceasefire": float(rc.pearson_r[1]),
            "r_resumption": float(rc.pearson_r[2]),
            "p_ceasefire": float(rc.p_value[1]),
            "fisher_z_combat_vs_ceasefire": float(fz.z[0]), "fisher_p_combat_vs_ceasefire": float(fz.p_raw[0]),
            "fisher_p_ceasefire_vs_resumption": float(fz.p_raw[1]),
            "fisher_p_combat_vs_resumption": float(fz.p_raw[2]),
            "holm_p_combat_vs_ceasefire": float(fz.p_holm[0]),
        },
        "finding_3_under_identification": {
            "strikes_first__strike_shocks_share_of_retal_var": fevd("strikes first", "retal", "strikes"),
            "strikes_first__retal_shocks_share_of_strike_var": fevd("strikes first", "strikes", "retal"),
            "retal_first__retal_shocks_share_of_strike_var": fevd("retaliation first", "strikes", "retal"),
            "retal_first__strike_shocks_share_of_retal_var": fevd("retaliation first", "retal", "strikes"),
            "residual_correlation": float(rr.residual_correlation[0]),
            "shared_same_day_share_rho2": float(rr.shared_same_day_share_rho2[0]),
        },
        "finding_4_asymmetry_reach": {
            "ratio_combat": float(ra.strike_retal_ratio[0]),
            "ratio_combat_ci95": [float(ra.ratio_ci95_low[0]), float(ra.ratio_ci95_high[0])],
            "ratio_ceasefire": float(ra.strike_retal_ratio[1]),
            "ratio_resumption": float(ra.strike_retal_ratio[2]),
            "ratio_resumption_ci95": [float(ra.ratio_ci95_low[2]), float(ra.ratio_ci95_high[2])],
            "countries_max": int(sp.max_distinct_countries[0]),
            "day_all_countries_reached": int(sp.first_day_reaching_max[0]),
            "new_countries_after": int(sp.new_countries_after_that_day[0]),
            "days_observed_after": int(sp.days_observed_after[0]),
        },
        "finding_5_diplomacy": {
            "weekly_r": float(wk.pearson_r_all_weeks[0]), "weekly_p": float(wk.p_all_weeks[0]),
            "n_weeks": int(len(wk)),
            "weekly_spearman_rho": float(wk.spearman_rho_all_weeks[0]),
            "granger_p_violence_to_diplomacy": float(gd.p_value[0]),
            "granger_p_diplomacy_to_violence": float(gd.p_value[1]),
            "diplomacy_per_day_by_phase": {r.phase: float(r.diplomatic_per_day) for r in dp.itertuples()},
            "kruskal_wallis_H_diplomacy": float(kw.H[0]), "kruskal_wallis_p_diplomacy": float(kw.p_value[0]),
            "kruskal_wallis_eps2_diplomacy": float(kw.epsilon_squared[0]),
        },
        "regimes_and_placebo": {
            "k_selected": int(bs.n_segments[bs.bic.idxmin()]),
            "break_days": [int(b) for b in bp.detected_break_day],
            "gaps_to_documented_boundaries": [int(g) for g in bp.gap_days],
            "bic_gain_observed": float(pl.observed_bic_gain[0]),
            "placebo": {r.null: {"share_selecting_k6": float(r.share_selecting_k6),
                                 "max_bic_gain": float(r.max_bic_gain),
                                 "p_value": float(r.p_value_gain_ge_observed)} for r in pl.itertuples()},
            "macro_breaks_recovered_under_criteria": {
                c: int(se[se.criterion == c].n_macro_recovered_within_7d.min()) for c in ["parent", "yao", "lwz"]},
        },
        "scoping": {
            "resumption_n_days": int(rs.n_days[0]), "resumption_n_obs_used": int(rs.n_obs_used[0]),
            "resumption_p_retal_to_strikes_primary": rs_p("primary", "retal -> strikes"),
            "resumption_p_strikes_to_retal_primary": rs_p("primary", "strikes -> retal"),
            "resumption_p_retal_to_strikes_raw_rows": rs_p("raw", "retal -> strikes"),
            "resumption_ccf_retal_leads": float(rs.ccf_retal_leads_strikes_1d[0]),
            "resumption_ccf_strikes_lead": float(rs.ccf_strikes_lead_retal_1d[0]),
            "full_naive_p_retal_to_strikes_aic": fs_p("Full sample, naive", "AIC", "retal -> strikes"),
            "full_demeaned4_p_retal_to_strikes_aic": fs_p("Full sample, regime-demeaned (4", "AIC", "retal -> strikes"),
            "full_demeaned4_p_retal_to_strikes_lag1": fs_p("Full sample, regime-demeaned (4", "HQIC", "retal -> strikes"),
            "full_demeaned6_p_retal_to_strikes_aic": fs_p("Full sample, regime-demeaned (6", "AIC", "retal -> strikes"),
            "full_demeaned6_p_retal_to_strikes_lag1": fs_p("Full sample, regime-demeaned (6", "BIC", "retal -> strikes"),
            "any_strikes_to_retal_significant": bool(fs[fs.direction == "strikes -> retal"].significant_05.any()),
        },
        "robustness": {
            "same_day_r_combat_by_measure": {r.measure: float(r.same_day_r) for r in op[op["sample"].str.startswith("combat")].itertuples()},
            "nb_full_same_day_strikes_IRR": float(cm[(cm["sample"].str.startswith("full")) & (cm.term == "strikes_L0")].IRR.iloc[0]),
            "nb_full_same_day_strikes_p": float(cm[(cm["sample"].str.startswith("full")) & (cm.term == "strikes_L0")].p_value.iloc[0]),
            "casualty_combat_min_p": float(cp[cp["sample"].str.startswith("combat")].p_value.min()),
        },
    }

    # ---------------- assertions against the manuscript's numbers -------- #
    print("\n--- Verifying headline numbers ---")
    f1, f2, f3, f4, f5 = (S["finding_1_same_day"], S["finding_2_regime_switch"],
                          S["finding_3_under_identification"], S["finding_4_asymmetry_reach"],
                          S["finding_5_diplomacy"])
    rp, sc, rb = S["regimes_and_placebo"], S["scoping"], S["robustness"]
    check("same-day r, combat", f1["same_day_r_combat"], 0.687, 0.0005)
    check("same-day r, full", f1["same_day_r_full"], 0.831, 0.0005)
    check("lags selected (combat) all zero", sum(f1["lag_selected_combat"].values()), 0)
    check("Granger strikes->retal p (combat)", f1["granger_p_strikes_to_retal_combat"], 0.7765, 0.0005)
    check("Granger retal->strikes p (combat)", f1["granger_p_retal_to_strikes_combat"], 0.4409, 0.0005)
    check("IRF impact response", f1["irf_impact_retal_to_strike_shock"], 2.28, 0.005)
    check("IRF cumulative 7-day", f1["irf_cumulative_7day"], 4.55, 0.005)
    check("IRF band includes zero from horizon", f1["irf_first_horizon_band_includes_zero"], 1)
    check("r combat", f2["r_combat"], 0.687, 0.0005)
    check("r ceasefire", f2["r_ceasefire"], 0.178, 0.0005)
    check("r resumption", f2["r_resumption"], 0.662, 0.0005)
    check("Fisher z combat vs ceasefire", f2["fisher_z_combat_vs_ceasefire"], 3.374, 0.0005)
    check("Fisher p combat vs ceasefire", f2["fisher_p_combat_vs_ceasefire"], 0.0007, 0.00005)
    check("Fisher p ceasefire vs resumption", f2["fisher_p_ceasefire_vs_resumption"], 0.0129, 0.00005)
    check("FEVD strikes-first: strike shocks -> retal var", f3["strikes_first__strike_shocks_share_of_retal_var"], 0.408, 0.0005)
    check("FEVD strikes-first: retal shocks -> strike var", f3["strikes_first__retal_shocks_share_of_strike_var"], 0.022, 0.0005)
    check("FEVD retal-first: retal shocks -> strike var", f3["retal_first__retal_shocks_share_of_strike_var"], 0.437, 0.0005)
    check("FEVD retal-first: strike shocks -> retal var", f3["retal_first__strike_shocks_share_of_retal_var"], 0.002, 0.0005)
    check("residual correlation", f3["residual_correlation"], 0.62, 0.0005)
    check("rho^2", f3["shared_same_day_share_rho2"], 0.385, 0.0005)
    check("ratio combat", f4["ratio_combat"], 0.68, 0.005)
    check("ratio resumption", f4["ratio_resumption"], 1.42, 0.005)
    check("countries max", f4["countries_max"], 13)
    check("day all countries reached", f4["day_all_countries_reached"], 22)
    check("new countries after", f4["new_countries_after"], 0)
    check("weekly r", f5["weekly_r"], 0.06, 0.0005)
    check("Granger violence->diplomacy p", f5["granger_p_violence_to_diplomacy"], 0.7495, 0.0005)
    check("Granger diplomacy->violence p", f5["granger_p_diplomacy_to_violence"], 0.9102, 0.0005)
    check("diplomacy/day ceasefire", f5["diplomacy_per_day_by_phase"]["First Ceasefire"], 3.22, 0.005)
    check("diplomacy/day resumption", f5["diplomacy_per_day_by_phase"]["Resumption"], 0.39, 0.005)
    check("regimes selected", rp["k_selected"], 6)
    check("break days", rp["break_days"], [7, 23, 40, 131, 147])
    check("gaps to documented boundaries", rp["gaps_to_documented_boundaries"][2:], [-1, 1, -6])
    check("observed BIC gain", rp["bic_gain_observed"], 170.3, 0.05)
    for null, v in rp["placebo"].items():
        check(f"placebo p ({null[:24]})", v["p_value"], 0.001, 0.0005)
    check("macro breaks under parent BIC", rp["macro_breaks_recovered_under_criteria"]["parent"], 3)
    check("macro breaks under Yao BIC", rp["macro_breaks_recovered_under_criteria"]["yao"], 3)
    check("macro breaks under LWZ", rp["macro_breaks_recovered_under_criteria"]["lwz"], 1)
    check("resumption n days", sc["resumption_n_days"], 23)
    check("resumption retal->strikes p (primary)", sc["resumption_p_retal_to_strikes_primary"], 0.0264, 0.0005)
    check("resumption retal->strikes p (raw rows)", sc["resumption_p_retal_to_strikes_raw_rows"], 0.7774, 0.0005)
    check("full naive retal->strikes p (AIC)", sc["full_naive_p_retal_to_strikes_aic"], 0.0001, 0.00005)
    check("full demeaned-4 retal->strikes p (AIC)", sc["full_demeaned4_p_retal_to_strikes_aic"], 0.0013, 0.00005)
    check("full demeaned-4 retal->strikes p (lag 1)", sc["full_demeaned4_p_retal_to_strikes_lag1"], 0.0552, 0.00005)
    check("full demeaned-6 retal->strikes p (lag 1)", sc["full_demeaned6_p_retal_to_strikes_lag1"], 0.2578, 0.00005)
    check("strikes->retal never significant", sc["any_strikes_to_retal_significant"], False)
    check("NB full same-day strikes IRR", rb["nb_full_same_day_strikes_IRR"], 1.141, 0.0005)
    check("casualty model, combat, all p > 0.05", rb["casualty_combat_min_p"] > 0.05, True)

    # ---------------- headline table + json ------------------------------ #
    head = pd.DataFrame([
        {"finding": 1, "claim": "Reciprocity is same-day, not lagged",
         "statistic": f"same-day r = {f1['same_day_r_combat']:.2f} in combat; every criterion selects lag 0; "
                      f"Granger p = {f1['granger_p_strikes_to_retal_combat']:.2f} and {f1['granger_p_retal_to_strikes_combat']:.2f}"},
        {"finding": 2, "claim": "The coupling switches with the political regime",
         "statistic": f"r = {f2['r_combat']:.2f} (combat) vs {f2['r_ceasefire']:.2f} (ceasefire) vs "
                      f"{f2['r_resumption']:.2f} (resumption); Fisher z p = {f2['fisher_p_combat_vs_ceasefire']:.4f}"},
        {"finding": 3, "claim": "Who set the tempo is not identified at daily resolution",
         "statistic": f"FEVD {100*f3['strikes_first__strike_shocks_share_of_retal_var']:.0f}% vs "
                      f"{100*f3['strikes_first__retal_shocks_share_of_strike_var']:.0f}% under one ordering; "
                      f"{100*f3['retal_first__retal_shocks_share_of_strike_var']:.0f}% vs "
                      f"{100*f3['retal_first__strike_shocks_share_of_retal_var']:.1f}% under the other"},
        {"finding": 4, "claim": "The balance flipped and retaliation's reach saturated early",
         "statistic": f"strike:retaliation ratio {f4['ratio_combat']:.2f} -> {f4['ratio_resumption']:.2f}; "
                      f"{f4['countries_max']} countries by Day {f4['day_all_countries_reached']}, none after"},
        {"finding": 5, "claim": "Diplomacy moves with the regime, not the week",
         "statistic": f"weekly r = {f5['weekly_r']:.2f} (n.s.); diplomacy/day {f5['diplomacy_per_day_by_phase']['First Ceasefire']:.2f} "
                      f"(ceasefire) vs {f5['diplomacy_per_day_by_phase']['Resumption']:.2f} (resumption), Kruskal-Wallis p < 0.001"},
    ])
    util.write_table(head, "t0_headline_findings.csv")
    with open(util.OUT_DIR / "synthesis.json", "w") as fh:
        json.dump(S, fh, indent=2)
    print("  wrote output/synthesis.json")

    # ---------------- manuscript cross-check ----------------------------- #
    needles = [
        "r = 0.69", "r = 0.18", "r = 0.66", "p = 0.0007", "41%", "2%", "44%", "0.2%",
        "0.68", "1.42", "13 countries", "Day 22", "r = 0.06", "p = 0.026", "1, 1, and 6 days",
        "p = 0.001", "p = 0.055", "p = 0.78",
    ]
    if MANUSCRIPT.exists():
        text = MANUSCRIPT.read_text(encoding="utf8")
        missing = [s for s in needles if s not in text]
        print(f"\n--- Manuscript cross-check ({MANUSCRIPT.name}) ---")
        for s in needles:
            print(f"  [{'OK' if s not in missing else 'MISSING'}] {s!r}")
        if missing:
            raise AssertionError(f"headline strings missing from manuscript: {missing}")
    else:
        print(f"\n  [skip] manuscript not found at {MANUSCRIPT}")

    print("\nAll headline numbers verified.")


if __name__ == "__main__":
    sys.exit(main())
