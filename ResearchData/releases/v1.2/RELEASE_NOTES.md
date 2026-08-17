# IranWar.ai Event-Level Research Dataset — Release v1.2

**Status:** Latest release. Frozen copy preserved here for reproducibility; the identical
files also live at the `ResearchData/` root as the "latest" pointers.

| Field | Value |
|-------|-------|
| Version | 1.2 |
| Released | 2026-08-17 |
| Coverage | Day 0 (2026-02-27 baseline) – Day 170 (2026-08-16) |
| Rows | 4,612 |
| Columns | 52 (unchanged from v1.1) |
| Source files | 15 extracted JSON files |
| As-of (cumulative records) | Day 170 (2026-08-16) |

## Contents

| File | Description |
|------|-------------|
| `iranwar_event_dataset.csv` | The v1.2 dataset (4,612 rows). |
| `codebook.csv` | v1.2 codebook (52 variables). |
| `dataset_README.md` | v1.2 dataset documentation. |
| `build_dataset.py` | The exact extraction script that produced v1.2. |
| `source_snapshot_2026-08-17_Day1-170.zip` | Snapshot of `public/data/` at extraction. |

## Reproducibility

The attached source snapshot regenerates v1.2 **byte-for-byte** (verified — identical MD5
for both the dataset and the codebook):

```bash
unzip source_snapshot_2026-08-17_Day1-170.zip -d /tmp/v12_src
# point build_dataset.py DATA_DIR at /tmp/v12_src, then run
python3 build_dataset.py   # -> 4,612 rows, 52 cols, dates 2026-01-02 .. 2026-08-16
```

The frozen snapshot is built from the exact `public/data/` bytes used for the build; the
daily `snapshots/*.zip` archive was taken at a slightly different moment and is not
guaranteed to reproduce the CSV.

## What changed since v1.1

See `../../CHANGELOG.md` for the full list. This is a coverage extension (Day 100 → Day 170,
+1,025 rows) with **no schema changes** (52 columns unchanged) and four small, documented
classification refinements. Relative to a naive re-run of the v1.1 script on the Day-170
data, v1.2 changes exactly **30 cells**:

- `houthi_proxy_attack` (new Houthi Red Sea maritime attacks) → `RETALIATION` /
  `maritime_attack` (2 `event_type` cells).
- New `infrastructure.json` category "Water/Desalination Facilities Struck" →
  new `infrastructure_target_type` `water_infrastructure` (1 cell).
- `notes_addendum` (new `strikes-iran.json` field) folded into `strike_notes`
  (27 cells, the exploded `kharg-island` record).
- `mine_countermeasures` and `unmanned_surface_vessel` added as explicit naval
  `event_type` tokens (44 → 46 event types; no output delta vs. the prior regex fallback).

## Validation (all pass)

0 duplicate event_ids · 0 missing dates · 0 non-ISO dates · 0 invalid event_domain values ·
0 day_of_conflict↔date inconsistencies · canonical sort order (date ASC, event_domain ASC)
confirmed.
