# IranWar.ai Event-Level Research Dataset

## Purpose

This dataset provides a structured, event-level record of the first 30 days of the 2026 US-Iran conflict (Operation Epic Fury, February 28 - March 29, 2026), extracted from the IranWar.ai OSINT intelligence dashboard. It is designed for quantitative analysis by researchers in political science, international relations, public health, psychology, psychiatry, and trauma studies.

## Unit of Observation

Each row represents a **single discrete event**: a strike on a specific target on a specific day, a retaliation attack, a financial data point, a casualty report for one faction on one day, a naval deployment, a diplomatic action, or a humanitarian development. Events are not aggregated -- researchers can aggregate as needed.

## Date Range

- **Pre-war financial baselines**: 2026-01-02 to 2026-02-27 (oil prices, market indices)
- **Conflict events**: 2026-02-28 (Day 1) to 2026-03-29 (Day 30)
- **Day 0** (2026-02-27) = pre-war baseline reference date

## Dataset Summary

| Metric | Value |
|--------|-------|
| Total rows | 1,653 |
| Total columns | 48 |
| Event domains | 9 (STRIKE, RETALIATION, MILITARY, NAVAL, FINANCIAL, DIPLOMATIC, HUMANITARIAN, CYBER, OTHER) |
| Event types | 25 unique subcategories |
| Source files | 17 JSON files from `public/data/` |
| Date range | 2026-01-02 to 2026-03-29 |

### Row Counts by Domain

| Domain | Rows | Description |
|--------|------|-------------|
| STRIKE | 641 | US/Israeli offensive strikes on Iran (exploded by target x active day) |
| RETALIATION | 307 | Iranian/proxy retaliation attacks + maritime attacks |
| FINANCIAL | 301 | Oil prices, market indices, war costs, tanker transits, baselines |
| HUMANITARIAN | 173 | Daily casualty reports (5 factions x 30 days) + infrastructure damage |
| OTHER | 69 | Daily briefings, aggregate snapshots, historical comparisons |
| DIPLOMATIC | 66 | Political, diplomatic, and domestic events |
| MILITARY | 64 | General military events, base reference records |
| NAVAL | 28 | Fleet deployments, Strait of Hormuz events, strategic geography |
| CYBER | 4 | Cyber operations |

## Source Files Used

All data extracted from JSON files in the `public/data/` directory of the IranWar.ai repository:

| Source File | Records Extracted | Description |
|------------|-------------------|-------------|
| `timeline-events.json` | 293 | Master conflict timeline across all domains |
| `strikes-iran.json` | 620 | US/Israeli strike locations on Iran (61 locations, exploded) |
| `strikes-retaliation.json` | 237 | Iranian retaliation / Hezbollah / proxy strikes (72 locations) |
| `casualties.json` | 150 | Daily estimated killed by faction (30 days x 5 factions) |
| `markets.json` | 84 | Market sector performance (21 trading days x 4 sectors) |
| `war-costs.json` | 63 | Daily war cost estimates + tanker transit counts |
| `oil-prices.json` | 60 | Brent and WTI crude oil prices |
| `hero-stats.json` | 31 | Daily aggregate metric snapshots |
| `briefings/index.json` | 30 | Daily intelligence briefing headlines |
| `baselines.json` | 28 | Pre-war financial baseline metrics |
| `hormuz.json` | 20 | Strait of Hormuz closure, maritime impacts, day narratives |
| `carriers.json` | 13 | Naval asset deployments (US, UK, France) |
| `global-bases.json` | 13 | US military base reference locations |
| `infrastructure.json` | 7 | Cumulative infrastructure damage by category |
| `historical-comparison.json` | 4 | Historical conflict comparisons |

## Construction Decisions

### Strike explosion logic
Strike locations in `strikes-iran.json` have arrays of `targets` and `active_days`. Each location is exploded into one row per target per active day. A location with 5 targets active on 10 days produces 50 rows. This preserves maximum granularity for researchers studying strike tempo, target selection, and geographic patterns.

### Casualty data structure
Rows from `casualties.json` represent **daily estimated killed** for one faction, not cumulative totals. The five factions tracked are: Iranian military, Iranian civilian, US military, Lebanese (all), and Israeli military. These are from chart data that represents estimated daily toll. For cumulative figures, see `snapshot_us_kia`, `snapshot_iranian_killed`, etc. from `hero-stats.json` history.

### Retaliation type handling
The `strikes-retaliation.json` file includes five types: `iran_retaliation` (mapped to RETALIATION/missile_attack), `hezbollah_front` and `hezbollah` (RETALIATION/rocket_attack), `operational_loss` (MILITARY/operational_loss -- e.g., the KC-135 crash), and `us_strike_on_militia` (STRIKE/airstrike). These are classified by domain to maintain analytical clarity about who initiated each action.

### Financial data duplication
Some financial metrics appear in multiple source files (e.g., Brent crude in `oil-prices.json`, `baselines.json`, and `hero-stats.json` snapshots). These are preserved as separate rows because they serve different analytical purposes: `oil-prices.json` has the full time series, `baselines.json` has the pre-war anchor point, and snapshots capture the daily dashboard state. Researchers should filter by `source_file` when analyzing financial trends.

### Country extraction
Country is inferred from city/location name fields using keyword matching (e.g., "Bahrain" in city name -> country = "Bahrain"). Maritime events in the Strait of Hormuz are coded as "International Waters". Four retaliation records targeting uncertain locations may have country = "Unknown".

### Infrastructure target type inference
The `infrastructure_target_type` field is inferred from target description keywords for strike records. This is a best-effort classification -- researchers should review `event_description` for edge cases.

### Data confidence scoring
Every row receives a `data_confidence` rating:
- **HIGH**: Directly from structured data field with authoritative source attribution (DoD, CENTCOM, IDF, IAEA, verified reporting)
- **MEDIUM**: Inferred from secondary sources, satellite imagery, or ACLED
- **LOW**: From unverified sources, Wikipedia, or records flagged as unverified in source data

### Reference rows
Some rows are not discrete events but reference records: global military bases (13 rows), historical conflict comparisons (4 rows), and strategic Hormuz islands (5 rows). These provide geographic and contextual anchors. Filter by `event_type` to exclude if not needed.

## Known Limitations

1. **Casualty figures are estimates from initial reports.** Iranian figures come from Red Crescent, HRANA, and health ministry claims. These are difficult to verify independently due to internet blackout and fog of war. Discrepancies between sources are noted in `strike_notes`.

2. **Some retaliation entries are unverified.** Four of 72 retaliation location records have `strike_verified = False` (Ain al-Asad, Nevatim, Dimona, Oman ports). These are plausible based on conflict patterns but lack direct open-source confirmation.

3. **Financial data on weekends/holidays is NULL.** Oil prices and market indices are only available for trading days. `snapshot_*` fields from hero-stats are also NULL on days without reported data.

4. **Oil prices are chart-display data.** Values from `oil-prices.json` are the prices used for dashboard chart rendering, which may represent closes, intraday points, or weekly averages depending on the date.

5. **Market sector data is normalized.** Market indices from `markets.json` are expressed as an index where February 27 = 100, not raw index points. For S&P 500 raw values, use `snapshot_sp500` from hero-stats or `baselines.json`.

6. **Strike "active_days" reflect days a location was struck, not sortie counts.** A single active day may represent multiple strikes or a single strike. The data does not capture individual sortie-level detail.

7. **Datetime timezone is approximate.** The `datetime_utc` field from timeline events uses times as recorded in the source data. Events span multiple time zones (Iran/IRST, Gulf/GST, Israel/IST, US/ET) and the source does not specify timezone per event.

8. **Daily war cost estimates are interpolated.** Pentagon confirmed $11.3B through Day 6 and CSIS confirmed $16.5B through Day 12. Values between and after these anchors are extrapolated by the dashboard maintainers.

9. **Infrastructure damage counts are minimums.** Values like "29+" are parsed as 29. Actual totals are likely higher.

10. **No ground truth for event completeness.** This dataset captures what was tracked by the IranWar.ai dashboard. Events not covered by the dashboard's sources are not represented.

## Files

| File | Description |
|------|-------------|
| `iranwar_event_dataset.csv` | Main dataset (1,653 rows, 48 columns, UTF-8) |
| `codebook.csv` | Variable definitions, types, valid values, completeness, and researcher notes |
| `build_dataset.py` | Python extraction script (reproducible from source JSON) |
| `seed.md` | Build specification document |
| `dataset_README.md` | This file |

## Reproducibility

To regenerate the dataset from source JSON:

```bash
cd ResearchData/
pip install pandas
python3 build_dataset.py
```

The script reads all JSON files from `../public/data/` and outputs `iranwar_event_dataset.csv` and `codebook.csv` to the current directory. Event IDs are deterministically generated and stable across re-runs if source data is unchanged.

## Suggested Citation

> Thomas, J. (2026). IranWar.ai Event-Level Research Dataset: 30-Day OSINT Record of the 2026 US-Iran Conflict (Operation Epic Fury). Extracted from the IranWar.ai Intelligence Dashboard (https://iranwar.ai). GitHub: https://github.com/jethomasphd/WarTheater.

## License

This dataset is derived from the IranWar.ai project. See the repository root for license terms.

## Disclaimer

This dataset is compiled from open-source intelligence (OSINT) and should not be treated as ground truth. Casualty figures, cost estimates, and operational details reflect the best available information at the time of reporting and may be revised as more information becomes available. Researchers should cross-reference with primary sources for any claims used in publication.
