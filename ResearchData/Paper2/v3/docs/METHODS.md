# Methods and design decisions — Paper 2, v3

This document records the analytical choices behind the three findings in
enough detail to audit or contest them. It is written for the first author to
use when defending the paper. Where v3 departs from v2, the departure is marked
and explained in `CHANGES_FROM_V2.md`.

## 1. Data source and pinning

- **Input:** `ResearchData/releases/v1.2/iranwar_event_dataset.csv` (frozen
  release; Days 1–170; 4,612 event rows). Pinned so that the analysis
  reproduces exactly regardless of later dataset versions. Override with the
  `IRANWAR_DATASET` environment variable.
- Day 1 = 2026-02-28. Nothing in the pipeline is random and nothing uses the
  network or the clock.

## 2. Study design

A retrospective **ecological time-series study**. The unit of analysis is the
**conflict-day** (N = 170). All variables are daily aggregates for a population;
no individual-level data exist in the source and no individual-level claim is
made. The four phases follow Paper 1: Major Combat (Days 1–40), First Ceasefire
(41–129), Resumption (130–152), Diplomatic Pause (153–170).

## 3. Variables

- **Outcomes.** `killed_total` (all five factions added; Finding 1) and
  `iran_civ` (Iranian civilian deaths per day; Findings 2 and 3). Both are daily
  counts from `casualties.json`, not running totals. The dashboard's running
  totals (`snap_iranian_killed`, `snap_lebanese_killed`, `snap_children_killed`)
  are used only as the upper bound of the direct toll and in the accounting-gap
  analysis. The two accountings disagree (Iran 3,166 vs 3,636; Lebanon 2,993 vs
  4,308); both are carried, never averaged.
- **Exposure.** `strikes`: distinct strike-file locations active that day plus
  discrete timeline strike events (Paper 1's definition).
- **Damage, two measures.** `facil_damage_pct`: a piecewise-linear curve through
  institutional cumulative counts of damaged health facilities found in the
  dataset (31 by Day 15; 307 by Day 39; 309 by Day 170), as a percentage of the
  Day-170 value. This is the **primary** measure. `hssi_pct`: the running count
  of 21 audited health-system insult events, scaled 0–100. This is the
  **secondary** measure and a check. The 21 events, the 82 screened rows, and
  the 17 documented corrections ship in `data/health_system_events.csv`;
  `00_build_panel.py` verifies at run time that every audited event still exists
  and still contains its anchor text.

Full definitions: `CODEBOOK_panel.md`.

## 4. Finding 1 — means comparison (`01_means_comparison.py`)

- **Shares.** Deaths in each phase as a share of all 6,213 documented deaths,
  against the phase's share of the 170 days. Cumulative curve: the day on which
  50%, 80%, and 90% of all deaths had occurred.
- **ANOVA.** One-way ANOVA across the four phases for each outcome, with η² and
  ω². Welch's ANOVA is reported as a check because phase variances differ
  greatly; it is undefined for Iranian civilian deaths (two phases are all
  zeros) and the table says so.
- **Pairwise contrasts.** Welch t-tests for the six phase pairs, Holm-adjusted;
  difference in means with a 95% CI (Welch–Satterthwaite df); Hedges' g.
- **Deaths per strike location.** On strike days, Iranian deaths (civilian +
  military) divided by strike locations. Major Combat vs Resumption by Welch
  t-test with g and a CI; Mann–Whitney kept as a check column because the values
  are skewed.
- **Why "means comparison" is enough.** The effect sizes are enormous (η² =
  0.76; g = 3.1–3.4). No refinement of the test changes the conclusion. The
  design question is not "is there a difference" but "how concentrated in time
  was the dying", which the shares and the cumulative curve answer directly.

## 5. Bridge — correlation (`02_correlation.py`)

- **Periods.** Defined by the damage curve, not by phase: A = Days 1–15 (0 → 31
  facilities), B = Days 16–39 (31 → 307), C = Days 40–170 (307 → 309). The
  Resumption (Days 130–152) is reported as a subset of C because it is the only
  late period with sustained strikes.
- **Statistics.** Pearson r with p; Spearman's rho as a rank check; simple
  regression slope of deaths on strikes with a 95% CI. Fisher's r-to-z test
  compares correlations between periods. Everything is repeated on strike days
  only.
- **Why not tertiles of the damage variable?** Because the curve is saturated:
  131 of 170 days sit at 99–100%. Rank-based tertiles would split the flat part
  of the curve into meaningless bands. Periods anchored to the benchmark counts
  are interpretable and were fixed before the analysis was run.
- **What the bridge shows and does not show.** r rises from −0.41 (n.s.) to
  +0.52 across the periods, and the A-vs-C difference is significant (p = .001).
  The within-period slopes do not rise monotonically (−1.03, +0.44, +0.29); what
  changes is how consistently deaths track strikes. The manuscript says this
  explicitly.

## 6. Finding 2 — regression with an interaction (`03_regression.py`)

- **Models.** M1: deaths on strikes. M2: adds damage. M3: adds the product of
  mean-centered strikes and mean-centered damage. Outcome: Iranian civilian
  deaths per day; all 170 days.
- **Standard errors.** Ordinary and Newey–West HAC (7-day lag) are both reported
  for every coefficient. The residual lag-1 autocorrelation of M3 is 0.19
  (Durbin–Watson 1.6); the raw series are strongly autocorrelated (0.73 for
  deaths, 0.71 for strikes). HAC p-values are the ones quoted. The interaction is
  significant under both (HAC p = .006; ordinary p < .001).
- **Simple slopes at observed levels (change from v2).** The slope of deaths on
  strikes is evaluated at 31, 155, 232, and 307 damaged facilities (10%, 50%,
  75%, 99% of the final count), each with its HAC standard error from the
  coefficient covariance. The mean ± 1 SD convention is not used because mean +
  1 SD (116%) is outside the observed range; the v2 rows are still written to
  the table for comparison and marked.
- **Threshold.** The lowest damage level at and above which the slope is
  significant at α = .05 (Johnson–Neyman): about 238 facilities (77%), reached on
  Day 33.
- **Checks.** Strike days only; kinetic days only; Major Combat only (Days
  1–40; HAC p = .012, ordinary p = .075; low power with 40 days); Days 1–60; the
  HSSI as the damage measure (same sign; HAC p = .32; ordinary p = .078; slope
  at the top of the index +0.80, p = .023); HSSI on strike days only (HAC p =
  .049); and the phase check (strikes × Resumption on Major Combat + Resumption
  days: p = .89, with the Resumption's baseline 10.7 deaths/day lower).
- **Interpretation, stated carefully.** Effect modification consistent with a
  health system losing its ability to absorb shocks. Not mechanism proof: damage
  is confounded with time. The model is linear and predicts a negative slope at
  the lowest damage levels, which mirrors the negative within-period
  correlation in Days 1–15 rather than a protective effect of strikes. The
  outcome is direct deaths, so the mechanism's main predicted effect (indirect
  deaths) is invisible here by construction.
- **Average vs marginal (the most likely committee question).** Finding 1's
  deaths per strike location *fell* 95.6% between Major Combat and the
  Resumption. That is an average yield, dominated by the early mass-casualty
  days. Finding 2's slope is a marginal, conditional quantity inside a model:
  at a given damage level, what did one more strike location cost. Averages fell;
  the marginal coupling tightened. Both are true.

## 7. Finding 3 — the floor (`04_floor.py`)

- **What the series records.** Welch t-test and g for deaths per day on strike
  days (n = 89) vs non-strike days (n = 81), for three outcomes. The First
  Ceasefire block: 89 days, 0 Iranian civilian deaths, 34 strike days, 8 health-
  system insult events, damage at 99–100%.
- **Accounting gap.** Summed daily series vs dashboard counter at milestone
  days (all of them observed snapshot days, flagged in the table) and phase by
  phase: deaths added by the daily series vs change in the counter. The Iran
  re-anchoring signature (9,226 on Day 56 → 3,375 on Day 57) is asserted at run
  time, as in the parent paper.
- **Projection.** Literature ratios 1:1, 3:1, 4:1, 15:1 applied to both
  direct-toll bounds. Always called a projection. The 4:1 row is labelled a
  reference scenario; the manuscript presents the range first.
- **WASH rows.** Population figures quoted verbatim from source events, each
  anchored to an event id verified at run time.

## 8. Self-checks (`05_check_numbers.py`, `06_manuscript_tables.py`)

`05` re-derives every headline number from the tables and asserts it against
the manuscript's value; it writes `output/numbers.json`. `06` renders all eleven
manuscript tables from the CSVs and checks that `manuscript/paper2_v3.md`
contains each one verbatim. `run_all.sh` runs both; either failing stops the
pipeline.

## 9. Limitations (short form; full text in the manuscript §6)

Ecological day-level associations; contested casualty series (both bounds
carried); a 21-event register that is a proxy, hence the benchmark curve;
damage confounded with time; a linear model extrapolating at the low end; no
spatial analysis; projections that only a post-war mortality survey can test.
