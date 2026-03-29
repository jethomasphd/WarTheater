# IranWar.ai: An Open-Source Event-Level Dataset of the 2026 US-Iran Conflict

**Authors**: J. Eric Thomas, PhD

**Preprint**: [To be submitted to SSRN / OSF Preprints / arXiv]

**Data Repository**: https://github.com/jethomasphd/WarTheater

**Dashboard**: https://iranwar.ai

---

## Abstract

We introduce the IranWar.ai Event-Level Research Dataset, a structured, openly available record of the first 30 days of the 2026 US-Iran conflict (Operation Epic Fury, February 28 -- March 29, 2026). The dataset contains 1,653 event-level observations across 48 variables, extracted from 17 curated JSON data files that power the IranWar.ai public intelligence dashboard. Each row represents a discrete observable event — an airstrike on a specific target on a specific day, a retaliation attack, a financial market data point, a daily casualty estimate for a specific faction, a naval deployment, or a diplomatic development. The dataset spans nine analytical domains (military strikes, retaliation attacks, naval operations, financial markets, diplomatic actions, humanitarian impacts, cyber operations, general military events, and reference data) and integrates open-source intelligence (OSINT) from over 60 primary sources including CENTCOM, IDF, ACLED, the Iranian Red Crescent, IAEA, Bloomberg, and the IMO. All data, code, and documentation are released under an open license to support research in political science, international relations, public health, psychology, psychiatry, and trauma studies. We describe the data collection methodology, the event-level schema design, known limitations, and invite collaborative contributions from the research community.

---

## 1. Introduction

The US-Iran conflict that began on February 28, 2026 — designated Operation Epic Fury by the US Department of Defense — represents the largest American military engagement since the 2003 invasion of Iraq. Within its first 30 days, the conflict produced over 30,500 US and Israeli strike targets across 26 of Iran's 31 provinces, an effective closure of the Strait of Hormuz affecting 20% of global oil supply, a 58% surge in Brent crude oil prices, the opening of secondary fronts in Lebanon and Yemen, and casualty estimates in the thousands across multiple countries.

The pace and complexity of this conflict create an urgent need for structured, research-ready data. Existing sources — news reports, think-tank analyses, government press releases — are fragmented across organizations, inconsistent in format, and difficult to analyze quantitatively. Real-time tracking dashboards provide situational awareness but are designed for visualization, not statistical analysis.

The IranWar.ai project addresses this gap. Originally built as a public-facing OSINT intelligence dashboard (https://iranwar.ai), it has tracked the conflict daily since Day 1 using structured JSON data files that feed interactive maps, charts, and briefings. This paper describes the transformation of that dashboard data into a research-ready, event-level CSV dataset suitable for quantitative analysis.

We release this dataset with three goals: (1) to provide researchers with immediate access to structured conflict data without the months-long lag typical of academic datasets; (2) to establish an open, versioned, and reproducible data infrastructure that can be updated as the conflict continues; and (3) to invite collaborative contributions from researchers across disciplines who can bring domain expertise to data validation, extension, and analysis.

### 1.1 Related Work

Event-level conflict datasets have a strong tradition in political science and peace research. The Uppsala Conflict Data Program (UCDP) Georeferenced Event Dataset (Sundberg & Melander, 2013) and the Armed Conflict Location & Event Data Project (ACLED; Raleigh et al., 2010) provide global coverage of political violence events, but with reporting lags of weeks to months. The Militarized Interstate Dispute (MID) dataset (Palmer et al., 2022) captures interstate conflicts at lower temporal resolution. For economic dimensions of conflict, researchers typically rely on FRED, Bloomberg, or custom data collection.

Our dataset differs from these in three ways. First, it is released in near-real-time — within the first month of the conflict — rather than retrospectively. Second, it integrates military, financial, humanitarian, and diplomatic data in a single event-level structure, enabling cross-domain analysis. Third, it is fully reproducible: the extraction script, source data, and codebook are versioned in a public git repository.

---

## 2. Data Collection

### 2.1 The IranWar.ai Dashboard

The IranWar.ai dashboard is a static-site intelligence dashboard built with HTML, CSS, and JavaScript (no backend framework), hosted on Cloudflare Pages, and powered entirely by structured JSON files stored in a public GitHub repository. The dashboard has been updated daily since Day 1 of the conflict using a two-phase protocol:

1. **Phase 1 (Deep Research)**: A research agent processes the latest reporting from primary sources (CENTCOM press releases, IDF statements, ACLED event data, Reuters/AP wire reports, government ministry statements, satellite imagery analysis, financial data feeds) and produces an "Update Manifest" — a structured document listing every data change for the day.

2. **Phase 2 (Code Execution)**: A coding agent applies the manifest to the JSON data files, validates all modifications, and commits to the repository. Changes deploy automatically to the live dashboard.

This protocol ensures that every data point is traceable to a primary source, and the full history of changes is preserved in git.

### 2.2 Source Attribution

The dashboard draws from over 60 primary sources, including:

- **US Government**: CENTCOM, DoD, Pentagon, White House, CISA, State Department
- **Israeli Government**: IDF, Magen David Adom
- **Iranian Sources**: Red Crescent, Health Ministry, IRNA, HRANA (US-based human rights organization)
- **International Organizations**: IAEA, WHO, OCHA, UNHCR, IMO, IEA
- **Conflict Monitoring**: ACLED, Critical Threats Project (CTP-ISW), Bellingcat, BBC Verify
- **Financial Data**: Bloomberg, ICE Futures, NYMEX, AAA, EIA, FRED
- **Military Tracking**: USNI Fleet Tracker, CRS Reports, DVIDSHUB
- **News Wire Services**: Reuters, AP, AFP, Al Jazeera, CNN, NYT

Source attribution is preserved at the record level in most data files and propagated to the research dataset.

---

## 3. Dataset Construction

### 3.1 Design Principles

The dataset was designed around four principles:

1. **Event-level granularity**: Each row represents a single discrete event, not an aggregate. A researcher can aggregate; they cannot disaggregate.

2. **Cross-domain integration**: Military strikes, financial data, humanitarian impacts, and diplomatic events share a common schema, enabling cross-domain analysis (e.g., correlating strike tempo with oil price movements).

3. **Preservation of all source data**: No information from the source JSON files was discarded. Fields that don't map to the common schema are preserved in domain-prefixed extra columns.

4. **Reproducibility**: The extraction script (`build_dataset.py`) regenerates the entire dataset from source JSON files. Running the script on the same source data produces identical output.

### 3.2 Schema Design

Every row contains nine required columns:

| Column | Description |
|--------|-------------|
| `event_id` | Unique sequential identifier (EVT-0001, EVT-0002, ...) |
| `date` | ISO 8601 date (YYYY-MM-DD) |
| `datetime_utc` | Full timestamp when available |
| `day_of_conflict` | Integer (Day 0 = pre-war baseline, Day 1 = first strikes) |
| `event_domain` | Primary classification (9 categories) |
| `event_type` | Subcategory within domain (25 unique values) |
| `event_description` | Free-text description |
| `source_file` | Which JSON file the row was extracted from |
| `source_record_id` | Original identifier from source data |

These are supplemented by 17 domain-specific columns (location, actors, weapons, casualties, financial metrics, infrastructure type) and 22 extra columns preserving domain-specific detail (naval escorts, strike notes, daily aggregate snapshots, etc.). All domain-specific columns are NULL when not applicable to a given event type.

### 3.3 Event Domain Taxonomy

| Domain | N | Description |
|--------|---|-------------|
| STRIKE | 641 | US/Israeli offensive military strikes on Iranian territory |
| RETALIATION | 307 | Iranian, Hezbollah, Houthi, and proxy counter-attacks |
| FINANCIAL | 301 | Oil prices, market indices, war costs, tanker transits, baseline metrics |
| HUMANITARIAN | 173 | Daily casualty reports by faction, infrastructure damage |
| OTHER | 69 | Daily briefing headlines, aggregate snapshots, historical comparisons |
| DIPLOMATIC | 66 | Political statements, ceasefire negotiations, domestic politics |
| MILITARY | 64 | General military events, US military base reference data |
| NAVAL | 28 | Fleet deployments, Strait of Hormuz events, strategic geography |
| CYBER | 4 | Offensive and defensive cyber operations |

### 3.4 Explosion Logic

Two source files — `strikes-iran.json` and `strikes-retaliation.json` — use a compact representation where one record describes a location that was active across multiple days. These are "exploded" into event-level rows:

- **Strikes on Iran**: Each of 61 location records contains arrays of `targets` (specific installations) and `active_days` (days the location was struck). The Cartesian product yields one row per target per active day: 620 total rows.

- **Retaliation strikes**: Each of 72 location records contains an `active_days` array but no target sub-array. Explosion yields one row per active day: 237 total rows.

This granularity enables analysis of strike tempo, geographic concentration, and target selection patterns over time.

### 3.5 Data Confidence Scoring

Every row receives a `data_confidence` rating:

- **HIGH** (76% of rows): Extracted directly from structured data fields with authoritative source attribution (CENTCOM, DoD, IDF, IAEA, verified financial feeds).
- **MEDIUM** (20%): Inferred from secondary sources (ACLED, satellite imagery, interpolated financial data).
- **LOW** (4%): From unverified reports, Wikipedia-sourced entries, or records explicitly flagged as unconfirmed in the source data.

---

## 4. Summary Statistics

### 4.1 Temporal Coverage

The dataset spans from January 2, 2026 (pre-war oil price data) through March 29, 2026 (Day 30 of the conflict). The conflict event window is February 28 -- March 29, 2026.

### 4.2 Geographic Coverage

Strike and retaliation records span 13 countries or zones: Iran, Israel, Kuwait, Qatar, UAE, Bahrain, Iraq, Saudi Arabia, Lebanon, Jordan, Cyprus, Oman, and International Waters (Strait of Hormuz). Within Iran, strikes affected 61 distinct locations across 26 of 31 provinces.

### 4.3 Column Completeness

Core columns (event_id, date, day_of_conflict, event_domain, event_type, event_description, source_file, data_confidence) are 100% complete. Geographic columns (location, lat/lon, country) are populated for 53-55% of rows (geographic data is not applicable to financial, diplomatic, and humanitarian time-series events). Casualty columns are populated for 26% of rows. Financial metric columns are populated for 15% of rows.

### 4.4 Source File Contribution

The timeline-events file contributes the most diverse set of events (293 rows spanning all domains), while the strike files contribute the most rows by volume (620 + 237 = 857 rows, 52% of the dataset).

---

## 5. Known Limitations

Researchers should be aware of the following limitations:

1. **Casualty figures are from initial reports.** Iranian casualty data comes primarily from the Iranian Red Crescent and HRANA. These figures are difficult to verify independently due to internet blackouts and the fog of war. Discrepancies between sources (e.g., Red Crescent reporting 1,900+ killed vs. HRANA reporting 3,461) are documented in the data but not reconciled.

2. **Daily casualty data represents estimates, not counts.** The `casualties.json` data is derived from chart-display data on the dashboard, representing estimated daily killed per faction. These are not ground-truth body counts. Cumulative totals in the snapshot columns may not equal the sum of daily estimates.

3. **Four retaliation location records are unverified.** The `strike_verified` column flags records where open-source confirmation was not found as of the extraction date.

4. **Financial data has gaps on non-trading days.** Oil prices and market indices are NULL on weekends and holidays. Market sector data is normalized (Feb 27 = 100), not raw index values.

5. **War cost estimates are interpolated.** Two anchor points — $11.3B through Day 6 (Pentagon) and $16.5B through Day 12 (CSIS) — anchor the cost time series. Inter- and extrapolation uses estimated daily run rates.

6. **Strike active_days indicate location-level activity, not sortie counts.** A single active day may represent multiple strikes or a sustained bombardment.

7. **The dataset cannot capture what was not reported.** Events that evaded media coverage, classified operations, and actions in areas under communications blackout are not represented.

8. **Timezone imprecision.** Timeline event timestamps reflect the timezone of the reporting source (which varies: Iran/IRST, Gulf/GST, Israel/IST, US/ET) and are not normalized to UTC.

---

## 6. Research Applications

This dataset is designed to support multiple research agendas:

### 6.1 Political Science and International Relations
- Strike tempo and escalation dynamics (daily strike counts, target category shifts)
- Deterrence failure analysis (retaliation patterns in response to specific strike types)
- Coalition behavior (actor_initiating distributions over time)
- Ceasefire negotiation dynamics (diplomatic events correlated with military tempo)

### 6.2 Economics and Financial Markets
- Oil price response to military events (event study designs using strike/financial data)
- Market sector divergence (defense vs. airlines vs. broad market)
- Economic cost estimation (war cost time series with confidence intervals)
- Supply chain disruption (tanker transit data as proxy for Hormuz closure effects)

### 6.3 Public Health, Psychology, and Trauma Studies
- Population-level trauma exposure estimation (strike frequency × geographic proximity to population centers)
- Civilian casualty patterns (infrastructure_target_type = "civilian" events by day and location)
- Displacement dynamics (snapshot_displaced time series)
- Child mortality patterns (snapshot_children_killed, the Minab school event)
- Healthcare system degradation (infrastructure damage to hospitals, WHO-verified attacks on healthcare)

### 6.4 Military Science
- Air campaign effectiveness (targets struck vs. stated objectives)
- Naval blockade dynamics (tanker transits, vessel attacks, insurance cascades)
- Historical comparison (Iran 2026 vs. Iraq 2003, Gulf 1991, Libya 2011)
- Force disposition analysis (carrier positions, deployment timelines)

### 6.5 Media and Communication Studies
- Framing analysis (event_description text across domains)
- Source attribution patterns (timeline_source field)
- Information lag analysis (first_strike dates vs. reporting dates)

---

## 7. Invitation to Collaborate

We release this dataset as a living resource and explicitly invite collaborative contributions. The following types of contributions are especially welcome:

### 7.1 Data Validation
Researchers with regional expertise (Iranian studies, Gulf politics, Israeli security) can help verify unconfirmed records, resolve casualty discrepancies, and cross-reference against local-language sources.

### 7.2 Data Extension
- **Sub-national coding**: Adding province-level or district-level codes for Iranian strike locations
- **Target taxonomy**: Refining the infrastructure_target_type classification with domain expertise
- **Casualty disaggregation**: Breaking down composite casualty reports into structured fields
- **Economic impact variables**: Adding exchange rates, commodity prices, shipping indices, or insurance premiums

### 7.3 Methodological Contributions
- **Event deduplication**: Some events may appear in both timeline-events.json and strike files — methods for systematic deduplication are welcome
- **Temporal resolution**: Improving datetime precision using cross-referenced reporting timestamps
- **Confidence calibration**: Empirical assessment of the HIGH/MEDIUM/LOW confidence ratings against later-confirmed reports

### 7.4 Analysis and Publication
We encourage researchers to use this dataset for peer-reviewed publications. We ask only for appropriate citation and that any corrections or extensions be contributed back to the repository.

### How to Contribute

1. Fork the repository at https://github.com/jethomasphd/WarTheater
2. Add data, corrections, or analysis to the `ResearchData/` directory
3. Submit a pull request with a description of your contribution
4. For questions or coordination, open an issue on the repository

---

## 8. Ethics Statement

This dataset documents a real, ongoing armed conflict. The data includes records of civilian casualties, attacks on schools and hospitals, and other events involving human suffering. Researchers using this data should:

1. Treat casualty figures with appropriate gravity and uncertainty. These numbers represent real human lives.
2. Acknowledge the limitations of OSINT data in conflict zones, particularly regarding civilian harm.
3. Be transparent about the provenance and limitations of any findings.
4. Consider the potential for their work to be misused or misinterpreted.
5. Follow their institutional IRB/ethics board guidance for research involving conflict data.

The authors affirm that this dataset was compiled exclusively from publicly available open-source intelligence. No classified, proprietary, or restricted-access data was used.

---

## 9. Conclusion

The IranWar.ai Event-Level Research Dataset provides the research community with immediate, structured access to multi-domain data from the 2026 US-Iran conflict. By releasing 1,653 event-level observations across military, financial, humanitarian, and diplomatic domains — with full source attribution, confidence scoring, and reproducible extraction code — we aim to lower the barrier to rigorous quantitative analysis of this conflict.

The dataset will be updated monthly as the conflict continues, with each release versioned and snapshotted. We invite researchers across disciplines to validate, extend, and analyze this data, and to contribute their findings and improvements back to the open-source repository.

---

## Data Availability Statement

The complete dataset, codebook, extraction script, source data, and documentation are available at:

- **Repository**: https://github.com/jethomasphd/WarTheater
- **Dataset directory**: `ResearchData/`
- **Live dashboard**: https://iranwar.ai

---

## Acknowledgments

The IranWar.ai dashboard and dataset rely on the work of journalists, conflict monitors, humanitarian organizations, and government transparency offices whose reporting makes open-source intelligence possible. We particularly acknowledge the Armed Conflict Location & Event Data Project (ACLED), the Critical Threats Project at AEI, the USNI Fleet Tracker, and the IAEA for their systematic public reporting.

---

## References

Palmer, G., D'Orazio, V., Kenwick, M., & Lane, M. (2022). The MID5 Dataset, 2011-2014: Procedures, coding rules, and description. *Conflict Management and Peace Science*, 39(4), 470-482.

Raleigh, C., Linke, A., Hegre, H., & Karlsen, J. (2010). Introducing ACLED: An Armed Conflict Location and Event Dataset. *Journal of Peace Research*, 47(5), 651-660.

Sundberg, R., & Melander, E. (2013). Introducing the UCDP Georeferenced Event Dataset. *Journal of Peace Research*, 50(4), 523-532.

---

*Corresponding author: J. Eric Thomas (jethomasphd@github)*

*Date: March 2026*

*Version: 1.0 (Day 30)*
