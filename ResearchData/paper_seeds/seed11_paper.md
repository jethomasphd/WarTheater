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
