# Research Dataset Monthly Update Protocol — Agent Instructions

## Overview

This document gives a coding agent everything needed to regenerate and extend the IranWar.ai research dataset after new data has been added to the dashboard. The dashboard is updated daily; this research dataset is rebuilt monthly (or on demand) to capture the latest data.

**You are extending an existing dataset, not building from scratch.** The extraction script (`build_dataset.py`) already works. Your job is to update it if source schemas changed, re-run it, validate the output, and commit.

---

## Quick Start (Happy Path)

If the dashboard JSON schemas haven't changed since the last build:

```bash
cd ResearchData/
pip install pandas
python3 build_dataset.py
# Review stdout summary stats
# If all validation checks pass, commit the updated CSV + codebook
```

That's it. The script reads all 17 JSON files, extracts events, and regenerates both `iranwar_event_dataset.csv` and `codebook.csv` from scratch each run.

---

## When Schemas Change (The Real Work)

The dashboard evolves. New JSON files may appear, existing files may gain new fields, or array structures may change. Here's how to handle each case.

### Step 1: Inventory Check

Run this to compare current data files against what the script expects:

```bash
python3 -c "
import json, os
for f in sorted(os.listdir('../public/data')):
    if f.endswith('.json'):
        path = f'../public/data/{f}'
        with open(path) as fh:
            d = json.load(fh)
        if isinstance(d, list):
            print(f'{f}: list[{len(d)}]')
        else:
            print(f'{f}: dict, keys={sorted(d.keys())}')
"
```

Compare against the schemas documented in `SOURCE_SCHEMAS.md`. If you see:
- **New files** not listed in SOURCE_SCHEMAS.md → Need a new extraction function
- **New keys** in existing files → May need new columns or mapping logic
- **Changed array lengths** → Normal (more days of data)
- **Missing files** → Error; investigate

### Step 2: Update the Script

`build_dataset.py` has one extraction function per source file:

| Function | Source File | Phase |
|----------|-----------|-------|
| `extract_timeline_events()` | `timeline-events.json` | 1 |
| `extract_strikes_iran()` | `strikes-iran.json` | 2 |
| `extract_strikes_retaliation()` | `strikes-retaliation.json` | 3 |
| `extract_carriers()` | `carriers.json` | 4a |
| `extract_casualties()` | `casualties.json` | 4b |
| `extract_infrastructure()` | `infrastructure.json` | 4c |
| `extract_oil_prices()` | `oil-prices.json` | 5a |
| `extract_markets()` | `markets.json` | 5b |
| `extract_war_costs()` | `war-costs.json` | 5c |
| `extract_baselines()` | `baselines.json` | 5d |
| `extract_hero_stats_history()` | `hero-stats.json` | 5e |
| `extract_hormuz()` | `hormuz.json` | 6a |
| `extract_historical_comparison()` | `historical-comparison.json` | 6b |
| `extract_global_bases()` | `global-bases.json` | 6c |
| `extract_briefings()` | `briefings/index.json` | 6d |

To add a new source file:
1. Write a new `extract_<name>()` function following the existing patterns
2. Add its call in the `main()` function under the appropriate phase
3. If it introduces new columns, add them to `EXTRA_COLS` and `VARIABLE_METADATA`
4. Run the script and check that row counts make sense

### Step 3: Run and Validate

```bash
python3 build_dataset.py
```

The script prints summary stats to stdout. Check:
- Total row count increased (new days of data)
- No duplicate event_ids
- No missing dates or domains
- New event types appear if expected
- Column completeness looks reasonable

### Step 4: Commit

```
git add iranwar_event_dataset.csv codebook.csv build_dataset.py
git commit -m "research-data: Monthly update — Day [N] — YYYY-MM-DD

- [row count] total rows (was [old count])
- [new events] new events since last build
- [schema changes if any]"
```

---

## Architecture of build_dataset.py

### Global State
- `_event_counter`: Sequential counter for EVT-NNNN IDs. Resets to 0 each run.
- `CONFLICT_START = date(2026, 2, 28)`: Day 1 of the war.
- `BASELINE_DATE = date(2026, 2, 27)`: Day 0.
- `DATA_DIR`: Points to `../public/data/` relative to the script.

### Key Functions
- `next_event_id()` → returns `EVT-0001`, `EVT-0002`, etc.
- `war_day(d)` → converts a date to day-of-conflict integer
- `date_from_war_day(n)` → converts day number to date
- `parse_short_date(label)` → parses "Mar 27" or "Feb 5" to date objects
- `load_json(filename)` → loads from DATA_DIR, returns None on error
- `empty_row()` → returns dict with all 48 columns set to None

### Column Schema
Defined in three lists at module level:
- `REQUIRED_COLS` (9): event_id, date, datetime_utc, day_of_conflict, event_domain, event_type, event_description, source_file, source_record_id
- `DOMAIN_COLS` (17): location_*, actor_*, weapon_system, military_asset, casualties_*, infrastructure_target_type, financial_metric_*, escalation_level, data_confidence
- `EXTRA_COLS` (22): timeline_*, strike_*, naval_*, infrastructure_damage_count, snapshot_*

### Adding New Columns

1. Add the column name to `EXTRA_COLS` (or `DOMAIN_COLS` if broadly applicable)
2. Add an entry to `VARIABLE_METADATA` dict with: `(label, type, source_domain, missing_code, notes)`
3. The codebook generator will automatically pick it up

### Event Domain Classification

Valid domains: `STRIKE`, `RETALIATION`, `NAVAL`, `FINANCIAL`, `DIPLOMATIC`, `HUMANITARIAN`, `CYBER`, `MILITARY`, `OTHER`

For timeline events with `category = "military"`, the script uses regex heuristics to classify into STRIKE vs RETALIATION vs MILITARY. If new categories appear in the timeline, add them to `CATEGORY_DOMAIN_MAP`.

### Explosion Logic

Strike records use "explosion" — one source record becomes many rows:
- `strikes-iran.json`: 1 row per target × per active_day
- `strikes-retaliation.json`: 1 row per active_day (no targets array)
- All other sources: 1 row per source record (or per day × per faction for casualties)

Casualties are **not** exploded from aggregates — they are daily per-faction counts from chart data.

---

## Critical Rules

1. **NEVER modify files in `public/`** — this is the live dashboard. Only touch `ResearchData/`.
2. **NEVER fabricate data.** If a field is ambiguous, set `data_confidence = "LOW"` and note it.
3. **Preserve backward compatibility** of the CSV schema. Only ADD columns, never remove or rename existing ones. Downstream researchers may depend on column names.
4. **Validate JSON after any data directory changes** — `python3 -m json.tool < file.json`
5. **Sort the final CSV** by date ASC, then event_domain ASC (the script does this automatically).
6. **Update the codebook** if you add columns (the script does this automatically via `VARIABLE_METADATA`).
7. **Update dataset_README.md** if you change construction decisions or discover new limitations.

---

## Handling Edge Cases

### New JSON file appears in public/data/
1. Read it, understand its schema
2. Write a new extraction function
3. Decide: is each record a discrete event? If so, map 1:1. If it's aggregate data, decide on the right unit of observation.
4. Add to main() and test

### A field is renamed in a source file
1. Update the extraction function to use the new field name
2. Keep the output column name the same (backward compat)
3. Note the change in the commit message

### War day numbering changes
The script computes day_of_conflict from dates using `BASELINE_DATE = 2026-02-27`. If the project ever changes the Day 1 convention, update `CONFLICT_START` and `BASELINE_DATE` at the top of the script.

### Data looks wrong
Before overwriting the existing CSV, diff the summary stats against the previous run. If row counts decreased or key columns lost completeness, investigate before committing.

---

## Monthly Checklist

- [ ] `git pull` latest main
- [ ] Check for new/changed JSON files in `public/data/` vs `SOURCE_SCHEMAS.md`
- [ ] If schemas changed, update extraction functions
- [ ] `python3 build_dataset.py`
- [ ] Review summary stats: row count, domain distribution, completeness
- [ ] Verify 0 duplicate event_ids, 0 missing dates
- [ ] Update `dataset_README.md` row count and date range
- [ ] Commit with descriptive message
- [ ] Push
