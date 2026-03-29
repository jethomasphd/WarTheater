# Source JSON Schemas — Reference for Coding Agents

This document describes the exact schema of every JSON file in `public/data/` as of Day 30 (March 29, 2026). When updating the research dataset, compare current files against these schemas to detect changes.

---

## Conflict Reference

- **Day 1** = 2026-02-28 (first strikes)
- **Day 0** = 2026-02-27 (pre-war baseline)
- **Date from war day**: `date(2026, 2, 27) + timedelta(days=N)`
- **War day from date**: `(date - date(2026, 2, 27)).days`

---

## 1. timeline-events.json

**Type**: Array of event objects
**Record count (Day 30)**: 293
**Unit**: One discrete event (military, financial, diplomatic, etc.)

```json
{
  "date": "2026-02-28",          // ISO date
  "time": "02:00",               // HH:MM local time (timezone varies)
  "title": "Short event title",
  "description": "Detailed description paragraph",
  "category": "military",        // military|financial|diplomatic|humanitarian|cyber|economic|political|domestic|summary
  "source": "DoD / White House",
  "data_point": "3,000+ targets" // nullable — quantitative highlight
}
```

**Growth pattern**: ~10 events/day added during daily updates. Expect ~300 new records per month.

**Category values observed**: military (141), financial (57), diplomatic (54), humanitarian (16), domestic (8), economic (5), cyber (4), political (4), summary (4).

**Agent note**: The `category` field maps to `event_domain` via `CATEGORY_DOMAIN_MAP` in the script. For `military` events, regex heuristics determine STRIKE vs RETALIATION vs MILITARY. If new categories appear, add them to the map.

---

## 2. strikes-iran.json

**Type**: Array (first element is `_metadata`, skip it; rest are location records)
**Record count (Day 30)**: 62 (1 metadata + 61 locations)
**Unit**: One geographic strike location — may span multiple days and targets

```json
{
  "id": "tehran-leadership",         // unique location ID
  "city": "Tehran",
  "lat": 35.6892,
  "lng": 51.3890,
  "type": "us_strike",              // always "us_strike"
  "actor": "us_israel_joint",       // us|israel|us_israel_joint|israel_us_coordinated|unknown
  "targets": [                       // array of target descriptions
    "Leadership House compound (Feb 28, Day 1)",
    "IRGC Malek-Ashtar building (Mar 2, Day 3)"
  ],
  "first_strike": "2026-02-28",     // ISO date
  "casualties_reported": "Unknown — heavy",  // text or null
  "casualties_source": "ACLED / Iranian state media",
  "active_days": [1, 2, 3, 4],      // array of war day integers
  "notes": "Detailed operational notes...",
  "subtype": "civilian_casualty",    // nullable — civilian_casualty|civilian_casualties|civilian_infrastructure|energy_infrastructure|targeted_killing
  "verified": true,                  // nullable boolean
  "last_updated": "2026-03-29"      // nullable
}
```

**_metadata record** (id="_metadata"): Contains aggregate statistics. Skip during extraction but useful for validation:
- `total_targets_struck`, `provinces_struck`, `aggregate_casualties_iran`

**Explosion**: Each location → `len(targets) * len(active_days)` rows. Day 30 total: 620 rows.

**Growth pattern**: New locations added when strikes hit new cities. Existing locations get new entries in `active_days` and `targets` arrays. Expect both new records and expanded arrays.

---

## 3. strikes-retaliation.json

**Type**: Array of location records (no metadata record)
**Record count (Day 30)**: 72
**Unit**: One retaliation target location

```json
{
  "id": "ali-al-salem-kuwait",
  "city": "Ali Al Salem Air Base, Kuwait",
  "lat": 29.3467,
  "lng": 47.5231,
  "type": "iran_retaliation",       // iran_retaliation|hezbollah_front|hezbollah|operational_loss|us_strike_on_militia
  "weapon": "Ballistic missiles / cruise missiles / drones",
  "origin": "Western Iran",         // geographic origin of attack
  "first_strike": "2026-02-28",
  "casualties_reported": "Runway damage, debris injuries...",
  "casualties_source": "Kuwaiti MoD / Stars and Stripes",
  "active_days": [1, 2, 3, 4, 5, 6, 7, 8],
  "notes": "Detailed notes...",
  "verified": true,                  // boolean
  "last_updated": "2026-03-17"
}
```

**Key difference from strikes-iran.json**: No `targets` array. Each record is a single target. Explosion is by `active_days` only.

**Type values**: iran_retaliation (most common), hezbollah_front, hezbollah, operational_loss (e.g., KC-135 crash), us_strike_on_militia.

**Explosion**: Each location → `len(active_days)` rows. Day 30 total: 237 rows.

---

## 4. carriers.json

**Type**: Array of naval asset objects
**Record count (Day 30)**: 13
**Unit**: One naval asset (carrier, submarine, destroyer group, amphibious ship, ground unit)

```json
{
  "id": "cvn-72",
  "name": "USS Abraham Lincoln",
  "hull": "CVN-72",                 // nullable for ground units
  "type": "carrier",                // carrier|amphibious|submarine|destroyer|littoral_combat_ship|air|ground
  "strike_group": "Carrier Strike Group 3",
  "lat": 20.80,
  "lng": 59.50,
  "area": "Arabian Sea — continuous combat ops",
  "aircraft": "F/A-18E/F Super Hornets, F-35C...",  // string or null
  "escorts": ["DDG-121 USS Frank E. Petersen Jr.", ...],  // array
  "independently_deployed_destroyers": [...],  // some records only
  "status": "ENGAGED",
  "mission_summary": "Primary strike platform...",
  "deployed_since": "2025-11-21",   // nullable ISO date
  "operation_start_date": "2026-02-28",  // nullable
  "eta_theater": "2026-04-09",      // some records only
  "notes": "Day 30: ...",
  "source": "USNI Fleet Tracker..."
}
```

**Growth pattern**: New assets added as deployments change. Existing records get updated positions, status, and notes. May also lose records if assets leave theater.

---

## 5. casualties.json

**Type**: Dict with parallel arrays
**Unit**: Daily estimated killed per faction (chart data)

```json
{
  "labels": ["Feb 28", "Mar 1", "Mar 2", ...],   // 30 date strings
  "day_contexts": ["Day 1 — First strikes...", ...],  // 30 narrative summaries
  "datasets": {
    "iranian_military": { "label": "Iranian Military", "data": [65, 98, 122, ...], "color": "#b81c1c" },
    "iranian_civilian": { "label": "Iranian Civilian", "data": [5, 10, 15, ...], "color": "#ffffff" },
    "us_military":      { "label": "US Military",      "data": [0, 6, 0, ...],   "color": "#4a9eff" },
    "lebanese":         { "label": "Lebanese (all)",    "data": [0, 0, 44, ...],  "color": "#7b3fa0" },
    "israeli_military": { "label": "Israeli Military",  "data": [0, 0, 0, ...],   "color": "#ffc832" }
  },
  "last_updated": "2026-03-29"
}
```

**CRITICAL**: These are **daily estimated killed**, NOT cumulative. Each value is that day's toll for one faction. For cumulative figures, use `hero-stats.json` history snapshots.

**Growth pattern**: Arrays grow by 1 element per day. New factions could theoretically be added.

---

## 6. oil-prices.json

**Type**: Dict with parallel arrays
**Unit**: One price observation per date per commodity

```json
{
  "labels": ["Jan 2", "Jan 8", ..., "Mar 27"],  // 30 date labels
  "brent": [74.2, 73.8, ..., 112.57],           // USD/bbl
  "wti": [71.8, 71.2, ..., 99.64],              // USD/bbl
  "baselines": { "brent": 71.00, "wti": 66.50 },
  "pre_war_index": 8,                            // index of Feb 27 in labels
  "day_map": [3, 4, 5, 6, 7, ...],              // war day numbers for post-war entries
  "last_updated": "2026-03-29"
}
```

**Date parsing**: Labels are "Mon D" format (e.g., "Mar 27"). Parse with year 2026. Pre-war dates go back to January.

**Growth pattern**: One new entry per trading day in labels/brent/wti arrays.

---

## 7. markets.json

**Type**: Dict with parallel arrays
**Unit**: One index observation per trading day per sector

```json
{
  "labels": ["Feb 27", "Mar 2", ..., "Mar 27"],  // 21 trading dates
  "contexts": ["Pre-war close — baseline", "Day 3 — ...", ...],  // narrative per day
  "datasets": {
    "sp500":     { "label": "S&P 500",              "data": [100, 100.0, 99.1, ...], "color": "#ef4444" },
    "defense":   { "label": "Defense (RTX + LMT)",   "data": [100, 103.5, ...],       "color": "#22c55e" },
    "oil_majors": { "label": "Oil Majors (XOM + CVX)", "data": [100, 106.0, ...],     "color": "#d4a020" },
    "airlines":  { "label": "Airlines (DAL + UAL)",  "data": [100, 92.0, ...],        "color": "#7b3fa0" }
  },
  "last_updated": "2026-03-29"
}
```

**CRITICAL**: Values are **normalized indices** where Feb 27 = 100, NOT raw index points. Note this in any output.

**Growth pattern**: One new entry per trading day. New sectors could be added.

---

## 8. war-costs.json

**Type**: Dict with parallel arrays + nested tanker object
**Unit**: Daily cost estimate + daily tanker transit count

```json
{
  "labels": ["Day 1", "Day 2", ...],               // 30 day labels
  "daily_cost_millions": [3000, 2600, 2000, ...],   // USD millions
  "day_notes": ["First strikes — $5.6B...", ...],   // 30 narrative notes
  "median_home_price_millions": 0.42,
  "tanker_transits": {
    "labels": ["Feb 25", "Feb 26", ..., "Mar 29"],  // 33 date labels
    "data": [50, 50, 50, 25, 5, 0, ...],            // transits per day
    "prewar_daily": 50
  },
  "last_updated": "2026-03-29"
}
```

**Day label parsing**: "Day N" format → extract integer, compute date as `date(2026,2,27) + timedelta(days=N)`.

**Growth pattern**: Both arrays grow by 1 per day.

---

## 9. hero-stats.json

**Type**: Dict with current snapshot + history array
**Unit**: Daily aggregate snapshot

The `history` array is the key research data:

```json
{
  "history": [
    {
      "date": "2026-02-27", "war_day": 0, "label": "Pre-war baseline",
      "brent": 71.00, "wti": 66.50, "gas": 2.98, "sp500": 6878.88,
      "daily_cost_millions": null, "total_cost_billions": null,
      "targets_struck": null, "us_kia": 0, "us_wia": 0,
      "iranian_killed": null, "lebanese_killed": null,
      "displaced": null, "flights_cancelled": null, "children_killed": null
    },
    // ... one entry per day
  ]
}
```

**CRITICAL**: `us_kia`, `iranian_killed`, `lebanese_killed`, `displaced`, `flights_cancelled`, `children_killed` are **CUMULATIVE** totals, unlike casualties.json which has daily estimates. Document this for researchers.

**Growth pattern**: One new entry in `history[]` per day. Top-level `cost` and `toll` objects update daily but only latest values matter (history captures the timeseries).

---

## 10. infrastructure.json

**Type**: Array of damage category objects
**Record count (Day 30)**: 7
**Unit**: One infrastructure damage category (cumulative)

```json
{
  "label": "Hospitals Damaged",
  "count": "29+",                    // text — may contain +, ~, etc.
  "note": "Short summary...",
  "source": "Iranian Health Ministry / WHO...",
  "detail": "Extended description..."
}
```

**Categories**: Hospitals Damaged, Schools Destroyed, Power Plants Hit, Oil/Gas Facilities Hit, Nuclear Facilities Struck, Airports Damaged, Bridges Destroyed.

**Growth pattern**: Counts update. New categories could be added.

---

## 11. hormuz.json

**Type**: Dict with three sections: `strait`, `geometry`, `impact`
**Unit**: Mixed — strategic metrics, geographic features, day narratives

**strait**: Closure metadata (closure_date, method, status, etc.)
**geometry**: Coordinates for chokepoint, shipping lanes, islands
**impact**: Extensive metrics + day narratives

Day narratives are in `impact.day_NN_events` fields (e.g., `day_22_events`, `day_30_events`). These are long text strings summarizing Hormuz-related events for that day.

**Growth pattern**: New `day_NN_events` fields added. Metrics update. May gain new subsections.

---

## 12. historical-comparison.json

**Type**: Dict with `conflicts` array
**Record count**: 4

```json
{ "conflicts": [
  { "label": "Iran 2026 (Day 30)", "targets_struck": 30500, "us_kia": 13, "daily_cost_millions": 1250, "note": "..." },
  { "label": "Iraq 2003 (Day 21)", ... },
  { "label": "Libya 2011 (Day 21)", ... },
  { "label": "Gulf 1991 (Day 21)", ... }
]}
```

**Growth pattern**: Iran 2026 entry updates. Others are static reference.

---

## 13. global-bases.json

**Type**: Array of base objects
**Record count**: 13
**Unit**: One military installation

```json
{ "name": "Norfolk Naval Station", "lat": 36.95, "lng": -76.30, "type": "naval", "note": "Largest naval base..." }
```

**Growth pattern**: Rarely changes. New bases added if relevant to conflict.

---

## 14. baselines.json

**Type**: Dict — pre-war financial snapshot
**Unit**: Single snapshot dated 2026-02-27

Contains nested objects: `oil`, `gas`, `markets`, `treasury`, `commodities`, `national_debt`, `defense_stocks`, `oil_stocks`, `airline_stocks`, `hormuz`, `humanitarian`, `audit`.

**Growth pattern**: Should not change (it's a historical baseline). The `audit` field tracks data verification status.

---

## 15. calculator.json

**Type**: Dict — gas price calculator config
**Currently NOT extracted** by `build_dataset.py` (dashboard-only UI config).

If you want to extract it: 16 state-level gas price premiums + national average. Could produce 16 FINANCIAL/gas_price rows.

---

## 16. war-day.json

**Type**: Dict — current war day counter
**Currently NOT extracted** (metadata only, redundant with dates in other files).

```json
{ "war_day": 30, "date": "2026-03-29", "label": "DAY 30", "start_date": "2026-02-28" }
```

---

## 17. briefings/index.json

**Type**: Array of briefing index entries
**Record count (Day 30)**: 30
**Unit**: One daily briefing

```json
{
  "day": 1,
  "date": "2026-02-28",
  "label": "FEBRUARY 28, 2026 — DAY 1",
  "headline": "Operation Epic Fury begins — Khamenei killed...",
  "file": "data/briefings/day-1.html"
}
```

**Growth pattern**: One new entry per day. The HTML files are not parsed (they're presentation content).

---

## Schema Change Detection Checklist

When you start a monthly update, run the inventory script and check:

1. Any new `.json` files in `public/data/`?
2. For each file, are the top-level keys the same as documented above?
3. For array files, have any records gained new fields?
4. For `casualties.json`, are there new factions in `datasets`?
5. For `markets.json`, are there new sectors in `datasets`?
6. Has `hormuz.json` gained new `day_NN_events` fields? (Expected — one per new day)
7. Are `strikes-iran.json` or `strikes-retaliation.json` records still using the same structure?

If everything matches, just re-run the script. If not, update the extraction function and this document.
