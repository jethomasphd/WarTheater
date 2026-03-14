# US/Israel Strikes on Iran — JSON Correction Instructions

**Date**: March 14, 2026  
**Scope**: US and Israeli strikes on Iranian territory only (counter-strikes tracked separately)  
**Convention**: Day 1 = February 28, 2026

---

## 1. CRITICAL FIX: `minab-school`

This is the single most important correction. The existing entry is wrong on date, casualties, and framing.

**Replace the entire `minab-school` object with:**

```json
{
  "id": "minab-school",
  "city": "Minab",
  "lat": 27.1053,
  "lng": 57.0681,
  "type": "us_strike",
  "subtype": "civilian_casualty",
  "targets": [
    "IRGC Navy 'Sayyid al-Shuhada' military complex / Asif missile brigade HQ (intended target)",
    "Shajareh Tayyebeh girls' elementary school (struck directly — adjacent to but walled off from IRGC base since 2016)"
  ],
  "first_strike": "2026-02-28",
  "casualties_reported": "165–180 killed (mostly girls aged 7–12), 95+ wounded",
  "casualties_source": "Iranian Red Crescent / IRNA / Iranian Ministry of Education; corroborated by NYT, CNN, NPR, BBC Verify, Bellingcat, TIME, Al Jazeera, OHCHR",
  "active_days": [1],
  "notes": "Deadliest confirmed civilian casualty incident of the war. Struck at approximately 10:45 AM local time on Day 1 during opening wave. School was triple-tapped per Iranian officials (mayor of Minab, Ministry of Education). Victims were primarily girls aged 7–12, plus teachers, parents, and the school principal. School had been physically separated from adjacent IRGC naval base by a wall and separate entrance since ~2016, with a visible soccer pitch in the courtyard by 2017 (confirmed by satellite imagery reviewed by HRW, NYT, CNN, TIME). Bellingcat and BBC Verify geolocated footage of a US Tomahawk cruise missile striking the area. Eight munitions experts confirmed to the Washington Post the missile was a Tomahawk. Pentagon preliminary internal investigation found US was likely responsible due to outdated DIA intelligence that failed to distinguish the school from the military compound. CNN reported CENTCOM created target coordinates using outdated DIA information. Trump initially blamed Iran; munitions experts confirmed no Iranian missile matches the weapon in verified footage. US is the only belligerent operating Tomahawk missiles. Under formal Pentagon investigation expected to take months."
}
```

---

## 2. FIX: `tehran-leadership` — disaggregate target dates

The current entry lumps targets struck on different days. Update the `targets` array to include per-target date annotations, and revise `notes`.

**Replace `targets` with:**

```json
"targets": [
  "Leadership House compound (Feb 28, Day 1)",
  "IRGC Malek-Ashtar building (Mar 2, Day 3 — confirmed destroyed by Iran International footage)",
  "Mehrabad Airport cargo aircraft (Feb 28, Day 1)",
  "Parliament building (approx. Mar 3, Day 4)",
  "IRIB state broadcaster HQ (early hours Mar 3, Day 4 — separate Israeli air operation)"
]
```

**Replace `notes` with:**

```
"notes": "Continuous bombardment since Day 1. Supreme Leader Khamenei killed in initial strike on Leadership House compound along with his daughter, son-in-law, grandchild, and daughter-in-law Zahra Haddad-Adel. Defense Minister Aziz Nasirzadeh, IRGC commander Mohammad Pakpour, chief of staff Abdolrahim Mousavi, Ali Shamkhani, and multiple other senior officials also killed. Mojtaba Khamenei (son) injured but survived; named new Supreme Leader on Mar 8 (Day 9). Day 11 (Mar 10): 40+ killed in Resalat Square residential area strike in eastern Tehran (see tehran-east-residential). Day 12: IDF destroys IRGC Air Force HQ (see tehran-irgc-af-hq). 460+ killed and 4,300+ wounded in Tehran alone as of Day 11 per Tehran Emergency Health Department. A further 20 civilians killed at Niloofar Square on Mar 2 (Day 3) per Iranian state media."
```

---

## 3. FIX: `tehran-east-residential` — refine location and details

**Update the following fields:**

```json
"city": "Tehran (East — Resalat Square)",
"lat": 35.7350,
"lng": 51.4650,
"targets": [
  "Residential apartment buildings near Resalat Square, Narmak neighborhood",
  "Iranian police building on same street"
],
"first_strike": "2026-03-10",
"casualties_reported": "40+ killed",
"casualties_source": "Tasnim News Agency / Iranian Red Crescent (spokesman Mojtaba Khaledi) / Drop Site News / Al Jazeera",
"active_days": [11],
"notes": "Strike hit at 1:00 AM on March 10 (during Ramadan, when shops were open late and people were gathering). Three residential buildings bombed simultaneously on the same street, plus a police building. One of the deadliest attacks on Tehran since the start of the war. Rescue crews searched rubble for survivors. Second major civilian casualty incident in Tehran after Niloofar Square (Day 3, 20 killed)."
```

Remove `active_days: [11, 12]` — the strike was a single event on Day 11. The Day 12 references in previous data appear to conflate this with the separate IDF wave of strikes on March 11.

---

## 4. FIX: `ahvaz-hospital` — clarify and split

The current entry conflates multiple Ahvaz incidents. The Aboozar Children's Hospital damage was reported as early as March 2 (Day 3), not March 12.

**Replace the entire `ahvaz-hospital` object with:**

```json
{
  "id": "ahvaz-military",
  "city": "Ahvaz",
  "lat": 31.3183,
  "lng": 48.6706,
  "type": "us_strike",
  "targets": [
    "Artesh Ground Forces 92nd Division",
    "IRGC Aerospace Force Ali Akbar Drone Base (runway cratered — confirmed by satellite imagery Mar 8)",
    "Various regime headquarters (IDF-announced Mar 13)"
  ],
  "first_strike": "2026-03-01",
  "casualties_reported": "Unknown — military targets; hospital collateral damage reported separately",
  "casualties_source": "Critical Threats / ISW / IDF / satellite imagery",
  "active_days": [2, 3, 8, 9, 13, 14],
  "notes": "Multiple military targets struck across Ahvaz over the course of the war. Aboozar Children's Hospital in Ahvaz reported damaged (not directly struck) as early as March 2 per Iranian authorities and Al Jazeera. IDF announced March 13 strikes on 'headquarters of various regime bodies' in Ahvaz simultaneously with Tehran and Shiraz. Iranian Deputy Health Minister Ali Jafarian reported 31 major clinical facilities and hospitals damaged nationwide, 12 rendered inactive, as of Day 14. WHO verified 13 attacks on healthcare infrastructure in Iran."
}
```

---

## 5. ADD: `actor` field to ALL entries

Add a new field `"actor"` to every object. Use the following values based on the documented US-south / Israel-north division of operations and specific IDF/CENTCOM claims:

| Entry ID | actor |
|---|---|
| `tehran-leadership` | `"us_israel_joint"` |
| `isfahan-nuclear` | `"us"` |
| `bushehr-nuclear` | `"us"` |
| `bandar-abbas` | `"us"` |
| `shiraz-airbase` | `"us_israel_joint"` |
| `tabriz-airbase` | `"israel"` |
| `parchin-military` | `"us_israel_joint"` |
| `arak-reactor` | `"us"` |
| `fordow-enrichment` | `"us"` |
| `kharg-island` | `"israel"` |
| `abadan-refinery` | `"us_israel_joint"` |
| `minab-school` | `"us"` |
| `kermanshah-irgc` | `"us_israel_joint"` |
| `dezful-missile` | `"us"` |
| `chabahar-port` | `"us"` |
| `mashhad-irgc` | `"us"` |
| `tehran-irgc-af-hq` | `"israel"` |
| `tehran-east-residential` | `"us_israel_joint"` |
| `ahvaz-military` | `"us_israel_joint"` |

**Rationale**: Minab is in southern Iran near Strait of Hormuz, within confirmed US area of operations per CBC, multiple analysts. IDF specifically claimed IRGC AF HQ and oil infrastructure. Tabriz is in northwest near Azerbaijan border — IDF operational zone. Nuclear sites struck with US GBU-57 bunker busters. Where unclear, default to `"us_israel_joint"`.

---

## 6. ADD: New entries for confirmed missing strike locations

### 6a. Karaj

```json
{
  "id": "karaj",
  "city": "Karaj",
  "lat": 35.8400,
  "lng": 50.9391,
  "type": "us_strike",
  "actor": "us_israel_joint",
  "targets": [
    "Military and government sites (Day 1 target city)",
    "Continued strikes on Karaj, Fardis, Malard, Garmdareh suburbs in subsequent days"
  ],
  "first_strike": "2026-02-28",
  "casualties_reported": "Unknown",
  "casualties_source": "Wikipedia (2026 Israeli–United States strikes on Iran) / NCRI local accounts",
  "active_days": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
  "notes": "Listed alongside Tehran, Isfahan, Qom, and Kermanshah as a Day 1 target city. Western Tehran suburb with significant military infrastructure. Local accounts on Day 13 described ~20 explosions in Shahriar, ~30 in Malard/Fardis, 7-8 in Garmdareh."
}
```

### 6b. Kerman

```json
{
  "id": "kerman",
  "city": "Kerman",
  "lat": 30.2839,
  "lng": 57.0834,
  "type": "us_strike",
  "actor": "us_israel_joint",
  "targets": [
    "Military and government sites"
  ],
  "first_strike": "2026-02-28",
  "casualties_reported": "Unknown",
  "casualties_source": "Wikipedia (2026 Israeli–United States strikes on Iran)",
  "active_days": [1],
  "notes": "Listed as a Day 1 target city in multiple sources alongside Tehran, Isfahan, Qom, Karaj, and Kermanshah."
}
```

### 6c. Qom (separate from Fordow)

```json
{
  "id": "qom-city",
  "city": "Qom",
  "lat": 34.6416,
  "lng": 50.8746,
  "type": "us_strike",
  "actor": "us_israel_joint",
  "targets": [
    "Military and government sites in Qom city proper (distinct from Fordow enrichment facility)"
  ],
  "first_strike": "2026-02-28",
  "casualties_reported": "Unknown",
  "casualties_source": "Multiple sources list Qom as Day 1 target city / NCRI reports 6 explosions on Day 13",
  "active_days": [1, 2, 3, 13],
  "notes": "Qom city listed as a Day 1 target alongside Tehran, Isfahan, Karaj, Kermanshah, and Kerman. Fordow enrichment facility (near Qom) tracked separately. Continued strikes reported in subsequent days."
}
```

### 6d. Konarak Naval Base

```json
{
  "id": "konarak-naval",
  "city": "Konarak",
  "lat": 25.3500,
  "lng": 60.3800,
  "type": "us_strike",
  "actor": "us",
  "targets": [
    "Konarak Naval Base"
  ],
  "first_strike": "2026-03-01",
  "casualties_reported": "Unknown",
  "casualties_source": "USNI News satellite imagery / CENTCOM",
  "active_days": [2, 3],
  "notes": "Southern coastal naval base. Confirmed struck by satellite imagery published by USNI News (March 1 image). Located in Sistan-Baluchistan province, 400km southeast of Minab. Part of US southern flank naval suppression campaign (Operation Epic Fury)."
}
```

### 6e. Khojir Military Complex

```json
{
  "id": "khojir-military",
  "city": "Khojir (Tehran Province)",
  "lat": 35.6600,
  "lng": 51.6300,
  "type": "us_strike",
  "actor": "us_israel_joint",
  "targets": [
    "Structures flanked by earthen berms (weapons/munitions research)",
    "Underground facilities"
  ],
  "first_strike": "2026-03-01",
  "casualties_reported": "Unknown",
  "casualties_source": "Critical Threats / ISW / satellite imagery (March 7 capture)",
  "active_days": [2, 3, 4, 5, 6, 7, 8],
  "notes": "Military complex east of Tehran. Satellite imagery captured March 7 confirmed several structures destroyed. Long associated with weapons research programs."
}
```

### 6f. Tehran cultural/civilian sites

```json
{
  "id": "tehran-civilian-sites",
  "city": "Tehran",
  "lat": 35.6762,
  "lng": 51.4215,
  "type": "us_strike",
  "subtype": "civilian_infrastructure",
  "actor": "us_israel_joint",
  "targets": [
    "Golestan Palace complex (UNESCO World Heritage Site — damaged by strike on Arg Square, Mar 2)",
    "Azadi Stadium (Iran's largest sports complex — bombed, Day 6+)",
    "Tehran Grand Bazaar (damaged)",
    "Bank Sepah branch (struck)",
    "Oil storage/fuel depots near Tehran (Israeli strikes Mar 7–8, caused 'river of fire' and toxic black smoke/acid rain over city)",
    "Gandhi Hospital (damaged by nearby strike on state TV tower, Mar 2 — IVF department destroyed)",
    "Schools in Parand, southwest Tehran (two schools struck)",
    "Narmak neighborhood school (damaged Day 3, at least 2 children killed)"
  ],
  "first_strike": "2026-03-02",
  "casualties_reported": "Multiple incidents — see individual notes; 460+ killed in Tehran alone as of Day 11",
  "casualties_source": "Iranian MFA / Red Crescent / WHO (verified 13 attacks on healthcare in Iran) / Al Jazeera / AP / NCRI",
  "active_days": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
  "notes": "Aggregated entry for confirmed civilian infrastructure damage across Tehran beyond the dedicated residential and military entries. Iranian MFA claimed 33 civilian locations struck nationwide including hospitals, schools, residential areas, the Grand Bazaar, Golestan Palace, and Azadi Stadium. Iranian Red Crescent reported 3,600+ civilian sites damaged as of Day 6; 20,000 civilian buildings including 16,000 residential units affected as of Day 11. WHO verified 13 attacks on healthcare infrastructure in Iran (4 healthcare workers killed, 25 injured, 4 ambulances affected). 77 healthcare facilities affected per Red Crescent; 31 major clinical facilities/hospitals damaged and 12 rendered inactive per Deputy Health Minister. Niloofar Square strike (Day 3) killed 20 civilians per state media."
}
```

### 6g. Isfahan Missile Complex (separate from nuclear)

```json
{
  "id": "isfahan-missile",
  "city": "Isfahan (Missile Complex)",
  "lat": 32.6000,
  "lng": 51.7500,
  "type": "us_strike",
  "actor": "us_israel_joint",
  "targets": [
    "Isfahan Missile Complex — underground facilities",
    "Artesh Air Force 8th Tactical Airbase (F-14 jets destroyed, confirmed by IDF Mar 7)"
  ],
  "first_strike": "2026-03-01",
  "casualties_reported": "Unknown — military targets",
  "casualties_source": "Critical Threats / ISW / IDF / satellite imagery (March 8 capture)",
  "active_days": [2, 3, 7, 8, 9],
  "notes": "Distinct from Isfahan nuclear facilities (tracked under isfahan-nuclear). Ground-penetrating munitions used on underground missile silos. IDF confirmed on March 8 that IAF strikes on March 7 destroyed F-14 fighter jets at an airbase in Isfahan, likely the 8th Tactical Airbase."
}
```

### 6h. Shiraz Missile Base (underground)

```json
{
  "id": "shiraz-missile-base",
  "city": "Shiraz (South)",
  "lat": 29.5000,
  "lng": 52.5000,
  "type": "us_strike",
  "actor": "israel",
  "targets": [
    "Underground ballistic missile production and storage facility south of Shiraz",
    "Shiraz Air Base (additional strikes beyond Day 1-2)",
    "SaIran electronics complex",
    "Shiraz airport and control tower"
  ],
  "first_strike": "2026-03-07",
  "casualties_reported": "Unknown",
  "casualties_source": "Critical Threats / ISW / IDF / satellite imagery (March 7 capture)",
  "active_days": [8, 9, 10, 11, 12, 13, 14],
  "notes": "Separate from the shiraz-airbase entry which covers Day 1-2 strikes. Satellite imagery March 7 showed ground-penetrating munitions used on underground facilities at a missile base south of Shiraz — one of at least 25 Iranian medium-range ballistic missile bases. June 2025 strikes had caused only light above-ground damage. IDF announced on March 13 that underground missile production site in Shiraz was struck. NCRI reports heavy strikes on Shiraz from early March 13, including airport, control tower, Gulf Highway, Moharrab Street, and SaIran complex."
}
```

### 6i. Khorramabad, Lorestan

```json
{
  "id": "khorramabad-lec",
  "city": "Khorramabad",
  "lat": 33.4878,
  "lng": 48.3558,
  "type": "us_strike",
  "actor": "us_israel_joint",
  "targets": [
    "IRGC headquarters",
    "Law Enforcement Command (LEC) police station",
    "LEC HQ in Borujerd (nearby)",
    "LEC targets in Kuhdasht, Eslamabad-e Gharb, Abdanan"
  ],
  "first_strike": "2026-03-08",
  "casualties_reported": "Unknown",
  "casualties_source": "Critical Threats / ISW / OSINT accounts",
  "active_days": [9, 10],
  "notes": "Part of the combined force campaign against Iran's internal security apparatus. LEC institutions targeted in cities that saw significant anti-government protests in Dec 2025–Jan 2026. CTP-ISW confirmed protests had occurred in Eslamabad-e Gharb, Borujerd, and Abdanan during the protest wave."
}
```

---

## 7. FIX: `shiraz-airbase` — update notes

Append to existing notes:

```
" IDF confirmed it has targeted 6 Iranian airbases total since Feb 28. CTP-ISW recorded strikes on 10 of Iran's 17 Artesh Air Force tactical airbases. Shiraz was struck again in the second week — see shiraz-missile-base for Day 8+ strikes."
```

---

## 8. FIX: `bandar-abbas` — remove USS Paul Ignatius reference

The current notes mention "batteries that fired on USS Paul Ignatius" on Day 14. I could not independently verify this specific incident in available sources. The IRGC coastal batteries at Bandar Abbas were struck repeatedly as part of the Strait of Hormuz suppression campaign, and commercial ships were attacked in the strait on March 11, but the Paul Ignatius claim needs sourcing.

**Replace the Day 14 portion of the notes with:**

```
"Day 14: Continued strikes on remaining coastal defense positions as part of Strait of Hormuz suppression campaign. CENTCOM reported that within 48 hours of war start, all 11 Iranian warships in the Gulf of Oman had been denied presence. Three commercial ships struck by suspected Iranian projectiles in the strait on March 11."
```

---

## 9. ADD: Aggregate metadata object

Add a top-level metadata object (either as first element or as a wrapper):

```json
{
  "id": "_metadata",
  "dataset": "us_israel_strikes_on_iran",
  "conflict": "2026 Iran War / Operation Epic Fury",
  "start_date": "2026-02-28",
  "last_updated": "2026-03-14",
  "day_convention": "Day 1 = 2026-02-28",
  "total_targets_struck": "5,000+ (per CENTCOM, as of March 10)",
  "provinces_struck": "26 of 31 (per ACLED)",
  "aggregate_casualties_iran": {
    "killed": "1,245–1,444+",
    "injured": "10,000–12,000+",
    "sources": "HRANA / Iranian Red Crescent / Iranian Deputy Health Minister / ACLED",
    "as_of": "2026-03-13"
  },
  "civilian_buildings_affected": "~20,000 (including 16,000 residential units) per Iranian Red Crescent as of Day 11",
  "healthcare_facilities_affected": "77 per Red Crescent; 31 major hospitals damaged, 12 inactive per Deputy Health Minister; WHO verified 13 attacks on healthcare",
  "us_operation_name": "Operation Epic Fury",
  "notes": "Casualty figures are Iranian government claims via Red Crescent and health ministry; independently difficult to verify due to internet blackout. HRANA (US-based) figures broadly consistent. ACLED tracking ongoing. Scope of this dataset: strikes ON Iranian territory by US and Israeli forces only. Iranian counter-strikes and regional escalation tracked in separate dataset."
}
```

---

## 10. VERIFY before committing

The coding agent should flag the following items for manual review — I could not conclusively verify these from available sources:

1. **USS Paul Ignatius incident** (referenced in original `bandar-abbas` notes) — needs specific sourcing
2. **Abadan refinery** start date of March 7 — oil infrastructure campaign timing confirmed for Tehran-area depots on that date, but Abadan specifically may have been later
3. **Bushehr reactor "not directly struck"** — plausible but thinly sourced in available materials
4. **Tabriz active_days: [1]** — only Day 1 is documented; may have been struck on subsequent days but I found no confirmation
5. Exact coordinates for `shiraz-missile-base` and `khojir-military` are approximate — refine if satellite imagery coordinates are available
