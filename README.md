# THE WAR THEATER

**A Public Intelligence Dashboard for the 2026 Iran War**

Live at [iranwar.ai](https://iranwar.ai)

---

## What This Is

A situation room for the public. Every bomb has a price tag. Every missile has a human cost. Every day the Strait of Hormuz stays closed, a gas station in Texas charges more per gallon. This dashboard makes those connections visible.

The model is the [Johns Hopkins COVID-19 Dashboard](https://coronavirus.jhu.edu/) — a single authoritative reference point for a global crisis. It didn't editorialize. It presented the numbers and let the weight of the data speak. We're building that, but for war.

---

## How It Works

**Two-phase AI-assisted update cycle, once daily.**

```
┌─────────────────────────────────────────────────────────┐
│  PHASE 1 — Deep Research                                │
│                                                         │
│  1. Export the current data JSONs from public/data/     │
│  2. Upload them to Claude Deep Research along with      │
│     ops/prompts/phase1-deep-research.md                 │
│  3. Claude researches overnight events and produces     │
│     a structured Update Manifest (.md)                  │
│  4. QA review the manifest (ops/daily-checklist.md)     │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  PHASE 2 — Code Execution                               │
│                                                         │
│  1. Open Claude Code (connected to this repo)           │
│  2. Paste ops/prompts/phase2-code-execution.md          │
│     + the approved Update Manifest                      │
│  3. Claude Code updates the JSON data files             │
│  4. Review, commit, push → Cloudflare auto-deploys      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

The dashboard reads ALL data from 15 JSON files in `public/data/`. No data lives in HTML or JS — code is presentation only. See `ops/protocol.md` for the full operational protocol.

**Data sources:**
- **Financial**: FRED, Yahoo Finance, Bloomberg, ICE, NYMEX, AAA, GasBuddy
- **Military/Conflict**: ACLED, CENTCOM, DoD press releases, USNI Fleet Tracker
- **Humanitarian**: UNHCR, OCHA, ICRC, Iranian Red Crescent
- **News Wire**: Reuters, AP, Al Jazeera, Times of Israel

Updates are published **once daily**, typically mornings US Eastern.

---

## Disclaimer

**Read this before using the data.**

Much of this project was built and maintained with AI agents (Claude). These models hallucinate dates, fabricate figures, and miscalculate with total confidence. The creator audits aggressively but makes no guarantees of accuracy.

In a kinetic conflict, accurate information is nearly impossible to obtain. Sources contradict. Governments lie. Propaganda is pervasive on every side. This project sources data with fidelity where possible, but the flood is real and no filter is perfect.

**Do not rely on this data for financial, military, or life-safety decisions.**

This project is built in good faith. Fork it. Audit it. Improve it.

---

## Architecture

```
WarTheater/
├── public/                    # Static site (Cloudflare Pages deploy root)
│   ├── index.html             # Main dashboard
│   ├── archive.html           # Briefing archive
│   ├── _headers               # Cloudflare Pages headers
│   ├── _redirects              # SPA fallback
│   ├── css/
│   │   ├── design-system.css  # Core design tokens and layout
│   │   ├── animations.css     # Transitions and keyframes
│   │   └── responsive.css     # Mobile/tablet breakpoints
│   ├── js/
│   │   ├── app.js             # Boot sequence and navigation
│   │   ├── data.js            # Data loader (fetches all 15 JSONs)
│   │   ├── map.js             # Leaflet map + strike/carrier layers
│   │   ├── financial.js       # Oil, markets, Hormuz, cost charts
│   │   ├── humanitarian.js    # Casualties, infrastructure, comparison
│   │   ├── calculator.js      # Gas cost calculator
│   │   ├── timeline.js        # Conflict timeline
│   │   ├── briefing.js        # Daily briefing loader
│   │   └── utils.js           # Shared utilities
│   ├── img/
│   │   ├── us-flag.svg
│   │   └── iran-flag.svg
│   └── data/                  # ALL dashboard data (update target)
│       ├── hero-stats.json          # Hero panel metrics + history
│       ├── strikes-iran.json        # U.S./Israeli strike locations
│       ├── strikes-retaliation.json # Iranian retaliation strikes
│       ├── carriers.json            # Naval force disposition
│       ├── timeline-events.json     # Conflict timeline
│       ├── baselines.json           # Pre-war financial baselines
│       ├── hormuz.json              # Strait of Hormuz incidents
│       ├── oil-prices.json          # Oil price time series
│       ├── markets.json             # S&P 500 + sector indices
│       ├── war-costs.json           # Daily war cost + tanker transits
│       ├── casualties.json          # Daily casualty breakdown
│       ├── infrastructure.json      # Infrastructure damage grid
│       ├── historical-comparison.json
│       ├── global-bases.json        # US military base locations
│       ├── calculator.json          # Gas calculator config
│       └── briefings/               # Daily HTML briefings + index.json
│
├── ops/                       # Operational protocol
│   ├── protocol.md            # Full daily update protocol
│   ├── daily-checklist.md     # QA checklist for manifest review
│   └── prompts/
│       ├── phase1-deep-research.md   # Claude Deep Research template
│       └── phase2-code-execution.md  # Claude Code agent template
│
├── scripts/
│   ├── validate-data.sh       # Validate all 15 JSON data files
│   └── war-day.sh             # Calculate current war day number
│
├── updates/                   # Historical update tracking
│   ├── manifests/             # Archived update manifests
│   └── YYYY-MM-DD*/           # Per-day update logs and corrections
│
├── CLAUDE.md                  # Agent context (auto-read by Claude Code)
└── README.md
```

### Tech Stack

- **Hosting**: Cloudflare Pages (static)
- **Maps**: Leaflet.js with OpenStreetMap
- **Charts**: Chart.js 4.x
- **Fonts**: Barlow Condensed, JetBrains Mono, IBM Plex Sans
- **AI**: Claude (Anthropic) for research, data enrichment, and code execution
- **No framework**. No build step. No npm. Just HTML, CSS, and vanilla JS.

---

## Data Integrity

### What's Verified

Financial baselines in `baselines.json` are cross-referenced against:
- FRED DGS10 (10-year Treasury yield)
- Federal Reserve H.15 (fed funds rate)
- Yahoo Finance (S&P 500, VIX, DXY)
- ICE / NYMEX (Brent, WTI closing prices)
- Treasury FiscalData (national debt)
- COMEX (gold, silver)
- AAA (gas prices)

### What's AI-Generated

- Timeline event descriptions (audited by creator)
- Strike coordinates and geolocation data
- Daily intelligence briefings
- Some data enrichment and calculations

### Known Limitations

- Financial data is snapshotted, not live-streaming
- Strike data uses approximate coordinates
- Casualty figures rely on multiple conflicting sources
- AI-generated content may contain errors despite auditing

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

---

## Contact

**Jacob E. Thomas, PhD**
JEThomasPhD@gmail.com

Questions, corrections, data submissions, bug reports — all welcome.

---

## License

Open source. Use it, fork it, build on it. Attribution appreciated but not required. The effort is what matters.
