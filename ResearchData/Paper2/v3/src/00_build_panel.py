#!/usr/bin/env python3
"""
00 — Build the daily analysis panel and the health-system event register.

What this step does, in plain terms
-----------------------------------
The raw dataset has one row per event (a strike on one place on one day, a
casualty report for one faction on one day, and so on). Every analysis in
this paper works with one row per DAY instead. This script builds that daily
table (the "panel") and the list of health-system events (the "register").

Outputs:
  data/panel_daily.csv           170-day panel (one row per conflict-day)
  data/health_system_events.csv  register of distinct health-system events

The code is carried over from v2 unchanged, so the panel is identical to the
one used in v2 and in the parent paper. The script prints cross-checks against
the source dataset so that silent extraction drift fails loudly.
"""
from __future__ import annotations

import pandas as pd

import util


def main():
    df = util.load_events()
    panel = util.build_panel()
    hreg = util.extract_health_events(df)

    panel.to_csv(util.DATA_DIR / "panel_daily.csv")
    hreg.to_csv(util.DATA_DIR / "health_system_events.csv", index=False)

    print(f"dataset: {util.dataset_path()}")
    print(f"panel  : {panel.shape[0]} days x {panel.shape[1]} columns")
    print(f"health register: {len(hreg)} screened rows | "
          f"{int(hreg.counted.sum())} counted insult events | "
          f"{int((hreg.health_category == 'system_report').sum())} system reports | "
          f"{int((hreg.audit_action == 'excluded').sum())} excluded | "
          f"{int((hreg.audit_action == 'merged_duplicate').sum())} merged duplicates")
    print("\ncounted insult events by category:")
    print(hreg[hreg.counted].health_category.value_counts().to_string())
    print("\naudit actions:")
    print(hreg.audit_action.value_counts().to_string())

    # ---------------- Cross-checks (fail loudly on drift) ----------------- #
    conf = df[df.day_of_conflict >= 1]
    cas = conf[conf.source_file == "casualties.json"].copy()
    cas["v"] = pd.to_numeric(cas["casualties_reported"], errors="coerce")
    assert len(cas) == 850, f"expected 850 casualty rows, got {len(cas)}"
    assert int(panel["killed_total"].sum()) == int(cas["v"].sum()), \
        "panel killed_total does not reproduce the casualty-file total"
    assert int(panel["iran_civ"].sum()) == 543, \
        f"Iran civilian total drifted: {int(panel['iran_civ'].sum())} != 543"
    assert int(panel["leb_all"].sum()) == 2993, \
        f"Lebanon total drifted: {int(panel['leb_all'].sum())} != 2993"
    assert panel.loc[170, "hssi"] == panel["health_insults"].sum()
    assert (panel["strikes_civfac"] + panel["strikes_milfac"] <= panel["strikes"]).all(), \
        "civfac+milfac exceeds total strike tempo on some day"

    # The daily casualty series is known to run below the dashboard's
    # cumulative snapshots (recording lag / conservative daily attribution).
    # Quantify and report the gap; it is used analytically in 06/07.
    gap_iran = panel.loc[170, "snap_iranian_killed"] - panel.loc[170, "cum_iran_daily"]
    gap_leb = panel.loc[170, "snap_lebanese_killed"] - panel.loc[170, "cum_leb_daily"]
    print(f"\ncumulative-vs-daily gap at Day 170: Iran +{gap_iran:.0f} "
          f"({100 * gap_iran / panel.loc[170, 'cum_iran_daily']:.1f}%), "
          f"Lebanon +{gap_leb:.0f} "
          f"({100 * gap_leb / panel.loc[170, 'cum_leb_daily']:.1f}%)")

    print("\nper-phase daily means:")
    print(panel.groupby("phase", sort=False)[
        ["strikes", "strikes_civfac", "health_insults",
         "iran_civ", "iran_mil", "leb_all", "killed_total"]
    ].mean().round(2).to_string())

    print("\nwrote data/panel_daily.csv and data/health_system_events.csv")


if __name__ == "__main__":
    main()
