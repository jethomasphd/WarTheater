# Methods and design decisions — Paper 1, Major Revision 1

This document records every analytical choice behind Major Revision 1 in enough detail to
audit or contest it. It complements the inline documentation in `src/`. Where a choice
responds to the reviewer memo, the memo point is named.

## 1. Data source, pinning, and integrity

- **Input:** `ResearchData/releases/v1.2/iranwar_event_dataset.csv` (frozen release; Days
  1–170, 2026-02-28 → 2026-08-16; 4,612 rows). The analysis is pinned to the frozen file and
  `src/util.py` verifies its MD5 (`9a2ac6b3afb7fbc2203ff248bac824fd`) before any script runs.
  A different input can be analysed deliberately with `IRANWAR_DATASET=/path/to.csv`, which
  skips the hash check and prints a notice.
- Day 1 = 2026-02-28 (`BASELINE_DATE = 2026-02-27`; war-day N = 2026-02-27 + N days).

## 2. Unit of analysis and intensity measures

The unit is the conflict-day (Days 1–170; 170 observations). The strike files expand each
location into one row per target × active day, so a raw row count over-weights multi-target,
multi-day locations. The **primary tempo** measures de-duplicate that expansion:

- `strikes` — distinct offensive locations (`source_record_id`) active on day *t* in the
  STRIKE domain, plus discrete STRIKE-domain timeline events (which carry no location id).
- `retal` — the analogous count for the RETALIATION domain.

Two alternatives are carried for robustness: raw event rows (`strikes_rows`, `retal_rows`)
and timeline-only discrete events (`strikes_tl`, `retal_tl`). Definitions:
`docs/CODEBOOK_panel.md`. The panel is asserted identical to the parent paper's panel.

## 3. Phases

| Phase | Days | Dates | Source of boundary |
|---|---|---|---|
| Major Combat | 1–40 | 2026-02-28 … 04-08 | narrative; endogenous break at Day 40 |
| First Ceasefire | 41–129 | 2026-04-09 … 07-06 | narrative |
| Resumption | 130–152 | 2026-07-07 … 07-29 | documented "ceasefire collapsed" (Jul 7); break at Day 131 |
| Diplomatic Pause | 153–170 | 2026-07-30 … 08-16 | documented "no US strikes" (Jul 30); break at Day 147 |

Narrative boundaries come from `strikes-iran.json` `_metadata.phase`. `KINETIC_END = 40`
defines the combat regime used as the primary estimation window.

## 4. Finding 1 — same-day reciprocity (`02_reciprocity_var.py`)

- Same-day Pearson correlation with a Fisher-z 95% CI; cross-correlation at lags −5…+5 with
  the ±1.96/√n no-association band.
- Bivariate VAR on `[strikes, retal]`, combat regime. Lag order by AIC/BIC/HQIC/FPE with
  `maxlags = 5`; all four select 0. A VAR(1) is then fitted (the minimum feasible lag) for
  the Granger F-tests in both directions.
- Orthogonalised impulse responses, horizon 12. **Error band (corrected).** statsmodels'
  `errband_mc(seed=…)` passes the same seed to every replication, so all replications are
  identical and the band collapses to a line; the parent paper's Figure 3 inherited that
  defect. `mc_errband()` in `02_reciprocity_var.py` draws a fresh seed per replication from
  one seeded generator (1,000 replications, seed 42), reproducing statsmodels' resimulation
  otherwise exactly. The resulting band includes zero from horizon 1 onward.

## 5. Finding 2 — regime-contingent coupling (`03_regime_coupling.py`)

- Same-day Pearson r within each phase with a Fisher-z CI. The pause has no strikes; the
  correlation is reported as not estimable rather than as zero.
- Fisher r-to-z tests for the three pairs among combat, ceasefire, and resumption, with Holm
  step-down adjustment. The combat-vs-ceasefire test is the primary contrast (parent paper);
  the other two are reported for completeness.
- Rolling 21-day correlation for the figure.

## 6. Finding 3 — under-identification (`04_identification_fevd.py`)

- FEVD from the combat VAR(1) at horizons 1, 6, 12 under **both** Cholesky orderings. Because
  the residual correlation is 0.62, the share ρ² = 0.385 of same-day variance is assigned to
  whichever series is ordered first (it equals the h = 1 cross-share in both orderings). Any
  ordering-dependent asymmetry is treated as unidentified. This finding is given its own
  figure and results section (memo: "give that more prominence").

## 7. Finding 4 — asymmetry and reach (`05_asymmetry_spread.py`)

- Strike:retaliation ratio by phase (phase totals). **Bootstrap CI:** days resampled within
  phase, 2,000 draws, seed 42, percentile interval of the ratio of sums.
- One-day lead-lag cross-correlations by phase.
- Geographic reach: cumulative distinct countries hit by retaliation; the first day at which
  the maximum is reached and the count of countries added afterwards.

## 8. Finding 5 — diplomacy (`06_diplomacy.py`)

- Weekly aggregates (week = (day−1)//7; 25 weeks, the last with 2 days): Pearson r, Spearman
  ρ, and Pearson r on full weeks only.
- Daily cross-correlation, lags −10…+10, with the no-association band.
- Granger tests between `violence = strikes + retal` and `diplomatic`, lag by BIC.
- Kruskal–Wallis across the four phases for diplomatic/day and violence/day, with ε² = H/(n−1)
  as the effect size. This quantifies "clear co-movement at the regime level" (memo).

## 9. Regime detection and the placebo check (`07_breaks_placebo.py`)

- **Detector.** Bai–Perron change-in-mean model fitted by an exact dynamic programme
  (vectorised; identical optimum to the parent's implementation), minimum segment 6 days,
  K = 1…6, chosen by the parent paper's BIC: `n·log(RSS/n) + (K+1)·log n`.
- **Placebo (memo: "a placebo or permutation check on the break dates").** Three nulls,
  1,000 draws each, seed 42:
  1. *Shuffle* — the observed values randomly re-ordered (exact marginal distribution, no
     time structure).
  2. *AR(1), within-regime persistence* — Gaussian AR(1) matched to the observed mean and
     variance with φ equal to the lag-1 autocorrelation of the phase-demeaned series (0.29).
     This is the natural null under the alternative of true level shifts plus persistence.
  3. *AR(1), whole-series persistence* — the same with φ from the raw series (0.71). This
     null is conservative: that φ is inflated by the very level shifts under test.
  For each draw: the number of segments the BIC selects and the BIC improvement of the
  selected model over one regime. The p-value is (draws with gain ≥ observed + 1)/(draws + 1).
- **What the placebo shows.** The BIC's segment count is not itself evidence (it chooses ≥ 2
  segments in 72% of shuffles and 6 segments in 60% / 99% of AR(1) draws). The observed
  improvement (170.3) exceeds every one of the 3,000 draws (maxima 40.2, 40.4, 157.3).
- **Sensitivity.** The detector is re-run under two stricter penalties — the Yao (1988) /
  Bai–Perron BIC `(2K−1)·log n` that counts break dates as parameters, and the Liu–Wu–Zidek
  (1997) criterion `0.299·(2K−1)·(log n)^2.1` — and under minimum segment lengths 6, 8, 10,
  14. The Day-40 break survives everything; Days 131/147 survive both BIC-type criteria at
  every segment length but not LWZ; the early sub-breaks (7, 23) are penalty-sensitive.
- **Replication.** The detector on `retal` and on `strikes + retal`.

## 10. Directional evidence, scoped (`08_directional_scoping.py`)

- **Resumption phase** (memo: "rests on 23 daily observations"): VAR lag by BIC (min 1) with
  `maxlags = 2`, Granger both directions, usable observations reported (22), one-day
  lead-lag correlations, and the same test under the raw-row measure. Under raw rows the
  result is null (p = 0.78). Reported as suggestive.
- **Full sample** (memo: "estimated across the mean shift … re-estimate on a regime-demeaned
  series"): the naive levels VAR (AIC and BIC lags) is retained for the record; the primary
  full-sample estimate subtracts each of the four phase means from both series, reports the
  lag order under AIC/HQIC/BIC (BIC selects 0; lag 1 is used as the minimum feasible), and
  runs Granger tests at each. Sensitivity: means of the six detected regimes removed instead.
  The retal→strikes direction is consistent but its strength is specification-dependent
  (p = 0.0009–0.26); strikes→retal is never significant. The abstract carries no full-sample
  p-value.

## 11. Robustness (`09_robustness.py`)

ADF/KPSS on levels (full and combat); the same-day coupling under all three measures;
negative-binomial (NB2, α = 1; Poisson-HC1 fallback) distributed-lag models of retaliation on
strikes (lags 0–2) plus its own lag; and of daily deaths on strike and retaliation tempo
(lags 0–2) — the casualty caveat.

## 12. Synthesis and verification (`10_synthesis.py`)

Re-derives every headline number from the regenerated tables, asserts each against the value
the manuscript reports (tolerances at the last reported digit), writes `output/synthesis.json`
and `output/tables/t0_headline_findings.csv`, and checks that each headline value appears
verbatim in `manuscript/paper1_major_revision1.md`. The Word build (`manuscript/make_docx.js`)
adds a second guard: every table in the .docx is built from the CSVs and compared cell by
cell with the markdown table.

## 13. Determinism

All randomness is seeded (`SEED = 42`): IRF Monte-Carlo replications, bootstrap ratios,
placebo draws. `run_all.sh` sets `PYTHONHASHSEED=0` and `MPLBACKEND=Agg`. No network, no
wall-clock dependence. Runtime about three minutes (the placebo step dominates).

## 14. Known limitations

See manuscript Section 7. In brief: OSINT reporting; the row-expansion caveat (mitigated);
sub-daily ordering invisible (the identification limit); coarse casualty and diplomacy
fields; the BIC segment count is not evidence on its own; 23-day resumption sample; one war.
