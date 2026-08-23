# First-Author's Guide to Paper 2

*A plain-language walkthrough of every analysis in this paper — what it is, why we chose
it, how to read the output, and what to say when someone asks about it. Written for a
public-health graduate student taking first authorship of this manuscript.*

You do not need to write any code to own this paper. You need to be able to (1) run one
command, (2) explain every number, and (3) defend every decision. This guide gets you
there. Read it side-by-side with `docs/METHODS.md` (the formal version of the same
decisions) and the manuscript.

---

## 0. Run it yourself first

```bash
cd ResearchData/Paper2
python3 -m pip install -r requirements.txt
bash run_all.sh
```

Roughly a minute later you have every table (`output/tables/`) and figure
(`output/figures/`) in the paper, regenerated from the raw event dataset. Nothing in the
manuscript exists that this command does not produce. If a committee member asks "where
does Table 4 come from?", the answer is: `src/04_mediation.py`, and you can show them.

**Why this matters:** this is what "reproducible" means in practice. Your results section
is not a claim about what we once saw — it is a recipe anyone can re-run.

---

## 1. The study in one paragraph

We follow 170 days of war. Each day we measure how much bombing happened (`strikes`), how
much of it hit civilian-facing infrastructure like hospitals, water plants, and power
(`strikes_civfac`), how degraded the health system had become by that day (two versions:
our audited 21-event insult index, and a curve anchored to WHO/ministry facility-damage
reports), and how many people were reported killed (`iran_civ`, `leb_all`, ...). Then we
ask four questions with four standard tools: Did mortality differ across the war's phases?
(**means comparison**) Does bombing intensity predict same-day deaths? (**regression**)
Does the civilian-facing share of the bombing *carry* that relationship? (**mediation**)
Does a degraded health system *change* the strike–death relationship? (**moderation**)
Finally we project what the direct death counts imply about the deaths we *cannot* see
(**indirect mortality projection**), and we take the disagreements between casualty
sources seriously as data (**source-divergence analysis**).

---

## 2. Tool by tool

### 2.1 Means comparison (script `02`, Tables 2a–c, Figure 4)

**What it is.** Comparing average daily deaths across the four phases (ANOVA family), and
between strike days and quiet days (t-tests).

**Why we chose it.** The war has a clear phase structure (combat → ceasefire → resumption
→ pause). "Did mortality differ by phase?" is the most natural first question, and ANOVA
is the standard tool for comparing more than two group means.

**How to read it.**
- *F and p* — how much the phase means differ relative to within-phase noise. Our F values
  are enormous (e.g. F(3,166) = 172 for total daily killed) because Major Combat carries
  ~80% of all deaths.
- *η² (eta-squared)* — proportion of variance explained by phase: 0.76 for total killed.
  In behavioral research anything above 0.14 is "large."
- *Welch / Kruskal–Wallis* — the same question under fewer assumptions (unequal variances /
  no normality). We report them because daily death counts are skewed and one phase has
  literally zero variance (no Iranian deaths at all during the ceasefire — Welch is
  "undefined" there, and the table says so rather than hiding it).
- *Pairwise Welch t-tests with Holm correction* — which specific phases differ. Holm
  protects us from fishing across 6 comparisons.
- *Hedges' g* — the size of each difference in standard-deviation units, corrected for
  small samples. Combat vs ceasefire g ≈ 3.4 is a gigantic effect (clinical trials
  celebrate g = 0.5).

**One sentence for the paper:** phase explains most of the variance in daily mortality;
the war's political regime, not its day-to-day tempo, is the first-order determinant of
who dies when.

### 2.2 Correlation and regression (script `03`, Tables 3a–c)

**What it is.** Pearson/Spearman correlations among the daily series, then ordinary least
squares (OLS) regression predicting daily deaths from strike tempo, split into
military-facing vs civilian-facing components, plus retaliation.

**Why we chose it.** Correlations describe the raw co-movement; regression asks the
sharper question — *which component* of the bombing is associated with civilian deaths,
holding the others constant?

**How to read it.**
- The key row is `strikes_civfac` in model M3: **b ≈ 2.07 (p < .001)** — each additional
  civilian-facing strike location on a given day is associated with about two additional
  Iranian civilian deaths that day, holding military-facing strikes and retaliation
  constant. Military-facing tempo has *no* positive association (b ≈ −0.47, n.s.).
- *HAC (Newey–West) standard errors*: consecutive war days are not independent (violence
  clusters), which breaks the usual standard-error formula. HAC standard errors fix the
  *standard errors* (not the coefficients) for serial dependence up to 7 days.
- *Negative-binomial robustness*: deaths are counts (0, 1, 2, …), not continuous. NB2
  re-fits the same model respecting that. Same story: civilian-facing tempo carries an
  incidence-rate ratio of 1.62 per location (p < .001) — a 62% higher expected death count
  per additional civilian-facing location.

**Watch out:** Paper 1 (finding 8) showed total tempo is a poor lethality proxy. Our
result is the refinement: tempo *disaggregated by target class* is informative — the
civilian-facing component is where mortality lives.

### 2.3 Mediation (script `04`, Table 4, Figure 5)

**What it is.** The classic single-mediator model (Baron & Kenny's logic, tested the
modern way with a bootstrap). X = military-facing strike tempo, M = civilian-facing strike
tempo, Y = Iranian civilian deaths. Does the military tempo–death association run
*through* the widening of targeting into civilian-facing infrastructure?

**Why we chose it.** It formalizes a substantive public-health claim: military bombing
does not kill civilians *as* military bombing; it kills civilians insofar as heavy-tempo
days widen the target set into infrastructure civilians depend on. X and M are separate
counts (no overlap), which keeps the model honest.

**How to read it.**
- *Path a* (X→M) = 0.33: heavier military-facing days have more civilian-facing locations.
- *Path b* (M→Y | X) = 3.07: civilian-facing tempo predicts deaths holding X constant.
- *Indirect effect a×b* = **1.02, 95% bootstrap CI [0.60, 1.84]** — the CI excludes zero,
  so the indirect path is statistically reliable. About **68% of the total association is
  mediated** (c = 1.50 → c′ = 0.48).
- *Bootstrap* = re-run the two regressions on 10,000 resampled versions of the 170 days
  and read the middle 95% of the a×b estimates. It beats the old Sobel test because a×b
  is not normally distributed. Seeded (42), so everyone gets the same CI.

**Be ready to say (and the manuscript says it):** same-day mediation on a time series is
an *associational decomposition*, not causal proof — and the full-sample effect partly
reflects the war switching on and off. Inside Major Combat only (n = 40) the indirect CI
touches zero. We show both; that is the honest version.

### 2.4 Moderation (script `05`, Tables 5a–b, Figure 6)

**What it is.** An interaction model: does the strike→death slope *change* as the health
system degrades? Y = civilian deaths, X = strikes (centered), W = degradation (centered),
plus X×W.

**Why we chose it.** It is the direct statistical translation of the resilience question
(Kruk et al.): a degraded system should convert the same kinetic dose into more deaths
(interaction > 0). The rival hypothesis (harm front-loading: early strikes are the
deadliest, populations adapt) predicts the opposite.

**How to read it.**
- With the **benchmark-anchored facility-damage curve** as W: interaction b₃ = 0.0145,
  **p = .006**. *Simple slopes*: at low damage the strike–death slope is 0.18 (n.s.); at
  mean damage 0.63 (p = .02); at high damage **1.07 (p = .006)**. The marginal association
  per additional strike location roughly *quintuples* across the observed damage range.
- With the **21-event HSSI** as W: same direction, not significant (p = .32). We report
  both — the two operationalizations bracket the measurement uncertainty.
- *Johnson–Neyman* tells you the exact degradation level where the slope becomes
  significant.
- The W main effect is strongly negative: late-war days have far *fewer* deaths overall.
  Rising marginal slope + falling baseline is not a contradiction — see §2.6.

**Crucial nuance (committee-proof):** degradation accumulates with time, so W is
confounded with everything else that changed over the war (munitions, tactics, sheltering,
reporting). The moderation is an observed effect-modification pattern consistent with
resilience erosion — evidence, not proof.

### 2.5 Indirect mortality projection (script `06`, Tables 6a–b, Figure 7)

**What it is.** Scenario arithmetic, deliberately *not* a model. Conflict epidemiology
consistently finds 3–15 indirect deaths (disease, disrupted care, displacement, water
failure) per direct death, with ~4:1 an often-cited cross-conflict average (Geneva
Declaration 2008). We apply R ∈ {1, 3, 4, 15} to the documented direct toll — computed on
both internal bases (daily-series sum and dashboard snapshot), so the dataset's own
measurement spread carries into the projection.

**How to read it.** Iran: 3,166–3,636 documented direct deaths → at 4:1, a projected
~12,700–14,500 indirect deaths (~15,800–18,200 total). The point is not the specific
number; it is that **the documented count is a floor**, and the plausible range under
standard ratios is large. Say "projection," never "estimate."

### 2.6 Two lethality findings that look contradictory (they aren't)

- Table 2c: deaths *per strike location* collapsed from 15.4 (Major Combat) to 0.7
  (Resumption) — the **average yield** per strike fell 95%. Mortality was front-loaded.
- Table 5: the **marginal slope** (extra deaths per extra strike, within a day, at a given
  degradation level) *rose* with facility damage.

The ratio divides total deaths by total strikes and is dominated by the early mass-
casualty days (the Minab school strike alone killed ~150–170 on Day 1). The slope asks a
conditional question within the model. Averages fell; marginal coupling tightened. The
manuscript walks through this; internalize it — it is the most likely "gotcha" question.

### 2.7 Source divergence & confidence weighting (script `07`, Tables 7a–c, Figure 8)

**What it is.** The counter-technology extension (the source preprint, §6.4–6.5, §7.3.2).
Instead of treating disagreement between casualty sources as noise, we measure it: at Day
45 the cross-source spread on Iran's cumulative toll was **3.8×** (Health Ministry ~2,000
vs Hengaw 7,650), and — remarkably — the *civilian* counts diverge in the **opposite
direction** from the totals (HRANA counts more civilians than Hengaw while counting far
fewer total). Each source's number serves its institutional position; the divergence is a
political fact, not a data-cleaning problem. The dashboard itself re-anchored its
cumulative metric on Day 57 (9,226 → 3,375, −63%) when Iran's forensic institute published
its count — the tracking series wears the source war on its sleeve.

Then we re-run the core regression three ways: all rows; HIGH-confidence rows only;
confidence-weighted (1.0/0.7/0.4). The civilian-facing coefficient stays 1.6–2.4 across
variants (significance drops in the HIGH-only variant because we discard data, i.e. we
lose power, not direction). **This is what the dataset's transparency infrastructure is
for** — because every row carries a confidence rating, we can show the finding does not
depend on the shakiest rows.

---

## 3. Answers to the questions you will be asked

**"Why only 21 health-system events when WHO counted 307 damaged facilities?"**
Because our register counts *discretely reported, nationally salient* insult events in the
event stream, not a facility census — and we say so. That is why every degradation model is
run twice, the second time with the WHO/ministry benchmark curve. The honest term for the
HSSI is "trajectory proxy."

**"Aren't the casualty numbers unreliable?"**
They are contested — and we quantify exactly how contested (3.8× at the worst), analyze
the disagreement as data, run the models on the conservative series, and show robustness
under confidence weighting. Contrast this with pretending a single authoritative number
exists; no such number exists in an active war.

**"Is this causal?"**
No, and the paper never says it is. Ecological day-level associations, same-day mediation
as decomposition, moderation as observed effect modification. The design cannot support
counterfactual claims and doesn't make them.

**"Why is the ANOVA so extreme?"**
Because the phenomenon is extreme — the political regime turned mortality on and off.
Large F values are the *finding*, not an artifact: violence in this war was governed by
regime, not accumulation.

**"What would strengthen this paper?"**
Hospital coordinates (WHO EMRO registry) for spatial analysis; morbidity/utilization data;
post-war mortality surveys to convert the projection into an estimate. All named in
future-work.

---

## 4. Where everything lives

| You need | Location |
|---|---|
| The paper | `manuscript/paper2_healthcare_collapse.md` (+ `.docx`) |
| Any number in the results | `output/tables/t0*.csv` (script number = table number) |
| Any figure | `output/figures/fig*.png` (PDF versions for submission) |
| Why we made a decision | `docs/METHODS.md` |
| What a variable means | `docs/CODEBOOK_panel.md` |
| The 21 events + audit trail | `data/health_system_events.csv` |
| The daily panel | `data/panel_daily.csv` |

Welcome to first authorship. Run the pipeline, read the outputs against the manuscript
until every number is yours, and bring your public-health judgment to the discussion
section — that is the part only you can write.
