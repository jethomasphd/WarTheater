#!/usr/bin/env python3
"""
00 — Build the daily analysis panel from the frozen v1.2 event dataset.

Writes  data/panel_daily.csv  (Day 1..170 x 14 columns) and output/tables/t00_phase_totals.csv.
Prints cross-checks against the raw dataset and, when the parent paper's panel is present,
asserts that this panel is identical to it cell for cell.
"""
from __future__ import annotations

import pandas as pd

import util


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 00 · Build daily panel")
    print("=" * 70)
    print(f"Source dataset : {util.dataset_path()}")
    print(f"Coverage       : Day 1..{util.LAST_DAY} "
          f"({util.date_from_day(1)} .. {util.date_from_day(util.LAST_DAY)})")

    panel = util.build_panel()
    out = util.DATA_DIR / "panel_daily.csv"
    panel.reset_index().to_csv(out, index=False)
    print(f"\nWrote {out}  ({panel.shape[0]} days x {panel.shape[1]} columns)")

    print("\n--- Column totals (Day 1..170) ---")
    for c in ["strikes", "retal", "strikes_rows", "retal_rows", "strikes_tl", "retal_tl",
              "killed", "diplomatic", "naval"]:
        s = panel[c]
        print(f"  {c:14s} sum={s.sum():8.0f}  mean={s.mean():6.2f}  max={s.max():5.0f}  "
              f"nonzero_days={(s > 0).sum():3d}")

    print("\n--- Cross-checks against the raw dataset ---")
    df = util.load_events()
    conf = df[df.day_of_conflict >= 1]
    checks = {
        "STRIKE rows == strikes_rows sum":
            (conf.event_domain == "STRIKE").sum() == panel["strikes_rows"].sum(),
        "RETALIATION rows == retal_rows sum":
            (conf.event_domain == "RETALIATION").sum() == panel["retal_rows"].sum(),
        "DIPLOMATIC rows == diplomatic sum":
            (conf.event_domain == "DIPLOMATIC").sum() == panel["diplomatic"].sum(),
    }
    for k, v in checks.items():
        print(f"  [{'OK' if v else 'FAIL'}] {k}")
    assert all(checks.values()), "panel cross-check failed"

    parent = util.PARENT_DIR / "data" / "panel_daily.csv"
    if parent.exists():
        pp = pd.read_csv(parent).set_index("day")
        same = pp.shape == panel.shape and (pp.astype(str) == panel.astype(str)).all().all()
        print(f"  [{'OK' if same else 'FAIL'}] panel identical to the parent paper's panel")
        assert same, "panel differs from the parent paper's panel"
    else:
        print("  [skip] parent panel not present; identity check skipped")

    print("\n--- Totals by phase ---")
    by = panel.groupby("phase")[["strikes", "retal", "killed", "diplomatic"]].sum()
    by = by.reindex(util.PHASE_ORDER)
    by.insert(0, "n_days", panel.groupby("phase").size().reindex(util.PHASE_ORDER))
    print(by.to_string())
    util.write_table(by.reset_index(), "t00_phase_totals.csv")
    print("\nOK — panel built.")


if __name__ == "__main__":
    main()
