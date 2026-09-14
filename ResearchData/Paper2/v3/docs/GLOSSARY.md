# Glossary

*Every statistical term used in Paper 2, v3, with a plain definition, an example
from this paper, and the way to write it. Terms are in the order a reader meets
them.*

---

**Conflict-day.** The unit of analysis. One row per day, Days 1–170. Everything
in the paper is a property of a day: strikes that day, deaths that day, damage
accumulated by that day.

**Mean and standard deviation (SD).** The mean is the average. The SD measures
how spread out the values are around the mean. *Example:* during Major Combat,
all-faction deaths per day had a mean of 123.6 and an SD of 47.0. *Write:*
"123.6 (SD 47.0)".

**Share of days / share of deaths.** A phase's length as a percentage of 170
days, and its deaths as a percentage of all 6,213 documented deaths. *Example:*
Days 1–40 are 23.5% of the days and hold 79.6% of the deaths.

**One-way ANOVA.** A test of whether three or more group means differ. It
compares the variation between groups with the variation within groups and
gives an F statistic with two degrees of freedom and a p-value. *Example:*
F(3, 166) = 172.3, p < .001 for deaths per day across the four phases.
*Write:* "F(df1, df2) = value, p".

**Welch's ANOVA.** The same test without the assumption that the groups have
equal variances. Reported here as a check; it agrees with the ordinary ANOVA.

**p-value.** The probability of seeing a difference at least as large as the one
observed if there were really no difference. Below .05 is called statistically
significant. A p-value says nothing about how large the difference is. *Write:*
"p = .034"; "p < .001". No leading zero.

**η² (eta-squared).** The share of the total variance in the outcome that group
membership explains. Runs from 0 to 1. Conventions: 0.01 small, 0.06 medium,
0.14 large. *Example:* η² = 0.76: phase explains 76% of the day-to-day variance
in deaths.

**ω² (omega-squared).** A version of η² corrected for the number of groups and
the sample size. Slightly smaller than η². *Example:* ω² = 0.75.

**Welch t-test.** A test of whether two group means differ, without assuming the
groups have equal variances. Gives t, degrees of freedom (often not a whole
number), and p. *Example:* Welch t(46.7) = 14.11, p < .001.

**Difference in means with 95% confidence interval (CI).** The gap between two
group means, with a range of values consistent with the data. If the range
excludes zero, the difference is significant at the 5% level. *Example:*
109.9 deaths per day (95% CI 94.3 to 125.6).

**Holm adjustment.** When several tests are run, the chance that at least one
is a false positive rises. The Holm procedure raises the p-values so that this
chance stays at 5% across all the tests. *Example:* six pairwise comparisons,
each reported with a Holm-adjusted p.

**Hedges' g.** The difference between two means divided by the pooled standard
deviation, with a small-sample correction. It is Cohen's d with the correction.
Conventions: 0.2 small, 0.5 medium, 0.8 large. *Example:* g = 3.44 for Major
Combat vs the First Ceasefire.

**Mann–Whitney test.** A rank-based test of whether two groups differ, used when
the values are skewed. Reported here only as a check on the Welch t-test for
deaths per strike location.

**Deaths per strike location.** On a strike day, Iranian deaths (civilian plus
military) divided by the number of distinct places struck. An average yield per
place struck. *Example:* 15.4 in Major Combat, 0.7 in the Resumption.

**Cumulative curve.** The share of all documented deaths that had happened by
each day. *Example:* 50% by Day 21; 80% by Day 42.

**Pearson correlation (r).** How closely two variables move together, from −1
(perfect opposite movement) through 0 (no linear relationship) to +1 (perfect
joint movement). *Example:* r = +0.52 between strike locations and civilian
deaths in Days 40–170. *Write:* "r = +0.52, p < .001, n = 131".

**Spearman's rank correlation (rho).** A correlation computed on ranks instead
of raw values; less affected by extreme days. Reported as a check.

**Fisher's r-to-z test.** A test of whether two correlations from independent
samples differ. *Example:* r = −0.41 (Days 1–15) vs r = +0.52 (Days 40–170):
z = −3.35, p = .001.

**Simple regression.** A straight line fitted to predict one variable from
another. Its **slope** is the change in the outcome for a one-unit change in the
predictor. *Example:* within Days 40–170, the slope of deaths on strike
locations was +0.29: one more strike location, 0.29 more deaths.

**Intercept.** The predicted value of the outcome when the predictor is zero.

**R² (R-squared).** The share of the outcome's variance that the regression
explains. *Example:* R² = 0.44 for Model 1, 0.69 for Model 3.

**Multiple regression.** A regression with more than one predictor. Each
coefficient is the change in the outcome for a one-unit change in that
predictor, holding the others fixed.

**Mean-centering.** Subtracting the mean from a predictor before fitting the
model, so that zero means "average". Used in interaction models so that the
lower-order coefficients are interpretable and the product term is not highly
correlated with its parts.

**Interaction term.** The product of two predictors, added to a regression. Its
coefficient says how much the slope of one predictor changes for each one-unit
rise in the other. *Example:* b₃ = 0.0145: each one-point rise in damage (0–100
scale) raises the strike slope by 0.0145 deaths per strike location.

**Moderator.** The variable that changes the slope of another. Here, facility
damage moderates the strike–death slope.

**Simple slope.** The slope of one predictor at a chosen value of the
moderator, computed from the interaction model. *Example:* the strike slope at
307 damaged facilities is +0.83.

**Johnson–Neyman boundary.** The value of the moderator above which the simple
slope is statistically significant. *Example:* about 238 damaged facilities
(Day 33).

**Standard error (SE).** How much a coefficient would vary from sample to
sample. The coefficient divided by its SE gives t; t gives p.

**Ordinary standard errors.** The default SEs, which assume that the 170 days
are independent observations.

**Newey–West (HAC) standard errors.** SEs that allow neighbouring days to be
correlated ("autocorrelation") and the spread of the outcome to vary
("heteroskedasticity"). Usually larger than ordinary SEs, so p-values are more
conservative. The paper quotes these. *Example:* HAC p = .006 versus ordinary
p < .001 for the interaction.

**Autocorrelation.** The correlation of a series with itself one day later. A
bad day tends to follow a bad day. *Example:* 0.73 for civilian deaths per day.

**Effect modification.** When the relationship between an exposure and an
outcome differs depending on a third variable. The interaction model tests for
it. It is not the same as a mechanism: it shows that the slope changes, not why.

**Confounding.** When a third variable is tied to both the exposure and the
outcome, so that an association may not be causal. *Example:* damage rose with
time, and so did many other things; the paper cannot separate them.

**Ecological study.** A study whose units are populations or periods, not
individuals. Its associations apply to the aggregates, not to any person.

**Daily series.** The dataset's estimated deaths per day for each group. Summed
over days it gives 3,166 for Iran and 2,993 for Lebanon.

**Dashboard counter.** The dashboard's running total of deaths, updated as
reports arrived. At Day 170: 3,636 for Iran and 4,308 for Lebanon.

**Re-anchoring.** A day on which a running total was moved to a different
source's figure. *Example:* Day 57, Iran: 9,226 → 3,375.

**Lower and upper bound.** The two accountings of the direct toll, carried
together as a range rather than averaged. *Example:* Iran 3,166–3,636.

**Direct death.** A death from the attack itself, reported on or near the day.

**Indirect death.** A death that follows from damage to the systems people
depend on: disrupted care, destroyed water supply, displacement, disease.

**Indirect-to-direct ratio.** The number of indirect deaths per direct death
reported in studies of past conflicts: about 3:1 to 15:1, with 4:1 often cited
as an average.

**Projection.** A number computed under a stated assumption. *Example:*
multiplying the documented toll by 4 gives a projection of indirect deaths. Not
an estimate from the data, and never called one.

**Floor.** The lowest value a quantity can have. The documented death count is a
floor for the true toll.

**HSSI (Health-System Stress Index).** The running count of 21 audited
health-system insult events (attacks on facilities, harm to health workers,
water and sanitation disruptions, supply and access disruptions), scaled 0–100.
The secondary damage measure.

**Facility-damage curve.** The primary damage measure: a line through three
institutional counts of damaged health facilities (31 by Day 15; 307 by Day 39;
309 by Day 170), scaled 0–100.

**Strike location.** A distinct place struck on a day. A place struck on several
days counts once on each day.

**Strike day / non-strike day.** A day with at least one strike location / a day
with none. 89 and 81 days respectively.

**Kinetic day.** A day with a strike or a retaliation attack. 138 days.

**WASH.** Water, sanitation, and hygiene. The water and power events in the
paper are WASH events.
