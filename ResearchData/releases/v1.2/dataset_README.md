# IranWar.ai Event-Level Research Dataset

**Current version: v1.2** (Day 0–170, 2026-02-27 → 2026-08-16). Released 2026-08-17.
For the change history and the frozen v1.0 / v1.1 releases, see `CHANGELOG.md` and `releases/`.

## Purpose

This dataset provides a structured, event-level record of the 2026 US-Iran conflict
(Operation Epic Fury, beginning February 28, 2026), extracted from the IranWar.ai OSINT
intelligence dashboard. It is designed for quantitative analysis by researchers in
political science, international relations, public health, psychology, psychiatry,
economics, military studies, and information science.

## Unit of Observation

Each row represents a **single discrete event**: a strike on a specific target on a
specific day, a retaliation attack, a financial data point, a casualty report for one
faction on one day, a naval deployment, a diplomatic action, or a humanitarian
development. Events are not aggregated — researchers can aggregate as needed.

## Date Range

- **Pre-war financial baselines**: 2026-01-02 to 2026-02-27 (oil prices, market indices)
- **Conflict events**: 2026-02-28 (Day 1) to 2026-08-16 (Day 170)
- **Day 0** (2026-02-27) = pre-war baseline reference date

## Dataset Summary (v1.2)

| Metric | Value |
|--------|-------|
| Total rows | 4,612 |
| Total columns | 52 |
| Event domains | 9 (STRIKE, RETALIATION, MILITARY, NAVAL, FINANCIAL, DIPLOMATIC, HUMANITARIAN, CYBER, OTHER) |
| Event types | 46 unique subcategories |
| Source files | 15 extracted JSON files from `public/data/` |
| Date range | 2026-01-02 to 2026-08-16 |
| As-of (cumulative records) | Day 170 (2026-08-16) |

### Row Counts by Domain

| Domain | Rows | Description |
|--------|------|-------------|
| FINANCIAL | 1,178 | Oil prices, market indices, war costs, tanker transits, baselines, alt routes |
| STRIKE | 967 | US/Israeli offensive strikes (exploded by target × active day) + offensive timeline/retaliation-file events |
| HUMANITARIAN | 915 | Daily casualty reports (5 factions × 170 days) + infrastructure damage + timeline |
| RETALIATION | 622 | Iranian/Hezbollah/Houthi/proxy attacks + maritime attack summary |
| DIPLOMATIC | 414 | Political, diplomatic, sanctions, congressional, and domestic events |
| OTHER | 276 | Daily briefings, aggregate snapshots, historical comparisons, summaries |
| MILITARY | 152 | General military events, base references, operational losses, ground ops |
| NAVAL | 84 | Fleet deployments, Strait of Hormuz events, maritime incidents, strategic geography |
| CYBER | 4 | Cyber operations |

## Source Files Used

| Source File | Records Extracted | Description |
|------------|-------------------|-------------|
| `timeline-events.json` | 1,050 | Master conflict timeline across all domains |
| `strikes-iran.json` | 902 | US/Israeli strike locations on Iran (129 locations, exploded) |
| `strikes-retaliation.json` | 480 | Retaliation / cross-front / maritime / operational-loss events (227 locations) |
| `casualties.json` | 850 | Daily estimated killed by faction (170 days × 5 factions) |
| `markets.json` | 398 | Market sector performance (116 trading days × 4 sectors, non-null) |
| `war-costs.json` | 303 | Daily war cost estimates (170) + tanker transit counts (133) |
| `oil-prices.json` | 275 | Brent and WTI crude oil prices (138 dates × 2) |
| `hero-stats.json` | 126 | Daily aggregate metric snapshots |
| `briefings/index.json` | 107 | Daily intelligence briefing headlines |
| `hormuz.json` | 34 | Strait of Hormuz closure, maritime impacts, day narratives |
| `baselines.json` | 28 | Pre-war financial baseline metrics |
| `carriers.json` | 21 | Naval asset deployments (US, UK, France) |
| `global-bases.json` | 25 | US military base reference locations |
| `infrastructure.json` | 8 | Cumulative infrastructure damage by category |
| `historical-comparison.json` | 5 | Historical conflict comparisons |

(`calculator.json` and `war-day.json` are dashboard-only config and are not extracted.)

## Construction Decisions

### Strike explosion logic
Strike locations in `strikes-iran.json` have arrays of `targets` and `active_days`. Each
location is exploded into one row per target per active day. This preserves maximum
granularity for researchers studying strike tempo, target selection, and geographic
patterns. Retaliation locations (no `targets` array) explode by `active_days` only.

### Timeline classification (expanded in v1.1)
The dashboard's free-text `category` field grew from 9 values at Day 30 to ~95 distinct,
inconsistently formatted values by Day 100. Each timeline record is mapped to one of the
nine `event_domain` values and a normalized `event_type` via an ordered keyword classifier
(`classify_timeline`), with precedence: explicit *retaliation* token → CYBER → HUMANITARIAN
→ NAVAL → FINANCIAL → DIPLOMATIC → MILITARY (military events are then split into
STRIKE/RETALIATION/MILITARY by description heuristics). **The verbatim source category is
preserved in the new `timeline_category_raw` column** so that any researcher can re-derive
an alternative coding. This implements the manuscript's commitment that classification is a
documented interpretive act (Manuscript §3.1, §5.1).

### Retaliation-file classification (expanded in v1.1)
The retaliation source file now contains ~32 `type` values, including **Israeli and US
offensive actions** (e.g., `idf_strike`, `israel_strike_lebanon`, `us_counter_action`).
These are classified `STRIKE` (with the appropriate initiating actor), not `RETALIATION`.
Iranian/Hezbollah/Houthi/proxy actions remain `RETALIATION`; maritime seizure/blockade
incidents are `NAVAL`; operational losses and other non-retaliatory military actions are
`MILITARY`. The initiating actor is taken from the source `actor`/`origin` fields where
present.

### Casualty data structure
Rows from `casualties.json` represent **daily estimated killed** for one faction, not
cumulative totals. The five factions tracked are Iranian military, Iranian civilian, US
military, Lebanese (all), and Israeli military. For cumulative figures, see the
`snapshot_*` columns from `hero-stats.json` history.

### As-of dating of cumulative records (fixed in v1.1)
Cumulative/reference records (infrastructure damage, Hormuz vessel-attack and
alternative-route summaries, historical comparison) are dated to the **latest day present
in the data** (computed dynamically; Day 100 / 2026-06-07 for this release), not to a
hardcoded date.

### Financial data duplication
Some financial metrics appear in multiple source files (e.g., Brent crude in
`oil-prices.json`, `baselines.json`, and `hero-stats.json` snapshots). These are preserved
as separate rows because they serve different analytical purposes. Filter by `source_file`
when analyzing financial trends.

### Data confidence scoring
Every row receives a `data_confidence` rating (HIGH / MEDIUM / LOW). HIGH = structured
field with authoritative source attribution (DoD/CENTCOM/IDF/IAEA/verified feeds); MEDIUM =
inferred/secondary (ACLED, satellite, interpolation); LOW = unverified, single-source, or
flagged as unconfirmed in the source data.

## New in v1.2

v1.2 extends coverage from Day 100 to **Day 170** (+1,025 rows, 3,587 → 4,612). **No
columns were added or renamed** (schema stable at 52). The extraction logic gained four
small, documented refinements to keep new source values correctly coded (see `CHANGELOG.md`
for the exact deltas — the changes touch 30 cells relative to a naive re-run):

- **`houthi_proxy_attack`** (new retaliation `type`, Houthi USV/missile strikes on Red Sea
  shipping) is coded `RETALIATION` / `maritime_attack`, consistent with the existing
  `drone_strike_on_commercial_vessel` handling.
- **`Water/Desalination Facilities Struck`** (new `infrastructure.json` category) maps to a
  new `infrastructure_target_type` value, **`water_infrastructure`** (parallel to
  `power_grid` / `oil_infrastructure`). No infrastructure row falls to `other`.
- **`mine_countermeasures`** and **`unmanned_surface_vessel`** appear as `event_type` values
  for two new naval asset classes in `carriers.json` (2 new controlled-vocabulary tokens; 44
  → 46 event types).
- **`notes_addendum`** (new `strikes-iran.json` field) is folded into `strike_notes` so no
  source text is discarded.

Casualty factions (5) and market sectors (4) are unchanged. The three singleton timeline
categories (`aviation_civil`, `us_iran_direct`, `regional_disruption`) remain in `OTHER`
pending a clearer rule; `timeline_category_raw` preserves all originals.

## New in v1.1 (columns)

Four columns were **appended** (v1.0's 48 columns retain their exact names and order):

| Column | Source | Description |
|--------|--------|-------------|
| `timeline_category_raw` | timeline-events.json | Verbatim source `category` before classification |
| `snapshot_nasdaq` | hero-stats.json | Nasdaq Composite from the daily snapshot |
| `snapshot_dow` | hero-stats.json | Dow Jones Industrial Average from the daily snapshot |
| `snapshot_sp500_change_pct` | hero-stats.json | Reported daily % change in the S&P 500 |

`weapon_system` is now also populated for `strikes-iran.json` records that carry a `weapon`
field (previously NULL for all strike rows).

## Known Limitations

1. **Casualty figures are estimates from initial reports.** Iranian figures come from Red
   Crescent, HRANA, and health ministry claims, difficult to verify independently. Source
   discrepancies are documented, not reconciled (Manuscript §5, §6.5).
2. **Some retaliation entries are unverified.** `strike_verified = False` flags records
   lacking open-source confirmation as of extraction; `data_confidence` is LOW for these
   and for single-source records.
3. **Financial data on weekends/holidays is NULL.** Oil/market series only cover trading
   days. Market indices are normalized (Feb 27 = 100), not raw points.
4. **Daily war cost estimates are interpolated** between two public anchors ($11.3B through
   Day 6, Pentagon; $16.5B through Day 12, CSIS) and extrapolated thereafter.
5. **Strike `active_days` reflect days a location was struck, not sortie counts.**
6. **`datetime_utc` timezone is approximate** — events span IRST/GST/IST/ET without
   normalization; only timeline events carry timestamps.
7. **Timeline classification is interpretive.** ~95 free-text categories are mapped via a
   documented keyword classifier; `timeline_category_raw` preserves the original. Three
   singleton categories (`aviation_civil`, `us_iran_direct`, `regional_disruption`) remain
   in OTHER pending a clearer rule.
8. **`event_id` is a build artifact, not a stable cross-version key.** IDs are sequential
   per build; the same event may carry a different `event_id` across versions. To track an
   event across releases, use `source_record_id` + `date` (where available) or pin to a
   specific versioned release in `releases/`.
9. **Infrastructure counts are minimums** (e.g., "29+" parsed as 29).
10. **No ground truth for event completeness.** The dataset captures what the dashboard
    tracked; unreported events are not represented.

## Files & Layout

```
ResearchData/
├── iranwar_event_dataset.csv   # latest dataset (v1.2) — stable citation path
├── codebook.csv                # latest codebook (52 variables)
├── build_dataset.py            # extraction script (reproducible)
├── dataset_README.md           # this file
├── CHANGELOG.md                # version history (v1.0 → v1.1)
├── SOURCE_SCHEMAS.md           # source JSON schema reference
├── AGENT_PROTOCOL.md           # monthly-update protocol for coding agents
└── releases/
    ├── v1.0/                   # frozen v1.0 (1,653 rows) + source snapshot + notes
    ├── v1.1/                   # frozen v1.1 (3,587 rows) + source snapshot + notes
    └── v1.2/                   # frozen v1.2 (4,612 rows) + source snapshot + notes
```

The root files always reflect the **latest** release; each `releases/vN/` directory is an
immutable, reproducible snapshot (dataset + codebook + script + source data) so that
analyses pinned to a version remain exactly reproducible.

## Reproducibility

```bash
cd ResearchData/
pip install pandas
python3 build_dataset.py          # reads ../public/data, writes the latest CSV + codebook
```

Event IDs are deterministic and stable across re-runs of the same version on unchanged
source data. To reproduce a specific version exactly, unzip that release's
`source_snapshot_*.zip` and run its bundled `build_dataset.py` against it.

## Suggested Citation

> Thomas, J. E., Alpysbekova, A., Osei Mensah, E., Masara, N., & Sharma, P. (2026).
> IranWar.ai Event-Level Research Dataset (v1.2): OSINT Record of the 2026 US-Iran Conflict
> (Operation Epic Fury). Extracted from the IranWar.ai Intelligence Dashboard
> (https://iranwar.ai). GitHub: https://github.com/jethomasphd/WarTheater.

## Disclaimer

This dataset is compiled from open-source intelligence (OSINT) and should not be treated as
ground truth. Casualty figures, cost estimates, and operational details reflect the best
available information at the time of reporting and may be revised. Researchers who cite
specific figures should carry forward the associated `data_confidence` ratings and source
attributions (Manuscript §9, Ethics).
