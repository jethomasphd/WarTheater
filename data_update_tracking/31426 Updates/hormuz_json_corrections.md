# Strait of Hormuz JSON — Correction Instructions

**Date of audit:** 2026-03-14  
**Sources:** CRS Report R45281 (March 11, 2026), Wikipedia (2026 Strait of Hormuz crisis), USNI News, NPR, CNN, CNBC, Al Jazeera, Fortune, Reuters, Foreign Policy, Newsweek, CBS News, Time, Seoul Economic Daily, Alma Research Center

---

## 1. FIELD-LEVEL CORRECTIONS

### `strait.percent_global_lng`
- **Current:** `25`
- **Correct:** `20`
- **Reason:** Multiple sources (EIA, Wikipedia, Al Jazeera) cite ~20% of global LNG. The 25% figure corresponds to seaborne oil trade share, not LNG. The data was transposed.

### `strait.closure_date`
- **Current:** `"2026-03-01"`
- **Correct:** `"2026-03-04"`
- **Reason:** CRS Report and Wikipedia both use March 4 as the date Iranian forces formally declared the strait "closed." The IRGC confirmed closure on March 2, attacks on vessels began March 1, but the formal operational closure — with attacks on transiting vessels and insurance withdrawal — is dated March 4 in authoritative sources. Add a `closure_date_note` field if granularity is needed.

### `strait.closure_method`
- **Current value is inaccurate.** Replace entirely with:
```json
"closure_method": "Asymmetric denial via drone and missile strikes on commercial vessels, triggering insurance-driven shutdown. IRGC used sea drones, anti-ship missiles, and shore-launched projectiles to strike 16+ vessels since Feb 28. War risk insurance withdrawn or repriced at 4-5x prewar rates, making transit economically unviable. Reports of naval mine deployment began ~March 10; US destroyed 16 Iranian minelayers in response. IRGC fast attack craft fleet largely intact per US assessments. Chinese-flagged and shadow fleet vessels continue transiting with de facto Iranian permission."
```

### `strait.daily_oil_flow_current_mbd`
- **Current:** `1.2`
- **Correct:** `1.3`
- **Reason:** Iran exported 1.1–1.5 mbd (mostly to China) from Feb 28 through March 12 per TankerTrackers.com satellite data cited by Reuters. Midpoint estimate is ~1.3. Flag as approximate.

### `strait.status`
- **Current value is fabricated.** Replace entirely with:
```json
"status": "Effectively closed to Western-allied shipping. No US Navy escort convoys have been conducted as of March 14. Energy Secretary Wright confirmed March 12 the US is 'not ready' to escort tankers. Trump said March 13 escorts will happen 'soon.' Iran selectively permitting passage for non-Western vessels: Turkish ship approved March 13, two Indian LPG carriers and one Saudi tanker carrying oil for India allowed through. Shadow fleet and Chinese-flagged vessels account for majority of remaining transits. Approximately 1,000 ships anchored near strait entrance including ~200 oil tankers. US struck Kharg Island military targets March 13, threatening oil infrastructure if strait passage not restored."
```

---

## 2. IMPACT SECTION CORRECTIONS

### `impact.insurance_cost_increase_pct`
- **Current:** `1100`
- **Correct:** `400`
- **Reason:** CRS report and pre-war reporting document premiums rising from 0.125% to 0.2%–0.4% of hull value, i.e. roughly 60%–220% increase in rate. Multiple sources say "four or five times" prewar levels. Use `400` (representing 4x / 300% increase) as the upper bound. Do NOT use 1100 — no source supports it.

### `impact.tankers_transiting_prewar_daily`
- **Current:** `85`
- **Correct:** `50`
- **Reason:** USNI reports 50 tanker transits on Feb 28. The ~138 vessels/day figure (JMIC) includes all vessel types. NPR's industry source says 80-100 total ships. Since the field says "tankers," use 50. If you want total vessels, rename the field and use 138.

### `impact.tankers_transiting_current_daily`
- **Current:** `8`
- **Replace with:** `null`
- **Add field:** `"tankers_transiting_current_note": "Virtually zero for Western-allied tankers. A small number of shadow fleet, Chinese-flagged, and Iranian-permitted vessels transit daily. Precise count unavailable — most tracking relies on AIS signals which many vessels have disabled."`

### `impact.vessels_attacked_total`
- **Current:** `8`
- **Correct:** `16`
- **Reason:** NYT reported at least 16 vessels attacked in the Gulf since the war began (cited by Seoul Economic Daily, March 14). USNI reported 13 as of March 10. UKMTO reported 10 by March 8 alone. The count has continued rising.

### `impact.stranded_tankers`
- **Current:** `390`
- **Correct:** `1000`
- **Add field:** `"stranded_tankers_oil_only": 200`
- **Reason:** AP journalist reported to Al Jazeera on March 14 that ~1,000 ships are anchored near the strait entrance, including ~200 oil tankers. Fortune reported 300+ ships as of March 13 but was likely undercounting. The 390 figure may have been accurate earlier but is stale.

### `impact.shadow_tanker_transits_daily`
- **Current:** `13`
- **Replace with:** `null`
- **Add field:** `"shadow_tanker_transit_note": "USNI/Lloyd's List reports shadow fleet ships made approximately half of all Strait of Hormuz transits in March 2026. Daily count not independently verifiable."`

### `impact.escorted_convoy_transits`
- **Current:** `8`
- **Correct:** `0`
- **Reason:** No US Navy escort convoys have occurred. Energy Secretary Wright's social media claim was retracted and confirmed false by the White House. As of March 14, the Pentagon says escorts are not yet feasible. Trump says they will happen "soon."

### `impact.us_navy_engaged_march_12`
- **Current:** `true`
- **Correct:** `false`
- **Reason:** No US Navy engagement with IRGC forces occurred on March 12 in the strait. Remove or set to false.

### `impact.irgc_batteries_destroyed_march_13`
- **Current:** `5`
- **Correct:** `0` (for this specific claim)
- **Reason:** The March 13 strike was on Kharg Island (~300 miles northwest of the strait), not on IRGC coastal batteries along the strait. Replace with:
```json
"kharg_island_strike_march_13": true,
"kharg_island_strike_note": "US struck military targets on Kharg Island. Oil infrastructure deliberately spared. Trump threatened to reconsider if Iran continues blocking strait.",
"irgc_batteries_destroyed_march_13": null
```

---

## 3. FIELDS TO ADD

Add these to the `impact` object:

```json
"vessels_sunk_or_damaged_by_us": 90,
"iranian_minelayers_destroyed": 16,
"us_military_deaths": 13,
"seafarer_fatalities": 6,
"brent_crude_prewar_usd": 71.32,
"brent_crude_current_usd": 100,
"brent_crude_increase_pct": 40,
"iea_reserve_release_mbarrels": 400,
"us_spr_release_mbarrels": 172,
"iran_selective_passage": true,
"iran_selective_passage_note": "Iran permitting transit for non-Western vessels on case-by-case basis. Turkish, Indian, and Saudi (India-bound) ships allowed through. Chinese-flagged vessels transiting continuously. Iran exporting 1.1-1.5 mbd to China.",
"us_escort_status": "Not yet operational. Pentagon describes strait as 'kill box.' Escorts planned for late March at earliest. 2,500 Marines (31st MEU aboard USS Tripoli) deploying to region."
```

Add to the `strait` object:

```json
"closure_declared_by": "IRGC",
"closure_type": "De facto (insurance-driven + active attacks on vessels)",
"kharg_island_distance_from_strait_km": 483
```

---

## 4. GEOMETRY — NO CHANGES NEEDED

Island coordinates, chokepoint polygon, and shipping lane paths appear geographically accurate. No corrections required.

---

## 5. FIELDS CONFIRMED ACCURATE — NO CHANGES

- `strait.name`
- `strait.width_km` (33)
- `strait.shipping_lane_width_km` (3)
- `strait.daily_oil_flow_prewar_mbd` (20.5 — slightly high but defensible with condensate)
- `strait.percent_global_oil` (20)
- `impact.vessels_attacked_march_11` (3)
- `impact.alternative_routes` (all three entries and capacities correct)
- `impact.total_alternative_capacity_mbd` (8.15)
- `impact.shortfall_mbd` (12.35 — recalculate if prewar flow changes)
- `geometry.islands` (all coordinates and control attributions correct)
- `geometry.chokepoint` (polygon is reasonable)
- `geometry.shipping_lanes` (paths are reasonable)
