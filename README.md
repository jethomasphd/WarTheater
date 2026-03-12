# THE WAR THEATER

**A Public Intelligence Dashboard for the 2026 Iran War**

Live at [iranwar.ai](https://iranwar.ai)

---

## What This Is

A situation room for the public. Every bomb has a price tag. Every missile has a human cost. Every day the Strait of Hormuz stays closed, a gas station in Texas charges more per gallon. This dashboard makes those connections visible.

The model is the [Johns Hopkins COVID-19 Dashboard](https://coronavirus.jhu.edu/) — a single authoritative reference point for a global crisis. It didn't editorialize. It presented the numbers and let the weight of the data speak. We're building that, but for war.

---

## How It Works Today

**This dashboard is currently powered by AI-agent web crawling, not live API feeds.**

A Claude Code agent scrapes, cross-references, and curates data from public sources each morning. The creator audits the output, applies domain-informed guardrails, and publishes updates. This is a manual-with-AI-assistance workflow — not an automated pipeline.

Data is sourced from:
- **Financial**: FRED, Yahoo Finance, Bloomberg, ICE, NYMEX, AAA, GasBuddy
- **Military/Conflict**: ACLED, CENTCOM, DoD press releases
- **Humanitarian**: UNHCR, OCHA, ICRC, Iranian Red Crescent
- **News Wire**: Reuters, AP, Al Jazeera, Times of Israel

Updates are published **once daily**, typically mornings US Eastern. The data you see may lag current events by hours.

### Future: Live API Integration

The architecture includes a Cloudflare Worker (`/worker`) designed to serve live data from financial and conflict APIs:

| API | Purpose | Status |
|-----|---------|--------|
| FRED (Federal Reserve) | Treasury yields, fed funds rate, economic indicators | Planned |
| Yahoo Finance / Alpha Vantage | S&P 500, sector stocks, VIX, DXY | Planned |
| ACLED | Conflict event data, strike counts | Planned |
| EIA | Oil prices, petroleum supply data | Planned |
| Anthropic Claude API | Daily AI-generated intelligence briefings | Scaffolded |

The worker routes exist (`/api/markets`, `/api/oil`, `/api/timeline`, etc.) and the caching layer is built. API keys are referenced but not yet connected to live data. This is a known limitation, not a bug.

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
├── public/                    # Static site (Cloudflare Pages)
│   ├── index.html             # Main dashboard
│   ├── archive.html           # Briefing archive
│   ├── css/
│   │   ├── design-system.css  # Core design system
│   │   ├── animations.css     # Transitions and effects
│   │   └── responsive.css     # Mobile breakpoints
│   ├── js/
│   │   ├── app.js             # Boot, intro, disclaimer gate
│   │   ├── data.js            # Data loading and fallbacks
│   │   ├── map.js             # Leaflet theater map
│   │   ├── financial.js       # Chart.js financial panels
│   │   ├── timeline.js        # Conflict timeline
│   │   ├── humanitarian.js    # Casualty and displacement
│   │   ├── briefing.js        # AI briefing display
│   │   ├── calculator.js      # Cost calculator
│   │   └── utils.js           # Shared utilities
│   └── data/                  # Static JSON datasets
│       ├── baselines.json     # Pre-war financial baselines
│       ├── timeline-events.json
│       ├── strikes-iran.json
│       ├── strikes-retaliation.json
│       ├── carriers.json
│       ├── hormuz.json
│       └── briefings/         # Daily HTML briefings
│
├── worker/                    # Cloudflare Worker API (future)
│   ├── src/
│   │   ├── index.js           # Router
│   │   ├── routes/            # API route handlers
│   │   └── lib/               # Cache, CORS, Claude integration
│   └── wrangler.toml          # Worker configuration
│
├── seed.md                    # Original project brief
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
