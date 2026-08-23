# Codebook — `data/panel_daily.csv` (Paper 2)

One row per conflict-day, Days 1–170 (2026-02-28 … 2026-08-16). Built by
`src/00_build_panel.py` from the frozen v1.2 event dataset; construction details in
`docs/METHODS.md` §3–5.

| Column | Type | Definition |
|---|---|---|
| `day` | int | Day of conflict (1 = 2026-02-28). Index column. |
| `date` | date | Calendar date (day = date − 2026-02-27). |
| `phase` | cat | Major Combat (1–40), First Ceasefire (41–129), Resumption (130–152), Diplomatic Pause (153–170). Paper 1 phase structure (documented boundaries, corroborated by structural breaks). |
| `strikes` | int | Offensive strike tempo: distinct strike-file locations active that day (STRIKE domain, de-duplicated on `source_record_id`) + discrete STRIKE timeline events. |
| `retal` | int | Retaliation tempo, same operationalization (RETALIATION domain). |
| `strikes_civfac` | int | Distinct civilian-facing strike locations active that day (target type in {civilian, oil_infrastructure, communications, water_infrastructure} or civilian-facing keywords; ANY-target rule at the location-day level). |
| `strikes_milfac` | int | Distinct military-facing strike locations (the remainder; `civfac + milfac ≤ strikes`). |
| `health_insults` | int | New audited health-system insult events with onset that day (register `counted == True`). |
| `hssi` | int | Health-System Stress Index: cumulative `health_insults` through day t (0 → 21). |
| `hssi_pct` | float | `hssi` min-max normalized to 0–100 across Days 1–170. |
| `facil_damage_bench` | float | Benchmark-anchored cumulative Iranian health-facility damage: piecewise-linear through Day 15 = 31 (Health Ministry), Day 39 = 307 (WHO), Day 170 = 309 (IRCS); 0 at Day 0. |
| `facil_damage_pct` | float | `facil_damage_bench` as % of its Day-170 value. |
| `iran_civ` | int | Iranian civilian estimated killed that day (casualties.json; daily, not cumulative). |
| `iran_mil` | int | Iranian military estimated killed that day. |
| `us_mil` | int | US military estimated killed that day. |
| `leb_all` | int | Lebanese estimated killed that day (all categories). |
| `isr_mil` | int | Israeli military estimated killed that day. |
| `killed_total` | int | Sum of the five faction series. |
| `cum_iran_daily` | int | Running sum of `iran_civ + iran_mil` (daily-series cumulative; Day-170 value 3,166). |
| `cum_leb_daily` | int | Running sum of `leb_all` (Day-170 value 2,993). |
| `snap_iranian_killed` | float | Dashboard cumulative Iranian killed snapshot, linearly interpolated between observed days (raw coverage 107/170). Carries the Day-57 re-anchoring (9,226 → 3,375); see METHODS §5, Table 7. |
| `snap_lebanese_killed` | float | Dashboard cumulative Lebanese killed snapshot, interpolated. |
| `snap_displaced` | float | Dashboard cumulative displaced snapshot, interpolated (terminal 1.2M). |
| `snap_children_killed` | float | Dashboard cumulative children-killed snapshot, interpolated (terminal 379). |
| `conf_high_share` | float | Share of that day's STRIKE + RETALIATION + casualty rows with `data_confidence == "HIGH"` (NaN when the day has no such rows). |
| `strike_day` | 0/1 | 1 if `strikes > 0` (89 days). |
| `kinetic_day` | 0/1 | 1 if `strikes > 0` or `retal > 0` (139 days). |

# Codebook — `data/health_system_events.csv`

One row per screened health-system row (82 rows; see METHODS §5). Rows are **retained even
when excluded or merged**, so the audit is inspectable.

| Column | Definition |
|---|---|
| `event_id` | Dataset event id (stable across releases). |
| `day_of_conflict`, `date` | Onset day (strike-file locations dated to first active day). |
| `event_domain`, `event_type`, `source_file`, `country`, `location_name` | Carried from the dataset. |
| `health_category` | facility_attack / workforce_harm / supply_disruption / wash_disruption / access_disruption / system_report. |
| `insult` | True for physical/material blows to the health system; False for surveillance reports. |
| `counted` | True if the row accumulates into the HSSI (insult, not excluded, not a merge duplicate). **21 rows.** |
| `audit_action` | rule / reclassified / excluded / merged_canonical / merged_duplicate. |
| `audit_note` | Reason for any manual audit action (empty for pure rule rows). |
| `data_confidence` | Dataset confidence rating (HIGH/MEDIUM/LOW). |
| `event_description` | Verbatim event text. |
