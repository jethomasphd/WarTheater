# IranWar.ai Event-Level Research Dataset — Release v1.1

**Status:** Latest release. Frozen copy preserved here for reproducibility; the identical
files also live at the `ResearchData/` root as the "latest" pointers.

| Field | Value |
|-------|-------|
| Version | 1.1 |
| Released | 2026-06-09 |
| Coverage | Day 0 (2026-02-27 baseline) – Day 100 (2026-06-07) |
| Rows | 3,587 |
| Columns | 52 (v1.0's 48 + 4 appended) |
| Source files | 15 extracted JSON files |
| As-of (cumulative records) | Day 100 (2026-06-07) |

## Contents

| File | Description |
|------|-------------|
| `iranwar_event_dataset.csv` | The v1.1 dataset (3,587 rows). |
| `codebook.csv` | v1.1 codebook (52 variables). |
| `dataset_README.md` | v1.1 dataset documentation. |
| `build_dataset.py` | The exact extraction script that produced v1.1. |
| `source_snapshot_2026-06-09_Day1-100.zip` | Snapshot of `public/data/` at extraction. |

## Reproducibility

The attached source snapshot regenerates v1.1 **byte-for-byte** (verified):

```bash
unzip source_snapshot_2026-06-09_Day1-100.zip -d /tmp/v11_src
# point build_dataset.py DATA_DIR at /tmp/v11_src, then run
python3 build_dataset.py   # -> 3,587 rows, 52 cols, dates 2026-01-02 .. 2026-06-07
```

## What changed since v1.0

See `../../CHANGELOG.md` for the full list. Highlights: expanded timeline-category and
retaliation-type classifiers (≈200 timeline events rescued from `OTHER`; Israeli/US
offensives in the retaliation file correctly coded `STRIKE`); dynamic as-of dating of
cumulative records; four new columns (`timeline_category_raw`, `snapshot_nasdaq`,
`snapshot_dow`, `snapshot_sp500_change_pct`); `weapon_system` populated for strikes;
normalized naval event types.

## Validation (all pass)

0 duplicate event_ids · 0 missing dates · 0 non-ISO dates · 0 invalid event_domain values ·
0 day_of_conflict↔date inconsistencies · canonical sort order (date ASC, event_domain ASC)
confirmed.
