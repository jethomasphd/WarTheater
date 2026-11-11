# IranWar.ai Update Manifest
## Date: 2026-11-11 | War Day: 257
## Coverage: Events since 2026-10-30 (Day 245 snapshot, 12:25 ET) through 2026-11-11

> **Cycle note.** This is a 12-day catch-up cycle (Days 246–257), not a single-day update. Per-day series (hero `history`, `war-costs`, `casualties`) get one entry per day. `oil-prices` and `markets` get one entry per trading day from Oct 30. Section 9 lists everything held back for human judgment, and Phase 2 skips it. Section 11 ends with **QA flags on included items** for the operator to check before running Phase 2.

### METADATA

**Data horizon per file** (verified against the repo at commit `f299716`; every uploaded file was byte-identical to the repo copy):

| File | Horizon |
|---|---|
| hero-stats.json | war_day **245** (last_updated 2026-10-30, "OCT 30, 2026 12:25 ET") |
| strikes-iran.json | last_updated **2026-10-30**; last strike entry 2026-09-14 |
| strikes-retaliation.json | last_updated **2026-10-30**; last entry `mecca-drone-claim-2026-10-30` |
| carriers.json | no file-level date; latest `last_verified` **2026-10-27** (USNI Oct 26 baseline) |
| timeline-events.json | last entry **2026-10-30** (1,212 events) |
| oil-prices.json | last data point **Oct 29** (Brent 114.88 / WTI 102.00) |
| markets.json | last trading day **Oct 29** (S&P 7,720.39) |
| war-costs.json | last day entry **Day 245** (cumulative ~$74.8B modeled) |
| casualties.json | last day entry **Day 245** (Oct 30) |
| infrastructure.json | no date field; latest notes tagged "DAY 245 (Oct 16-30)" |
| hormuz.json | strait.last_updated **2026-10-30** |
| calculator.json | current_gas **4.2** (AAA $4.2046, Oct 30) |
| historical-comparison.json | last_updated 2026-10-30 ("Iran 2026 (Day 245)") |
| global-bases.json | 28 entries, no date field |
| briefings/index.json | latest briefing **Day 245** (`day-245.html`) |

**Sources consulted** (primary and wire first):
- **Official:** CENTCOM statements (via Stars and Stripes, Maritime Executive, CBS); Pentagon DCAS (via Euronews, Newsweek); Saudi Joint Forces Command and Saudi Energy Ministry (via SPA, AFP, Reuters, Gulf News); UKMTO advisories and weekly reports; Ambrey; Lebanese Ministry of Public Health; India MEA; Velos Tankers; ADNOC/WAM; Dana Gas; EIA (STEO, weekly SPR file); AAA; IMF PortWatch API.
- **Naval:** USNI News Fleet & Marine Tracker for Oct 26, Nov 2 and Nov 9, 2026 (full text), plus USNI News articles of Oct 12 and Nov 5-6; The War Zone.
- **Wires and broadcasters:** AP (closing tables via WTOP; stories via KSAT, AJC, Spokesman-Review); Reuters (via Khaleej Times, The Star, US News, Business Day, Internazionale); CBS News live blogs (Nov 2-11); NBC News; Washington Post; WSJ and FT (as cited by others); Al Jazeera; Times of Israel live blogs; Stars and Stripes; Fox News live blog; Axios (as cited).
- **Analysis and trackers:** CTP-ISW Iran Updates (Oct 30, Nov 2, 3, 4, 6); CFR Global Conflict Tracker; Long War Journal; Lloyd's List Intelligence; Windward; Kpler (via Reuters); Allianz Trade.
- **Iranian outlets (attributed as such):** Tasnim, IRNA, IRIB, Fars, Press TV (via others), Iran International.
- **Gas and airlines:** The National (airline suspensions); Newsquawk and Xinhua (oil settle wraps).

**Access limits this cycle:**
- **GlobalSecurity:** the daily Iran War OPREP returned HTTP 402/403 and was **not** used.
- **USNI:** article pages returned 403 to the fetch tool, so the Nov 2 and Nov 9 tracker text was taken from USNI's public WordPress JSON endpoint. A follow-up attempt was blocked by the session's safety classifier and not retried. **Operator: confirm the Nov 2 and Nov 9 USNI pages in a browser before Phase 2** (key lines were spot-checked against the saved text).
- **Search budget:** the web-search budget was exhausted near the end of the run. Items marked NOT LOCATED were not exhaustively searched (Iran rial, IEA November OMR, war-risk insurance premiums, CTP-ISW for Nov 5 and Nov 7-11).

**Confidence by domain:**

| Domain | Confidence | Basis |
|---|---|---|
| Hero stats (market/oil/gas) | HIGH | AP closing tables; Xinhua/Reuters settles; AAA. Nov 11 oil is PROVISIONAL. |
| Hero stats (tolls) | HIGH (unchanged) / MEDIUM (Lebanese +1) | DCAS reported unchanged through Nov 11 |
| Strikes on Iran | MEDIUM-HIGH | Two US strikes acknowledged by officials/Trump; no CENTCOM release |
| Retaliation / proxy | MEDIUM | Saudi intercepts confirmed; Houthi hit claims largely unverified |
| Naval disposition | HIGH (areas) / MEDIUM (coordinates) | USNI full text; positions are sea-area approximations |
| Timeline | MEDIUM-HIGH | Mostly multi-sourced; 5 single-source items held back |
| Financial (war cost) | LOW | Modeled; no new official figure |
| Humanitarian | HIGH (no change) / MEDIUM | No new HRANA/UN cumulative figures |
| Hormuz | MEDIUM | UKMTO/Ambrey-confirmed incidents; counters are DERIVED floors |

---

### 1. HERO-STATS UPDATES

Confidence: **HIGH** for oil through Nov 10, S&P, gas and official tolls. **MEDIUM** for the Nov 11 oil settles (PROVISIONAL) and the Lebanese +1. **LOW** for war cost, which is modeled.

#### 1a. CURRENT SNAPSHOT

**Top-level fields**
```
last_updated:    "2026-10-30"  →  "2026-11-11"
war_day:         245           →  257
timestamp_label: "LAST UPDATED: OCT 30, 2026 12:25 ET"  →  "LAST UPDATED: NOV 11, 2026 HH:MM ET"   (use the actual ET time at execution)
```

**COST PANEL.** Replace the listed fields. Unlisted fields (e.g., `label` when unchanged) stay as they are.

```
brent:
  price:   "92.76"
  label:   "Brent Crude ($/bbl)"   (unchanged)
  change:  "+1.39% Nov 11 settle (Jan contract, PROVISIONAL); +21.76 (+30.6%) vs pre-war $71.00"
  tooltip: "ICE Brent January 2027 (LCOF7) settled ~$92.76 on Wed Nov 11 (+$1.27; Xinhua/AP, PROVISIONAL, confirm vs ICE) as Iran denied talks were under way and ships were hit off Lima, Oman. Brent has fallen ~21% since the expiring December contract's $117.64 final settle on Oct 30, a six-month high. The fall followed Democratic wins in both chambers and Trump signalling restraint: Nov 4 -8.7% to $94.62 (lowest since Aug 31); Nov 9 -5.85% after Trump called strikes 'highly unlikely'; Nov 10 settle $91.49 after touching $89.16 intraday, the first sub-$90 print since August. Front month rolled Dec→Jan at the Oct 30 expiry (roll gap $4.21). EIA November STEO: ~$100 in Nov-Dec."

wti:
  price:   "86.53"
  label:   "WTI Crude ($/bbl)"   (unchanged)
  change:  "+0.57% Nov 11 settle (Dec contract, PROVISIONAL); +20.03 (+30.1%) vs pre-war $66.50"
  tooltip: "NYMEX WTI December 2026 (CLZ26) settled ~$86.53 on Nov 11 (+$0.49; PROVISIONAL), down from $104.12 on Oct 30. Confirmed Nov 10 settle: $86.04. Nov 4: $88.12 (-8.3%), lowest since Aug 31. The December contract expires ~Nov 19-20. The Brent-WTI spread has narrowed to ~$5.45 (Nov 10) from ~$12.90 in late October."

gas:
  price:   "3.94"
  label:   "US Avg Gas ($/gal)"   (unchanged)
  change:  "-0.26 vs Oct 30 ($4.20); +0.95 (+31.9%) vs pre-war $2.99"
  tooltip: "AAA national average regular $3.9429 on Nov 11, after falling below $4 on Nov 10 ($3.9788). Earlier: $4.1239 Nov 4; $4.1003 Nov 5 (AAA weekly release); $4.2046 Oct 30; month-ago $4.3585. AAA (Nov 5): November pump prices are the highest ever for this time of year. National diesel $6.1306; California diesel $8.0836. EIA weekly retail $3.995 (week of Nov 9). EIA November STEO: US gasoline averages $3.89 in 2026."

sp500:
  value:   "7619.38"
  label:   "S&P 500"   (unchanged)
  change:  "+1.31% Nov 11; +740.50 (+10.8%) vs pre-war 6,878.88"
  tooltip: "Close Wed Nov 11 7,619.38 (+1.31%; AP) on an AI rebound led by CoreWeave, within 2.6% of the Oct 6 record (7,818.93). Window low Nov 5: 7,353.73 (-4.36%, the worst day since April 2025), an AI data-centre rout on moratorium fears after the Democratic sweep. Nov 4: +1.58% and the Dow +3.0% on the midterm result as defense and oil majors fell. Nov 9: +2.35%, best day since Apr 8, after Trump called new strikes 'highly unlikely'. A hot October CPI (Nov 10) pushed the 10-yr back above 5%."

daily_cost:
  value:   "500"
  unit:    "M/day"
  label:   "Daily War Cost ($M/day)"   (unchanged)
  change:  "HELD"
  tooltip: "Estimated daily US operating cost, modeled at $500M/day (methodology unchanged). No new official Pentagon, CBO, CRS or CSIS figure since the $47.1B estimate through mid-October (CBS Oct 27; ABC Oct 28): ~$29B munitions, $11.9B operations, $6B equipment losses, excluding base damage. That implies ~$80M-$120M/day, consistent with CBO's $2B-$3B/month and far below the modeled rate. Hegseth urged Congress (Nov 5) to approve at least $350B in defense funding; a $95B White House package (war plus other priorities) is pending with no vote reported."
  note:    "DERIVED: $500M/day carried forward through Day 257. RECALIBRATION RECOMMENDED: the modeled series now runs ~$31.5B above the official-anchored path (see Section 11)."

total_cost:
  value:   "80.8"
  unit:    "B"
  label:   "Cumulative Cost ($B)"   (unchanged)
  change:  "+6.0 since Day 245"
  tooltip: "MODELED: about $80.8B at Day 257 ($74.8B at Day 245 + 12 × $500M). Not an official figure."
  note:    "DERIVED: accrued at $500M/day. FLAGGED: official-only alternative $47.1B (through ~Oct 16); official-anchored alternative ~$49.3B at Day 257 (~$48.3B at Day 245 + 12 × ~$86M/day, CBO $2-3B/month)."
```

**TOLL PANEL.** Keep each item's existing `color`. Only `lebanese_killed` changes value.

```
targets_struck:
  value:   "35914"   (HELD)
  label:   "Cumulative targets struck (US+IL on Iran/proxies)"   (unchanged)
  note:    "HELD — two acknowledged US strikes on Qeshm (Nov 2, Nov 6); no CENTCOM tally"
  tooltip: "Cumulative targets struck per CENTCOM; no change this cycle (CENTCOM stopped releasing cumulative strike data after May 5). The US acknowledged limited self-defense strikes on Qeshm Island against an IRGC surface-to-air missile launcher (Nov 2) and an air-defence system (Nov 6), with no CENTCOM tally. Iran claims a third strike on the night of Nov 8 (unconfirmed). WSJ reports earlier smaller strikes were kept secret. Hegseth (Nov 10) cited 'more than 13,000 targets in under 40 days', a US-only major-combat figure that is not comparable with this combined cumulative. IRGC drone-shootdown claims are unverified and not counted."

us_kia:
  value:   "23"   (HELD)
  label:   "US service-member deaths (Pentagon DCAS, all causes)"   (unchanged)
  note:    "HELD — no DCAS change Oct 30-Nov 11"
  tooltip: "Official DCAS count of US service-member deaths, combat and noncombat: 23 total, 11 hostile and 12 nonhostile (unchanged; Euronews Nov 9, Newsweek Nov 11). Hegseth (Nov 10) and Trump (Nov 11) cite 18 Americans killed, a hostile-action framing that does not match DCAS. On Nov 9 Trump said 'we haven't lost anybody' in recent months. No US casualties were reported in the Nov 2 and Nov 6 Qeshm strikes."

us_wia:
  value:   "865"   (HELD)
  label:   "US service-member WIA (Pentagon DCAS)"   (unchanged)
  note:    "HELD — DCAS 865 (417 Epic Fury + 448 Overseas Ops)"
  tooltip: "Official DCAS wounded count: 417 under Operation Epic Fury and 448 under 'Overseas Operations' (Newsweek, Nov 11, citing the late-October update). A Daily Caller report (Nov 11) gives 866 'per DCAS' with no as-of date; it is not adopted (single source; see Section 9)."

iranian_killed:
  value:   "3636"   (HELD)
  label:   "Iranian killed (cumulative, tracked line)"   (unchanged)
  note:    "HELD (HRANA, through Apr 7)"
  tooltip: "HRANA cumulative 3,636 as of Apr 7: 1,701 civilians, 1,221 military, 714 unclassified. No authoritative later update located. The US strikes on Qeshm (Nov 2, Nov 6) and the strike Iran claims for Nov 8 reported no casualties; Hormozgan deputy governor Ahmad Nafisi said the Nov 8 targets were outside residential and commercial areas. Other series (Foundation of Martyrs 3,468; Iranian Health Ministry 2,362+ civilians) are not merged."

lebanese_killed:
  value:   "4389"  →  "4390"
  label:   "Lebanese killed (cumulative, all)"   (unchanged)
  note:    "+1 — Israeli drone strike at Qabrikha, Nov 4 (Lebanese MoPH)"
  tooltip: "Lebanese Ministry of Public Health cumulative since Mar 2: 4,390 killed and 12,429 injured, per a Nov 5 MoPH update cited by the Daily Caller (secondary; primary release not located). This is consistent with the prior 4,389 (through Oct 12) plus the Nov 4 death at Qabrikha, Marjayoun, of a Risala Scouts paramedic, reported by the Health Ministry via Times of Israel, which called it the first Israeli airstrike in southern Lebanon in weeks. MoPH total since Oct 2023: almost 9,000 (CBS, Nov 4)."

displaced:
  value:   "1200000"   (HELD)
  label:   "Displaced (cumulative)"   (unchanged)
  note:    "HELD — no new UNHCR/IOM figure"
  tooltip: "Carried forward; Lebanon-weighted. Iran's up to ~3.2M IDPs (UNHCR, Mar 12) are tracked separately. Latest Lebanon IOM DTM round (118, Oct 1): 329,686 internally displaced, 877,203 returned. Yemen is a separate theater and is not added: OCHA counts more than 313,000 displaced since August (Nov 9)."

flights_cancelled:
  value:   "8000"   (HELD)
  label:   "Flights cancelled (cumulative)"   (unchanged)
  note:    "HELD"
  tooltip: "Carried forward; no new cumulative Cirium or FlightAware aggregate. Saudi suspensions extended (The National, Nov 6): Etihad Riyadh/Dammam to Nov 19; flydubai Riyadh/Abha to Nov 16; Lufthansa Riyadh to Nov 18 and Dammam to Nov 30; KLM to Nov 27; Air France Riyadh to Dec 12; British Airways London-Riyadh to Jan 11, 2027; Cathay Pacific Riyadh to Jan 31, 2027. Riyadh King Khalid has operated under restrictions since its partial reopening on Oct 25. The cumulative is likely understated (see Section 9)."

children_killed:
  value:   "379"   (HELD)
  label:   "Children killed (cumulative, tracked)"   (unchanged)
  note:    "HELD"
  tooltip: "Carried forward; no new verified cumulative figure (UNICEF or other). The Yemen theater is not added (e.g., 13 children among 33 killed at al-Shariya on Nov 7, per the Houthi Health Ministry, unverified)."
```

#### 1b. HISTORY ENTRIES

Append **12** objects to `history` (Days 246-257) in this order. The schema matches the current last entry: no `label` key; field order as shown. Weekend days carry the prior close forward with `sp500_change_pct: 0.0` (file convention). Gas uses only confirmed AAA points, carried forward between them: Oct 30 $4.2046 → Nov 4 $4.1239 → Nov 5 $4.1003 → Nov 10 $3.9788 → Nov 11 $3.9429. The Nov 8 ticker value $4.0203 came from a search snippet only and is not used.

**MODIFICATION to the existing Day 245 (2026-10-30) history entry.** Its market fields were captured before the Oct 30 close and still hold Oct 29 values. Replace them with the Oct 30 closes:

```
ENTRY: history[war_day=245]
FIELD: brent             OLD: 114.88    NEW: 117.64   (ICE Brent December LCOZ6 final settle; Newsquawk / Kotak)
FIELD: wti               OLD: 102.0     NEW: 104.12   (NYMEX WTI December CLZ26 settle; Newsquawk)
FIELD: sp500             OLD: 7720.39   NEW: 7580.07  (AP closing table)
FIELD: sp500_change_pct  OLD: -0.3      NEW: -1.82
FIELD: nasdaq            OLD: 26184.72  NEW: 25437.0
FIELD: dow               OLD: 52342.56  NEW: 51770.31
All other Day 245 fields unchanged.
```

```json
[
  {
    "date": "2026-10-31",
    "war_day": 246,
    "brent": 117.64,
    "wti": 104.12,
    "gas": 4.2,
    "sp500": 7580.07,
    "sp500_change_pct": 0.0,
    "nasdaq": 25437.0,
    "dow": 51770.31,
    "daily_cost_millions": 500,
    "total_cost_billions": 75.3,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4389,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 246 (October 31, Saturday) - Iranian team in Doha studies the Vance letter; Araghchi rules out a direct US meeting; Iran claims US fire on Qeshm fishing boats"
  },
  {
    "date": "2026-11-01",
    "war_day": 247,
    "brent": 117.64,
    "wti": 104.12,
    "gas": 4.2,
    "sp500": 7580.07,
    "sp500_change_pct": 0.0,
    "nasdaq": 25437.0,
    "dow": 51770.31,
    "daily_cost_millions": 500,
    "total_cost_billions": 75.8,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4389,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 247 (November 1, Sunday) - Doha round ends without breakthrough; Trump says Iran may need 'the hammer'; Iran blacklists the Royal Navy and RAF"
  },
  {
    "date": "2026-11-02",
    "war_day": 248,
    "brent": 104.77,
    "wti": 96.46,
    "gas": 4.2,
    "sp500": 7541.4,
    "sp500_change_pct": -0.51,
    "nasdaq": 25164.32,
    "dow": 51983.98,
    "daily_cost_millions": 500,
    "total_cost_billions": 76.3,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4389,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 248 (November 2, Monday) - US strikes Qeshm SAM launcher after IRGC fires on a US jet; Iran offers two-day Hormuz timeline; Brent -7.6% to $104.77; Indian sailor killed off Oman"
  },
  {
    "date": "2026-11-03",
    "war_day": 249,
    "brent": 103.6,
    "wti": 96.09,
    "gas": 4.2,
    "sp500": 7568.92,
    "sp500_change_pct": 0.36,
    "nasdaq": 25372.01,
    "dow": 51786.72,
    "daily_cost_millions": 500,
    "total_cost_billions": 76.8,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4389,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 249 (November 3, Tuesday) - Democrats win both chambers in war-shadowed midterms; Ghalibaf says Iran sent a 'firm' reply; Qatar expects feedback within 36 hours"
  },
  {
    "date": "2026-11-04",
    "war_day": 250,
    "brent": 94.62,
    "wti": 88.12,
    "gas": 4.12,
    "sp500": 7688.62,
    "sp500_change_pct": 1.58,
    "nasdaq": 25736.51,
    "dow": 53356.12,
    "daily_cost_millions": 500,
    "total_cost_billions": 77.3,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4390,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 250 (November 4, Wednesday) - Vance: 'the reason we lost is the war'; Khamenei sees no US shift; Brent -8.7% to $94.62; Israeli drone kills paramedic at Qabrikha"
  },
  {
    "date": "2026-11-05",
    "war_day": 251,
    "brent": 98.29,
    "wti": 90.52,
    "gas": 4.1,
    "sp500": 7353.73,
    "sp500_change_pct": -4.36,
    "nasdaq": 24315.0,
    "dow": 51523.06,
    "daily_cost_millions": 500,
    "total_cost_billions": 77.8,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4390,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 251 (November 5, Thursday) - Trump weighs renewed war ('you'll know soon enough'); Iran sends nuclear proposal via Qatar; seafarer killed on Velos Sapphire; S&P -4.4% on AI rout"
  },
  {
    "date": "2026-11-06",
    "war_day": 252,
    "brent": 98.32,
    "wti": 90.83,
    "gas": 4.1,
    "sp500": 7376.86,
    "sp500_change_pct": 0.31,
    "nasdaq": 24579.42,
    "dow": 51285.73,
    "daily_cost_millions": 500,
    "total_cost_billions": 78.3,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4390,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 252 (November 6, Friday) - First post-midterm US strike hits Qeshm air defenses; Trump calls it 'minor'; Taiz market strike kills 30 (attribution disputed)"
  },
  {
    "date": "2026-11-07",
    "war_day": 253,
    "brent": 98.32,
    "wti": 90.83,
    "gas": 4.1,
    "sp500": 7376.86,
    "sp500_change_pct": 0.0,
    "nasdaq": 24579.42,
    "dow": 51285.73,
    "daily_cost_millions": 500,
    "total_cost_billions": 78.8,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4390,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 253 (November 7, Saturday) - CENTCOM stands up Task Force Iron Gate; US aircraft disable M/V Huda; IRGC lifts missile range cap; two tankers hit off Khasab"
  },
  {
    "date": "2026-11-08",
    "war_day": 254,
    "brent": 98.32,
    "wti": 90.83,
    "gas": 4.1,
    "sp500": 7376.86,
    "sp500_change_pct": 0.0,
    "nasdaq": 24579.42,
    "dow": 51285.73,
    "daily_cost_millions": 500,
    "total_cost_billions": 79.3,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4390,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 254 (November 8, Sunday) - Intercept debris damages Aramco tower in Riyadh; drone hits Khor Mor gas field; Araghchi tells the White House to choose; Iran claims new Qeshm strike"
  },
  {
    "date": "2026-11-09",
    "war_day": 255,
    "brent": 92.57,
    "wti": 86.85,
    "gas": 4.1,
    "sp500": 7549.94,
    "sp500_change_pct": 2.35,
    "nasdaq": 25253.14,
    "dow": 52389.75,
    "daily_cost_millions": 500,
    "total_cost_billions": 79.8,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4390,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 255 (November 9, Monday) - Trump: war 'militarily, effectively over' after Qatar PM meeting; East-West pipeline fire near Medina; Brent -5.9% to $92.57"
  },
  {
    "date": "2026-11-10",
    "war_day": 256,
    "brent": 91.49,
    "wti": 86.04,
    "gas": 3.98,
    "sp500": 7520.93,
    "sp500_change_pct": -0.38,
    "nasdaq": 25065.87,
    "dow": 52231.89,
    "daily_cost_millions": 500,
    "total_cost_billions": 80.3,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4390,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 256 (November 10, Tuesday) - Rubio at G7: 'no need' for major combat; Hegseth: 'we control the Strait'; Reuters/Ipsos: 71% want Congress to end the war; ADNOC vessel hit"
  },
  {
    "date": "2026-11-11",
    "war_day": 257,
    "brent": 92.76,
    "wti": 86.53,
    "gas": 3.94,
    "sp500": 7619.38,
    "sp500_change_pct": 1.31,
    "nasdaq": 25466.19,
    "dow": 52486.49,
    "daily_cost_millions": 500,
    "total_cost_billions": 80.8,
    "targets_struck": 35914,
    "us_kia": 23,
    "us_wia": 865,
    "iranian_killed": 3636,
    "lebanese_killed": 4390,
    "displaced": 1200000,
    "flights_cancelled": 8000,
    "children_killed": 379,
    "headline": "Day 257 (November 11, Wednesday) - Trump claims 'total victory' at Arlington; Rezaei: no 'single particle' of enriched uranium leaves Iran; ship disabled off Lima; gas $3.94"
  }
]
```

---

### 2. STRIKES-IRAN UPDATES

Confidence: **MEDIUM-HIGH** (two US strikes on Iranian soil acknowledged by US officials or Trump; no CENTCOM statement for either; GlobalSecurity daily pages unreadable this cycle — HTTP 402/403).

No Israeli strike on Iran was found in-window (Israeli Defense Minister Katz, Nov 8: "mission is still not complete" — CBS).

#### 2a. NEW ENTRIES

Append these three objects to the end of the array, using the field order of the current last entry (`id, city, lat, lng, type, actor, weapon, targets, first_strike, casualties_reported, casualties_source, active_days, notes`).

```json
{
  "id": "us-strike-qeshm-sam-launcher-20261102",
  "city": "Qeshm Island, Hormozgan",
  "lat": 26.85,
  "lng": 55.9,
  "type": "us_strike",
  "actor": "US",
  "weapon": "US fighter aircraft (type and munition not disclosed)",
  "targets": ["IRGC surface-to-air missile launcher (US officials); anti-aircraft facility 'we watched it get built' (Trump); radar and missile launchers (NewsNation sources)"],
  "first_strike": "2026-11-02",
  "casualties_reported": "None reported by either side",
  "casualties_source": "US officials via NBC News / CBS News / Stars and Stripes (Nov 3); CTP-ISW Iran Update (Nov 3)",
  "active_days": [248],
  "notes": "Self-defense strike, per US officials: on the evening of Mon Nov 2 the IRGC fired a surface-to-air missile at a US fighter over the Strait of Hormuz, and the jet struck the launcher. The same day the US intercepted an IRGC missile fired from Qeshm at commercial shipping (US officials; CTP-ISW Nov 3). Iranian state media reported five explosions (via NBC); IRNA via Al Jazeera reported rapid blasts and two aircraft. CENTCOM issued no statement or video. Trump: a 'minor attack, it wasn't a war.' A US official called it 'part of ongoing operations': the US is 'occasionally striking Iranian missile launchers in self-defense' when the IRGC fires at US aircraft. WSJ described it as the latest in a series of limited strikes in recent weeks that were 'purposefully kept secret.' This is the first ACKNOWLEDGED US strike on Iranian territory since Sep 1. Coordinates approximate (island centroid; exact site not disclosed)."
}
```

```json
{
  "id": "us-strike-qeshm-suza-air-defense-20261106",
  "city": "Suza area, Qeshm Island, Hormozgan",
  "lat": 26.778,
  "lng": 56.064,
  "type": "us_strike",
  "actor": "US",
  "weapon": "Not disclosed (Tasnim / Iranian state TV: two missiles or projectiles; witnesses heard aircraft overhead)",
  "targets": ["Iranian air-defence system, Suza area (Trump: 'a little bit of an anti-aircraft device')"],
  "first_strike": "2026-11-06",
  "casualties_reported": "None reported",
  "casualties_source": "AP via KSAT / Washington Post (Nov 6); Al Jazeera (Nov 7); Tasnim via Iran International (Nov 6)",
  "active_days": [252],
  "notes": "Night of Fri Nov 6 local; Trump confirmed it early Sat Nov 7: 'we knocked it out in about 15 minutes, maybe five.' AP: the first US strike after the Nov 3 midterms. CENTCOM described the area as 'relatively calm' and gave no detail. Al Jazeera frames it as following attacks on vessels in Hormuz, within a weeks-long series against Iranian air defences and launchers. The specific trigger for Nov 6 is NOT confirmed; the general US framing is a response to IRGC fire at US aircraft. Iran's army (IRIB, announced early Nov 7) claimed it downed an MQ-9 over Qeshm with a 'new system' (UNVERIFIED). Coordinates approximate."
}
```

```json
{
  "id": "us-strike-mv-huda-gulf-of-oman-20261107",
  "city": "Gulf of Oman, ~18 nm east of Khor Fakkan (UAE)",
  "lat": 25.34,
  "lng": 56.69,
  "type": "us_strike",
  "actor": "US",
  "weapon": "US aircraft, precision munitions (CENTCOM)",
  "targets": ["M/V Huda (St Kitts & Nevis-flag bulk carrier, 1999, 24,993 dwt, Turkish-managed), stern/propulsion, after it left an Iranian port in violation of the blockade"],
  "first_strike": "2026-11-07",
  "casualties_reported": "None reported; crew told to 'abandon targeted spaces' before the strike",
  "casualties_source": "CENTCOM via Stars and Stripes / Maritime Executive (Nov 7)",
  "active_days": [253],
  "notes": "Blockade enforcement, not a strike on Iranian territory. The crew ignored repeated warnings. CENTCOM's Blockade 2.0 tally (Nov 7): 147 vessels redirected and 5 disabled since the blockade was reimposed in July; Huda is the 5th disabled (the 4th was M/V Ocean Molica, Oct 10). Maritime Executive: the first cargo ship disabled in about a month. A UAE National Guard rescue of 22 crew (Arab nationals) from a burning cargo ship in the Gulf of Oman on Nov 8 may be the same vessel; CBS says the link is unclear. Coordinates approximate."
}
```

#### 2b. MODIFICATIONS TO EXISTING ENTRIES

None. No existing strike entry continued in-window.

#### 2c. GLOBAL UPDATES (element `[0]`, the metadata object)

```
FIELD: last_updated
OLD VALUE: "2026-10-30"
NEW VALUE: "2026-11-11"
```

```
FIELD: last_strike_on_iran
OPERATION: PREPEND the text below, followed by a space and "PRIOR: ", to the existing value.
NEW TEXT: "2026-11-06 (US 'minor' strikes destroyed an Iranian air-defence system in the Suza area of Qeshm Island; no casualties reported; Trump confirmed Nov 6-7). Also 2026-11-07: US aircraft disabled M/V Huda, a St Kitts & Nevis-flag bulk carrier leaving an Iranian port, ~18 nm east of Khor Fakkan (blockade enforcement, not Iranian territory or an Iranian flag). Iran CLAIMS a further US projectile strike on Qeshm on the night of Nov 8 (Tasnim; Hormozgan deputy governor Ahmad Nafisi: no casualties, targets outside residential and commercial areas); the US has not confirmed it. PRIOR: 2026-11-02 (Qeshm Island: IRGC surface-to-air missile launcher struck by a US fighter in self-defense after an IRGC SAM was fired at it; first acknowledged US strike ashore since Sep 1)."
REASON: Two US strikes acknowledged by US officials / Trump (NBC, CBS, Stars and Stripes, AP, Al Jazeera); Huda per CENTCOM.
```

```
FIELD: last_iran_territory_strike
OPERATION: PREPEND the text below, followed by a space and "PRIOR: ", to the existing value.
NEW TEXT: "2026-11-06 (Suza area, Qeshm Island: air-defence system) PRIOR: 2026-11-02 (Qeshm Island: IRGC SAM launcher). Iran claims a Nov 8 night strike on Qeshm (unconfirmed). WSJ and NBC report smaller US strikes in the preceding weeks were 'purposefully kept secret' (unconfirmed reports: Sirik Oct 22, Jask Oct 29). The earlier 'no strikes on Iranian territory Oct 16-30' line should be read as 'none acknowledged'."
```

```
FIELD: phase
OPERATION: PREPEND the text below, followed by " PRIOR: ", to the existing value.
NEW TEXT: "LIMITED 'SELF-DEFENSE' STRIKES, EXPANDED BLOCKADE, NO RETURN TO MAJOR COMBAT (from Nov 2): the first acknowledged US strikes ashore since Sep 1 (Qeshm, Nov 2 and Nov 6) followed IRGC fire at US aircraft. The expected post-midterm 'short, intense campaign' did not materialize after Democrats won both chambers on Nov 3. Trump: new strikes 'highly unlikely' while talks continue (Nov 7-8); the war 'militarily, is effectively over' (Nov 9). Rubio (G7, Nov 10): 'no need for major combat operations.' Hegseth (Nov 10-11): operations would resume if needed. CENTCOM stood up Task Force Iron Gate (Nov 7) to extend the blockade to Iran's land-border and Caspian routes. The IRGC lifted its self-imposed missile-range limit (Nov 7). Maritime war continues: near-daily IRGC mine claims, confirmed projectile strikes on ships off Musandam, and an intensified Houthi campaign against Riyadh and Aramco."
```

```
FIELD: summary
OPERATION: PREPEND the text below, followed by " PRIOR — ", to the existing value.
NEW TEXT: "DAY 257 UPDATE (Oct 31-Nov 11): Two acknowledged US strikes on Iranian territory, both on Qeshm Island: Nov 2 (IRGC SAM launcher, after an IRGC surface-to-air missile was fired at a US fighter; US officials via NBC/CBS/WSJ) and Nov 6 (air-defence system, Suza area; Trump called it 'minor'). Neither had a CENTCOM statement and no casualties were reported. Iran claims a third US strike on Qeshm the night of Nov 8 (unconfirmed). WSJ: earlier smaller strikes were kept secret. No Israeli strike on Iran. Nov 7: US aircraft disabled the St Kitts & Nevis-flag bulk carrier M/V Huda leaving an Iranian port. Blockade 2.0 tally (CENTCOM, Nov 7): 147 redirected and 5 disabled since July. This tally is NOT merged into the war-cumulative centcom_* fields, which are HELD. IRGC/Army drone-shootdown claims (MQ-9, MQ-1, MQM-170, LUCAS; claimed running total 16 MQ-1 + 56 MQ-9) are UNVERIFIED. total_targets_struck HELD: there is no CENTCOM tally, and at most two individual targets are acknowledged. Post-midterm posture: Democrats won the House and Senate on Nov 3; the expected short, intense campaign did not begin. Trump said strikes are 'highly unlikely' while talks continue (Nov 7-8) and that the war is 'effectively over' militarily (Nov 9). Task Force Iron Gate (CENTCOM, Nov 7) targets Iran's land and Caspian trade routes. The Theodore Roosevelt CSG was in the Andaman Sea westbound on Nov 9 (USNI)."
```

```
FIELDS: centcom_blockade_redirected_cum (142), centcom_blockade_turnarounds_cum (52), centcom_tankers_disabled_cum (9)
OPERATION: NO CHANGE. These are war-cumulative fields, and the file's convention keeps them separate from the Blockade 2.0 tally (147 redirected / 5 disabled as of Nov 7, recorded in summary). Huda is a bulk carrier, not a tanker.
```

---

### 3. STRIKES-RETALIATION UPDATES

Confidence: **MEDIUM**. Saudi intercepts and damage are confirmed by Saudi authorities. Houthi claims of hits are mostly unverified. Hormuz ship strikes are confirmed by UKMTO / Ambrey / owners, but most attacks are unclaimed.

#### 3a. NEW ENTRIES

Append in this order. Field order follows the current last entry: `id, city, lat, lng, type, weapon, origin, first_strike, casualties_reported, casualties_source, active_days, notes, verified, last_updated`. Every `type` below already exists in the file.

```json
{
  "id": "irgc-sam-us-fighter-qeshm-2026-11-02",
  "city": "Strait of Hormuz / Qeshm Island, Hormozgan, Iran",
  "lat": 26.85,
  "lng": 55.9,
  "type": "iran_retaliation",
  "weapon": "Surface-to-air missile (IRGC); separately, a missile fired from Qeshm at commercial shipping",
  "origin": "Iran (IRGC), Qeshm Island",
  "first_strike": "2026-11-02",
  "casualties_reported": "None; the US fighter was not hit and the anti-ship missile was intercepted",
  "casualties_source": "Two US military officials via WSJ / CNN / CBS / NBC (Nov 2-3); CTP-ISW Iran Update (Nov 3)",
  "active_days": [248],
  "notes": "An IRGC surface-to-air missile was fired at a US fighter over the Strait of Hormuz, and the jet struck the launcher (see strikes-iran us-strike-qeshm-sam-launcher-20261102). The same day the US intercepted an IRGC missile fired from Qeshm at commercial shipping. A US official said the IRGC 'has routinely targeted and shot at US manned and unmanned aircraft' in recent weeks. IRGC/Army drone claims are UNVERIFIED and not logged separately: two MQM-170s 'grounded' and the '55th MQ-9' downed (Nov 2), an MQ-1 (Nov 4), two LUCAS drones seized by electronic warfare (Nov 5), two more MQM-170s (Nov 5), an MQ-1 (Nov 6), and an MQ-9 with a 'new system' (Nov 6-7). CENTCOM rejected a separate capture claim. Coordinates approximate.",
  "verified": true,
  "last_updated": "2026-11-11"
}
```

```json
{
  "id": "velos-sapphire-central-gulf-2026-11-05",
  "city": "Central Arabian Gulf, ~50 nm north of Madinat ash Shamal, Qatar",
  "lat": 26.96,
  "lng": 51.2,
  "type": "iran_retaliation",
  "weapon": "Two unidentified projectiles (suspected missile)",
  "origin": "Unclaimed; suspected Iran (attribution unconfirmed)",
  "first_strike": "2026-11-05",
  "casualties_reported": "1 seafarer killed; no other injuries (Velos Tankers)",
  "casualties_source": "UKMTO; Velos Tankers via Reuters / gCaptain / Baird Maritime / Maritime Executive (Nov 5-6)",
  "active_days": [251],
  "notes": "MT Velos Sapphire, a Marshall Islands-flag, Greek-managed products tanker sailing unladen to Bahrain, was hit at 23:13-23:20 UTC Nov 4 (about 02:20 local Nov 5). The fire was extinguished and the ship was taken to Khalifa Bin Salman Port, Bahrain. This is the deepest-in-Gulf attack of the window, far from Hormuz. The Philippine Department of Migrant Workers reports the victim as Filipino (PROVISIONAL, from search snippets; the Reuters text gives no nationality). Logged once despite the Nov 4 (UTC) / Nov 5 (local) dating. Coordinates approximate.",
  "verified": true,
  "last_updated": "2026-11-11"
}
```

```json
{
  "id": "hormuz-ship-attacks-2026-10-30-to-11-11",
  "city": "Strait of Hormuz approaches (Musandam: Khasab and Lima, Oman), UAE waters and Gulf of Oman",
  "lat": 26.2,
  "lng": 56.4,
  "type": "iran_retaliation",
  "weapon": "Unidentified projectiles and UAVs; naval mines claimed by Iran",
  "origin": "Mostly unclaimed; suspected Iran. The IRGC claims daily mine strikes; CENTCOM (Oct 30) says the mines Iran laid early in the war were cleared.",
  "first_strike": "2026-10-30",
  "casualties_reported": "1 Indian seafarer killed and 13 rescued from the dhow MSV Al Jusufi, struck off Oman on Nov 2 (India MEA; UKMTO). No casualties reported in the other logged incidents.",
  "casualties_source": "UKMTO / Ambrey / Nakilat / ADNOC via WAM / India MEA; via Middle East Eye, gCaptain, Maritime Executive, Riviera, Asharq Al-Awsat, Gulf News",
  "active_days": [245, 247, 248, 252, 253, 256, 257],
  "notes": "Confirmed incidents, all excluding Velos Sapphire (logged separately):\n- Oct 30 (evening): LNG carrier Al Mayeda (Nakilat) hit ~13 nm west of Al Jazirah Al Hamra, Ras al-Khaimah. Fire extinguished; all 25 crew safe.\n- Nov 1: unnamed vessel holed on the starboard side by a projectile off Lima, Oman.\n- Nov 2: Indian-crewed dhow MSV Al Jusufi struck off Oman during an outbound transit. 1 killed; 13 rescued by the Royal Navy of Oman.\n- Nov 6: unnamed tanker had an explosion at the waterline while leaving the strait. Crew safe.\n- Nov 7: two outbound tankers hit, ~15 nm north and ~8 nm northwest of Khasab. UKMTO 199-26 was reclassified as an attack; OSINT tentatively names Navig8 Messi (UNVERIFIED).\n- Nov 10: Barbados-flag tanker SEA 1 hit by a UAV ~19 nm northeast of Lima (UKMTO 201-26).\n- Nov 10: an ADNOC L&S vessel was damaged in UAE waters (ADNOC/WAM; the UAE called it a 'grave threat').\n- Nov 11: a merchant vessel was disabled by a projectile in its engine room ~7 nm northeast of Lima (Ambrey). It may be the Saudi-flag NCC Fajr (UKMTO 202-26 'suspicious activity'; 3 Indian crew safe).\nThe UKMTO weekly report (week to ~Nov 4-6) counts 11 ships attacked and 3 sunk (unnamed). Also reported but NOT counted pending dedupe: on Oct 30 the Panama-flag tanker RITI was targeted and set afire 1.6 NM off Musandam, and all 25 crew were evacuated by the Royal Navy of Oman (Oman MSC via Reuters / Oman Observer; same crew count as Al Mayeda, so possible conflation). UKMTO via CBS also reported a ship hit 40 NM south of Lavan Island (Oct 30) and a tanker hit by two projectiles 72 NM east of Ras al-Khafji (Nov 2). Iranian mine and 'halted' claims are UNVERIFIED and excluded: about 25-30 hulls claimed Oct 31-Nov 11, with heavy overlap. The 'four tankers on fire after mines' claim is dated Wed Nov 4. Coordinates are a regional centroid.",
  "verified": true,
  "last_updated": "2026-11-11"
}
```

```json
{
  "id": "riyadh-houthi-salvos-2026-11",
  "city": "Riyadh, Saudi Arabia (incl. King Abdullah Financial District)",
  "lat": 24.7646,
  "lng": 46.6412,
  "type": "iran_retaliation",
  "weapon": "Ballistic missiles, cruise missiles and drones",
  "origin": "Houthis (Ansar Allah), Iran-aligned",
  "first_strike": "2026-11-02",
  "casualties_reported": "None reported. Intercept shrapnel caused minor damage to a Saudi Aramco administrative tower in KAFD on Nov 8.",
  "casualties_source": "Saudi Joint Forces Command (Maj. Gen. al-Maliki) via Anadolu / ABC News / Gulf News / Reuters; Saudi Energy Ministry (KAFD damage)",
  "active_days": [248, 253, 254, 256, 257],
  "notes": "Confirmed intercepts:\n- Nov 2: two drones over Riyadh Province, plus a ballistic missile over southern Saudi Arabia.\n- Nov 7: a missile toward Riyadh Province and a ballistic missile toward the Eastern Region.\n- Nov 8: 3 ballistic missiles, 2 cruise missiles and 1 drone, including 2 ballistic and 2 cruise missiles at Riyadh. Falling shrapnel caused 'minor damage' to an Aramco administrative tower in King Abdullah Financial District, with no casualties (Saudi Energy Ministry). A Reuters witness saw blown-out windows across several floors. Houthi spokesman Saree claimed the attack.\n- Nov 10: a ballistic missile at Riyadh was intercepted; explosions were heard.\n- Nov 11: 3 cruise missiles toward Riyadh were intercepted (Reuters).\nUNVERIFIED Houthi claims, not logged as separate entries: King Khalid International Airport 'extensive damage' (Nov 4), Aramco storage tanks and Abqaiq (Nov 8), and 'several pumping stations' near Riyadh (Nov 10). Coordinates: KAFD.",
  "verified": true,
  "last_updated": "2026-11-11"
}
```

```json
{
  "id": "najran-bm-intercept-2026-11-06",
  "city": "Najran, Najran Province, Saudi Arabia",
  "lat": 17.4924,
  "lng": 44.1277,
  "type": "drone_attack_intercepted",
  "weapon": "Two ballistic missiles (intercepted)",
  "origin": "Houthis (Ansar Allah), Iran-aligned",
  "first_strike": "2026-11-06",
  "casualties_reported": "None reported; debris fell and a damage assessment was under way",
  "casualties_source": "Saudi-led coalition via CBS News; CTP-ISW Iran Update (Nov 6)",
  "active_days": [252],
  "notes": "Two Houthi ballistic missiles were intercepted near Najran, with debris falling and civil-defence alerts. Damage to Najran airport facilities is NOT confirmed, so the airports count is unchanged.",
  "verified": true,
  "last_updated": "2026-11-11"
}
```

```json
{
  "id": "east-west-pipeline-medina-2026-11-09",
  "city": "East-West (Petroline) pipeline, Medina region, Saudi Arabia",
  "lat": 24.5,
  "lng": 39.6,
  "type": "iran_retaliation",
  "weapon": "Not specified",
  "origin": "Unattributed: the Saudi Energy Ministry named no perpetrator; occurred amid the Houthi campaign on Saudi energy",
  "first_strike": "2026-11-09",
  "casualties_reported": "None",
  "casualties_source": "Saudi Energy Ministry via Saudi Press Agency / AFP / Gulf News / Okaz (Nov 9)",
  "active_days": [255],
  "notes": "An energy ministry official said the pipeline was 'targeted' and a 'limited fire' broke out. It was extinguished, with no casualties and no disruption to operations. Cause under investigation. This follows the Oct 4 Khurais pumping-station hit (khurais-east-west-pipeline-pumping-station) and the September drone strike on the line. Exact location NOT published; coordinates are the Medina-region centroid.",
  "verified": true,
  "last_updated": "2026-11-11"
}
```

```json
{
  "id": "qatabah-dhale-camp-2026-11-04",
  "city": "Qatabah District, Al Dhale Governorate, Yemen",
  "lat": 13.86,
  "lng": 44.7,
  "type": "houthi_attack",
  "weapon": "Ballistic missile",
  "origin": "Houthis (Ansar Allah), Iran-aligned",
  "first_strike": "2026-11-04",
  "casualties_reported": "At least 11 government soldiers killed and at least 60 wounded",
  "casualties_source": "Yemeni media and journalists via CTP-ISW Iran Update (Nov 4)",
  "active_days": [250],
  "notes": "A Houthi ballistic missile hit a Yemeni government military camp. Casualty figures come from Yemeni media and were not independently verified. Wider Yemen front in-window: government forces took Jabal Huwayshiyan near al-Hazm (Oct 31). Houthis took Souq al-Roubah (Nov 1) and Jabal Irf (Nov 2); government forces retook Jabal Irf (Nov 3) and gained ground at Jabal Dahida, al-Jawf (Nov 2-6), with Saudi Apache and air support. Coordinates approximate.",
  "verified": false,
  "last_updated": "2026-11-11"
}
```

```json
{
  "id": "khor-mor-gas-field-2026-11-08",
  "city": "Khor Mor gas field, Chamchamal, Kurdistan Region, Iraq",
  "lat": 35.06,
  "lng": 44.74,
  "type": "non_state_actor_kinetic",
  "weapon": "Suspected drone",
  "origin": "Unclaimed. A security source told Rudaw it was launched from east of Tuz Khurmatu. A Nov 7 statement by Kataib Hezbollah security chief Abu Mujahid al-Assaf hinted at grievances against the UAE; operator Dana Gas is UAE-based.",
  "first_strike": "2026-11-08",
  "casualties_reported": "None",
  "casualties_source": "Dana Gas; Iraqi prime minister's office; KRG Electricity Ministry; via Long War Journal / Jerusalem Post (Nov 9)",
  "active_days": [254],
  "notes": "At 23:10 local on Sun Nov 8, a suspected drone hit the LPG storage and truck-loading unit. The fire was extinguished. Production was suspended, and about 2,800 MW of generation in the Kurdistan Region was lost (KRG Electricity Ministry). US envoy Tom Barrack condemned the attack. Attribution is UNVERIFIED. No militia attacks on US forces or Kuwait were found in-window. Coordinates approximate.",
  "verified": true,
  "last_updated": "2026-11-11"
}
```

```json
{
  "id": "south-lebanon-israeli-strikes-2026-11",
  "city": "Qabrikha (Marjayoun) and villages across southern Lebanon",
  "lat": 33.24,
  "lng": 35.49,
  "type": "israel_kinetic_lebanon",
  "weapon": "Israeli drone and air strikes; artillery",
  "origin": "Israel (IDF)",
  "first_strike": "2026-11-04",
  "casualties_reported": "1 killed (Muhammad Nasser Yousef, a paramedic with the Amal-affiliated Risala Scouts) and 1 wounded at Qabrikha, Nov 4. Olive harvesters injured Nov 9 (number not reported).",
  "casualties_source": "Lebanese Health Ministry via Times of Israel (Nov 5); CFR Global Conflict Tracker; Janoubia via APA (Nov 9)",
  "active_days": [250, 252, 253, 255, 256],
  "notes": "Times of Israel calls the Nov 4 drone strike at Qabrikha 'the first Israeli airstrike in southern Lebanon in weeks.' CFR reports the same Nov 4 event as an airstrike on a motorcycle.\n- Nov 4: shelling of al-Mansouri and Wadi Zibqin.\n- Nov 6: airstrike on Bint Jbeil.\n- Nov 7: detonation and shelling in Bani Hayyan; shelling of Zawtar al-Sharqiyah.\n- Nov 9: airstrikes on Kfar Tibnit, Mayfadun, Markaba, Tallousa and al-Qantara; drone strikes on Deir Mimas and al-Jarmaq; artillery on Majdal Zoun, Haddatha, Haris and al-Majadel.\n- Nov 10: airstrike on Qantara; artillery near al-Mansouri and Majdal Zoun.\nNo Hezbollah attacks were reported (CTP-ISW; CFR). Israel-Lebanon talks remain stalled over Hezbollah disarmament. Do NOT confuse with a Nov 5, 2023 Aynata car strike that resurfaces in searches. Coordinates: Qabrikha, approximate.",
  "verified": true,
  "last_updated": "2026-11-11"
}
```

#### 3b. MODIFICATIONS TO EXISTING ENTRIES

```
ENTRY ID: mecca-drone-claim-2026-10-30
FIELD: active_days
OLD VALUE: [245]
NEW VALUE: [245, 249, 252, 257]
REASON: Saudi JFC reported further drones intercepted over the Mecca region on Nov 3 and Nov 6, and two drones toward Mecca and the south on Nov 11. The Houthis again denied targeting Mecca (Reuters, Nov 11; CTP-ISW Nov 3 / Nov 6).

ENTRY ID: mecca-drone-claim-2026-10-30
FIELD: notes
OPERATION: APPEND " Nov 3: Saudi JFC (al-Maliki) said one drone was intercepted over Mecca Province. Nov 6: a drone was intercepted in the Mecca region (CTP-ISW). Nov 11: the coalition said two drones toward Mecca and the south were intercepted, with Civil Defence alerts in Taif, Yanbu and Khamis Mushait; the Houthis denied targeting Mecca (Reuters). Still DISPUTED."

ENTRY ID: mecca-drone-claim-2026-10-30
FIELD: last_updated
OLD VALUE: "2026-10-30"
NEW VALUE: "2026-11-11"

ENTRY ID: medina-2026-10-01
FIELD: active_days
OLD VALUE: [216, 230]
NEW VALUE: [216, 230, 251]
REASON: The coalition said it intercepted a ballistic missile aimed at the Medina region on Nov 5; the Houthis denied targeting Medina (CTP-ISW; CBS live blog).

ENTRY ID: medina-2026-10-01
FIELD: notes
OPERATION: APPEND " Nov 5: the coalition said it intercepted a ballistic missile aimed at the Medina region; the Houthis denied targeting Medina (DISPUTED). The Nov 9 East-West pipeline fire in the Medina region is logged separately (east-west-pipeline-medina-2026-11-09)."

ENTRY ID: medina-2026-10-01
FIELD: last_updated
OLD VALUE: "2026-10-15"
NEW VALUE: "2026-11-11"
```

#### 3c. GLOBAL

The file has no file-level metadata object. Each new or modified entry carries `"last_updated": "2026-11-11"`.

---

### 4. CARRIERS UPDATES

Confidence: **HIGH** for sea areas and escort listings. The full text of the USNI Fleet & Marine Tracker editions for Oct 26, Nov 2 and Nov 9, 2026 was read, and key lines were spot-checked against the saved text. **MEDIUM** for coordinates: USNI publishes sea areas only, so every new lat/lng below is an approximation and is labelled as such.

Source keys used below:
- **USNI-Nov9:** https://news.usni.org/2026/11/09/usni-news-fleet-and-marine-tracker-nov-9-2026
- **USNI-Nov2:** https://news.usni.org/2026/11/02/usni-news-fleet-and-marine-tracker-nov-2-2026
- **USNI-TR (Nov 6):** https://news.usni.org/2026/11/06/theodore-roosevelt-carrier-strike-group-pulls-into-singapore
- **USNI-Dragon (Oct 12):** https://news.usni.org/?p=125877
- **TWZ (Nov 6):** https://www.twz.com/sea/uss-theodore-roosevelt-arrives-in-singapore-last-stop-before-third-strike-group-reaches-the-middle-east
- **MarEx (Nov 9):** https://maritime-executive.com/article/uss-theodore-roosevelt-csg-leaves-singapore-bound-for-the-gulf
- **Stripes (Nov 9):** https://www.stripes.com/theaters/middle_east/2026-11-09/iran-trump-strikes-diplomacy-war-23410322.html

**Headline:** No carrier has left CENTCOM. George Washington and George H.W. Bush remain in the Arabian Sea. Theodore Roosevelt is in the Andaman Sea, westbound, and is NOT yet in CENTCOM. The Boxer ARG has moved east to the vicinity of the Laccadive Sea; no departure from theater has been announced. The Makin Island ARG is in the Sea of Japan. One escort moved: USS Ross (DDG-71) now appears under George Washington's DESRON 15 instead of Bush's DESRON 22.

For every `notes` change below, PREPEND the new text plus " PRIOR — " to the existing value (file convention).

#### 4a. POSITION/STATUS CHANGES

```
SHIP: USS George Washington (CVN-73)
FIELD: escorts
OLD VALUE: ["DDG-86 USS Shoup"]
NEW VALUE: ["DDG-86 USS Shoup", "DDG-71 USS Ross"]
SOURCE: USNI-Nov2; USNI-Nov9 (Destroyer Squadron 15 lists Shoup and Ross)
VERIFIED: 2026-11-09

FIELD: area
OLD VALUE: "Arabian Sea / 5th Fleet AOR — supporting US operations against Iran with CVW-5 and USS Shoup (DDG-86) (USNI Oct 13). Lat/lng remain a PLACEHOLDER pending a USNI positional fix."
NEW VALUE: "Arabian Sea / 5th Fleet AOR — supporting US operations in the Middle East with CVW-5; USNI Nov 9 lists Destroyer Squadron 15 as USS Shoup (DDG-86) and USS Ross (DDG-71). Lat/lng remain a PLACEHOLDER pending a USNI positional fix."

FIELD: status
OLD VALUE: "DAY 245 (OCT 26, USNI): ARABIAN SEA, ENFORCING THE BLOCKADE OF IRANIAN PORTS; DVIDS FLIGHT OPERATIONS OCT 24; AIS DARK (TWZ OCT 27). TO BE RELIEVED BY THEODORE ROOSEVELT."
NEW VALUE: "DAY 257 (NOV 9, USNI): ARABIAN SEA WITH CVW-5; DESRON 15 = SHOUP + ROSS; REPLENISHED AT SEA WITH USNS WALLY SCHIRRA (T-AKE-8) NOV 7; AIS DARK. STILL AWAITING RELIEF BY THEODORE ROOSEVELT (EXPECTED NO EARLIER THAN MID-NOVEMBER)."

FIELD: notes (PREPEND)
NEW TEXT: "Day 257 (November 11): USNI's Nov 2 and Nov 9 trackers keep George Washington in the Arabian Sea with CVW-5. Destroyer Squadron 15 now lists USS Ross (DDG-71) alongside Shoup. Ross was previously listed under Bush's DESRON 22; the reassignment rests on the USNI listing only, with no Navy announcement. USNI's lead sentence still reads 'CVW 5 and USS Shoup.' Navy imagery shows a replenishment-at-sea with USNS Wally Schirra on Nov 7. USNI (Nov 6) reports Theodore Roosevelt is expected to relieve George Washington; TR was in the Andaman Sea on Nov 9. The US strikes on Qeshm Island (Nov 2, Nov 6) and the disabling of M/V Huda (Nov 7) were not attributed to a named platform. USS Benfold (DDG-65) returned to Everett on Oct 16 (USNI)."

FIELD: independently_deployed_destroyers
OLD VALUE: ["DDG-119 USS Delbert D. Black (CENTCOM)", "DDG-69 USS Milius (CENTCOM)", "DDG-87 USS Mason (CENTCOM)", "DDG-76 USS Higgins (CENTCOM)", "DDG-53 USS John Paul Jones (CENTCOM)", "DDG-115 USS Rafael Peralta (CENTCOM)", "DDG-112 USS Michael Murphy (CENTCOM)", "ESB-5 USS Miguel Keith (CENTCOM)", "DDG-79 USS Oscar Austin (Red Sea)", "DDG-109 USS Jason Dunham (Red Sea)", "DDG-89 USS Mustin (Indian Ocean)", "DDG-111 USS Spruance (Indian Ocean)", "CG-59 USS Princeton (Indian Ocean)", "DDG-113 USS John Finn (Indian Ocean)", "DDG-51 USS Arleigh Burke (E. Mediterranean)", "DDG-80 USS Roosevelt (E. Mediterranean)", "DDG-84 USS Bulkeley (E. Mediterranean)", "DDG-66 USS Gonzalez (E. Mediterranean)"]
NEW VALUE: ["DDG-119 USS Delbert D. Black (CENTCOM)", "DDG-69 USS Milius (CENTCOM)", "DDG-87 USS Mason (CENTCOM)", "DDG-53 USS John Paul Jones (CENTCOM)", "DDG-115 USS Rafael Peralta (CENTCOM)", "DDG-113 USS John Finn (CENTCOM)", "DDG-120 USS Carl M. Levin (CENTCOM)", "DDG-108 USS Wayne E. Meyer (CENTCOM)", "CG-59 USS Princeton (CENTCOM)", "ESB-5 USS Miguel Keith (CENTCOM)", "DDG-89 USS Mustin (Indian Ocean)", "DDG-109 USS Jason Dunham (Red Sea)", "DDG-66 USS Gonzalez (Red Sea)", "DDG-79 USS Oscar Austin (Mediterranean)", "DDG-84 USS Bulkeley (Mediterranean)", "DDG-117 USS Paul Ignatius (Mediterranean)", "DDG-55 USS Stout (Mediterranean)"]
SOURCE: USNI-Nov9, cross-checked against USNI Oct 26 and Nov 2.
  Removed since Oct 26: Higgins (DDG-76).
  Removed as corrections (absent from all three editions): Michael Murphy (DDG-112), Spruance (DDG-111), Arleigh Burke (DDG-51), Roosevelt (DDG-80).
  Region corrections: Oscar Austin → Mediterranean (left Koper Oct 27); Gonzalez → Red Sea; Princeton and John Finn → CENTCOM region list.
  Added: Wayne E. Meyer; Carl M. Levin; Stout (Mediterranean since at least Oct 26); Paul Ignatius (new to the Mediterranean, Nov 9).
VERIFIED: 2026-11-09

FIELD: source
OPERATION: PREPEND "USNI Fleet & Marine Tracker (Nov 2, Nov 9, 2026); USNI News (Nov 6); "

FIELD: last_verified
OLD VALUE: "2026-10-26"
NEW VALUE: "2026-11-09"
```

```
SHIP: USS George H.W. Bush (CVN-77)
FIELD: escorts
OLD VALUE: ["DDG-75 USS Donald Cook", "DDG-71 USS Ross"]
NEW VALUE: ["DDG-75 USS Donald Cook"]
SOURCE: USNI-Nov2; USNI-Nov9 (Destroyer Squadron 22, embarked on Bush, lists Donald Cook only)
VERIFIED: 2026-11-09

FIELD: area
OLD VALUE: "Arabian Sea / 5th Fleet AOR — CSG-10 with Carrier Air Wing 7 (CVW-7) and DESRON 22 (USS Donald Cook DDG-75, USS Ross DDG-71); back in the Arabian Sea after a po…" (full current value)
NEW VALUE: "Arabian Sea / 5th Fleet AOR — CSG-10 with Carrier Air Wing 7 (CVW-7) and DESRON 22 (USS Donald Cook DDG-75) per USNI Nov 2 and Nov 9. Lat/lng approximate."

FIELD: status
OLD VALUE: "DAY 245 (OCT 26, USNI): ARABIAN SEA; 210 DAYS INTO DEPLOYMENT; AIS DARK (TWZ OCT 27). CSG-10 WITH CVW-7 AND DESRON 22."
NEW VALUE: "DAY 257 (NOV 9, USNI): ARABIAN SEA; ~224 DAYS INTO DEPLOYMENT ON NOV 9 (210 ON OCT 26); NOT RELIEVED; NO RETURN DATE ANNOUNCED. CSG-10 WITH CVW-7 AND DESRON 22 (DONALD COOK)."

FIELD: notes (PREPEND)
NEW TEXT: "Day 257 (November 11): USNI's Nov 2 and Nov 9 trackers keep Bush in the Arabian Sea. DESRON 22 now lists only USS Donald Cook; Ross appears under George Washington's DESRON 15. A Navy photo shows Donald Cook and USS Wayne E. Meyer (DDG-108) passing on Nov 5. The relief question is unresolved: USNI (Nov 6) and TWZ say Theodore Roosevelt relieves George Washington, while Maritime Executive (Nov 9) implies Bush stays on the line for a brief three-carrier overlap. Stars and Stripes (Nov 9): at least 15 other US warships in the region besides the two carriers; about 50,000 US forces."

FIELD: last_verified
OLD VALUE: "2026-10-26"
NEW VALUE: "2026-11-09"
```

```
SHIP: USS Theodore Roosevelt (CVN-71)
FIELD: lat / lng
OLD VALUE: 20.0 / 132.0
NEW VALUE: 7.0 / 95.5  (APPROXIMATE: USNI-Nov9 says only "operating in the Andaman Sea")
SOURCE: USNI-Nov9; USNI-TR; TWZ; MarEx
VERIFIED: 2026-11-09

FIELD: area
OLD VALUE: "Philippine Sea — Exercise Keen Sword 27 (ran through Oct 29), after a Yokosuka port call Oct 16-19 … Reportedly Middle Ea…" (full current value)
NEW VALUE: "Andaman Sea / eastern Indian Ocean (USNI Nov 9), westbound for the Middle East after a Singapore port visit (Changi Naval Base; arrived Fri Nov 6, departed Nov 8-9). AIS switched off after the Malacca Strait transit (Maritime Executive). NOT yet in the CENTCOM AOR — a US official told Axios it would not arrive before mid-November (via TWZ Nov 6). Lat/lng APPROXIMATE."

FIELD: status
OLD VALUE: "DAY 245 (OCT 26, USNI): PHILIPPINE SEA, KEEN SWORD 27; REPORTEDLY DEPLOYING TO CENTCOM AS THE THIRD CARRIER (NOT CONFIRMED BY USNI)."
NEW VALUE: "DAY 257 (NOV 9, USNI): ANDAMAN SEA, WESTBOUND TO THE MIDDLE EAST AFTER THE SINGAPORE PORT VISIT; EXPECTED TO RELIEVE GEORGE WASHINGTON (USNI NOV 6). NOT YET IN CENTCOM."

FIELD: escorts
OLD VALUE: ["CG-65 USS Chosin", "DDG-60 USS Paul Hamilton", "DDG-73 USS Decatur", "DDG-120 USS Carl M. Levin", "MUSV Seahawk"]
NEW VALUE: ["CG-65 USS Chosin", "DDG-60 USS Paul Hamilton", "DDG-73 USS Decatur", "MUSV Seahawk"]
REASON: USNI's Destroyer Squadron 23 lists Paul Hamilton and Decatur only. Carl M. Levin appears separately among destroyers deployed in the CENTCOM region.

FIELD: notes (PREPEND)
NEW TEXT: "Day 257 (November 11):
- Crossed the South China Sea (USNI Nov 2) and replenished at sea with HMAS Stalwart on Nov 4.
- Singapore port visit Nov 6 to Nov 8-9 (USNI Nov 6; TWZ). Paul Hamilton docked with the carrier; Decatur docked at Sembawang.
- Andaman Sea, westbound, on Nov 9 (USNI).
- CENTCOM arrival not official: 'not before mid-November' (Axios via TWZ); Maritime Executive estimates the north Arabian Sea by about Nov 16; an earlier WSJ report said by end-November.
- Carl M. Levin removed from the escort list per USNI's group listing."

FIELD: last_verified
OLD VALUE: "2026-10-26"
NEW VALUE: "2026-11-09"
```

```
SHIP: USS Boxer (LHD-4)
FIELD: lat / lng
OLD VALUE: 19.0 / 60.5
NEW VALUE: 10.0 / 74.0  (APPROXIMATE: USNI-Nov9 says "Indian Ocean in the vicinity of the Laccadive Sea")
SOURCE: USNI-Nov9; USNI-Nov2
VERIFIED: 2026-11-09

FIELD: area
OLD VALUE: "Arabian Sea — Boxer Amphibious Ready Group (Boxer, Comstock LSD-45, Portland LPD-27) with 11th MEU embarked (USNI Sep 28)"
NEW VALUE: "Indian Ocean, vicinity of the Laccadive Sea (USNI Nov 9) — moved east from the Arabian Sea (Oct 26) via the Indian Ocean (Nov 2). Boxer ARG (Boxer, Comstock LSD-45, Portland LPD-27) with 11th MEU embarked. Departure from CENTCOM NOT ANNOUNCED. Lat/lng APPROXIMATE."

FIELD: status
OLD VALUE: "DAY 245 (OCT 26, USNI): BOXER ARG (BOXER, COMSTOCK LSD-45, PORTLAND LPD-27) WITH 11TH MEU; ON STATION IN CENTCOM (TWZ OCT 27). Exact position not published."
NEW VALUE: "DAY 257 (NOV 9, USNI): INDIAN OCEAN NEAR THE LACCADIVE SEA, MOVING EAST AWAY FROM THE ARABIAN SEA; NO ANNOUNCEMENT THAT IT HAS LEFT CENTCOM; RELIEF ARG (MAKIN ISLAND) STILL IN THE SEA OF JAPAN."

FIELD: notes (PREPEND)
NEW TEXT: "Day 257 (November 11): USNI tracked the Boxer ARG from the Arabian Sea (Oct 26) to the Indian Ocean (Nov 2) and to the vicinity of the Laccadive Sea, off southwest India (Nov 9). That area is generally outside the CENTCOM AOR. TWZ (Nov 6) describes the ARG as about 235 days deployed and 'due for relief.' WATCH ITEM: if Boxer has left theater, CENTCOM has no ARG on station. Not removed pending confirmation."

FIELD: last_verified
OLD VALUE: "2026-10-26"
NEW VALUE: "2026-11-09"
```

```
SHIP: USS Makin Island (LHD-8)  [id: lha-makin-island]
FIELD: lat / lng
OLD VALUE: 35.29 / 139.67
NEW VALUE: 38.5 / 134.5  (APPROXIMATE: USNI-Nov9 says "now operating in the Sea of Japan")
SOURCE: USNI-Nov9
VERIFIED: 2026-11-09

FIELD: area
OLD VALUE: "Yokosuka, Japan — in port since Oct 26 with the 13th MEU, reportedly for a maintenance availability … Reportedly Middle East-bound (two …" (full current value)
NEW VALUE: "Sea of Japan (USNI Nov 9) — left Yokosuka Sat Nov 7 after a port visit that began Oct 26. ARG: Makin Island, USS Anchorage (LPD-23), USS John P. Murtha (LPD-26), 13th MEU. Still in 7th Fleet; the reported Middle East destination is UNCONFIRMED. Lat/lng APPROXIMATE."

FIELD: status
OLD VALUE: "IN PORT YOKOSUKA (OCT 26); ARG: MAKIN ISLAND, USS ANCHORAGE (LPD-23), USS JOHN P. MURTHA (LPD-26), 13TH MEU; REPORTEDLY MIDDLE EAST-BOUND."
NEW VALUE: "DAY 257 (NOV 9, USNI): SEA OF JAPAN AFTER LEAVING YOKOSUKA NOV 7; REPORTEDLY MIDDLE EAST-BOUND (NOT CONFIRMED); NOT IN THEATER."

FIELD: last_verified
OLD VALUE: "2026-10-26"
NEW VALUE: "2026-11-09"
```

```
SHIP: USS Dwight D. Eisenhower (CVN-69)
FIELD: status
OLD VALUE: "LEFT NORFOLK FOR WORKUPS OCT 24 (TWZ). NOT DEPLOYED."
NEW VALUE: "IN PORT NORFOLK — RETURNED OCT 30 (USNI NOV 2); ONE-DAY UNDERWAY NOV 4-5 (USNI NOV 9). NOT DEPLOYED."
SOURCE: USNI-Nov2; USNI-Nov9 ("departed Wednesday and returned Thursday to Norfolk")

FIELD: last_verified
OLD VALUE: "2026-10-27"
NEW VALUE: "2026-11-09"
```

```
SHIP: USS Carl M. Levin (DDG-120)
FIELD: strike_group
OLD VALUE: "Theodore Roosevelt CSG (CSG-9) — disaggregated, operating ahead of the group"
NEW VALUE: "Independently deployed — CENTCOM (USNI region list; a Navy official told TWZ on Oct 27 it belongs to the TR CSG)"

FIELD: area
OLD VALUE: "CENTCOM AOR (exact position not published; DVIDS imagery of flight operations in the AOR)"
NEW VALUE: "Middle East / 5th Fleet region (USNI Oct 26, Nov 2, Nov 9 — listed among destroyers deployed in the region); exact position not published"

FIELD: status
OLD VALUE: "OPERATING IN CENTCOM AOR (TWZ OCT 27, citing DVIDS) — FIRST TR CSG UNIT IN THEATER"
NEW VALUE: "IN CENTCOM REGION (USNI NOV 9)"

FIELD: source
OPERATION: PREPEND "USNI Fleet & Marine Tracker (Nov 2, Nov 9, 2026); "

FIELD: last_verified
OLD VALUE: "2026-10-27"
NEW VALUE: "2026-11-09"
SOURCE: USNI-Nov9
```

```
SHIP: USS John Finn (DDG-113)
FIELD: strike_group
OLD VALUE: "CSG-3 (independently deployed)"
NEW VALUE: "Independently deployed"

FIELD: area
OLD VALUE: "Indian Ocean (USNI Sep 28) — previously Arabian Sea with the CSG-3 destroyer screen"
NEW VALUE: "Middle East / 5th Fleet region (USNI Oct 26, Nov 2, Nov 9 region list); exact position not published"

FIELD: status
OLD VALUE: "DAY 216 (SEP 28, USNI): INDIAN OCEAN, WITH MUSTIN (DDG-89), SPRUANCE (DDG-111) AND PRINCETON (CG-59)."
NEW VALUE: "IN CENTCOM REGION (USNI NOV 9)"

FIELD: last_verified
OLD VALUE: "2026-09-28"
NEW VALUE: "2026-11-09"
SOURCE: USNI-Nov9
```

```
SHIP: USS Rafael Peralta (DDG-115)
FIELD: source
OPERATION: PREPEND "USNI Fleet & Marine Tracker (Nov 2, Nov 9, 2026); "

FIELD: last_verified
OLD VALUE: "2026-10-17"
NEW VALUE: "2026-11-09"
SOURCE: USNI-Nov9 (listed in the CENTCOM region)
```

```
SHIP: USS Gonzalez (DDG-66)
FIELD: area
OLD VALUE: "Red Sea (USNI Oct 13) — with USS Jason Dunham (DDG-109); Mediterranean now covered by USS Roosevelt (DDG-80) and USS Oscar Austin (DDG-79). Lat/lng approximate."
NEW VALUE: "Red Sea (USNI Nov 9) — with USS Jason Dunham (DDG-109); Mediterranean covered by USS Oscar Austin (DDG-79), USS Bulkeley (DDG-84), USS Paul Ignatius (DDG-117) and USS Stout (DDG-55). Lat/lng approximate."

FIELD: status
OLD VALUE: "DAY 230 (OCT 13, USNI): RED SEA, WITH USS JASON DUNHAM (DDG-109)."
NEW VALUE: "DAY 257 (NOV 9, USNI): RED SEA, WITH USS JASON DUNHAM (DDG-109)."

FIELD: last_verified
OLD VALUE: "2026-10-13"
NEW VALUE: "2026-11-09"
SOURCE: USNI-Nov9
```

```
SHIP: USS Tripoli (LHA-7)
FIELD: area
OLD VALUE: "Sasebo, Japan (in port, USNI Oct 13) — departed CENTCOM theater July 2026; NOT IN THEATER."
NEW VALUE: "Sasebo, Japan (in port, USNI Nov 9) — departed CENTCOM theater July 2026; NOT IN THEATER."

FIELD: status
OLD VALUE: "NOT IN THEATER — IN PORT AT SASEBO, JAPAN (USNI OCT 13). Departed CENTCOM in July; arrived White Beach, Okinawa, July 22 and offloaded the 31st MEU."
NEW VALUE: "NOT IN THEATER — IN PORT AT SASEBO, JAPAN (USNI NOV 9). Departed CENTCOM in July; arrived White Beach, Okinawa, July 22 and offloaded the 31st MEU."

FIELD: escorts
OLD VALUE: ["LPD-18 USS New Orleans", "LSD-47 USS Rushmore", "DDG-115 USS Rafael Peralta"]
NEW VALUE: ["LPD-18 USS New Orleans", "LSD-47 USS Rushmore"]
REASON: Rafael Peralta is deployed in the CENTCOM region (USNI-Nov9; carriers.json ddg-115), so it is no longer a Tripoli ARG escort.

FIELD: last_verified
OLD VALUE: "2026-10-19"
NEW VALUE: "2026-11-09"
SOURCE: USNI-Nov9 ("USS Tripoli (LHA-7) is in port in Sasebo, Japan.")
```

```
SHIP: USS Carl Vinson (CVN-70)
FIELD: last_verified
OLD VALUE: "2026-10-27"
NEW VALUE: "2026-11-06"
SOURCE: TWZ (Nov 6): still pierside in San Diego. No other change.
```

#### 4b. NEW ASSETS

Append to the end of the array. Field order follows the ddg-115 entry.

```json
{
  "id": "ddg-108",
  "name": "USS Wayne E. Meyer",
  "hull": "DDG-108",
  "type": "destroyer",
  "strike_group": "Independently deployed",
  "lat": 21.5,
  "lng": 61.5,
  "area": "Middle East / 5th Fleet region (USNI Oct 26, Nov 2, Nov 9 region list); exact position not published. Lat/lng PLACEHOLDER.",
  "aircraft": null,
  "escorts": [],
  "status": "IN CENTCOM REGION (USNI NOV 9)",
  "mission_summary": "Arleigh Burke-class guided-missile destroyer (homeported at Pearl Harbor) deployed in the region in support of US operations in the Middle East.",
  "deployed_since": null,
  "operation_start_date": null,
  "notes": "Listed by USNI among warships deployed in the region since at least Oct 26; a Navy photo shows it passing USS Donald Cook on Nov 5. Not previously in carriers.json.",
  "source": "USNI News Fleet & Marine Tracker (Oct 26, Nov 2, Nov 9, 2026)",
  "last_verified": "2026-11-09",
  "position_confidence": "LOW — placeholder"
}
```

Task Force Iron Gate (CENTCOM, Nov 7) is **not** added here: it is a coordination cell of about 20 staff in Tampa with no ships. It is logged in timeline-events instead.

#### 4c. ESCORT COMPOSITION CHANGES

| Strike group | Oct 26 | Nov 2 and Nov 9 (USNI) |
|---|---|---|
| CSG-5 George Washington (DESRON 15) | Shoup | Shoup, **Ross** |
| CSG-10 George H.W. Bush (DESRON 22) | Donald Cook, Ross | Donald Cook |
| CSG-9 Theodore Roosevelt (DESRON 23) | Chosin (air defense commander); Paul Hamilton, Decatur; MUSV Seahawk; Levin carried in the file | Chosin; Paul Hamilton, Decatur; MUSV Seahawk. Levin is listed separately in the CENTCOM region. |
| Boxer ARG | Comstock, Portland, 11th MEU | Unchanged |
| Makin Island ARG | Anchorage, Murtha, 13th MEU | Unchanged (Anchorage and Murtha took part in Malabar 2026, Nov 5-12, per USNI Western Pacific Pulse) |

#### 4d. REMOVALS

No US carrier or ARG has confirmed leaving CENTCOM. Boxer is the watch item (see 4a). Following file precedent (e.g., cvn-72 "RETURNED HOME"), the entries below are updated in place rather than deleted.

```
SHIP: HMS Dragon (D35)
FIELD: lat / lng
OLD VALUE: 34.7 / 33.0
NEW VALUE: 50.8 / -1.11

FIELD: area
OLD VALUE: "Eastern Mediterranean / Cyprus"
NEW VALUE: "HMNB Portsmouth, UK (home port) — returned Oct 9 after a seven-month deployment to the Mediterranean, Red Sea and Indian Ocean. NOT IN THEATER."

FIELD: status
OLD VALUE: "DEPLOYED — REDIRECTING TO MIDDLE EAST (per UK MoD May 9 announcement)"
NEW VALUE: "RETURNED HOME — PORTSMOUTH, OCT 9 (USNI OCT 12). RFA Lyme Bay (L3007), in the Indian Ocean, is now the only Royal Navy presence near Hormuz."

FIELD: last_verified
OLD VALUE: "2026-05-10"
NEW VALUE: "2026-10-12"
SOURCE: USNI-Dragon (Oct 12): "returned home to Portsmouth on Friday following a seven-month deployment"
```

```
SHIP: Bundeswehr Frankenthal-class minesweeper + command/supply ship  [id: deu-mcm-frankenthal-med]
FIELD: name
OLD VALUE: "Bundeswehr Frankenthal-class minesweeper + command/supply ship"
NEW VALUE: "FGS Fulda (M1058) + FGS Rhein (A513)"

FIELD: area
OLD VALUE: "Mediterranean Sea — pre-positioning for potential Hormuz mine-clearance mission"
NEW VALUE: "Mediterranean Sea — operating with Standing NATO Mine Countermeasures Group Two; FGS Rhein relieved FGS Mosel (A512) in September (USNI Oct 12)"

FIELD: status
OLD VALUE: "PRE-POSITIONING (NOT DEPLOYED) — pending Bundestag mandate"
NEW VALUE: "NOT DEPLOYED TO HORMUZ — NO BUNDESTAG MANDATE; IN THE MEDITERRANEAN WITH SNMCMG2 (USNI OCT 12)"

FIELD: last_verified
OLD VALUE: "2026-04-26"
NEW VALUE: "2026-10-12"
SOURCE: USNI-Dragon (Oct 12)
```

---

### 5. TIMELINE-EVENTS UPDATES

Confidence: **MEDIUM-HIGH**. Diplomatic and political events are mostly multi-sourced (AP, Reuters, CBS live blogs, Al Jazeera, Times of Israel). Several Iranian-side items rest on Iran International, Tasnim or IRNA and are attributed as such. GlobalSecurity daily pages were unreadable (HTTP 402/403).

**SCHEMA NOTE:** the template in the Phase 1 prompt shows `id / war_day / sources`, but the live file uses `date, time, title, description, category, source, data_point`. Per CLAUDE.md ('Preserve schema'), the events below use the LIVE FILE schema. Every event uses `"time": "day"` and one of the five categories the file has used since October.

#### 5a. NEW EVENTS (87 events, Oct 30 gap-fill through Nov 11)

Append in the order given; the list is chronological. The 4 Oct 30 events cover developments after the Day 245 snapshot (12:25 ET) and go after the existing last Oct 30 entry. Five single-source events were removed to Section 9.

```json
[
  {
    "date": "2026-10-30",
    "time": "day",
    "title": "Qatari LNG carrier Al Mayeda struck near Hormuz",
    "description": "Nakilat said its Marshall Islands-flagged LNG carrier Al Mayeda, sailing from Qatar to Pakistan, was struck by 'unidentified objects' on the evening of Oct 30 while approaching the Strait; all 25 crew were safe and the ship remained operational. Bloomberg reported Iran had cleared its passage hours earlier at Pakistan's request. Qatar condemned the attack and said it reserves the right to take 'all necessary measures'; the UAE also condemned it.",
    "category": "military",
    "source": "Nakilat / QNA / Bloomberg via gCaptain / Al Jazeera / Khaleej Times",
    "data_point": "25 crew safe"
  },
  {
    "date": "2026-10-30",
    "time": "day",
    "title": "Oman evacuates 25 from burning tanker RITI",
    "description": "Oman's Maritime Security Centre said the Panama-flagged tanker RITI was targeted and caught fire 1.6 NM off Musandam; the Royal Navy of Oman evacuated all 25 crew. UKMTO separately reported a ship hit by an unknown projectile 40 NM south of Iran's Lavan Island with a fire on board, and a crude tanker struck while exiting the Strait.",
    "category": "military",
    "source": "Oman MSC via Reuters / Oman Observer / UKMTO",
    "data_point": "25 evacuated"
  },
  {
    "date": "2026-10-30",
    "time": "day",
    "title": "Friday prayers air call to revisit nuclear doctrine",
    "description": "Tehran's interim Friday prayer leader called a revision of Iran's nuclear doctrine a 'national demand' (BBC Persian). SNSC Secretary Rezaei said Europe must now pay the costs of the war.",
    "category": "political",
    "source": "BBC Persian / Iran International",
    "data_point": "Doctrine debate"
  },
  {
    "date": "2026-10-30",
    "time": "day",
    "title": "Iran claims drone and USV kills; CENTCOM denies",
    "description": "The IRGC said it downed and captured a US MQM-170 drone over Qeshm using electronic warfare, and Iran's navy said it destroyed an 'enemy' unmanned vessel east of Hormuz. CENTCOM denied losing any vessel.",
    "category": "military",
    "source": "Iran International / Middle East Monitor",
    "data_point": "UNVERIFIED claims"
  },
  {
    "date": "2026-10-31",
    "time": "day",
    "title": "Iranian team in Doha; Araghchi rules out US meeting",
    "description": "Iranian negotiators held talks with Qatari mediators in Doha a day after a 12-hour session in Tehran (Reuters). Araghchi told Al Jazeera the US outreach was 'a positive step' but Iran sees 'no need to meet with the Americans at this stage'; he said the current proposal cuts Iran's Hormuz reopening timeline to two days, after Qatar proposed five.",
    "category": "diplomatic",
    "source": "Reuters via The National / Al Jazeera",
    "data_point": "2-day plan"
  },
  {
    "date": "2026-10-31",
    "time": "day",
    "title": "Rezaei: Vance letter studied, not answered",
    "description": "SNSC Secretary Mohsen Rezaei told state TV he had studied the Vance letter but not replied, calling Washington's changed tone a good sign, and said Iran will not resume talks or reopen Hormuz until its seven conditions are met. He said officials are discussing whether to keep Iran's nuclear policy if war resumes, but no decision has been made.",
    "category": "diplomatic",
    "source": "IRIB via The National / Iran International",
    "data_point": "7 conditions"
  },
  {
    "date": "2026-10-31",
    "time": "day",
    "title": "Rubio: no strike decision, no deadline",
    "description": "At a G20 foreign ministers' meeting in Atlanta, Rubio said Trump had set no deadline for diplomacy and made no decision on further strikes; any deal must address core US security concerns and the US retains the military option.",
    "category": "political",
    "source": "The National / i24NEWS / Al Jazeera",
    "data_point": "No deadline"
  },
  {
    "date": "2026-10-31",
    "time": "day",
    "title": "Khamenei reportedly orders wider target list",
    "description": "Armed forces chief Maj. Gen. Ali Abdollahi said Iran would answer any attack with 'immense force' and no geographic limits on Supreme Leader Mojtaba Khamenei's orders; Khamenei reportedly told commanders to expand the list of US and Israeli targets (CTP-ISW). Army spokesman Akraminia said Iran will receive Russian Su-35s after the war.",
    "category": "military",
    "source": "Al Jazeera / The National / CTP-ISW / Tabnak",
    "data_point": "No geographic limits"
  },
  {
    "date": "2026-10-31",
    "time": "day",
    "title": "Iran says US fired on fishing boats off Qeshm",
    "description": "Iranian state media said US forces attacked two fishing boats off Qeshm, leaving two missing and one wounded; there was no US confirmation. Iran's navy claimed a tanker caught fire after hitting mines east of the Strait.",
    "category": "military",
    "source": "Iranian state media via Express Tribune / Al Arabiya",
    "data_point": "UNVERIFIED"
  },
  {
    "date": "2026-11-01",
    "time": "day",
    "title": "Doha round ends; Tehran cites shuttle diplomacy",
    "description": "Iranian negotiators ended three days of talks with Qatari mediators in Doha with a draft proposal circulating (BBC Persian). Araghchi said Tehran is pursuing shuttle diplomacy through Qatari and Pakistani mediators and no meeting with US officials is planned.",
    "category": "diplomatic",
    "source": "BBC Persian / Anadolu",
    "data_point": "3 days of talks"
  },
  {
    "date": "2026-11-01",
    "time": "day",
    "title": "Iran blacklists Royal Navy and RAF",
    "description": "Iran's Foreign Ministry designated the UK's Royal Navy and Royal Air Force terrorist organizations and MI6 a hostile group, citing Britain's 'illegal and hostile actions'. UK Defence Secretary Wes Streeting called it 'bare-faced cheek' on Nov 2.",
    "category": "diplomatic",
    "source": "Iranian MFA via Middle East Monitor / ITV / The JC",
    "data_point": "RN, RAF listed"
  },
  {
    "date": "2026-11-01",
    "time": "day",
    "title": "Trump: Iran may need 'the hammer'",
    "description": "At a rally in Dubuque, Iowa, two days before the midterms, Trump said he was holding back to save lives but 'at some point we're going to have to give them the hammer.' He also said 'Either they'll make a deal, or we'll just end it,' after what he called a 'very good talk' with Netanyahu on Saturday.",
    "category": "political",
    "source": "AFP via EWN / CBS News / Axios",
    "data_point": "Pre-midterm threat"
  },
  {
    "date": "2026-11-01",
    "time": "day",
    "title": "Vessel holed off Lima; IRGC claims two tankers",
    "description": "UKMTO said a vessel hit by an unknown projectile about 9 NM off Lima, Oman, was holed on its starboard side; all crew were safe. The IRGC Navy said two tankers exploded after hitting mines in Hormuz.",
    "category": "military",
    "source": "UKMTO via CBS News / IRGC via Middle East Eye",
    "data_point": "IRGC claim UNVERIFIED"
  },
  {
    "date": "2026-11-02",
    "time": "day",
    "title": "Oil plunges 7.6% on deal hopes",
    "description": "Brent settled at $104.77, down $8.66 (7.63%), after Trump posted that Iran 'wants a settlement, as soon as possible' and a deal 'could happen'. Vance said there had been 'some progress' and he and Trump 'feel pretty good' about a negotiated settlement.",
    "category": "economic",
    "source": "Reuters via Nation Thailand / CBS News / NYT",
    "data_point": "Brent $104.77"
  },
  {
    "date": "2026-11-02",
    "time": "day",
    "title": "Iran offers two-day timeline; 'ball in US court'",
    "description": "Araghchi said talks were 'proceeding very intensively' and Tehran had proposed cutting the deal's implementation period from seven days to two. Spokesman Baqaei said the plan could be implemented within two days if Washington lifts the blockade and ends hostilities, adding 'the ball is in the U.S. court.' First VP Aref claimed intermediaries' messages showed US acknowledgment of Iran's 'victory.'",
    "category": "diplomatic",
    "source": "CBS News / Al Jazeera / Iran International",
    "data_point": "7 days to 2"
  },
  {
    "date": "2026-11-02",
    "time": "day",
    "title": "US strikes Qeshm after IRGC fires on aircraft",
    "description": "US officials said limited defensive strikes hit Iranian targets on Qeshm Island late Monday after the IRGC fired surface-to-air missiles at a US aircraft; WSJ first reported them, and an official said it was not 'the start of expanded strikes.' IRNA reported explosions on Qeshm and Fars in Bandar Lengeh; the IRGC claimed it captured two US MQM-170s and downed an MQ-9 (unverified).",
    "category": "military",
    "source": "WSJ / AP / Fox News via Al Jazeera / CBS News / IRNA",
    "data_point": "Limited strikes"
  },
  {
    "date": "2026-11-02",
    "time": "day",
    "title": "AP: Netanyahu presses for post-midterm strikes",
    "description": "AP, citing regional officials, reported Netanyahu is pressing Trump for another wave of strikes after the midterms; Axios said Trump preferred to let negotiations play out. At the Lincoln Memorial Trump said 'it's not a war.'",
    "category": "political",
    "source": "AP / Axios via CBS News",
    "data_point": "Strike pressure"
  },
  {
    "date": "2026-11-02",
    "time": "day",
    "title": "Indian sailor killed as vessel hit off Oman",
    "description": "India said an unidentified aerial object struck an Indian vessel off Oman; one Indian national was killed and 13 were rescued by Oman's coast guard. CBS identified the vessel as the dhow MSV Al Jusufi; no one claimed responsibility.",
    "category": "humanitarian",
    "source": "India MEA via AP / CBS News",
    "data_point": "1 killed"
  },
  {
    "date": "2026-11-02",
    "time": "day",
    "title": "Record October for ship attacks",
    "description": "CBS, citing UKMTO, said October saw a record 30 attacks on commercial vessels; Iran's IRIB claimed 11 tankers caught fire in nine days, disputing CENTCOM's Adm. Cooper that routes were clear. UKMTO reported a tanker hit by two projectiles 72 NM east of Ras al-Khafji.",
    "category": "military",
    "source": "UKMTO via CBS News / IRIB / Khaama Press",
    "data_point": "30 attacks in Oct"
  },
  {
    "date": "2026-11-02",
    "time": "day",
    "title": "Iran warns of winter gas shortages",
    "description": "First Vice President Aref said Iran faces gas shortages, partly from war damage, and asked the public to conserve, warning of higher prices for heavy users. AFP reported Tehran residents crowding cafes amid inflation and war anxiety.",
    "category": "economic",
    "source": "Iran International / AFP via CBS News",
    "data_point": "Gas shortfall"
  },
  {
    "date": "2026-11-03",
    "time": "day",
    "title": "Democrats sweep Congress in war-shadowed midterms",
    "description": "Democrats won both chambers: by early Nov 4, AP tallies showed a 54-44 Senate majority after seven flips (Alaska, Mississippi outstanding) and a 228-139 House lead, up 19, with races uncalled. An AP Election Day poll found about 60% of voters called the Iran war the 'wrong decision' and about a third said it was a key factor.",
    "category": "political",
    "source": "AP / NPR / NBC News / The Week",
    "data_point": "Senate 54-44"
  },
  {
    "date": "2026-11-03",
    "time": "day",
    "title": "Ghalibaf: Iran sent 'firm and rational response'",
    "description": "Chief negotiator and Speaker Ghalibaf said Tehran had delivered a 'firm and rational response' and it is up to Washington to prevent new fighting, with Iran's 'finger on the trigger.' Rezaei called the US response 'not convincing,' and Baqaei said any deal must halt the war on all fronts, including Lebanon.",
    "category": "diplomatic",
    "source": "AP / CBS News",
    "data_point": "Reply delivered"
  },
  {
    "date": "2026-11-03",
    "time": "day",
    "title": "Qatar expects feedback within 36 hours",
    "description": "A Qatari official told Reuters both sides were studying mediators' new suggestions, with feedback expected within 36 hours. Spokesman Majed Al Ansari said Qatar remains hopeful for an interim deal after its delegation returned from Tehran.",
    "category": "diplomatic",
    "source": "Reuters / Qatar MFA via CBS News",
    "data_point": "36 hours"
  },
  {
    "date": "2026-11-03",
    "time": "day",
    "title": "Iran 'retains the right' to respond after Qeshm strikes",
    "description": "Deputy FM Gharibabadi said Iran retains the right to self-defense after the US strikes, and the IRGC said the Supreme Leader's orders had been conveyed and Iran will set the 'time and conditions' for ending attacks. UKMTO said two projectiles hit a tanker's engine room off northeast Oman (no injuries); the IRGC claimed three tankers hit mines.",
    "category": "military",
    "source": "CBS News / UKMTO / CTP-ISW",
    "data_point": "Engine room hit"
  },
  {
    "date": "2026-11-03",
    "time": "day",
    "title": "Trump: $4B annual aid to Israel to end",
    "description": "Trump told Fox News the US will stop its roughly $4B a year in aid to Israel by year's end while still selling arms, saying it was agreed with Netanyahu: 'You can consider it barter.'",
    "category": "political",
    "source": "AP / Fox News / CBS News",
    "data_point": "$4B/yr"
  },
  {
    "date": "2026-11-03",
    "time": "day",
    "title": "Aramco Q3 profit jumps 35%",
    "description": "Saudi Aramco's third-quarter net profit rose 35% to $36.3B on an average realized price of $95.20 a barrel, versus $70.10 a year earlier. The AFC moved the 2027 Asian Cup in Saudi Arabia forward to Dec 23.",
    "category": "economic",
    "source": "CBS News",
    "data_point": "$36.3B"
  },
  {
    "date": "2026-11-03",
    "time": "day",
    "title": "Israeli opposition backs Eisenkot",
    "description": "Israel's opposition leaders met for the first time since the Oct 27 election and agreed to recommend Yashar leader Gadi Eisenkot to form the first coalition.",
    "category": "political",
    "source": "AP",
    "data_point": "Eisenkot recommended"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "Vance: 'The reason we lost is the war'",
    "description": "Vance posted that 'The reason we lost is the war,' citing 2024 Trump voters who backed Democrats; Trump called that 'largely true' but said he 'would have done it again.' Trump told the FT he has no immediate plan to strike, saying he is 'locked and loaded' but 'there may be no reason for it.'",
    "category": "political",
    "source": "Spokesman-Review / CBS News / FT / WSJ",
    "data_point": "'Largely true'"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "Schumer: Iran war 'must end'",
    "description": "Schumer said 'We are going to end the war' and suggested Congress could use its funding power; Rep. Jason Crow said Congress has voted on seven war powers resolutions and passed two. Democrats lack veto-proof majorities, and the new Congress convenes Jan 3.",
    "category": "political",
    "source": "CBS News / Al Jazeera",
    "data_point": "7 WPR votes"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "Khamenei: no US shift after midterms",
    "description": "In a written statement on the anniversary of the 1979 embassy seizure, Supreme Leader Mojtaba Khamenei said anyone expecting a US policy change was 'seriously mistaken' and warned renewed attacks would bring a much wider war. He has not appeared publicly since his father was killed in February; rallies outside the former US embassy included a mock execution of Trump aired on state TV.",
    "category": "political",
    "source": "Al Jazeera / AFP / CBS News / Iran International",
    "data_point": "Embassy anniversary"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "Tehran hails 'NO TO WAR' verdict",
    "description": "Ghalibaf said 'Americans said NO TO WAR,' warning Iran's 'NO' comes with a 'Nightmare' if ignored; Rezaei said Iran handed Trump a 'strategic defeat' and Mokhber said Trump was 'slapped in the face by his own people.' IRGC adviser Moghadamfar threatened targets in the UAE and Bahrain if they host attacks.",
    "category": "diplomatic",
    "source": "Al Jazeera / CBS News",
    "data_point": "Rhetoric"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "Brent sinks below $95",
    "description": "Brent settled near $94.62, down $8.98 (8.7%), and WTI near $88.12, both the lowest since Aug 31, on the midterm result and Trump's comments on no immediate strikes.",
    "category": "economic",
    "source": "Reuters via Business Day / Trading Economics / CBS News",
    "data_point": "Brent $94.62"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "Treasury widens 'Economic Outcast' sanctions",
    "description": "Treasury sanctioned Indian nationals Suniel Kumar Sharma and Jaspreet Preeti Shahid for a maritime-fraud network aiding Iran's shadow fleet, plus Turkish firms; Bessent cited 'Operation Economic Outcast.'",
    "category": "economic",
    "source": "US Treasury via CBS News / The New Arab",
    "data_point": "New designations"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "Trump asks advisers about Hegseth's future",
    "description": "Sources told CBS Trump has asked advisers whether Defense Secretary Hegseth should stay, with some aides inclined to blame Adm. Cooper and Gen. Caine; no decision was made.",
    "category": "political",
    "source": "CBS News",
    "data_point": "No decision"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "China, Lebanon urge restraint",
    "description": "China's foreign ministry said preventing renewed hostilities is a 'top priority' and an envoy will visit Iran, Oman and Saudi Arabia this month. Lebanese PM Nawaf Salam warned against dragging Lebanon into the 'risks of renewed war.'",
    "category": "diplomatic",
    "source": "CBS News",
    "data_point": "Envoy trip"
  },
  {
    "date": "2026-11-04",
    "time": "day",
    "title": "ICRC reaches Taiz hospitals",
    "description": "The ICRC delivered four trucks of medical supplies to Taiz, its first delivery to the city's hospitals since Sept 23.",
    "category": "humanitarian",
    "source": "ICRC via CBS News",
    "data_point": "4 trucks"
  },
  {
    "date": "2026-11-05",
    "time": "day",
    "title": "Trump weighs renewed war: 'You'll know soon enough'",
    "description": "After national security meetings on Nov 4 and 5, Trump said in the Oval Office he would 'rather not destroy the rest of the country' but 'maybe I'll have to,' adding 'You'll know soon enough.' A US official said CENTCOM is finalizing preparations to resume major combat but has no new directive.",
    "category": "political",
    "source": "AP via Khaleej Times / Gulf News / Axios",
    "data_point": "Decision 'soon'"
  },
  {
    "date": "2026-11-05",
    "time": "day",
    "title": "Iran sends nuclear proposal via Qatar",
    "description": "A senior Iranian official said Tehran sent a nuclear proposal to Washington via Qatar, conditioned on its seven demands; NYT reported Iran reviewing 'concrete proposals' after two rounds in Tehran, one in Doha and talks in Armenia. Fox said it seeks sanctions relief, war-damage compensation and a smaller US presence; Trump said 'They're not doing anything without our approval.'",
    "category": "diplomatic",
    "source": "Arab News / NYT via Boston Globe / Fox News",
    "data_point": "Proposal sent"
  },
  {
    "date": "2026-11-05",
    "time": "day",
    "title": "Rezaei delivers Khamenei message to Putin",
    "description": "Rezaei met Putin at the Kremlin, delivering a message from Mojtaba Khamenei and discussing post-war regional security and a gas pipeline; he briefed Putin on the late-October four-nation Tehran meeting. Russia's Foreign Ministry advised citizens not to travel to Iran, citing the 'risk of a new escalation.'",
    "category": "diplomatic",
    "source": "Al Jazeera / Tasnim / TASS / CBS News",
    "data_point": "Kremlin meeting"
  },
  {
    "date": "2026-11-05",
    "time": "day",
    "title": "Oman and Iran work on Hormuz control system",
    "description": "Oman said it is still working with Iran on a joint mechanism to manage Hormuz traffic that could 'end the state of war.' Araghchi held calls with regional counterparts including Pakistan, Saudi Arabia, the UAE, Turkey, Qatar and Kuwait; Iran called EU foreign policy chief Kallas's accusation that it backs the Houthis 'baseless.'",
    "category": "diplomatic",
    "source": "CBS News / Al Jazeera",
    "data_point": "Joint mechanism"
  },
  {
    "date": "2026-11-05",
    "time": "day",
    "title": "Third carrier group en route via Singapore",
    "description": "The USS Theodore Roosevelt strike group will call at Singapore and is at least two weeks from the Middle East, where two carrier groups are already deployed. Hegseth, in a video outside the Pentagon, called the war historic and urged Congress to approve at least $350B in defense funding.",
    "category": "military",
    "source": "CBS News / Fox News / Iran International",
    "data_point": "3rd CSG"
  },
  {
    "date": "2026-11-05",
    "time": "day",
    "title": "Tanker hit north of Qatar; IRGC claims more",
    "description": "UKMTO said a tanker was hit by two projectiles about 50 NM north of Madinat ash Shamal, Qatar; manager Velos Tankers said one seafarer aboard MT Velos Sapphire was killed (Reuters/gCaptain). The IRGC claimed two tankers and a tug caught fire and said it downed two US MQM-170 drones (unverified).",
    "category": "military",
    "source": "UKMTO / Velos Tankers via Reuters / gCaptain / IRGC via CBS News",
    "data_point": "1 killed"
  },
  {
    "date": "2026-11-05",
    "time": "day",
    "title": "Houthis target Dammam and Medina",
    "description": "The Houthis claimed a drone attack disrupted air traffic at King Fahd International Airport in Dammam (unverified), and the Saudi-led coalition said it intercepted a missile fired at the Medina region; the Houthis denied targeting Medina.",
    "category": "military",
    "source": "CBS News",
    "data_point": "Missile intercepted"
  },
  {
    "date": "2026-11-06",
    "time": "day",
    "title": "US hits Qeshm air defenses; Trump calls it 'minor'",
    "description": "US forces struck Iranian air defenses on Qeshm Island, the first strike since the midterms; Tasnim and IRNA said two missiles hit the Suza area. Trump called it 'minor,' saying an anti-aircraft site was knocked out 'in about 15 minutes, maybe five.' Iran said it shot down a US MQ-1 over Qeshm (unverified).",
    "category": "military",
    "source": "Tasnim / IRNA via Reuters / Times of Israel / Fox News / CTP-ISW",
    "data_point": "1st post-midterm strike"
  },
  {
    "date": "2026-11-06",
    "time": "day",
    "title": "Trump calls Qatar's emir; Doha denies collapse",
    "description": "The emir's office said Trump called to discuss de-escalation, and Qatar's media office rejected reports the PM said talks had failed. Trump said 'We are doing very well with Iran' and that Iran wants a deal 'very badly.'",
    "category": "diplomatic",
    "source": "QNA via The New Arab / Fox News / Middle East Eye",
    "data_point": "Talks continue"
  },
  {
    "date": "2026-11-06",
    "time": "day",
    "title": "Tehran demands action, not paper",
    "description": "SNSC deputy Ali Bagheri said Iran will no longer rely on written US commitments and needs practical steps first (IRNA). IRGC aerospace adviser Ali Balali said any country helping a new US attack would be a legitimate target.",
    "category": "diplomatic",
    "source": "IRNA via Iran International / Tasnim via Fox News",
    "data_point": "Hard line"
  },
  {
    "date": "2026-11-06",
    "time": "day",
    "title": "Treasury targets Canadian exchangers, MEXC",
    "description": "Treasury sanctioned eight Canada-based money services businesses accused of helping Iran evade restrictions, including IRGC-linked crypto activity, and barred US banks from dealing with exchange MEXC Global. Bessent: 'Canada cannot be a safe haven for illicit financial facilitators.'",
    "category": "economic",
    "source": "US Treasury via Fox News / Middle East Eye",
    "data_point": "8 firms"
  },
  {
    "date": "2026-11-06",
    "time": "day",
    "title": "US offers $20M for nuclear program tips",
    "description": "CENTCOM announced a Rewards for Justice offer of up to $20M, plus possible relocation, for information on Iran's nuclear facilities, equipment, personnel and material movements.",
    "category": "political",
    "source": "CENTCOM / State Dept via Fox News / Times of Israel",
    "data_point": "$20M reward"
  },
  {
    "date": "2026-11-06",
    "time": "day",
    "title": "Iodine pills near Bushehr; new digging seen",
    "description": "The Times reported iodine tablets being distributed near Iranian nuclear sites; Iran's health ministry denied any link to strike fears. BBC Verify said satellite images show new digging and construction at the Garmdarreh base in Karaj and at Shahrud.",
    "category": "humanitarian",
    "source": "The Times via Fox News / YJC via Middle East Monitor / BBC Verify",
    "data_point": "Bushehr"
  },
  {
    "date": "2026-11-07",
    "time": "day",
    "title": "CENTCOM launches Task Force Iron Gate",
    "description": "Adm. Cooper ordered a roughly 20-person task force based in Tampa to disrupt weapons, sanctioned material and illicit revenue moving across Iran's land borders and Caspian routes, reinforcing what he called the 'ironclad blockade against Iran at sea.'",
    "category": "military",
    "source": "CENTCOM / Reuters / Stars and Stripes / Al Jazeera",
    "data_point": "~20 personnel"
  },
  {
    "date": "2026-11-07",
    "time": "day",
    "title": "US aircraft disable blockade runner Huda",
    "description": "CENTCOM said US aircraft disabled the cargo vessel M/V Huda in the Gulf of Oman after its crew ignored repeated warnings while trying to break the blockade.",
    "category": "military",
    "source": "CENTCOM / CBS News",
    "data_point": "Huda disabled"
  },
  {
    "date": "2026-11-07",
    "time": "day",
    "title": "IRGC lifts missile range cap",
    "description": "IRGC spokesman Mohebbi said range limits on Iran's missiles have been lifted on the Supreme Leader's order and told Fars the IRGC would establish 'the necessary readiness' if leaders change the nuclear doctrine. The IRGC also announced underground complexes to sustain missile and drone production under bombardment.",
    "category": "military",
    "source": "Fars via Middle East Eye / Iran International / Al Jazeera",
    "data_point": "Range cap lifted"
  },
  {
    "date": "2026-11-07",
    "time": "day",
    "title": "NBC: aides urge restart before new Congress",
    "description": "NBC reported Trump's advisers told him to restart major combat before the new Congress is sworn in in January; WSJ said Vance and Witkoff favor diplomacy, Hegseth and Cooper renewed strikes, and Rubio and Bessent economic pressure. Trump said a new offensive is 'highly unlikely' if talks progress.",
    "category": "political",
    "source": "NBC News / WSJ via Fox News / Times of Israel",
    "data_point": "Advisers split"
  },
  {
    "date": "2026-11-07",
    "time": "day",
    "title": "Tankers hit off Khasab; blasts across Hormozgan",
    "description": "UKMTO reported a tanker on fire 8 NM northwest of Khasab and another hit by a projectile leaving the Strait; CTP-ISW assessed Iran likely attacked. Iranian state media reported explosions on eastern Qeshm and in Jask, Sirik and Bandar Abbas, cause unclear.",
    "category": "military",
    "source": "UKMTO / CTP-ISW / Iranian state media via Middle East Eye",
    "data_point": "2 tankers hit"
  },
  {
    "date": "2026-11-07",
    "time": "day",
    "title": "Iraq says US asked it to shut Iran crossings",
    "description": "Iraqi FM Fuad Hussein said the US asked Baghdad to close all but two border crossings with Iran. David Ignatius reported Bessent asked China to use its influence with Tehran to end the war.",
    "category": "diplomatic",
    "source": "Iran International / Washington Post via Times of Israel",
    "data_point": "2 crossings"
  },
  {
    "date": "2026-11-08",
    "time": "day",
    "title": "Trump: Iron Gate 'in full force and effect'",
    "description": "Trump posted that Task Force Iron Gate is 'in full force and effect' and 'Very little gets into, or out of, Iran!' In a 60 Minutes interview aired Sunday he said he sees 'no reason' to escalate; the IRGC dismissed Iron Gate as 'a play on words.'",
    "category": "political",
    "source": "Truth Social via Al Jazeera / CBS News / Fars",
    "data_point": "Land blockade"
  },
  {
    "date": "2026-11-08",
    "time": "day",
    "title": "Araghchi: White House must make its own choice",
    "description": "Araghchi said the midterms sent a message and it is time for the White House to make its own choice, adding that Iran's two-day proposal stands if the US ends the war on all fronts. He said mediated talks have made no progress since the midterm results.",
    "category": "diplomatic",
    "source": "Tasnim / Middle East Eye",
    "data_point": "2-day offer stands"
  },
  {
    "date": "2026-11-08",
    "time": "day",
    "title": "Rubio: no breakthrough with Iran",
    "description": "Rubio said the US and Iran are not 'at the verge of a breakthrough,' calling Tehran's demands unacceptable and talks unproductive.",
    "category": "diplomatic",
    "source": "CBS News / Anadolu",
    "data_point": "No breakthrough"
  },
  {
    "date": "2026-11-08",
    "time": "day",
    "title": "Herzog gives Eisenkot mandate",
    "description": "President Herzog tasked Gadi Eisenkot with forming Israel's next government (67 MKs backed him, per Times of Israel), as Netanyahu demanded a unity government. Defense Minister Katz said Iran is seeking to renew its nuclear weapons effort and warned Hezbollah against joining any attack.",
    "category": "political",
    "source": "Times of Israel / Iran International",
    "data_point": "67 MKs"
  },
  {
    "date": "2026-11-08",
    "time": "day",
    "title": "Intercept debris damages Aramco tower in Riyadh",
    "description": "Saudi defenses intercepted 3 ballistic missiles, 2 cruise missiles and a drone; falling shrapnel caused minor damage to a Saudi Aramco administrative tower in Riyadh's King Abdullah Financial District, with no casualties (Saudi Energy Ministry); the Houthis claimed the attack. In Iraqi Kurdistan, a suspected drone hit the LPG storage unit at the Khor Mor gas field, halting production.",
    "category": "military",
    "source": "Saudi Energy Ministry via Reuters / ABC News / CBS News; Dana Gas via Long War Journal",
    "data_point": "Aramco hit"
  },
  {
    "date": "2026-11-08",
    "time": "day",
    "title": "Burning tanker off Khasab; IRGC halts four",
    "description": "UKMTO reclassified the Nov 7 tanker fire about 8 NM northwest of Khasab as an attack; IRIB said four tankers were halted in 24 hours, and the IRGC claimed three tankers on an 'illegal' route exploded (unverified).",
    "category": "military",
    "source": "UKMTO via CBS News / IRIB / LBCI",
    "data_point": "4 halted (claim)"
  },
  {
    "date": "2026-11-08",
    "time": "day",
    "title": "Iran executes three over January unrest",
    "description": "Iran executed three men convicted over armed unrest in January's protests, accused of operations for Israel and the US (Reuters); Baluch man Mohammad Aref Shahbakhsh was executed in Zahedan on Nov 7.",
    "category": "humanitarian",
    "source": "Reuters via Times of Israel / Mizan",
    "data_point": "3 executed"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "Qatar's PM meets Vance and Trump",
    "description": "Qatari PM Sheikh Mohammed bin Abdulrahman Al Thani met Vance and then Trump at the White House and welcomed 'positive discussions'; Axios said he sought more time for diplomacy.",
    "category": "diplomatic",
    "source": "Axios via CBS News / Iran International",
    "data_point": "White House talks"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "Trump: war 'militarily effectively over'",
    "description": "In unscheduled briefing-room remarks, Trump said the Iran war 'militarily, is effectively over... We're just keeping it the status quo,' at Gulf partners' behest, with a 'good chance' of a deal; he told Reuters 'we're ready to go anytime we want.' The FT reported Netanyahu has been calling Trump daily urging a resumption.",
    "category": "political",
    "source": "AP via 1News / Reuters / CBS News / FT via Times of Israel",
    "data_point": "'Status quo'"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "Rezaei: 'Time to SURRENDER' to seven conditions",
    "description": "Rezaei accused Washington of 'manufacturing fake news about imaginary talks' and said it is 'time to surrender to the seven conditions'; an Iranian security official said there will be no talks until they are met.",
    "category": "diplomatic",
    "source": "Rezaei on X via CBS News / Times of Israel / Middle East Eye",
    "data_point": "7 conditions"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "Baqaei: uranium removal off the table",
    "description": "Spokesman Baqaei said removing enriched uranium from Iran is not on the table and called the two-day plan a 'sign of goodwill' that must include the June Islamabad terms. He said the IAEA inspected a site at Bushehr 'a few days ago.'",
    "category": "diplomatic",
    "source": "CBS News / Iran International",
    "data_point": "IAEA at Bushehr"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "Massie files Hegseth impeachment articles",
    "description": "Rep. Thomas Massie introduced a 34-page, eight-article impeachment resolution against Hegseth, three articles accusing him of waging war on Iran without congressional authorization. Hegseth said he is 'not worried.'",
    "category": "political",
    "source": "CBS News / 1News",
    "data_point": "8 articles"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "France blames IRGC for supermarket fridge hack",
    "description": "The Paris prosecutor said an IRGC cyber unit was behind the Oct 11 hack of refrigeration at about 700 supermarkets that caused about 20 fires; similar hacks hit Belgium, Luxembourg and Sweden. France's foreign minister said Iran's ambassador would be summoned and EU sanctions sought.",
    "category": "diplomatic",
    "source": "Paris prosecutor via CBS News / Times of Israel / Iran International",
    "data_point": "~700 stores"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "Brent settles at $92.57; gas near $4",
    "description": "Brent fell 5.85% to $92.57, its lowest since Aug 31, after a 13.3% drop the prior week. AAA's national average was $4.0093, down more than 36 cents in a month.",
    "category": "economic",
    "source": "Reuters via Gulf News / Trading Economics / AAA via CBS News",
    "data_point": "Brent $92.57"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "Erdogan urged no strikes; Gargash sees long haul",
    "description": "Turkey's intelligence chief said Erdogan urged Trump not to launch new strikes while mediators work on a seven-point plan. UAE adviser Anwar Gargash said a resolution is unlikely for a 'long period.'",
    "category": "diplomatic",
    "source": "Middle East Eye / CBS News",
    "data_point": "Regional pressure"
  },
  {
    "date": "2026-11-09",
    "time": "day",
    "title": "Pipeline fire in Medina; spill closes UAE beach",
    "description": "Saudi Arabia's energy ministry reported a 'limited fire' on the East-West pipeline in the Medina region with no casualties or disruption. Khor Fakkan closed a beach after an oil spill about 20 miles south of the Strait.",
    "category": "military",
    "source": "Saudi Energy Ministry via CBS News",
    "data_point": "Limited fire"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "Rubio at G7: 'no need' for major combat",
    "description": "After G7 foreign ministers met in Paris, Rubio said Trump 'has concluded that for the time being there is no need for major combat operations because we are achieving the same objective by economic means,' warning Iran would 'pay a terrible price' if it crosses red lines. Host Jean-Noel Barrot said the risk of escalation 'has not been completely ruled out'; Qatar's PM joined Saudi and European ministers in Paris.",
    "category": "diplomatic",
    "source": "AFP via Yahoo / CBS News / C-SPAN / Al Arabiya",
    "data_point": "Economic track"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "Hegseth: 'We control the Strait of Hormuz'",
    "description": "At a Pentagon news conference, Hegseth cited more than 13,000 targets struck in under 40 days, over 80% of Iran's nuclear industrial base destroyed and 18 Americans killed, and said the US remains 'locked and loaded' with CENTCOM. He called the impeachment push 'sabotage.'",
    "category": "political",
    "source": "Foreign Policy (transcript) / CBS News / White House",
    "data_point": "13,000+ targets"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "House GOP blocks Hegseth impeachment",
    "description": "House Republicans blocked Massie's effort to impeach Hegseth in a near party-line procedural vote that evening (Stars and Stripes); the vote tally was not independently verified.",
    "category": "political",
    "source": "Stars and Stripes / Yahoo News / 1News",
    "data_point": "Impeachment blocked"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "Poll: 71% want Congress to end the war",
    "description": "A Reuters/Ipsos poll of 1,705 US adults found 71%, including 93% of Democrats and 51% of Republicans, want the new Congress to pass a law ending the Iran war; 26% approve of Trump's handling of it.",
    "category": "political",
    "source": "Reuters/Ipsos via Iran International / The Hill / US News",
    "data_point": "71%"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "26th Knesset sworn in",
    "description": "Israel's new Knesset was sworn in; Netanyahu told the session toppling Iran's regime is the only way to end its threat and accused Arab parties of seeking Israel's destruction. Eisenkot's bloc nominated Matan Kahana for speaker.",
    "category": "political",
    "source": "Times of Israel / Iran International",
    "data_point": "46 new MKs"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "US charges three over RAF Fairford plot",
    "description": "The Justice Department charged three alleged Iran-backed operatives over a September attempted attack on RAF Fairford; FBI Director Patel said they were linked to 'nearly 20 attempted attacks' in Europe and the US. WSJ said US aircraft were moved from RAF Mildenhall over a possible Iranian threat.",
    "category": "political",
    "source": "DOJ via CBS News / WSJ via Times of Israel",
    "data_point": "3 charged"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "Iran rejects France hack charge; EU vows response",
    "description": "Iran's foreign ministry rejected France's 'baseless accusations' and Araghchi mocked France as 'unable to manage fridges'; the EU promised a 'swift and united response.' Canada reimposed sanctions on Iranian entities, citing nuclear reporting non-compliance.",
    "category": "diplomatic",
    "source": "CBS News / Anadolu",
    "data_point": "EU response pledged"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "Tanker and ADNOC vessel hit",
    "description": "UKMTO said a tanker was hit by a projectile off Oman's northeast coast, about 19 NM northeast of Lima, with no injuries; the IRGC claimed three tankers hit mines. WAM said an ADNOC Logistics vessel was damaged in an attack in UAE territorial waters.",
    "category": "military",
    "source": "UKMTO via CBS News / IRIB / WAM",
    "data_point": "ADNOC vessel hit"
  },
  {
    "date": "2026-11-10",
    "time": "day",
    "title": "Brent briefly dips below $90",
    "description": "Brent briefly fell below $90 for the first time since late August and US crude traded near $84.94 after Trump's remarks on no new strikes.",
    "category": "economic",
    "source": "CBS News / Gulf News",
    "data_point": "Brent <$90"
  },
  {
    "date": "2026-11-11",
    "time": "day",
    "title": "Trump at Arlington: 'total victory'",
    "description": "At a Veterans Day event at Arlington, Trump said the US has won and the end is 'just a question of when we want to end it,' adding he wants 'a total victory, not a 93% victory' and that Iran would need 25 years to rebuild.",
    "category": "political",
    "source": "CBS News / Yahoo News",
    "data_point": "Veterans Day"
  },
  {
    "date": "2026-11-11",
    "time": "day",
    "title": "Rezaei: no 'single particle' of HEU leaves Iran",
    "description": "Rezaei said Iran 'will not remove even a single particle of enriched nuclear material' from the country (IRIB). He told Al Mayadeen Iran would strike US bases in Europe if used for attacks, that an attack on Pickaxe Mountain would bring strikes on all US bases, and that a new war would last '4 to 5 days.'",
    "category": "diplomatic",
    "source": "IRIB / Al Mayadeen via CBS News / Yahoo News",
    "data_point": "HEU stays"
  },
  {
    "date": "2026-11-11",
    "time": "day",
    "title": "Bessent moved to military base after threats",
    "description": "Treasury said Bessent moved from his Washington-area home to a military base after Iranian threats against his life and 'will not be deterred'; a source blamed a WSJ photo that let his Georgetown home be geolocated.",
    "category": "political",
    "source": "CBS News / Iran International",
    "data_point": "Relocated"
  },
  {
    "date": "2026-11-11",
    "time": "day",
    "title": "Pezeshkian decries MOAB threat; meets Sharif",
    "description": "Pezeshkian accused the US of 'diplomacy through threats' over the 'mother of all bombs.' Pakistani PM Shehbaz Sharif met him at the COP31 summit in Turkey and urged dialogue and building on June's interim US-Iran deal.",
    "category": "diplomatic",
    "source": "CBS News",
    "data_point": "COP31"
  },
  {
    "date": "2026-11-11",
    "time": "day",
    "title": "Iran rejects Hegseth's damage figures",
    "description": "Iran's Defense Ministry called Hegseth's figures 'deceptive' and said its stockpiles remain substantial, and a spokesman said the war ends only when Iran's demands are accepted or the enemy surrenders. Araghchi called the $20M US reward for nuclear information 'repugnant' and urged the UN and IAEA to condemn it.",
    "category": "diplomatic",
    "source": "CBS News / Iran International / Dawn",
    "data_point": "Claims disputed"
  },
  {
    "date": "2026-11-11",
    "time": "day",
    "title": "Allianz: Gulf war damage tops $200B",
    "description": "Allianz Trade put physical damage to Gulf states at just over $200B, mostly energy infrastructure, with total GCC costs of up to $790B in lost output through 2030. US winter heating costs are projected up 7.1% to $1,002, and 70.2% to $2,977 for heating oil (NEADA).",
    "category": "economic",
    "source": "Allianz Trade / NEADA via CBS News",
    "data_point": "$200B+"
  },
  {
    "date": "2026-11-11",
    "time": "day",
    "title": "Tankers hit mines; Houthi missiles at Riyadh",
    "description": "The IRGC said two tankers on an unauthorized route struck mines and caught fire, and UKMTO reported an incident involving a tanker in the eastern Strait. The Saudi-led coalition said it destroyed three Houthi cruise missiles aimed at Riyadh.",
    "category": "military",
    "source": "IRGC via CBS News / UKMTO via Arab News / Saudi-led coalition",
    "data_point": "3 missiles intercepted"
  }
]
```

---

### 6. FINANCIAL DATA UPDATES

Confidence: **HIGH** for oil settles through Nov 10, all equities, and AAA gas. **MEDIUM** for the Nov 11 oil settle (PROVISIONAL). **LOW** for war cost, which is modeled.

#### 6a. OIL PRICES (oil-prices.json)

**Roll convention:** follows the file's Sep 30 precedent, where the expiring contract's final settle is used on its expiry day. Oct 30 therefore uses the Brent December (LCOZ6) final settle of $117.64. From Nov 2 the Brent series is the January contract (LCOF7). The Oct 30 roll gap was $4.21 (January settled $113.43). Nov 2's apparent -$12.87 therefore includes the roll; the move within the January contract was -7.63%. WTI stays on NYMEX December (CLZ26) all window; it expires about Nov 19-20.

Append to the four parallel arrays (keep lengths equal: labels = brent = wti = day_map + 9 pre-war points):

```
labels  += ["Oct 30", "Nov 2", "Nov 3", "Nov 4", "Nov 5", "Nov 6", "Nov 9", "Nov 10", "Nov 11"]
brent   += [117.64, 104.77, 103.6, 94.62, 98.29, 98.32, 92.57, 91.49, 92.76]
wti     += [104.12, 96.46, 96.09, 88.12, 90.52, 90.83, 86.85, 86.04, 86.53]
day_map += [245, 248, 249, 250, 251, 252, 255, 256, 257]
last_updated: "2026-10-30" → "2026-11-11"
```

| Date | Day | Brent | Δ | WTI | Δ | Status / source |
|---|---|---|---|---|---|---|
| Oct 30 | 245 | 117.64 (Z6 final) | +2.76 | 104.12 | +2.12 | CONFIRMED (Newsquawk WTI wrap; Kotak; Reuters) |
| Nov 2 | 248 | 104.77 (F7) | -7.63% in F7 | 96.46 | -7.36% | CONFIRMED (Xinhua via The Star; Reuters via Nation Thailand; Newsquawk) |
| Nov 3 | 249 | 103.60 | -1.17 | 96.09 | -0.37 | CONFIRMED (Nation Thailand; Newsquawk) |
| Nov 4 | 250 | 94.62 | -8.98 | 88.12 | -7.97 | CONFIRMED (Reuters via The Star) |
| Nov 5 | 251 | 98.29 | +3.67 | 90.52 | +2.40 | CONFIRMED (Xinhua/AP via The Star) |
| Nov 6 | 252 | 98.32 | +0.03 | 90.83 | +0.31 | CONFIRMED (Xinhua via The Star) |
| Nov 9 | 255 | 92.57 | -5.75 | 86.85 | -3.98 | CONFIRMED (Reuters via Khaleej Times; Xinhua) |
| Nov 10 | 256 | 91.49 | -1.08 | 86.04 | -0.81 | CONFIRMED (Xinhua via The Star) |
| Nov 11 | 257 | 92.76 | +1.27 | 86.53 | +0.49 | PROVISIONAL (Xinhua via The Star Nov 12; CNBC Nov 11). Confirm against ICE/CME. |

**provisional_note: APPEND** the following text (preceded by a space):

```
UPDATE 2026-11-11: Days 245 and 248-257 added this cycle (Oct 30, Nov 2-6, Nov 9-11; the Oct 31-Nov 1 and Nov 7-8 weekends have no points). BRENT ROLL: Oct 30 uses the final settle of the expiring December contract (LCOZ6) of $117.64 (+$2.76, a six-month high), following the Sep 30 precedent. From Nov 2 the series uses January (LCOF7), which settled $113.43 on Oct 30. The roll gap of $4.21 means Nov 2's apparent -$12.87 includes an artificial step; the January-contract move was -7.63%. Reuters' 'Brent -16% on the week' and '-21% since the start of November' are measured on the continuous front month from $117.64. WTI = NYMEX December (CLZ26) throughout; it expires about Nov 19-20. SETTLES (Xinhua/AP, Reuters, Newsquawk): Oct 30 Brent 117.64 / WTI 104.12; Nov 2 104.77 / 96.46 (Qatari mediation; Iran's two-day plan); Nov 3 103.60 / 96.09 (Brent lowest since Oct 7); Nov 4 94.62 (-8.7%) / 88.12 (-8.3%), both lowest since Aug 31, after Democrats won Congress; Nov 5 98.29 / 90.52 on tanker attacks; Nov 6 98.32 / 90.83; Nov 9 92.57 (-5.85%) / 86.85 after Trump called strikes 'highly unlikely'; Nov 10 91.49 / 86.04 (Brent touched $89.16 intraday, first sub-$90 print since August). PROVISIONAL: Nov 11 Brent 92.76 / WTI 86.53 (Xinhua via The Star). The WTI change matches an early-Asia quote and Brent sits below the $93.90 intraday high, so confirm against ICE/CME. DISCREPANCIES: Nov 5 Brent 98.23 (one lead) vs 98.29 (Xinhua/AP; 98.29 used); Nov 4 Brent 94.11 (secondary snippet, likely the intraday low) vs Reuters 94.62 (used). Brent-WTI spread narrowed to ~$5.45 (Nov 10) from ~$12.90. EIA November STEO (Nov 10): Brent ~$100 in Nov-Dec, $97 average for 2026, $86 for 2027; October Dated Brent spot averaged $124.
```

#### 6b. MARKETS (markets.json)

Append **9** trading days. `sp500.data` uses the file's existing implied index base (~6,934.7; see Section 9 #12), so the chart stays continuous: value = close / 6,934.7 × 100, rounded to 2 dp. `defense`, `oil_majors` and `airlines` are null at the file tail, so append `null` ×9 to each to keep array lengths aligned.

```
labels               += ["Oct 30", "Nov 2", "Nov 3", "Nov 4", "Nov 5", "Nov 6", "Nov 9", "Nov 10", "Nov 11"]
sp500.data           += [109.31, 108.75, 109.15, 110.87, 106.04, 106.38, 108.87, 108.45, 109.87]
defense.data         += [null, null, null, null, null, null, null, null, null]
oil_majors.data      += [null, null, null, null, null, null, null, null, null]
airlines.data        += [null, null, null, null, null, null, null, null, null]
last_updated: "2026-10-30" → "2026-11-11"
```

`contexts`: append these 9 strings in order. Source for every close is the AP closing table (via WTOP).

```json
[
  "Day 245 (October 30, Friday) — S&P -1.82% to 7,580.07, its worst day since June, on an Intel collapse (-29%) and AI-spending fears; Nasdaq -2.9% to 25,437.00, Dow -1.1% to 51,770.31 (-0.6% on the week). Brent's expiring December contract settled $117.64 (+$2.76, six-month high; January LCOF7 $113.43) and WTI $104.12 (+$2.12) on post-midterm strike risk and Houthi claims on Saudi energy; Qatari LNG carrier Al Mayeda struck near Hormuz.",
  "Day 248 (November 2, Monday) — S&P -0.51% to 7,541.40 after erasing an early 1.1% gain (Marvell -12.7%); Dow +0.4% to 51,983.98, Nasdaq -1.1% to 25,164.32; airlines rose. Brent (January, first day as front month) -7.63% to $104.77 and WTI -7.36% to $96.46 on Qatari mediation and Iran's offer to cut its Hormuz plan from seven days to two; that evening the US struck an IRGC SAM launcher on Qeshm after the IRGC fired on a US jet.",
  "Day 249 (November 3, Tuesday, Election Day) — S&P +0.36% to 7,568.92 on an AI rebound despite an Apple margin warning; Nasdaq +0.8%, Dow -0.4%. Brent -1.1% to $103.60 (lowest settle since Oct 7), WTI $96.09 as Speaker Ghalibaf said Iran sent a 'firm and rational' reply via Qatar.",
  "Day 250 (November 4, Wednesday) — S&P +1.58% to 7,688.62 and Dow +3.0% (+1,569.40) to 53,356.12 after Democrats won both chambers; defense (LMT -6.9%) and oil majors (XOM -4.9%) fell. Brent -8.7% (-$8.98) to $94.62 and WTI -8.3% to $88.12, both lowest since Aug 31, as Trump told the FT there are no immediate strike plans; EIA crude stocks -865k bbl to 409.8M.",
  "Day 251 (November 5, Thursday) — S&P -4.36% to 7,353.73, its worst day since April 2025, in an AI data-centre rout on moratorium fears after the Democratic wins (Nvidia -9.3%, AMD -17.3%); Nasdaq -5.5% to 24,315.00, Dow -3.4%; 10-yr 4.84%. Brent +3.88% to $98.29 and WTI +2.72% to $90.52 after tanker attacks (one seafarer killed on Velos Sapphire) and Trump's 'you'll know soon enough.'",
  "Day 252 (November 6, Friday) — S&P +0.31% to 7,376.86 on an AI bounce and a strong jobs report (-2.7% on the week; Nasdaq -3.4%); Dow -0.5%. Brent +$0.03 to $98.32, WTI $90.83; that night the US struck an air-defence site at Suza, Qeshm Island, the first strike since the midterms.",
  "Day 255 (November 9, Monday) — S&P +2.35% to 7,549.94, best day since Apr 8, with all 11 sectors up; Nasdaq +2.7%, Dow +2.2%. Brent -5.85% to $92.57 and WTI -4.38% to $86.85 after Trump said new strikes were 'highly unlikely' while talks continue and that the war 'militarily, is effectively over.' Brent's prior week was -16% on the continuous front month (Reuters), the steepest weekly fall since early COVID.",
  "Day 256 (November 10, Tuesday) — S&P -0.38% to 7,520.93 on a hot October CPI (+0.4% m/m, core +0.3%) that pushed the 10-yr back above 5% (Nvidia -5%). Brent -1.17% to $91.49 after touching $89.16 intraday, its first dip below $90 since August; WTI $86.04. EIA's November STEO sees Brent near $100 in Nov-Dec. Rubio at the G7: 'no need for major combat operations.'",
  "Day 257 (November 11, Wednesday, Veterans Day; bond market closed) — S&P +1.31% to 7,619.38 on an AI rebound led by CoreWeave results, within 2.6% of the Oct 6 record (7,818.93); Nasdaq +1.6% to 25,466.19, Dow +0.5% to 52,486.49. Brent +1.39% to $92.76 and WTI +0.57% to $86.53 (PROVISIONAL settles) as Iran denied talks were under way and ships were hit off Lima, Oman."
]
```

#### 6c. WAR COSTS (war-costs.json)

Append **12** days. The methodology is unchanged: modeled at $500M/day (DERIVED). No new official figure was found in-window.

```
labels              += ["Day 246", "Day 247", "Day 248", "Day 249", "Day 250", "Day 251", "Day 252", "Day 253", "Day 254", "Day 255", "Day 256", "Day 257"]
daily_cost_millions += [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
last_updated: "2026-10-30" → "2026-11-11"
```

`day_notes`: append these 12 strings in order.

```json
[
  "Day 246 (October 31, Saturday) — Iranian negotiators in Doha; Rubio says no strike decision and no deadline. Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$75.3B.",
  "Day 247 (November 1, Sunday) — Doha round ends without a breakthrough; Trump threatens 'the hammer.' Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$75.8B.",
  "Day 248 (November 2, Monday) — First acknowledged US strike on Iranian soil since Sep 1 (Qeshm SAM launcher, Nov 2), described as limited and defensive; no change to the modeled rate. Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$76.3B.",
  "Day 249 (November 3, Tuesday) — Midterm elections; Democrats win both chambers. Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$76.8B.",
  "Day 250 (November 4, Wednesday) — No new official cost data. A $95B White House package (war plus other priorities) remains before Congress with no vote reported (Daily Sabah, Oct 28). Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$77.3B.",
  "Day 251 (November 5, Thursday) — Hegseth urges Congress to approve at least $350B in defense funding (video, Nov 5); CENTCOM reported finalizing preparations to resume major combat, with no new directive. Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$77.8B.",
  "Day 252 (November 6, Friday) — Limited US strike on a Qeshm air-defence site (Nov 6). Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$78.3B.",
  "Day 253 (November 7, Saturday) — CENTCOM stands up Task Force Iron Gate (~20 staff, Tampa); US aircraft disable M/V Huda (blockade enforcement). Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$78.8B.",
  "Day 254 (November 8, Sunday) — Iran claims a further US strike on Qeshm (unconfirmed). No new cost data. Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$79.3B.",
  "Day 255 (November 9, Monday) — Trump: the war 'militarily, is effectively over'; posture held at 'status quo.' Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$79.8B.",
  "Day 256 (November 10, Tuesday) — Hegseth Pentagon briefing: more than 13,000 targets struck in under 40 days and 'locked and loaded.' No new official cost figure. Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$80.3B.",
  "Day 257 (November 11, Wednesday) — No new official Pentagon, CBO, CRS or CSIS figure located since the $47.1B anchor through ~Oct 16 (~$29B munitions, $11.9B operations, $6B equipment losses; ABC News via Daily Sabah). Official-anchored alternative ~$49.3B (Day 245 ~$48.3B + 12 days × ~$86M/day, CBO's $2-3B/month). FLAG: the modeled series now runs ~$31.5B above the official anchor; recalibration recommended (Section 11). Modeled ~$500M/day (DERIVED, carried forward); cumulative ~$80.8B."
]
```

**tanker_transits:** append ONE point, which keeps the file's Kpler-style point-count convention (the Oct 6 point = 7 was Kpler):

```
tanker_transits.labels += ["Nov 8"]
tanker_transits.data   += [14]
```
Source: Kpler, about Sun Nov 8: 14 vessels including 4 crude tankers (via an aggregator citing Reuters; PROVISIONAL). Record this attribution in the Day 254 context if desired; the series has no notes field. Non-comparable series (Windward, IMF PortWatch, Lloyd's List) are listed in Section 9 and Section 11 and must NOT be mixed in.

#### 6d. CALCULATOR (calculator.json)

Source: AAA State Gas Price Averages, a single timestamp on 11/11/26 (two fetches matched). National average regular **$3.9429**. Premium = state price − $3.9429, rounded to 2 dp.

```
current_gas:  4.2   →  3.94
war_increase: 1.21  →  0.95
pre_war_gas:  2.99  (unchanged)
default_state: "TX" (unchanged)
last_updated: "2026-10-30"  →  "2026-11-11"
```

| code | state price 11/11 | premium OLD | premium NEW |
|---|---|---|---|
| avg | 3.9429 | 0 | 0 |
| CA | 5.6738 | 1.72 | 1.73 |
| HI | 5.6220 | 1.46 | 1.68 |
| TX | 3.4198 | -0.52 | -0.52 |
| FL | 3.7436 | -0.29 | -0.20 |
| NY | 4.2087 | 0.15 | 0.27 |
| PA | 4.3159 | 0.24 | 0.37 |
| OH | 3.6958 | 0.01 | -0.25 |
| IL | 4.3855 | 0.57 | 0.44 |
| AZ | 4.1911 | 0.25 | 0.25 |
| GA | 3.4335 | -0.60 | -0.51 |
| WA | 4.9439 | 1.02 | 1.00 |
| MI | 4.0108 | 0.42 | 0.07 |
| NJ | 4.0131 | -0.07 | 0.07 |
| VA | 3.8077 | -0.22 | -0.14 |
| CO | 3.7845 | 0.10 | -0.16 |
| NC | 3.2095 | -0.79 | -0.73 |

`source` → replace with:
```
"AAA national average regular $3.9429 on Nov 11, 2026 (AAA State Gas Price Averages, single timestamp 11/11/26). All 16 state premiums recomputed against $3.9429 on that timestamp. Largest moves vs Oct 30: MI +0.42 to +0.07 and OH +0.01 to -0.25 (Midwest price cycling), CO +0.10 to -0.16, HI +1.46 to +1.68, NY +0.15 to +0.27. Up $0.95 / +31.9% vs the $2.99 pre-war baseline; wartime peak $4.55 (May 21). The national average fell below $4 on Nov 10 ($3.9788); $4.1239 on Nov 4; AAA weekly release $4.1003 on Nov 5 ('highest ever for this time of year'). National diesel $6.1306; CA diesel $8.0836. EIA weekly retail $3.995 (week of Nov 9). Re-pull weekly from the same AAA page. Source: AAA."
```

---

### 7. HUMANITARIAN DATA UPDATES

Confidence: **HIGH** that official tolls are unchanged (DCAS 23 / 865 confirmed in reporting through Nov 11). **MEDIUM** for the Lebanese +1, where the event is confirmed and the cumulative 4,390 comes from one secondary source and is arithmetically consistent.

#### 7a. CASUALTIES (casualties.json)

Append **12** days (Days 246-257). Only one plotted change: **lebanese +1 on Day 250 (Nov 4)**, following the file's MoPH-increment convention with a known date of death (as on Days 226-227). No DCAS change occurred in-window, so nothing is added to us_military.

```
labels                  += ["Oct 31", "Nov 1", "Nov 2", "Nov 3", "Nov 4", "Nov 5", "Nov 6", "Nov 7", "Nov 8", "Nov 9", "Nov 10", "Nov 11"]
iranian_military.data   += [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
iranian_civilian.data   += [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
us_military.data        += [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
lebanese.data           += [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]   # the 1 is Day 250 / Nov 4
israeli_military.data   += [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
last_updated: "2026-10-30" → "2026-11-11"
```

`day_contexts`: append these 12 strings in order.

```json
[
  "Day 246 (October 31, Saturday) — No new casualties plotted; values carried forward. Iran says US forces fired on two fishing boats near Qeshm, injuring one or two fishermen (Hormozgan official via IRIB; no US comment; UNVERIFIED, not plotted). Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,389 (Lebanese MoPH since Mar 2; no update after Oct 12 located). Israeli and Iraqi figures carried forward.",
  "Day 247 (November 1, Sunday) — No new casualties plotted; values carried forward. Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,389 (Lebanese MoPH since Mar 2; no update after Oct 12 located). Israeli and Iraqi figures carried forward.",
  "Day 248 (November 2, Monday) — No new casualties plotted; values carried forward. The US strike on a Qeshm SAM launcher reported no casualties on either side. Regional (not plotted): one Indian seafarer was killed and 13 rescued when the dhow MSV Al Jusufi was struck off Oman (India MEA; UKMTO). Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,389 (Lebanese MoPH since Mar 2; no update after Oct 12 located). Israeli and Iraqi figures carried forward.",
  "Day 249 (November 3, Tuesday) — No new casualties plotted; values carried forward. Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,389 (Lebanese MoPH since Mar 2; no update after Oct 12 located). Israeli and Iraqi figures carried forward.",
  "Day 250 (November 4, Wednesday) — PLOTTED: Lebanese +1. An Israeli drone strike at Qabrikha (Marjayoun) killed Risala Scouts paramedic Muhammad Nasser Yousef and wounded one (Lebanese Health Ministry via Times of Israel, Nov 5), which ToI called the first Israeli airstrike in southern Lebanon in weeks. Regional (not plotted): a Houthi ballistic missile on a government camp in Qatabah, Dhale, killed at least 11 Yemeni soldiers and wounded at least 60 (Yemeni media via CTP-ISW). Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,390 (Lebanese MoPH since Mar 2; +1 on Nov 4 (Qabrikha). A Nov 5 MoPH update cited by the Daily Caller gives 4,390 killed / 12,429 injured (secondary source)). Israeli and Iraqi figures carried forward.",
  "Day 251 (November 5, Thursday) — No new casualties plotted; values carried forward. Regional (not plotted): one seafarer was killed when projectiles hit the tanker Velos Sapphire ~50 nm north of Qatar (Velos Tankers via Reuters/gCaptain; nationality reported as Filipino, PROVISIONAL). Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,390 (Lebanese MoPH since Mar 2; +1 on Nov 4 (Qabrikha). A Nov 5 MoPH update cited by the Daily Caller gives 4,390 killed / 12,429 injured (secondary source)). Israeli and Iraqi figures carried forward.",
  "Day 252 (November 6, Friday) — No new casualties plotted; values carried forward. The US strike on a Qeshm air-defence site reported no casualties. Regional (not plotted): at least 30 were killed at al-Hadara market, al-Wazi'iyah, Taiz (Houthi officials via AP); the Houthis blame Saudi airstrikes and the Yemeni government blames a Houthi missile (DISPUTED). Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,390 (Lebanese MoPH since Mar 2; +1 on Nov 4 (Qabrikha). A Nov 5 MoPH update cited by the Daily Caller gives 4,390 killed / 12,429 injured (secondary source)). Israeli and Iraqi figures carried forward.",
  "Day 253 (November 7, Saturday) — No new casualties plotted; values carried forward. Regional (not plotted): the Houthi Health Ministry said coalition strikes on al-Shariya, Bani Hushaysh (Sanaa province), killed 33 including 13 children and wounded 39 (Reuters/AP could not verify; the toll was revised from 22 within a day). Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,390 (Lebanese MoPH since Mar 2; +1 on Nov 4 (Qabrikha). A Nov 5 MoPH update cited by the Daily Caller gives 4,390 killed / 12,429 injured (secondary source)). Israeli and Iraqi figures carried forward.",
  "Day 254 (November 8, Sunday) — No new casualties plotted; values carried forward. Iran claims a US strike on Qeshm; Hormozgan deputy governor Ahmad Nafisi said there were no casualties. No casualties at the Aramco tower in Riyadh (intercept debris) or the Khor Mor gas field. Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,390 (Lebanese MoPH since Mar 2; +1 on Nov 4 (Qabrikha). A Nov 5 MoPH update cited by the Daily Caller gives 4,390 killed / 12,429 injured (secondary source)). Israeli and Iraqi figures carried forward.",
  "Day 255 (November 9, Monday) — No new casualties plotted; values carried forward. Regional (not plotted): OCHA puts displacement in Yemen since August at more than 313,000 (via TASS); the UN human rights office has verified 281 civilian casualties since August (69 killed, 212 injured), more than a third of them children. Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,390 (Lebanese MoPH since Mar 2; +1 on Nov 4 (Qabrikha). A Nov 5 MoPH update cited by the Daily Caller gives 4,390 killed / 12,429 injured (secondary source)). Israeli and Iraqi figures carried forward.",
  "Day 256 (November 10, Tuesday) — No new casualties plotted; values carried forward. CONTEXT: Hegseth (Nov 10) cited 18 Americans killed, the hostile-action framing; the official DCAS total remains 23 (11 hostile, 12 nonhostile). The US Military chart series still sums to 21 against the official 23 (pre-existing FLAG). Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,390 (Lebanese MoPH since Mar 2; +1 on Nov 4 (Qabrikha). A Nov 5 MoPH update cited by the Daily Caller gives 4,390 killed / 12,429 injured (secondary source)). Israeli and Iraqi figures carried forward.",
  "Day 257 (November 11, Wednesday) — No new casualties plotted; values carried forward. Trump (Veterans Day) also cited 18 Americans killed; DCAS is unchanged at 23. No casualties reported in the ship disabled ~7 nm northeast of Lima (Ambrey). IMO count of seafarers killed since the war began: at least 25 across 130 incidents (Reuters, Nov 10-11; different scope from hormuz.json). Cumulative reference values: US killed 23 / wounded 865 (DCAS); Iranian killed 3,636 (HRANA, as of Apr 7; unchanged - no authoritative later figure); Lebanese killed 4,390 (Lebanese MoPH since Mar 2; +1 on Nov 4 (Qabrikha). A Nov 5 MoPH update cited by the Daily Caller gives 4,390 killed / 12,429 injured (secondary source)). Israeli and Iraqi figures carried forward."
]
```

#### 7b. INFRASTRUCTURE (infrastructure.json)

One count changes: **Oil/Gas Facilities Hit 55+ → 57+**. For every category, PREPEND the text below plus " PRIOR — " to the existing `note`. `source` and `detail` are unchanged except where stated.

```
LABEL: Oil/Gas Facilities Hit
FIELD: count
OLD VALUE: "55+"
NEW VALUE: "57+"
NOTE (PREPEND): "DAY 257 (Oct 31-Nov 11): +2 REGIONAL, count 55+ → 57+ (MEDIUM confidence). (1) Nov 8: intercept shrapnel caused minor damage to a Saudi Aramco administrative tower in King Abdullah Financial District, Riyadh, with no casualties (Saudi Energy Ministry; a Reuters witness saw blown-out windows across several floors). Counted per the Day 230 precedent for the Dhahran HQ office tower; flag that it is an office building, not a production site. (2) Nov 9: the East-West pipeline was 'targeted' in the Medina region; a limited fire was extinguished and operations were unaffected (Energy Ministry via SPA/AFP/Gulf News). Counted per the Oct 4 Khurais precedent. NOT ADDED: Houthi claims on Aramco storage tanks and Abqaiq (Nov 8) and on 'pumping stations' near Riyadh (Nov 10), all unverified; the ADNOC L&S vessel damaged Nov 10 (a ship, not a facility); the Khor Mor gas field in Iraqi Kurdistan (Nov 8; attribution unclear, see Section 9); a South Pars fire (Nov 10; single-source, cause unknown)."
FIELD: source
OPERATION: APPEND " / Saudi Energy Ministry via SPA (Nov 8-9)"
SOURCES: https://khaleejtimes.com/world/gulf/saudi-arabia-riyadh-aramco-building-minor-damage-attempted-attack ; https://gulfnews.com/world/gulf/saudi/saudi-arabia-says-east-west-pipeline-targeted-operations-unaffected-1.500741614 ; https://aljazeera.com/news/2026/11/8/saudi-arabia-intercepts-houthi-missiles-targeting-riyadh-eastern-province
```

```
LABEL: Hospitals Damaged        (count 443+ HELD)
NOTE (PREPEND): "DAY 257 (Oct 31-Nov 11): NO NEW DAMAGE LOCATED. The US strikes on Qeshm Island (Nov 2, Nov 6) hit military air-defence targets; Hormozgan deputy governor Ahmad Nafisi said there was no damage to critical or public-service infrastructure. The ICRC reached Taiz hospitals with 4 trucks (Nov 4; Yemen theater, not counted)."

LABEL: Schools Destroyed        (count 65+ HELD)
NOTE (PREPEND): "DAY 257 (Oct 31-Nov 11): NO NEW DAMAGE LOCATED. The Qeshm strikes (Nov 2, Nov 6) hit military air-defence targets only."

LABEL: Power Plants Hit         (count 5+ HELD)
NOTE (PREPEND): "DAY 257 (Oct 31-Nov 11): HOLD 5+. Trump named power plants and bridges as potential targets (Nov 9); these are threats, not damage. The Nov 8 drone attack on the Khor Mor gas field in Iraqi Kurdistan cut about 2,800 MW of generation but hit a gas facility, not a power plant (see Section 9)."

LABEL: Nuclear Facilities Struck   (count 9+ HELD)
NOTE (PREPEND): "DAY 257 (Oct 31-Nov 11): HOLD 9+. No strike on nuclear facilities. Iran's foreign ministry says the IAEA inspected Bushehr 'a few days ago' (CBS, Nov 9); the IAEA has not confirmed. BBC Verify: new digging and construction at the Garmdarreh base (Karaj) and at Shahrud (Nov 6). Hegseth (Nov 10) claims more than 80% of Iran's nuclear industrial base was destroyed; Iran's Defense Ministry calls the figures 'deceptive.' UN experts' estimate of ~440 kg of 60%-enriched uranium is unchanged. Rezaei (Nov 11): Iran 'will not remove even a single particle of enriched nuclear material.'"

LABEL: Airports Damaged         (count 17+ HELD)
NOTE (PREPEND): "DAY 257 (Oct 31-Nov 11): HOLD 17+. Najran: two Houthi ballistic missiles were intercepted on Nov 6 with debris falling; facility damage is unconfirmed. UNVERIFIED Houthi claims: Riyadh King Khalid ('extensive damage', Nov 4; again Nov 8), Dammam King Fahd (Nov 5), Abha (Nov 3) and a transport aircraft at Jizan (Oct 31-Nov 2). Riyadh and Dammam are already counted."

LABEL: Bridges Destroyed        (count 18+ HELD)
NOTE (PREPEND): "DAY 257 (Oct 31-Nov 11): HOLD 18+. No new damage. Trump named bridges among potential targets (Nov 9); this is a threat, not damage."

LABEL: Water/Desalination Facilities Struck   (count 1+ HELD)
NOTE (PREPEND): "DAY 257 (Oct 31-Nov 11): HOLD 1+. No new damage located."
```

#### 7c. HORMUZ (hormuz.json)

Confidence: **MEDIUM**. Incidents are confirmed by UKMTO, Ambrey or owners. Counters are DERIVED floors.

```
FIELD: strait.display_status
OLD VALUE: "CLOSED — contested; October the worst month for ship attacks on record; first limpet-type attack (Louise 1, Oct 29); CENTCOM rejects Iran's mine claims; Vance letter via Qatar."
NEW VALUE: "CLOSED — contested; US 'minor' strikes on Qeshm air defences (Nov 2, Nov 6); seafarer killed on Velos Sapphire off Qatar (Nov 5); US disables M/V Huda (Nov 7); Task Force Iron Gate extends the blockade to land routes; near-daily IRGC mine claims."

FIELD: strait.status
OPERATION: PREPEND the text below plus " PRIOR — " to the existing value.
NEW TEXT: "Day 257 (Nov 11): CLOSED, CONTESTED; LIMITED US STRIKES ASHORE RESUME.
- US strikes on Qeshm: an IRGC SAM launcher (Nov 2), after the IRGC fired on a US fighter and launched a missile at shipping that the US intercepted; then an air-defence site at Suza (Nov 6). Iran claims a further strike on Nov 8.
- Confirmed ship strikes (UKMTO/Ambrey/owners): LNG carrier Al Mayeda off Ras al-Khaimah (Oct 30); a vessel holed off Lima (Nov 1); the dhow Al Jusufi, with 1 Indian seafarer killed (Nov 2); MT Velos Sapphire ~50 nm north of Qatar, with 1 seafarer killed (Nov 5, the deepest-in-Gulf attack of the window); a tanker leaving the strait (Nov 6); two outbound tankers off Khasab (Nov 7); SEA 1 off Lima and an ADNOC L&S vessel in UAE waters (Nov 10); a vessel disabled ~7 nm northeast of Lima (Nov 11; possibly the Saudi-flag NCC Fajr).
- UKMTO weekly (to ~Nov 4-6): 11 ships attacked, 3 sunk (unnamed). Reuters: 37 attacks in October and at least 10 in the first 10 days of November. IMO: 130 incidents and at least 25 seafarers killed since the war began.
- Iranian mine and 'halted' claims (about 25-30 hulls, Oct 31-Nov 11) are unverified and contradicted by CENTCOM, which says Iran's mines were cleared.
- Blockade 2.0 (CENTCOM, Nov 7): 147 redirected and 5 disabled since July; M/V Huda disabled ~18 nm east of Khor Fakkan (Nov 7). CENTCOM's Task Force Iron Gate (Nov 7) targets land-border and Caspian routes; the US asked Iraq to close all but two border crossings with Iran.
- Iran's position: Rezaei says the strait stays shut until seven conditions are met (Nov 4, Nov 10); Ghalibaf: 'no return to pre-war status' (Nov 11); Iran's Navy told shipowners to coordinate with Iranian forces (Nov 11).
- US position: Hegseth (Nov 10): 'We control the Strait of Hormuz.' Oman and Iran are reportedly working on a joint Hormuz control mechanism (CBS, Nov 5).
- About 162 ships anchored off Fujairah and Khor Fakkan (Nov 8)."

FIELD: strait.status_timeline
OPERATION: APPEND "; limited US self-defense strikes on Qeshm Island Nov 2 and Nov 6 (first acknowledged strikes ashore since Sep 1); CENTCOM Task Force Iron Gate stood up Nov 7 to extend the blockade to Iran's land and Caspian routes"

FIELD: strait.last_updated
OLD VALUE: "2026-10-30"
NEW VALUE: "2026-11-11"

FIELD: impact.vessels_attacked_total
OLD VALUE: 93
NEW VALUE: 102

FIELD: impact.vessels_attacked_note
OPERATION: PREPEND the text below plus " PRIOR — " to the existing value.
NEW TEXT: "NOV 11 (Day 257): floor raised to ~102 (LOW confidence, DERIVED FLOOR) = prior ~93 + 9 UKMTO/Ambrey/owner-confirmed strikes Oct 30-Nov 11: Al Mayeda (Oct 30), the Lima holing (Nov 1), dhow Al Jusufi (Nov 2), Velos Sapphire (Nov 5), the Nov 6 tanker leaving the strait, two tankers off Khasab (Nov 7), SEA 1 (Nov 10) and the ADNOC L&S vessel (Nov 10). The Nov 11 Lima strike (Ambrey) and NCC Fajr (UKMTO 202-26) are treated as possibly one hull and are NOT counted pending dedupe. Excluded: M/V Huda (a US blockade action, tracked in strikes-iran); Iranian mine and 'halted' claims; RITI (Oct 30, possible conflation with Al Mayeda); UKMTO-via-CBS reports south of Lavan Island (Oct 30) and east of Ras al-Khafji (Nov 2) pending dedupe. Upper-bound cross-checks: UKMTO >120 commercial ships hit since the war began (Nov 1); IMO 130 incidents (Nov 10-11); JMIC 177 incidents since Mar 1, including non-attacks. The floor is likely low."

FIELD: impact.seafarer_fatalities
OLD VALUE: 18
NEW VALUE: 20
REASON: +1 Indian seafarer, dhow MSV Al Jusufi (Nov 2; India MEA; UKMTO weekly: '1 crew member killed after a dhow was struck on 2 November'); +1 seafarer, MT Velos Sapphire (Nov 5; Velos Tankers via Reuters/gCaptain). Different scope from IMO's 'at least 25' (Section 9).

FIELD: impact.brent_crude_current_usd
OLD VALUE: 114.88
NEW VALUE: 92.76

FIELD: impact.brent_crude_increase_pct
OLD VALUE: 61.8
NEW VALUE: 30.6

FIELD: impact.tankers_transiting_current_daily
OLD VALUE: 8
NEW VALUE: 8   (HELD)

FIELD: impact.tankers_transiting_current_note
OPERATION: PREPEND the text below plus " PRIOR — " to the existing value.
NEW TEXT: "NOV 11 (Day 257): HELD at ~8 (LOW). Point counts by source:
- Kpler: about Sun Nov 8, 14 vessels including 4 crude tankers (via Reuters; PROVISIONAL).
- Windward: Nov 1, 8 vessels (4 in, 4 out, 3 dark); Nov 9, 6; Nov 10, 10 (5 in, 5 out). All PROVISIONAL.
- IMF PortWatch: 1-8 vessels/day (0-4 tankers) Oct 31-Nov 8, against a pre-war average of 84.1 total / 47.2 tankers.
- Lloyd's List (non-Iranian-linked tankers and gas carriers over 10k dwt): 95 in the week of Oct 19-25, about 13.6/day.
- UKMTO weekly: 170 outbound and 155 inbound, about 65% below pre-war.
These methods are not comparable; do not merge them. Vortexa: Gulf exports averaged 17.1M bpd in October vs 18.9M in September."
```

---

### 8. OTHER UPDATES

#### 8a. GLOBAL BASES (global-bases.json)

**No change.** Candidates were reviewed and rejected:
- Task Force Iron Gate is a coordination cell at CENTCOM HQ in Tampa, not a new base.
- A GCC forward command in Kuwait rests on a single source (MEMO); see Section 9.

#### 8b. HISTORICAL COMPARISON (historical-comparison.json)

```
ENTRY: conflicts[0]  (label "Iran 2026 (Day 245)")
FIELD: label
OLD VALUE: "Iran 2026 (Day 245)"
NEW VALUE: "Iran 2026 (Day 257)"

FIELD: targets_struck / us_kia / daily_cost_millions
VALUES: "35914" / "23" / "500"   (all HELD; match hero-stats)

FIELD: note
NEW VALUE: "Operation Epic Fury / 2026 Iran war — Day 257 (November 11, 2026). After Democrats won both chambers on Nov 3, the expected post-midterm campaign did not begin. The US carried out limited 'self-defense' strikes on Qeshm Island (Nov 2, Nov 6) and expanded the blockade to land routes (Task Force Iron Gate, Nov 7). Trump says the war is 'militarily, effectively over'; Rubio: 'no need for major combat operations.' Targets struck held at the CENTCOM/JINSA cumulative; US deaths per DCAS (23, all causes); daily cost modeled at $500M/day (official-anchored ~$86M/day; see war-costs)."

FIELD: last_updated
OLD VALUE: "2026-10-30"
NEW VALUE: "2026-11-11"
```

The chart title in `public/index.html` ("Historical Comparison — Day 245 of Conflict" → "Day 257") is handled by Phase 2 Step 3 of BRIEFING CREATION.

---

### 9. DISCREPANCIES & UNVERIFIED INTELLIGENCE

**Phase 2 must SKIP everything in this section.** Each item gives the claim, the competing sources and an assessment, for the analyst to rule on.

**A. Kinetic claims held back**

1. **Third US strike on Qeshm, night of Nov 8.**
   - Claim: Tasnim (Nov 9, 10:13) said "US projectiles struck locations on Qeshm Island Sunday night." Hormozgan deputy governor Ahmad Nafisi said the targets were outside residential and commercial areas, with no casualties. An Iranian source told Reuters, via Iran International and warhistory.org, that radar, missile and naval-mining sites were hit early Monday; the Reuters original was not located. OSINT reports two blasts at Mahshahr at 22:20.
   - Against: no US confirmation. Trump called strikes "highly unlikely" (Nov 7-8) and "status quo" (Nov 9).
   - Assessment: HOLD. If the US confirms, add a strikes-iran entry `us-strike-qeshm-20261108` (lat 26.85, lng 55.9, approx; active_days [254]).
2. **Undisclosed October US strikes.**
   - Claim: WSJ and NBC say smaller US strikes in recent weeks were "purposefully kept secret." Specific reports are unconfirmed: Sirik launchers (Oct 22; an Israeli outlet plus OSINT) and Jask (Oct 29).
   - Iran separately claims US fire on two fishing boats off Qeshm on Oct 31, with 1-2 fishermen injured (IRIB/Reuters; no US comment).
   - Assessment: the manifest softens the existing "no strikes Oct 16-30" language to "none acknowledged" (Section 2c). Whether to log any October strike entries is an analyst decision.
3. **Nov 7 evening explosions** (eastern Qeshm, Sirik, Jask, Bandar Abbas).
   - Claim: IRNA reported blasts.
   - Against: Iranian state TV said no missile strike was confirmed and suggested Iranian military activity; Gulf News says projectiles were fired *from* Sirik.
   - Assessment: not a strike entry. It is mentioned as "cause unclear" in a timeline event.
4. **IRGC/Army drone claims** (Oct 30-Nov 7): MQM-170s "grounded" or captured, MQ-1s billed as the "15th" and "16th", MQ-9s (the "55th", a "new system"), LUCAS drones seized by electronic warfare, and an unmanned surface vessel "destroyed" (Oct 30). The claimed running total is 16 MQ-1 + 56 MQ-9.
   - Against: CENTCOM denied the USV claim and rejected a capture claim. The National (Nov 3) relayed the Nov 2 MQ-9 claim as fact.
   - Assessment: unverified; not counted.
5. **Iranian mine and "halted" claims**: about 25-30 hulls claimed Oct 31-Nov 11, with heavy overlap.
   - Against: CENTCOM's Adm. Cooper (Oct 30) says the mines laid early in the war were cleared, and Trump accuses Iran of fabricating incidents.
   - Assessment: excluded from every counter.
6. **Houthi claims of hits on Saudi targets**: Dammam King Fahd airport (Oct 31-Nov 2, Nov 5); a transport aircraft and radar at Jizan; Abha airport and King Khalid Air Base, Khamis Mushait (Nov 3); Riyadh King Khalid "extensive damage" (Nov 4, Nov 8); the Akfa camp at Najran and the Jizan border guard HQ (Nov 4); six missiles "east of al-Jawf" with "dozens" of casualties (Nov 4); Aramco storage and Abqaiq (Nov 8); "pumping stations" near Riyadh (Nov 10).
   - Against: Saudi Arabia confirmed only the intercepts and the minor KAFD damage.
   - Assessment: unverified.
7. **Taiz, al-Hadara market, Nov 6** (at least 30 killed).
   - Claim: the Houthis blame three Saudi airstrikes.
   - Against: the Yemeni government blames a Houthi ballistic missile (AP via Courthouse News).
   - Assessment: attribution DISPUTED. The file has no type for Saudi-coalition strikes in Yemen. Logged only as context in casualties Day 252.
8. **Al-Shariya, Bani Hushaysh (Sanaa province), Nov 7.**
   - Claim: coalition strikes killed 33 including 13 children and wounded 39 (Houthi Health Ministry; revised from 22 within a day). Saba says paramedics were hit in follow-up strikes.
   - Against: Reuters and AP could not verify; Saudi Arabia is investigating.
   - Assessment: a new type (e.g., `saudi_coalition_strike_yemen`) would be needed. Context only for now.
9. **Khor Mor gas field (Iraq, Nov 8) as an Oil/Gas facility hit.**
   - Event confirmed (Dana Gas; KRG): LPG storage hit, production suspended, ~2,800 MW lost.
   - Unclear: attribution. A Kataib Hezbollah hint, a launch from east of Tuz Khurmatu, and a history of pre-war militia attacks on the field.
   - Assessment: logged in strikes-retaliation as `non_state_actor_kinetic`. Adding it to infrastructure Oil/Gas (57+ → 58+) is an analyst call.
10. **South Pars fire (Nov 10)**: one Khaleej Times live-blog line, cause unknown. Not used.
11. **Kataib Hezbollah official "Al-Fraiji" killed in Babylon**: the Iraqi News page shows Nov 7, 2026, but this is probably a display date; earlier reporting (March, July) names the same commander. Not used.

**B. Hormuz deduplication**

12. Unresolved possible duplicates:
    - RITI (Oct 30, 1.6 NM off Musandam, 25 crew evacuated) vs Al Mayeda (Oct 30, 25 crew safe).
    - NCC Fajr (UKMTO 202-26) vs the Ambrey-confirmed Lima strike (Nov 11) vs Iran's Nov 11 mine claim.
    - M/V Huda vs the UAE National Guard rescue of 22 crew from a burning cargo ship (Nov 8).
    - "Navig8 Messi" as the Nov 7 Khasab tanker (OSINT only).
    - UKMTO-via-CBS reports south of Lavan Island (Oct 30) and east of Ras al-Khafji (Nov 2).
    - The UKMTO weekly "3 sank" (unnamed).
    - Assessment: the vessels_attacked floor (102) excludes all of these. The plausible upper range is ~105-108 before UKMTO's own ">120 since the war began."
13. **October attack count.** UKMTO via CBS: a record 30. Reuters / Trading Economics: 37. Washington Institute: 37. Earlier dashboard text: "UKMTO 23 since Oct 1." Not reconciled.
14. **Seafarer deaths, different scopes.** Dashboard 20 (after this update). IMO "at least 25" (130 incidents; Reuters, Nov 10-11). CENTCOM (Nov 2) "more than 20." Iran's mariners' union claims 44 Iranians killed (Feb 28-Apr 1, unverified). Do not merge.
15. **hormuz.json `us_military_deaths` = 15** is stale against DCAS 23 (11 hostile). Recommend aligning it to DCAS, or relabelling it as Hormuz-operations deaths with a source.
16. **hormuz.json `escorted_convoy_transits` = 0 looks stale.** Reported: 91 US-facilitated transits Nov 5-7 (~30/day), and Cooper (Oct 30) saying more than 3,000 vessels were escorted since summer and 1.5 billion barrels exported. URLs were not re-verified this cycle.

**C. Casualties and tolls**

17. **US deaths.** Trump (Nov 9: "we haven't lost anybody" in recent months; Nov 11: 18) and Hegseth (Nov 10: 18) vs DCAS 23 (11 hostile, 12 nonhostile). Hero holds DCAS 23. The casualties.json US series still sums to **21 vs the official 23** (pre-existing; needs a reconciliation decision).
18. **US wounded.** The Daily Caller (Nov 11) says "866 … per DCAS" with no as-of date, vs Newsweek's 865 (Nov 11). Hold 865.
19. **Israeli series.** `israeli_military` was last non-zero Jun 19 (sum 34). Times of Israel (Oct 9) reported the "17th Israeli soldier killed since June ceasefire" (Humvee rollover). Out of window; needs reconciliation.
20. **Flights cancelled is likely understated.** Cirium counted "just over 4,000" of 8,883 scheduled Saudi departures cancelled Oct 8-15 alone (Khaleej Times, Oct 15; pre-window, different scope). A low-quality count of 108 cancellations and 775 delays on Nov 2-3 (nomadlawyer) was not used. Analyst may recalibrate the 8,000.
21. **Misdated items rejected**: "Al-Tiri 1 killed, Nov 3" (a Reuters story from Nov 2025); "Israel warns four south Lebanon villages" (Nov 2025); the Aynata car strike (Nov 5, 2023); Khaleej Times Cirium pages showing Nov 11 but published Oct 12 and Oct 15.

**D. Data-structure issues (pre-existing; no Phase 2 action)**

22. **markets.json S&P index base.** The file's implied base is ~6,934.7, while hero-stats and baselines.json use the 6,878.88 pre-war close (Feb 27). This manifest keeps the file's base so the chart stays continuous. Rebasing the whole series would move every point by about +0.8%. Analyst decision.
23. **carriers.json `lcs-mcm-bahrain`.** Its lat/lng (5.42, 100.35) is Penang, Malaysia, which contradicts its "Bahrain" area text. None of the Oct 26, Nov 2 or Nov 9 USNI editions lists the LCS MCM ships. No status found after March. Recommend verifying, then moving it to ~26.21, 50.61 (NSA Bahrain) or marking it UNVERIFIED.
24. **Stale carriers entries with no in-window update**: `esb-6` John L. Canley (last verified Jun 5), `mcm-9-pioneer` and `mcm-14-chief` (Jun 15), `ssgn-728` Florida and `ssn-anson` HMS Anson (no `last_verified`), `ssbn-732` Alaska (unconfirmed). Consider downgrading their status to "UNVERIFIED — no current source."
25. **Optional allied entries** (positions notional): RFA Lyme Bay (L3007), Indian Ocean, the only Royal Navy presence near Hormuz (USNI, Oct 12); HNLMS Evertsen (F805), deployed to the Middle East Sep 27 as the Hormuz-mission forward HQ (USNI Oct 12; Netherlands MoD). Ready-to-append objects are available from the naval research notes on request.

**E. Financial alternatives not used**

26. **Tanker transits, non-comparable series**: Windward Nov 1 = 8, Nov 9 = 6, Nov 10 = 10; IMF PortWatch daily totals of 1-8 (Oct 31-Nov 8); Lloyd's List 95 per week (Oct 19-25). Only the Kpler-convention Nov 8 = 14 point was appended (Section 6c).
27. **AAA Nov 8 ticker of $4.0203**: from a search snippet only; not used in history.
28. **SPR.** EIA weekly file: 282.184M bbl (week ending Oct 30, lowest since 1982). Reuters via Khaleej Times: 279.5M. Use EIA unless the Nov 6 week print confirms the lower figure. Not currently a dashboard field.
29. **Allianz ">80 energy facilities hit"**: CBS attributes this to Allianz Trade, but Allianz's Nov 9 page gives no facility count; the number matches the IEA's 84 facilities (34 serious) from the March-April wave. Removed from the timeline event.

**F. Timeline events held back (single-source)**

30. Oct 31: "Tanker oil slicks close UAE beaches" (FT via Middle East Eye only).
31. Nov 1: "Manama Dialogue: US says channels open" (Iran International only).
32. Nov 6: "Iraqi PM makes surprise Tehran visit" (Middle East Monitor / Iran International).
33. Nov 10: "GCC approves forward command in Kuwait" (Middle East Monitor; CBS and CTP-ISW mentions unconfirmed).
34. Nov 11: "Seoul extends navy unit to Hormuz" (Iran International only).

Also deliberately not drafted:
- Channel 12's claim that the US derailed a secret Israeli operation (Nov 6).
- Pezeshkian's claims that the leader delegated peace-talk authority (Nov 2; MEE only) and ordered an end to "neither war nor peace" (Nov 9; aggregator only).
- Trump's "within 10 minutes" nuclear-site remark (MEMO only).
- Trump's "in no hurry" remark (Oct 30; Iran International Persian only).
- The 211-204 Hegseth impeachment referral tally (search snippet only).

---

### 10. BRIEFING METADATA

```
HEADLINE: Democrats win Congress; US hits Qeshm twice; Trump: war 'effectively over'; Brent sinks 21% as ship attacks persist
```
(115 characters)

Briefing index entry for Phase 2 Step 2:
```json
{
  "day": 257,
  "date": "2026-11-11",
  "label": "NOVEMBER 11, 2026 — DAY 257",
  "headline": "Democrats win Congress; US hits Qeshm twice; Trump: war 'effectively over'; Brent sinks 21% as ship attacks persist",
  "file": "data/briefings/day-257.html"
}
```

**Scaffold note for Phase 2:** the latest existing briefing is **day-245.html**; Days 246-256 have no briefings. Copy `day-245.html` → `day-257.html` (not `day-256.html`). The briefing should frame the full 12-day window.

**Suggested briefing structure** (5-7 sections, per the Phase 2 rules):
1. **Situation Summary.** The post-midterm inflection. Democrats won both chambers on Nov 3, and the "short, intense" campaign allies were told to expect did not begin. The US instead carried out two acknowledged limited strikes on Qeshm (Nov 2, Nov 6) and opened a land-route blockade (Task Force Iron Gate). Trump says the war is "militarily, effectively over," while Iran insists that no enriched uranium leaves the country and the strait stays shut until its seven conditions are met.
2. **Key Developments** (10-15 bullets): the Qeshm strikes; the midterm result and Vance's "the reason we lost is the war"; Iran's reply via Qatar and its two-day Hormuz timeline; Task Force Iron Gate and M/V Huda; the IRGC lifting its missile-range cap; Rubio at the G7 ("no need for major combat"); Hegseth ("we control the Strait"); the Reuters/Ipsos 71% poll; the Velos Sapphire and Al Jusufi deaths; the Riyadh KAFD and East-West pipeline incidents; the Khor Mor attack; Brent from $117.64 to ~$92.76; gas below $4.
3. **Thematic — Washington after the midterms:** war powers (Schumer; seven WPR votes), the Hegseth impeachment push, adviser splits over restarting before Jan 3 (NBC/WSJ), and economic means replacing combat (Rubio).
4. **Thematic — Hormuz and the maritime war:** confirmed strikes off Musandam and deep in the Gulf, the mine-claim information war, the expanded blockade, and transit counts.
5. **Thematic — the Houthi-Saudi front and the wider region:** the Riyadh salvos, the East-West pipeline, the Yemen ground war and the Taiz and al-Shariya casualties, Khor Mor in Iraq, and low-intensity Israeli fire in southern Lebanon.
6. **Thematic — markets:** the oil collapse and the Dec→Jan roll, the AI-led equity volatility (Nov 5 -4.36%), CPI and yields, and the EIA STEO.
7. **What to Watch:** TR CSG arrival (mid-November) and whether Bush or GW rotates out; the Boxer ARG's status; Iran's response to Qatar's proposals; Pickaxe Mountain threats; the lame-duck supplemental and war-powers votes; WTI's December expiry (~Nov 19-20); the next DCAS update.

---

### 11. ANALYST NOTES

**Structural observations**
1. **Regime change in US posture: from campaign to containment.** The cycle's central fact is a non-event. The post-midterm "short, intense campaign" did not happen. In its place, the US posture now has three parts: (a) tit-for-tat "self-defense" strikes on air defences that fire at US aircraft, (b) an expanding economic blockade (Iron Gate adds land and Caspian routes), and (c) public declarations of victory ("effectively over," "total victory"). Read epidemiologically, the exposure (US strikes) has dropped to a low endemic rate while the outcome (maritime attacks, Houthi salvos) has not: the war's incidence has shifted to proxies and shipping. Watch whether the lame-duck window (to Jan 3) brings an escalation spike, as NBC/WSJ report some advisers want.
2. **The information war over Hormuz is now the main battlespace.** Iran claims mine strikes almost daily (25-30 hulls in 12 days), while UKMTO/Ambrey confirm roughly one projectile strike per day near Musandam. CENTCOM says the mines are gone. Expect continued divergence; keep the dashboard on confirmed-floor counters.
3. **Oil has priced in de-escalation faster than the physical system.** Brent fell from $117.64 to ~$92.76 (-21%) while transits stayed in single or low double digits and October Dated Brent averaged $124 (EIA). Morgan Stanley notes Dated now trades at a discount to futures. A renewed strike wave would hit a market that has removed most of its risk premium.
4. **War-cost model drift is now material.** The $500M/day model sits ~$31.5B above the official-anchored path (~$49.3B). Recommendation for the next cycle: switch the headline to the official-anchored series ($47.1B at Oct 16 + CBO $2-3B/month) and show the modeled series as an upper bound, or recalibrate the modeled rate to ~$100M/day for the post-September low-intensity phase.
5. **Strike-count transparency gap.** WSJ/NBC's "kept secret" reporting means `last_iran_territory_strike` now marks the last *acknowledged* strike. Consider adding an explicit metadata field (e.g., `unacknowledged_strike_reports`) to separate the two.
6. **Saudi Arabia is now the most-attacked state in the theater.** Near-daily Houthi salvos on Riyadh, Mecca, Najran and Medina hit pipeline and Aramco assets. The Houthi campaign is the war's main active kinetic front, and the infrastructure grid's "regional" increments are growing faster than Iran-internal ones.
7. **Naval watch items.** (a) TR CSG arrival (estimates range from ~Nov 12 to end-November) and whether it relieves GW alone or creates a brief three-carrier overlap. (b) Boxer ARG may have left CENTCOM with no ARG relief; Makin Island is still in the Sea of Japan. (c) Bush passes ~225 days deployed.

**QA flags on included items** (verify before running Phase 2; none of these block execution):
- Q1. **Nov 11 oil settles** (Brent 92.76 / WTI 86.53) are PROVISIONAL (Xinhua via The Star). If ICE/CME differ, replace them in oil-prices, the hero cost panel, the Day 257 history entry and hormuz `brent_crude_current_usd`. The fallback is the Nov 10 confirmed settles (91.49 / 86.04).
- Q2. **Lebanese 4,390 / 12,429.** The event-level death is confirmed (MoPH via Times of Israel); the cumulative comes from one secondary source (Daily Caller). The arithmetic is consistent with 4,389 + 1.
- Q3. **USNI Nov 2 and Nov 9 editions**: confirm in a browser (see METADATA access limits).
- Q4. **Midterm seat counts** in the Nov 3 timeline event are early AP tallies (Senate 54-44; House 228-139), labelled as such. Al Jazeera (Nov 5) gave House 242-151. Update when final.
- Q5. **Ross (DDG-71) reassignment** from Bush to GW rests on the USNI listing only.
- Q6. **Tanker transit Nov 8 = 14** (Kpler via an aggregator citing Reuters) is PROVISIONAL.
- Q7. **Velos Sapphire victim nationality** (Filipino) is PROVISIONAL and appears only in the retaliation entry notes.
- Q8. **Coordinates** for the new strike and retaliation entries and the moved ships are approximations (stated in each entry's notes).

**Next-cycle priorities**
- Official DCAS update and casualties.json US-series reconciliation (21 vs 23).
- Lebanese MoPH primary cumulative release.
- Final midterm counts and lame-duck war-powers votes.
- WTI roll at the December expiry (~Nov 19-20) and the Brent February roll (late November): document both in provisional_note.
- War-cost methodology decision (note 4).
- Re-attempt GlobalSecurity (licence) and CTP-ISW for Nov 5 and Nov 7-11 to backfill any missed kinetic events.

---
END MANIFEST
