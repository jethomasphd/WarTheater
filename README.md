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

The dashboard reads ALL data from JSON files in `public/data/`. No data lives in HTML or JS — code is presentation only. See `ops/protocol.md` for the full operational protocol.

**Data sources:**
- **Financial**: FRED, Yahoo Finance, Bloomberg, ICE, NYMEX, AAA, GasBuddy
- **Military/Conflict**: ACLED, CENTCOM, DoD press releases
- **Humanitarian**: UNHCR, OCHA, ICRC, Iranian Red Crescent
- **News Wire**: Reuters, AP, Al Jazeera, Times of Israel

Updates are published **once daily**, typically mornings US Eastern.

### Future: Live API Integration

The architecture includes a Cloudflare Worker (`/worker`) designed to serve live data from financial and conflict APIs. The worker routes exist (`/api/markets`, `/api/oil`, `/api/timeline`, etc.) and the caching layer is built. API keys are referenced but not yet connected. This is a known limitation, not a bug.

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
│   ├── css/                   # design-system, animations, responsive
│   ├── js/                    # app, map, financial, timeline, etc.
│   ├── img/                   # SVG assets
│   └── data/                  # ALL dashboard data (agent update target)
│       ├── hero-stats.json          # Hero panel metrics (daily snapshot)
│       ├── strikes-iran.json        # U.S./Israeli strike locations
│       ├── strikes-retaliation.json # Iranian retaliation strikes
│       ├── carriers.json            # Naval force disposition
│       ├── timeline-events.json     # Conflict timeline
│       ├── baselines.json           # Pre-war financial baselines
│       ├── hormuz.json              # Strait of Hormuz incidents
│       ├── oil-prices.json          # Oil price time series
│       ├── markets.json             # S&P 500 series + contexts
│       ├── war-costs.json           # Daily war cost + notes
│       ├── casualties.json          # Daily casualty breakdown
│       ├── infrastructure.json      # Infrastructure damage
│       ├── historical-comparison.json
│       ├── global-bases.json        # US military base locations
│       ├── calculator.json          # Gas cost calculator config
│       └── briefings/               # Daily HTML briefings + index.json
│
├── ops/                       # Operational protocol
│   ├── protocol.md            # Full daily update protocol
│   ├── daily-checklist.md     # QA checklist for manifest review
│   └── prompts/
│       ├── phase1-deep-research.md   # Claude Deep Research template
│       └── phase2-code-execution.md  # Claude Code agent template
│
├── scripts/                   # Helpers
│   ├── validate-data.sh       # Validate all JSON data files
│   └── war-day.sh             # Calculate current war day
│
├── updates/                   # Historical update tracking
│   ├── manifests/             # Archived update manifests
│   └── YYYY-MM-DD*/           # Per-day logs and corrections
│
├── worker/                    # Cloudflare Worker API (future)
│   ├── src/
│   │   ├── index.js           # Router
│   │   ├── routes/            # API route handlers
│   │   └── lib/               # Cache, CORS, Claude integration
│   └── wrangler.toml          # Worker configuration
│
├── CLAUDE.md                  # Agent context for Claude Code sessions
└── README.md
```

### Tech Stack

- **Hosting**: Cloudflare Pages (static) + Cloudflare Workers (API, future)
- **Maps**: Leaflet.js with OpenStreetMap
- **Charts**: Chart.js 4.x
- **Fonts**: Barlow Condensed, JetBrains Mono, IBM Plex Sans
- **AI**: Claude (Anthropic) for data enrichment, briefing generation, and build assistance
- **No framework**. No build step. No npm for the frontend. Just HTML, CSS, and vanilla JS.

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
