#!/usr/bin/env python3
"""
04 — FINDING 3: the deaths we can count are a floor, not a total.
     (Tools: descriptive means comparison + plain arithmetic.)

Three pieces of evidence, in order.

(1) What the daily death series can and cannot see (means comparison).
    The daily series records deaths reported on the day of an attack. We show
    this by comparing Iranian civilian deaths per day on strike days with
    non-strike days, and by looking at the First Ceasefire: 89 days in which
    the series records zero Iranian civilian deaths while facility damage
    stood at 99-100% of its final level and health-system events continued.
    Deaths from disrupted care (a missed dialysis session, a delivery without
    a skilled attendant, diarrhoeal illness after a water plant is destroyed)
    do not happen on strike days only, so this series cannot contain them.

(2) Even the direct count is revised upward (accounting gap).
    The dataset carries two accountings of direct deaths: the daily series
    summed over days, and the dashboard's cumulative counter. At Day 170 the
    daily sum is below the counter by 14.8% (Iran) and 43.9% (Lebanon). We
    show WHEN each gap opened, phase by phase, so the reader can see what
    kind of gap it is. (Iran: the counter re-anchored on Day 57 from a
    Hengaw-scale total to the Legal Medicine Organization figure and then
    moved to HRANA-family verified counts; the daily series added only 41
    deaths after Day 40. Lebanon: the two agreed at Day 40; almost the whole
    gap opened during the ceasefire, when the ministry's cumulative count
    grew by more than twice what the daily series recorded.)

(3) The projection (arithmetic, not a model).
    Conflict epidemiology reports 3 to 15 indirect deaths per direct death
    across studied conflicts, with about 4:1 often cited as an average
    (Geneva Declaration Secretariat 2008). We multiply the documented direct
    toll by each ratio. This is a projection under a stated assumption, not
    an estimate from these data, and it is computed on BOTH direct-toll
    bases so the dataset's own uncertainty carries through.

Also written: the WASH exposure rows (population figures quoted from the
source events; each anchored to a dataset event id and verified at run time).

Outputs
-------
  output/tables/t4_direct_toll.csv
  output/tables/t4_strike_vs_nonstrike_days.csv
  output/tables/t4_ceasefire_block.csv
  output/tables/t4_accounting_gap_by_phase.csv
  output/tables/t4_accounting_gap_milestones.csv
  output/tables/t4_projection.csv
  output/tables/t4_wash_exposure.csv
  output/figures/fig4_two_counts.(png|pdf)
  output/figures/fig5_floor_projection.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import util

SCENARIOS = [
    ("floor_1to1", 1.0, "1:1 — very conservative floor"),
    ("low_3to1", 3.0, "3:1 — low end of the reported range"),
    ("avg_4to1", 4.0, "4:1 — often-cited cross-conflict average (reference scenario)"),
    ("high_15to1", 15.0, "15:1 — upper end of the reported range (weakest health systems)"),
]

# WASH / environmental exposure events with population figures quoted in the
# dataset (event ids verified against the dataset at run time).
WASH_ROWS = [
    ("EVT-3311", 140, "Bonji (Jask) desalination plant intake station destroyed",
     "~10,000 people across 20 villages lost drinking water (Iran, Hormozgan)"),
    ("EVT-1019", 140, "Two Kuwaiti power-and-desalination plants struck, ablaze",
     "Kuwait relies on desalination for ~90% of potable water"),
    ("EVT-1769", 33, "Qeshm Island desalination plant struck (Days 33-34)",
     "Island population depends on desalinated supply"),
    ("EVT-0303", 31, "Kuwait water/electrical plant struck",
     "First strike on Gulf water infrastructure"),
    ("EVT-0060", 11, "ICRC damage assessment: 30-40% of the national grid offline in western Iran",
     "Water treatment disrupted in Ahvaz and Kermanshah; hospitals on backup generators (ICRC)"),
]

MILESTONE_DAYS = [20, 40, 56, 57, 66, 80, 100, 118, 129, 150, 170]


def main():
    util.apply_style()
    p = util.load_panel()
    h = util.load_health_register()
    df = util.load_events()

    # ------------------------------------------------------------------ #
    # (1) What the daily series can see: strike days vs non-strike days
    # ------------------------------------------------------------------ #
    sd = p[p.strike_day == 1]
    ns = p[p.strike_day == 0]
    rows = []
    for col, label in (("iran_civ", "Iranian civilian deaths per day"),
                       ("iran_mil", "Iranian military deaths per day"),
                       ("leb_all", "Lebanese deaths per day")):
        a, b = sd[col].astype(float).values, ns[col].astype(float).values
        t, pv = stats.ttest_ind(a, b, equal_var=False)
        rows.append({"outcome": col, "label": label,
                     "strike_days_n": len(a), "strike_days_mean": a.mean(), "strike_days_sd": a.std(ddof=1),
                     "strike_days_total": int(a.sum()),
                     "non_strike_days_n": len(b), "non_strike_days_mean": b.mean(),
                     "non_strike_days_sd": b.std(ddof=1), "non_strike_days_total": int(b.sum()),
                     "welch_t": t, "p": pv, "hedges_g": util.hedges_g(a, b)})
    t_sn = pd.DataFrame(rows)
    t_sn.round(4).to_csv(util.TAB_DIR / "t4_strike_vs_nonstrike_days.csv", index=False)

    cf = p.loc[41:129]
    cf_ins = h[h.counted & (h.day_of_conflict >= 41) & (h.day_of_conflict <= 129)]
    t_cf = pd.DataFrame([
        {"metric": "first_ceasefire_days", "value": len(cf)},
        {"metric": "iran_civilian_deaths_recorded", "value": int(cf.iran_civ.sum())},
        {"metric": "iran_military_deaths_recorded", "value": int(cf.iran_mil.sum())},
        {"metric": "days_with_recorded_strikes", "value": int(cf.strike_day.sum())},
        {"metric": "strike_locations_recorded", "value": int(cf.strikes.sum())},
        {"metric": "health_system_insult_events_in_register", "value": len(cf_ins)},
        {"metric": "facility_damage_pct_of_final_min", "value": round(cf.facil_damage_pct.min(), 1)},
        {"metric": "facility_damage_pct_of_final_max", "value": round(cf.facil_damage_pct.max(), 1)},
        {"metric": "lebanese_deaths_recorded", "value": int(cf.leb_all.sum())},
        {"metric": "insult_event_ids", "value": "; ".join(cf_ins.event_id.tolist())},
    ])
    t_cf.to_csv(util.TAB_DIR / "t4_ceasefire_block.csv", index=False)

    r0 = t_sn.iloc[0]
    print("FINDING 3 — the counted dead are a floor")
    print(f"  (1) Iranian civilian deaths/day: strike days {r0.strike_days_mean:.2f} (n={r0.strike_days_n}) vs "
          f"non-strike days {r0.non_strike_days_mean:.2f} (n={r0.non_strike_days_n}); Welch t = {r0.welch_t:.2f}, p = {r0.p:.2e}, g = {r0.hedges_g:.2f}")
    print(f"      First Ceasefire: {len(cf)} days, {int(cf.iran_civ.sum())} Iranian civilian deaths recorded, "
          f"{int(cf.strike_day.sum())} strike days, {len(cf_ins)} health-system insult events, damage at "
          f"{cf.facil_damage_pct.min():.1f}-{cf.facil_damage_pct.max():.1f}% of final")

    # ------------------------------------------------------------------ #
    # (2) Accounting gap: daily-series sum vs dashboard counter
    # ------------------------------------------------------------------ #
    snap_days = set(df[(df.event_type == "daily_aggregate_snapshot") & (df.day_of_conflict >= 1)]
                    .day_of_conflict.astype(int).tolist())
    ms_rows = []
    for day in MILESTONE_DAYS:
        for pop, cum_col, snap_col in (("Iran", "cum_iran_daily", "snap_iranian_killed"),
                                       ("Lebanon", "cum_leb_daily", "snap_lebanese_killed")):
            c, s = float(p.loc[day, cum_col]), float(p.loc[day, snap_col])
            ms_rows.append({"population": pop, "day": day, "phase": util.phase_of(day),
                            "daily_series_cumulative": int(c), "dashboard_counter": int(round(s)),
                            "gap": int(round(s - c)), "gap_pct_of_daily": round(100 * (s - c) / c, 1) if c else np.nan,
                            "counter_observed_that_day": day in snap_days})
    t_ms = pd.DataFrame(ms_rows)
    t_ms.to_csv(util.TAB_DIR / "t4_accounting_gap_milestones.csv", index=False)

    ph_rows = []
    for pop, cum_col, snap_col in (("Iran", "cum_iran_daily", "snap_iranian_killed"),
                                   ("Lebanon", "cum_leb_daily", "snap_lebanese_killed")):
        for name, lo, hi in util.PHASES:
            daily_added = float(p.loc[hi, cum_col]) - (float(p.loc[lo - 1, cum_col]) if lo > 1 else 0.0)
            snap_start = float(p.loc[lo - 1, snap_col]) if lo > 1 else np.nan
            snap_end = float(p.loc[hi, snap_col])
            counter_added = snap_end - snap_start if pd.notna(snap_start) else np.nan
            ph_rows.append({"population": pop, "phase": name, "days": f"{lo}-{hi}",
                            "daily_series_deaths_added": int(daily_added),
                            "counter_at_phase_start": int(round(snap_start)) if pd.notna(snap_start) else np.nan,
                            "counter_at_phase_end": int(round(snap_end)),
                            "counter_change": int(round(counter_added)) if pd.notna(counter_added) else np.nan,
                            "gap_at_phase_end": int(round(snap_end - float(p.loc[hi, cum_col]))),
                            "gap_pct_at_phase_end": round(100 * (snap_end - float(p.loc[hi, cum_col])) / float(p.loc[hi, cum_col]), 1)})
    t_ph = pd.DataFrame(ph_rows)
    t_ph.to_csv(util.TAB_DIR / "t4_accounting_gap_by_phase.csv", index=False)

    # The Iran re-anchoring signature (verified, as in the parent paper).
    peak = float(p.snap_iranian_killed.max())
    peak_day = int(p.index[p.snap_iranian_killed == peak].max())
    post = float(p.snap_iranian_killed.loc[peak_day + 1])
    assert peak == 9226.0 and post == 3375.0 and peak_day == 56, (peak, peak_day, post)

    print("  (2) accounting gap at Day 170: Iran daily sum "
          f"{int(p.cum_iran_daily.iloc[-1]):,} vs counter {int(p.snap_iranian_killed.iloc[-1]):,}; "
          f"Lebanon {int(p.cum_leb_daily.iloc[-1]):,} vs {int(p.snap_lebanese_killed.iloc[-1]):,}")
    print("      where the gap opened (counter change vs daily-series deaths added, by phase):")
    for _, r in t_ph.iterrows():
        print(f"        {r.population:8s} {r.phase:17s} daily +{r.daily_series_deaths_added:5d}   counter "
              f"{'n/a' if pd.isna(r.counter_change) else '%+6d' % r.counter_change}   gap at end {r.gap_at_phase_end:+5d} ({r.gap_pct_at_phase_end:+.1f}%)")
    print(f"      Iran counter re-anchored on Day {peak_day + 1}: {peak:,.0f} -> {post:,.0f}")

    # ------------------------------------------------------------------ #
    # (3) Direct toll bounds and the projection
    # ------------------------------------------------------------------ #
    rows = [
        {"population": "Iran (total)", "basis": "daily series summed (lower bound)",
         "direct_killed": int(p.cum_iran_daily.iloc[-1])},
        {"population": "Iran (total)", "basis": "dashboard counter at Day 170 (upper bound)",
         "direct_killed": int(p.snap_iranian_killed.iloc[-1])},
        {"population": "Iran (total)", "basis": "dashboard counter peak before re-anchoring (Day 56)",
         "direct_killed": int(peak)},
        {"population": "Iran (civilian)", "basis": "daily series summed",
         "direct_killed": int(p.iran_civ.sum())},
        {"population": "Lebanon (all)", "basis": "daily series summed (lower bound)",
         "direct_killed": int(p.cum_leb_daily.iloc[-1])},
        {"population": "Lebanon (all)", "basis": "dashboard counter at Day 170 (upper bound)",
         "direct_killed": int(p.snap_lebanese_killed.iloc[-1])},
        {"population": "Children (dashboard counter)", "basis": "dashboard counter at Day 170",
         "direct_killed": int(p.snap_children_killed.iloc[-1])},
    ]
    pd.DataFrame(rows).to_csv(util.TAB_DIR / "t4_direct_toll.csv", index=False)

    bases = {
        "Iran": (int(p.cum_iran_daily.iloc[-1]), int(p.snap_iranian_killed.iloc[-1])),
        "Lebanon": (int(p.cum_leb_daily.iloc[-1]), int(p.snap_lebanese_killed.iloc[-1])),
    }
    proj = []
    for pop, (lo_base, hi_base) in bases.items():
        for label, R, note in SCENARIOS:
            proj.append({
                "population": pop, "scenario": label, "ratio_indirect_to_direct": R, "note": note,
                "direct_lower": lo_base, "direct_upper": hi_base,
                "indirect_lower": int(round(lo_base * R)), "indirect_upper": int(round(hi_base * R)),
                "total_lower": int(round(lo_base * (1 + R))), "total_upper": int(round(hi_base * (1 + R))),
            })
    t_proj = pd.DataFrame(proj)
    t_proj.to_csv(util.TAB_DIR / "t4_projection.csv", index=False)
    ir4 = t_proj[(t_proj.population == "Iran") & (t_proj.scenario == "avg_4to1")].iloc[0]
    lb4 = t_proj[(t_proj.population == "Lebanon") & (t_proj.scenario == "avg_4to1")].iloc[0]
    ir3 = t_proj[(t_proj.population == "Iran") & (t_proj.scenario == "low_3to1")].iloc[0]
    ir15 = t_proj[(t_proj.population == "Iran") & (t_proj.scenario == "high_15to1")].iloc[0]
    print(f"  (3) documented direct deaths at Day 170: Iran {ir4.direct_lower:,}-{ir4.direct_upper:,}; "
          f"Lebanon {lb4.direct_lower:,}-{lb4.direct_upper:,}")
    print(f"      projected total (Iran): 3:1 -> {ir3.total_lower:,}-{ir3.total_upper:,}; "
          f"4:1 -> {ir4.total_lower:,}-{ir4.total_upper:,}; 15:1 -> {ir15.total_lower:,}-{ir15.total_upper:,}")
    print(f"      projected total (Lebanon) at 4:1: {lb4.total_lower:,}-{lb4.total_upper:,}")

    # ------------------------------------------------------------------ #
    # WASH exposure rows (anchored and verified)
    # ------------------------------------------------------------------ #
    idx = df.set_index("event_id")["event_description"].fillna("")
    wash = []
    for eid, day, event, exposure in WASH_ROWS:
        assert eid in idx.index, f"WASH anchor {eid} missing"
        wash.append({"event_id": eid, "day": day, "event": event, "population_exposure": exposure,
                     "in_insult_register": bool((h.event_id == eid).any()
                                                and h.loc[h.event_id == eid, "counted"].any())})
    pd.DataFrame(wash).to_csv(util.TAB_DIR / "t4_wash_exposure.csv", index=False)

    # ------------------------------------------------------------------ #
    # Figure 4 — the two counts, Iran and Lebanon
    # ------------------------------------------------------------------ #
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    for ax, pop, cum_col, snap_col in ((axes[0], "Iran", "cum_iran_daily", "snap_iranian_killed"),
                                       (axes[1], "Lebanon", "cum_leb_daily", "snap_lebanese_killed")):
        util.shade_phases(ax)
        ax.plot(p.index, p[cum_col], color="0.15", lw=1.8, label="Daily series, summed")
        ax.plot(p.index, p[snap_col], color=util.C_GOLD, lw=1.6, ls="--", label="Dashboard cumulative counter")
        ax.set_xlabel("Day of the war")
        ax.set_ylabel(f"Cumulative {'Iranian' if pop == 'Iran' else 'Lebanese'} deaths")
        ax.set_xlim(0, 171)
        ax.set_title(f"{'A' if pop == 'Iran' else 'B'}. {pop}: the two counts",
                     loc="left", fontweight="bold", fontsize=9.5)
        end_c, end_s = float(p[cum_col].iloc[-1]), float(p[snap_col].iloc[-1])
        ax.annotate(f"Day 170: {end_c:,.0f} vs {end_s:,.0f}\n(gap {100*(end_s-end_c)/end_c:+.1f}%)",
                    (170, end_s), textcoords="offset points", xytext=(-6, -34 if pop == "Lebanon" else 14),
                    fontsize=8.0, ha="right", color="0.2")
        if pop == "Iran":
            ax.annotate("Day 57: counter re-anchored\n9,226 → 3,375", xy=(57, 6300), xytext=(78, 7300),
                        fontsize=8.0, arrowprops=dict(arrowstyle="->", lw=0.9, color="0.3"))
        else:
            ax.annotate("gap opens during the\nFirst Ceasefire", xy=(90, 3300), xytext=(95, 1500),
                        fontsize=8.0, arrowprops=dict(arrowstyle="->", lw=0.9, color="0.3"))
        ax.legend(fontsize=8, loc="upper left" if pop == "Lebanon" else "upper right")
    util.savefig(fig, "fig4_two_counts")
    plt.close(fig)

    # ------------------------------------------------------------------ #
    # Figure 5 — the floor and the projected total
    # ------------------------------------------------------------------ #
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4), sharey=False)
    for ax, pop in zip(axes, ("Iran", "Lebanon")):
        sub = t_proj[t_proj.population == pop]
        x = np.arange(len(sub))
        direct_hi = sub.direct_upper.iloc[0]
        ax.bar(x, sub.direct_upper, width=0.62, color=util.C_KILLED, alpha=0.85, label="Direct deaths (documented)")
        ax.bar(x, sub.indirect_upper, width=0.62, bottom=sub.direct_upper, color=util.C_GOLD, alpha=0.78,
               label="Indirect deaths (projected)")
        ax.errorbar(x, sub.total_upper, yerr=[sub.total_upper - sub.total_lower, np.zeros(len(sub))],
                    fmt="none", ecolor="0.3", elinewidth=1.2, capsize=4)
        ax.axhline(direct_hi, color="0.4", lw=0.8, ls=":")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{int(r)}:1" for r in sub.ratio_indirect_to_direct])
        ax.set_xlabel("Assumed ratio of indirect to direct deaths")
        ax.set_title(f"{'A' if pop == 'Iran' else 'B'}. {pop}: documented floor and projected total (Day 170)",
                     loc="left", fontweight="bold", fontsize=9.5)
        if ax is axes[0]:
            ax.set_ylabel("Deaths")
            ax.legend(fontsize=8, loc="upper left")
    fig.text(0.5, -0.02,
             "Bars use the higher direct-toll basis (dashboard counter); whiskers extend down to the lower basis (daily series). "
             "Projections under stated ratios, not estimates from these data.",
             ha="center", fontsize=7.4, color="0.25")
    util.savefig(fig, "fig5_floor_projection")
    plt.close(fig)
    print("\nwrote t4 tables + fig4_two_counts + fig5_floor_projection")


if __name__ == "__main__":
    main()
