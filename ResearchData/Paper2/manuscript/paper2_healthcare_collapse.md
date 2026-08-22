# The Direct Toll Is a Floor: Civilian-Facing Targeting, Health-System Degradation, and Mortality in the First 170 Days of the 2026 US–Iran War

**Working paper — Paper 2 of the IranWar.ai research-agenda series**

*Prepared from the IranWar.ai Event-Level Research Dataset, v1.2 (Days 1–170; 2026-02-28 to 2026-08-16).*
All results are reproducible from the scripts in `ResearchData/Paper2/src/` (see the Reproducibility section).

---

## Abstract

**Background.** Armed conflict kills far more people than bombs kill directly: the
conflict-epidemiology literature consistently finds 3–15 indirect deaths — from disrupted
healthcare, displacement, water failure, and disease — for every direct death. The 2026
US–Iran war (Operation Epic Fury) is the first sustained interstate air war tracked at
daily resolution in an openly available event dataset, and its record documents systematic
harm to the machinery of survival: 309 health facilities and 42 ambulances damaged in Iran,
152 verified attacks on healthcare in Lebanon, destroyed desalination plants, and a
national grid degraded by a third within eleven days.

**Methods.** Retrospective ecological time-series study of 170 conflict-days. From 4,612
event records we constructed a daily panel joining strike tempo (split into civilian-facing
vs military-facing target classes), an audited 21-event health-system insult register with
a documented, runtime-verified audit trail, a benchmark-anchored facility-damage curve
(31 → 307 → 309 facilities), and daily estimated deaths for five factions. Analyses use the
standard behavioral-statistics toolkit: ANOVA-family phase comparisons with Holm-corrected
pairwise tests and effect sizes; hierarchical OLS with Newey–West standard errors and
negative-binomial robustness; single-mediator analysis with seeded bootstrap (10,000
resamples); moderation with simple slopes and Johnson–Neyman probing; scenario projection
of indirect mortality; and a source-divergence analysis that treats casualty-figure
disagreement as data.

**Results.** Mortality was front-loaded and regime-gated: the Major Combat phase (Days
1–40, 23.5% of the war) carried 79.6% of all documented deaths (phase η² = 0.76;
combat-vs-ceasefire Hedges' g = 3.4), and deaths per strike location collapsed from 15.4
to 0.7 between the initial campaign and the July resumption (Mann–Whitney p < 0.0001).
Within days, civilian-facing strike tempo — not overall or military-facing tempo — carried
the mortality association (b = 2.07 civilian deaths per civilian-facing location, p < .001;
military-facing b = −0.47, n.s.; NB2 incidence-rate ratio 1.62); 67.8% of the
military-tempo–mortality association was mediated by civilian-facing targeting (indirect
effect 1.02, bootstrap CI [0.60, 1.84]). As benchmark facility damage accumulated, the
marginal strike–mortality slope steepened from 0.18 (n.s.) to 1.07 (p = .006)
(interaction p = .006), a pattern consistent with resilience erosion, though the
event-count degradation index showed the same direction without significance. The
documented direct toll (Iran 3,166–3,636; Lebanon 2,993–4,308) is a floor: at the
literature-average 4:1 indirect:direct ratio it implies roughly 15,800–18,200 total deaths
in Iran and 15,000–21,500 in Lebanon. Casualty sources diverged by up to 3.8× at Day 45 —
with civilian counts diverging in the opposite direction from totals — and the dashboard's
own cumulative metric re-anchored by −63% in a single day; the core regression result was
stable across data-confidence weighting variants (b = 1.60–2.36).

**Conclusions.** In this war, what killed civilians on any given day was not how much was
struck but *what* was struck, and every additional strike was associated with more
marginal deaths as the health system's infrastructure accumulated damage. Direct death
counts — themselves contested at up to 3.8× — should be communicated as floors, with the
indirect tail made explicit. The analysis demonstrates a transparency-aware epidemiology
in which confidence ratings and source disagreements are analytic inputs: the
counter-technology stance the dataset was built to enable, extended here to the empirical
study of the war's health consequences.

**Keywords:** armed conflict, civilian mortality, attacks on healthcare, health-system
resilience, indirect mortality, WASH, OSINT event data, mediation, moderation, US–Iran

---

## 1. Introduction

Wars kill twice. The first killing is visible: the strike, the collapsed apartment block,
the daily toll in the briefing. The second killing is quiet and much larger — the dialysis
schedule that ends when the hospital loses power, the childbirth complication two hours
from the nearest functioning surgical theater, the cholera that follows a destroyed water
intake. Across modern conflicts, this indirect mortality has repeatedly been found to
exceed direct battle deaths by factors of three to fifteen (Guha-Sapir & van Panhuis 2004;
Geneva Declaration Secretariat 2008; Checchi & Roberts 2008). The mechanism is not
mysterious: populations survive on systems — healthcare, water, power, supply chains — and
modern air campaigns degrade systems efficiently. Health-system resilience theory (Kruk et
al. 2015, 2017) names the capacities a system needs to absorb shock; sustained bombardment
attacks exactly those capacities, and epidemiological work has linked healthcare
infrastructure destruction to excess non-battle mortality at the population level (Jawad
et al. 2020; Spiegel 2017; Levy & Sidel 2008).

The 2026 US–Iran war offers an unusual window on this process. It is the first sustained
interstate air war of its scale to be tracked openly, daily, and at event-level resolution
from its opening hours (Thomas et al. 2026). The IranWar.ai Event-Level Research Dataset
records — alongside strikes, retaliations, and market reactions — a granular trail of harm
to the machinery of survival: a Tehran hospital's IVF department destroyed by blast on Day
3; the ICRC's assessment on Day 11 that 30–40% of Iranian power generation was degraded; a
pharmaceutical factory strike that killed ten nurses on Day 33; the WHO's Day-39 count of
307 damaged health facilities; the WHO's global emergency logistics hub placed on hold on
Day 45; 152 verified attacks on healthcare in Lebanon by Day 69, killing 103; the
destruction of the Bonji desalination intake on Day 140, cutting drinking water to some
10,000 people across 20 villages; and, by Day 170, an Iranian Red Crescent inventory of
309 damaged health facilities, 42 damaged ambulances, and 7 evacuated hospitals.

This paper — the second in the dataset's research-agenda series, executing the public
health seed of that agenda — asks four questions of the war's first 170 days, each with a
deliberately standard statistical tool:

1. **How was mortality distributed across the war's political phases?** (means
   comparison: ANOVA family, pairwise tests, effect sizes)
2. **What component of daily violence predicted daily deaths?** (correlation and
   hierarchical regression, with count-model robustness)
3. **Did civilian-facing targeting carry the tempo–mortality association?** (single-
   mediator analysis with bootstrapped indirect effects)
4. **Did accumulating health-system damage change what a strike cost in lives?**
   (moderation with simple slopes and Johnson–Neyman probing)

We then place the answers in their epidemiological frame: the direct toll these analyses
model is, by everything the literature knows, a **floor**, and we make the implied
indirect tail explicit through transparent scenario projection rather than leaving it
unstated (Section 4.6).

Two prior results discipline the design. Paper 1 of this series established that daily
kinetic tempo is a poor proxy for lethality (its casualty-tempo caveat) and that the war's
violence switched on and off with its political regime. We take both seriously: our
regression models disaggregate tempo by *target class* rather than using raw tempo, and
phase structure enters every analysis. Second, the dataset's own methods paper argues that
in an information environment characterized by a structural and strategic "flood,"
casualty discrepancies are political facts to be analyzed, not noise to be cleaned
(Thomas et al. 2026, §6.4–6.5). Section 4.7 operationalizes that stance: we quantify the
divergence between casualty sources (including a −63% single-day re-anchoring of the
dashboard's own cumulative metric), and we re-estimate the core model under
data-confidence weighting — the "raw and confidence-weighted variants in parallel"
practice the dataset's documentation recommends. The paper is thus both an empirical study
of the war's health consequences and a demonstration that the dataset's transparency
infrastructure — confidence ratings, source attribution, event-level provenance — can be
used *as analytic inputs*: the counter-technology extended from data publication to data
analysis.

## 2. Data

### 2.1 Source and pinning

All analyses use the frozen v1.2 research release of the IranWar.ai Event-Level Research
Dataset (4,612 event rows, 52 columns, Days 0–170; Thomas et al. 2026), pinned so the
paper reproduces byte-for-byte regardless of later releases. The unit of analysis is the
conflict-day (N = 170; Day 1 = 2026-02-28). The four-phase structure follows Paper 1:
Major Combat (Days 1–40), First Ceasefire (41–129), Resumption (130–152), and Diplomatic
Pause (153–170) — documented boundaries corroborated by structural-break detection.

### 2.2 Outcomes

Daily estimated deaths by faction come from the dataset's casualty file (850 rows = 170
days × 5 factions; daily estimates, not cumulative): Iranian civilian (primary outcome;
543 total), Iranian military (2,623), Lebanese all-category (2,993), US military (20), and
Israeli military (34). Cumulative dashboard snapshots provide reference series (Iranian
killed, Lebanese killed, displaced, children killed), linearly interpolated across the
44–63 unobserved days. The two internal accountings disagree — the summed daily series
runs 14.8% (Iran) and 43.9% (Lebanon) below the terminal snapshots — and we carry both
forward as bounds rather than reconciling them (Sections 4.6–4.7).

### 2.3 Exposures

Strike tempo uses Paper 1's operationalization (distinct strike-file locations active per
day plus discrete timeline events), split here into **civilian-facing** locations — coded
target type civilian, oil/energy, communications, or water infrastructure, or
civilian-facing keywords (hospital, school, residential, desalination, power, refinery,
broadcast, airport) — and **military-facing** locations (the remainder). The
civilian-facing class deliberately includes energy, water, and communications: in the
public-health frame these are civilian-facing regardless of dual-use classification,
because their destruction transmits harm through the systems civilians survive on.

### 2.4 The health-system insult register and two degradation curves

We built a register of discrete health-system events by keyword screen over the strike,
retaliation, military, and humanitarian domains (excluding headline-echo row types and
reference files), de-duplicated strike-file locations to their onset day, classified rows
by ordered rules into five insult categories plus surveillance reports, and then **read
and audited every screened row**. Seventeen corrections (6 reclassifications, 6
exclusions, 5 same-incident merges) are recorded by event id with reasons in the analysis
code and verified against the dataset at run time; all 82 screened rows ship in
`data/health_system_events.csv` with their audit actions visible. The result: **21 counted
insult events** — 6 facility attacks (from the Gandhi Hospital blast damage on Day 3 to
the strike near the Tyre hospital on Day 94), 6 workforce-harm events (including the ten
nurses killed in the Tofigh Daru pharmaceutical factory strike and at least three Red
Cross/Crescent paramedics killed in Lebanon), 6 WASH disruptions (three desalination
plants among them), 2 humanitarian-access disruptions (the WHO Dubai logistics hub hold;
a seized cargo of medical supplies), and 1 pharmaceutical supply attack.

The cumulative count of these events forms the **Health-System Stress Index (HSSI)** — an
index of *reported, nationally salient* insults, not a facility census. Because
surveillance benchmarks show true facility damage two orders of magnitude larger, a second
operationalization anchors a piecewise-linear **facility-damage curve** to institutional
reports verified in the event stream: 31 hospitals damaged by Day 15 (Iran Health
Ministry-linked reporting), 307 health facilities by Day 39 (WHO), 309 by Day 170 (IRCS).
Every degradation model is estimated with both curves; their disagreement is reported, not
averaged away. (The ICRC's Day-28 figure of 25 damaged facilities — *lower* than the
Day-15 ministry figure — is excluded from the monotone curve and analyzed as a political
fact in Section 4.7.)

## 3. Statistical methods

Phase comparisons use one-way ANOVA, Welch's ANOVA (flagged as undefined where a phase has
zero variance), and Kruskal–Wallis, with pairwise Welch t-tests under Holm correction,
η²/ω², and Hedges' g. Strike-day contrasts use Welch t and Mann–Whitney U. Regression
models are hierarchical OLS with Newey–West (HAC, 7-day) standard errors — daily war
series are serially dependent — with negative-binomial (NB2) count models as
distributional robustness, estimated on the full sample and Major Combat only. Mediation
uses the single-mediator product-of-coefficients with a seeded nonparametric percentile
bootstrap (10,000 day-resamples; Preacher & Hayes 2008), Sobel test for reference; X
(military-facing) and M (civilian-facing) are non-overlapping counts. Moderation models
interact centered strike tempo with each centered degradation curve (HAC SEs), probed by
simple slopes at ±1 SD and Johnson–Neyman boundaries (Aiken & West 1991), with
kinetic-days-only and phase-interaction sensitivity checks. Indirect-mortality projection
applies literature indirect:direct ratios (1:1 floor; 3:1; 4:1 average; 15:1 upper;
Geneva Declaration Secretariat 2008) to both direct-toll bases. The source-divergence
analysis compiles cumulative casualty claims by named source — each anchored to a dataset
event id and verified at run time — and re-estimates the core model under three
data-confidence variants. All computation is seeded and reproducible (`run_all.sh`,
~1 minute); α = .05 two-sided throughout.

## 4. Results

### 4.1 The shape of mortality (Table 1; Figures 1–3)

The war killed 6,213 people across the five tracked factions by the daily series' account
— 4,944 of them (79.6%) in the 40 days of Major Combat, which is 23.5% of the war's
duration. Iranian deaths (civilian + military) averaged 78.1/day during Major Combat and
then fell to zero for the entire 89-day First Ceasefire; the Lebanon front, by contrast,
kept absorbing 13.5 deaths/day through that same ceasefire — 1,200 Lebanese deaths accrued
while the Iran front was silent — before the fronts inverted at the Resumption (Iranian
deaths resumed at 1.7/day; Lebanese deaths effectively ceased). Mortality in this war was
not a smooth function of its duration; it was gated by regime and reallocated across
fronts (Figure 1).

The health-system insult register concentrates the same way: 11 of 21 events (52%) fall in
Major Combat, and the benchmark facility-damage curve completes 99% of its Day-170 level
by Day 39 (Figure 3). Displacement reached 1.2 million and the children-killed snapshot
379 by Day 170 (Figure 2); Iran's Legal Medicine Organization reported 383 children ≤18
among the dead as early as Day 53.

**Table 1. Per-phase summary (daily means; totals in parentheses).**

| Phase | Days | Strikes/day | Civ-facing/day | Iran civ/day | Iran mil (total) | Lebanon/day (total) | All-faction total |
|---|---|---|---|---|---|---|---|
| Major Combat | 1–40 | 7.02 | 2.60 | 13.08 (523) | (2,602) | 44.52 (1,781) | 4,944 |
| First Ceasefire | 41–129 | 0.57 | 0.09 | 0.00 (0) | (3) | 13.48 (1,200) | 1,215 |
| Resumption | 130–152 | 2.35 | 0.91 | 0.87 (20) | (18) | 0.04 (1) | 43 |
| Diplomatic Pause | 153–170 | 0.00 | 0.00 | 0.00 (0) | (0) | 0.61 (11) | 11 |
| Full war | 1–170 | 2.27 | 0.78 | 3.19 (543) | (2,623) | 17.61 (2,993) | 6,213 |

### 4.2 Phase comparisons (Table 2; Figure 4)

Phase differences are enormous by behavioral-science standards. For all-faction daily
killed, F(3,166) = 172.3, p < .001, η² = .757 (ω² = .751); Welch's F = 97.6 and
Kruskal–Wallis H = 104.9 agree (both p < .001). For Iranian civilian deaths, F = 106.6,
η² = .658 (Welch undefined — two phases have zero variance — Kruskal–Wallis H = 149.8,
p < .001); for Lebanese deaths, F = 23.4, η² = .297. Holm-corrected pairwise contrasts
show Major Combat exceeding every other phase at g = 3.1–3.4 (all p < .001) for total
killed; the three post-combat phases differ from one another only modestly (the
ceasefire's Lebanese toll keeps it above the later phases, g = 0.6, p < .001).

Strike days (n = 89) carried 6.5× the daily mortality of quiet days (61.3 vs 9.4 killed,
Welch t = 7.09, p < .001, g = 1.04); Iranian civilian deaths averaged 6.0 on strike days
vs 0.1 on quiet days (g = 0.96).

Per-strike lethality collapsed across regimes. On strike days, Iranian deaths per distinct
strike location averaged **15.4** during Major Combat (median 10.8), **0.7** at the
Resumption (median 0.2), and effectively zero during ceasefire-era enforcement activity —
a 95% decline from the initial campaign to the July re-escalation (Mann–Whitney U = 623,
p < .0001, g = 2.16). The deadliest single day of the war remained its first (the Minab
girls' school strike alone killed 150–170). Direct mortality, in short, was front-loaded:
the opening campaign against an unprepared population and an intact urban target set did
almost all of the war's direct killing.

### 4.3 Which component of the violence predicted death (Table 3)

Daily Iranian civilian deaths correlate with overall strike tempo (r = .67), retaliation
tempo (r = .74), and — most strongly among the kinetic series — civilian-facing strike
tempo (r = .72; all p < .001). Cross-correlations peak at short lags (killed_total: peak
r = .74 at 6 days; Lebanese deaths build gradually from r = .29 same-day to r ≈ .46–.48 at
1–7 days, consistent with that front's slower operational rhythm), but same-day structure
dominates for Iranian outcomes.

The hierarchical models sharpen this. Raw tempo predicts civilian deaths (M1: b = 1.27,
R² = .44), but when tempo is split by target class (M3), **the entire association
concentrates in the civilian-facing component**: b = 2.07 (HAC p < .001) per
civilian-facing location, against b = −0.47 (p = .20) for military-facing locations, with
retaliation contributing b = 0.89 (p < .001). Adding phase dummies (M4) attenuates but
does not displace the civilian-facing coefficient (b = 1.31, model R² = .70). The
Major-Combat-only estimates repeat the pattern (civilian-facing b = 1.69, p < .001;
military-facing n.s.). Negative-binomial models tell the same story in count terms: each
additional civilian-facing location multiplies expected civilian deaths by **1.62**
(IRR, p < .001), each military-facing location by 0.86 (p = .053, *below* one), each
retaliation unit by 1.44 (p < .001).

This is the constructive refinement of Paper 1's casualty-tempo caveat: total tempo is
indeed a poor lethality proxy — because lethality lives almost entirely in the
civilian-facing slice of the target set.

### 4.4 Mediation: civilian-facing targeting carries the association (Table 4; Figure 5)

If military-facing tempo does not predict civilian deaths directly, why do heavy bombing
days kill civilians? The mediation model formalizes the target-set-widening explanation:
days of heavier military-facing tempo are days when strikes also widen into
civilian-facing infrastructure (path a = 0.33, p < .001), and it is that widening which
predicts deaths (path b = 3.07, p < .001). The indirect effect is **a×b = 1.02 (95%
bootstrap CI 0.60–1.84**, 10,000 seeded resamples; Sobel z = 6.60), accounting for
**67.8%** of the total association (c = 1.50 → c′ = 0.48, the direct path no longer
distinguishable from zero). The same decomposition holds for all-faction deaths (50.3%
mediated, CI 3.92–11.82).

Two honesty notes. First, same-day mediation on a time series is an associational
decomposition, not a causal identification. Second, the full-sample estimate partly
reflects the war switching on and off — within Major Combat alone (n = 40) the direction
is identical but the bootstrap CI touches zero (indirect 0.13, CI −0.03–0.68; proportion
mediated 86%). The full-sample result says: across this war, the days that killed
civilians were the days the target set widened; the within-combat result says the same
with less certainty from forty observations.

### 4.5 Moderation: what a strike cost as the system degraded (Table 5; Figure 6)

The resilience-erosion hypothesis (Kruk et al. 2015) predicts that as health-system
capacity erodes, the same kinetic dose converts to more deaths — survival after injury
depends on intact trauma care. The rival account — harm front-loading — notes that early
strikes catch unprepared, densely settled populations, and that adaptation (sheltering,
flight, the 1.2 million displaced) should *reduce* per-strike deaths over time.

Both are visible, because they answer different questions. In *average yield* terms,
front-loading wins decisively (the 15.4 → 0.7 collapse of §4.2). But in *marginal* terms —
the within-day slope of deaths on strikes at a given level of accumulated damage — the
association steepens as the system degrades. With the benchmark-anchored facility-damage
curve as moderator, the strikes × damage interaction is positive and significant
(b₃ = 0.0145, HAC p = .006; kinetic-days-only p = .006): the simple slope of civilian
deaths on strike tempo rises from **0.18 (n.s.) at −1 SD** of facility damage, through
**0.63 (p = .02) at the mean**, to **1.07 (p = .006) at +1 SD** — a roughly fivefold
steepening across the observed damage range, with the Johnson–Neyman boundary indicating
significance for all but the lowest-damage early days. The 21-event HSSI, the coarser
operationalization, shows the same direction without significance (interaction p = .32;
slopes 0.45 → 0.82) — we report both rather than selecting the favorable one. A
phase-interaction variant finds no slope difference between Major Combat and the
Resumption (interaction p = .89) once the Resumption's far lower baseline (−10.7 deaths/
day, p < .001) is absorbed, indicating the moderation tracks the *damage curve*
specifically rather than a generic late-war regime shift.

The moderation pattern is consistent with resilience erosion in the marginal sense — by
late war, a degraded system had less capacity to keep each additional strike's victims
alive — but degradation is confounded with everything else that changed over 170 days
(munitions, tactics, sheltering, reporting practices). We read this as evidence, not
proof, and note that the direct-death series is structurally incapable of registering the
mechanism's main predicted effect, which is indirect mortality (next section).

### 4.6 The floor and the tail: projecting indirect mortality (Table 6; Figure 7)

Everything modeled above concerns *direct, reported* deaths. The conflict-epidemiology
literature is unambiguous that such counts are floors: across late-20th- and
21st-century conflicts, indirect deaths — from health-system collapse, displacement,
water failure, and disease — have exceeded direct deaths by roughly 3:1 to 15:1, with ~4:1
an often-cited cross-conflict average (Geneva Declaration Secretariat 2008; Guha-Sapir &
van Panhuis 2004; Checchi & Roberts 2008). This war's documented degradation profile —
309 damaged health facilities, 12 hospitals rendered inactive by Day 15 and 7 evacuated by
Day 170, 127 healthcare workers killed in Lebanon by Day 93, three destroyed desalination
plants, 30–40% of power generation degraded by Day 11, a blockade that seized medical
supplies and idled the WHO's regional logistics hub — sits squarely in the class of
conflicts where the higher ratios have been observed.

We therefore project, explicitly as scenario arithmetic and not as an estimate from these
data. The documented direct toll at Day 170 is itself an interval — Iran 3,166 (daily
series) to 3,636 (terminal snapshot); Lebanon 2,993 to 4,308 — and we carry that interval
through each ratio:

**Table 6. Projected total conflict deaths at Day 170 under literature indirect:direct ratios.**

| Ratio (indirect:direct) | Iran — indirect | Iran — total | Lebanon — indirect | Lebanon — total |
|---|---|---|---|---|
| 1:1 (floor) | 3,166–3,636 | 6,332–7,272 | 2,993–4,308 | 5,986–8,616 |
| 3:1 (low) | 9,498–10,908 | 12,664–14,544 | 8,979–12,924 | 11,972–17,232 |
| **4:1 (average)** | **12,664–14,544** | **15,830–18,180** | **11,972–17,232** | **14,965–21,540** |
| 15:1 (upper) | 47,490–54,540 | 50,656–58,176 | 44,895–64,620 | 47,888–68,928 |

The projection's function is communicative discipline: any public rendering of "3,600
dead in Iran" that does not mark the number as a floor misrepresents what conflict
epidemiology knows. The WASH record makes the mechanism concrete at household scale: the
Bonji intake's destruction alone removed drinking water from ~10,000 people in 20
villages; Kuwait — struck twice at its Mina Abdullah power-and-desalination complex —
relies on desalination for ~90% of its potable water.

### 4.7 Reading the disagreements: the flood, quantified (Table 7; Figure 8)

The dataset's methods paper argues that in this war's information environment, casualty
discrepancies are political facts — "signal to be interpreted," not noise to be cleaned
(Thomas et al. 2026, §6.5). This section does that interpretation quantitatively.

**The spread.** Cumulative Iranian-toll claims by named source, each anchored to a
verified dataset event: at Day 29, Iran's deputy UN representative acknowledged 1,750
dead while HRANA had documented 3,114 (ratio 1.78). By Day 45 the spread had widened to
**3.8×**: the Health Ministry held near ~2,000, HRANA's named-verification count stood at
3,636, and Hengaw's field-reporting count at 7,650 — with the IDF separately claiming
6,000+ IRGC dead. The structure of the disagreement is as informative as its size:
**the civilian counts diverge in the opposite direction from the totals** (HRANA counted
more civilians than Hengaw, 1,701 vs 1,030, while counting fewer than half Hengaw's
total), because the contest is really over *military* deaths — the number that measures
regime damage. Each figure is legible as its source's institutional position; averaging
them would manufacture a number no one reported.

**The re-anchoring.** The tracking infrastructure itself records the source war. The
dashboard's cumulative Iranian-killed metric climbed to 9,226 by Day 56 and dropped to
3,375 on Day 57 — a **−63% single-day revision** that re-anchored the series onto the
Legal Medicine Organization's forensic count published days earlier (and, at Day 170,
onto HRANA-family verification at 3,636). A transparency-first tracker does not escape
the flood; it *documents its own passage through it*, which is what makes the revision
recoverable as an analytic object at all.

**The stability check.** Because every event row carries a confidence rating, the core
result can be stress-tested rather than asserted. Rebuilding the exposure series (i) from
all rows, (ii) from HIGH-confidence rows only, and (iii) confidence-weighted
(1.0/0.7/0.4), the civilian-facing coefficient is **2.07 / 1.60 / 2.36** respectively —
direction and magnitude stable, with the HIGH-only variant losing significance purely
through discarded data (its standard error triples), and the military-facing coefficient
remaining null in every variant (−0.47 / −0.56 / −0.57). The headline finding does not
depend on the dataset's shakiest rows. This is the counter-technology used as intended:
transparency artifacts functioning as instruments of verification rather than
disclaimers.

**Table 7. Divergence summary.**

| Moment | Scope | Low | High | Ratio |
|---|---|---|---|---|
| Day 29 | Iran total | 1,750 (deputy UN rep) | 3,114 (HRANA) | 1.78 |
| Day 45 | Iran total | ~2,000 (Health Ministry) | 7,650 (Hengaw) | 3.82 |
| Day 45 | Iran civilian | 1,030 (Hengaw) | 1,701 (HRANA) | 1.65 |
| Day 57 | Dashboard re-anchoring | 3,375 (post) | 9,226 (pre) | 2.73 |
| Day 170 | Dataset-internal, Iran | 3,166 (daily series) | 3,636 (snapshot) | 1.15 |
| Day 170 | Dataset-internal, Lebanon | 2,993 (daily series) | 4,308 (snapshot) | 1.44 |

## 5. Discussion

**What killed civilians was what was struck, not how much.** The war's central
public-health regularity is the concentration of mortality in the civilian-facing slice
of the target set. Military-facing strike tempo — the majority of locations struck — has
no positive association with civilian deaths in any specification or confidence variant;
civilian-facing tempo carries the association everywhere, and two-thirds of the
military-tempo association is mediated through it. In operational terms: civilian
mortality in this war was not the random by-product of volume; it tracked the widening of
the target set into the infrastructure civilians live on. This aligns the quantitative
record with what the qualitative record already shows — a girls' school on Day 1, a
hospital's IVF department on Day 3, a pharmaceutical factory and its ten nurses on Day
33, desalination intakes by Day 140 — and gives the protection-of-civilians and
attacks-on-healthcare literatures (WHO SSA; Levy & Sidel 2008) a day-level statistical
correlate in an interstate air war.

**Front-loaded averages, steepening margins.** The two lethality findings are not in
tension; they are the two halves of the epidemiological story. Average per-strike yield
collapsed 95% from the opening campaign to the July resumption — direct harm was
front-loaded onto an unprepared population, and adaptation (1.2 million displaced,
sheltering, evacuation) plus target-set depletion drove the average down. Yet at any
given point, the *marginal* association between one more strike location and same-day
deaths steepened as facility damage accumulated — precisely the signature a resilience
frame predicts when trauma-care capacity erodes. The moderation is observational and
time-confounded, and the coarser event-count index does not reach significance; we weight
it accordingly. But its practical reading deserves emphasis: **late-war "low-intensity"
operations were not low-cost per event** — by the resumption, each strike landed on a
system with little remaining slack.

**The direct toll is a floor, and saying so is a public-health act.** Every model above
runs on direct, reported deaths, and Section 4.7 shows even those are contested at up to
3.8×. The degradation record — hundreds of damaged facilities, killed health workers,
destroyed water infrastructure, blockaded medical supply — is exactly the machinery of
indirect mortality, which this design structurally cannot observe and which the
literature expects to be several times larger than what it can. The 4:1-average scenario
implies on the order of thirty thousand total deaths across Iran and Lebanon against a
documented ~6,200–7,900. We do not claim that number; we claim its *communicability*:
tolls should be published as floors with explicit tails, and the projection table is a
template for doing so.

**Extending the counter-technology to analysis.** The dataset was framed as a
counter-technology against the information flood — structure, provenance, and visible
uncertainty as restorations of the reader's capacity to evaluate (Thomas et al. 2026,
§6.4). This paper extends that stance from publication to analysis. The flood's strategic
layer appears here as a measured object: a 3.8× spread whose civilian and military
components diverge in opposite directions because different actors need different
numbers; a tracking metric that re-anchored by −63% in a day when a more authoritative
count appeared — and left the revision visible in its own history. The structural
response appears as method: anchor-verified curation, an audit trail that ships with its
exclusions, and a headline coefficient reported in parallel across confidence variants.
None of this makes the numbers true. It makes them *assessable* — which is the property
the flood strips away, and the property analysis can restore.

**For health systems.** Three operational implications follow. First, surveillance of
attacks on healthcare (WHO SSA-style) provided the benchmarks that made our
better-performing degradation curve possible; sustaining such surveillance *during*
active interstate war has analytic as well as protective value. Second, the WASH events
are early-warning markers: destroyed desalination capacity in a region where one struck
state draws ~90% of its potable water from it defines a predictable morbidity tail that
demands pre-positioned response. Third, the front-loading result argues that the window
for protecting civilians in an air war of this type is measured in days: most of the
direct dying happened before the fortieth.

## 6. Limitations

(1) Ecological day-level design: no individual-level inference; associations, not causal
effects. (2) The casualty series are contested estimates passing through internet
blackouts and strategic reporting; we quantify the spread (up to 3.8×), run models on the
conservative series, and carry both internal bases through every cumulative claim, but no
weighting scheme can manufacture ground truth. (3) The 21-event insult register captures
reported, salient insults, not the damage census (WHO's 307 by Day 39); the
benchmark-anchored curve mitigates but interpolates between sparse anchors. (4)
Major-Combat-only models rest on 40 observations. (5) Degradation is confounded with
time; the moderation result is effect-modification evidence, not mechanism proof. (6)
Same-day mediation is decomposition, not identification; the full-sample estimate partly
reflects regime switching. (7) No spatial analysis: strike coordinates exist but hospital
coordinates do not (the WHO EMRO facility registry would enable seed #4's spatial
analysis). (8) Indirect-mortality figures are projections under stated ratios, falsifiable
only by post-war mortality surveys — which we hope this paper helps motivate.

## 7. Conclusion

Across 170 days of the 2026 US–Iran war, direct civilian mortality was gated by political
regime, front-loaded into the first forty days, and — within days — carried almost
entirely by the civilian-facing slice of the target set, with the marginal cost of each
strike rising as the health system's infrastructure accumulated damage. The documented
toll is a floor several times below what conflict epidemiology expects the war's full
mortality to be, and the numbers that make up that floor diverge across sources in ways
that are themselves informative about the actors producing them. A dataset built to keep
its uncertainty visible made all of this analyzable with nothing more exotic than the
standard behavioral-statistics toolkit — which is, we think, the point: against the
flood, the counter-technology is not sophistication but transparency, carried all the way
from collection through analysis to the sentence a health ministry, journalist, or
humanitarian planner repeats.

---

## Reproducibility

```bash
cd ResearchData/Paper2
python3 -m pip install -r requirements.txt
bash run_all.sh     # regenerates the panel, register, all 20 tables, all 8 figures (~1 min)
```

Pinned input: `ResearchData/releases/v1.2/iranwar_event_dataset.csv` (frozen release).
Every curated constant (register audit, benchmark anchors, toll claims, WASH rows) is
verified against the dataset at run time by anchor-text assertion. Bootstraps are seeded
(SEED = 42). Design decisions: `docs/METHODS.md`; variable definitions:
`docs/CODEBOOK_panel.md`; plain-language analysis guide: `docs/STUDENT_GUIDE.md`.

## References

- Aiken, L. S., & West, S. G. (1991). *Multiple Regression: Testing and Interpreting
  Interactions.* Sage.
- Checchi, F., & Roberts, L. (2008). Documenting mortality in crises: What keeps us from
  doing better? *PLoS Medicine*, 5(7), e146.
- Geneva Declaration Secretariat. (2008). *Global Burden of Armed Violence.* Geneva.
- Guha-Sapir, D., & van Panhuis, W. G. (2004). Conflict-related mortality: An analysis of
  37 datasets. *Disasters*, 28(4), 418–428.
- Hedges, L. V. (1981). Distribution theory for Glass's estimator of effect size and
  related estimators. *Journal of Educational Statistics*, 6(2), 107–128.
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian
  Journal of Statistics*, 6(2), 65–70.
- Jawad, M., Hone, T., Vamos, E. P., Cetorelli, V., & Millett, C. (2020). Implications of
  armed conflict for maternal and child health: A regression analysis of data from 181
  countries for 2000–2019. *PLoS Medicine*, 18(9), e1003810.
- Kruk, M. E., Myers, M., Varpilah, S. T., & Dahn, B. T. (2015). What is a resilient
  health system? Lessons from Ebola. *The Lancet*, 385(9980), 1910–1912.
- Kruk, M. E., et al. (2017). Building resilient health systems: A proposal for a
  resilience index. *BMJ*, 357, j2323.
- Levy, B. S., & Sidel, V. W. (2008). *War and Public Health* (2nd ed.). Oxford
  University Press.
- Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite,
  heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*,
  55(3), 703–708.
- Preacher, K. J., & Hayes, A. F. (2008). Asymptotic and resampling strategies for
  assessing and comparing indirect effects in multiple mediator models. *Behavior
  Research Methods*, 40(3), 879–891.
- Roberts, L., Lafta, R., Garfield, R., Khudhairi, J., & Burnham, G. (2004). Mortality
  before and after the 2003 invasion of Iraq: Cluster sample survey. *The Lancet*,
  364(9448), 1857–1864.
- Salama, P., Spiegel, P., Talley, L., & Waldman, R. (2004). Lessons learned from complex
  emergencies over past decade. *The Lancet*, 364(9447), 1801–1813.
- Spiegel, P. B. (2017). The humanitarian system is not just broke, but broken:
  Recommendations for future humanitarian action. *The Lancet* (online).
- Thomas, J. E., Alpysbekova, A., Osei Mensah, E., Masara, N., & Sharma, P. (2026).
  IranWar.ai: An open-source event-level dataset of the 2026 US–Iran conflict. Preprint,
  github.com/jethomasphd/WarTheater.
- IranWar.ai Research Agenda, Paper 1. (2026). *Reciprocity Without a Lag:
  Contemporaneous Coupling and Regime-Contingent Escalation in the 2026 US–Iran War.*
  github.com/jethomasphd/WarTheater.
- World Health Organization. Surveillance System for Attacks on Health Care (SSA).
  Geneva: WHO.

*Dataset citation:* IranWar.ai Event-Level Research Dataset, v1.2 (2026). Days 1–170.
github.com/jethomasphd/WarTheater, `ResearchData/releases/v1.2/`.
