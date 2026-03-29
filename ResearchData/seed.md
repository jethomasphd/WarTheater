# Research Dataset Build — Agent Instructions

## Goal
Transform all JSON data in `public/data/` into a single event-level CSV dataset (`iranwar_event_dataset.csv`) plus a codebook (`codebook.csv`) and README (`dataset_README.md`), suitable for quantitative analysis by war/trauma researchers.

## Constraints
- Python only. Standard library + pandas + json.
- Do NOT hallucinate data. Mark ambiguous fields `data_confidence = LOW`.
- Do NOT merge/aggregate rows — keep event-level granularity.
- Sort final dataset by `date` then `event_domain`.
- If a source file fails to parse, log the error and continue.
- All output goes in `/ResearchData/`.
- Commit after each phase below with message: `research-data: Phase N — <description>`

---

## Phase 1: Build the extraction script skeleton + timeline events
**File:** `ResearchData/build_dataset.py`

Create a single Python script that:
1. Defines the output schema (all columns listed below).
2. Loads each JSON file from `public/data/`.
3. Has one extraction function per source file.
4. Writes `iranwar_event_dataset.csv`, `codebook.csv`, and prints summary stats to stdout.

For Phase 1, implement **only** the extraction of `timeline-events.json` (293 records).
Each record maps 1:1 to a row. Field mapping:

| Source field | Target column |
|---|---|
| (generate sequential) | `event_id` = `EVT-NNNN` |
| `date` | `date` |
| `date` + `time` (if present) | `datetime_utc` (ISO 8601, assume local = UTC+3:30 Iran or leave as-is with note) |
| day_of_conflict = `(date - 2026-02-28).days + 1`, 0 for pre-war | `day_of_conflict` |
| `category` mapped → STRIKE / RETALIATION / NAVAL / FINANCIAL / DIPLOMATIC / HUMANITARIAN / CYBER / OTHER | `event_domain` |
| `category` | `event_type` (keep original value) |
| `title` + `: ` + `description` | `event_description` |
| `"timeline-events.json"` | `source_file` |
| (none) | `source_record_id` = NULL |
| `source` | `timeline_source` (extra column) |
| `data_point` | `timeline_data_point` (extra column) |
| all domain-specific columns | NULL for timeline events unless inferable |

Category mapping for `event_domain`:
```
military → STRIKE (if description mentions US/Israeli strike) or RETALIATION (if Iranian/proxy) or MILITARY
financial → FINANCIAL
diplomatic → DIPLOMATIC
humanitarian → HUMANITARIAN
cyber → CYBER
other / unknown → OTHER
```
For `military` category, use heuristics on the description:
- Contains "Iran retaliates" / "Hezbollah" / "IRGC launches" / "Houthi" → RETALIATION
- Contains "US strikes" / "Israeli" / "B-2" / "Tomahawk" / "CENTCOM" → STRIKE
- Otherwise → MILITARY (add MILITARY as a valid domain)

Set `data_confidence = HIGH` for all timeline events (they come from structured fields).

**Commit after Phase 1.**

---

## Phase 2: Strikes on Iran (`strikes-iran.json`)

61 location records (skip the `_metadata` record where `id == "_metadata"`).

**Explosion logic:** Each location has an `active_days` array. Create one row per location per active day. If a location has multiple entries in `targets[]`, create one row per target per active day.

So: `rows = len(targets) * len(active_days)` per location record.

Field mapping:

| Source field | Target column |
|---|---|
| `id` | `source_record_id` |
| `first_strike` or computed from active_day | `date` = `2026-02-27 + active_day` |
| active_day | `day_of_conflict` |
| `"STRIKE"` | `event_domain` |
| `type` (e.g. `us_strike`) | `event_type` = `"airstrike"` |
| `actor` | `actor_initiating` (normalize: `us`, `israel`, `us_israel_joint`) |
| `"Iran"` | `country` |
| `city` | `location_name` |
| `lat` | `location_lat` |
| `lng` | `location_lon` |
| individual target string | `event_description` |
| `casualties_reported` | parse into `casualties_reported` (text), attempt numeric extraction for `casualties_civilian` / `casualties_military` |
| `subtype` if present | `infrastructure_target_type` mapping: nuclear_facility, oil_infrastructure, civilian, military_base, air_defense, communications |
| `notes` | `strike_notes` (extra column) |
| `"strikes-iran.json"` | `source_file` |

Infer `infrastructure_target_type` from target description keywords:
- "nuclear" / "enrichment" / "reactor" → `nuclear_facility`
- "oil" / "refinery" / "gas" / "Kharg" → `oil_infrastructure`
- "school" / "residential" / "civilian" / "hospital" → `civilian`
- "airbase" / "air base" / "runway" / "naval" / "IRGC" / "missile" → `military_base`
- "radar" / "air defense" / "S-300" → `air_defense`
- "IRIB" / "broadcaster" / "communications" → `communications`

Set `data_confidence`:
- HIGH if `casualties_source` cites DoD/CENTCOM/IDF/IAEA
- MEDIUM if cites ACLED/satellite imagery
- LOW if cites Wikipedia or "unconfirmed"

Generate `event_id` continuing from where Phase 1 left off.

**Commit after Phase 2.**

---

## Phase 3: Retaliation strikes (`strikes-retaliation.json`)

72 location records. Same explosion logic as Phase 2 (per target × per active day).

Field mapping — same as Phase 2 except:

| Source field | Target column |
|---|---|
| `"RETALIATION"` | `event_domain` |
| `type` → map: `iran_retaliation` = `"missile_attack"`, `hezbollah_front` = `"rocket_attack"`, `operational_loss` = `"operational_loss"` | `event_type` |
| `weapon` | `weapon_system` |
| `origin` | `actor_initiating` |
| `city` split → country from city name | `country` (parse: "Israel" if city contains Israel, "Kuwait" if Kuwait, etc.) |
| `verified` | `strike_verified` (extra boolean column) |

Country extraction heuristic from city field:
- Contains "Israel" → Israel
- Contains "Kuwait" → Kuwait
- Contains "Qatar" → Qatar
- Contains "UAE" / "Dubai" / "Abu Dhabi" / "Fujairah" → UAE
- Contains "Bahrain" → Bahrain
- Contains "Iraq" → Iraq
- Contains "Saudi" → Saudi Arabia
- Contains "Lebanon" / "Beirut" / "Tyre" → Lebanon
- Contains "Jordan" → Jordan
- Contains "Cyprus" → Cyprus
- Contains "Oman" → Oman
- Contains "Hormuz" / "maritime" → International Waters
- Otherwise → Unknown

Set `data_confidence`:
- HIGH if `verified == true`
- LOW if `verified == false`
- MEDIUM otherwise

**Commit after Phase 3.**

---

## Phase 4: Naval assets, casualties, and infrastructure

### 4a: Naval assets (`carriers.json`) — 13 records

Each naval asset = 1 event (deployment/positioning event).

| Source field | Target column |
|---|---|
| `"NAVAL"` | `event_domain` |
| `type` → `event_type` (carrier, amphibious, submarine, destroyer, etc.) |
| `operation_start_date` or `deployed_since` | `date` (use whichever is available; if neither, use `2026-02-28`) |
| `name` + `hull` | `military_asset` |
| `lat`, `lng` | `location_lat`, `location_lon` |
| `area` | `location_name` |
| `status` | `event_description` = `name` + " — " + `status` + " — " + `mission_summary` |
| `strike_group` | `naval_strike_group` (extra column) |
| `aircraft` | `naval_aircraft` (extra column) |
| `escorts` joined | `naval_escorts` (extra column) |
| `"carriers.json"` | `source_file` |

### 4b: Daily casualties (`casualties.json`) — 30 days × 5 factions = 150 rows

Each day × faction = 1 row.

| Source field | Target column |
|---|---|
| `"HUMANITARIAN"` | `event_domain` |
| `"daily_casualty_report"` | `event_type` |
| labels[i] parsed to date | `date` |
| i+1 | `day_of_conflict` |
| faction label | `actor_target` |
| data value | `casualties_reported` (integer) |
| day_contexts[i] | `event_description` |
| Faction → `casualties_military` or `casualties_civilian` | split by faction name |
| `"casualties.json"` | `source_file` |

For faction mapping:
- `iranian_military` → `actor_target = "Iran (military)"`, value → `casualties_military`
- `iranian_civilian` → `actor_target = "Iran (civilian)"`, value → `casualties_civilian`
- `us_military` → `actor_target = "US (military)"`, value → `casualties_military`
- `lebanese` → `actor_target = "Lebanon (all)"`, value → `casualties_reported`
- `israeli_military` → `actor_target = "Israel (military)"`, value → `casualties_military`

### 4c: Infrastructure damage (`infrastructure.json`) — 7 records

Each = 1 cumulative event.

| Source field | Target column |
|---|---|
| `"HUMANITARIAN"` | `event_domain` |
| `"infrastructure_damage"` | `event_type` |
| `"2026-03-29"` | `date` (cumulative as-of date) |
| `label` | `infrastructure_target_type` |
| `count` (parse numeric) | (store in `infrastructure_damage_count` extra column) |
| `detail` | `event_description` |
| `source` | stored in extra column |
| `"infrastructure.json"` | `source_file` |

**Commit after Phase 4.**

---

## Phase 5: Financial data (oil, markets, war costs, baselines, hero-stats)

### 5a: Oil prices (`oil-prices.json`)

30 date entries. Each date gets 2 rows (one for Brent, one for WTI).

| Source field | Target column |
|---|---|
| `"FINANCIAL"` | `event_domain` |
| `"oil_price"` | `event_type` |
| labels[i] parsed to full date (use year 2026, handle "Jan"→01, etc.) | `date` |
| `"Brent Crude"` or `"WTI Crude"` | `financial_metric_name` |
| price value | `financial_metric_value` |
| `"USD/bbl"` | `financial_metric_unit` |
| `"oil-prices.json"` | `source_file` |

### 5b: Markets (`markets.json`)

21 trading dates × 4 sectors = 84 rows.

| Source field | Target column |
|---|---|
| `"FINANCIAL"` | `event_domain` |
| `"market_index"` | `event_type` |
| labels[i] → date | `date` |
| sector label | `financial_metric_name` |
| data[i] | `financial_metric_value` |
| `"index (Feb 27 = 100)"` | `financial_metric_unit` |
| contexts[i] | `event_description` |
| `"markets.json"` | `source_file` |

### 5c: War costs (`war-costs.json`)

30 days → 30 cost rows + 33 tanker transit rows.

Cost rows:
| `"FINANCIAL"` | `event_domain` |
| `"daily_war_cost"` | `event_type` |
| computed date from day index | `date` |
| `daily_cost_millions[i]` | `financial_metric_value` |
| `"USD millions"` | `financial_metric_unit` |
| `day_notes[i]` | `event_description` |

Tanker rows:
| `"FINANCIAL"` | `event_domain` |
| `"tanker_transit"` | `event_type` |
| tanker_transits.labels[i] → date | `date` |
| tanker_transits.data[i] | `financial_metric_value` |
| `"transits/day"` | `financial_metric_unit` |

### 5d: Baselines (`baselines.json`)

Single pre-war snapshot → multiple rows, one per metric.
Flatten all nested values into individual FINANCIAL events dated `2026-02-27`.

Metrics to extract: brent, wti, gas, sp500, nasdaq, djia, 10yr_yield, fed_funds_rate, dxy, gold, silver, vix, national_debt, and each stock ticker (RTX, LMT, NOC, GD, BA, XOM, CVX, COP, DAL, UAL, AAL).

### 5e: Hero-stats history (`hero-stats.json` → `history[]`)

31 daily records. Extract as daily snapshot events with domain `OTHER` and type `daily_snapshot`. Each row captures that day's cumulative totals (us_kia, iranian_killed, displaced, etc.) — these are aggregate tracking rows, not discrete events.

| `"OTHER"` | `event_domain` |
| `"daily_aggregate_snapshot"` | `event_type` |
| history[i].date | `date` |
| history[i].war_day | `day_of_conflict` |
| Concatenate all non-null values into description | `event_description` |
| Individual fields → extra columns: `snapshot_brent`, `snapshot_wti`, `snapshot_gas`, `snapshot_sp500`, `snapshot_daily_cost_millions`, `snapshot_total_cost_billions`, `snapshot_targets_struck`, `snapshot_us_kia`, `snapshot_us_wia`, `snapshot_iranian_killed`, `snapshot_lebanese_killed`, `snapshot_displaced`, `snapshot_flights_cancelled`, `snapshot_children_killed` |
| `"hero-stats.json"` | `source_file` |

**Commit after Phase 5.**

---

## Phase 6: Hormuz, historical comparison, global bases, briefing index

### 6a: Hormuz (`hormuz.json`)

Create events for:
1. Strait closure event (1 row) — date = `closure_date`, domain = NAVAL
2. Each vessel attack summary → 1 row, domain = RETALIATION
3. Each alternative route → 1 row, domain = FINANCIAL
4. Each island → 1 row, domain = NAVAL (strategic geography)
5. Each day narrative from `impact.day_events` if present → domain varies

### 6b: Historical comparison (`historical-comparison.json`)

4 rows, one per conflict. Domain = OTHER, type = `historical_comparison`. These are reference rows.

### 6c: Global bases (`global-bases.json`)

13 rows, domain = NAVAL (or MILITARY), type = `military_base`. These are reference/context rows with lat/lon.

### 6d: Briefing index (`briefings/index.json`)

30 rows, domain = OTHER, type = `daily_briefing`. Each row captures the headline for that day.

**Commit after Phase 6.**

---

## Phase 7: Codebook, README, summary stats, final validation

### 7a: Generate `codebook.csv`

After building the full dataset, introspect every column and generate:

| Column | Description |
|---|---|
| `variable_name` | exact column name |
| `variable_label` | human-readable label |
| `variable_type` | string / integer / float / date / datetime / categorical / text |
| `valid_values` | for categoricals: list all unique values; for numerics: min–max |
| `missing_code` | what NULL means (not applicable / not available / not recorded) |
| `source_domain` | which data file(s) populate this column |
| `notes` | researcher-relevant caveats |

### 7b: Generate `dataset_README.md`

Contents:
- Purpose and scope
- Unit of observation (event-level)
- Date range: Feb 27 – Mar 29, 2026 (Day 0 baseline through Day 30)
- Source files used (list all 17 JSON files)
- Construction decisions:
  - Strike locations exploded by active_day × target
  - Casualty data is daily estimated killed (not cumulative)
  - Financial data includes pre-war baseline
  - Timeline events mapped from category to event_domain with heuristics
  - Historical comparison and global bases are reference rows
- Known limitations:
  - Casualty figures are estimates from initial reports
  - Some retaliation entries are unverified (`verified: false`)
  - Financial data on weekends/holidays is NULL
  - Oil prices are time-series chart data, not exact trading closes
  - Market sector data is normalized (index = 100 on Feb 27)
  - Strike "active_days" indicates the day a location was actively struck, not individual sortie counts
- Suggested citation format

### 7c: Print summary statistics

After building the full CSV:
1. Total row count and date range
2. Row counts by `event_domain` and `event_type`
3. Completeness profile: for each column, % of non-null rows
4. Data quality concerns (duplicates, inconsistencies, gaps)

### 7d: Validate

- Run `python3 -m json.tool` equivalent validation on outputs
- Ensure no duplicate `event_id` values
- Ensure all dates are valid ISO 8601
- Ensure `day_of_conflict` is consistent with dates
- Check that sort order is correct (date ASC, then event_domain ASC)

**Commit after Phase 7. This is the final commit.**

---

## Full Output Schema

### Required columns (every row):
```
event_id                    — EVT-0001, EVT-0002, ...
date                        — YYYY-MM-DD
datetime_utc                — YYYY-MM-DDTHH:MM:SSZ or NULL
day_of_conflict             — integer (0 = pre-war, 1 = Feb 28, ...)
event_domain                — STRIKE | RETALIATION | NAVAL | FINANCIAL | DIPLOMATIC | HUMANITARIAN | CYBER | MILITARY | OTHER
event_type                  — subcategory string
event_description           — text
source_file                 — which JSON file
source_record_id            — original ID or NULL
```

### Domain-specific columns (NULL when N/A):
```
location_name               — string
location_lat                — float
location_lon                — float
country                     — string
actor_initiating            — string
actor_target                — string
weapon_system               — string
military_asset              — string
casualties_reported         — integer or text
casualties_civilian         — integer
casualties_military         — integer
infrastructure_target_type  — categorical
financial_metric_name       — string
financial_metric_value      — float
financial_metric_unit       — string
escalation_level            — not present in source data; leave NULL
data_confidence             — HIGH | MEDIUM | LOW
```

### Extra columns (domain-prefixed, NULL when N/A):
```
timeline_source             — from timeline-events.json
timeline_data_point         — from timeline-events.json
strike_notes                — from strikes-iran/retaliation.json
strike_verified             — boolean, from strikes-retaliation.json
naval_strike_group          — from carriers.json
naval_aircraft              — from carriers.json
naval_escorts               — from carriers.json
infrastructure_damage_count — from infrastructure.json
snapshot_brent              — from hero-stats.json history
snapshot_wti                — from hero-stats.json history
snapshot_gas                — from hero-stats.json history
snapshot_sp500              — from hero-stats.json history
snapshot_daily_cost_millions — from hero-stats.json history
snapshot_total_cost_billions — from hero-stats.json history
snapshot_targets_struck     — from hero-stats.json history
snapshot_us_kia             — from hero-stats.json history
snapshot_us_wia             — from hero-stats.json history
snapshot_iranian_killed     — from hero-stats.json history
snapshot_lebanese_killed    — from hero-stats.json history
snapshot_displaced          — from hero-stats.json history
snapshot_flights_cancelled  — from hero-stats.json history
snapshot_children_killed    — from hero-stats.json history
```

## Key Reference

- **Conflict start date:** 2026-02-28 (Day 1)
- **Day 0 = 2026-02-27** (pre-war baseline)
- **Date from war day:** `datetime.date(2026, 2, 27) + timedelta(days=war_day)`
- **War day from date:** `(date - datetime.date(2026, 2, 27)).days`
- **Data directory:** `public/data/`
- **Output directory:** `ResearchData/`
- **Event ID counter:** global, sequential across all phases, zero-padded to 4+ digits
