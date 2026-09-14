# First author's guide to Paper 2, v3

*A plain-language walkthrough of the three findings, written for the first
author. Read it next to the manuscript (`manuscript/paper2_v3.md` or the Word
file) and the glossary (`GLOSSARY.md`).*

You will not need to write any code. You need to do three things: run one
command, understand every number, and write the sections marked for you. This
guide takes you through the numbers. `WRITING_GUIDE.md` takes you through the
writing.

---

## 0. Run it yourself first

```bash
cd ResearchData/Paper2/v3
python3 -m pip install -r requirements.txt
bash run_all.sh
```

About thirty seconds later you have every table (`output/tables/`) and every
figure (`output/figures/`) in the paper. The last two steps check the work. If
the run ends with "checked: all 11 tables appear verbatim in
manuscript/paper2_v3.md", the paper and the analysis agree. Nothing in the
manuscript exists that this command does not produce.

---

## 1. The argument in one paragraph

The war killed early: four of every five documented deaths happened in the
first 40 days, before the health system could adapt (**Finding 1**). As
health-facility damage accumulated, each additional strike was associated with
more civilian deaths, which is what a health system losing its ability to absorb
shocks would produce (**Finding 2**). Everything those two findings measure is
direct, counted death. The daily series cannot record deaths from disrupted
care, and even the direct counts are revised upward, so the documented count is
a floor; published ratios put the true total several times higher
(**Finding 3**). Three findings, one sentence: *killed early, left fragile,
counted short.*

---

## 2. The three tools

You have met all three in your statistics course.

**Means comparison** asks whether groups differ on average. Here the groups
are the four phases of the war and the measurement is deaths per day. The
outputs are an ANOVA (F, p, η²), pairwise t-tests (difference in means, 95% CI,
Holm-adjusted p), and an effect size (Hedges' g). Script: `01_means_comparison.py`.

**Correlation** asks whether two variables move together. Here the two
variables are strike locations per day and Iranian civilian deaths per day, and
we compute the correlation separately in three periods of the war. The outputs
are Pearson r with p, and the slope of a simple regression. Script:
`02_correlation.py`.

**Regression with an interaction term** asks whether the relationship between
two variables depends on a third. Here: does the strike–death slope depend on
how much facility damage has accumulated? The outputs are the coefficients of
three models, the interaction coefficient with its p-value, and the strike slope
at four levels of damage. Script: `03_regression.py`.

Finding 3 uses a descriptive means comparison (strike days vs non-strike days)
and plain arithmetic (a ratio times a count). Script: `04_floor.py`.

---

## 3. Finding 1 — the war killed early

**The question.** When did people die?

**The numbers you own** (all in `output/tables/t1_*.csv`):

| Number | Value | Where it comes from |
|---|---|---|
| Documented deaths, all five groups, 170 days | 6,213 | `t1_phase_summary.csv`, "Full war" row |
| Deaths in Days 1–40 | 4,944 (79.6%) | same table, "Major Combat" row |
| Days 1–40 as a share of the war | 23.5% | 40 ÷ 170 |
| Day by which half of all deaths had happened | Day 21 | `t1_milestones.csv` |
| Day by which 80% had happened | Day 42 | `t1_milestones.csv` |
| Iranian deaths by Day 40 | 3,125 of 3,166 (98.7%) | `t1_milestones.csv` |
| Iranian civilian deaths by Day 40 | 523 of 543 (96.3%) | `t1_milestones.csv` |
| Lebanese deaths by Day 40 | 1,781 of 2,993 (59.5%) | `t1_milestones.csv` |
| ANOVA, all-faction deaths per day | F(3, 166) = 172.3, p < .001, η² = 0.76 | `t1_anova.csv` |
| Major Combat vs First Ceasefire | 123.6 vs 13.7 per day; g = 3.44 | `t1_pairwise.csv` |
| Iranian deaths per strike location | 15.4 (Major Combat) → 0.7 (Resumption); 95.6% lower; g = 1.33 | `t1_lethality.csv` |

**How to read η² = 0.76.** Phase alone accounts for 76% of the day-to-day
variation in deaths. In behavioural research anything above 0.14 is called
large. This is not a subtle effect.

**How to read g = 3.44.** The Major Combat mean is 3.44 standard deviations above
the First Ceasefire mean. A clinical trial is usually happy with g = 0.5.

**What to say.** "Most of the documented deaths happened in the first 40 days,
before the health system could adapt. Half of all deaths had occurred by Day 21."

**The likely question.** *"Isn't 79.6% just because Major Combat is when the
fighting was?"* Yes, and that is the point. Front-loading is not only a fact
about the fighting. It is a fact about when the burden reached the health system:
all at once, at the start, before adaptation was possible. And it is a fact about
policy: protection that arrived after Day 40 arrived for a much smaller problem.

---

## 4. The correlation bridge

**The question.** Did strikes and same-day civilian deaths move together more
closely as facility damage accumulated?

**The numbers you own** (`t2_correlation_by_period.csv`):

| Period | Damage | r (p) | Slope |
|---|---|---|---|
| A. Days 1–15 | 0 → 31 facilities | −0.41 (.133) | −1.03 |
| B. Days 16–39 | 31 → 307 | +0.43 (.034) | +0.44 |
| C. Days 40–170 | 307 → 309 | +0.52 (< .001) | +0.29 |

The correlation in A differs from the correlation in C (Fisher's z = −3.35,
p = .001; `t2_correlation_comparison.csv`).

**How to read it.** Early in the war, a day with more strikes did not have more
civilian deaths; deaths were high every day whatever the number of strikes.
Later, days with more strikes had more deaths. The relationship became
consistent. That is what the interaction model in Finding 2 tests.

**A detail to get right.** The within-period slopes do not rise in a straight
line (−1.03, +0.44, +0.29). What rises is r, the strength of the relationship.
Do not say "the slope rose across the three periods". Say "the relationship
became stronger and more consistent".

---

## 5. Finding 2 — as facility damage accumulated, each additional strike was associated with more civilian deaths

**The question.** Does facility damage change the strike–death slope?

**The numbers you own** (`t3_models.csv`, `t3_simple_slopes.csv`, `t3_robustness.csv`):

| Number | Value |
|---|---|
| Model 1 (strikes only): slope, R² | 1.27 deaths per strike location; R² = 0.44 |
| Model 3: interaction coefficient b₃ | 0.0145 per damage point; HAC p = .006; ordinary p < .001; R² = 0.69 |
| Strike slope at 31 damaged facilities (Day 15) | −0.46, p = .176 (not significant) |
| Strike slope at 155 (Day 26) | +0.12, p = .621 |
| Strike slope at 232 (Day 33) | +0.48, p = .060 |
| Strike slope at 307 (Day 39 onward) | +0.83, p = .011 |
| Damage level from which the slope is significant | about 238 facilities (77%), Day 33 |
| Check: Major Combat only (40 days) | b₃ = 0.0145; HAC p = .012; ordinary p = .075 |
| Check: HSSI as the damage measure | b₃ = 0.0059; HAC p = .32; ordinary p = .078; slope at top +0.80 (p = .023) |
| Check: strikes × Resumption (phase check) | p = .89 |

**How to read b₃ = 0.0145.** Damage is on a 0–100 scale. For each one-point
rise in damage, the strike slope rises by 0.0145 deaths per strike location.
Ten points (about 31 facilities) raise it by about 0.15.

**How to read the simple slopes.** At 31 damaged facilities, one more strike
location was associated with no extra civilian deaths (the slope is not
different from zero). At 307, one more strike location was associated with
about 0.8 more civilian deaths.

**Why two p-values.** Days in a war are not independent: a bad day tends to
follow a bad day. The HAC p-value allows for that and is the one to quote. The
ordinary p-value is shown so a reader can see that the conclusion does not
depend on the adjustment.

**What to say.** "As facility damage accumulated, each additional strike was
associated with more civilian deaths. The evidence is consistent with a health
system losing its ability to absorb shocks. Of the two damage measures, the
facility-damage curve gives a significant interaction; the coarser 21-event
index points the same way but does not reach significance."

**The likely question (the big one).** *"You said deaths per strike FELL by 95%
in Finding 1. Now you say each strike was associated with MORE deaths. Which is
it?"* Both. Finding 1's number is an average (total deaths ÷ total strike
locations), dominated by the early mass-casualty days. Finding 2's number is a
marginal slope inside a model: at a given damage level, what did one more strike
location add? Averages fell because the early catastrophe was over. The marginal
coupling tightened because the buffer was gone. Practise saying this until it is
automatic.

**One honesty note to keep.** Damage accumulated with time, so it is confounded
with everything else that changed. This is effect-modification evidence
consistent with resilience erosion, not proof of the mechanism. The manuscript
says so; keep it that way.

---

## 6. Finding 3 — the counted dead are a floor

**The question.** How much of the toll do the counts miss?

**The numbers you own** (`t4_*.csv`):

| Number | Value |
|---|---|
| Iranian civilian deaths per day, strike days vs non-strike days | 6.00 vs 0.11 (g = 0.96) |
| Iranian civilian deaths recorded on the 81 non-strike days | 9 (all on days with a retaliation attack) |
| First Ceasefire: days, strike days, health-system events, deaths recorded | 89, 34, 8, 0 |
| Direct toll, Iran: daily series vs dashboard counter | 3,166 vs 3,636 (gap 14.8%) |
| Direct toll, Lebanon | 2,993 vs 4,308 (gap 43.9%) |
| Iran gap: where it comes from | the counter tracked high totals (9,100 at Day 40), re-anchored on Day 57 to 3,375, later 3,636; the daily series added 41 after Day 40 |
| Lebanon gap: where it comes from | agreement at Day 40 (1,781 vs 1,751); during the ceasefire the counter rose by 2,550 while the daily series added 1,200 |
| Projected total, Iran, 3:1 to 15:1 | 12,664 to 58,176 |
| Projected total, Iran, 4:1 (reference) | 15,830–18,180 |
| Projected total, Lebanon, 4:1 (reference) | 14,965–21,540 |

**How to read the strike-day comparison.** The daily series records deaths on the
day of an attack. Deaths from disrupted care do not happen on the day of an
attack, so the series cannot contain them. The ceasefire block shows this
sharply: 89 days with damage at 99–100%, eight new health-system events, and
zero Iranian civilian deaths recorded.

**How to present the projection.** Range first. "Under published ratios of 3:1
to 15:1, the total would be 12,664 to 58,176 for Iran." Then the reference:
"At the often-cited 4:1 ratio it would be 15,830–18,180." Never "we estimate".
The ratio is imported from other wars, not measured in this one.

**The likely question.** *"Aren't you just inventing a big number?"* No. Show
the whole table (1:1 to 15:1) and say "projection". The point is not the
specific figure. It is that the documented count is a floor and that the
plausible range under standard ratios is large. It becomes an estimate only when
someone runs a post-war mortality survey.

---

## 7. The sections you own

Each is marked in the manuscript with a shaded "Drafting note".

1. **Section 1.2, the policy window.** Expand the ward-side paragraph: what a
   mass-casualty surge means on a ward, and how the pressure carries into the
   shifts that follow. Two or three short paragraphs.
2. **Section 4.4, the water passage.** Start here, as you offered. The chain from
   the water event to the death in the ward, for a reader who has never worked
   in one. Half a page to a page. Use the numbers already in the text.
3. **Section 5.1 and 5.2.** Read them and add one paragraph, in your voice, on
   what "sustaining trauma care during the war" means in practice.
4. **Section 5.3.** Use the sentences as written when you speak about Finding 2.

`WRITING_GUIDE.md` has sentence frames for each of these.

---

## 8. Where everything lives

| You need | Location |
|---|---|
| The paper | `manuscript/paper2_v3.md` (+ `.docx`) |
| Any number in Finding 1 | `output/tables/t1_*.csv` |
| The correlation bridge | `output/tables/t2_*.csv` |
| Any number in Finding 2 | `output/tables/t3_*.csv` |
| Any number in Finding 3 | `output/tables/t4_*.csv` |
| Every headline number, checked | `output/numbers.json`, `output/tables/t0_headline_findings.csv` |
| Any figure | `output/figures/fig1–fig5.png` (PDF for submission) |
| Why we made a decision | `docs/METHODS.md` |
| What a variable means | `docs/CODEBOOK_panel.md` |
| What a statistical term means | `docs/GLOSSARY.md` |
| How to write a result | `docs/WRITING_GUIDE.md` |
| Your four review questions, answered | `docs/ANSWERS_TO_REVIEW_QUESTIONS.md` |
| The 21 events and the audit trail | `data/health_system_events.csv` |
