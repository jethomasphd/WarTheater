# Iran Retaliation Strikes JSON — Correction Instructions

**Dataset scope:** Iranian and proxy retaliation strikes on US, Israeli, and regional targets during the 2026 Iran War (Operation Epic Fury), beginning February 28, 2026.

**Source file:** The JSON array of strike location objects. Each object has: `id`, `city`, `lat`, `lng`, `type`, `weapon`, `origin`, `first_strike`, `casualties_reported`, `casualties_source`, `active_days`, `notes`.

**Day numbering convention:** Day 1 = February 28, 2026. Day 2 = March 1. Day 3 = March 2. Etc.

---

## 1. ENTRY CORRECTIONS

### 1.1 — `ali-al-salem-kuwait`: Decouple casualties, fix weapon type

The 6 US KIA did NOT occur at Ali Al Salem Air Base. They occurred at Port Shuaiba, Kuwait (see new entry 2.2 below). Ali Al Salem was struck by ballistic missiles on Feb 28 but Kuwaiti air defenses intercepted the projectiles; damage was from debris and fragments only.

**Changes:**
- `weapon`: Change to `"Ballistic missiles / cruise missiles / drones"`
- `casualties_reported`: Change to `"Runway damage, debris injuries. 3 Kuwaiti soldiers slightly injured. Italian facilities damaged."`
- `casualties_source`: Change to `"Kuwaiti MoD / Italian Foreign Ministry / Stars and Stripes"`
- `active_days`: Change to `[1, 2, 3, 4, 5, 6, 7, 8]` (IRGC confirmed launching 230 drones at Ali Al Salem and Camp Arifjan on Day 6 alone; sustained attacks throughout first two weeks)
- `notes`: Change to `"386th Air Expeditionary Wing hub. Kuwaiti air defenses intercepted initial ballistic missiles on Feb 28; debris fell on base. Satellite imagery confirmed damage to 12+ structures, aircraft shelters, and runway areas. Camp Canada (Canadian forces) bunkers also damaged. On March 2, Kuwaiti F/A-18 shot down 3 US F-15Es in friendly fire incident — all 6 crew ejected safely. Italian 51st Stormo personnel sheltered in bunkers."`

Remove the reference to "Fattah hypersonic" — this weapon type is unverified for this specific location.

### 1.2 — `al-udeid-qatar`: Expand active_days

**Changes:**
- `casualties_reported`: Change to `"Two missiles reached base on March 1. Early warning radar targeted. No US casualties reported."`
- `casualties_source`: Change to `"Qatar Defence Ministry / QNA / Al Jazeera"`
- `active_days`: Change to `[1, 2, 3, 4, 5, 6]` (new waves of missiles and drones intercepted over Qatar through at least Day 6, per Al Jazeera reporting from Doha)
- `notes`: Change to `"CENTCOM forward HQ. Qatar Defence Ministry said it thwarted attacks per pre-approved security plan. Two missiles reached base on March 1 per Qatar's official news agency. Long-range early warning radar in northern Qatar also targeted. Dozens of explosions heard in Doha from Patriot intercepts."`

### 1.3 — `al-dhafra-uae`: Fix casualty data, expand active_days

**Changes:**
- `casualties_reported`: Change to `"Significant infrastructure damage. 6 civilians injured by falling debris in Abu Dhabi (Pakistani and Nepalese nationals)."`
- `casualties_source`: Change to `"UAE MoD / Abu Dhabi Media Office / Xinhua"`
- `active_days`: Change to `[1, 2, 3, 4, 5, 6]` (sustained attacks; UAE intercepted multiple waves)
- `notes`: Change to `"Joint US-UAE base. Satellite imagery confirmed significant infrastructure damage. Debris fell in two locations in Abu Dhabi's Industrial City (ICAD II). UAE closed airspace and withdrew ambassador from Tehran. Attacks included both direct Iranian launches and Houthi drones from Yemen."`

### 1.4 — `bahrain-nsab`: Fix casualty data, expand active_days significantly

The "no casualties" claim is wrong.

**Changes:**
- `casualties_reported`: Change to `"1 worker killed (March 2, debris on vessel in Salman Industrial City). 1 woman killed, 8 injured (March 10, residential building hit in Manama). Significant damage to Fifth Fleet facilities."`
- `casualties_source`: Change to `"Bahrain Ministry of Interior / Bahrain National Communication Center / Xinhua"`
- `active_days`: Change to `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]` (Bahrain Defence Force confirmed intercepting 105 missiles and 176 drones since the start)
- `notes`: Change to `"US Fifth Fleet / NAVCENT HQ. Imagery showed significant damage to radomes, warehouses, and communication terminals at Juffair facility. Stena Imperative (US-flagged) struck twice at port of Bahrain, causing fire and killing a port worker. Seef commercial district in Manama also damaged. Iran also hit a desalination plant in Bahrain."`

### 1.5 — `erbil-iraq`: Add French KIA, expand details

**Changes:**
- `casualties_reported`: Change to `"1 French chief warrant officer KIA. Several French soldiers wounded. 1 airport guard killed. Iraqi Kurdish casualties reported. 27 total killed in Iraq (including 21 pro-Iran faction fighters, 3 Iranian Kurdish fighters, 1 civilian near Baghdad)."`
- `casualties_source`: Change to `"KRG / ACLED / French MoD / Al Jazeera"`
- `notes`: Change to `"US consulate area and Erbil International Airport targeted. Smoke seen rising from US base near airport. Kurdish Peshmerga positions also targeted. French soldiers casualties confirmed in Erbil region attack."`

### 1.6 — `ain-al-asad-iraq`: Flag as partially unverified

**Changes:**
- `notes`: Append `" [NOTE: Limited specific sourcing for Ain al-Asad during 2026 conflict. Entry based on pattern of attacks on US facilities across Iraq and confirmed IRGC claims of striking 27+ bases. Specific active_days and casualty details require further verification.]"`

### 1.7 — `haifa-israel`: Fix first_strike date, fix attribution

Haifa was first struck by Hezbollah on March 2, not by Iran on Feb 28.

**Changes:**
- `first_strike`: Change to `"2026-03-02"`
- `type`: Change to `"hezbollah_front"` (primary threat to Haifa is Hezbollah from Lebanon, not direct Iranian launches)
- `weapon`: Change to `"Hezbollah rockets and missiles / Iranian Kheibar Shekan MRBM (unverified)"`
- `origin`: Change to `"Lebanon (Hezbollah) / Iran"`
- `casualties_reported`: Change to `"Casualties reported but Haifa-specific figures unconfirmed. Major Israeli casualties were in Beit Shemesh (9 killed) and Tel Aviv, not Haifa."`
- `casualties_source`: Change to `"IDF / Israeli media"`
- `active_days`: Change to `[3, 4, 5, 12, 13, 14]` (Hezbollah entered March 2 = Day 3; remove Days 1-2 for Haifa)
- `notes`: Change to `"Hezbollah targeted missile defense site south of Haifa on March 2, first strikes since 2024 ceasefire. Hezbollah also launched drone swarm at Ramat David airbase targeting radar sites and control rooms. Direct Iranian missile fire at Haifa unverified — most Haifa-area attacks attributed to Hezbollah."`

### 1.8 — `tel-aviv-israel`: Fix casualty details

**Changes:**
- `casualties_reported`: Change to `"1 woman killed by direct hit on Feb 28 (plus 1 elderly woman died of respiratory distress during sirens). 22 injured on Feb 28. Ongoing missile impacts and debris casualties through conflict. 2 workers killed in Yehud (near Tel Aviv) on March 9 by Iranian cluster munitions."`
- `casualties_source`: Change to `"IDF / Magen David Adom / Israeli media"`
- `notes`: Change to `"Multiple direct missile impacts, not just debris. Feb 28 strike killed Filipina caregiver and injured 22 others including one seriously. 102-year-old man in Ramat Gan died falling during siren. March 9: two workers killed in Yehud by cluster submunitions from Iranian missile — first confirmed cluster munition casualties. By Day 10, Iran had fired ~300 missiles at Israel total, nearly half with cluster warheads. Iranian missile volleys decreased from 90 on Day 1 to 20 by Day 4, attributed to US-Israeli suppression of launchers."`

### 1.9 — `nevatim-israel`: Flag as unverified for this conflict

**Changes:**
- `notes`: Append `" [NOTE: Nevatim was confirmed targeted in 2024 and 2025 Iran-Israel exchanges. Targeting during 2026 conflict is plausible but specific damage reports for this war unverified in open-source reporting as of March 14.]"`

### 1.10 — `dimona-israel`: Flag as unverified for this conflict

**Changes:**
- `notes`: Append `" [NOTE: Symbolic targeting plausible given precedent. Arrow-3 intercepts plausible. But specific confirmed reporting of Dimona-area strikes during 2026 war not found in open sources as of March 14.]"`

### 1.11 — `beirut-lebanon`: Update casualties, remove speculative ground op details

**Changes:**
- `casualties_reported`: Change to `"773+ killed (as of March 13), 1,774+ wounded. 800,000+ displaced. At least 83 children among dead."`
- `casualties_source`: Change to `"Lebanese Health Ministry / OCHA / ACLED / CIR"`
- `active_days`: Change to `[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]` (no change)
- `notes`: Change to `"Hezbollah entered war March 2 after Khamenei assassination. Israel responded with massive strikes on Dahieh (southern suburbs) and throughout Lebanon. IDF struck 250+ targets. CIR verified 99 Israeli airstrikes between March 2-9 including 41 in Beirut. Ramada Plaza Hotel in Raouche struck March 8 (4 killed, 10 injured). Lebanese army withdrew from forward border positions. IDF limited ground incursions verified up to 2.75km inside Lebanese territory (Qaouzah village). As of March 14, Israel planning large-scale ground invasion south of Litani River per Axios/Israeli officials — NOT YET LAUNCHED. Lebanon ordered Hezbollah to disarm; Hezbollah refused."`

### 1.12 — `tyre-lebanon`: Remove speculative ground op details

**Changes:**
- `notes`: Change to `"Southern Lebanese city, Hezbollah rocket launch sites targeted. IDF issued evacuation orders for all residents south of Litani on ~Day 5, affecting 250-300 settlements. IDF 36th Division operating in southern Lebanon as of March 9. Limited incursions and active combat between IDF and Hezbollah confirmed in eastern sector near Khiyam and Ed Dhayra. Large-scale invasion south of Litani being planned but NOT YET LAUNCHED as of March 14."`

### 1.13 — `saudi-oil` (Ras Tanura): Fix date

**Changes:**
- `first_strike`: Change to `"2026-03-02"` (Saudi Arabia confirmed shooting down drones targeting Ras Tanura on Monday March 2, not March 3)
- `active_days`: Change to `[3, 4, 5]` (Day 3 = March 2)
- `notes`: Change to `"World's largest oil loading facility. Saudi Arabia confirmed shooting down two drones, debris started limited fire. No civilian injuries. Saudi Aramco warned of 'catastrophic consequences' for oil markets. Saudi Arabia increasingly diverted oil to Red Sea port of Yanbu via East-West Crude Oil Pipeline."`

### 1.14 — `hormuz-shipping-attacks`: Fix timeline, remove unverified USS Paul Ignatius details

The Strait of Hormuz crisis started much earlier than Day 12.

**Changes:**
- `first_strike`: Change to `"2026-03-02"` (IRGC officially declared strait closed on March 2)
- `weapon`: Change to `"Anti-ship missiles / drones / naval mines / explosive unmanned surface vessels / coastal batteries"`
- `active_days`: Change to `[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]` (strait effectively closed from Day 3 onward)
- `casualties_reported`: Change to `"Multiple vessels struck. 3 crew missing from Thai bulk carrier Mayuree Naree (March 11). 1 port worker killed in Bahrain (Stena Imperative). Tugboat sunk March 6 with 3 crew missing. UKMTO reported 17 incidents (13 attacks, 4 suspicious) between Feb 28 and March 11."`
- `casualties_source`: Change to `"UKMTO / Bloomberg / Precious Shipping / IRGC claims / Windward / CRS"`
- `notes`: Change to `"IRGC declared strait closed March 2, warned all ships will be attacked. Traffic dropped ~70% then to near-zero. 15M barrels crude + 5M barrels other products stranded daily. March 5: IRGC narrowed closure to US/Israel/Western allies only. March 6: tugboat assisting Safeen Prestige struck and sunk. March 7: IRGC claimed hits on tankers Prima and Louis P. March 10: Iran began planting naval mines — US destroyed 16 minelayers. March 11: large wave of attacks, 3+ vessels hit including Mayuree Naree, Express Room, One Majesty. March 12: 6 vessels attacked, reports of explosive unmanned surface vessels. IRGC small craft fleet largely intact despite airstrikes. New Supreme Leader Mojtaba Khamenei declared strait remains closed as 'tool of pressure.' Some selective passage allowed for Turkish, Indian, Saudi ships by March 13."`

Remove all references to USS Paul Ignatius intercepts and IRGC fast boat withdrawal — these are unverified.

### 1.15 — `saudi-base-attack`: Fix identification, casualty count, location

**Changes:**
- `id`: Change to `"prince-sultan-air-base-saudi"`
- `city`: Change to `"Prince Sultan Air Base, Al-Kharj, Saudi Arabia"`
- `lat`: Change to `24.0625`
- `lng`: Change to `47.5802`
- `weapon`: Change to `"Ballistic missiles / drones"`
- `origin`: Change to `"Iran"`
- `first_strike`: Change to `"2026-03-01"`
- `casualties_reported`: Change to `"1 US KIA (Sgt. Benjamin Pennington, wounded March 1, died March 8). ~12 personnel suffered concussions and shrapnel wounds."`
- `casualties_source`: Change to `"DoD / CENTCOM / Task and Purpose"`
- `active_days`: Change to `[2, 3, 8, 9, 10, 11, 12]` (Prince Sultan under repeated targeting; Saudi MoD confirmed intercepting missile headed toward PSAB on March 9)
- `notes`: Change to `"378th Air Expeditionary Wing. 2,300+ US troops stationed. Chinese satellite imagery showed 13 KC-135 tankers, 6 E-3 Sentries, 4 E-11 BACN aircraft pre-war. Saudi MoD confirmed intercepting multiple missiles. Iranian state media claimed hits on command centers and fuel storage (unconfirmed by CENTCOM). Sgt. Pennington was 7th US combat death of conflict. Pennington assigned to 1st Space Battalion, 1st Space Brigade."`

---

## 2. NEW ENTRIES TO ADD

### 2.1 — Beit Shemesh, Israel (CRITICAL — deadliest strike on Israeli civilians)

```json
{
  "id": "beit-shemesh-israel",
  "city": "Beit Shemesh, Israel",
  "lat": 31.7469,
  "lng": 34.9882,
  "type": "iran_retaliation",
  "weapon": "Iranian ballistic missile",
  "origin": "Iran",
  "first_strike": "2026-03-01",
  "casualties_reported": "9 killed (including 3 teenage siblings), 49 wounded, 11 missing",
  "casualties_source": "Magen David Adom / IDF / Israeli media",
  "active_days": [2],
  "notes": "Deadliest single strike on Israeli civilians in the conflict. Iranian ballistic missile struck synagogue and public bomb shelter in residential neighborhood, 35km west of Jerusalem. Roof of reinforced shelter collapsed. Two interceptors had been launched against the missile but failed. Demonstrated limits of Israeli missile defense even for reinforced shelters. Three Bitton siblings (ages 16, 15, 13) among the dead. United Hatzalah volunteer Ronit Elimelech and her mother Sarah also killed."
}
```

### 2.2 — Port Shuaiba, Kuwait (CRITICAL — deadliest strike on US forces)

```json
{
  "id": "port-shuaiba-kuwait",
  "city": "Port Shuaiba, Kuwait",
  "lat": 29.0386,
  "lng": 48.1636,
  "type": "iran_retaliation",
  "weapon": "Drone / projectile (under investigation)",
  "origin": "Iran",
  "first_strike": "2026-03-01",
  "casualties_reported": "6 US Army Reserve soldiers KIA, multiple wounded",
  "casualties_source": "DoD / CENTCOM / CNN / Stars and Stripes",
  "active_days": [2],
  "notes": "Deadliest single attack on US forces in the conflict. Direct hit on makeshift tactical operations center (triple-wide trailer) at civilian port, ~9am local time March 1. One projectile penetrated air defenses. All 6 KIA were from 103rd Sustainment Command (Army Reserve, Des Moines, Iowa): Capt. Cody Khork (35), SFC Nicole Amor (39), SFC Noah Tietjens (42), Sgt. Declan Coady (20), Maj. Jeffrey O'Brien, CWO3 Robert Marzan. Bodies of two initially unaccounted for, recovered from burning building. Dignified transfer at Dover AFB attended by President Trump on March 8."
}
```

### 2.3 — Camp Buehring, Kuwait

```json
{
  "id": "camp-buehring-kuwait",
  "city": "Camp Buehring, Kuwait",
  "lat": 29.5500,
  "lng": 47.5500,
  "type": "iran_retaliation",
  "weapon": "Drones",
  "origin": "Iran",
  "first_strike": "2026-02-28",
  "casualties_reported": "1 US National Guard soldier died of health-related incident on March 6 (Maj. Sorffly Davius, 46, NYPD officer). Not classified as combat death.",
  "casualties_source": "DoD / CENTCOM",
  "active_days": [1, 2, 3, 4, 5, 6, 7],
  "notes": "Northeastern Kuwait. Iranian drone struck the US garrison. Maj. Davius died during medical emergency at Camp Buehring on March 6 — incident under investigation, classified as health-related, not combat. IRGC claimed 230-drone wave targeting Camp Buehring among other Kuwait facilities on Day 6."
}
```

### 2.4 — Jordan

```json
{
  "id": "jordan-intercepts",
  "city": "Jordan (multiple locations)",
  "lat": 31.95,
  "lng": 35.93,
  "type": "iran_retaliation",
  "weapon": "Ballistic missiles / drones",
  "origin": "Iran",
  "first_strike": "2026-02-28",
  "casualties_reported": "14 people injured",
  "casualties_source": "Jordanian government / Al Jazeera",
  "active_days": [1, 2],
  "notes": "Jordan intercepted 2 ballistic missiles on Feb 28. Total of 119 Iranian missiles and drones targeted Jordan. 14 people injured. Jordan has historically cooperated with US/Israeli air defense operations."
}
```

### 2.5 — Cyprus (British base)

```json
{
  "id": "akrotiri-cyprus",
  "city": "RAF Akrotiri, Cyprus",
  "lat": 34.5907,
  "lng": 32.9879,
  "type": "iran_retaliation",
  "weapon": "Drone",
  "origin": "Iran",
  "first_strike": "2026-03-02",
  "casualties_reported": "No casualties reported",
  "casualties_source": "UK Defence Ministry",
  "active_days": [3],
  "notes": "British air force base on Mediterranean island of Cyprus struck by Iranian drone. No casualties. Represents furthest west Iranian retaliation reached. UK sovereign base area."
}
```

### 2.6 — Oman port attacks (Duqm and Salalah)

```json
{
  "id": "oman-ports",
  "city": "Duqm / Salalah, Oman",
  "lat": 19.6700,
  "lng": 57.7000,
  "type": "iran_retaliation",
  "weapon": "Drones",
  "origin": "Iran (unconfirmed — possibly Houthi)",
  "first_strike": "2026-03-05",
  "casualties_reported": "At least 1 fuel storage tank damaged in Duqm",
  "casualties_source": "Wikipedia / maritime intelligence sources",
  "active_days": [6, 7, 8],
  "notes": "Oman's deep-water ports (Duqm, Salalah, Sohar) are potential bypass routes around Strait of Hormuz closure. Drone strikes on Duqm and Salalah damaged fuel infrastructure and discouraged alternative routing. Sohar fell within insurer war risk area. Oman was only GCC country Iran did not strike on Day 1, given its mediator role. These strikes represent escalation against a traditional neutral party. First_strike date approximate — verify against maritime intelligence dailies."
}
```

### 2.7 — Kuwait International Airport

```json
{
  "id": "kuwait-intl-airport",
  "city": "Kuwait International Airport",
  "lat": 29.2266,
  "lng": 47.9689,
  "type": "iran_retaliation",
  "weapon": "Drone",
  "origin": "Iran",
  "first_strike": "2026-02-28",
  "casualties_reported": "Minor injuries to airport workers. Limited material damage to passenger terminal. 1 girl later died from shrapnel injuries (March 4).",
  "casualties_source": "Kuwaiti General Authority of Civil Aviation / Kuwaiti Ministry of Health",
  "active_days": [1],
  "notes": "Civilian airport struck by drone on evening of Feb 28. Kuwaiti authorities confirmed minor injuries and damage to passenger building. On March 4, Kuwaiti Ministry of Health reported death of a girl from shrapnel-induced injuries — likely related to airport or broader Kuwait strikes."
}
```

### 2.8 — US Embassy Kuwait area

```json
{
  "id": "us-embassy-kuwait",
  "city": "US Embassy, Hawalli, Kuwait",
  "lat": 29.3375,
  "lng": 48.0247,
  "type": "iran_retaliation",
  "weapon": "Missile (type unconfirmed)",
  "origin": "Iran",
  "first_strike": "2026-03-02",
  "casualties_reported": "Unknown — embassy personnel sheltering in place",
  "casualties_source": "Wikipedia / Xinhua (smoke visible near embassy)",
  "active_days": [3, 4, 5],
  "notes": "US Embassy in Kuwait likely hit by Iranian missile strike per Wikipedia citing multiple sources. Xinhua published screenshot showing smoke billowing near embassy area on March 2. US Embassy warned public not to approach, all personnel sheltering in place. US embassies in Saudi Arabia and UAE consulate in Dubai also reportedly targeted by drones during the week."
}
```

### 2.9 — KC-135 crash, western Iraq (non-hostile but combat operation loss)

```json
{
  "id": "kc135-crash-iraq",
  "city": "Western Iraq (crash site)",
  "lat": 33.20,
  "lng": 42.50,
  "type": "operational_loss",
  "weapon": "N/A — aircraft loss not due to hostile or friendly fire",
  "origin": "N/A",
  "first_strike": "2026-03-12",
  "casualties_reported": "6 US crew members killed",
  "casualties_source": "CENTCOM / NPR / CBS",
  "active_days": [13],
  "notes": "US KC-135 refueling aircraft lost over western Iraq on March 12. All 6 crew confirmed dead by March 13. CENTCOM confirmed loss was NOT due to hostile fire or friendly fire. Under investigation. Brings total US military deaths in conflict to 13. KC-135s from Prince Sultan Air Base form backbone of strike operations — loss highlights vulnerability of tanker fleet."
}
```

---

## 3. GLOBAL FIELD UPDATES

### 3.1 — US casualty summary (for reference/metadata)

As of March 14, 2026:
- **7 killed by enemy fire:** 6 at Port Shuaiba, Kuwait (March 1) + 1 at Prince Sultan Air Base, Saudi Arabia (wounded March 1, died March 8)
- **6 killed in KC-135 crash** over Iraq (March 12, non-hostile)
- **1 health-related death:** Maj. Davius at Camp Buehring, Kuwait (March 6)
- **Total: 13 US deaths** (+ ~140 wounded, 108 returned to duty, 8 severely injured)

### 3.2 — Israeli casualty summary (for reference)

- **15+ killed** as of March 13 per Al Jazeera tracker
- Key events: 1 killed Tel Aviv Feb 28, 9 killed Beit Shemesh March 1, 2 killed Yehud March 9
- **2,000+ wounded** (mostly minor)

### 3.3 — Consider adding a `verified` boolean field

Many entries mix confirmed reporting with plausible inference. Adding `"verified": true/false` to each entry would improve data integrity. Suggested unverified entries: `nevatim-israel`, `dimona-israel`, `ain-al-asad-iraq`, `oman-ports`.

### 3.4 — Consider adding a `last_updated` field

Given how rapidly this situation is evolving, each entry should carry `"last_updated": "2026-03-14"` so the dashboard can display data freshness.

---

## 4. VALIDATION CHECKLIST

After applying all changes, verify:

- [ ] No entry claims casualties at Ali Al Salem that belong to Port Shuaiba
- [ ] Beit Shemesh entry exists (9 Israeli civilians killed)
- [ ] Port Shuaiba entry exists (6 US KIA)
- [ ] Jordan entry exists (119 missiles/drones, 14 injured)
- [ ] Bahrain entry reflects actual casualties (2 killed, multiple injured)
- [ ] Hormuz timeline starts Day 3, not Day 12
- [ ] Prince Sultan Air Base properly identified (not generic "US base, Saudi Arabia")
- [ ] No speculative Day 13-14 IDF ground invasion details in Lebanon entries (large-scale invasion planned but NOT YET LAUNCHED)
- [ ] All `active_days` arrays extended to reflect sustained 2-week campaign
- [ ] US total KIA referenced anywhere = 13 (7 enemy fire + 6 KC-135 crash), not 6 or 8
- [ ] Weapon types flagged as unverified where specific missile variant names lack sourcing
