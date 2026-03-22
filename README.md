# THE WAR THEATER

**A Public Intelligence Dashboard for the 2026 Iran War**

Live at [iranwar.ai](https://iranwar.ai) | Archive at [iranwar.ai/archive](https://iranwar.ai/archive)

---

## What This Is

A situation room for the public.

Every bomb has a price tag. Every missile has a human cost. Every day the Strait of Hormuz stays closed, a gas station in Texas charges more per gallon. This dashboard makes those connections visible.

The model is the [Johns Hopkins COVID-19 Dashboard](https://coronavirus.jhu.edu/) — a single reference point for a global crisis that didn't editorialize. It presented the numbers and let the weight of the data speak. We're building that, but for war.

**IranWar.ai tracks:**
- Military operations — strikes, naval deployments, carrier positions, retaliation
- Financial impact — oil prices, markets, gas costs, war spending
- Human cost — casualties, displacement, infrastructure destruction
- Diplomacy and politics — timeline of events, congressional action, international response
- Daily intelligence briefings — analytical narratives synthesizing the day's developments

---

## The Conceptual Model

Think of this project as three concentric layers: **data**, **presentation**, and **operations**.

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ┌─────────────────────────────────────────────────────────────┐     ║
║   │              LAYER 3: OPERATIONS                             │     ║
║   │                                                              │     ║
║   │   Human analyst + AI research agent + AI code agent          │     ║
║   │   Working together in a daily cycle to update the data       │     ║
║   │                                                              │     ║
║   │   ┌───────────────────────────────────────────────────┐     │     ║
║   │   │           LAYER 2: PRESENTATION                    │     │     ║
║   │   │                                                    │     │     ║
║   │   │   HTML + CSS + JS — reads JSON, renders visuals    │     │     ║
║   │   │   Maps, charts, timelines, briefings               │     │     ║
║   │   │   Never modified during daily updates              │     │     ║
║   │   │                                                    │     │     ║
║   │   │   ┌─────────────────────────────────────────┐     │     │     ║
║   │   │   │        LAYER 1: DATA                     │     │     │     ║
║   │   │   │                                          │     │     │     ║
║   │   │   │   15 JSON files in public/data/          │     │     │     ║
║   │   │   │   + Daily briefing HTML fragments         │     │     │     ║
║   │   │   │                                          │     │     │     ║
║   │   │   │   This is the single source of truth.    │     │     │     ║
║   │   │   │   Everything the dashboard displays      │     │     │     ║
║   │   │   │   comes from these files.                │     │     │     ║
║   │   │   │                                          │     │     │     ║
║   │   │   └─────────────────────────────────────────┘     │     │     ║
║   │   │                                                    │     │     ║
║   │   └───────────────────────────────────────────────────┘     │     ║
║   │                                                              │     ║
║   └─────────────────────────────────────────────────────────────┘     ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Layer 1: Data (the truth)

Fifteen JSON files and a collection of briefing HTML fragments. That's it.

Every number on the dashboard — every marker on the map, every point on a chart, every casualty figure, every oil price — comes from a JSON file in `public/data/`. The dashboard is a pure function of this data. Change the data, the dashboard changes. Don't change the data, it doesn't.

**Core data files (updated daily):**

| File | What it powers |
|------|---------------|
| `hero-stats.json` | The big numbers at the top — oil, gas, S&P, war cost, casualties |
| `oil-prices.json` | Brent/WTI price charts |
| `markets.json` | S&P 500 + sector breakdown charts |
| `war-costs.json` | Daily spending + tanker transit charts |
| `casualties.json` | Casualty breakdown charts |
| `timeline-events.json` | The conflict timeline |
| `calculator.json` | "What is this war costing you?" gas calculator |

**Event-driven files (updated as needed):**

| File | What it powers |
|------|---------------|
| `strikes-iran.json` | Strike markers on the map (U.S./Israeli) |
| `strikes-retaliation.json` | Retaliation markers (Iranian/proxy) |
| `carriers.json` | Naval force disposition on the map |
| `hormuz.json` | Strait of Hormuz incident tracker |
| `infrastructure.json` | Infrastructure damage grid |
| `global-bases.json` | U.S. military base markers |
| `historical-comparison.json` | "How does this compare?" panel |
| `baselines.json` | Pre-war financial snapshot (Feb 27) |

**Briefings:**

| File | What it powers |
|------|---------------|
| `briefings/index.json` | Archive page index — day, date, headline, file path per briefing |
| `briefings/day-N.html` | Individual briefing content (HTML fragment, not a full page) |

### Layer 2: Presentation (the glass)

Pure HTML, CSS, and vanilla JavaScript. No framework. No build step. No npm.

The JS files (`public/js/`) fetch the JSON data and render it into interactive visualizations: Leaflet maps, Chart.js graphs, filterable timelines, and analytical briefings. The HTML and CSS are the structure and styling.

**The key architectural rule:** during a daily update, you only touch data files. The presentation layer is stable — it doesn't need to change when new events happen. The one exception is the current-day briefing panel in `index.html`, which is hardcoded for performance (it's what users see first).

The archive page (`archive.html`) is fully dynamic — it reads `briefings/index.json` and lazy-loads briefing HTML on demand. No manual archive editing is ever needed.

### Layer 3: Operations (the cycle)

A two-phase, human-in-the-loop AI workflow runs once daily:

```
 PHASE 1: RESEARCH                    PHASE 2: EXECUTION
 ─────────────────                    ──────────────────
 ┌──────────────────┐                 ┌──────────────────┐
 │                  │                 │                  │
 │  Claude Deep     │   Manifest     │  Claude Code     │
 │  Research        │ ──────────────>│  (coding agent)  │
 │                  │  (approved by  │                  │
 │  Ingests current │   analyst)     │  Reads manifest  │
 │  data state +    │                │  Updates JSONs   │
 │  researches      │                │  Creates briefing│
 │  overnight       │                │  Validates       │
 │  events          │                │  Commits + pushes│
 │                  │                │                  │
 └──────────────────┘                └────────┬─────────┘
                                              │
                                              v
                                     Cloudflare Pages
                                     auto-deploys to
                                     iranwar.ai
```

**Phase 1 — Deep Research:** The current data files are uploaded to Claude Deep Research along with a structured prompt (`ops/prompts/phase1-deep-research.md`). The research agent identifies the data horizon (the last date in each file), researches everything that has happened since, cross-verifies across multiple sources, and produces a structured **Update Manifest** — a markdown document containing complete JSON objects ready to be inserted.

**QA Gate:** The human analyst reviews the manifest against the operational checklist (`ops/daily-checklist.md`). Schema compliance, geographic plausibility, source quality, sanity checks. Nothing goes into the data without human approval.

**Phase 2 — Code Execution:** The approved manifest is given to Claude Code (`ops/prompts/phase2-code-execution.md`). The coding agent reads the current data files, parses the manifest section by section, executes the operations (appends, modifications, metadata updates), creates the daily briefing (HTML fragment + index entry), validates all JSON, commits, and pushes. Cloudflare Pages auto-deploys.

**The Update Manifest is the contract between phases.** It's structured enough for a coding agent to execute without ambiguity, and sourced enough for the analyst to audit before execution.

**Automated Data Snapshots:** A GitHub Action runs daily at 3:00 AM CT, bundling all 15 dashboard JSON files + the briefings index into a zip archive at `snapshots/YYYY-MM-DD_DATABASE_SNAPSHOT.zip`. This automates the pre-flight data export step — download the latest snapshot from [`snapshots/`](snapshots/) and upload it with the Phase 1 prompt to begin the daily update cycle. The action can also be triggered manually from the Actions tab.

---

## The Briefing Archive

Every day produces an intelligence briefing — an analytical narrative that synthesizes the day's developments into sections: situation summary, key developments, thematic analysis (energy war, naval posture, diplomacy, humanitarian), financial outlook, and forward-looking items.

Briefings live as HTML fragments in `public/data/briefings/day-N.html`. The archive page at [iranwar.ai/archive](https://iranwar.ai/archive) reads `briefings/index.json` and displays all briefings as collapsible cards, most recent at the top. The latest briefing auto-expands; others lazy-load on click.

```
Archive Page Load:
  1. Fetch briefings/index.json
  2. Sort by day descending
  3. Render cards (day label + headline)
  4. Auto-expand + fetch latest briefing HTML
  5. Other briefings fetch on click (lazy-load)
```

No manual editing of `archive.html` is ever required. Adding a new `day-N.html` file and an entry to `index.json` is all it takes.

---

## Data Sources

The dashboard draws from a deliberate source hierarchy. When sources conflict, we note the discrepancy rather than silently picking one.

| Domain | Primary Sources |
|--------|----------------|
| **Financial** | FRED, Yahoo Finance, Bloomberg, ICE/NYMEX, AAA, GasBuddy |
| **Military** | CENTCOM, DoD press releases, USNI Fleet Tracker, ACLED |
| **Humanitarian** | UNHCR, OCHA, ICRC, Iranian Red Crescent, Hengaw/HRANA |
| **News wire** | Reuters, AP, Al Jazeera, BBC, Times of Israel |
| **Defense media** | USNI News, The War Zone, Defense One, Breaking Defense |
| **OSINT** | Planet Labs imagery, Bellingcat, verified X accounts |

Updates are published **once daily**, typically mornings US Eastern.

---

## Disclaimer

**Read this before using the data.**

This project was built and is maintained with AI agents (Claude). These models hallucinate dates, fabricate figures, and miscalculate with total confidence. The creator audits aggressively but makes no guarantees of accuracy.

In a kinetic conflict, accurate information is nearly impossible to obtain. Sources contradict. Governments lie. Propaganda is pervasive on every side. This is the flood — and no filter is perfect.

**Do not rely on this data for financial, military, or life-safety decisions.**

Every line of code is open. Every data source is cited. The entire repository is public. Fork it. Audit it. Improve it.

---

## Architecture

```
WarTheater/
├── public/                           # Cloudflare Pages deploy root
│   ├── index.html                    # Main dashboard (single-page app)
│   ├── archive.html                  # Briefing archive (dynamic, reads index.json)
│   ├── _headers                      # Cloudflare Pages headers
│   ├── _redirects                    # SPA fallback
│   ├── css/
│   │   ├── design-system.css         # Core design tokens and layout
│   │   ├── animations.css            # Transitions and keyframes
│   │   └── responsive.css            # Mobile/tablet breakpoints
│   ├── js/
│   │   ├── app.js                    # Boot sequence and navigation
│   │   ├── data.js                   # Data loader (fetches all 15 JSONs)
│   │   ├── map.js                    # Leaflet map + strike/carrier layers
│   │   ├── financial.js              # Oil, markets, Hormuz, cost charts
│   │   ├── humanitarian.js           # Casualties, infrastructure, comparison
│   │   ├── calculator.js             # Gas cost calculator
│   │   ├── timeline.js               # Conflict timeline
│   │   ├── briefing.js               # Daily briefing loader
│   │   └── utils.js                  # Shared utilities
│   ├── img/                          # SVG assets
│   └── data/                         # ALL DASHBOARD DATA
│       ├── hero-stats.json           # Hero panel metrics + history
│       ├── strikes-iran.json         # U.S./Israeli strike locations
│       ├── strikes-retaliation.json  # Iranian retaliation strikes
│       ├── carriers.json             # Naval force disposition
│       ├── timeline-events.json      # Conflict timeline
│       ├── baselines.json            # Pre-war financial baselines
│       ├── hormuz.json               # Strait of Hormuz incidents
│       ├── oil-prices.json           # Oil price time series
│       ├── markets.json              # S&P 500 + sector indices
│       ├── war-costs.json            # Daily war cost + tanker transits
│       ├── casualties.json           # Daily casualty breakdown
│       ├── infrastructure.json       # Infrastructure damage grid
│       ├── historical-comparison.json
│       ├── global-bases.json         # US military base locations
│       ├── calculator.json           # Gas calculator config
│       └── briefings/                # Daily briefing archive
│           ├── index.json            # Briefing index (archive reads this)
│           ├── day-1.html            # Day 1 briefing (HTML fragment)
│           ├── day-2.html            # ...
│           └── day-N.html            # Latest briefing
│
├── ops/                              # Operational protocol
│   ├── protocol.md                   # Full daily update protocol
│   ├── daily-checklist.md            # QA checklist for manifest review
│   └── prompts/
│       ├── phase1-deep-research.md   # Claude Deep Research template
│       └── phase2-code-execution.md  # Claude Code agent template
│
├── scripts/
│   ├── validate-data.sh              # Validate all 15 JSON data files
│   └── war-day.sh                    # Calculate current war day number
│
├── updates/                          # Historical update tracking
│   ├── manifests/                    # Archived update manifests
│   └── YYYY-MM-DD*/                  # Per-day update logs and corrections
│
├── CLAUDE.md                         # Agent context (auto-read by Claude Code)
└── README.md
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| **Hosting** | Cloudflare Pages (static, auto-deploys on push to `main`) |
| **Maps** | Leaflet.js with OpenStreetMap tiles |
| **Charts** | Chart.js 4.x |
| **Fonts** | Barlow Condensed, JetBrains Mono, IBM Plex Sans |
| **AI** | Claude (Anthropic) — research, data enrichment, code execution |
| **Framework** | None. No build step. No npm. Just HTML, CSS, and vanilla JS. |

---

## Data Integrity

### What's verified by the human analyst

- Financial baselines cross-referenced against FRED, Yahoo Finance, ICE/NYMEX, AAA, Treasury FiscalData, COMEX
- Military events verified against CENTCOM press releases and USNI Fleet Tracker
- Casualty figures attributed to specific reporting bodies (never synthesized across incompatible sources)
- Geographic coordinates checked for plausibility

### What's AI-generated (and audited)

- Timeline event descriptions
- Strike coordinates and geolocation data
- Daily intelligence briefings
- Data enrichment and calculations
- The code itself

### Known limitations

- Financial data is snapshotted once daily, not live-streaming
- Strike data uses approximate coordinates
- Casualty figures rely on multiple conflicting sources with different methodologies
- AI-generated content may contain errors despite auditing
- The archive supports real-time feeds architecturally — that capability is not yet live

---

## Contributing

This is an open project. If you find an error, fix it. If you have better data, submit it.

```bash
# Clone
git clone https://github.com/jethomasphd/WarTheater.git

# It's static HTML — just open it
open public/index.html

# Or serve locally
npx serve public
```

**Want to add data?** The data files in `public/data/` are the only files that matter for content updates. Read the schemas by looking at existing entries, match the format, submit a PR.

**Want to improve the dashboard?** The JS and CSS are in `public/js/` and `public/css/`. No build step — edit and reload.

---

## Contact

**Jacob E. Thomas, PhD**
JEThomasPhD@gmail.com

Questions, corrections, data submissions, bug reports — all welcome.

---

## License

Open source. Use it, fork it, build on it. Attribution appreciated but not required. The effort is what matters.
