# Methods and design decisions — Paper 2

This document records the analytical choices behind Paper 2 in enough detail to audit or
contest them. It complements the inline documentation in `src/` and is written so that the
first author can defend every decision at a thesis committee or peer review.

## 1. Data source and pinning

- **Input:** `ResearchData/releases/v1.2/iranwar_event_dataset.csv` (frozen release; Days
  1–170, 2026-02-28 → 2026-08-16; 4,612 event rows, 52 columns). The analysis is pinned to
  the *frozen* release, not the moving root dataset, so it reproduces byte-for-byte
  regardless of later dataset versions. Override with the `IRANWAR_DATASET` environment
  variable.
- Day 1 = 2026-02-28 (`BASELINE_DATE = 2026-02-27`, so war-day N = 2026-02-27 + N days).
- All stochastic steps (the mediation bootstrap, the jitter in Figure 4) are seeded
  (`SEED = 42`); the pipeline has no network or wall-clock dependence.

## 2. Study design

A retrospective **ecological time-series study** with the **conflict-day** as the unit of
analysis (Days 1–170; N = 170). All variables are population-level daily aggregates.
No individual-level data exist in the source, and no individual-level inference is made.
This is the same unit and phase structure as Paper 1, so the two papers' findings compose.

## 3. Outcome variables

Daily estimated killed by faction, from `casualties.json` rows (850 rows = 170 days × 5
factions; **daily estimates, not cumulative**):

- `iran_civ` — Iranian civilian estimated killed/day (primary outcome; 543 over the war)
- `iran_mil`, `us_mil`, `leb_all`, `isr_mil` — the other factions
- `killed_total` — sum across factions (secondary outcome; 6,213)

Two cumulative reference series come from the dashboard's daily snapshots
(`hero-stats.json` history): `snap_iranian_killed`, `snap_lebanese_killed`,
`snap_displaced`, `snap_children_killed`. Raw coverage is 107–126 of 170 days; missing days
are **linearly interpolated** (interpolation affects display and terminal-value reads, not
the daily outcome models, which never use snapshots as outcomes).

**Known internal divergence, carried forward rather than hidden:** the summed daily series
runs below the terminal snapshots (Iran 3,166 vs 3,636, +14.8%; Lebanon 2,993 vs 4,308,
+43.9%). Both totals are reported wherever a cumulative toll is used (see §9, and Table 6).

## 4. Exposure variables

- `strikes`, `retal` — Paper 1's primary tempo operationalization: distinct offensive
  strike-file locations active per day (de-duplicating the target × active-day explosion)
  plus discrete timeline events in the domain.
- `strikes_civfac` / `strikes_milfac` — the strike-file locations split into
  **civilian-facing** vs **military-facing** targets. A location-day is civilian-facing if
  ANY of its target rows that day (a) has `infrastructure_target_type` in {civilian,
  oil_infrastructure, communications, water_infrastructure} or (b) matches the
  civilian-facing keyword pattern (hospital, clinic, medical, pharmaceutical, school,
  residential, civilian, desalination, water, power plant, electric, refinery, oil, gas,
  petrochemical, IRIB, broadcast, airport). Classifying at the location-day level prevents
  multi-target locations from being double-counted across the two series
  (`civfac + milfac ≤ strikes` is asserted at build time).
  Rationale: oil/energy, communications, and water targets are "civilian-facing" in the
  public-health sense — their destruction transmits harm to civilian populations even when
  militaries classify them as dual-use.

## 5. The health-system event register and the HSSI

**Construction (three stages, all in `src/util.py`):**

1. **Keyword screen.** `HEALTH_PAT` over STRIKE / RETALIATION / MILITARY / HUMANITARIAN
   rows, excluding (a) headline-echo event types (cost, market, briefing, snapshot,
   casualty-report rows repeat each day's narrative and would count one reported event many
   times) and (b) static reference files (`global-bases.json`, `historical-comparison.json`).
   The pattern covers facilities, workforce, supplies, WASH terms, and health institutions;
   `hospital(?!i[sz])` deliberately excludes "hospitalized" (harm to people, not facilities).
2. **De-duplication.** Strike-file locations collapse to one row per `source_record_id`,
   dated to the first (onset) active day.
3. **Rule classification + documented manual audit.** Rules assign five categories —
   `facility_attack`, `workforce_harm`, `supply_disruption`, `wash_disruption`,
   `access_disruption` (all *insults*) and `system_report` (surveillance signals, not
   insults). Every screened row was then read by the authors; the corrections are recorded
   **by event id with reasons** in `AUDIT_RECLASS` (6 rows), `AUDIT_EXCLUDE` (6), and
   `AUDIT_MERGE` (5 duplicates across 5 incident groups). `00_build_panel.py` verifies at
   run time that each audited id still exists and still contains its anchoring text, so the
   audit cannot silently drift from the data. **Every screened row is retained** in
   `data/health_system_events.csv` with `audit_action`, `audit_note`, and `counted`
   columns — exclusions stay visible.

**Result:** 82 screened rows → **21 counted insult events** (6 facility attacks, 6
workforce-harm events, 6 WASH disruptions, 2 access disruptions, 1 supply disruption) and
50 system reports.

**The HSSI** (`hssi`, normalized `hssi_pct`) is the cumulative count of counted insult
events through day *t* — an index of *reported salient insults*, in the spirit of
event-count exposure measures (ACLED-style), not a census of damage. The system reports
show true damage is far larger (WHO: 307 facilities by Day 39) than the reported-discrete-
event count; the HSSI is therefore a *trajectory proxy*, and a second operationalization
addresses its level bias:

**The benchmark-anchored facility-damage curve** (`facil_damage_bench`, `facil_damage_pct`)
interpolates piecewise-linearly through institutionally reported cumulative Iranian
facility-damage counts, each verified against its anchor row: Day 15 = 31 (Iran Health
Ministry-linked reporting, EVT-0094), Day 39 = 307 (WHO, EVT-0390), Day 170 = 309 (IRCS,
EVT-3304); 0 on Day 0, flat after Day 170's anchor. The ICRC Day-28 figure (25 damaged /
9 out of service, EVT-0273) is *lower* than the Day-15 figure and is excluded from the
monotone curve; the divergence is treated as a political fact and analyzed in `07`.

Both operationalizations are used wherever degradation enters a model; their divergence is
reported, not averaged away.

## 6. Statistical procedures

All models are estimable with a standard graduate behavioral-statistics toolkit.

- **Phase comparison (02).** One-way ANOVA, Welch's ANOVA (reported "undefined" with a note
  where a phase has zero variance), Kruskal–Wallis; pairwise Welch t-tests with **Holm**
  correction; effect sizes η², ω², Hedges' g. Strike-day vs quiet-day Welch t and
  Mann–Whitney U. Per-strike lethality (Iranian killed / strike location, strike days only)
  compared Major Combat vs Resumption with Mann–Whitney U.
- **Correlation and regression (03).** Pearson (lower triangle) and Spearman (upper)
  matrices; lagged cross-correlations (0–7 days); hierarchical OLS (M1–M4) with
  **Newey–West HAC standard errors (7-day lag)** because daily series are serially
  dependent; negative-binomial (NB2) count models as distributional robustness. Full-sample
  and Major-Combat-only estimates.
- **Mediation (04).** Single-mediator model X = `strikes_milfac`, M = `strikes_civfac`,
  Y = `iran_civ`; product-of-coefficients with a seeded nonparametric percentile bootstrap
  (10,000 resamples of days) and the Sobel test for reference. X and M are
  non-overlapping counts (military- vs civilian-facing locations).
- **Moderation (05).** `iran_civ ~ strikes_c * W_c` with HAC SEs, W = each degradation
  operationalization; simple slopes at W = mean ± 1 SD (HAC vcov delta method);
  Johnson–Neyman boundary; kinetic-days-only sensitivity; a phase-interaction variant
  (strikes × Resumption).
- **Projection (06).** Literature indirect:direct mortality ratios (1:1 floor; 3:1; 4:1
  Geneva Declaration average; 15:1 upper) applied to the documented direct toll under
  BOTH direct-toll bases (daily-series sum and terminal snapshot). Projections are labeled
  as scenario arithmetic, not estimates from these data.
- **Source-divergence and confidence sensitivity (07).** A claims register of cumulative
  Iranian-toll claims by named source (each anchored to an event id and verified at run
  time); divergence ratios; the Day-57 dashboard re-anchoring event (9,226 → 3,375, ratio
  2.73); and the core model (M3) re-estimated with exposure series rebuilt from (i) all
  rows, (ii) HIGH-confidence rows only, (iii) confidence-weighted rows
  (HIGH = 1.0, MEDIUM = 0.7, LOW = 0.4 — documented, admittedly arbitrary; the point is
  the sensitivity, not the weights).

## 7. Interpretation discipline

- **Ecological design.** Day-level associations; no individual-level claims.
- **Same-day mediation** is an associational decomposition of co-varying tempo components,
  not a causal identification; the full-sample effect partly reflects regime switching
  (war on/off), which is why the Major-Combat-only estimates (indirect CI includes 0) are
  reported alongside.
- **Two different lethality questions.** The per-strike *ratio of means* (Table 2c:
  15.4 → 0.7 across regimes) and the *conditional slope* (moderation: steeper at high
  degradation) answer different questions — average yield per strike vs marginal
  association per additional strike within a day. Both are reported; the manuscript
  explains the distinction.
- **Direct deaths only.** The daily series records reported direct deaths. Indirect
  mortality is *structurally unobservable* in this design — that is the point of §6's
  projections, and the reason the moderation results cannot refute the indirect-mortality
  mechanism.
- **Discrepancies are political facts** (Manuscript §6.5). Source divergence is quantified
  and interpreted, never averaged away.

## 8. Reproducibility

`bash run_all.sh` regenerates the panel, the register, all 20 tables, and all 8 figures in
about a minute. Dependencies are pinned in `requirements.txt`. Every curated constant
(audit decisions, benchmark anchors, toll claims, WASH exposure rows) is verified against
the dataset at run time by anchor-text assertion, so upstream drift fails loudly rather
than silently changing results.

## 9. Known limitations (paper-level)

1. Casualty inputs are contested estimates; the Day-45 cross-source spread is 3.8× and the
   dashboard itself re-anchored its cumulative metric by −63% on Day 57. All headline
   analyses use the dataset's conservative daily series; cumulative claims carry both
   internal bases.
2. The health-system register captures *reported, nationally salient* insults (21 events);
   WHO/IRCS benchmarks show two orders of magnitude more facility damage. The register is
   a trajectory proxy, mitigated by the benchmark-anchored curve.
3. N = 40 for Major-Combat-only models; power is limited and those estimates are wide.
4. HSSI/degradation is confounded with time and phase; the moderation result is an
   observed effect-modification pattern, not proof of the resilience-erosion mechanism.
5. Iranian reporting passed through internet blackouts (Manuscript §5); missingness is not
   random with respect to intensity.
6. No spatial analysis: strike coordinates exist, but hospital coordinates do not (seed
   #4's Analysis 3 requires the WHO EMRO facility registry — future work).
