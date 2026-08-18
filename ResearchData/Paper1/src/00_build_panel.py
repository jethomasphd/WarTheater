#!/usr/bin/env python3
"""
00 — Build the daily analysis panel from the pinned v1.2 event dataset.

Writes:
  data/panel_daily.csv   (Day 1..170 x intensity/casualty/diplomacy series)

Prints validation so a reader can confirm the panel matches the dataset.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import util


def main():
    print("=" * 68)
    print("Paper 1 · Step 00 · Build daily panel")
    print("=" * 68)
    print(f"Source dataset : {util.dataset_path()}")
    print(f"Coverage       : Day 1..{util.LAST_DAY} "
          f"({util.date_from_day(1)} .. {util.date_from_day(util.LAST_DAY)})")

    panel = util.build_panel()

    out = util.DATA_DIR / "panel_daily.csv"
    panel.reset_index().to_csv(out, index=False)
    print(f"\nWrote {out}  ({panel.shape[0]} days x {panel.shape[1]} columns)")

    # ---- validation / summary ------------------------------------------- #
    print("\n--- Column totals (Day 1..170) ---")
    for c in ["strikes", "retal", "strikes_rows", "retal_rows",
              "strikes_tl", "retal_tl", "killed", "diplomatic", "naval"]:
        s = panel[c]
        print(f"  {c:14s} sum={s.sum():8.0f}  mean={s.mean():6.2f}  "
              f"max={s.max():5.0f}  nonzero_days={(s > 0).sum():3d}")

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

    print("\n--- Events by phase ---")
    by = panel.groupby("phase")[["strikes", "retal", "killed", "diplomatic"]].sum()
    by = by.reindex(util.PHASE_ORDER)
    ndays = panel.groupby("phase").size().reindex(util.PHASE_ORDER)
    by.insert(0, "n_days", ndays)
    print(by.to_string())
    by.to_csv(util.TAB_DIR / "t00_phase_totals.csv")
    print(f"\nWrote {util.TAB_DIR / 't00_phase_totals.csv'}")

    print("\nOK — panel built.")


if __name__ == "__main__":
    main()
