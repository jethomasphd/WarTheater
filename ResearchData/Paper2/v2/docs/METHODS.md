# Methods and design decisions — Paper 2, v2 (three-findings edition)

This document records the analytical choices behind the three findings this
edition develops, in enough detail to audit or contest them. It is deliberately
narrower than the parent paper's `../../docs/METHODS.md` (which covers all eight
findings and every tool); nothing here departs from the parent's methods — the
same panel and the same models are run against the same frozen release, so every
number matches. What follows is the subset a first author needs to defend
Findings 1, 5, and 6 at a committee or in review.

## 1. Data source and pinning

- **Input:** `ResearchData/releases/v1.2/iranwar_event_dataset.csv` (frozen
  release; Days 1–170; 4,612 event rows). Pinned to the frozen release, not the
  moving root dataset, so the analysis reproduces byte-for-byte regardless of
  later dataset versions. Override with the `IRANWAR_DATASET` environment
  variable. This v2 edition lives one directory deeper than the parent and
  writes its own `data/`, `output/tables/`, and `output/figures/`, but reads the
  *same* release — hence identical numbers.
- Day 1 = 2026-02-28. All stochastic steps are seeded (`SEED = 42`); no network
  or wall-clock dependence.

## 2. Study design

A retrospective **ecological time-series study** with the **conflict-day** as
the unit of analysis (N = 170). All variables are population-level daily
aggregates; no individual-level data exist in the source and no individual-level
inference is made. The four documented phases follow Paper 1: Major Combat
(1–40), First Ceasefire (41–129), Resumption (130–152), Diplomatic Pause
(153–170).

## 3. Variables used by the three findings

- **Outcomes.** `iran_civ` (Iranian civilian estimated killed/day; primary for
  Findings 5 and 6) and `killed_total` (all-faction sum; primary for Finding 1),
  from `casualties.json` daily rows. Cumulative dashboard snapshots
  (`snap_iranian_killed`, `snap_lebanese_killed`, `snap_children_killed`) give
  reference/terminal series. **Internal divergence is carried forward, not
  hidden:** the summed daily series runs below the terminal snapshots (Iran 3,166
  vs 3,636, +14.8%; Lebanon 2,993 vs 4,308, +43.9%); both bounds enter Finding 6.
- **Exposure.** `strikes` — distinct strike-file locations active per day plus
  discrete timeline events (Paper 1's operationalization). Finding 5 uses total
  strike tempo as X.
- **Degradation (two curves).** `hssi_pct` — the cumulative count of 21 audited
  insult events, min–max normalized; a *trajectory proxy*, not a facility census.
  `facil_damage_pct` — a piecewise-linear curve through institutionally reported
  cumulative facility-damage counts verified in the event stream (31 by Day 15,
  Iran Health Ministry-linked; 307 by Day 39, WHO; 309 by Day 170, IRCS),
  normalized to its Day-170 level. The facility-damage curve is the **primary**
  moderator for Finding 5 and the HSSI a **sensitivity** check; both are always
  reported. Full variable definitions: `CODEBOOK_panel.md`.

The audited health-system register (`data/health_system_events.csv`) ships all
82 screened rows with their `audit_action`, `audit_note`, and `counted` flags;
17 corrections (6 reclassifications, 6 exclusions, 5 same-incident merges) are
recorded by event id, and `00_build_panel.py` verifies at run time that each
audited event still exists and still contains its anchoring text, so silent
upstream drift fails loudly.

## 4. Finding 1 — front-loading (means comparison)

*Script:* `01_frontloading.py`.

- **Phase comparison.** One-way ANOVA, Welch's ANOVA (flagged undefined where a
  phase has zero variance — Iranian civilian deaths are uniformly 0 in two
  phases), and Kruskal–Wallis, with η² and ω². Pairwise contrasts use Welch
  t-tests under Holm correction with Hedges' *g*. The enormous F values
  (η² = 0.76 for all-faction killed) are the finding, not an artifact: the
  political regime, not day-to-day tempo, governs when people die.
- **Temporal concentration.** Days are ordered chronologically; at each fraction
  of elapsed war-time we record the fraction of the war's total documented
  deaths already accrued. The Major-Combat cut-point (Day 40) yields the headline
  79.6%-of-deaths / 23.5%-of-days. The concentration ratio (2 × area under the
  curve − 1) summarizes front-loading in a single number (0 = evenly paced war,
  → 1 = all deaths on Day 1); here it is 0.64. Because days are in calendar
  order, this measures concentration *in time*, not inequality across an
  unordered set — it is deliberately not called a Lorenz/Gini statistic.
- **Per-strike lethality.** On strike days, Iranian deaths per distinct strike
  location by phase; Major Combat vs Resumption by Mann–Whitney U. Reported as
  supporting context for the *average-yield* half of the story reconciled in
  Finding 5. The collapse is 15.4 → 0.7 (95%), U = 623, p < .0001, Hedges
  g = 1.33. (An earlier parent draft printed g = 2.16 for this contrast; the
  regenerated value is 1.33 and is used here.)

## 5. Finding 5 — resilience erosion (moderation)

*Script:* `02_resilience_erosion.py`.

- **Model.** `iran_civ` ~ b0 + b1·strikes_c + b2·W_c + b3·(strikes_c × W_c),
  with strikes and the moderator W mean-centered so b1 is the simple slope at
  mean damage. **Newey–West (HAC, 7-day) standard errors** because daily war
  series are serially dependent; centering does not change the interaction, only
  the interpretability of the lower-order terms.
- **Probing.** Simple slopes of deaths on strikes at W = mean ± 1 SD, each with
  its own HAC standard error derived from the coefficient covariance; the
  Johnson–Neyman boundary is the moderator value where the strike slope's |t|
  crosses the critical value (Aiken & West 1991).
- **Two guards against over-reading.**
  1. *Two operationalizations.* The facility-damage curve gives a significant
     positive interaction (b3 = 0.0145, p = .006); the coarse HSSI points the
     same way but is not significant (p = .32). Both are reported; the honest
     summary is "consistent, one specification significant."
  2. *Is it just a late-war regime shift?* A phase-interaction variant regresses
     `iran_civ` on centered strikes, a Resumption dummy, and their product
     (Major-Combat + Resumption days only). The strike × Resumption interaction
     is null (p = .89) once the Resumption's lower baseline (−10.7 deaths/day) is
     absorbed — so the steepening tracks the *damage curve* specifically, not a
     generic passage into a later phase.
- **Interpretation.** Effect-modification evidence consistent with resilience
  erosion, **not** mechanism proof: accumulated damage is confounded with
  everything else that changed over 170 days (munitions, tactics, sheltering,
  reporting). The direct-death outcome is also structurally blind to the
  mechanism's main predicted effect, indirect mortality — which is why Finding 6
  exists.
- **Average vs marginal (the most likely committee question).** Finding 1's
  per-strike lethality *fell* 95% (average yield, dominated by the early
  mass-casualty days); Finding 5's *marginal* slope *rose* with damage
  (conditional, within-model). These are different quantities and not in
  tension — averages fell while marginal coupling tightened.

## 6. Finding 6 — the indirect floor (scenario projection)

*Script:* `03_indirect_floor.py`.

- **Not a model.** Deliberately scenario arithmetic. Literature indirect:direct
  ratios (1:1 floor, 3:1 low, 4:1 cross-conflict average, 15:1 upper; Geneva
  Declaration Secretariat 2008; Guha-Sapir & van Panhuis 2004; Checchi & Roberts
  2008) are applied to the documented direct toll. Each ratio is computed on
  **both** internal direct-toll bounds (daily-series sum = lower; dashboard
  snapshot = upper), so the dataset's own measurement spread carries into the
  projection. Say "projection," never "estimate."
- **WASH exposure.** Population-at-risk figures are quoted verbatim from the
  source events (e.g. the Bonji intake, ~10,000 people across 20 villages), each
  anchored to a dataset event id verified at run time. They make the indirect
  mechanism concrete at household scale but are not themselves a mortality
  estimate.

## 7. Reproducibility and self-checking

`run_all.sh` runs 00 → 01 → 02 → 03 → 04 in order (~30 s). `04_synthesis.py`
re-derives every headline number from the regenerated tables and **asserts** each
against its manuscript value (79.6%/23.5%; slopes 0.18/0.63/1.07; interaction
p = .006; Iran 3,166–3,636 → 15,830–18,180), so the pipeline fails loudly if any
number drifts from the frozen dataset. Outputs: `output/synthesis.json` and
`output/tables/t0_headline_findings.csv`.

## 8. Limitations (short form; full text in the manuscript §7)

Ecological day-level associations, not causal effects; contested casualty series
(run on the conservative daily series, both bounds carried forward); a 21-event
register that is a trajectory proxy, not a facility census (hence the benchmark
curve); degradation confounded with time (Finding 5 is effect-modification, not
mechanism); no spatial analysis; and indirect-mortality figures that are
projections under stated ratios, falsifiable only by post-war mortality surveys.
