# Codebook — `data/panel_daily.csv`

The daily analysis panel, 170 rows (Day 1–170), built by `src/00_build_panel.py` from the
frozen v1.2 event dataset. One row per conflict-day.

| Variable | Type | Definition |
|---|---|---|
| `day` | int | Day of conflict. Day 1 = 2026-02-28. Index column. |
| `date` | ISO date | Calendar date (= 2026-02-27 + `day`). |
| `phase` | categorical | `Major Combat` (1–40), `First Ceasefire` (41–129), `Resumption` (130–152), `Diplomatic Pause` (153–170). See `docs/METHODS.md §3`. |
| `strikes` | int | **Primary** US/Israeli offensive tempo: distinct offensive locations (`source_record_id`) active that day in the STRIKE domain + discrete STRIKE-domain timeline events. De-duplicates the target×day explosion. |
| `retal` | int | **Primary** Iranian/proxy retaliation tempo: distinct RETALIATION-domain locations active that day + discrete timeline events. |
| `strikes_rows` | int | Raw STRIKE event-rows that day (includes target explosion). Robustness measure. |
| `retal_rows` | int | Raw RETALIATION event-rows that day. (≈ `retal`; retaliation rows are not target-exploded.) |
| `strikes_tl` | int | Timeline-only discrete STRIKE events that day (one reported event = one count). Robustness measure. |
| `retal_tl` | int | Timeline-only discrete RETALIATION events that day. |
| `killed` | int | Summed daily **estimated killed** across the five tracked factions (Iranian military, Iranian civilian, US military, Lebanese all, Israeli military), from `casualties.json`. Daily estimates, **not** cumulative; carry the dataset's casualty caveats. |
| `diplomatic` | int | DIPLOMATIC-domain events that day. |
| `naval` | int | NAVAL-domain events that day. |
| `retal_countries` | int | Distinct countries (excluding `Unknown`) hit by retaliation that day. |
| `cum_countries` | int | Cumulative distinct countries hit by retaliation through day *t* (horizontal diffusion). |

## Provenance / reconstruction

The panel is a deterministic function of the frozen dataset. To rebuild:

```bash
cd ResearchData/Paper1/src && python3 00_build_panel.py
```

`00_build_panel.py` prints cross-checks confirming that the panel's `strikes_rows`,
`retal_rows`, and `diplomatic` totals equal the corresponding domain event counts in the source
dataset (Days ≥ 1).

## Window totals (Day 1–170), for reference

| series | sum | mean/day | max | nonzero days |
|---|---|---|---|---|
| strikes | 386 | 2.27 | 17 | 89 |
| retal | 621 | 3.65 | 20 | 126 |
| killed | 6213 | 36.6 | 257 | 108 |
| diplomatic | 414 | 2.44 | 11 | 139 |
| naval | 84 | 0.49 | 14 | 53 |

(Generated in `output/tables/t01_summary_stats.csv`.)
