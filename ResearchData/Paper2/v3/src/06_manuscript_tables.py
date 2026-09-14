#!/usr/bin/env python3
"""
06 — Render the manuscript's tables from the result CSVs, and check that the
     manuscript contains them verbatim.

Why this exists
---------------
The manuscript (manuscript/paper2_v3.md) is the canonical text. Its tables
are NOT typed by hand: this script renders each one from the CSVs in
output/tables/ into output/manuscript_tables.md, and the author pastes the
rendered blocks into the manuscript. When run after the manuscript exists,
the script also CHECKS that every rendered table appears in the manuscript
character for character. If a number changes upstream, the check fails and
the pipeline stops — so the paper cannot silently drift from the analysis.

  python3 06_manuscript_tables.py            # render + check (check skipped if no manuscript yet)
  python3 06_manuscript_tables.py --no-check # render only

Formatting conventions (APA-style, kept simple)
-----------------------------------------------
* p-values: "< .001" below .001, otherwise three decimals with no leading zero.
* Thousands separated by commas. Means and SDs to one or two decimals.
"""
from __future__ import annotations

import sys

import pandas as pd

import util

MAN = util.PAPER_DIR / "manuscript" / "paper2_v3.md"
OUT = util.OUT_DIR / "manuscript_tables.md"


def pfmt(p):
    p = float(p)
    if p < 0.001:
        return "< .001"
    return f"= {p:.3f}".replace("= 0.", "= .")


def ptxt(p):
    """p-value without the leading '= '/'< ' operator handling for table cells."""
    p = float(p)
    return "< .001" if p < 0.001 else f"{p:.3f}"[1:] if p < 1 else "1.000"


def c(x):
    return f"{int(round(float(x))):,}"


def md_table(headers, rows, aligns=None):
    aligns = aligns or (["---"] * len(headers))
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(aligns) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(str(v) for v in r) + " |")
    return "\n".join(lines)


def render_all():
    T = util.TAB_DIR
    blocks = {}

    # ---- Table 1: deaths per day by phase --------------------------------- #
    ph = pd.read_csv(T / "t1_phase_summary.csv")
    rows = []
    for _, r in ph.iterrows():
        rows.append([r.phase, r.days, f"{r.share_of_days_pct:.1f}%",
                     f"{r.killed_total_mean:.1f} ({r.killed_total_sd:.1f})", c(r.killed_total_total),
                     f"{r.share_of_deaths_pct:.1f}%",
                     f"{r.iran_civ_mean:.2f} ({r.iran_civ_sd:.2f})", f"{r.leb_mean:.1f} ({r.leb_sd:.1f})"])
    blocks["Table 1"] = md_table(
        ["Phase", "Days", "Share of days", "All-faction deaths per day, mean (SD)", "Total deaths",
         "Share of deaths", "Iranian civilian deaths per day, mean (SD)", "Lebanese deaths per day, mean (SD)"],
        rows)

    # ---- Table 2: pairwise comparisons (all-faction) ---------------------- #
    pw = pd.read_csv(T / "t1_pairwise.csv")
    pw = pw[pw.outcome == "killed_total"]
    rows = []
    for _, r in pw.iterrows():
        rows.append([f"{r.phase_1} vs {r.phase_2}",
                     f"{r.mean_diff:.1f} ({r.diff_ci95_low:.1f} to {r.diff_ci95_high:.1f})",
                     f"{r.welch_t:.2f} ({r.welch_df:.1f})", ptxt(r.p_holm), f"{r.hedges_g:.2f}"])
    blocks["Table 2"] = md_table(
        ["Comparison", "Difference in mean deaths per day (95% CI)", "Welch t (df)", "Holm-adjusted p", "Hedges' g"],
        rows)

    # ---- Table 3: deaths per strike location ------------------------------ #
    le = pd.read_csv(T / "t1_lethality.csv")
    rows = []
    for _, r in le.iterrows():
        if r.n_strike_days == 0:
            rows.append([r.phase, "0", "—", "—", "—", "—"])
            continue
        rows.append([r.phase, int(r.n_strike_days), f"{r.strike_locations_per_day:.1f}",
                     f"{r.iran_deaths_per_day:.1f}",
                     f"{r.deaths_per_location_mean:.1f} ({r.deaths_per_location_sd:.1f})",
                     f"{r.deaths_per_location_median:.1f}"])
    blocks["Table 3"] = md_table(
        ["Phase", "Strike days", "Strike locations per strike day", "Iranian deaths per strike day",
         "Iranian deaths per strike location, mean (SD)", "Median"], rows)

    # ---- Table 4: correlation by period ----------------------------------- #
    co = pd.read_csv(T / "t2_correlation_by_period.csv")
    co = co[co["sample"] == "all days in period"]
    names = {"A": "A. Days 1–15 (0 → 31 facilities; ≤ 10% of final damage)",
             "B": "B. Days 16–39 (31 → 307 facilities; 10% → 99%)",
             "C": "C. Days 40–170 (307 → 309 facilities; ≈ 100%)",
             "C-resumption": "Resumption only, Days 130–152 (inside C)",
             "all": "All days, 1–170"}
    rows = []
    for _, r in co.iterrows():
        rows.append([names[r.period], int(r.n_days), f"{r.strikes_per_day:.1f}", f"{r.civ_deaths_per_day:.1f}",
                     f"{r.pearson_r:+.2f} ({ptxt(r.pearson_p)})",
                     f"{r.slope:+.2f} ({r.slope_ci95_low:.2f} to {r.slope_ci95_high:.2f})"])
    blocks["Table 4"] = md_table(
        ["Period", "Days", "Strike locations per day", "Iranian civilian deaths per day",
         "Pearson r (p)", "Slope: extra deaths per extra strike location (95% CI)"], rows)

    # ---- Table 5: regression models --------------------------------------- #
    mo = pd.read_csv(T / "t3_models.csv")
    model_names = {"M1 strikes only": "M1: strikes only", "M2 strikes + damage": "M2: strikes + damage",
                   "M3 strikes x damage (interaction)": "M3: strikes × damage (interaction)"}
    term_names = {"const": "Intercept", "strikes": "Strikes per day", "damage_pct": "Facility damage (% of final)",
                  "strikes_c": "Strikes per day (centered)", "damage_c": "Facility damage (centered)",
                  "strikes_x_damage": "Strikes × damage (interaction)"}
    rows = []
    for _, r in mo.iterrows():
        if r.term == "_R2":
            rows.append([model_names[r.model], "R²", f"{r.coef:.2f}", "", "", "", ""])
        elif r.term == "_N":
            rows.append([model_names[r.model], "N (days)", str(int(r.coef)), "", "", "", ""])
        else:
            d = 4 if r.term == "strikes_x_damage" else 3   # the interaction is small; show 4 decimals
            rows.append([model_names[r.model], term_names[r.term], f"{r.coef:.{d}f}", f"{r.se_ols:.{d}f}", ptxt(r.p_ols),
                         f"{r.se_hac:.{d}f}", ptxt(r.p_hac)])
    blocks["Table 5"] = md_table(
        ["Model", "Term", "b", "Ordinary SE", "Ordinary p", "HAC SE", "HAC p"], rows)

    # ---- Table 6: simple slopes ------------------------------------------- #
    ss = pd.read_csv(T / "t3_simple_slopes.csv")
    rows = []
    for _, r in ss[ss.basis == "observed level (v3)"].iterrows():
        rows.append([int(r.facilities_damaged), f"{r.damage_level_pct:.0f}%", f"Day {int(r.first_day_at_level)}",
                     f"{r.slope:+.2f} ({r.se_hac:.2f})", ptxt(r.p_hac)])
    thr = ss[ss.basis.str.startswith("threshold")].iloc[0]
    rows.append([f"{int(thr.facilities_damaged)} (threshold)", f"{thr.damage_level_pct:.0f}%",
                 f"Day {int(thr.first_day_at_level)}", f"{thr.slope:+.2f}",
                 "slope is significant (p < .05) from this level upward"])
    blocks["Table 6"] = md_table(
        ["Damaged facilities", "% of final (309)", "First reached", "Strike slope (HAC SE)", "HAC p"], rows)

    # ---- Table 7: robustness ---------------------------------------------- #
    rb = pd.read_csv(T / "t3_robustness.csv")
    rows = []
    for _, r in rb.iterrows():
        rows.append([r.check.replace("primary: all days", "Primary model: all days")
                     .replace("phase check: strikes x Resumption (Major Combat + Resumption days)",
                              "Phase check: strikes × Resumption (Major Combat + Resumption days only)")
                     .replace("HSSI (21-event index) as the damage measure", "HSSI (21-event stress index) as the damage measure")
                     .replace("kinetic days only (strikes or retaliation)", "Kinetic days only (a strike or a retaliation)")
                     .replace("strike days only", "Strike days only").replace("HSSI, Strike days only", "HSSI, strike days only"),
                     int(r.n), f"{r.interaction_b:+.4f}", ptxt(r.interaction_p_hac), ptxt(r.interaction_p_ols)])
    blocks["Table 7"] = md_table(["Check", "N (days)", "Interaction b", "HAC p", "Ordinary p"], rows)

    # ---- Table 8: strike vs non-strike days ------------------------------- #
    sn = pd.read_csv(T / "t4_strike_vs_nonstrike_days.csv")
    rows = []
    for _, r in sn.iterrows():
        rows.append([r.label, f"{r.strike_days_mean:.2f} ({r.strike_days_sd:.2f}); n = {int(r.strike_days_n)}",
                     f"{r.non_strike_days_mean:.2f} ({r.non_strike_days_sd:.2f}); n = {int(r.non_strike_days_n)}",
                     c(r.non_strike_days_total), f"{r.welch_t:.2f}", ptxt(r.p), f"{r.hedges_g:.2f}"])
    blocks["Table 8"] = md_table(
        ["Outcome", "Strike days: mean (SD)", "Non-strike days: mean (SD)", "Total deaths recorded on non-strike days",
         "Welch t", "p", "Hedges' g"], rows)

    # ---- Table 9: accounting gap by phase --------------------------------- #
    gp = pd.read_csv(T / "t4_accounting_gap_by_phase.csv")
    rows = []
    for _, r in gp.iterrows():
        rows.append([r.population, f"{r.phase} ({r.days})", c(r.daily_series_deaths_added),
                     "—" if pd.isna(r.counter_change) else f"{int(r.counter_change):+,}",
                     c(r.counter_at_phase_end),
                     f"{int(r.gap_at_phase_end):+,} ({r.gap_pct_at_phase_end:+.1f}%)"])
    blocks["Table 9"] = md_table(
        ["Population", "Phase (days)", "Deaths added by the daily series", "Change in the dashboard counter",
         "Counter at end of phase", "Gap at end of phase (counter − daily series)"], rows)

    # ---- Table 10: projection --------------------------------------------- #
    pr = pd.read_csv(T / "t4_projection.csv")
    labels = {"floor_1to1": "1:1 (very conservative floor)", "low_3to1": "3:1 (low end of the reported range)",
              "avg_4to1": "4:1 (often-cited average; reference scenario)", "high_15to1": "15:1 (upper end of the reported range)"}
    rows = []
    for sc in ("floor_1to1", "low_3to1", "avg_4to1", "high_15to1"):
        ir = pr[(pr.population == "Iran") & (pr.scenario == sc)].iloc[0]
        lb = pr[(pr.population == "Lebanon") & (pr.scenario == sc)].iloc[0]
        rows.append([labels[sc], f"{c(ir.indirect_lower)}–{c(ir.indirect_upper)}", f"{c(ir.total_lower)}–{c(ir.total_upper)}",
                     f"{c(lb.indirect_lower)}–{c(lb.indirect_upper)}", f"{c(lb.total_lower)}–{c(lb.total_upper)}"])
    blocks["Table 10"] = md_table(
        ["Assumed ratio (indirect : direct)", "Iran: projected indirect deaths", "Iran: projected total deaths",
         "Lebanon: projected indirect deaths", "Lebanon: projected total deaths"], rows)

    # ---- Table 11: WASH exposure (appendix) -------------------------------- #
    wa = pd.read_csv(T / "t4_wash_exposure.csv")
    rows = [[r.event_id, int(r.day), r.event, r.population_exposure, "yes" if r.in_insult_register else "no"]
            for _, r in wa.iterrows()]
    blocks["Table 11"] = md_table(["Event id", "Day", "Event", "Population exposure (as quoted in the source)",
                                   "Counted in the 21-event register"], rows)
    return blocks


def main():
    blocks = render_all()
    with open(OUT, "w") as f:
        for name, block in blocks.items():
            f.write(f"<!-- {name} -->\n{block}\n\n")
    print(f"rendered {len(blocks)} tables -> output/manuscript_tables.md")

    if "--no-check" in sys.argv:
        return
    if not MAN.exists():
        print("manuscript not found; check skipped")
        return
    text = MAN.read_text()
    missing = [name for name, block in blocks.items() if block not in text]
    if missing:
        for name in missing:
            print(f"  MISMATCH: {name} in the manuscript does not match the rendered table")
        raise SystemExit(f"{len(missing)} manuscript table(s) out of date — paste the blocks from output/manuscript_tables.md")
    print(f"checked: all {len(blocks)} tables appear verbatim in manuscript/paper2_v3.md")


if __name__ == "__main__":
    main()
