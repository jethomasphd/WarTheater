# Paper 2 — v3: Killed Early, Left Fragile, Counted Short

**A plain-language, three-tool edition of Paper 2, built as a complete drafting
package for its first author.**

This is version 3 of [Paper 2](../README.md) of the IranWar.ai research agenda.
It keeps the same frozen dataset and the same three findings as
[version 2](../v2/README.md), and changes three things:

1. **Plain language.** Short sentences. Every statistical term is defined once in
   the text and again in a glossary. The intended reader has finished a first
   graduate statistics course in a psychology, nursing, or medical program.
2. **Three tools only.** Means comparison, correlation, and regression. Nothing
   else is used to make the case.
3. **The first author's review comments are built in.** The "policy window"
   point opens the Introduction; the exact wording for the weaker damage measure
   is given; the projection is presented as a range with 4:1 as a reference
   point; and a box explains why the dataset's two death counts differ.

> **The argument in one sentence.** The war killed early; as health-facility
> damage accumulated, each additional strike was associated with more civilian
> deaths; and the deaths we can count are a floor, not a total.

| # | Finding | Tool | Evidence |
|---|---|---|---|
| 1 | The war killed early | means comparison | 79.6% of documented deaths in Days 1–40 (23.5% of the days); half by Day 21; phase η² = 0.76; Major Combat vs First Ceasefire g = 3.44; Iranian deaths per strike location 15.4 → 0.7 |
| 2 | As facility damage accumulated, each extra strike was associated with more civilian deaths | correlation + regression with an interaction term | r(strikes, deaths) −0.41 in Days 1–15 → +0.52 in Days 40–170; strike slope −0.46 (n.s.) at 31 damaged facilities → +0.83 (p = .011) at 307; interaction p = .006 (HAC); coarser HSSI measure same direction, p = .32 |
| 3 | The counted dead are a floor | descriptive means comparison + arithmetic | 0.11 Iranian civilian deaths/day recorded on non-strike days; 0 in the 89-day ceasefire; the two direct counts differ by 14.8% (Iran) and 43.9% (Lebanon); 3:1–15:1 ratios give 12,664–58,176 total for Iran (4:1 reference: 15,830–18,180) |

## Reproduce everything (~30 seconds)

```bash
cd ResearchData/Paper2/v3
python3 -m pip install -r requirements.txt   # pandas, numpy, scipy, statsmodels, matplotlib
bash run_all.sh                              # panel + register + all tables + all figures + checks
```

The analysis is pinned to the frozen `../../releases/v1.2/iranwar_event_dataset.csv`.
There is no random element and no network access. The last two steps check the
work: `05_check_numbers.py` re-derives every headline number and asserts it
against the manuscript; `06_manuscript_tables.py` renders every table from the
result CSVs and checks that the manuscript contains it verbatim. Any drift fails
loudly.

To rebuild the Word document (optional; needs Node.js and the `docx` package):

```bash
cd manuscript && npm install docx && node make_docx.js
```

`run_all.sh` runs this step automatically when Node and the package are present
and skips it with a message otherwise. The committed `.docx` was built from the
committed outputs.

## What's here

```
v3/
├── README.md                        # this file
├── requirements.txt                 # pinned dependencies (same as v2)
├── run_all.sh                       # one-command reproduction + checks
├── src/
│   ├── util.py                      # pinning, health-system register (audited), daily panel, plot style
│   ├── 00_build_panel.py            # dataset -> data/panel_daily.csv + data/health_system_events.csv
│   ├── 01_means_comparison.py       # Finding 1 -> t1_*, fig1
│   ├── 02_correlation.py            # bridge: strikes vs deaths by damage period -> t2_*, fig2
│   ├── 03_regression.py             # Finding 2: interaction model, slopes at observed damage levels -> t3_*, fig3
│   ├── 04_floor.py                  # Finding 3: what the series records, accounting gap, projection -> t4_*, fig4-5
│   ├── 05_check_numbers.py          # every headline number re-derived + asserted -> numbers.json, t0
│   └── 06_manuscript_tables.py      # manuscript tables rendered from CSVs + checked verbatim
├── data/                            # regenerated panel + audited register (identical to v2 and the parent)
├── output/
│   ├── tables/                      # t0–t4 result tables (.csv)
│   ├── figures/                     # fig1–fig5 (.png + .pdf)
│   ├── numbers.json                 # machine-readable headline numbers
│   └── manuscript_tables.md         # the manuscript's tables, rendered
├── manuscript/
│   ├── paper2_v3.md                 # the paper (canonical text; plain language; drafting notes inside)
│   ├── paper2_v3.docx               # the Word drafting document, built from the .md
│   ├── make_docx.js                 # builds the .docx from the .md + figures
│   └── references.bib
└── docs/
    ├── STUDENT_GUIDE.md             # start here: the three findings, number by number
    ├── WRITING_GUIDE.md             # sentence frames for reporting each result; words to use and avoid
    ├── GLOSSARY.md                  # every statistical term, defined with an example from this paper
    ├── ANSWERS_TO_REVIEW_QUESTIONS.md  # the first author's four questions, answered
    ├── METHODS.md                   # design decisions for the three tools
    ├── CODEBOOK_panel.md            # variable definitions
    └── CHANGES_FROM_V2.md           # what changed and why, including two corrections
```

## Where to start

- **First author:** `docs/STUDENT_GUIDE.md`, then `manuscript/paper2_v3.docx`. The
  drafting notes inside the manuscript (shaded boxes; Word style "Drafting Note")
  say where your writing goes and how to phrase each claim. Start with the water
  passage in Section 4.4, as you offered.
- **Reviewer:** `manuscript/paper2_v3.md`, then `docs/METHODS.md` and
  `docs/CHANGES_FROM_V2.md`.
- **Anyone checking a number:** `output/numbers.json`, then the table it names.

## What changed from v2, in brief

Full record in `docs/CHANGES_FROM_V2.md`. Two corrections matter for anyone who
has read v2:

- v2 reported the strike slope at damage = mean ± 1 SD. Mean + 1 SD is 116% of
  the final damage level, above the highest level that occurred (100%). v3
  reports slopes at damage levels that occurred (31, 155, 232, and 307
  facilities). Same pattern, different end values: v2 0.18 → 1.07; v3 −0.46 → +0.83.
- v2 said the deadliest single day was Day 1. In the daily series it was Day 40
  (257 deaths, most in Lebanon). The sentence is removed.

## Data & citation

- **Data:** IranWar.ai Event-Level Research Dataset v1.2 (`../../releases/v1.2/`).
- **Cite:** Osei Mensah, E., & Thomas, J. E. (2026). *Killed Early, Left Fragile,
  Counted Short: Civilian Deaths and Health-System Damage in the First 170 Days
  of the 2026 US–Iran War.* IranWar.ai Research Agenda, Paper 2 (v3).
  github.com/jethomasphd/WarTheater.
