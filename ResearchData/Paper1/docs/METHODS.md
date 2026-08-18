# Methods and design decisions — Paper 1

This document records the analytical choices behind Paper 1 in enough detail to audit or
contest them. It complements the inline documentation in `src/`.

## 1. Data source and pinning

- **Input:** `ResearchData/releases/v1.2/iranwar_event_dataset.csv` (frozen release; Days
  1–170, 2026-02-28 → 2026-08-16). The analysis is pinned to the *frozen* release, not the
  moving root dataset, so it reproduces byte-for-byte regardless of later dataset versions.
  Override with the `IRANWAR_DATASET` environment variable.
- Day 1 = 2026-02-28 (`BASELINE_DATE = 2026-02-27`, so war-day N = 2026-02-27 + N days).

## 2. Unit of analysis and intensity measures

The unit is the **conflict-day** (Day 1–170), giving a 170-observation daily panel.

The core challenge is turning event rows into a daily *intensity*. The strike files explode
each location into one row per target × per active day, so a naive row count over-weights
multi-target, multi-day locations. We therefore define the **primary tempo** measures by
de-duplicating that explosion:

- `strikes` — number of **distinct offensive locations** (`source_record_id`) active on day *t*
  in the STRIKE domain, plus discrete STRIKE-domain timeline events (which carry no location id).
- `retal` — the analogous count for the RETALIATION domain. (Retaliation rows are not
  target-exploded, so `retal ≈ retal_rows`.)

Two alternative operationalizations are carried for robustness (§6 of the paper):

- `strikes_rows` / `retal_rows` — raw event-row counts (include the explosion).
- `strikes_tl` / `retal_tl` — **timeline-only** discrete events (one reported event = one count;
  the cleanest but sparsest measure).

The primary and raw-row strike series correlate r = 0.92, and every headline result holds under
all three measures (`output/tables/t06_operationalization.csv`).

Other series: `killed` = summed daily estimated fatalities across the five tracked factions;
`diplomatic`, `naval` = daily DIPLOMATIC / NAVAL event counts; `retal_countries`,
`cum_countries` = distinct / cumulative-distinct countries hit by retaliation (horizontal
diffusion). Full definitions in `docs/CODEBOOK_panel.md`.

## 3. Phases

Four phases are used for description and reported as **recovered**, not imposed:

| Phase | Days | Dates | Source of boundary |
|---|---|---|---|
| Major Combat | 1–40 | 2026-02-28 … 04-08 | narrative + endogenous break at Day 40 |
| First Ceasefire | 41–129 | 2026-04-09 … 07-06 | narrative |
| Resumption | 130–152 | 2026-07-07 … 07-29 | documented "ceasefire collapsed" (Jul 7) + break at Day 131 |
| Diplomatic Pause | 153–170 | 2026-07-30 … 08-16 | documented "no US strikes" (Jul 30) + break at Day 147 |

Narrative boundaries come from the dataset's `strikes-iran.json` `_metadata.phase` field. The
Bai–Perron detector (§5) recovers breaks at Days 40, 131, 147 — within 1, 1, and 6 days of the
documented transitions — so the phases are data-driven, not analyst-imposed. `KINETIC_END = 40`
defines the active-combat regime used as the primary estimation window.

## 4. Time-series models

- **VAR.** Bivariate VAR on `[strikes, retal]` (Sims 1980; Brandt & Williams 2007). Lag chosen
  by AIC, with BIC/HQIC/FPE reported (`select_order`). Primary estimation window is the combat
  regime (Days 1–40), where both series are stationary (§5); the full sample is reported as a
  war-average with the structural break made explicit.
- **Granger causality.** F-test in both directions (`test_causality`).
- **IRF.** Orthogonalized (Cholesky) impulse responses, horizon 12 days, with 95% Monte-Carlo
  error bands (`errband_mc`, `repl=1000`, `seed=42`).
- **FEVD.** Forecast-error variance decomposition at horizons 1/6/12, computed under **both**
  Cholesky orderings. Because the contemporaneous correlation is high, the FEVD asymmetry is
  ordering-dependent and therefore treated as **unidentified** (see §5.7 of the paper). All
  directional inference rests on the *lagged* Granger/lead-lag evidence, which is ordering-free.

## 5. Stationarity

ADF (H0: unit root) and KPSS (H0: stationary) on levels, full sample and combat regime
(`02_stationarity.py`). Strike and retaliation tempo are ADF-stationary within combat
(p = 0.0002, 0.010). Full-sample KPSS rejection reflects the ceasefire **mean shift** (a
structural break, confirmed by §6), not a unit root — hence the combat-regime primary window.

## 6. Structural breaks

A least-squares multiple-mean-shift model (the Bai–Perron 1998, 2003 change-in-mean model),
implemented dependency-free by dynamic programming with a minimum segment length of 6 days
(`04_structural_breaks.py`). The number of segments K is chosen by BIC
(`n·log(RSS/n) + (K+1)·log n`) over K = 1…6. This recovers the regime structure endogenously
and validates the documented phase boundaries.

## 7. Regime-dependence and asymmetry

- Within-phase contemporaneous Pearson correlation and small-lag Granger tests
  (`05_regime_reciprocity.py`).
- **Fisher r-to-z** test comparing the combat vs. ceasefire couplings (two independent samples).
- Lead–lag sign via ±1-day cross-correlation; strike/retaliation ratios by phase.

## 8. Count-model robustness

Negative-binomial (NB2) distributed-lag GLMs for retaliation (`retal_t ~ strikes_{0..2} +
retal_{t-1}`) and casualties (`killed_t ~ strikes_{0..2} + retal_{0..2} + killed_{t-1}`), with a
Poisson-HC1 fallback (`06_robustness.py`). Guards against the Gaussian-VAR approximation for
overdispersed counts and against reading strike *tempo* as a casualty proxy.

## 9. Determinism / reproducibility

- All randomness (IRF Monte-Carlo bands) is seeded (`SEED = 42`). `run_all.sh` sets
  `PYTHONHASHSEED=0` and `MPLBACKEND=Agg`.
- No network access, no wall-clock dependence in the computation (dates are derived from
  war-day integers).
- `run_all.sh` regenerates the panel, all tables, and all figures from the frozen dataset in
  one command.

## 10. Known limitations (see paper §9)

OSINT reporting bias; the target-explosion caveat (mitigated by de-duplication + timeline
replication); invisibility of sub-daily ordering (the contemporaneous-coupling result is also
the identification limit); coarse casualty/diplomacy fields; and single-conflict external
validity.
