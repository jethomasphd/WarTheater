# Codebook — `data/panel_daily.csv`

The daily analysis panel, 170 rows (Day 1–170), built by `src/00_build_panel.py` from the
frozen v1.2 event dataset. One row per conflict-day. It is identical, cell for cell, to the
parent paper's panel (`../data/panel_daily.csv`); step 00 asserts this.

| Variable | Type | Definition |
|---|---|---|
| `day` | int | Day of conflict. Day 1 = 2026-02-28. Index column. |
| `date` | ISO date | Calendar date (= 2026-02-27 + `day`). |
| `phase` | categorical | `Major Combat` (1–40), `First Ceasefire` (41–129), `Resumption` (130–152), `Diplomatic Pause` (153–170). Documented boundaries; recovered by the break detector in step 07. |
| `strikes` | int | **Primary** US/Israeli offensive tempo: distinct offensive locations (`source_record_id`) active that day in the STRIKE domain, plus discrete STRIKE-domain timeline events. De-duplicates the dataset's target × active-day expansion. |
| `retal` | int | **Primary** Iranian/proxy retaliation tempo: distinct RETALIATION-domain locations active that day, plus discrete timeline events. |
| `strikes_rows` | int | Raw STRIKE event rows that day (includes the expansion). Robustness measure. |
| `retal_rows` | int | Raw RETALIATION event rows that day (≈ `retal`; retaliation rows are not expanded). Robustness measure. |
| `strikes_tl` | int | Timeline-only discrete STRIKE events that day (one reported event = one count). Robustness measure. |
| `retal_tl` | int | Timeline-only discrete RETALIATION events that day. Robustness measure. |
| `killed` | int | Summed daily **estimated killed** across the five tracked factions (Iranian military, Iranian civilian, US military, Lebanese all, Israeli military) from `casualties.json`. Daily estimates, not cumulative; carries the dataset's casualty caveats. Used only for the casualty caveat in step 09. |
| `diplomatic` | int | DIPLOMATIC-domain events that day. |
| `naval` | int | NAVAL-domain events that day (descriptive only). |
| `retal_countries` | int | Distinct countries (excluding `Unknown`) hit by retaliation that day. |
| `cum_countries` | int | Cumulative distinct countries hit by retaliation through day *t* (geographic reach). |

## Derived quantities used in the analysis

| Quantity | Where | Definition |
|---|---|---|
| `violence` | step 06 | `strikes + retal`. |
| weekly aggregates | step 06 | Sums over calendar weeks of the conflict, week = (day − 1) // 7; 25 weeks, the last with 2 days. |
| regime-demeaned series | step 08 | `strikes` and `retal` minus their phase means (four documented phases; six detected regimes as sensitivity). |

## Window totals (Day 1–170)

| series | sum | mean/day | max | nonzero days |
|---|---|---|---|---|
| strikes | 386 | 2.27 | 17 | 89 |
| retal | 621 | 3.65 | 20 | 126 |
| killed | 6213 | 36.6 | 257 | 108 |
| diplomatic | 414 | 2.44 | 11 | 139 |
| naval | 84 | 0.49 | 14 | 53 |

(Generated in `output/tables/t01_summary_stats.csv`.)

## Provenance

```bash
cd ResearchData/Paper1/MajorRevision1/src && python3 00_build_panel.py
```

Step 00 verifies the MD5 of the frozen input, prints cross-checks confirming that the
panel's `strikes_rows`, `retal_rows`, and `diplomatic` totals equal the corresponding
domain counts in the source dataset (Days ≥ 1), and asserts identity with the parent panel.
