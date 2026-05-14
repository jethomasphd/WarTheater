# IranWar.ai

**An open, event-level research dataset and live public intelligence dashboard for the 2026 U.S.–Iran conflict.**

[![Live dashboard](https://img.shields.io/badge/dashboard-iranwar.ai-c1121f?style=flat-square)](https://iranwar.ai)
[![Archive](https://img.shields.io/badge/briefing-archive-555?style=flat-square)](https://iranwar.ai/archive)
[![Manuscript](https://img.shields.io/badge/manuscript-PDF-1d4ed8?style=flat-square)](ResearchData/IranWar.ai_Manuscript_05132026_PDF.pdf)
[![Dataset](https://img.shields.io/badge/dataset-v1.0%20(1%2C653%20events)-2d6a4f?style=flat-square)](ResearchData/iranwar_event_dataset.csv)
[![DOI](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.20181794-1682d4?style=flat-square)](https://doi.org/10.5281/zenodo.20181794)
[![Status](https://img.shields.io/badge/release-Zenodo%20live%20%E2%80%A2%20SSRN%20in%20process-2d6a4f?style=flat-square)](#release-status-zenodo--ssrn)

---

## Read the paper first

This repository accompanies the manuscript:

> **Thomas, J. E., Alpysbekova, A., Osei Mensah, E., Masara, N., & Sharma, P. (2026).**
> *IranWar.ai: An Open-Source Event-Level Dataset of the 2026 US–Iran Conflict.*

The paper is the primary reference for everything in this repository. **Before using the data, the dashboard, or any derived product, read the manuscript.** It documents the design, the two-phase AI-assisted production protocol, the confidence model, the known limitations, and — perhaps most importantly — the epistemic framing under which this work was released into a live information environment.

- **Manuscript PDF (in repo):** [`ResearchData/IranWar.ai_Manuscript_05132026_PDF.pdf`](ResearchData/IranWar.ai_Manuscript_05132026_PDF.pdf)
- **Editable source (DOCX):** [`ResearchData/IranWar.ai_Manuscript_05132026.docx`](ResearchData/IranWar.ai_Manuscript_05132026.docx)
- **Preferred citable copy:** the Zenodo-indexed release — **[doi.org/10.5281/zenodo.20181794](https://doi.org/10.5281/zenodo.20181794)**. Please cite this DOI in academic work; the in-repo PDF is provided as a convenience copy.

> *"The flood we have described is dual-layered. Its structural layer is largely a byproduct of how information now circulates; its strategic layer is something actors make on purpose. Transparent datasets are a meaningful counter-technology against the structural layer. Against the strategic layer, transparency is necessary but insufficient and must be paired with interpretive expertise."*
> — Manuscript, §10

---

## What this repository contains

This is a **single repository hosting four artifacts** that share a provenance trail:

1. **A live public intelligence dashboard** — [iranwar.ai](https://iranwar.ai) — updated daily since Day 1 of the conflict (February 28, 2026).
2. **The structured JSON corpus** that powers the dashboard — 16 files under `public/data/` representing the live source of truth.
3. **A versioned, event-level research dataset** — extracted from those JSON files on a scheduled cadence, released as CSV with a codebook, an extraction script, and a snapshot of the source data at the time of extraction.
4. **The manuscript** that documents items 1–3 as a research instrument and as an epistemic object: how it was built, what it knows, what it does not know, and how it should be cited and contested.

Every layer of this stack is in the public repository. There is no private companion. The prompts the AI agents use, the daily update manifests, the database snapshots, the briefing archive, and the manuscript source are all here.

---

## Release status: Zenodo & SSRN

| Channel | Status | Notes |
|---|---|---|
| **GitHub** (this repo) | **Live** | Continuously updated; the canonical working copy. |
| **Zenodo** | **Live — v1.0** | DOI: **[10.5281/zenodo.20181794](https://doi.org/10.5281/zenodo.20181794)**. Versioned deposit with long-term archival, immutable content hash, and the manuscript PDF as an attached object. **This is the preferred citation target.** |
| **SSRN** | **Submission in process** | The manuscript has been submitted to the Social Science Research Network. Until the SSRN abstract page is public and indexed, please cite the Zenodo DOI. |

**When citing, prefer (in order):** the Zenodo DOI → the SSRN abstract page when live → the in-repo manuscript PDF as a fallback.

The citation block is in [Citation](#citation) below.

---

## The paper, in one page

The manuscript is 29 pages including references. The TL;DR a reader needs to use this repository responsibly:

**What we released.** A structured, openly available record of the first 30 days of the 2026 U.S.–Iran conflict (Operation Epic Fury, February 28 – March 29, 2026): **1,653 event-level observations across 48 variables, derived from 16 curated JSON files**. Each row is a discrete, verifiable event — an airstrike on a named target, a retaliatory attack, a financial-market data point, a daily casualty estimate by faction, a naval deployment, or a diplomatic development. Nine analytical domains are covered. The dashboard is updated daily; the research dataset is released monthly with versioned snapshots and interim correction releases when warranted.

**How we built it.** A two-phase, human-in-the-loop AI workflow:

- **Phase 1 (Deep Research).** An AI research agent (Claude Opus) ingests the day's reporting from 60+ curated source streams (CENTCOM, IDF, ACLED, Iranian Red Crescent, HRANA, IAEA, Bloomberg, IMO, etc.) and produces an **Update Manifest** — a structured document specifying every change for the day, with sources, confidence ratings, and explicit handling of conflicting reports.
- **QA gate.** The human analyst reviews the manifest against an operational checklist.
- **Phase 2 (Code Execution).** A coding agent (Claude Code) applies the approved manifest to the JSON files, validates, commits, and pushes. Cloudflare Pages auto-deploys.

**What is novel.**

1. **Near-real-time, fully reproducible event data.** UCDP/ACLED-style event data with weeks-to-years of lag is reduced to a daily cadence with public provenance.
2. **Record-level confidence scoring** (HIGH 76% / MEDIUM 20% / LOW 4% in v1.0) carried into every downstream release.
3. **Cross-domain integration in one event-level structure** — military, financial, humanitarian, naval, diplomatic, cyber, and contextual events in one schema, enabling questions that fragmented datasets cannot answer (e.g., do strikes near Hormuz produce immediate Brent-crude spikes, and on what timescale do those spikes decay?).
4. **The dataset is released as an epistemic object,** not as ground truth — with known interpolations, unverified records, and confidence ratings preserved rather than averaged away.

**Why now.** The 2026 U.S.–Iran conflict is the first sustained interstate war of the generative-AI era. Synthetic video, AI-generated still imagery, and coordinated influence operations are entering the open-source pipeline at industrial scale (Cyabra, 2026; Murray & Linvill, 2026). The manuscript frames this as a **dual-layer information flood**: a *structural* layer (the volume, velocity, and synthetic origin of available data outpacing the infrastructure to evaluate it) and a *strategic* layer (deliberate adversarial production by state and non-state actors). The release argues that transparent datasets — datasets that carry their own provenance, uncertainty, and interpretive history — are a **counter-technology** against the structural layer, and a necessary (though not sufficient) foundation against the strategic one.

**What this is not.** It is not classified intelligence. It is not a verified body-count. It is not a war-crimes registry. It is not a substitute for retrospective, peer-reviewed conflict datasets (UCDP-GED, ACLED) that operate at slower verification timescales. It is a near-real-time, AI-assisted, publicly auditable record — **with its uncertainty visible.** Read the manuscript before applying these data to any sensitive question.

---

## Dataset v1.0 at a glance

The first scheduled monthly release covers the **first 30 days of conflict (Day 0 baseline, January 2, 2026 → Day 30, March 29, 2026)**.

| Metric | v1.0 |
|---|---|
| Event-level observations | **1,653** |
| Variables (columns) | 48 |
| Source JSON files | 16 |
| Curated source streams | 60+ |
| Countries / zones covered | 13 |
| Iranian provinces with documented strikes | 26 of 31 |
| Distinct strike locations | 61 |
| HIGH confidence rows | 76% |
| MEDIUM confidence rows | 20% |
| LOW confidence rows | 4% |
| Reproducible extraction | `ResearchData/build_dataset.py` |

**Event domains (v1.0):**

| Domain | N | Description |
|---|---|---|
| STRIKE | 641 | U.S./Israeli offensive strikes on Iranian territory |
| RETALIATION | 307 | Iranian / Hezbollah / Houthi / proxy counter-attacks |
| FINANCIAL | 301 | Oil prices, market indices, war costs, tanker transits |
| HUMANITARIAN | 173 | Daily casualty reports by faction, infrastructure damage |
| OTHER | 69 | Daily briefing headlines, aggregate snapshots |
| DIPLOMATIC | 66 | Political statements, ceasefire negotiations |
| MILITARY | 64 | General military events, U.S. base reference data |
| NAVAL | 28 | Fleet deployments, Strait of Hormuz events |
| CYBER | 4 | Offensive and defensive cyber operations |

### Files you actually want to open

| Path | What it is |
|---|---|
| [`ResearchData/iranwar_event_dataset.csv`](ResearchData/iranwar_event_dataset.csv) | **The dataset.** 1,653 rows × 48 columns. UTF-8 CSV. |
| [`ResearchData/codebook.csv`](ResearchData/codebook.csv) | Codebook — every column, type, definition, source. |
| [`ResearchData/build_dataset.py`](ResearchData/build_dataset.py) | Reproducible extraction script. Identical output from identical inputs. |
| [`ResearchData/dataset_README.md`](ResearchData/dataset_README.md) | Dataset-level README (schema, fields, examples). |
| [`ResearchData/SOURCE_SCHEMAS.md`](ResearchData/SOURCE_SCHEMAS.md) | The shape of each of the 16 source JSON files. |
| [`ResearchData/AGENT_PROTOCOL.md`](ResearchData/AGENT_PROTOCOL.md) | The two-phase AI protocol in operational detail. |
| [`ResearchData/paper_seeds/`](ResearchData/paper_seeds/) | Twelve seed proposals across disciplines (clinical psychology, financial economics, political science, public health, military studies, developmental psychology, IR, psychiatry, peace & conflict studies, environmental health, media studies, health economics) — starting points for collaborators. |
| [`ResearchData/IranWar.ai_Manuscript_05132026_PDF.pdf`](ResearchData/IranWar.ai_Manuscript_05132026_PDF.pdf) | **The manuscript.** Read first. |
| [`snapshots/YYYY-MM-DD_DATABASE_SNAPSHOT.zip`](snapshots/) | Daily bundles of the live JSON corpus (auto-generated at 03:00 CT). |

### Reproduce v1.0

```bash
git clone https://github.com/jethomasphd/WarTheater.git
cd WarTheater
python3 ResearchData/build_dataset.py
# Produces iranwar_event_dataset.csv from the JSON corpus in public/data/.
```

Identical inputs → identical outputs. Each future monthly release will ship the script *and* a frozen snapshot of the source JSON files it was run against, so any release can be regenerated bit-for-bit years later.

---

## Authorship

Contributions follow the [CRediT](https://credit.niso.org/) taxonomy.

| Author | Contributions |
|---|---|
| **Jacob E. Thomas, MA, PhD** | Principal investigator; conceptualization; dashboard architecture; data infrastructure and software; writing — original draft |
| **Aigerim Alpysbekova, MPH, PhD(c)** | Public health and humanitarian methodology; writing — review and editing |
| **Eugene Osei Mensah, BSN, RN** | Data validation; writing — review and editing |
| **Nigel Masara, BSc, MSc** | Data validation; writing — review and editing |
| **Prakhar Sharma, PhD** | Political science methodology; writing — review and editing |

**Corresponding author:** Jacob E. Thomas — [JEThomasPhD@gmail.com](mailto:JEThomasPhD@gmail.com)

---

## Citation

**Preferred citation (Zenodo v1.0):**

```
Thomas, J. E., Alpysbekova, A., Osei Mensah, E., Masara, N., & Sharma, P. (2026).
IranWar.ai: An Open-Source Event-Level Dataset of the 2026 US–Iran Conflict
(v1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.20181794
```

**BibTeX:**

```bibtex
@dataset{thomas2026iranwar,
  author       = {Thomas, Jacob E. and Alpysbekova, Aigerim and
                  Osei Mensah, Eugene and Masara, Nigel and Sharma, Prakhar},
  title        = {{IranWar.ai}: An Open-Source Event-Level Dataset of the
                  2026 {US}--{Iran} Conflict},
  year         = {2026},
  version      = {1.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.20181794},
  url          = {https://doi.org/10.5281/zenodo.20181794}
}
```

If you use the data in academic work, please also cite the underlying source streams (CENTCOM, ACLED, HRANA, IAEA, etc.) where appropriate — they are documented at record level in the dataset.

---

## How the dashboard and dataset relate

The dashboard and the research dataset are two faces of the same evidence base.

```
╔════════════════════════════════════════════════════════════════════════════╗
║                       PROVENANCE TRAIL (full repo)                         ║
║                                                                            ║
║   Source reporting  →  Phase 1 Research Agent  →  Update Manifest          ║
║   (CENTCOM, IDF,        (Claude Opus, prompted    (markdown, source-tagged,║
║   ACLED, Red             with daily checklist)    confidence-scored)       ║
║   Crescent, HRANA,                                                         ║
║   IAEA, Bloomberg…)                                                        ║
║                                          │                                 ║
║                                          ▼                                 ║
║                                Human analyst QA gate                       ║
║                                          │                                 ║
║                                          ▼                                 ║
║                          Phase 2 Code Agent (Claude Code)                  ║
║                                          │                                 ║
║                       ┌──────────────────┴──────────────────┐              ║
║                       ▼                                     ▼              ║
║              public/data/*.json                   ResearchData/            ║
║              (live dashboard)                     monthly versioned        ║
║                       │                           event-level CSV          ║
║                       ▼                                                    ║
║              Cloudflare Pages                     build_dataset.py         ║
║              auto-deploy                          (deterministic extract)  ║
║                       │                                                    ║
║                       ▼                                                    ║
║              https://iranwar.ai                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

The dashboard is what the public sees. The dataset is what researchers cite. Both come from the same JSON corpus and the same human-audited AI pipeline; only the **release cadence** differs (daily for the dashboard, monthly for versioned CSV releases).

---

## Repository architecture

```
WarTheater/
├── ResearchData/                       # ★ Research artifacts (Zenodo deposit target)
│   ├── IranWar.ai_Manuscript_05132026_PDF.pdf   # ★ THE PAPER — read first
│   ├── IranWar.ai_Manuscript_05132026.docx      # Editable manuscript source
│   ├── iranwar_event_dataset.csv                # v1.0 event-level dataset
│   ├── codebook.csv                              # Column-level codebook
│   ├── build_dataset.py                          # Reproducible extraction
│   ├── dataset_README.md                         # Dataset-level docs
│   ├── SOURCE_SCHEMAS.md                         # Shape of each source JSON
│   ├── AGENT_PROTOCOL.md                         # Two-phase AI protocol detail
│   ├── seed.md                                   # Project seed / origin doc
│   └── paper_seeds/                              # 12 cross-disciplinary research-question seeds
│
├── public/                             # Cloudflare Pages deploy root (the dashboard)
│   ├── index.html                      # Main dashboard (single-page app)
│   ├── archive.html                    # Briefing archive (dynamic; reads index.json)
│   ├── css/                            # design-system.css, animations.css, responsive.css
│   ├── js/                             # app.js, map.js, financial.js, timeline.js, briefing.js, …
│   ├── img/                            # SVG assets
│   └── data/                           # ALL LIVE DASHBOARD DATA (source of truth)
│       ├── hero-stats.json             # Hero metrics + history
│       ├── strikes-iran.json           # U.S./Israeli strike locations
│       ├── strikes-retaliation.json    # Iranian / proxy retaliation
│       ├── carriers.json               # Naval force disposition
│       ├── timeline-events.json        # Conflict timeline
│       ├── baselines.json              # Pre-war financial snapshot (Feb 27)
│       ├── hormuz.json                 # Strait of Hormuz incidents
│       ├── oil-prices.json             # Brent / WTI time series
│       ├── markets.json                # S&P 500 + sector indices
│       ├── war-costs.json              # Daily cost + tanker transits
│       ├── casualties.json             # Daily casualty breakdown
│       ├── infrastructure.json         # Infrastructure damage grid
│       ├── historical-comparison.json  # Conflict-vs-conflict comparator
│       ├── global-bases.json           # U.S. military base markers
│       ├── calculator.json             # Gas-cost calculator config
│       └── briefings/                  # Daily intelligence briefings
│           ├── index.json              # Dynamic archive index
│           └── day-N.html              # HTML fragments — one per day
│
├── ops/                                # Operational protocol & prompts
│   ├── protocol.md                     # Full daily-update protocol
│   ├── daily-checklist.md              # QA checklist for manifest review
│   └── prompts/
│       ├── phase1-deep-research.md     # Claude Deep Research template
│       └── phase2-code-execution.md    # Claude Code agent template
│
├── scripts/
│   ├── validate-data.sh                # Validate all JSON data files
│   ├── war-day.sh                      # Calculate the current war day number
│   └── snapshot-data.sh                # Bundle JSONs into a daily snapshot zip
│
├── snapshots/                          # Daily data snapshots (auto-generated 03:00 CT)
│   └── YYYY-MM-DD_DATABASE_SNAPSHOT.zip
│
├── .github/workflows/
│   └── daily-data-snapshot.yml         # GitHub Action: daily snapshot
│
├── updates/                            # Historical update tracking
│   ├── manifests/                      # Archived update manifests
│   └── YYYY-MM-DD*/                    # Per-day update logs and corrections
│
├── CLAUDE.md                           # Agent context (read by Claude Code)
└── README.md                           # This file
```

### Tech stack

| Layer | Technology |
|---|---|
| Hosting | Cloudflare Pages (static, auto-deploys on push to `main`) |
| Maps | Leaflet.js + OpenStreetMap tiles |
| Charts | Chart.js 4.x |
| Fonts | Barlow Condensed, JetBrains Mono, IBM Plex Sans |
| AI agents | Claude Opus (Anthropic) — research, data enrichment, code execution |
| Build step | **None.** No framework, no npm, no bundler. Pure HTML, CSS, vanilla JS. |
| Data | Static JSON in git, versioned per commit |

The absence of a build step is deliberate. Every byte the browser renders is in the repository.

---

## The daily update cycle

```
 PHASE 1: RESEARCH                       PHASE 2: EXECUTION
 ─────────────────                       ──────────────────
 ┌──────────────────┐                    ┌──────────────────┐
 │                  │                    │                  │
 │  Claude Deep     │      Manifest      │  Claude Code     │
 │  Research        │  ────────────────► │  (coding agent)  │
 │                  │   (analyst-        │                  │
 │  Ingests current │    approved)       │  Reads manifest  │
 │  data state +    │                    │  Updates JSONs   │
 │  researches      │                    │  Creates briefing│
 │  overnight       │                    │  Validates       │
 │  events          │                    │  Commits + pushes│
 │                  │                    │                  │
 └──────────────────┘                    └────────┬─────────┘
                                                  │
                                                  ▼
                                         Cloudflare Pages
                                         auto-deploys to
                                         iranwar.ai
```

- **03:00 CT:** A GitHub Action bundles the 15 dashboard JSONs + the briefings index into `snapshots/YYYY-MM-DD_DATABASE_SNAPSHOT.zip` — the daily pre-flight export.
- **Morning ET:** The operator uploads the snapshot + the Phase 1 prompt to Claude Deep Research. The agent emits an Update Manifest.
- **QA gate:** Operator reviews manifest against `ops/daily-checklist.md` — schema compliance, geographic plausibility, source quality, sanity checks. Nothing goes in without human approval.
- **Phase 2:** Approved manifest + the Phase 2 prompt are given to Claude Code, which executes JSON edits, builds the day's briefing HTML fragment, validates, and pushes.
- **Auto-deploy:** Cloudflare Pages publishes to [iranwar.ai](https://iranwar.ai).

The **Update Manifest is the contract** between phases — structured enough for a coding agent to execute without ambiguity, sourced enough for an analyst to audit before execution.

---

## Source hierarchy

The dashboard and dataset draw from a deliberate hierarchy. When sources conflict, we **document the discrepancy as a political fact**, not as a defect to be averaged away.

| Category | Examples |
|---|---|
| U.S. government | CENTCOM, DoD, Pentagon, White House, CISA, State Dept. |
| Israeli government | IDF, Magen David Adom |
| Iranian sources | Red Crescent, Health Ministry, IRNA, HRANA, Hengaw |
| International organizations | IAEA, WHO, OCHA, UNHCR, IMO, IEA |
| Conflict monitoring | ACLED, CTP-ISW, Bellingcat, BBC Verify |
| Financial | Bloomberg, ICE Futures, NYMEX, AAA, EIA, FRED |
| Military tracking | USNI Fleet Tracker, CRS Reports, DVIDSHUB, TWZ |
| Wire services | Reuters, AP, AFP, Al Jazeera, CNN, NYT |

Record-level source attribution is preserved in the dataset (see codebook).

---

## Known limitations

Reproduced from §5 of the manuscript. Read the full section before using the data for any sensitive question.

1. **Casualty figures are from initial reports.** Iranian casualty data comes primarily from the Iranian Red Crescent and HRANA. Order-of-magnitude discrepancies on the same dates are documented but **not** reconciled — we treat them as politically informative signal, not as defects.
2. **Daily casualty data are estimates, not counts.** Derived from dashboard chart-display data. Cumulative totals may not equal the sum of daily estimates.
3. **Four retaliation records are unverified** as of v1.0. Flagged via `strike_verified=false`; may be resolved in subsequent releases.
4. **Financial data has gaps on non-trading days.** Oil prices and market indices are NULL on weekends/holidays. Sector data is index-normalized to Feb 27 = 100.
5. **War-cost estimates are interpolated** from two public anchors ($11.3 B / Day 6 — Pentagon; $16.5 B / Day 12 — CSIS). Treat as approximations with meaningful uncertainty.
6. **`active_days` indicate location-level activity, not sortie counts.**
7. **The dataset cannot capture what was not reported** — classified operations, blackout zones, suppressed events.
8. **Time-zone imprecision** — timeline timestamps reflect the reporting source's time zone (IRST, GST, IST, ET) and are not normalized to UTC.

There is also a **politics of event classification** (§5.1 of the manuscript): every event is classified across three contested dimensions — *description*, *categorization*, and *attribution* — and the coding choices are not politically neutral. Researchers applying these data to coding-sensitive analyses should treat the labels as one defensible interpretation among several and use source-disaggregated records to measure contestation rather than hide it.

---

## Disclaimer

**Read this before using the data.**

This project is built and maintained with AI agents (Claude). These models hallucinate dates, fabricate figures, and miscalculate with full confidence. The principal investigator audits aggressively but makes no guarantee of accuracy.

In a kinetic conflict, accurate information is nearly impossible to obtain in real time. Sources contradict. Governments lie. Propaganda is pervasive on every side. This is the flood — and no filter is perfect.

**Do not rely on this data for financial, military, operational, clinical, or life-safety decisions.**

Every line of code is open. Every data source is cited. The entire repository is public. Fork it. Audit it. Improve it. Push corrections back.

---

## Ethics

This dataset documents a real, ongoing armed conflict. It contains records of civilian casualties, attacks on schools and hospitals, and other events of human suffering.

Researchers using these data **should**:

1. Treat casualty figures with appropriate gravity and uncertainty. These numbers represent real human lives.
2. Acknowledge the limitations of OSINT data in conflict zones, particularly regarding civilian harm.
3. Be transparent about the provenance and limitations of any findings derived from the dataset.
4. Consider the potential for their work to be misused or misinterpreted.
5. Follow institutional IRB / ethics-board guidance for research involving conflict data.
6. **Propagate uncertainty.** Carry forward the `data_confidence` ratings and source attributions. Stripping uncertainty metadata and presenting figures as established fact is a form of information loss that this dataset is specifically designed to resist.

The authors affirm that this dataset was compiled exclusively from publicly available open-source intelligence. **No classified, proprietary, or restricted-access data was used.**

---

## Contributing & collaboration

The collaboration invitation in §8 of the manuscript is genuine, not formal.

The most valuable contributions:

- **Data validation** — regional expertise in Iranian studies, Gulf politics, Israeli security, Hezbollah / Houthi operations, cross-referenced against local-language sources we did not access.
- **Data extension** — district-level coding for Iranian strike locations, casualty disaggregation, exchange-rate and shipping-insurance data, displacement / migration-flow layers.
- **Methodological contributions** — deduplication, confidence calibration against subsequently confirmed reporting, validation of the proposed Population Harm Exposure Index (PHEI, §7.3 of the manuscript).
- **Analysis and publication** — peer-reviewed work using the dataset is encouraged. Please cite (see [Citation](#citation)) and contribute corrections back.

**How to contribute.** Fork → branch → PR. Add data, corrections, or analyses to `ResearchData/` with a clear description of what changed and why. For coordination, open an issue.

### Run locally

```bash
git clone https://github.com/jethomasphd/WarTheater.git
cd WarTheater

# It's a static site — just open it
open public/index.html

# Or serve locally
npx serve public

# Reproduce the v1.0 CSV
python3 ResearchData/build_dataset.py
```

---

## Release cadence

| Channel | Cadence |
|---|---|
| Live dashboard (`public/data/*.json`) | **Daily.** Pushed to `main`, auto-deployed by Cloudflare Pages. |
| Daily database snapshots (`snapshots/`) | **Daily, 03:00 CT,** via GitHub Action. |
| Briefing archive (`public/data/briefings/`) | **Daily** — one HTML fragment per war day; archive page auto-discovers from `index.json`. |
| Research dataset (`ResearchData/iranwar_event_dataset.csv`) | **Monthly versioned releases** (v1.0, v1.1, …). Interim correction releases when source updates, major errors, or analytically important reclassifications warrant. |
| Zenodo deposit | **Per research release.** v1.0 live at [10.5281/zenodo.20181794](https://doi.org/10.5281/zenodo.20181794). |
| Manuscript revisions | **As-needed** (errata, methodological updates). Versioned in this repository and re-deposited on Zenodo when material. |

---

## Version 2 — Corpus of War

v1 is operational: a single-researcher intelligence system powered by frontier AI. The architecture has hard ceilings — one analyst's throughput, one analytical thread, no multilingual coverage, no structural disagreement detection.

**Version 2 — "Corpus of War"** — is a blueprint for what comes next: a corpus-grounded, multi-model intelligence-fusion engine that replaces *model knowledge* with *verified evidence* and uses competitive analysis across multiple AI systems to surface ambiguity rather than hide it.

We don't need more engineers. We need the people whose knowledge makes the numbers mean something: **historians, conflict researchers, public-health workers, veterans, economists, Farsi and Arabic speakers, clinicians, community organizers** — anyone with domain expertise that the machines do not have.

Blueprint: **[iranwar.ai/Blueprint](https://iranwar.ai/Blueprint)**

No credentials required. No security clearance. No technical prerequisites.

---

## Acknowledgments

The IranWar.ai dashboard and dataset rely on the work of journalists, conflict monitors, humanitarian organizations, and government transparency offices whose reporting makes open-source intelligence possible. We particularly acknowledge ACLED, the Critical Threats Project at AEI, the USNI Fleet Tracker, and the IAEA for their systematic public reporting.

---

## Contact

**Jacob E. Thomas, PhD** — [JEThomasPhD@gmail.com](mailto:JEThomasPhD@gmail.com)

Questions, corrections, data submissions, bug reports, collaboration inquiries — all welcome.

---

## License

The **code** in this repository (HTML, CSS, JS, Python, shell scripts, GitHub Actions) is released open-source: use it, fork it, build on it. Attribution appreciated.

The **dataset, manuscript, and accompanying research artifacts** under `ResearchData/` are released for open scholarly use under the same spirit. Cite the work (see [Citation](#citation)) when you build on it, propagate the uncertainty metadata, and contribute corrections back where you can. When the Zenodo deposit goes live, the formal license terms (anticipated: code under MIT, data and manuscript under CC-BY-4.0) will be attached to the deposit and reflected here.

The effort is what matters.
