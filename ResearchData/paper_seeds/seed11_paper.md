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
