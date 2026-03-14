# War Theater — Day 15 Update Summary (March 14, 2026)

**Update performed:** 2026-03-14
**Market data as of:** March 14, 2026 close
**Brent Crude:** $103.86/bbl | **S&P 500:** 6,632.19

---

## 1. BASELINES.JSON — Pre-War Financial Corrections

All pre-war baseline values (Feb 27, 2026) audited against primary sources:

| Field | Old Value | New Value | Source Confidence |
|-------|-----------|-----------|-------------------|
| oil.brent | 72.38 | 71.00 | High (EIA STEO) |
| oil.wti | 70.82 | 66.50 | Medium-high (FX Daily Report) |
| gas.national_avg | 3.05 | 2.98 | High (AAA weekly) |
| markets.sp500 | 6,867 | 6,878.88 | Exact (CNBC verified close) |
| markets.nasdaq | 22,100 | 22,668.21 | Exact (CNBC verified close) |
| markets.djia | 51,300 | 48,977.92 | Exact (CNBC verified close) |
| treasury.us_10yr_yield | 4.05 | 3.97 | Exact (Advisor Perspectives) |
| treasury.dxy | 98.20 | 97.57 | Medium-high (FX Daily) |
| commodities.gold_oz | 4,980 | 5,236 | High (4 sources converge) |
| commodities.silver_oz | 71.50 | 92.06 | High (Fortune verified) |
| commodities.vix | 19.20 | 19.86 | High (Cboe official) |
| defense_stocks.RTX | 128.50 | 200.00 | Medium (estimated) |
| defense_stocks.LMT | 485.20 | 647.00 | Medium (estimated) |
| defense_stocks.NOC | 520.80 | 640.00 | Medium (estimated) |
| defense_stocks.GD | 298.40 | 325.00 | Low-medium (estimated) |
| defense_stocks.BA | 178.90 | 200.00 | Low-medium (estimated) |
| oil_stocks.XOM | 108.30 | 122.00 | Low-medium (estimated) |
| oil_stocks.CVX | 152.60 | 186.75 | Exact (Simply Wall St verified) |
| national_debt.total_trillions | 38.86 | 38.73 | Adjusted to Feb 27 date |

**Added:** Top-level `audit` object with verified_closes, estimated_from_context, unverified arrays, and primary_sources list.

---

## 2. CARRIERS.JSON — Naval Asset Corrections

### Decommissioned Cruiser Replacements
- CG-52 USS Bunker Hill → **CG-65 USS Chosin** (CSG-3)
- CG-68 USS Anzio → **CG-64 USS Gettysburg** (CSG-12)
- CG-56 USS San Jacinto → **CG-71 USS Cape St. George** (CSG-10)

### Schema Changes
- Submarine aircraft field: `"N/A"` → `null`
- Added `operation_start_date: "2026-03-01"` to all entries
- Split `status` into enum `status` (ENGAGED/DEPLOYED/STANDBY) + `mission_summary`
- Normalized DDG-113 `strike_group` to `"CSG-3 (detached)"` with new `detachment_note` field
- Offset DDG-117 position slightly east (26.15, 57.30) to resolve LHA-6 co-location

---

## 3. HORMUZ.JSON — Strait of Hormuz Corrections

| Field | Old | New | Reason |
|-------|-----|-----|--------|
| percent_global_lng | 25 | 20 | Corrected from multiple sources |
| closure_date | 2026-03-01 | 2026-03-04 | CRS Report formal date |
| closure_method | (inaccurate) | Comprehensive rewrite | Asymmetric denial description |
| daily_oil_flow_current_mbd | 1.2 | 1.3 | TankerTrackers.com midpoint |
| status | (fabricated) | Comprehensive rewrite | No US escort convoys as of Mar 14 |
| insurance_cost_increase_pct | 1100 | 400 | CRS report: 4x, not 11x |
| tankers_transiting_prewar_daily | 85 | 50 | USNI: 50 tanker transits on Feb 28 |
| tankers_transiting_current_daily | 8 | null + note | Not independently verifiable |
| vessels_attacked_total | 8 | 16 | NYT: 16+ vessels attacked |
| stranded_tankers | 390 | 1,000 | AP journalist Mar 14 report |
| escorted_convoy_transits | 8 | 0 | No convoys conducted — Wright claim retracted |
| us_navy_engaged_march_12 | true | false | No engagement occurred |
| irgc_batteries_destroyed_march_13 | 5 | null | Strike was Kharg Island, not strait batteries |

**Added fields:** closure_declared_by, closure_type, kharg_island_distance_from_strait_km, stranded_tankers_oil_only, shadow_tanker_transit_note, kharg_island_strike_march_13/note, vessels_sunk_or_damaged_by_us, iranian_minelayers_destroyed, us_military_deaths, seafarer_fatalities, brent_crude_prewar/current/increase_pct, iea/us_spr_release_mbarrels, iran_selective_passage/note, us_escort_status

---

## 4. TIMELINE-EVENTS.JSON — Major Expansion

**Original entries:** 43
**Final entries:** ~88
**New entries added:** ~45

### New threads added:
- **Iraqi militia/PMF front** (5 entries): Feb 28, Mar 2, Mar 5, Mar 8, Mar 11
- **Houthi operations** (5 entries): Mar 1, Mar 5, Mar 8, Mar 10, Mar 13
- **Cyber warfare** (4 entries): Feb 28, Mar 3, Mar 7, Mar 12 — new `cyber` category
- **Nuclear BDA** (3 entries): Mar 1, Mar 4, Mar 9
- **Iranian drone operations** (3 entries): Feb 28, Mar 4, Mar 9
- **Oil price tracking gaps** (3 entries): Mar 1, Mar 3, Mar 5
- **S&P 500 tracking gaps** (3 entries): Mar 1, Mar 3, Mar 7
- **Diplomatic gaps** (6 entries): Saudi Arabia, India, Iraq, Japan/SK, Oman, Turkey
- **Israeli casualties & Iron Dome** (2 entries): Mar 2, Mar 6
- **Humanitarian running totals** (3 entries): Mar 6, Mar 10, Mar 12
- **US domestic** (3 entries): polls, protests, consumer sentiment
- **US force posture** (2 entries): B-2 opening strikes, IADS suppression
- **Financial gaps** (2 entries): Treasury/dollar flight-to-safety, supply chain cascades
- **Week 1 summary** (1 entry): cumulative tracker

### Key fixes:
- **Minab school**: Corrected from "23 children" to "165-180 killed" with Tomahawk attribution
- **Port Shuaiba**: Correctly attributed 6 US KIA to Port Shuaiba (not Ali Al Salem)
- **US KIA progression**: Now tracks 6 → 7 (Syria drone, Mar 6) → 8 (PSAB, Mar 11)
- **Mar 10 description**: Updated with S&P rebound explanation
- **Pre-war baselines**: All references updated (gas $2.98, S&P 6,878.88)
- **Gas price percentages**: Recalculated against corrected $2.98 baseline

---

## 5. STRIKES-IRAN.JSON — US/Israeli Strikes on Iran

**Original entries:** 19
**Final entries:** 28 + 1 metadata object

### Critical corrections:
- **minab-school**: Complete rewrite — date corrected to Feb 28, casualties to 165-180, Tomahawk confirmed, triple-tapped
- **tehran-leadership**: Targets disaggregated by date with detailed casualty notes
- **tehran-east-residential**: Refined to Resalat Square, corrected coords, active_days to [11] only
- **ahvaz-hospital**: Replaced with ahvaz-military — proper military target entry with hospital collateral noted
- **bandar-abbas**: Removed unverified USS Paul Ignatius reference
- **shiraz-airbase**: Appended IDF airbase campaign info

### New entries:
karaj, kerman, qom-city, konarak-naval, khojir-military, tehran-civilian-sites, isfahan-missile, shiraz-missile-base, khorramabad-lec

### New fields:
- `actor` field added to all entries (us, israel, us_israel_joint)
- Metadata object with aggregate casualty data and conflict scope

---

## 6. STRIKES-RETALIATION.JSON — Iranian & Proxy Retaliation

**Original entries:** 16
**Final entries:** 24

### Critical corrections:
- **ali-al-salem-kuwait**: Removed false 6 KIA attribution (belonged to Port Shuaiba), expanded active_days to [1-8], removed Fattah hypersonic claim
- **bahrain-nsab**: Updated from "no casualties" to 2 killed + 8 injured, active_days expanded to [1-14]
- **haifa-israel**: Fixed first_strike to Mar 2 (not Feb 28), type changed to hezbollah_front
- **tel-aviv-israel**: Added cluster munition casualties (2 killed in Yehud, Mar 9)
- **beirut-lebanon**: Updated to 773+ killed, 800K+ displaced, ground invasion "NOT YET LAUNCHED"
- **hormuz-shipping-attacks**: Timeline starts Day 3 (not Day 12), comprehensive rewrite
- **saudi-base-attack**: Renamed to prince-sultan-air-base-saudi with correct coordinates and Sgt. Pennington details
- **saudi-oil**: First strike corrected to Mar 2

### New entries:
beit-shemesh-israel (9 Israeli KIA), port-shuaiba-kuwait (6 US KIA), camp-buehring-kuwait, jordan-intercepts, akrotiri-cyprus, oman-ports, kuwait-intl-airport, us-embassy-kuwait, kc135-crash-iraq (6 US crew KIA)

### New fields:
- `verified` boolean and `last_updated` fields added to each entry

---

## 7. DASHBOARD UI CHANGES

### Record of Events (Timeline)
- Added **search bar** with real-time text filtering across title, description, data_point, and source
- Added **sort toggle** button (Newest First / Oldest First) — defaults to newest first
- Added **result count** indicator
- Added **Cyber** category filter button
- Added `cyber` category support with green color (#10b981) in labels and timeline rendering

### About Section
- Removed repetitive "flood" metaphor (appeared 6 times, now 0)
- Removed duplicate euphemism references ("surgical strike" / "degraded capability" appeared twice, now once implicitly)
- Consolidated "The Flood" and "The Theater" sections into single "Signal and Noise" section
- Simplified "The Space Between" to remove redundant examples
- Updated Data Fidelity section with more specific source citations and audit trail reference
- Streamlined "The Experiment" section
- Renamed "Spread the Signal" to "Contribute" — more direct
- Reduced overall About section by ~30% while preserving all substantive content

### Financial Metrics (Hero)
- Brent: $98.82 → $103.86 (+46.3%)
- WTI: $95.28 → $99.50 (+49.6%)
- Gas: $3.82 → $3.95 (+32.6%)
- S&P 500: 6,672.62 → 6,632.19 (-3.6%)
- Daily cost: $580M → $590M
- Total cost: $7.0B → $7.6B (15 days)

### Humanitarian Metrics
- US Military Deaths: 8 → 13 (7 enemy fire + 6 KC-135 crash)
- Minab reference: "23 children" → "165-180 killed"
- Briefing text updated with KC-135 crash details

### Charts
- Oil chart: Added Mar 14 data point, corrected pre-war baseline to $71.00/$66.50
- Markets chart: Added Mar 14 data point (S&P indexed to 96.4)
- Hormuz chart: Added Mar 14, corrected pre-war tankers from 85 to 50
- Daily cost chart: Added Day 15 ($590M), cumulative $7.6B
- Insurance premium tooltip: 1100% → 400%

### Other
- Cache-busting version strings updated to 20260314
- Calculator pre-war gas base: $3.05 → $2.98, current: $3.48 → $3.95
- Data.js fallback values updated to Day 15 figures

---

## 8. VALIDATION

- [x] All 6 JSON files pass Python JSON validation
- [x] Timeline covers every day Feb 28 – Mar 13 with 2+ entries each
- [x] Oil price data exists for all required dates
- [x] S&P 500 data exists for all required dates
- [x] US KIA progression: 6 → 7 → 8 → 13 (with KC-135 crash) properly logged
- [x] Iraqi militia thread: 5 entries across conflict
- [x] Houthi thread: 5 entries across conflict
- [x] Cyber thread: 4 entries (new category)
- [x] Nuclear BDA thread: 3 entries
- [x] All decommissioned cruisers replaced with active vessels
- [x] Minab school corrected across all files
- [x] Port Shuaiba properly attributed as location of 6 US KIA
- [x] Pre-war baselines corrected across all files and JS
- [x] No references to old baseline values remain in index.html or active JS

---

## 9. FILES MODIFIED

| File | Type | Changes |
|------|------|---------|
| public/data/baselines.json | Data | Complete rewrite with corrected values + audit object |
| public/data/carriers.json | Data | Cruiser replacements, schema normalization |
| public/data/hormuz.json | Data | 15+ field corrections, 12+ new fields |
| public/data/timeline-events.json | Data | 45 new entries, 3 fixes, sorted chronologically |
| public/data/strikes-iran.json | Data | 10 new entries, 5 major corrections, actor field |
| public/data/strikes-retaliation.json | Data | 9 new entries, 8 major corrections |
| public/index.html | UI | About section cleanup, Record search/filter, hero metrics, cyber button |
| public/js/timeline.js | UI | Search, sort, cyber category, result count |
| public/js/financial.js | Charts | Day 15 data, corrected baselines, insurance fix |
| public/js/humanitarian.js | Charts | Minab correction |
| public/js/calculator.js | Logic | Gas baseline correction |
| public/js/data.js | Logic | Fallback values updated |
