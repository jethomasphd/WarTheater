# What changed from version 2, and why

This file records every difference between v2 (`../../v2/`) and v3, so that a
reader of v2 is not surprised and so that nothing is hidden.

## Same

- The frozen dataset (v1.2, Days 1–170).
- The daily panel and the audited 21-event health-system register. The code in
  `src/util.py` and `src/00_build_panel.py` is carried over unchanged (only the
  header comments differ), so `data/panel_daily.csv` and
  `data/health_system_events.csv` are identical to v2's.
- The three findings and their direction.
- The primary interaction model (Model 3) and its interaction coefficient
  (b = 0.0145, HAC p = .006).
- The projection table (same ratios, same direct-toll bounds, same totals).

## Changed

### 1. Language

Every sentence in the manuscript, the methods, and the guides was rewritten in
plain language. Metaphors were removed. Each statistical term is defined where
it first appears and again in `GLOSSARY.md`. Each results section follows the
same skeleton: Question, What we compared, Result, What it means, What it does
not mean.

### 2. Tools

v2 used ANOVA, Welch's ANOVA, Kruskal–Wallis, Mann–Whitney, a temporal
concentration ratio, a moderation model with Johnson–Neyman probing, and the
projection. v3 uses three tools: means comparison, correlation, and regression.

- Kruskal–Wallis is dropped. Welch's ANOVA stays only as a one-line check that
  agrees with the ordinary ANOVA.
- Mann–Whitney stays only as a check column in the deaths-per-strike table; the
  reported test is a Welch t-test with Hedges' g and a confidence interval.
- The temporal concentration ratio (0.64 in v2) is dropped from the text; the
  cumulative curve, the day at which half the deaths had happened, and the share
  by Day 40 carry the same information in plainer form.
- A correlation step is added (`02_correlation.py`) as the plain version of the
  interaction model: Pearson r and simple regression slopes within three damage
  periods, with a Fisher r-to-z comparison.
- The interaction model reports both ordinary and HAC (Newey–West) p-values so
  the reader can see that the conclusion does not depend on the adjustment.
- The Johnson–Neyman boundary is kept but translated into a facility count and
  a day ("the slope is significant from about 238 damaged facilities upward,
  reached on Day 33").

### 3. Simple slopes probed at observed damage levels (correction)

v2 reported the strike slope at damage = mean − 1 SD, mean, and mean + 1 SD
(0.18, 0.63, 1.07). The facility-damage curve is not bell-shaped: it rises from
0 to 99% in 39 days and sits at 99–100% for the remaining 131 days, so its mean
is 85.3% and its SD is 30.7%. Mean + 1 SD is 116%, above the highest level that
ever occurred, and mean − 1 SD (54.6%) corresponds to about Day 27, not to the
"early war" as v2's label said. v3 probes at levels that occurred: 31 damaged
facilities (10%; Day 15), 155 (50%; Day 26), 232 (75%; Day 33), and 307 (99%;
Day 39 and every later day). The slopes are −0.46 (n.s.), +0.12 (n.s.), +0.48
(p = .060), and +0.83 (p = .011). The interaction coefficient is unchanged; the
"sixfold steepening" phrase from v2 is not used, because the low-damage slope is
not distinguishable from zero and a ratio of slopes is not meaningful there.
The v2 convention rows are still written to `t3_simple_slopes.csv` for
comparison, with the out-of-range row marked.

### 4. "The deadliest single day of the war was its first" (correction)

v2 stated this in Section 3. In the daily series the deadliest day for all
factions was Day 40 (257 deaths, of which 254 in Lebanon), and the deadliest day
for Iranian civilians was Day 12 (45). The sentence is removed and
`t1_milestones.csv` now records the deadliest days explicitly.

### 5. Per-strike decline reported as 95.6%

v2 wrote "95%". The value is 100 × (1 − 0.683/15.408) = 95.6%. v3 writes 95.6%.

### 6. Finding numbers

v3 numbers the findings 1, 2, 3. In v2 and the parent they were 1, 5, 6.

### 7. The accounting gap is analysed, not only stated

v2 stated the 14.8% and 43.9% gaps and carried both bounds. v3 adds
`t4_accounting_gap_by_phase.csv`, `t4_accounting_gap_milestones.csv`, Figure 4,
and Box 1 in the manuscript, which show when each gap opened: Iran's is a source
difference settled by the Day-57 re-anchoring; Lebanon's opened during the First
Ceasefire when the ministry's running total rose by 2,550 while the daily series
added 1,200. This answers the first author's review question.

### 8. What the daily series can record

v3 adds `t4_strike_vs_nonstrike_days.csv` and `t4_ceasefire_block.csv`: the
series records 0.11 Iranian civilian deaths per day on the 81 non-strike days and
zero in the 89-day ceasefire. This is the descriptive means comparison that
grounds Finding 3 before the projection.

### 9. Narrative claims checked against the source text

Every named event in the Introduction and in Section 4.4 was re-checked against
the event text in the frozen dataset. Three phrasings were tightened:
"30–40% of power generation degraded" is now "30–40% of the national grid
offline in western Iran" (the ICRC wording); "three destroyed desalination
plants" is now "desalination plants struck at Qeshm Island and Jask (Bonji) in
Iran and near Mina Abdullah in Kuwait"; "a blockade that seized medical supplies
and idled the WHO's regional logistics hub" is now "a seized cargo ship that the
Iranian Red Crescent said was carrying lifesaving medical supplies; and the WHO's
Dubai logistics hub put on hold because of regional insecurity."

### 10. Reference correction

The Jawad et al. PLoS Medicine article is 2021, 18(9), e1003810 (v2 printed 2020).
Cohen (1988) is added for the effect-size conventions the text uses.

### 11. Manuscript tables are generated and checked

v2 injected three tables into the Word file from CSVs. v3 renders all eleven
manuscript tables from the CSVs (`06_manuscript_tables.py`) and checks that the
markdown contains each one verbatim, so the text, the Word file, and the
analysis cannot drift apart.

### 12. A drafting document, not only a paper

The Word file contains shaded drafting notes (Word style "Drafting Note") that
say where the first author's writing goes and how each claim should be phrased.
They are meant to be deleted before submission.
