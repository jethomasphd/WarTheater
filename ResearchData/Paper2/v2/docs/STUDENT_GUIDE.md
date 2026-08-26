# First-Author's Guide to Paper 2 (v2 — the three findings)

*A plain-language walkthrough of the three findings this edition is built
around, written for the first author. Read it beside the manuscript
(`manuscript/paper2_v2_three_findings.md`) and the formal methods
(`docs/METHODS.md`).*

You picked three findings out of the parent paper's eight and wrote back that
they "feel like one argument." They do — and this edition turns that reading into
a paper you can own line by line. You don't need to write any code. You need to
(1) run one command, (2) explain every number, and (3) defend every decision.
This guide gets you there.

---

## 0. Run it yourself first

```bash
cd ResearchData/Paper2/v2
python3 -m pip install -r requirements.txt
bash run_all.sh
```

About thirty seconds later you have every table (`output/tables/`) and every
figure (`output/figures/`) in your manuscript, regenerated from the raw event
dataset. The last step, `04_synthesis.py`, re-derives your three headline numbers
and *checks* them — if it prints "All headline numbers verified," the paper's
spine is intact. Nothing in the manuscript exists that this command does not
produce.

---

## 1. Your argument in one paragraph

The war killed fast and early: most of the documented deaths happened in the
first six weeks, before the health system could adapt (**Finding 1**). Then, as
facility damage piled up, each additional strike was associated with more deaths
at the margin, not fewer — the system was losing its ability to absorb shocks
(**Finding 5**). And everything those two findings measure is only the
*counted*, direct death; the indirect deaths — the ward-side dying from disrupted
care and destroyed water — are several times larger and never reach a strike-day
tally (**Finding 6**). Three findings, one sentence: *killed fast, left fragile,
counted short.*

---

## 2. Finding 1 — the war killed fast and early

**What it is.** A comparison of average daily deaths across the four war phases
(ANOVA family), plus a simple picture of how fast the toll piled up
(concentration curve), plus how deadly each strike was per location (lethality).

**The numbers you own.**
- **79.6% of documented deaths fell in the 40 days of Major Combat — 23.5% of the
  war.** That is the headline. It comes straight from `t1_phase_summary.csv`
  (4,944 of 6,213 deaths) and `t1_concentration.csv`.
- The cumulative toll crossed **half by Day 21** and **80% by Day 42**
  (`t1_concentration.csv`). Figure 1B draws this.
- Phase explains **76%** of the day-to-day variance in total deaths (η² = 0.76;
  `t1_phase_anova.csv`). In behavioral research anything over 0.14 is "large" —
  0.76 is enormous, and that is the finding, not an artifact.
- Major Combat sits **3.1–3.4 standard deviations** above every other phase
  (Hedges' g; `t1_phase_pairwise.csv`). Clinical trials celebrate g = 0.5.
- Deaths **per strike location** fell from **15.4** (Major Combat) to **0.7**
  (Resumption) — a 95% collapse (`t1_lethality.csv`; Mann–Whitney U = 623,
  p < .0001, g = 1.33).

**What to say.** The political regime, not the calendar, governed when people
died — and the single largest casualty wave of the whole war landed in the first
six weeks, on a health system that had no chance to prepare. That sets up
everything else.

**The likely question.** *"Isn't 79.6% just because Major Combat is when the
fighting was?"* Yes — and that is the point. Front-loading is not only a fact
about the fighting; it is a fact about *when the burden hit the health system* —
all at once, at the start, before adaptation was possible.

---

## 3. Finding 5 — the system lost its ability to absorb shocks

**What it is.** An interaction (moderation) model: does the strike→death slope
*change* as accumulated facility damage rises?

**The numbers you own** (`t5_simple_slopes.csv`, facility-damage moderator, full
sample; and `t5_moderation.csv`):
- The slope of civilian deaths on strikes **steepens with damage**: **0.18**
  (not significant) at low damage → **0.63** (p = .025) at mean → **1.07**
  (p = .006) at high damage. Roughly a **sixfold** steepening. Figure 2A draws
  the three slopes fanning open.
- The interaction is significant with the facility-damage curve (p = .006) and
  points the same way — but is not significant — with the coarser 21-event HSSI
  (p = .32). **Report both.** You are not hiding the weaker one.
- It is not just "late war." A phase check shows the strike slope does **not**
  differ between Major Combat and the Resumption (p = .89) once the Resumption's
  lower baseline is absorbed — so the steepening tracks the *damage*, not merely
  the passage of time.

**What to say — this is your sentence to write.** *A functioning hospital can
absorb one bad night, but after enough bad nights it cannot absorb much more.*
The same strike that a health system shrugs off on Day 10 becomes catastrophic
on Day 90 because the buffer — theatre capacity, blood, power, staff — is gone.
That is resilience erosion, and you understand it clinically better than the
model does.

**The likely question (the big one).** *"You said deaths per strike FELL 95% in
Finding 1. Now you say each strike got MORE deadly. Which is it?"* Both — they
are different quantities. Finding 1's number is an **average** (total deaths ÷
total strikes), dominated by the early mass-casualty days. Finding 5's number is
a **marginal, conditional** slope inside a model, holding the moment fixed.
Averages fell; marginal coupling tightened. Internalize this — it is the most
likely gotcha.

**One honesty note to keep.** Damage accumulates with time, so it is confounded
with everything else that changed over the war. This is *effect-modification
evidence consistent with* resilience erosion — not proof of the mechanism. The
manuscript says so plainly; keep it that way.

---

## 4. Finding 6 — the counted dead are only a floor

**What it is.** Scenario arithmetic — deliberately not a model. Conflict
epidemiology consistently finds 3–15 indirect deaths per direct death, ~4:1
average. We apply those ratios to the documented direct toll.

**The numbers you own** (`t6_projection.csv`):
- Iran: **3,166–3,636** documented (the range is the two internal accountings,
  daily-series vs snapshot) → at 4:1, roughly **15,800–18,200** total.
- Lebanon: **2,993–4,308** documented → **15,000–21,500** total.
- WASH makes it concrete: the Bonji intake alone cut drinking water to **~10,000
  people across 20 villages** (`t6_wash_exposure.csv`).

**What to say — the part only you can write.** You wrote it already: the four who
die indirectly are the patient whose surgery is postponed because the theatre is
damaged, the mother who delivers without a skilled attendant because the midwife
evacuated, the dialysis patient who misses session after session. They do not
show up in the strike count. This finding is our estimate of how many of them
there are — and the argument that publishing "3,600 dead" without marking it as a
floor misrepresents what the field knows.

**The likely question.** *"Aren't you just inventing a big number?"* No — say
"projection," never "estimate," and show the whole table (1:1 to 15:1). The point
is not the specific figure; it is that the documented count is a **floor** and the
plausible range under standard ratios is large. It becomes an estimate only when
someone runs a post-war mortality survey — which is exactly what we hope this
motivates.

---

## 5. Why the three belong together

Write the discussion (§6 of the manuscript) as *one* argument, because it is one:

- Front-loading (F1) **set the terms** — the biggest wave hit first, before
  adaptation.
- Resilience erosion (F5) is **what happened next** — the system spent the long
  tail losing its slack, so late strikes cost more at the margin.
- The indirect floor (F6) is **the toll of both** — most of it uncounted.

Seen in that order, the 4:1 projection stops being a free-floating guess and
becomes the *expected shape* of the tail the first two findings predict. That
connective logic — the thing you saw when you said the findings "feel like one
argument" — is the contribution of this edition. It is yours to make in prose.

---

## 6. Where everything lives

| You need | Location |
|---|---|
| The paper | `manuscript/paper2_v2_three_findings.md` (+ `.docx`) |
| Any number in Finding 1 | `output/tables/t1_*.csv` |
| Any number in Finding 5 | `output/tables/t5_*.csv` |
| Any number in Finding 6 | `output/tables/t6_*.csv` |
| The three findings, wired + checked | `output/synthesis.json`, `t0_headline_findings.csv` |
| Any figure | `output/figures/fig1–fig3.png` (PDF for submission) |
| Why we made a decision | `docs/METHODS.md` |
| What a variable means | `docs/CODEBOOK_panel.md` |
| The 21 events + audit trail | `data/health_system_events.csv` |

Run the pipeline, read the outputs against the manuscript until every number is
yours, and bring your ward-side judgment to the discussion — that is the part
only you can write, and it is the reason this edition exists.
