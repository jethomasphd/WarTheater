# IranWar.ai Event-Level Research Dataset — Release v1.0

**Status:** Frozen / archival. Do not modify. This directory preserves v1.0 exactly so
that analyses published against it remain reproducible (Manuscript §2.1, §3.1).

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Coverage | Day 0 (2026-02-27 baseline) – Day 30 (2026-03-29) |
| Rows | 1,653 |
| Columns | 48 |
| Source files | 15 extracted JSON files |
| Extraction date | ~May 2026 (preprint release 2026-05-13) |

## Contents

| File | Description |
|------|-------------|
| `iranwar_event_dataset.csv` | The v1.0 dataset, exactly as first released (1,653 rows). |
| `codebook.csv` | v1.0 codebook (48 variables). |
| `dataset_README.md` | v1.0 dataset documentation. |
| `build_dataset.py` | The exact extraction script that produced v1.0. |
| `source_snapshot_2026-03-30_Day30.zip` | Snapshot of `public/data/` as of Day 30. |

## Reproducibility

The attached source snapshot regenerates v1.0 **exactly**:

```bash
unzip source_snapshot_2026-03-30_Day30.zip -d /tmp/v10_src
# point build_dataset.py DATA_DIR at /tmp/v10_src, then run
python3 build_dataset.py   # -> 1,653 rows, dates 2026-01-02 .. 2026-03-29
```

The `2026-03-30` database snapshot (captured 03:00 CT on 2026-03-30, containing data
through end of Day 30) was verified to reproduce the 1,653-row v1.0 dataset bit-for-bit
on row count, domain distribution, and date range. The `2026-03-29` snapshot yields
1,623 rows (it predates the final Day-30 additions) and is therefore *not* the v1.0
source of record.

## Superseded by

v1.1 (Day 1–100). See `../../CHANGELOG.md` for the full list of changes, including the
timeline-category and retaliation-type reclassifications and the columns added in v1.1.
v1.0 column and row semantics are unchanged here.
