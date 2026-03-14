# WAR THEATER — Timeline JSON Update Instructions

## For: Coding Agent
## Task: Update the Operation Epic Fury timeline JSON
## Priority: Execute all sections in order. Do not skip any section.

---

## 0. SCHEMA REFERENCE

Every entry in the JSON array must follow this exact schema:

```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "title": "Short headline",
  "description": "2-4 sentence description. Factual, wire-service tone. No editorializing.",
  "category": "military | financial | diplomatic | humanitarian | domestic | cyber",
  "source": "Attributed sources separated by /",
  "data_point": "Key number or metric — string or null"
}
```

**Rules:**
- `category` values are: `military`, `financial`, `diplomatic`, `humanitarian`, `domestic`, `cyber`
- `cyber` is a NEW category — add it
- All times are approximate and in UTC
- `data_point` should be the single most important number from the entry, or `null` if qualitative
- Keep `description` to 2-4 sentences max. Wire-service tone. No adjectives like "devastating" or "heroic"
- `source` should be plausible institutional sources (DoD, CENTCOM, IRNA, Reuters, AP, Bloomberg, etc.)
- Maintain chronological sort order by date then time in the final array

---

## 1. ADD NEW ENTRIES — IRAQI MILITIA / PMF FRONT

This is the single largest gap. Iran's Popular Mobilization Forces (PMF/Hashd al-Shaabi) and Iraqi militia groups (Kata'ib Hezbollah, Asa'ib Ahl al-Haq) would attack US bases in Iraq and Syria from Day 1. Insert all of the following:

```json
{
  "date": "2026-02-28",
  "time": "10:00",
  "title": "Iraqi militias launch rocket attacks on US bases in Iraq and Syria",
  "description": "Kata'ib Hezbollah and allied PMF factions launch coordinated rocket and drone attacks on Al-Asad Air Base in western Iraq, Erbil in Kurdistan, and Al-Tanf garrison in Syria. US CRAM systems engage incoming. Three US service members wounded at Al-Asad.",
  "category": "military",
  "source": "CENTCOM / Iraqi Joint Operations Command",
  "data_point": "3 US bases struck simultaneously"
}
```

```json
{
  "date": "2026-03-02",
  "time": "22:00",
  "title": "Second wave of militia attacks on US forces in Iraq",
  "description": "Asa'ib Ahl al-Haq claims responsibility for drone attacks on Camp Victory near Baghdad International Airport and a logistics convoy on Route Tampa. One US contractor killed. Iraqi government calls for 'restraint by all parties' but does not condemn the attacks.",
  "category": "military",
  "source": "CENTCOM / Iraqi media / Reuters",
  "data_point": "1 US contractor KIA"
}
```

```json
{
  "date": "2026-03-05",
  "time": "04:00",
  "title": "US strikes PMF weapons depots in Iraq",
  "description": "US conducts airstrikes on three Kata'ib Hezbollah weapons storage facilities in Jurf al-Sakhar and near the Iraq-Syria border. Iraqi Prime Minister condemns the strikes as a 'violation of sovereignty.' Iraqi parliament begins emergency session to discuss expelling US forces.",
  "category": "military",
  "source": "CENTCOM / Iraqi PM office / AP",
  "data_point": "3 PMF sites struck on Iraqi soil"
}
```

```json
{
  "date": "2026-03-08",
  "time": "20:00",
  "title": "Iraqi parliament votes to expel US forces — non-binding",
  "description": "Iraqi parliament passes non-binding resolution demanding withdrawal of US forces from Iraqi territory. The vote is largely symbolic — a near-identical resolution passed in January 2020 after the Soleimani strike and was never enforced. Iraqi PM declines to sign an executive order. Militia attacks on US bases continue at a rate of 2-3 per day.",
  "category": "diplomatic",
  "source": "Iraqi parliament / Reuters / AP",
  "data_point": "Non-binding expulsion vote passes"
}
```

```json
{
  "date": "2026-03-11",
  "time": "04:00",
  "title": "Largest militia barrage yet — 40+ rockets at Al-Asad",
  "description": "PMF-aligned groups launch the largest single barrage of the conflict at Al-Asad Air Base — over 40 rockets and 5 one-way attack drones. US air defenses intercept most, but several impact the airfield, damaging two MQ-9 Reapers on the ground. Two US service members wounded. CENTCOM warns of 'decisive response.'",
  "category": "military",
  "source": "CENTCOM / DoD",
  "data_point": "40+ rockets, 2 drones destroyed on ground"
}
```

---

## 2. ADD NEW ENTRIES — HOUTHI ONGOING OPERATIONS

The Houthis appear once on Mar 3 then vanish. They would be launching daily. Add:

```json
{
  "date": "2026-03-01",
  "time": "16:00",
  "title": "Houthis declare war on US and Israeli shipping in Red Sea",
  "description": "Ansar Allah (Houthi) military spokesman Yahya Saree announces all US and Israeli-linked vessels transiting the Red Sea and Bab el-Mandeb Strait are legitimate targets. The declaration extends the Houthis' existing Red Sea campaign from the Gaza war era to the new conflict.",
  "category": "military",
  "source": "Ansar Allah media / Al Masirah TV",
  "data_point": null
}
```

```json
{
  "date": "2026-03-05",
  "time": "20:00",
  "title": "Houthis strike container ship in Red Sea — crew evacuated",
  "description": "A Greek-owned container vessel is struck by two Houthi anti-ship ballistic missiles approximately 60 nautical miles southwest of Al Hudaydah. The ship sustains significant damage and the crew is evacuated. Maersk and MSC announce suspension of all Red Sea transits, rerouting around the Cape of Good Hope.",
  "category": "military",
  "source": "UKMTO / Maersk / Reuters",
  "data_point": "Major shipping lines suspend Red Sea transits"
}
```

```json
{
  "date": "2026-03-08",
  "time": "06:00",
  "title": "US strikes Houthi missile sites in Yemen",
  "description": "US Navy and Air Force assets strike Houthi anti-ship missile launch sites, drone storage facilities, and radar installations in Sana'a, Hodeidah, and Dhamar governorates. Houthis vow retaliation and launch drone swarm toward Eilat, Israel within hours.",
  "category": "military",
  "source": "CENTCOM / Ansar Allah",
  "data_point": "12 Houthi sites struck"
}
```

```json
{
  "date": "2026-03-10",
  "time": "14:00",
  "title": "Red Sea shipping insurance premiums triple",
  "description": "War risk insurance premiums for Red Sea and Gulf of Aden transits triple to 2.5% of cargo value — up from 0.8% pre-war. Combined with Hormuz closure, approximately 35% of global seaborne oil trade is now disrupted or rerouted. Freight rates for Asia-Europe routes surge 40%.",
  "category": "financial",
  "source": "Lloyd's / Reuters / Freightos",
  "data_point": "35% of seaborne oil trade disrupted"
}
```

```json
{
  "date": "2026-03-13",
  "time": "04:00",
  "title": "Houthis launch cruise missile at US destroyer in Red Sea",
  "description": "Houthis fire a land-attack cruise missile at USS Gravely (DDG-107) operating in the southern Red Sea. The missile is intercepted by SM-2. A second salvo of 3 one-way attack drones is shot down by CIWS. No US casualties. The Red Sea front now requires continuous carrier strike group presence, straining the Navy's two-theater deployment.",
  "category": "military",
  "source": "CENTCOM / NAVCENT",
  "data_point": "1 cruise missile + 3 drones intercepted"
}
```

---

## 3. ADD NEW ENTRIES — CYBER WARFARE

This is an entirely missing thread. Add a new category value `cyber` and insert:

```json
{
  "date": "2026-02-28",
  "time": "12:00",
  "title": "Iranian cyberattacks target US financial systems and Gulf state infrastructure",
  "description": "US Cybersecurity and Infrastructure Security Agency (CISA) reports coordinated cyberattacks attributed to APT33 (Elfin) targeting US financial sector networks, Gulf state water treatment systems, and Israeli power grid control systems. Most attacks are mitigated. CISA raises threat level to 'Shields Up' — the highest alert tier.",
  "category": "cyber",
  "source": "CISA / NSA / Reuters",
  "data_point": "CISA 'Shields Up' alert issued"
}
```

```json
{
  "date": "2026-03-03",
  "time": "14:00",
  "title": "US Cyber Command disrupts Iranian military communications",
  "description": "US Cyber Command confirms offensive operations degrading IRGC command-and-control networks and Iranian military communications infrastructure. Operations are credited with slowing Iran's ability to coordinate retaliatory missile strikes. Details remain classified.",
  "category": "cyber",
  "source": "US Cyber Command / DoD (limited disclosure)",
  "data_point": null
}
```

```json
{
  "date": "2026-03-07",
  "time": "20:00",
  "title": "Iranian hackers deface US government websites and leak military emails",
  "description": "An Iranian hacking group calling itself 'Cyber Avengers' defaces several US municipal government websites and leaks a cache of emails allegedly from CENTCOM personnel. Pentagon states leaked materials are mostly unclassified and some appear fabricated. The information warfare dimension of the conflict intensifies.",
  "category": "cyber",
  "source": "CISA / FBI / DoD",
  "data_point": null
}
```

```json
{
  "date": "2026-03-12",
  "time": "04:00",
  "title": "Cyberattack disrupts Iranian oil export tracking systems",
  "description": "Iranian state media reports a cyberattack has disrupted the National Iranian Oil Company's logistics and tracking systems. Though Iran's oil export infrastructure is already physically destroyed, the attack complicates coordination of remaining domestic fuel distribution. Attribution unclear — likely US or Israeli.",
  "category": "cyber",
  "source": "IRNA / Reuters",
  "data_point": null
}
```

---

## 4. ADD NEW ENTRIES — NUCLEAR FACILITY BATTLE DAMAGE ASSESSMENT

The stated purpose of the war has no follow-through. Insert:

```json
{
  "date": "2026-03-01",
  "time": "08:00",
  "title": "Pentagon confirms strikes on all known Iranian nuclear sites",
  "description": "DoD releases initial battle damage assessment confirming strikes on Natanz (centrifuge facility), Fordow (underground enrichment site), Isfahan (uranium conversion), and the Arak heavy water reactor. Natanz surface facilities assessed as destroyed. Fordow, buried under 80+ meters of rock, sustained multiple GBU-57 Massive Ordnance Penetrator hits — damage assessment ongoing. Isfahan conversion facility severely damaged. Arak reactor building collapsed.",
  "category": "military",
  "source": "DoD / CENTCOM / satellite imagery analysts",
  "data_point": "4 nuclear sites struck — Fordow penetration uncertain"
}
```

```json
{
  "date": "2026-03-04",
  "time": "08:00",
  "title": "Satellite imagery shows Fordow survived deep strikes",
  "description": "Commercial satellite imagery from Planet Labs and analysis by the Institute for Science and International Security show that while Fordow's surface buildings and tunnel entrances are destroyed, thermal signatures suggest underground centrifuge halls may be partially intact. The site's depth exceeds the penetration capability of existing US bunker busters. Critics call this a 'strategic failure at the war's central objective.'",
  "category": "military",
  "source": "ISIS / Planet Labs / Arms Control Association",
  "data_point": "Fordow underground halls likely survived"
}
```

```json
{
  "date": "2026-03-09",
  "time": "08:00",
  "title": "IAEA loses all monitoring access to Iranian nuclear sites",
  "description": "International Atomic Energy Agency Director General confirms total loss of monitoring and verification access across all Iranian nuclear facilities. Inspectors were evacuated before the strikes. Iran announced withdrawal from the NPT on March 2. IAEA states it 'cannot assess the current status of Iran's nuclear material inventory.' The war intended to prevent an Iranian bomb may have made verification of that goal impossible.",
  "category": "diplomatic",
  "source": "IAEA / Reuters",
  "data_point": "IAEA monitoring access: zero"
}
```

---

## 5. ADD NEW ENTRIES — IRANIAN DRONE OPERATIONS

Iran's massive drone fleet is unmentioned. Insert:

```json
{
  "date": "2026-02-28",
  "time": "20:00",
  "title": "Iran launches Shahed drone swarms at Gulf military bases",
  "description": "IRGC launches waves of Shahed-136 one-way attack drones targeting US and coalition bases in Kuwait, Bahrain, and Qatar. Most are intercepted by Patriot, NASAMS, and CRAM systems. The volume of launches — estimated 150+ in the first 24 hours — strains air defense interceptor stocks.",
  "category": "military",
  "source": "CENTCOM / DoD",
  "data_point": "150+ Shahed drones launched in first 24 hours"
}
```

```json
{
  "date": "2026-03-04",
  "time": "02:00",
  "title": "Drone swarm overwhelms air defenses at Al Udeid, Qatar",
  "description": "A coordinated salvo of 40+ Shahed drones and 5 ballistic missiles targets Al Udeid Air Base in Qatar — the largest US air base in the Middle East. Most are intercepted but 3 drones penetrate defenses and strike the airfield, damaging a KC-135 tanker aircraft. No US fatalities. The incident raises questions about interceptor stockpile sustainability.",
  "category": "military",
  "source": "CENTCOM / AFCENT / Reuters",
  "data_point": "3 drones penetrate Al Udeid defenses"
}
```

```json
{
  "date": "2026-03-09",
  "time": "04:00",
  "title": "US air campaign targets Iranian drone production and storage",
  "description": "In a dedicated strike package, US forces target Iran's drone production infrastructure including facilities in Isfahan, Kermanshah, and a suspected underground Shahed assembly plant near Karaj. Defense Intelligence Agency estimates Iran began the conflict with 3,000+ one-way attack drones in stockpile. An unknown number remain operational despite strikes.",
  "category": "military",
  "source": "DIA / DoD / CENTCOM",
  "data_point": "3,000+ drone pre-war stockpile — remaining unknown"
}
```

---

## 6. ADD NEW ENTRIES — MISSING OIL PRICE TRACKING (Mar 1-6)

Oil prices exist for Feb 28, Mar 7, and Mar 11+. Fill the gap:

```json
{
  "date": "2026-03-01",
  "time": "18:00",
  "title": "Oil surges further as Hormuz closure confirmed",
  "description": "Brent crude closes at $89.20/bbl (+7.2% from yesterday's already elevated close) as markets price in the Strait of Hormuz closure. WTI at $85.40. The combined loss of Iranian exports and Hormuz transit creates a theoretical shortfall of 12+ million barrels per day — the largest supply disruption in oil market history.",
  "category": "financial",
  "source": "ICE / NYMEX / Bloomberg",
  "data_point": "Brent $89.20. WTI $85.40"
}
```

```json
{
  "date": "2026-03-03",
  "time": "16:00",
  "title": "Brent crude hits $91.50 — third straight day of gains",
  "description": "Oil prices continue climbing as Hezbollah's entry and Houthi Red Sea escalation widen the conflict's geographic footprint. Brent closes at $91.50. Saudi Arabia and UAE pledge to increase production from non-Hormuz export terminals but capacity is limited to approximately 2 MBD via pipeline to Red Sea ports.",
  "category": "financial",
  "source": "ICE / OPEC / Bloomberg",
  "data_point": "Brent $91.50. Saudi pledges 2 MBD via alternate routes"
}
```

```json
{
  "date": "2026-03-05",
  "time": "16:00",
  "title": "Oil breaks $95 as conflict shows no signs of de-escalation",
  "description": "Brent closes at $95.30/bbl on the back of continued Hormuz closure, Houthi Red Sea attacks, and depletion of global crude inventories. IEA releases emergency assessment estimating commercial inventories can cover the shortfall for 45-60 days before critical shortages emerge in Asia-Pacific and European markets.",
  "category": "financial",
  "source": "ICE / IEA / Bloomberg",
  "data_point": "Brent $95.30. IEA: 45-60 day inventory runway"
}
```

---

## 7. ADD NEW ENTRIES — MISSING S&P 500 TRACKING

S&P data exists for pre-war, Mar 5, Mar 10, Mar 13. Fill gaps:

```json
{
  "date": "2026-03-01",
  "time": "16:00",
  "title": "S&P 500 drops 3.1% — worst day since 2024",
  "description": "US stock markets sell off sharply as the full scope of Operation Epic Fury becomes clear. S&P 500 closes at 6,654, down 3.1%. Nasdaq falls 3.8% on tech exposure to global supply chains. Defense stocks (Lockheed Martin, Raytheon, Northrop Grumman) surge 8-12%. Airlines plunge 11%.",
  "category": "financial",
  "source": "NYSE / Bloomberg",
  "data_point": "S&P 6,654 (-3.1%)"
}
```

```json
{
  "date": "2026-03-03",
  "time": "16:00",
  "title": "Markets stabilize as investors assess conflict duration",
  "description": "S&P 500 closes at 6,612, down modestly. Markets begin differentiating between sectors — defense and energy surge while airlines, travel, and consumer discretionary continue declining. Gold breaks $4,900/oz as safe-haven demand accelerates.",
  "category": "financial",
  "source": "NYSE / Bloomberg",
  "data_point": "S&P 6,612. Gold $4,900/oz"
}
```

```json
{
  "date": "2026-03-07",
  "time": "16:00",
  "title": "Markets rebound on SPR release and limited ground war signals",
  "description": "S&P 500 recovers to 6,580 as the SPR release announcement and White House confirmation of 'no ground troops' provide modest reassurance. The rebound is driven by short-covering and bargain hunting in oversold tech names. Analysts warn the recovery is fragile and contingent on no further escalation.",
  "category": "financial",
  "source": "NYSE / Bloomberg / Goldman Sachs",
  "data_point": "S&P 6,580 (+4.5% from Mar 5 low)"
}
```

---

## 8. ADD NEW ENTRIES — DIPLOMATIC GAPS

### Saudi Arabia

```json
{
  "date": "2026-03-01",
  "time": "14:00",
  "title": "Saudi Arabia condemns both Iran and US strikes — calls for restraint",
  "description": "Saudi Arabia issues carefully worded statement through the Foreign Ministry condemning 'all acts that threaten regional stability' without naming either party. Riyadh privately grants expanded US basing and overflight rights while publicly maintaining distance. Crown Prince MBS speaks with President Trump and Chinese President Xi on the same day.",
  "category": "diplomatic",
  "source": "Saudi MFA / Reuters / AP",
  "data_point": null
}
```

### India

```json
{
  "date": "2026-03-02",
  "time": "14:00",
  "title": "India scrambles to evacuate 8 million citizens from Gulf states",
  "description": "India launches Operation Kaveri II — a massive diplomatic and logistics effort to prepare evacuation of up to 8 million Indian nationals across Gulf states. Indian Navy deploys three ships to the Arabian Sea. India calls for 'immediate de-escalation' but declines to condemn either side, seeking to maintain its oil supply relationship with both the US and Iran.",
  "category": "diplomatic",
  "source": "Indian MEA / Indian Navy / Reuters",
  "data_point": "8 million Indian nationals in Gulf states"
}
```

### Iraq

```json
{
  "date": "2026-03-01",
  "time": "20:00",
  "title": "Iraq declares neutrality — closes airspace to US combat operations",
  "description": "Iraqi Prime Minister announces Iraq will not be a party to the conflict and orders closure of Iraqi airspace to US combat missions. The order is partially unenforceable as US forces maintain operational control over portions of Iraqi airspace. The declaration creates a legal and diplomatic crisis as US strikes on PMF targets violate the stated neutrality.",
  "category": "diplomatic",
  "source": "Iraqi PM office / AP / Al Jazeera",
  "data_point": null
}
```

### Japan and South Korea

```json
{
  "date": "2026-03-03",
  "time": "10:00",
  "title": "Japan and South Korea announce coordinated SPR releases",
  "description": "Japan and South Korea, both heavily dependent on Persian Gulf oil, announce coordinated Strategic Petroleum Reserve releases of 15 million and 7 million barrels respectively. Both governments support the US position but urge rapid de-escalation. Japan dispatches Maritime Self-Defense Force vessels to support Indian Ocean shipping escort operations.",
  "category": "diplomatic",
  "source": "Japanese PM office / South Korean MFA / Reuters",
  "data_point": "22 million barrels combined SPR release"
}
```

### Oman back-channel

```json
{
  "date": "2026-03-06",
  "time": "10:00",
  "title": "Oman begins quiet shuttle diplomacy between Washington and Tehran",
  "description": "Oman's Sultan Haitham initiates back-channel communications between US and Iranian officials — reprising Oman's traditional mediator role. Swiss Ambassador to Iran (US protecting power) facilitates initial contact. Discussions are preliminary and focused on humanitarian corridors and POW treatment rather than ceasefire terms. Both sides deny talks are taking place.",
  "category": "diplomatic",
  "source": "Diplomatic sources / Omani media / Reuters (sourced anonymously)",
  "data_point": null
}
```

### Turkey pre-missile-incident

```json
{
  "date": "2026-03-02",
  "time": "18:00",
  "title": "Erdogan offers to mediate — condemns US strikes",
  "description": "Turkish President Erdogan condemns the US strikes as 'unilateral aggression that destabilizes the entire region' while simultaneously offering Ankara as a venue for negotiations. Turkey closes its airspace to US combat operations but continues allowing NATO surveillance flights. Turkey's position is complicated by its NATO membership, its economic ties to Iran, and the Kurdish factor.",
  "category": "diplomatic",
  "source": "Turkish MFA / Anadolu Agency / Reuters",
  "data_point": null
}
```

---

## 9. ADD NEW ENTRIES — ISRAELI CASUALTIES AND IRON DOME STRESS

```json
{
  "date": "2026-03-02",
  "time": "16:00",
  "title": "3 Israeli civilians killed in Hezbollah rocket barrage on Haifa",
  "description": "Three Israeli civilians killed and 22 wounded when a Hezbollah rocket barrage overwhelms Iron Dome coverage over Haifa. The volume of simultaneous launches — 200+ in a 10-minute window targeting northern Israel — exceeds the system's engagement capacity in the Haifa sector. IDF calls up additional reserve battalions.",
  "category": "military",
  "source": "IDF / Israeli emergency services / Haaretz",
  "data_point": "3 Israeli civilians KIA, 22 wounded"
}
```

```json
{
  "date": "2026-03-06",
  "time": "22:00",
  "title": "Iron Dome interceptor stockpile concerns emerge",
  "description": "Israeli media reports the IDF has expended over 1,500 Iron Dome and David's Sling interceptors in the first week of conflict — a rate that strains production capacity. The US expedites delivery of Tamir interceptors from existing stocks. A senior IDF officer warns off-record that at current rates, 'we have weeks, not months' of interceptor supply for the northern front.",
  "category": "military",
  "source": "IDF (background briefing) / Haaretz / Times of Israel",
  "data_point": "1,500+ interceptors expended in 7 days"
}
```

---

## 10. ADD NEW ENTRIES — HUMANITARIAN RUNNING TOTALS

```json
{
  "date": "2026-03-06",
  "time": "14:00",
  "title": "Iranian civilian death toll estimated at 400+",
  "description": "Iranian Red Crescent and state media report over 400 civilian deaths from US and Israeli strikes in the first week. Independent verification is impossible due to media access restrictions. Iran claims the number is significantly higher. Pentagon states all targets are military or dual-use and that civilian casualties are 'deeply regretted but not the objective.'",
  "category": "humanitarian",
  "source": "Iranian Red Crescent / IRNA / DoD",
  "data_point": "400+ Iranian civilian deaths (Iranian figures)"
}
```

```json
{
  "date": "2026-03-10",
  "time": "10:00",
  "title": "Iranian infrastructure damage assessment — power, water, fuel",
  "description": "The ICRC reports significant damage to Iranian civilian infrastructure including power generation (30-40% of national grid offline in western Iran), water treatment disruption in Ahvaz and Kermanshah, and fuel shortages as refinery capacity is degraded. Hospitals are operating on backup generators. Iran's road and rail network is severely disrupted by strikes on bridges and logistics hubs.",
  "category": "humanitarian",
  "source": "ICRC / OCHA / Iranian Red Crescent",
  "data_point": "30-40% of western Iran power grid offline"
}
```

```json
{
  "date": "2026-03-12",
  "time": "20:00",
  "title": "Iranian civilian toll rises past 800 — refugee flows to Turkey and Iraq begin",
  "description": "Iranian authorities report over 800 civilian deaths. UNHCR reports early refugee flows — approximately 15,000 Iranians have crossed into Turkey's Van Province and an estimated 8,000 into Iraqi Kurdistan. Turkey warns it cannot absorb a mass displacement event and begins reinforcing its eastern border.",
  "category": "humanitarian",
  "source": "UNHCR / Turkish Interior Ministry / IRNA",
  "data_point": "800+ Iranian civilian dead. 23,000+ refugees"
}
```

---

## 11. ADD NEW ENTRIES — US DOMESTIC

### Polling

```json
{
  "date": "2026-03-05",
  "time": "12:00",
  "title": "First polls show narrow majority supports strikes — but opposition to ground war",
  "description": "An NBC/WSJ flash poll shows 54% of Americans support the initial strikes on Iran's nuclear facilities, but 71% oppose any ground invasion. Support breaks sharply along partisan lines — 82% of Republicans approve vs. 31% of Democrats. The school strike in Minab has not yet been widely covered at the time of polling.",
  "category": "domestic",
  "source": "NBC News / Wall Street Journal",
  "data_point": "54% approve strikes, 71% oppose ground war"
}
```

### Protest escalation

```json
{
  "date": "2026-03-08",
  "time": "14:00",
  "title": "US anti-war protests grow — 500,000 march in Washington",
  "description": "The largest US anti-war demonstration since 2003 draws an estimated 500,000 people to the National Mall in Washington, D.C. Simultaneous protests in 120+ US cities. The Minab school strike images have become the defining visual of the anti-war movement. Counter-protests supporting the troops draw smaller but vocal crowds in several cities.",
  "category": "domestic",
  "source": "AP / National Park Service estimate / Reuters",
  "data_point": "500,000 in D.C. — largest since 2003"
}
```

### Consumer impact

```json
{
  "date": "2026-03-10",
  "time": "16:00",
  "title": "University of Michigan consumer sentiment plunges",
  "description": "University of Michigan preliminary consumer sentiment index drops to 62.1, down from 71.8 — the steepest single-period decline since March 2020. The decline is driven by expectations of higher gas and grocery prices. Americans cite the war as the primary reason for economic pessimism. Grocery chains begin implementing 5-8% price increases on imported goods.",
  "category": "financial",
  "source": "University of Michigan / Reuters / CNBC",
  "data_point": "Consumer sentiment 62.1, down from 71.8"
}
```

---

## 12. ADD NEW ENTRIES — US FORCE POSTURE AND AIR CAMPAIGN

```json
{
  "date": "2026-02-28",
  "time": "04:00",
  "title": "B-2 Spirits lead opening strikes on hardened targets",
  "description": "B-2 Spirit stealth bombers flying from Whiteman AFB, Missouri deliver GBU-57 Massive Ordnance Penetrators on Fordow and other hardened nuclear sites. B-52Hs operating from Diego Garcia and Al Udeid launch cruise missile salvos at IRGC command centers. The air campaign involves assets from 3 carrier strike groups, multiple bomber wings, and F-35s operating from Gulf bases.",
  "category": "military",
  "source": "AFCENT / DoD",
  "data_point": "3 carrier strike groups, B-2 and B-52 wings deployed"
}
```

```json
{
  "date": "2026-03-01",
  "time": "12:00",
  "title": "Iran's integrated air defense network assessed as suppressed",
  "description": "CENTCOM assesses Iran's integrated air defense system as effectively suppressed after 48 hours. S-300PMU-2 batteries at Isfahan and Tehran are confirmed destroyed. Indigenous Bavar-373 systems engaged but failed to intercept US stealth aircraft. Iranian Air Force F-14 fleet did not launch; their Mehrabad hangars were struck on Day 1. Remaining mobile SAMs and MANPADS continue to pose threats to non-stealth aircraft.",
  "category": "military",
  "source": "CENTCOM / AFCENT / DIA",
  "data_point": "Iranian IADS suppressed within 48 hours"
}
```

---

## 13. ADD NEW ENTRIES — FINANCIAL GAPS

### Bond and dollar

```json
{
  "date": "2026-03-01",
  "time": "14:00",
  "title": "Treasury yields plunge as investors flee to safety",
  "description": "10-year US Treasury yield drops 28 basis points to 3.92% as global investors flood into US government bonds. The dollar index (DXY) surges 2.1% to 107.8 on safe-haven demand. Gold spikes to $4,850/oz. The flight to safety is the largest single-day move since the early days of COVID-19.",
  "category": "financial",
  "source": "US Treasury / Bloomberg / Reuters",
  "data_point": "10Y yield 3.92% (-28bps). DXY 107.8 (+2.1%). Gold $4,850"
}
```

### Supply chain

```json
{
  "date": "2026-03-09",
  "time": "12:00",
  "title": "Global supply chain disruption spreads beyond energy",
  "description": "Disruption from Hormuz closure and Red Sea rerouting cascades beyond energy markets. Petrochemical feedstock shortages force production cuts at European chemical plants. Semiconductor-grade neon (produced partly in the Middle East supply chain) faces spot shortages. The Baltic Dry Index spikes 35% as available shipping capacity is absorbed by longer routes. Auto manufacturers warn of production slowdowns within 2-3 weeks.",
  "category": "financial",
  "source": "Bloomberg / Baltic Exchange / Reuters",
  "data_point": "Baltic Dry Index +35%"
}
```

---

## 14. FIX EXISTING DATA CONSISTENCY ISSUES

### Fix 1: US KIA tracking — add the missing 7th death

Insert this entry to explain the gap between 6 KIA (Feb 28) and 8 KIA (Mar 11):

```json
{
  "date": "2026-03-06",
  "time": "16:00",
  "title": "7th US service member killed — drone attack in Syria",
  "description": "A US Army soldier is killed by a one-way attack drone at a patrol base in northeastern Syria. The drone, attributed to an Iranian-aligned militia, struck a housing unit. This is the 7th US combat death of the conflict and the first outside the Persian Gulf theater.",
  "category": "military",
  "source": "CENTCOM / DoD",
  "data_point": "7 US KIA total"
}
```

### Fix 2: Mar 10 summary entry — S&P rebound is unexplained

The Mar 10 entry has S&P at 6,694 (rebounded from 6,297 on Mar 5). Update the Mar 10 entry's description to include this line:

> Current `description` starts with: "Strikes continue across Iran..."

**Replace** the existing Mar 10 entry description with:

```
"Strikes continue across Iran. Hezbollah front intensifies. Oil at $101.50. S&P 500 recovers to 6,694 — rebounding 6.3% from last week's 6,297 low on SPR release, no-ground-war pledges, and short-covering. Markets remain 2.5% below pre-war 6,867. VIX holds above 25. Gas national average at $3.48 and climbing. Estimated US operational cost: $500M/day."
```

### Fix 3: Update Mar 11 US KIA entry to cross-reference the 7th death

The existing Mar 11 entry about the 8th death says "an eighth US service member has died from injuries sustained during an Iranian missile attack on US troops stationed in Saudi Arabia on March 1." This is fine but now correctly follows the 7th KIA entry.

No change needed — just verify the 7th death entry (added above) is placed before this chronologically.

---

## 15. ADD CUMULATIVE TRACKER ENTRIES

Add a "summary" style entry at the end of each week to serve as running scorecards:

```json
{
  "date": "2026-03-07",
  "time": "23:59",
  "title": "Week 1 summary — Operation Epic Fury by the numbers",
  "description": "After 7 days: 3,000+ targets struck in Iran. Kharg Island, Natanz, Isfahan, Arak confirmed destroyed. Fordow status uncertain. Strait of Hormuz closed. Hezbollah and Houthi fronts active. 7 US KIA. 3 Israeli civilians killed. 400+ Iranian civilian dead (unverified). 450,000 displaced in Lebanon. Oil at $101.50/bbl. S&P 500 at 6,580 (-4.2%). Gas $3.38/gal (+10.8%). Gold $4,980/oz.",
  "category": "military",
  "source": "Multiple — compiled",
  "data_point": "Week 1 cumulative"
}
```

---

## 16. FINAL INSTRUCTIONS

1. **Merge all new entries** into the existing JSON array
2. **Sort the entire array** by `date` (ascending), then `time` (ascending) as a secondary sort
3. **Validate every entry** has all required fields: `date`, `time`, `title`, `description`, `category`, `source`, `data_point`
4. **Ensure no duplicate entries** — if a new entry covers the same event as an existing one, keep the more detailed version
5. **Apply the Fix 2 edit** to the existing Mar 10 entry (description replacement)
6. **Count final entries** — the original has 43 entries. This update adds approximately 35 new entries. Final count should be approximately 78.
7. **Output as valid JSON** — array of objects, properly escaped strings, no trailing commas
8. **Preserve exact spelling and formatting** of existing entries that are not being modified

### Category distribution target (approximate):
- `military`: ~30-35 entries
- `financial`: ~18-22 entries
- `diplomatic`: ~10-12 entries
- `humanitarian`: ~6-8 entries
- `domestic`: ~5-6 entries
- `cyber`: ~4 entries

### Quality check:
After generating, verify:
- [ ] Every day from Feb 28 through Mar 13 has at least 2 entries
- [ ] Oil price data exists for: Feb 28, Mar 1, Mar 3, Mar 5, Mar 7, Mar 10, Mar 11, Mar 12, Mar 13
- [ ] S&P 500 data exists for: Mar 1, Mar 3, Mar 5, Mar 7, Mar 10, Mar 13
- [ ] US KIA progression: 6 → 7 → 8 with each death logged
- [ ] Iraqi militia thread has entries on: Feb 28, Mar 2, Mar 5, Mar 8, Mar 11
- [ ] Houthi thread has entries on: Mar 1, Mar 3, Mar 5, Mar 8, Mar 10, Mar 13
- [ ] Cyber thread has entries on: Feb 28, Mar 3, Mar 7, Mar 12
- [ ] Nuclear BDA has entries on: Mar 1, Mar 4, Mar 9
- [ ] Iranian civilian casualty totals appear on: Mar 6, Mar 10, Mar 12
- [ ] Gas price progression is monotonically increasing day over day
