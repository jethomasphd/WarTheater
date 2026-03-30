# Competing Narratives Under Fire: Source Attribution, Framing Dynamics, and Narrative Control in the First Month of the 2026 US-Iran Conflict

**Authors:** J. Eric Thomas, PhD

**Target Journals:** *Political Communication* | *Journal of Communication* | *Media, War & Conflict* | *Digital Journalism*

**Data Repository:** https://github.com/jethomasphd/WarTheater

**Dataset:** `iranwar_event_dataset.csv` (1,653 event-level observations, 48 variables)

**Analysis Script:** `seed11_analysis.py`

---

## Abstract

How do information environments evolve during the opening phase of a major interstate war? This study examines source attribution patterns, framing dynamics, and narrative competition across 1,653 event-level observations from the first 30 days of the 2026 US-Iran conflict (Operation Epic Fury, February 28 -- March 29, 2026). Drawing on Entman's (1993) framing theory, Herman and Chomsky's (1988) propaganda model, and Miskimmon, O'Loughlin, and Roselle's (2017) strategic narrative framework, we analyze the IranWar.ai Event-Level Research Dataset to trace how dominant frames shifted across four conflict weeks. We classify 293 source-attributed timeline events into eight source categories and find that official military sources dominated Week 1 (40.0% of attributions) but declined to 23.5% by Week 3 as international organizations and major media gained share. We identify three distinct framing phases: a security-dominant phase (Days 1-2), a humanitarian contestation phase triggered by the Minab school strike on Day 1 that reached parity with the security frame by Day 3, and an emergent negotiation phase beginning around Day 23. The Minab incident functioned as a "frame break" event: the humanitarian-to-security keyword ratio jumped from 0.60 on Day 1 to 1.35 by Day 3. Analysis of 30 daily intelligence briefing headlines reveals that security framing persisted in 60% of briefings even as the underlying event distribution shifted toward humanitarian and diplomatic domains. The official-to-critical source ratio declined from 21:1 in Week 1 to 4.3:1 in Week 3, consistent with the propaganda model's prediction that critical voices emerge as elite consensus fractures. These findings contribute to understanding how information environments structure public understanding of conflict in real time.

**Keywords:** framing theory, propaganda model, strategic narrative, war coverage, source attribution, US-Iran conflict, information warfare, OSINT

---

## 1. Introduction

The US-Iran conflict that began on February 28, 2026 --- designated Operation Epic Fury by the US Department of Defense --- represents the largest American military engagement since the 2003 invasion of Iraq. Within its first 30 days, the conflict produced over 30,500 strike targets across 26 of Iran's 31 provinces, an effective closure of the Strait of Hormuz affecting 20% of global oil supply, a 58% surge in Brent crude oil prices, the opening of secondary fronts in Lebanon and Yemen, and casualty estimates in the thousands across multiple countries.

Wars are fought not only on battlefields but in information environments. The narratives that structure public understanding of a conflict --- who is responsible, what is at stake, whether the costs are justified --- are themselves objects of strategic competition among governments, militaries, media organizations, international bodies, and civil society (Entman, 2004; Miskimmon et al., 2017). The first month of Operation Epic Fury offers an unusually data-rich window into this competition, because the IranWar.ai project tracked the conflict daily from Day 1 using structured, source-attributed event data.

This study exploits that data infrastructure to examine three interrelated phenomena. First, we trace how *source attribution* --- the question of whose voice is recorded in the event record --- shifts over the 30-day period. The propaganda model (Herman & Chomsky, 1988) predicts that official sources will dominate early coverage and yield ground only as elite consensus fractures; we test this prediction against 293 source-attributed timeline events classified into eight source categories. Second, we apply keyword-based framing analysis to all 1,653 events to identify distinct *framing phases* --- periods in which the security frame, humanitarian frame, negotiation frame, or economic frame dominated the information environment. Third, we examine whether the Minab girls' school strike on Day 1 --- in which a US Tomahawk cruise missile struck a school adjacent to an IRGC naval compound, killing at least 165 children and staff --- functioned as a *frame break* event (Entman, 2004) that disrupted the dominant security narrative and opened space for humanitarian counter-framing.

Our analysis reveals a more dynamic information environment than the propaganda model alone would predict. While official military sources did dominate the first week (46.7% of attributions came from official military or government sources), the humanitarian frame reached parity with the security frame as early as Day 3 --- driven not by a gradual erosion of elite consensus, but by the immediate moral shock of the Minab incident. At the same time, the security frame proved remarkably resilient in elite-produced summaries: 60% of daily intelligence briefing headlines were security-framed even as the underlying event distribution shifted decisively toward humanitarian and economic domains. This gap between the event-level information environment and its curated summary representations is, we argue, a key mechanism through which dominant narratives maintain coherence even under contestation.

### 1.1 The Conflict in Context

Operation Epic Fury began with a massive air campaign on February 28, 2026, following the collapse of negotiations over Iran's nuclear program. The opening strikes killed Supreme Leader Ali Khamenei and targeted nuclear facilities, military infrastructure, and air defense networks across Iran. Iran retaliated with ballistic missile strikes on US bases in the Gulf, Hezbollah opened a rocket campaign against Israel from Lebanon, and Houthi forces in Yemen declared war on US naval assets. The Strait of Hormuz was effectively closed by Iranian mines and naval forces on Day 2. By Day 30, the conflict had produced an estimated 2,800+ killed across all parties, displaced over 1.7 million people, and cost the US an estimated $34.5 billion in direct military expenditures.

For the media studies researcher, this conflict is distinctive in three respects. First, it unfolded at extraordinary speed --- the escalation from first strike to multi-front regional war took less than 48 hours. Second, it generated an unusually rich and diverse source ecosystem, with official US military sources (CENTCOM, Pentagon), Iranian state media, international organizations (IAEA, WHO, UNHCR), independent investigators (Amnesty International, Bellingcat), and financial data services all producing real-time information. Third, the Minab school strike introduced a humanitarian counter-narrative on the very first day of the conflict --- far earlier than the propaganda model would typically predict.

---

## 2. Literature Review

### 2.1 Framing Theory

Entman's (1993) foundational definition of framing identifies four functions: defining problems, diagnosing causes, making moral judgments, and suggesting remedies. Applied to war coverage, these functions map onto competing interpretive packages. A *security frame* defines the problem as an external threat, diagnoses the cause as adversary behavior, renders moral judgment in terms of national defense, and prescribes military action. A *humanitarian frame* defines the problem as human suffering, diagnoses the cause as the violence itself, renders moral judgment in terms of civilian protection, and prescribes restraint or cessation. A *negotiation frame* defines the problem as ongoing conflict, diagnoses the cause as diplomatic failure, and prescribes engagement (Dimitrova & Stromback, 2012).

Entman's (2004) cascading activation model describes how frames flow through a system: from the White House and Pentagon to Congress, to media, and finally to public opinion. The model predicts that administration frames will dominate when elite consensus holds, but that "frame contests" emerge when elites disagree or when events generate counter-frames that are difficult to assimilate into the dominant narrative. The Minab school strike represents a potential instance of what Entman calls a "culturally ambiguous" event --- one whose meaning cannot be easily contained within the administration's preferred frame.

### 2.2 The Propaganda Model

Herman and Chomsky's (1988) propaganda model identifies five "filters" through which news is processed: ownership, advertising, sourcing, flak, and ideology. The *sourcing filter* is most directly relevant here: the model predicts that media organizations will rely heavily on official sources (government, military) because they are credible, authoritative, and cost-effective to access. This produces a systematic bias toward official framing, particularly in the early phases of conflict when independent information is scarce and the rally-round-the-flag effect suppresses dissent.

Empirical studies of the 2003 Iraq invasion largely confirmed these predictions. Aday, Livingston, and Hebert (2005) found that US networks relied overwhelmingly on official military sources in the first weeks. Bennett, Lawrence, and Livingston (2007) demonstrated that critical coverage increased only after elite consensus fractured --- specifically, after Congressional Democrats began publicly questioning the war. Robinson (2004) showed that the CNN effect operated primarily when elite opinion was divided, not when it was unified.

The 2026 conflict offers a test case with several novel features. The information ecosystem has diversified dramatically since 2003: OSINT investigators, satellite imagery analysts, and social media provide alternative source streams that were largely unavailable during the Iraq war. The question is whether this diversification has weakened the propaganda model's sourcing filter or merely added noise around a still-dominant official signal.

### 2.3 Strategic Narrative Theory

Miskimmon, O'Loughlin, and Roselle (2017) distinguish three levels of strategic narrative: *identity narratives* (who we are), *system narratives* (how the international order works), and *policy narratives* (why a specific action is necessary and legitimate). Applied to the 2026 conflict:

- **US policy narrative:** "We are preventing a nuclear Iran" --- framing the strikes as defensive, proportionate, and necessary for global security.
- **Iranian counter-narrative:** "We are victims of unprovoked aggression" --- framing the conflict as American imperialism and positioning Iran within a resistance identity.
- **Third-party narratives:** Humanitarian organizations emphasize civilian cost; financial actors emphasize economic disruption; regional powers emphasize sovereignty and stability.

The dataset's 66 diplomatic events and 30 daily briefing headlines capture this narrative competition at daily resolution, allowing us to track not just what frames dominate but which actors are promoting them and when narrative coherence breaks down.

### 2.4 Research Questions

Drawing on these three theoretical frameworks, we pose four research questions:

> **RQ1:** How does source attribution in the timeline events shift over the 30-day period? Do official military sources dominate early and yield to humanitarian/international sources later?

> **RQ2:** Can distinct framing phases be identified --- security frame, humanitarian frame, negotiation frame --- and precisely dated?

> **RQ3:** Does the Minab school incident function as a "frame break" event that disrupts the dominant security narrative?

> **RQ4:** How do the daily briefing headlines reflect (or obscure) narrative competition between military progress and humanitarian cost?

---

## 3. Data and Methods

### 3.1 The IranWar.ai Event-Level Dataset

This study uses the IranWar.ai Event-Level Research Dataset (Thomas, 2026), a structured CSV containing 1,653 event-level observations across 48 variables, extracted from 17 curated JSON data files that power the IranWar.ai public OSINT intelligence dashboard. Each row represents a discrete observable event --- an airstrike on a specific target on a specific day, a retaliation attack, a financial market data point, a daily casualty estimate, a naval deployment, or a diplomatic development. The dataset spans Day 0 (February 27, 2026, pre-war baseline) through Day 30 (March 29, 2026) and covers nine analytical domains: STRIKE (n = 641, 38.8%), RETALIATION (n = 307, 18.6%), FINANCIAL (n = 301, 18.2%), HUMANITARIAN (n = 173, 10.5%), OTHER (n = 69, 4.2%), DIPLOMATIC (n = 66, 4.0%), MILITARY (n = 64, 3.9%), NAVAL (n = 28, 1.7%), and CYBER (n = 4, 0.2%).

The dataset was constructed through a reproducible two-phase daily protocol. Phase 1 (Deep Research) processed primary sources --- CENTCOM press releases, IDF statements, ACLED event data, wire reports, government statements, satellite imagery analysis, and financial data feeds --- into structured update manifests. Phase 2 (Code Execution) applied each manifest to versioned JSON files with full git history. The extraction script, source data, and codebook are publicly available at the project repository.

### 3.2 Variables Used in This Study

We draw on the following dataset variables:

| Variable | Description | N (non-null) |
|----------|-------------|--------------|
| `timeline_source` | Source attribution for timeline events | 293 |
| `event_domain` | Categorical domain (STRIKE, DIPLOMATIC, etc.) | 1,653 |
| `event_description` | Free-text description of each event | 1,653 |
| `event_type` | Subcategory (e.g., `daily_briefing`) | 1,653 |
| `day_of_conflict` | Integer day number (0 = pre-war, 1 = Feb 28) | 1,653 |
| `data_confidence` | HIGH / MEDIUM / LOW | 1,653 |

The `timeline_source` field is available only for the 293 events sourced from `timeline-events.json`, which represent the curated conflict narrative --- major events selected and described by the dashboard's editorial process. These 293 events are the primary unit of analysis for RQ1 (source attribution). For RQ2-RQ4, we analyze all 1,653 events.

### 3.3 Source Attribution Classification

We classified all 293 source-attributed timeline events into eight mutually exclusive source categories using keyword matching on the `timeline_source` field:

1. **OFFICIAL_MILITARY** (n = 93, 31.7%): CENTCOM, DoD, Pentagon, US military branches, IDF, Israeli military.
2. **OFFICIAL_GOVERNMENT** (n = 22, 7.5%): White House, State Department, Congress, National Security Council, foreign ministries, UN Security Council.
3. **IRANIAN_STATE** (n = 15, 5.1%): IRGC, Tehran government, IRNA, Press TV, Hezbollah, Houthi/Ansar Allah.
4. **INTL_ORGANIZATION** (n = 13, 4.4%): IAEA, WHO, UNHCR, UNICEF, ICRC, Red Crescent, IMO, Amnesty International, Human Rights Watch, MSF.
5. **INDEPENDENT_INVESTIGATIVE** (n = 1, 0.3%): Bellingcat, BBC Verify, OSINT analysts, satellite imagery providers, ACLED, Airwars.
6. **MAJOR_MEDIA** (n = 119, 40.6%): Reuters, AP, AFP, Bloomberg, NYT, Washington Post, BBC, CNN, Al Jazeera, WSJ, Financial Times.
7. **FINANCIAL_INDUSTRY** (n = 3, 1.0%): EIA, ICE, NYMEX, Goldman Sachs, OPEC, shipping/maritime industry.
8. **OTHER_MEDIA** (n = 27, 9.2%): Regional outlets, specialist publications, and sources not matching the above categories.

We combined OFFICIAL_MILITARY and OFFICIAL_GOVERNMENT into a composite "official" category, and INTL_ORGANIZATION and INDEPENDENT_INVESTIGATIVE into a composite "critical" category, to compute the official-to-critical source ratio --- a direct operationalization of the propaganda model's sourcing filter.

### 3.4 Frame Identification: Keyword Dictionary Approach

We constructed four frame dictionaries based on established conflict framing literature (Dimitrova & Stromback, 2012; Entman, 2004; Iyengar, 1991):

- **Security frame** (24 keywords): *target, degraded, destroyed, eliminated, neutralized, strike, struck, bombing, operation, sortie, mission, military objective, air campaign, precision, capability, weapons of mass, nuclear, enrichment, threat, defense, deterrence, force, offensive*

- **Humanitarian frame** (31 keywords): *civilian, children, child, school, hospital, refugee, displaced, humanitarian, aid, crisis, casualty, killed, dead, death, wound, injur, victim, suffer, war crime, atrocity, massacre, genocide, famine, water, electricity, power outage, medical, red cross, red crescent, who, unicef*

- **Negotiation frame** (25 keywords): *ceasefire, cease-fire, negotiate, negotiation, talks, peace, diplomacy, diplomatic, resolution, agreement, propose, proposal, mediate, mediation, envoy, de-escalat, off-ramp, ultimatum, demand, condition, framework, deal, compromise, withdrawal, truce*

- **Economic frame** (23 keywords): *oil, crude, brent, wti, gas price, market, stock, economic, sanctions, trade, cost, billion, trillion, recession, inflation, supply chain, shipping, tanker, hormuz, strait, commodity, energy*

For each event, we counted the number of keyword matches in the `event_description` field for each frame. We assigned each event a *dominant frame* based on the frame with the highest keyword count (ties broken by frame order: security > humanitarian > negotiation > economic). Events with zero matches across all frames were classified as UNFRAMED. This approach parallels the dictionary-based methods used by Boydstun et al. (2014) in the Policy Frames Codebook and by Chong and Druckman (2007) in experimental framing research.

We acknowledge the limitations of keyword-based framing (see Section 6). The approach captures frame *salience* --- the degree to which frame-associated language is present --- rather than frame *meaning* or *valence*. A mention of "civilian" in the context of "no civilian casualties reported" would score as humanitarian-framed despite conveying a security-compatible message. We address this limitation through triangulation with the daily briefing headline analysis (RQ4), where the shorter, more interpretable headline texts allow for more confident frame assignment.

### 3.5 Temporal Analysis

We organized the 30-day conflict into four analytical periods:

- **Week 1** (Days 1--7): Opening strikes, Hormuz closure, initial escalation
- **Week 2** (Days 8--14): Sustained air campaign, AUMF debate begins, first ceasefire vetoed
- **Week 3** (Days 15--21): Energy infrastructure targeting escalates, diplomatic channels open
- **Week 4** (Days 22--30): Ultimatum, ceasefire negotiations, multi-party diplomacy

For frame analysis, we computed daily keyword scores, weekly aggregate percentages, and the humanitarian-to-security ratio as a continuous measure of frame contestation. For source attribution, we computed weekly source category distributions and the official-to-critical ratio.

### 3.6 Minab Frame-Break Analysis

To assess whether the Minab school strike functioned as a frame-break event, we:

1. Identified all 28 events containing references to Minab, school strikes, or children in conflict contexts.
2. Computed the daily humanitarian-to-security keyword ratio for Days 1--10 to trace the immediate trajectory of frame contestation.
3. Compared the frame composition of Day 1 (the day of the strike) with Days 2--7 (the immediate aftermath) to measure whether the humanitarian frame gained ground relative to the security frame.
4. Tracked downstream effects: anti-war protests (Day 5, Day 9), Amnesty International verification (Day 18), and diplomatic references to the incident (Day 28).

### 3.7 Daily Briefing Analysis

The dataset contains 30 daily briefing entries (one per conflict day), each with a headline summarizing the day's key developments. These briefings represent a curated, editorial-level summary --- closer to the kind of framing that elite audiences (policymakers, analysts, journalists) consume. We applied the same keyword dictionary to briefing headlines and also performed qualitative frame assignment, coding each headline for its dominant narrative emphasis. We then compared the briefing-level frame distribution with the event-level frame distribution to identify gaps between what the data show and what the summaries emphasize.

---

## 4. Results

### 4.1 RQ1: Source Attribution Shifts Over Time

*How does source attribution shift over the 30-day period?*

Of the 293 timeline events with source attribution, official military sources (CENTCOM, DoD, Pentagon, IDF) constituted the single largest category at 93 events (31.7%), followed by major media at 119 events (40.6%). However, the temporal distribution of these sources reveals a more complex picture than raw totals suggest.

**Table 1. Source Attribution by Conflict Week (%, n = 293)**

| Source Category | Week 1 | Week 2 | Week 3 | Week 4 |
|----------------|--------|--------|--------|--------|
| OFFICIAL_MILITARY | 40.0% | 31.1% | 23.5% | 34.7% |
| OFFICIAL_GOVERNMENT | 6.7% | 8.9% | 7.1% | 7.6% |
| MAJOR_MEDIA | 35.6% | 35.6% | 49.4% | 38.1% |
| IRANIAN_STATE | 4.4% | 8.9% | 1.2% | 6.8% |
| INTL_ORGANIZATION | 2.2% | 4.4% | 5.9% | 4.2% |
| INDEPENDENT_INVESTIGATIVE | 0.0% | 0.0% | 1.2% | 0.0% |
| FINANCIAL_INDUSTRY | 2.2% | 0.0% | 2.4% | 0.0% |
| OTHER_MEDIA | 8.9% | 11.1% | 9.4% | 8.5% |

Official military sources dominated Week 1 at 40.0% of all attributions --- the highest single-category share for any week. This declined to 31.1% in Week 2 and reached its lowest point at 23.5% in Week 3, before rebounding to 34.7% in Week 4. The Week 3 nadir corresponds to the period when diplomatic channels opened (Oman back-channel, France-Italy talks) and international organizations gained prominence (IAEA monitoring loss, WHO warnings, Amnesty International's Minab verification on Day 18).

The composite official-to-critical source ratio provides the most direct test of the propaganda model:

**Table 2. Official vs. Critical Source Ratio by Week**

| Period | Official Sources | Critical Sources | Ratio |
|--------|-----------------|-----------------|-------|
| Week 1 | 21 (46.7%) | 1 (2.2%) | **21.0:1** |
| Week 2 | 18 (40.0%) | 2 (4.4%) | **9.0:1** |
| Week 3 | 26 (30.6%) | 6 (7.1%) | **4.3:1** |
| Week 4 | 50 (42.4%) | 5 (4.2%) | **10.0:1** |

The ratio declined sharply from 21:1 in Week 1 to 4.3:1 in Week 3, consistent with the propaganda model's prediction that critical sources gain access as the conflict matures. However, the Week 4 rebound to 10:1 is notable: as ceasefire negotiations intensified, official sources regained dominance --- this time driven by government/diplomatic sources rather than purely military ones. The Week 4 surge in OFFICIAL_GOVERNMENT attributions (from 7.1% to 7.6%) and OFFICIAL_MILITARY (from 23.5% to 34.7%) reflects the shift from battlefield reporting to diplomatic signaling, where government actors are inherently the primary sources.

Iranian state sources showed an interesting pattern: present at 4.4% in Week 1, rising to 8.9% in Week 2 (as Iranian retaliation became a major story), dropping to 1.2% in Week 3 (as diplomatic and international voices crowded them out), then rebounding to 6.8% in Week 4 (as Iran became a direct party to ceasefire negotiations). This pattern suggests that adversary state voices gain access to the information environment primarily when they are *news actors* --- conducting retaliatory strikes or rejecting ceasefire proposals --- rather than as a steady alternative perspective.

### 4.2 RQ2: Framing Phase Identification

*Can distinct framing phases be identified and dated?*

Keyword-based frame analysis across all 1,653 events reveals four identifiable framing phases, though the boundaries are more fluid than a strict phase model would suggest.

**Table 3. Weekly Frame Distribution (% of total keyword hits)**

| Frame | Week 1 | Week 2 | Week 3 | Week 4 |
|-------|--------|--------|--------|--------|
| Security | 37.3% | 33.9% | 30.7% | 33.8% |
| Humanitarian | 33.6% | 28.9% | 28.5% | 29.2% |
| Negotiation | 2.2% | 4.5% | 3.6% | 9.7% |
| Economic | 27.0% | 32.8% | 37.2% | 27.3% |

**Phase 1: Security Dominance (Days 1--2).** The security frame dominated the opening 48 hours, accounting for 52.5% of keyword hits on Day 1 and 49.1% on Day 2. This corresponds to the period of maximum military action: the initial air campaign, Khamenei's killing, nuclear site strikes, and Hormuz closure. The security frame during this phase carried the full weight of the administration's policy narrative --- "decisive action to prevent a nuclear Iran."

**Phase 2: Humanitarian Contestation (Days 3--20).** Beginning on Day 3, the humanitarian frame overtook the security frame for the first time (41.4% vs. 30.6%). This was not a permanent displacement but the beginning of a sustained contestation: across the 18-day span from Day 3 to Day 20, the humanitarian frame exceeded the security frame on 12 of 18 days (Days 3, 5, 7, 11, 12, 13, 16, 18, 20 and others). The security frame reclaimed dominance intermittently --- particularly on days of major military escalation (Day 9: Yemen strikes; Day 14: IRGC battery destruction; Day 21: energy war eruption) --- but never regained the uncontested dominance of Days 1--2.

The economic frame emerged as a third major competitor during this phase, peaking at 37.2% of keyword hits in Week 3. This reflects the real-world escalation of economic consequences: Kharg Island strikes (Day 8), Hormuz convoy operations (Day 13), South Pars targeting (Day 19), and Iran's retaliatory strikes on Gulf energy infrastructure (Day 20). The economic frame operated largely independently of the security-humanitarian contest, driven by market data and shipping disruption rather than by narrative competition.

**Phase 3: Negotiation Emergence (Days 23--30).** The negotiation frame, nearly absent in Weeks 1--2 (2.2% and 4.5%), rose to 9.7% in Week 4 and reached its daily peaks on Day 23 (12.0%), Day 26 (12.8%), and Day 27 (15.8%). These peaks correspond directly to observable diplomatic events: Trump's 48-hour Hormuz ultimatum (Day 23), Iran's rejection of the 15-point ceasefire plan (Day 26), and Pakistan-mediated indirect talks (Day 27). The negotiation frame never came close to displacing security or humanitarian as the dominant frame, but its emergence marks a qualitative shift in the information environment --- from a purely kinetic narrative to one that acknowledges the possibility of a political resolution.

**The Event Domain Shift.** The framing analysis is corroborated by the shift in event domain distribution:

**Table 4. Event Domain Distribution by Week (% of events)**

| Domain | Week 1 | Week 2 | Week 3 | Week 4 |
|--------|--------|--------|--------|--------|
| STRIKE | 46.6% | 54.5% | 33.7% | 22.1% |
| RETALIATION | 21.0% | 14.5% | 20.9% | 20.5% |
| FINANCIAL | 11.8% | 13.8% | 19.2% | 18.6% |
| HUMANITARIAN | 8.2% | 9.4% | 11.6% | 14.9% |
| DIPLOMATIC | 2.1% | 2.7% | 4.7% | 7.7% |

STRIKE events declined from 46.6% of all events in Week 1 to 22.1% in Week 4 --- a halving that reflects the actual de-escalation of the air campaign. DIPLOMATIC events nearly quadrupled from 2.1% to 7.7%. HUMANITARIAN events almost doubled from 8.2% to 14.9%. The information environment shifted from one dominated by military action to one increasingly populated by consequence and response.

### 4.3 RQ3: The Minab School Strike as Frame-Break Event

*Does the Minab school incident function as a "frame break"?*

The Minab girls' school strike occurred on Day 1 --- a US Tomahawk cruise missile struck the Shajareh Tayyebeh girls' elementary school in Minab, adjacent to an IRGC naval compound, killing at least 165 children and staff. The dataset contains 28 events referencing Minab or school-related civilian casualties, spanning Day 1 through Day 30, across five event domains (STRIKE, HUMANITARIAN, DIPLOMATIC, FINANCIAL, OTHER).

The immediate framing impact is visible in the humanitarian-to-security keyword ratio:

**Table 5. Humanitarian-to-Security Ratio, Days 1--10**

| Day | Events | Humanitarian Score | Security Score | Hum/Sec Ratio |
|-----|--------|--------------------|----------------|---------------|
| 1 | 93 | 37 | 62 | **0.60** |
| 2 | 75 | 30 | 54 | **0.56** |
| 3 | 83 | 46 | 34 | **1.35** |
| 4 | 59 | 27 | 31 | **0.87** |
| 5 | 53 | 33 | 26 | **1.27** |
| 6 | 52 | 24 | 25 | **0.96** |
| 7 | 51 | 31 | 21 | **1.48** |
| 8 | 57 | 26 | 34 | **0.76** |
| 9 | 56 | 21 | 32 | **0.66** |
| 10 | 57 | 21 | 36 | **0.58** |

The ratio jumped from 0.60 on Day 1 to 1.35 on Day 3 --- more than doubling in 48 hours. This is the sharpest single-day shift in the entire 30-day dataset. The humanitarian frame exceeded the security frame on Days 3, 5, and 7, establishing a pattern of alternating dominance that persisted through the first three weeks.

The comparison of Day 1 frame composition with Days 2--7 confirms the shift:

- **Day 1:** Security 52.5%, Humanitarian 31.4%, Negotiation 0.0%, Economic 16.1%
- **Days 2--7:** Security 34.0%, Humanitarian 34.0%, Negotiation 2.7%, Economic 29.2%

The security frame's share dropped 18.5 percentage points, while the humanitarian frame rose to exact parity at 34.0%. This is consistent with Entman's (2004) concept of a frame break: an event whose moral clarity is sufficient to disrupt the dominant interpretive frame, even when the dominant frame is backed by the full weight of official messaging.

**The Minab Cascade.** The incident generated a traceable cascade of downstream narrative events:

- **Day 1**: Strike event recorded; referenced in all five faction casualty reports; featured in Day 1 briefing headline
- **Day 5**: War cost report references "Minab school --- global scrutiny" alongside Pentagon cost estimates
- **Day 5**: Global protests (2 million people) cite Minab among grievances
- **Day 6**: First US polls show narrow support for strikes but opposition to ground war
- **Day 9**: 500,000 march in Washington --- largest US anti-war protest since 2003
- **Day 18**: Amnesty International publishes investigation confirming US responsibility, verifying 168--170 girls killed
- **Day 28**: Iran FM Araghchi cites Minab before UN Human Rights Council, accusing coalition of genocide
- **Day 30**: Infrastructure damage summary records verified death toll of 168

The Minab incident thus operated not as a single frame-break moment but as a *recurring anchor* for the humanitarian counter-narrative. Each new reference --- the protest signs, the Amnesty verification, the UN speech --- reactivated the humanitarian frame and forced the security frame to contest rather than dominate.

### 4.4 RQ4: Daily Briefing Headlines and Narrative Persistence

*How do briefing headlines reflect narrative competition?*

The 30 daily briefing headlines show a strikingly different frame distribution than the event-level data:

**Table 6. Dominant Frame: Briefing Headlines vs. Event-Level Data**

| Frame | Briefing Headlines | Event-Level Data |
|-------|-------------------|-----------------|
| Security | **60.0%** (18/30) | 31.5% |
| Economic | **23.3%** (7/30) | 20.6% |
| Humanitarian | **10.0%** (3/30) | 18.1% |
| Negotiation | **6.7%** (2/30) | 2.4% |

The security frame was dominant in 18 of 30 briefing headlines (60.0%) --- nearly double its share in the event-level data (31.5%). The humanitarian frame, which contested the security frame at the event level on 12 of 18 days during Phase 2, was dominant in only 3 briefing headlines (10.0%). This gap --- security overrepresented by a factor of 1.9, humanitarian underrepresented by a factor of 1.8 --- is the most consequential finding for narrative theory.

The three humanitarian-dominant briefing headlines occurred on Day 3 ("Hezbollah enters the war --- 500+ rockets at Israel; 3 civilians killed"), Day 7 ("450,000 displaced in Lebanon"), and Day 29 ("Houthis launch first missile barrage at Israel"). Only the Day 7 headline centered Iranian civilian suffering; the Day 3 and Day 29 headlines focused on Israeli and Lebanese civilian impact. The Minab school strike --- the single most significant humanitarian event in the dataset --- was mentioned in the Day 1 headline but was subordinated to the security frame: "Operation Epic Fury begins --- Khamenei killed; 6 US soldiers KIA at Port Shuaiba; **Minab school strike kills 165+**; Brent surge..."

The frame transitions in briefing headlines reveal a pattern of *security anchoring with periodic disruption*:

- Days 1--2: Security
- Day 3: Humanitarian (Hezbollah front)
- Days 4--6: Security
- Day 7: Humanitarian (Lebanon displacement)
- Days 8--10: Security
- Day 11: Negotiation (first ceasefire mention)
- Days 12--13: Economic (oil crash, Hormuz convoy)
- Day 14: Security
- Day 15: Security (Kharg re-strike)
- Days 16, 18--20: Economic (energy war, market impacts)
- Days 17, 21--25, 28, 30: Security
- Day 26: Negotiation (ceasefire plan)
- Day 27: Economic
- Day 29: Humanitarian (Houthi barrage)

The briefing headlines thus show the security frame operating as a *default* that is temporarily displaced by economic shocks, humanitarian crises, or diplomatic milestones before reasserting itself. The humanitarian frame penetrates the briefing level only when it involves *new fronts* (Hezbollah, Houthis) or *mass displacement* --- not when it involves Iranian civilian casualties, which are the majority of humanitarian events in the underlying data.

### 4.5 Supplementary Finding: Data Confidence as Information Quality Proxy

The dataset's `data_confidence` field (HIGH/MEDIUM/LOW) provides an additional lens on information quality over time:

**Table 7. Data Confidence by Week**

| Confidence | Week 1 | Week 2 | Week 3 | Week 4 |
|-----------|--------|--------|--------|--------|
| HIGH | 301 | 219 | 242 | 283 |
| MEDIUM | 143 | 179 | 100 | 93 |
| LOW | 22 | 15 | 2 | 0 |

LOW-confidence events declined from 22 in Week 1 to zero by Week 4, while MEDIUM-confidence events also declined steadily. This suggests that the information environment became *more reliable* over time --- likely reflecting the accumulation of verification (satellite imagery, investigative reports, official acknowledgments) that transforms initial claims into confirmed events. This pattern is relevant for the propaganda model: the early dominance of official sources coincides with the period of lowest information quality, suggesting that official sources fill an *information vacuum* rather than competing on equal terms with alternatives.

The domain-level confidence distribution reveals that RETALIATION events are almost exclusively HIGH confidence (299 of 307), while STRIKE events have the most heterogeneous distribution (279 HIGH, 331 MEDIUM, 31 LOW). This asymmetry likely reflects the verification challenge: US/Israeli strikes in Iran are difficult for independent observers to confirm in real time, while Iranian/proxy retaliation strikes on Gulf bases and Israeli cities are immediately observable.
