# Reciprocity Without a Lag: Same-Day Coupling and Regime-Contingent Escalation in the 2026 US–Iran War

**Major Revision 1 — Paper 1 of the IranWar.ai research series**

Jacob E. Thomas (Results Generation, Austin, Texas) and [Co-author: name, affiliation]

*Prepared from the IranWar.ai Event-Level Research Dataset, v1.2 (Days 1–170; 28 February to 16 August 2026). Every number, table, and figure in this document regenerates from `ResearchData/Paper1/MajorRevision1/` with one command (see Reproducibility).*

*Revision convention. Sections 1 (Introduction) and 6 (Discussion) are drafted as bullet points, one bullet per intended paragraph, for the co-author to write by hand. Sections 2 to 5 and 7 (data, methods, results, robustness, limitations) are complete and carry the numbers.*

---

## Abstract

Classical accounts of escalation expect adversaries to answer each other's violence with a measurable lag. We test that expectation on 170 days of daily strike and retaliation counts from the 2026 US–Iran war, the first interstate air war recorded openly at daily resolution from its first day. The record spans four political regimes (major combat, ceasefire, resumption, pause), which we treat as a within-case natural experiment. Five results follow. First, reciprocity is same-day, not lagged: during combat the two series correlate at r = 0.69 within the day, yet every information criterion selects a zero-lag model and neither series Granger-causes the other. Second, the coupling switches with the regime: r = 0.69 in combat, 0.18 in the ceasefire, and 0.66 at the resumption (combat versus ceasefire, Fisher z, p = 0.0007). Third, which side set the tempo cannot be identified from daily data: a variance decomposition attributes 41% of retaliation to strikes under one ordering assumption and 44% of strikes to retaliation under the other. Fourth, the strike-to-retaliation ratio rose from 0.68 to 1.42, and retaliation reached all 13 countries it would ever reach by Day 22. Fifth, diplomacy and violence were unrelated week to week (r = 0.06) but shifted together across regimes. Structural-break detection recovers the documented regime boundaries to within 1, 1, and 6 days, and a placebo check shows the fit improvement exceeds every one of 3,000 noise draws. Directional claims about the July re-escalation rest on 23 days and are reported as suggestive.

**Keywords:** escalation, reciprocity, vector autoregression, structural breaks, identification, US–Iran war, event data

---

## 1. Introduction

*[Drafted as bullet points for the co-author. Each bullet is the claim of one paragraph.]*

- **The expectation.** Richardson's (1960) reaction equations, Jervis's (1976) spiral, Kahn's (1965) ladder, and Axelrod's (1984) tit-for-tat differ in mechanism but share one observable implication: one side's violence today should predict the other side's violence tomorrow. [Characterise the lineage and where the mechanisms differ.]
- **The record.** Event-data studies that looked for that lag in interstate interaction report mixed and mostly modest results (Dixon, 1986; Goldstein, 1991; Goldstein & Freeman, 1990; Moore, 1995; Ward, 1982). Most rest on retrospective coding at weekly or monthly resolution, so the timescale of reciprocity has rarely been treated as an empirical quantity in its own right.
- **The case.** The 2026 US–Iran war is the first sustained interstate air war recorded openly, event by event, at daily resolution from Day 1 (Thomas et al., 2026). Its first 170 days span four regimes: major combat (Days 1–40), a ceasefire (Days 41–129), a resumption (Days 130–152), and a diplomatic pause (Days 153–170).
- **The design.** The regimes are not a nuisance to be differenced away. They are a within-case natural experiment on whether reciprocity is a fixed property of a hostile pair or something that switches with the political moment. This is the design the dataset descriptor's research agenda called for (Thomas et al., 2026, Section 7.1).
- **The questions.** (a) Does one side's violence predict the other's at a daily lag, or do the two move together within the day? (b) Is the coupling stable across regimes? (c) Can daily data say which side set the tempo? (d) Did the balance of the exchange shift as the war went on? (e) Did diplomacy and violence trade off day to day, or move at the regime level?
- **The answers, in brief.** Same-day rather than lagged; regime-contingent; not identifiable at daily resolution; a balance that flipped and a geographic reach that saturated by Day 22; and diplomacy that tracked the regime, not the week. The under-identification result (question c) is the paper's methodological contribution.
- **Scope.** One war, four regimes, open-source data. The findings are within-case regularities offered for comparative testing. Directional claims are scoped explicitly in Sections 4.7 and 6.

---

## 2. Data and Measures

**Source.** All series come from the IranWar.ai Event-Level Research Dataset, version 1.2 (Thomas et al., 2026), a public, versioned record of the war assembled from open-source reporting (among others CENTCOM, the IDF, ACLED, the Iranian Red Crescent, Bloomberg, and the IMO). The frozen v1.2 release holds 4,612 records in nine domains. We use the STRIKE, RETALIATION, and DIPLOMATIC domains and the daily casualty estimates. Day 1 is 28 February 2026. The analysis is pinned to the frozen file, whose checksum is verified before any script runs, so later dataset releases cannot change a number in this paper.

**Unit and series.** The unit is the conflict-day, giving a panel of 170 daily observations. Two series carry the argument. *Strikes* is the number of distinct locations struck by US or Israeli forces that day, plus any discrete offensive events recorded in the dataset's timeline. *Retaliation* is the same count for Iranian and proxy attacks. Counting distinct locations rather than raw records avoids over-weighting a single location that was hit on many days or listed with many targets. Two alternative measures, raw event records and timeline-only events, are carried for robustness (Section 5). *Diplomatic* is the daily count of DIPLOMATIC-domain events. *Killed* is the summed daily estimated deaths across the five tracked factions and is used only for a caveat (Section 5).

**Regimes.** The four phases in Table 1 are taken from the dataset's own phase narrative. Section 4.6 shows that a break detector recovers their boundaries from the strike series alone. Over the 170 days the panel holds 386 strike-location-days, 621 retaliation events, and 414 diplomatic events (Figure 1).

**Table 1.** *Daily Intensity by Phase*

| Phase | Days | n | Strikes/day | Retaliation/day | Strike:retaliation | Diplomatic/day | Days with any strike (%) |
|---|---|---|---|---|---|---|---|
| Major Combat | 1–40 | 40 | 7.02 | 10.30 | 0.68 | 2.62 | 97.5 |
| First Ceasefire | 41–129 | 89 | 0.57 | 1.79 | 0.32 | 3.22 | 38.2 |
| Resumption | 130–152 | 23 | 2.35 | 1.65 | 1.42 | 0.39 | 69.6 |
| Diplomatic Pause | 153–170 | 18 | 0.00 | 0.67 | 0.00 | 0.72 | 0.0 |

*Note.* Strikes are distinct locations struck per day plus discrete timeline events; retaliation is defined the same way. The ratio is the phase total of strikes divided by the phase total of retaliation. Source: `t01_phase_intensity.csv`.

**Figure 1.** *Daily Strike and Retaliation Tempo (A) and Diplomatic Activity (B), Days 1–170.* Shaded bands mark the four phases; dashed lines mark the documented transitions.

---

## 3. Analytic Approach

Each method is stated first in plain terms and then as the specification used. All estimation uses Python 3.11 with pandas 3.0.5, statsmodels 0.14.6, scipy 1.17.1, and numpy 2.4.6; every random step is seeded (seed 42).

**Same-day association and association by lag.** The Pearson correlation between the two series on the same day, with a Fisher confidence interval, and the cross-correlation at lags of minus five to plus five days. A lagged pattern of reciprocity would show a peak at a lag other than zero.

**Vector autoregression (VAR).** A model in which today's value of each series is predicted from the past values of both series (Sims, 1980; Brandt & Williams, 2007). The number of past days included (the lag order) is chosen by four information criteria (AIC, BIC, HQIC, FPE); a choice of zero means that no day of history improves the forecast. The primary model is fitted within the combat regime, where both series are stationary (Section 5); a full-sample version is reported with the regime problem addressed directly (Section 4.7).

**Granger causality.** A test of whether the past of one series improves the prediction of the other beyond what the other's own past already provides (Granger, 1969). It is an F-test on the VAR coefficients and is run in both directions.

**Impulse responses.** How much extra retaliation follows a typical one-day surge in strikes, and for how long. Responses are orthogonalised, and the 95% band comes from 1,000 seeded Monte-Carlo replications (Appendix Figure A1).

**Forecast-error variance decomposition (FEVD).** A split of the uncertainty in each series into the parts attributable to surprises in each series. When two series move together within the day, the method must first assume which one moved first inside the day (the Cholesky ordering). That assumption is not testable from daily data, so we compute the decomposition under both orderings and treat any conclusion that changes with the ordering as unidentified.

**Comparing correlations across regimes.** Fisher's r-to-z test for the equality of two independent correlations, applied to the three pairs of fighting or ceasefire regimes, with Holm adjustment for the three comparisons.

**Structural breaks.** A change-in-mean model of the Bai–Perron type (Bai & Perron, 1998, 2003) fitted by an exact dynamic programme with a minimum segment length of six days; the number of segments (one to six) is chosen by the BIC used in the parent paper. Three checks follow. A placebo check re-runs the detector 1,000 times on each of three noise series with no regime structure: the observed days randomly re-ordered; a persistent AR(1) series with the within-regime day-to-day autocorrelation (0.29); and a persistent AR(1) series with the whole-series autocorrelation (0.71, a deliberately conservative null because that value is inflated by the very shifts under test). A sensitivity check re-runs the detector under stricter penalties (the Yao/Bai–Perron BIC that counts break dates as parameters, and the Liu–Wu–Zidek criterion) and under minimum segment lengths of 6 to 14 days. A replication runs the detector on the retaliation and combined series.

**Regime-demeaned re-estimation.** The full-sample VAR is re-estimated after subtracting each phase's mean from each series, so that regime-level shifts in average intensity cannot masquerade as day-to-day prediction.

**Count models.** Negative-binomial distributed-lag models of daily retaliation on same-day and lagged strikes, a check on the Gaussian VAR for over-dispersed counts, and a parallel model of daily deaths on tempo.

**Stationarity.** Augmented Dickey–Fuller and KPSS tests on each series, full sample and combat regime.

---

## 4. Results

### 4.1 Finding 1: Reciprocity Is Same-Day, Not Lagged

Within the combat regime (Days 1–40) strikes and retaliation are strongly correlated on the same day, r = 0.69 (95% CI 0.48 to 0.82, n = 40 days; Figure 2A). Every information criterion selects a lag order of zero, meaning that no day of history improves the forecast of either series once the same day is known (Table 2). In a one-lag VAR fitted for the test, neither direction is significant: strikes to retaliation, F(1, 72) = 0.08, p = 0.78; retaliation to strikes, F(1, 72) = 0.60, p = 0.44. The raw cross-correlations at lags of one and two days are 0.3 to 0.4, less than half the same-day value (Figure 2B), and they disappear once each series' own persistence is accounted for, which is what the Granger tests show. The impulse responses say the same thing in event units: a typical one-day surge in strikes is accompanied by 2.3 additional retaliation events the same day (95% band 1.3 to 3.3) and 4.6 over a week, and the band includes zero from the first day after the shock onward (Appendix Figure A1). The action and the reaction happen inside the same 24-hour bin. The exchange runs faster than the day.

**Table 2.** *Same-Day Coupling, Lag Selection, and Granger Tests, Combat Regime (Days 1–40)*

| Quantity | Value |
|---|---|
| Same-day Pearson r (95% CI) | 0.69 (0.48 to 0.82) |
| Lag order selected: AIC / BIC / HQIC / FPE | 0 / 0 / 0 / 0 |
| Granger, strikes → retaliation (VAR(1)) | F(1, 72) = 0.08, p = 0.78 |
| Granger, retaliation → strikes (VAR(1)) | F(1, 72) = 0.60, p = 0.44 |
| Cross-correlation at lags −1 / 0 / +1 / +2 | 0.32 / 0.69 / 0.33 / 0.38 |
| Impulse response of retaliation to a strike shock, day 0 (95% band) | 2.28 (1.26 to 3.34) events |
| Cumulative response over 7 days | 4.55 events |
| First day on which the band includes zero | Day 1 |

*Note.* n = 40 days (39 usable observations in the VAR). Lag selection considered up to five lags. Sources: `t02_same_day.csv`, `t02_lag_selection.csv`, `t02_granger.csv`, `t02_ccf_combat.csv`, `t02_irf_summary.csv`.

**Figure 2.** *Same-Day Pairing (A) and Association by Lag (B), Combat Regime.* In B the shaded band is the 95% range expected if the two series were unrelated; the association peaks at lag zero.

### 4.2 Finding 2: The Coupling Switches With the Political Regime

The same-day coupling is not a constant feature of the pair of belligerents (Table 3, Figure 3). It is r = 0.69 in combat (n = 40), r = 0.18 in the ceasefire (n = 89, p = 0.10, indistinguishable from zero), and r = 0.66 at the resumption (n = 23, p = 0.0006). In the pause there are no strikes, so no correlation can be computed. The combat and ceasefire values differ, Fisher z = 3.37, p = 0.0007 (Holm-adjusted p = 0.002). The ceasefire and resumption values also differ, p = 0.013 (Holm-adjusted p = 0.026), while combat and resumption do not, p = 0.87. The rolling 21-day correlation shows the switch directly: near 0.8 through combat, between 0 and 0.5 through the ceasefire, and above 0.7 again once fighting resumed.

**Table 3.** *Same-Day Coupling by Phase and Fisher r-to-z Comparisons*

| Phase | Days | n | r | 95% CI | p |
|---|---|---|---|---|---|
| Major Combat | 1–40 | 40 | 0.69 | 0.48 to 0.82 | < 0.001 |
| First Ceasefire | 41–129 | 89 | 0.18 | −0.03 to 0.37 | 0.095 |
| Resumption | 130–152 | 23 | 0.66 | 0.34 to 0.84 | 0.0006 |
| Diplomatic Pause | 153–170 | 18 | — | — | not estimable (no strikes) |

| Comparison | z | p | Holm p |
|---|---|---|---|
| Combat vs Ceasefire | 3.37 | 0.0007 | 0.0021 |
| Ceasefire vs Resumption | −2.49 | 0.013 | 0.026 |
| Combat vs Resumption | 0.17 | 0.87 | 0.87 |

*Note.* Sources: `t03_regime_coupling.csv`, `t03_fisher_pairwise.csv`.

**Figure 3.** *Rolling 21-Day Same-Day Correlation (A) and Correlation by Phase With 95% Confidence Intervals (B).*

### 4.3 Finding 3: Which Side Set the Tempo Is Not Identified at Daily Resolution

A reader will want to know which side drove the same-day exchange in open combat. The variance decomposition appears to answer, and then answers the opposite way (Table 4, Figure 4). With strikes ordered first, strike shocks explain 41% of the forecast-error variance of retaliation over 12 days while retaliation shocks explain 2% of the variance of strikes. With retaliation ordered first, retaliation shocks explain 44% of the variance of strikes while strike shocks explain 0.2% of the variance of retaliation. The mechanism is arithmetic, not substantive. The residual correlation of the two equations is 0.62, so 38% of the same-day variance (0.62 squared) is shared, and the Cholesky step hands that shared share to whichever series is placed first. The data record that the two sides moved together within the day. They do not record who moved first, and no daily-resolution model can recover it. Any answer to "who started it" drawn from these data is the analyst's ordering assumption returned as a finding. This is the paper's methodological result, and it is why every directional statement in the paper rests on lagged evidence only (Section 4.7).

**Table 4.** *Forecast-Error Variance Decomposition Under Both Orderings, Combat Regime, Horizon 12 Days*

| Ordering assumption | Strike shocks → share of retaliation variance | Retaliation shocks → share of strike variance |
|---|---|---|
| Strikes first, then retaliation | 41% | 2% |
| Retaliation first, then strikes | 0.2% | 44% |

*Note.* VAR(1), Days 1–40. Residual correlation 0.62; shared same-day share ρ² = 0.38, which is the share credited at horizon 1 to whichever series is ordered first. Sources: `t04_fevd_orderings.csv`, `t04_residual_corr.csv`.

**Figure 4.** *Share of Variance Explained Under Each Ordering Assumption.* The two bars that matter swap places when the ordering swaps.

### 4.4 Finding 4: The Balance of the Exchange Flipped, and Retaliation's Reach Saturated Early

The strike-to-retaliation ratio was 0.68 in combat (bootstrap 95% CI 0.59 to 0.77), when recorded retaliation out-paced recorded strikes, and 1.42 at the resumption (95% CI 0.94 to 2.32), when strikes outnumbered responses; the two intervals do not overlap (Table 5, Figure 5A). The one-day lead-lag structure changed with it: symmetric in combat (strikes leading retaliation 0.33, retaliation leading strikes 0.32) and asymmetric at the resumption (retaliation leading strikes 0.45, strikes leading retaliation −0.06). Retaliation's geographic reach saturated early: Iranian and proxy attacks had struck 13 countries by Day 22, and no new country was struck in the 148 days that followed (Figure 5B). The interpretation of these patterns is deferred to Section 6, where the competing explanations are named.

**Table 5.** *Strike-to-Retaliation Ratio, Lead-Lag Correlation, and Geographic Reach by Phase*

| Phase | Strikes/day | Retaliation/day | Ratio (bootstrap 95% CI) | Strikes lead (+1 day) | Retaliation leads (+1 day) |
|---|---|---|---|---|---|
| Major Combat | 7.02 | 10.30 | 0.68 (0.59 to 0.77) | 0.33 | 0.32 |
| First Ceasefire | 0.57 | 1.79 | 0.32 (0.22 to 0.44) | 0.05 | 0.11 |
| Resumption | 2.35 | 1.65 | 1.42 (0.94 to 2.32) | −0.06 | 0.45 |
| Diplomatic Pause | 0.00 | 0.67 | 0.00 | — | — |

*Note.* Bootstrap intervals resample days within phase (2,000 draws, seeded). Reach: 13 countries by Day 22 (21 March 2026); 0 added over the following 148 days. Sources: `t05_ratio_by_phase.csv`, `t05_spread.csv`.

**Figure 5.** *Strike and Retaliation Tempo by Phase With the Strike-to-Retaliation Ratio (A), and Cumulative Countries Struck by Retaliation (B).*

### 4.5 Finding 5: Diplomacy Moved With the Regime, Not With the Week

Week to week, fighting and talking were unrelated (Table 6, Figure 6A). Weekly violence (strikes plus retaliation) and weekly diplomatic events correlate at r = 0.06 (p = 0.78, n = 25 weeks); the rank correlation is 0.36 (p = 0.077) and positive, so there is no sign of week-to-week substitution either. Neither series Granger-causes the other (p = 0.75 and p = 0.91), and the daily cross-correlation lies inside the no-association band at every lag from minus ten to plus ten days. Regime to regime, the picture is different (Figure 6B). Diplomatic activity ran at 2.6 events per day through combat, rose to 3.2 per day in the ceasefire, fell to 0.4 per day at the resumption (present on 39% of days), and returned to 0.7 per day in the pause; the phases differ, Kruskal–Wallis H(3) = 55.0, p < 0.001, ε² = 0.33. The belligerents talked while they fought, and the diplomatic channel and the ceasefire broke together in July.

**Table 6.** *Diplomacy and Violence: Weekly Association and Regime-Level Contrast*

| Quantity | Value |
|---|---|
| Weekly Pearson r, violence vs diplomacy (n = 25 weeks) | 0.06 (p = 0.78) |
| Weekly Spearman rho | 0.36 (p = 0.077) |
| Granger, violence → diplomacy (lag 4) | F = 0.48, p = 0.75 |
| Granger, diplomacy → violence (lag 4) | F = 0.25, p = 0.91 |
| Diplomatic events/day: Combat / Ceasefire / Resumption / Pause | 2.62 / 3.22 / 0.39 / 0.72 |
| Share of days with any diplomacy: Combat / Ceasefire / Resumption / Pause | 0.95 / 0.90 / 0.39 / 0.67 |
| Kruskal–Wallis across phases, diplomatic events/day | H(3) = 55.0, p < 0.001, ε² = 0.33 |

*Note.* Sources: `t06_weekly.csv`, `t06_granger.csv`, `t06_diplomacy_phase.csv`, `t06_regime_test.csv`.

**Figure 6.** *Weekly Violence Against Weekly Diplomacy (A) and Violence and Diplomacy per Day by Phase (B).*

### 4.6 The Regimes Are Recovered From the Data, and They Survive a Placebo Check

The break detector, given only the daily strike series, selects six segments with breaks at Days 7, 23, 40, 131, and 147 (Table 7, Figure 7A). The three documented macro-transitions, at Days 41, 130, and 153, are recovered to within 1, 1, and 6 days without the detector being told where to look. The two early breaks (Days 7 and 23) subdivide the combat phase into descending tiers of intensity.

A referee will ask whether six regimes is BIC finding structure or finding noise. The placebo check answers in two parts (Table 7, Figure 7B). The count of segments is not by itself evidence: on randomly re-ordered days the same BIC still chooses two or more segments in 72% of draws, and on a persistent series with no level shifts it chooses six segments in 60% of draws at the within-regime autocorrelation and in 99% at the whole-series autocorrelation. What is evidence is the size of the fit improvement. The observed six-segment model improves on a single regime by 170 BIC points, more than any of the 3,000 placebo draws (maxima 40, 40, and 157; p = 0.001 against each null). The break dates are also stable where it matters. The Day-40 break appears under every criterion and every minimum segment length. The July breaks (Days 131 and 147) appear under both BIC-type criteria at every minimum segment length, but not under the strictest criterion (Liu–Wu–Zidek), which keeps only the combat-era breaks at Days 15 and 40; the July level shift is small in absolute terms (0.6 to 3.2 strikes per day). The two early sub-breaks move or merge as the penalty tightens. Applied to the retaliation series the detector recovers the Day-40 transition; applied to the combined series it recovers Days 40 and 130.

**Table 7.** *Regime Detection and Placebo Check, Strike Series*

| Number of segments | Break days | BIC |
|---|---|---|
| 1 | — | 442.1 |
| 2 | 40 | 305.4 |
| 3 | 15, 40 | 289.2 |
| 4 | 7, 23, 40 | 286.3 |
| 5 | 15, 40, 131, 147 | 275.9 |
| 6 | 7, 23, 40, 131, 147 | 271.8 |

| Placebo null (1,000 draws each) | Share choosing 6 segments | Median BIC gain | Maximum BIC gain | p (gain ≥ observed 170.3) |
|---|---|---|---|---|
| Shuffled days (no time structure) | 0.07 | 2.3 | 40.2 | 0.001 |
| AR(1), within-regime autocorrelation 0.29 | 0.60 | 12.3 | 40.4 | 0.001 |
| AR(1), whole-series autocorrelation 0.71 | 0.99 | 65.9 | 157.3 | 0.001 |

*Note.* Detected breaks versus documented boundaries: Day 40 vs 41 (−1), Day 131 vs 130 (+1), Day 147 vs 153 (−6). The p-value is (number of draws with gain at least the observed + 1) / (draws + 1). Sensitivity by criterion and minimum segment length in `t07_sensitivity.csv`. Sources: `t07_break_selection.csv`, `t07_breakpoints.csv`, `t07_placebo_summary.csv`, `t07_other_series.csv`.

**Figure 7.** *Detected Regime Means Against the Documented Boundaries (A), and the Placebo Distribution of the BIC Improvement Against the Observed Value (B).*

### 4.7 Directional Evidence, Scoped

Two directional results from the parent draft are re-reported here with their limits stated (Table 8).

*The resumption phase.* On the 23 days of the resumption (22 usable observations), retaliation Granger-causes strikes at one lag, F(1, 38) = 5.34, p = 0.026, and strikes do not Granger-cause retaliation, p = 0.085; the one-day lead-lag correlations are 0.45 with retaliation leading and −0.06 with strikes leading. Under the raw event-record measure of tempo, however, the same test is null, p = 0.78. A result that rests on 22 observations and one of two measures is suggestive, and it is reported as such.

*The full sample.* The parent draft's full-sample result (retaliation to strikes, p < 0.001 at the AIC lag of 9) was estimated across the regime mean shifts that Section 4.6 documents, and a shift in average intensity between regimes can register as day-to-day prediction. After subtracting each of the four phase means, BIC selects a lag order of zero, which is Finding 1 restated for the whole war. At one lag the retaliation-to-strikes test gives p = 0.055; at the AIC lag of 4 it gives p = 0.0013. With the six detected regimes removed instead, the corresponding values are p = 0.26 and p = 0.0009. In every specification the reverse direction, strikes to retaliation, is non-significant. The direction is consistent; its strength depends on the lag order and on how the regime means are removed. The abstract therefore carries no full-sample p-value, and Section 6 treats the direction as suggestive rather than established.

**Table 8.** *Directional Evidence With Its Limits*

| Sample and specification | Retaliation → strikes | Strikes → retaliation |
|---|---|---|
| Resumption, primary measure, lag 1 (22 obs.) | F(1, 38) = 5.34, p = 0.026 | F(1, 38) = 3.13, p = 0.085 |
| Resumption, raw event records, lag 1 (22 obs.) | F(1, 38) = 0.08, p = 0.78 | F(1, 38) = 0.96, p = 0.33 |
| Full sample, levels, AIC lag 9 (parent draft) | F(9, 284) = 4.05, p < 0.001 | F(9, 284) = 1.14, p = 0.33 |
| Full sample, four phase means removed, lag 1 (HQIC; BIC selects 0) | F(1, 332) = 3.70, p = 0.055 | F(1, 332) = 0.07, p = 0.80 |
| Full sample, four phase means removed, AIC lag 4 | F(4, 314) = 4.58, p = 0.0013 | F(4, 314) = 1.30, p = 0.27 |
| Full sample, six detected regime means removed, lag 1 | F(1, 332) = 1.29, p = 0.26 | F(1, 332) = 0.32, p = 0.57 |
| Full sample, six detected regime means removed, AIC lag 4 | F(4, 314) = 4.83, p = 0.0009 | F(4, 314) = 0.89, p = 0.47 |

*Note.* Sources: `t08_resumption.csv`, `t08_full_sample.csv`.

---

## 5. Robustness

**Measurement.** The same-day coupling in combat is positive and significant under all three measures of tempo: r = 0.69 with distinct locations, 0.62 with raw event records, and 0.34 with timeline-only events (p = 0.03), the sparsest and noisiest measure (Table 9). The finding does not depend on how the dataset expands strike records into rows.

**Count models.** Negative-binomial distributed-lag models of daily retaliation reproduce the picture. Over the full sample, same-day strikes raise expected retaliation (incidence-rate ratio 1.14, p = 0.0008) and retaliation's own lag matters (1.17, p < 0.001); within combat, no lagged strike term is significant.

**Stationarity.** Within combat, the augmented Dickey–Fuller test rejects a unit root for both series (strikes p = 0.0002; retaliation p = 0.010). Over the full sample the KPSS test rejects stationarity for every series, which reflects the regime mean shifts of Section 4.6 rather than a unit root, and is the reason the primary model is estimated within combat and the full-sample model is regime-demeaned.

**Casualties.** Daily deaths do not track daily strike or retaliation tempo within combat (every lag p > 0.05). Deaths in this dataset are driven by discrete mass-casualty events and by reporting lags, so tempo should not be used as a proxy for lethality, and no argument in this paper rests on it.

**Table 9.** *Robustness Summary*

| Check | Result |
|---|---|
| Same-day r, combat: distinct locations / raw records / timeline-only | 0.69 / 0.62 / 0.34 (all p < 0.05) |
| Same-day r, full sample: distinct locations / raw records / timeline-only | 0.83 / 0.80 / 0.35 (all p < 0.001) |
| Negative binomial, full sample: same-day strikes IRR (p) | 1.14 (0.0008) |
| Negative binomial, full sample: lagged retaliation IRR (p) | 1.17 (< 0.001) |
| Negative binomial, combat: lagged strikes (1 and 2 days) | not significant |
| ADF within combat: strikes / retaliation | p = 0.0002 / p = 0.010 (unit root rejected) |
| KPSS full sample: every series | stationarity rejected (regime mean shifts) |
| Deaths on tempo, combat, all lags | not significant (minimum p = 0.19) |

*Note.* Sources: `t09_operationalization.csv`, `t09_countmodel_retal.csv`, `t09_stationarity.csv`, `t09_casualty_propagation.csv`.

---

## 6. Discussion

*[Drafted as bullet points for the co-author. Each bullet is the claim of one paragraph. Alternatives that a referee will raise are named in place.]*

- **Resolution.** The lagged action–reaction cycle that the classical models describe is absent here at daily resolution because the exchange is faster than the day. A weekly or monthly record of this war would have reported a lag that is really within-bin exchange smeared across bins. As high-frequency conflict records become available, the timescale of reciprocity becomes something to estimate rather than assume.
- **Reciprocity as a switch.** The coupling was strong in combat, absent in the ceasefire, and strong again at the resumption. It is a property of the regime, not of the pair of belligerents. Models with a fixed reaction coefficient will misfit wars that move between pauses and fighting. [Connect to the commitment and audience-cost literature; what switches the coupling on is the question this design makes visible.]
- **Under-identification.** With same-day coupling, the question "who set the tempo" has no answer in daily data, and the variance decomposition shows what happens when one is forced: the answer follows the ordering assumption. Only sub-daily timestamps could resolve it. This protects the paper from the "who started it" reading and is the methodological contribution.
- **Compellence, scoped.** The July direction (retaliation leading strikes) is consistent with a compellence logic, but it is equally consistent with plain tit-for-tat or with punishment triggered by a threshold, it rests on 22 observations, and it does not survive the raw-record measure. The full-sample direction survives regime demeaning at one lag order and not at another. "Compellence-consistent" is the strongest defensible phrase; "reactive (compellence)" is not.
- **Depletion, scoped.** The rising strike-to-retaliation ratio and the saturation of geographic reach by Day 22 are consistent with a decline in Iran's capacity to respond. They are also consistent with deliberate restraint to keep the resumption limited, with a shift from direct to proxy action, and with a shift in what reporters were attending to. The data cannot separate these, and the paper is more persuasive for saying so.
- **Diplomacy.** Fighting and talking ran on parallel tracks at weekly resolution and shifted together at regime boundaries. Talking continued through the heaviest combat. A single strike should not be read as a diplomatic signal from these data alone. [Connect to bargaining accounts in which fighting and negotiating are simultaneous instruments.]
- **Generalisation and the next record.** These are within-case regularities from one war, offered as hypotheses for comparative testing. The next high-frequency conflict record should carry sub-daily timestamps, an explicit direct-versus-proxy attribution for retaliation, and source-disaggregated coding, because those are the three things this record could not resolve.

---

## 7. Limitations

- **Reported, not observed.** Event counts reflect what was reported. Systematic under- or over-reporting by any party would bias the tempo series. The dataset's record-level source attribution supports a source-disaggregated replication that this paper does not attempt.
- **Record expansion.** The dataset expands some strike records into one row per target per active day. The primary measure counts distinct locations and the finding holds under the timeline-only measure, but a purpose-built sortie count would be better.
- **Sub-daily order is invisible.** The central finding is also the identification limit. Nothing in the paper resolves the order of strikes and retaliation inside a day.
- **Coarse casualty and diplomacy fields.** Deaths are lagged and contested; diplomatic events are heterogeneous. Both are used for regime-level description only.
- **Segment count.** The number of segments a BIC selects is not evidence on its own; the placebo and sensitivity checks are the evidence, and the July breaks are found by BIC-type criteria but not by the strictest one.
- **Small samples.** The resumption phase has 23 days. Results estimated on it are suggestive.
- **One war.** Four regimes within one conflict do not license generalisation to other conflicts.

---

## Reproducibility

Every number, table, and figure in this document regenerates from the frozen v1.2 dataset with `cd ResearchData/Paper1/MajorRevision1 && bash run_all.sh` (about three minutes). The input file's MD5 is verified before any script runs; the daily panel is asserted identical to the parent paper's; every stochastic step is seeded; and the final step re-derives every headline number, asserts it against the value reported here, and checks that each headline value appears verbatim in this text. Design decisions are recorded in `docs/METHODS.md`, variable definitions in `docs/CODEBOOK_panel.md`, and the changes made in response to the reviewer memo in `REVISION_NOTES.md`.

## Data Availability

IranWar.ai Event-Level Research Dataset v1.2, `ResearchData/releases/v1.2/` in the project repository (github.com/jethomasphd/WarTheater).

---

## References

- Axelrod, R. (1984). *The evolution of cooperation*. Basic Books.
- Bai, J., & Perron, P. (1998). Estimating and testing linear models with multiple structural changes. *Econometrica, 66*(1), 47–78.
- Bai, J., & Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics, 18*(1), 1–22.
- Brandt, P. T., & Williams, J. T. (2007). *Multiple time series models*. Sage.
- Dixon, W. J. (1986). Reciprocity in United States–Soviet relations: Multiple symmetry or issue linkage? *American Journal of Political Science, 30*(2), 421–445.
- Fearon, J. D. (1994). Domestic political audiences and the escalation of international disputes. *American Political Science Review, 88*(3), 577–592.
- Fearon, J. D. (1995). Rationalist explanations for war. *International Organization, 49*(3), 379–414.
- Goldstein, J. S. (1991). Reciprocity in superpower relations: An empirical analysis. *International Studies Quarterly, 35*(2), 195–209.
- Goldstein, J. S., & Freeman, J. R. (1990). *Three-way street: Strategic reciprocity in world politics*. University of Chicago Press.
- Granger, C. W. J. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica, 37*(3), 424–438.
- Jervis, R. (1976). *Perception and misperception in international politics*. Princeton University Press.
- Kahn, H. (1965). *On escalation: Metaphors and scenarios*. Praeger.
- Liu, J., Wu, S., & Zidek, J. V. (1997). On segmented multivariate regression. *Statistica Sinica, 7*(2), 497–525.
- Moore, W. H. (1995). Action–reaction or rational expectations? Reciprocity and the domestic–international conflict nexus. *Journal of Conflict Resolution, 39*(1), 129–167.
- Richardson, L. F. (1960). *Arms and insecurity: A mathematical study of the causes and origins of war*. Boxwood Press.
- Schelling, T. C. (1966). *Arms and influence*. Yale University Press.
- Sims, C. A. (1980). Macroeconomics and reality. *Econometrica, 48*(1), 1–48.
- Thomas, J. E., Alpysbekova, A., Osei Mensah, E., Masara, N., & Sharma, P. (2026). *IranWar.ai: An open-source event-level dataset of the 2026 US–Iran conflict* [Dataset descriptor and preprint]. github.com/jethomasphd/WarTheater
- Ward, M. D. (1982). Research gaps in alliance dynamics. *International Studies Quarterly, 26*(1), 95–125.
- Yao, Y.-C. (1988). Estimating the number of change-points via Schwarz' criterion. *Statistics & Probability Letters, 6*(3), 181–189.

---

## Appendix A

**Table A1.** *VAR(1) Coefficients, Combat Regime (Days 1–40)*

| Equation | Term | Coefficient | SE | p |
|---|---|---|---|---|
| Strikes | constant | 3.38 | 1.82 | 0.063 |
| Strikes | strikes, lag 1 | 0.23 | 0.20 | 0.26 |
| Strikes | retaliation, lag 1 | 0.17 | 0.22 | 0.44 |
| Retaliation | constant | 5.21 | 1.75 | 0.003 |
| Retaliation | strikes, lag 1 | 0.05 | 0.19 | 0.78 |
| Retaliation | retaliation, lag 1 | 0.43 | 0.21 | 0.039 |

*Note.* 39 observations. Residual correlation 0.62. Source: `t02_var_combat_summary.txt`.

**Figure A1.** *Orthogonalised Impulse Responses, Combat Regime, With 95% Monte-Carlo Bands (1,000 Seeded Replications).* The only response distinguishable from zero is the same-day response; every band includes zero from the first day after the shock.
