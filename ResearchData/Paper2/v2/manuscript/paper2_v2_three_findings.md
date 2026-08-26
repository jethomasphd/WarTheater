# Killed Fast, Left Fragile, Counted Short: Front-Loaded Mortality, Health-System Resilience Erosion, and the Uncounted Indirect Toll in the First 170 Days of the 2026 US–Iran War

**Working paper — Paper 2 (v2, student-findings edition) of the IranWar.ai research-agenda series**

*First author: Eugene Osei Mensah. Prepared from the IranWar.ai Event-Level Research Dataset, v1.2 (Days 1–170; 2026-02-28 to 2026-08-16).*
All results are reproducible from the scripts in `ResearchData/Paper2/v2/src/` (see the Reproducibility section). This edition re-narrates the parent paper's evidence around three findings; every number regenerates, unchanged, from the same frozen dataset.

---

## About this version

The parent paper (`../manuscript/paper2_healthcare_collapse.md`) reports eight
findings across the full behavioral-statistics toolkit. This version narrows to
**three** — the parent paper's Findings 1, 5, and 6 — because they form a single
argument that reads clearly from the clinical side of the health system, which
is where its first author works:

> *The war killed fast and early; the health system gradually lost its ability
> to absorb further shocks; and the deaths we can count may only represent part
> of the real human toll.*

Nothing in the analysis is re-estimated: the panel, the audited health-system
register, the facility-damage curve, the moderation model, and the projection
arithmetic are the parent paper's, run against the same frozen v1.2 release, so
every statistic below matches the parent exactly. What is new here is the
framing — the three findings assembled into one causal-sounding story about how
a health system fails under sustained air war, and read the way a nurse on a
ward reads it. (One number is corrected against the regenerated tables: the
effect size for the per-strike-lethality collapse is Hedges *g* = 1.33, not the
2.16 printed in an earlier draft of the parent; the underlying 95% decline and
Mann–Whitney *U* = 623 are unchanged.)

---

## Abstract

**Background.** Wars kill twice — once by blast, and again, more quietly and
usually in far greater numbers, through the systems people survive on:
healthcare, water, power, supply chains. Across modern conflicts, indirect
deaths have run three to fifteen times direct battle deaths. This paper follows
the machinery of that second killing through the first 170 days of the 2026
US–Iran war, the first sustained interstate air war tracked openly at daily,
event-level resolution.

**Methods.** Retrospective ecological time-series study of 170 conflict-days.
From 4,612 event records we built a daily panel of strike tempo, an audited
21-event health-system insult register, a benchmark-anchored facility-damage
curve (31 → 307 → 309 damaged facilities), and daily estimated deaths by
faction. Three standard tools answer three questions. **Means comparison**
(ANOVA family, effect sizes, per-strike lethality): how was mortality
distributed in time? **Moderation** (strike × degradation interaction with
Newey–West standard errors, simple slopes, Johnson–Neyman): did the cost of a
strike change as the system was damaged? **Scenario projection** (literature
indirect:direct ratios applied to the documented toll): how large is the
uncounted tail? All computation is seeded and reproduces in about half a minute.

**Results.** Mortality was **front-loaded**: the 40 days of Major Combat (23.5%
of the war) carried **79.6%** of all documented deaths (phase η² = 0.76; combat
vs. ceasefire Hedges *g* = 3.4); the cumulative toll crossed half by Day 21. Yet
as facility damage accumulated, the **marginal** cost of each strike **rose**:
the slope of civilian deaths on strike tempo steepened from 0.18 (not
significant) at low damage, to 0.63 at mean damage, to **1.07** at high damage
(interaction *p* = .006) — a roughly sixfold steepening consistent with
resilience erosion, and specific to the damage curve rather than a generic
late-war shift (phase-interaction *p* = .89). Finally, the documented direct
toll (Iran 3,166–3,636; Lebanon 2,993–4,308) is a **floor**: at the
literature-average 4:1 indirect:direct ratio it implies roughly **15,800–18,200**
total deaths in Iran and **15,000–21,500** in Lebanon.

**Conclusions.** The war did most of its visible killing in its first six weeks,
against an unprepared population and an intact health system. The system then
spent the remaining months absorbing the consequences of that opening damage,
with less capacity to keep each new strike's victims alive. And the counted dead
are only the part of the toll that reaches a tally — the indirect deaths, which
this design cannot observe, are where conflict epidemiology expects most of the
dying to be. Tolls from wars like this should be published as floors, with the
tail made explicit.

**Keywords:** armed conflict, civilian mortality, attacks on healthcare,
health-system resilience, indirect mortality, WASH, front-loading, OSINT event
data, US–Iran

---

## 1. Introduction

Wars kill twice. The first killing is visible: the strike, the collapsed
building, the number in the evening briefing. The second is quiet and usually
much larger — the surgery postponed because the operating theatre is damaged,
the delivery that goes wrong two hours from the nearest working theatre, the
dialysis patient who misses three sessions in a row, the cholera that follows a
destroyed water intake. Across late-20th- and 21st-century conflicts, this
indirect mortality has repeatedly been found to exceed direct battle deaths by
factors of three to fifteen (Guha-Sapir & van Panhuis 2004; Geneva Declaration
Secretariat 2008; Checchi & Roberts 2008). The mechanism is not mysterious:
people survive on systems, and air campaigns degrade systems efficiently.
Health-system resilience theory (Kruk et al. 2015, 2017) names the capacities a
system needs to absorb a shock and keep functioning; sustained bombardment
attacks exactly those capacities.

The 2026 US–Iran war is an unusual chance to watch that process unfold. It is
the first sustained interstate air war of its scale tracked openly, daily, and
at event-level resolution from its opening hours (Thomas et al. 2026). The
dataset records, alongside strikes and casualties, a granular trail of harm to
the machinery of survival: a Tehran hospital's IVF department destroyed by blast
on Day 3; the ICRC's Day-11 assessment that 30–40% of Iranian power generation
was degraded; a pharmaceutical factory strike that killed ten nurses on Day 33;
the WHO's Day-39 count of 307 damaged health facilities; 152 verified attacks on
healthcare in Lebanon by Day 69; the destruction of the Bonji desalination
intake on Day 140, cutting drinking water to some 10,000 people across 20
villages; and, by Day 170, an Iranian Red Crescent inventory of 309 damaged
health facilities, 42 damaged ambulances, and 7 evacuated hospitals.

This paper reads that record as **one argument in three movements**, each with a
single, standard statistical tool:

1. **The war killed fast and early.** Most of the documented dying happened in
   the first six weeks, before the health system could adapt — a claim about the
   *distribution of mortality in time* (means comparison).
2. **The system then lost its ability to absorb further shocks.** As facility
   damage accumulated, each additional strike was associated with more deaths,
   not fewer — a claim about *how the cost of a strike changed* as the system
   degraded (moderation).
3. **The deaths we can count are only a floor.** Everything the first two
   movements measure is *direct, reported* death; the literature is unanimous
   that the indirect tail — the ward-side dying that never enters a strike-day
   tally — is several times larger (scenario projection).

The three are not independent observations that happen to sit in the same paper.
They are the same story told from three distances. The front-loading (movement 1)
is what placed an enormous, sudden burden on the health system before it had any
opportunity to adapt. The resilience erosion (movement 2) is what that system
did over the following months — gradually running out of the slack that lets a
hospital absorb a bad night. And the indirect floor (movement 3) is the toll of
those two processes together, most of which never reaches a count. Read in that
order, the projection in movement 3 stops looking like a theoretical estimate
and starts looking like the expected consequence of the mechanism the first two
movements document.

Two results from earlier in the series discipline the reading. The dataset's own
methods paper argues that in this war's information environment, casualty figures
are contested political facts, not clean measurements (Thomas et al. 2026,
§6.4–6.5); we therefore treat every direct toll as an interval, never a point,
and carry both internal accountings forward. And Paper 1 established that raw
daily tempo is a poor proxy for lethality; we take that seriously by never
resting the argument on tempo alone. What follows is deliberately built from the
plainest tools in the behavioral-statistics kit — a means comparison, an
interaction, and an arithmetic projection — because the point is not statistical
sophistication but legibility: an argument a health ministry, a journalist, or a
ward nurse can follow number by number and check line by line.

## 2. Data and methods

**Source and unit.** All analyses use the frozen v1.2 research release of the
IranWar.ai Event-Level Research Dataset (4,612 event rows; Days 0–170; Thomas et
al. 2026), pinned so the paper reproduces byte-for-byte. The unit of analysis is
the conflict-day (N = 170; Day 1 = 2026-02-28). The four-phase structure follows
Paper 1: **Major Combat** (Days 1–40), **First Ceasefire** (41–129),
**Resumption** (130–152), and **Diplomatic Pause** (153–170).

**Outcomes.** Daily estimated deaths by faction come from the dataset's casualty
file (170 days × 5 factions; daily, not cumulative): Iranian civilian (primary;
543 total), Iranian military (2,623), Lebanese all-category (2,993), US military
(20), Israeli military (34). Cumulative dashboard snapshots (Iranian killed,
Lebanese killed, children killed, displaced) provide reference series. The two
internal accountings disagree — the summed daily series runs 14.8% (Iran) and
43.9% (Lebanon) below the terminal snapshots — and we carry both forward as
bounds (Section 5).

**Exposure and degradation.** Strike tempo is the count of distinct strike-file
locations active per day plus discrete timeline events. Health-system
degradation is operationalized two ways. The **Health-System Stress Index
(HSSI)** is the cumulative count of 21 audited, discretely reported insult
events (facility attacks, workforce harm, WASH disruptions, supply and access
insults), built by keyword screen and then read and corrected row by row, with
the full audit trail (17 documented corrections) shipping in
`data/health_system_events.csv`. Because surveillance benchmarks show true
facility damage two orders of magnitude larger than 21 events, a second
operationalization anchors a piecewise-linear **facility-damage curve** to
institutional reports verified in the event stream: **31** hospitals damaged by
Day 15 (Iran Health Ministry-linked), **307** health facilities by Day 39 (WHO),
**309** by Day 170 (IRCS). Every degradation model runs on both curves; the
facility-damage curve is the primary moderator and the coarse HSSI the
sensitivity check.

**The three tools.** *Means comparison* (Finding 1): one-way ANOVA, Welch's
ANOVA, and Kruskal–Wallis across the four phases, with Holm-corrected pairwise
Welch t-tests, η²/ω², and Hedges' *g*; plus deaths-per-strike-location by phase
(Mann–Whitney). *Moderation* (Finding 5): centered strike tempo interacted with
each centered degradation curve, Y = Iranian civilian deaths, Newey–West (HAC,
7-day) standard errors because war days are serially dependent; probed by simple
slopes at ±1 SD and Johnson–Neyman boundaries, with kinetic-days-only and
phase-interaction sensitivity checks. *Scenario projection* (Finding 6):
literature indirect:direct ratios (1:1 floor, 3:1, 4:1 average, 15:1 upper;
Geneva Declaration Secretariat 2008) applied to both direct-toll bounds. All
computation is seeded (SEED = 42) and reproduces from `run_all.sh` in about
thirty seconds; α = .05 two-sided throughout. Full variable definitions are in
`docs/CODEBOOK_panel.md`; every design decision is in `docs/METHODS.md`.

## 3. Finding 1 — The war killed fast and early

*The distribution of mortality in time.*

By the daily series' account, the war killed 6,213 people across the five
tracked factions in 170 days — and **4,944 of them (79.6%) fell in the 40 days
of Major Combat**, which is **23.5%** of the war's duration (Table 1, Figure 1).
Mortality was not a smooth function of how long the war lasted. The cumulative
toll crossed **half** of its 170-day total by **Day 21** and **80%** by **Day
42**; a temporal-concentration ratio of 0.64 (0 would be a perfectly even war,
1 would be every death on the first day) puts the front-loading in a single
number. Iranian deaths averaged 78 per day during Major Combat and then fell to
**zero** for the entire 89-day First Ceasefire; the Lebanon front kept absorbing
about 13 deaths per day through that same ceasefire before the fronts inverted
at the Resumption. The deadliest single day of the war was its first.

**Table 1. Per-phase summary (daily means; totals in parentheses).**

| Phase | Days | Strikes/day | Iran civ/day (total) | Iran mil (total) | Lebanon/day (total) | All-faction total |
|---|---|---|---|---|---|---|
| Major Combat | 1–40 | 7.02 | 13.08 (523) | (2,602) | 44.52 (1,781) | 4,944 |
| First Ceasefire | 41–129 | 0.57 | 0.00 (0) | (3) | 13.48 (1,200) | 1,215 |
| Resumption | 130–152 | 2.35 | 0.87 (20) | (18) | 0.04 (1) | 43 |
| Diplomatic Pause | 153–170 | 0.00 | 0.00 (0) | (0) | 0.61 (11) | 11 |
| Full war | 1–170 | 2.27 | 3.19 (543) | (2,623) | 17.61 (2,993) | 6,213 |

The phase differences are enormous by behavioral-science standards, not a
close call dressed up with stars. For all-faction daily killed, F(3,166) = 172.3,
*p* < .001, **η² = 0.76** (ω² = 0.75) — phase alone explains three-quarters of
the day-to-day variance in mortality; Welch's F and Kruskal–Wallis agree.
Holm-corrected pairwise contrasts put Major Combat above every other phase at
Hedges' **g = 3.1–3.4** (all *p* < .001), a gulf several times what clinical
trials are built to detect. And the *yield* of each strike collapsed across
regimes: on strike days, Iranian deaths per distinct strike location averaged
**15.4** during Major Combat and **0.7** at the Resumption — a **95% decline**
(Mann–Whitney U = 623, *p* < .0001, *g* = 1.33). The opening campaign, against an
unprepared population and an intact urban target set, did almost all of the
war's direct killing.

**Why this matters for what follows.** Front-loading is not only a fact about
the fighting; it is a fact about the *burden placed on the health system*. The
system met the single largest wave of casualties of the entire war in its first
six weeks — before there was any opportunity to reinforce, disperse, resupply,
or adapt. Everything the health system did for the remaining 130 days, it did
while already absorbing the damage of that opening blow. That is the setup for
Finding 5.

## 4. Finding 5 — The system lost its ability to absorb shocks

*How the cost of a strike changed as the system degraded.*

There are two ways to ask whether strikes got "more deadly" over the war, and
they have opposite answers because they are different questions. The *average*
yield per strike fell 95% (Finding 1) — early strikes caught an unprepared,
densely settled population, and over time people sheltered, fled, and the intact
high-value target set was depleted. But the clinically important question is
*marginal*: holding the moment fixed, at a given level of accumulated damage,
what did **one more** strike cost in lives? The resilience-erosion hypothesis
(Kruk et al. 2015) predicts that answer should **grow** as the system degrades,
because surviving a blast injury depends on intact trauma care — a functioning
theatre, blood, power, staff — and each of those is exactly what sustained
bombardment removes.

We test it with an interaction model: Iranian civilian deaths regressed on
centered strike tempo, centered facility damage, and their product, with
Newey–West standard errors. The interaction is positive and significant
(b₃ = 0.0145, HAC *p* = **.006**). Read through simple slopes, the association
between one more strike location and same-day civilian deaths **steepens as
damage accumulates** (Table 2, Figure 2):

**Table 2. Simple slope of civilian deaths on strike tempo, by accumulated facility damage (full sample, HAC covariance).**

| Accumulated facility damage | Slope (deaths per strike location) | *p* |
|---|---|---|
| Low (−1 SD; early war) | 0.18 | .44 (n.s.) |
| Mean | 0.63 | .025 |
| High (+1 SD; late war) | **1.07** | **.006** |

The marginal cost of a strike roughly **sextuples** across the observed damage
range, from a slope indistinguishable from zero when the system was intact to
about one civilian death per additional strike location once it was heavily
degraded; the Johnson–Neyman boundary indicates significance for all but the
lowest-damage early days. This is the clinical intuition made quantitative: *a
functioning hospital can absorb one bad night, but after enough bad nights it
cannot absorb much more.* The same strike that a health system shrugs off on Day
10 can become catastrophic on Day 90, because the buffer is gone.

Two checks guard the reading. First, the coarse 21-event HSSI moderator points
the **same way** but does not reach significance (interaction *p* = .32; slopes
0.45 → 0.82) — we report both operationalizations rather than selecting the
favorable one, and the honest summary is "consistent, one specification
significant." Second, and more important: is this just a generic late-war regime
shift dressed as damage? A phase-interaction variant says no. Once the
Resumption's far lower baseline is absorbed (−10.7 deaths/day, *p* < .001), the
strike slope does **not** differ between Major Combat and the Resumption
(interaction *p* = **.89**). The steepening tracks the *damage curve*
specifically, not merely the passage into a later phase — which is what the
resilience account, and not a bare time-trend, predicts.

This is effect-modification evidence, not mechanism proof. Accumulated damage is
confounded with everything else that changed over 170 days — munitions, tactics,
sheltering, reporting practices — and no observational model can fully separate
them. But its practical reading deserves emphasis: **late-war "low-intensity"
operations were not low-cost per event.** By the Resumption, each strike was
landing on a system with almost no slack left to keep its victims alive. And the
direct-death series we are modeling is structurally blind to the mechanism's
*main* predicted effect — the indirect dying that follows a degraded system,
which is Finding 6.

## 5. Finding 6 — The counted dead are only a floor

*The uncounted tail.*

Everything in Findings 1 and 5 concerns **direct, reported** deaths. Conflict
epidemiology is unanimous that such counts are a floor, not a total: across
studied conflicts, indirect deaths — from disrupted care, displacement, water
failure, and disease — have exceeded direct deaths by roughly 3:1 to 15:1, with
~4:1 an often-cited cross-conflict average (Geneva Declaration Secretariat 2008;
Guha-Sapir & van Panhuis 2004; Checchi & Roberts 2008). This war's documented
degradation profile sits squarely in the class where the higher ratios appear:
309 damaged health facilities, 12 hospitals rendered inactive by Day 15 and 7
evacuated by Day 170, 127 healthcare workers killed in Lebanon by Day 93, three
destroyed desalination plants, 30–40% of power generation degraded by Day 11, a
blockade that seized medical supplies and idled the WHO's regional logistics hub.

We therefore **project** — explicitly as scenario arithmetic, not as an estimate
from these data. The documented direct toll at Day 170 is itself an interval
(the two internal accountings disagree), and we carry that interval through each
ratio (Table 3, Figure 3):

**Table 3. Projected total conflict deaths at Day 170 under literature indirect:direct ratios.**

| Ratio (indirect:direct) | Iran — indirect | Iran — total | Lebanon — indirect | Lebanon — total |
|---|---|---|---|---|
| 1:1 (floor) | 3,166–3,636 | 6,332–7,272 | 2,993–4,308 | 5,986–8,616 |
| 3:1 (low) | 9,498–10,908 | 12,664–14,544 | 8,979–12,924 | 11,972–17,232 |
| **4:1 (average)** | **12,664–14,544** | **15,830–18,180** | **11,972–17,232** | **14,965–21,540** |
| 15:1 (upper) | 47,490–54,540 | 50,656–58,176 | 44,895–64,620 | 47,888–68,928 |

At the 4:1 literature average, a documented Iranian floor of **3,166–3,636** implies
on the order of **15,800–18,200** total deaths; Lebanon's **2,993–4,308** implies
**15,000–21,500**. The projection's job is communicative discipline, not
precision: any public rendering of "about 3,600 dead in Iran" that does not mark
the number as a floor misrepresents what conflict epidemiology knows.

The WASH record makes the mechanism concrete at household scale — the level a
ward nurse recognizes. The Bonji intake's destruction alone removed drinking
water from **~10,000 people across 20 villages**; Kuwait, struck twice at its
Mina Abdullah power-and-desalination complex, draws **~90%** of its potable water
from desalination. These are not abstractions. A region that loses its water
treatment does not record its dead at the strike; it records them weeks later, as
diarrhoeal disease in infants and the frail, in facilities that may themselves be
damaged. **The four people who die for every one killed directly are the patient
whose operation is postponed because the theatre is gone, the mother who delivers
without a skilled attendant because the midwife has evacuated, and the dialysis
patient who misses session after session.** They do not appear in the strike
count. Finding 6 is the paper's estimate of how many of them there are — and its
argument that leaving them unstated is itself a failure of public-health
communication.

## 6. The three findings as one argument

The three findings are one story seen from three distances, and each makes the
next more legible.

**Front-loading set the terms.** The health system met the war's single largest
casualty wave in its first six weeks (Finding 1), against an intact target set
and an unprepared population. That is why the opening did most of the visible
killing — and why the system spent the rest of the war working through the
consequences of damage it absorbed before it could adapt.

**Resilience erosion is what happened next.** Through the long tail after Major
Combat, accumulated facility damage made each additional strike costlier at the
margin (Finding 5): the strike–death slope steepened roughly sixfold as the
buffer eroded. Average yields fell while marginal coupling tightened — not a
contradiction, but the two halves of one epidemiological process. The system was
being asked to do more with less exactly as its capacity to absorb shocks ran
down.

**The indirect floor is the toll of both.** A system that is hit hardest before
it can adapt, and then loses its slack as damage accumulates, produces indirect
mortality — the ward-side dying that follows disrupted care and destroyed water
(Finding 6). Because that dying never enters a strike-day tally, the documented
count is a floor, and the literature's ratios put the true total several times
higher. Seen after Findings 1 and 5, the 4:1 projection is not a free-floating
guess; it is the expected shape of the tail that front-loading and resilience
erosion together predict.

Put in one sentence: **the war killed fast and early, the health system
gradually lost its ability to absorb further shocks, and the deaths we can count
may only represent part of the real human toll.** Each clause is a finding; the
sentence is the paper.

Three operational implications follow, in the order the argument builds them.
First, the window for protecting civilians in an air war of this type is measured
in **days**, not months — most of the direct dying was over before Day 40, so
protection that arrives later arrives for a different, smaller problem. Second,
because the marginal cost of a strike rises as the system degrades, **sustaining
trauma-care and surveillance capacity during** active war has direct
life-saving value, not merely reconstructive value afterward; the WHO SSA-style
benchmarks that made our better degradation curve possible are themselves a
protective instrument. Third, WASH events are **early-warning markers of a
predictable morbidity tail** — destroyed desalination in a region that draws most
of its water from it defines a coming wave of indirect mortality that demands
pre-positioned response before the deaths arrive.

## 7. Limitations

(1) Ecological, day-level design: associations, not individual-level causal
effects. (2) The casualty series are contested estimates passing through
internet blackouts and strategic reporting; the parent paper quantifies the
cross-source spread (up to 3.8×). We run on the conservative daily series and
carry both internal bases through every cumulative figure, but no method
manufactures ground truth. (3) The 21-event insult register captures reported,
salient insults, not a facility census (WHO counted 307 by Day 39) — which is
why every degradation model also runs on the benchmark-anchored curve. (4)
Degradation is confounded with time; Finding 5 is effect-modification evidence
consistent with resilience erosion, not mechanism proof, and its coarser
operationalization does not reach significance. (5) No spatial analysis: strike
coordinates exist but hospital coordinates do not. (6) The indirect-mortality
figures are **projections under stated ratios**, falsifiable only by post-war
mortality surveys — which we hope this paper helps motivate.

## 8. Conclusion

Across 170 days, the 2026 US–Iran war did most of its documented killing in its
first six weeks, against a health system that had no chance to prepare; that
system then lost its capacity to absorb further shocks as its infrastructure
accumulated damage, so that each late strike cost more at the margin than an
early one; and the dead we can count are a floor several times below what
conflict epidemiology expects the war's full toll to be. None of this required
anything more exotic than a means comparison, an interaction, and an arithmetic
projection — three plain tools, read in order, against a dataset built to keep
its uncertainty visible. That legibility is the point. Against an information
environment designed to overwhelm, the useful response is not sophistication but
a chain of numbers a health worker can follow from the ward back to the data and
forward again to the sentence a ministry, a journalist, or a planner will repeat.

---

## Reproducibility

```bash
cd ResearchData/Paper2/v2
python3 -m pip install -r requirements.txt
bash run_all.sh     # regenerates panel, register, all focused tables and the 3 figures (~30 s)
```

Pinned input: `ResearchData/releases/v1.2/iranwar_event_dataset.csv` (the same
frozen release the parent paper uses). `src/04_synthesis.py` re-derives every
headline number in this manuscript from the regenerated tables and asserts each
against its reported value, so the pipeline fails loudly on any drift. Bootstraps
are seeded (SEED = 42). Design decisions: `docs/METHODS.md`; variable
definitions: `docs/CODEBOOK_panel.md`; plain-language walkthrough:
`docs/STUDENT_GUIDE.md`.

## References

- Checchi, F., & Roberts, L. (2008). Documenting mortality in crises: What keeps
  us from doing better? *PLoS Medicine*, 5(7), e146.
- Geneva Declaration Secretariat. (2008). *Global Burden of Armed Violence.*
  Geneva.
- Guha-Sapir, D., & van Panhuis, W. G. (2004). Conflict-related mortality: An
  analysis of 37 datasets. *Disasters*, 28(4), 418–428.
- Hedges, L. V. (1981). Distribution theory for Glass's estimator of effect size
  and related estimators. *Journal of Educational Statistics*, 6(2), 107–128.
- Holm, S. (1979). A simple sequentially rejective multiple test procedure.
  *Scandinavian Journal of Statistics*, 6(2), 65–70.
- Jawad, M., Hone, T., Vamos, E. P., Cetorelli, V., & Millett, C. (2020).
  Implications of armed conflict for maternal and child health. *PLoS Medicine*,
  18(9), e1003810.
- Kruk, M. E., Myers, M., Varpilah, S. T., & Dahn, B. T. (2015). What is a
  resilient health system? Lessons from Ebola. *The Lancet*, 385(9980),
  1910–1912.
- Kruk, M. E., et al. (2017). Building resilient health systems: A proposal for a
  resilience index. *BMJ*, 357, j2323.
- Levy, B. S., & Sidel, V. W. (2008). *War and Public Health* (2nd ed.). Oxford
  University Press.
- Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite,
  heteroskedasticity and autocorrelation consistent covariance matrix.
  *Econometrica*, 55(3), 703–708.
- Thomas, J. E., Alpysbekova, A., Osei Mensah, E., Masara, N., & Sharma, P.
  (2026). IranWar.ai: An open-source event-level dataset of the 2026 US–Iran
  conflict. Preprint, github.com/jethomasphd/WarTheater.
- IranWar.ai Research Agenda, Paper 2. (2026). *The Direct Toll Is a Floor.*
  github.com/jethomasphd/WarTheater, `ResearchData/Paper2/` (the parent paper).
- World Health Organization. Surveillance System for Attacks on Health Care
  (SSA). Geneva: WHO.

*Dataset citation:* IranWar.ai Event-Level Research Dataset, v1.2 (2026). Days
1–170. github.com/jethomasphd/WarTheater, `ResearchData/releases/v1.2/`.
