# WarTheater — Claude Code Agent Context

## What This Is
IranWar.ai — a public OSINT intelligence dashboard tracking the 2026 U.S.-Iran conflict.
Live at https://iranwar.ai. Hosted on Cloudflare Pages (auto-deploys on push to `main`).

## Repository Structure
```
WarTheater/
├── public/              # Static site (Cloudflare Pages deploy root)
│   ├── index.html       # Main dashboard (single-page app)
│   ├── archive.html     # Briefing archive (dynamic, reads index.json)
│   ├── css/             # design-system.css, animations.css, responsive.css
│   ├── js/              # app.js, map.js, financial.js, timeline.js, etc.
│   ├── data/            # ALL DASHBOARD DATA (your primary target)
│   │   ├── hero-stats.json          # Hero panel metrics (daily snapshot)
│   │   ├── strikes-iran.json        # U.S./Israeli strike locations
│   │   ├── strikes-retaliation.json # Iranian retaliation strikes
│   │   ├── carriers.json            # Naval force disposition
│   │   ├── timeline-events.json     # Conflict timeline
│   │   ├── baselines.json           # Pre-war financial baselines
│   │   ├── hormuz.json              # Strait of Hormuz incidents
│   │   ├── oil-prices.json          # Oil price time series (charts)
│   │   ├── markets.json             # S&P 500 series + contexts (charts)
│   │   ├── war-costs.json           # Daily war cost + tanker transits
│   │   ├── casualties.json          # Daily casualty breakdown (charts)
│   │   ├── infrastructure.json      # Infrastructure damage grid
│   │   ├── historical-comparison.json
│   │   ├── global-bases.json        # US military base locations (map)
│   │   ├── calculator.json          # Gas cost calculator config
│   │   └── briefings/               # Daily briefing archive
│   │       ├── index.json           # Briefing index (archive.html reads this)
│   │       ├── day-1.html           # Day 1 briefing (HTML fragment)
│   │       ├── day-2.html           # ...
│   │       └── day-N.html           # Latest briefing
│   └── img/             # SVG assets
├── ops/                 # Operational protocol and prompts
│   ├── protocol.md      # Full daily update protocol
│   ├── daily-checklist.md
│   └── prompts/
│       ├── phase1-deep-research.md   # Template for Claude Deep Research
│       └── phase2-code-execution.md  # Template for Claude Code (you)
├── scripts/             # Helpers
│   ├── validate-data.sh # Validate all JSON data files
│   └── war-day.sh       # Calculate current war day number
├── updates/             # Historical update tracking (ISO-dated)
│   ├── manifests/       # Archived update manifests
│   └── YYYY-MM-DD*/     # Per-day update logs and corrections
├── CLAUDE.md            # Agent context (this file)
└── README.md
```

## Architecture: Data-Driven Dashboard
ALL dashboard data lives in JSON files under `public/data/`. The HTML and JS are
presentation only — they read from JSON and render. During daily updates, you modify
JSON files only. The JS/HTML should never need to change for data updates.

**Key data files updated daily:**
- `hero-stats.json` — all hero panel numbers (costs, toll counters, tooltips)
- `oil-prices.json` — append new day's oil prices
- `markets.json` — append new day's market data + context
- `war-costs.json` — append new day's cost + tanker transits
- `casualties.json` — append new day's casualty estimates
- `strikes-iran.json` / `strikes-retaliation.json` — new strike entries
- `carriers.json` — position/status updates
- `timeline-events.json` — new timeline events
- `infrastructure.json` — update damage counts
- `calculator.json` — update gas prices if changed

## Daily Update Workflow
1. **Phase 1**: Operator uploads data JSONs + `ops/prompts/phase1-deep-research.md` to Claude Deep Research → gets Update Manifest
2. **QA**: Operator reviews manifest against `ops/daily-checklist.md`
3. **Phase 2**: Operator pastes `ops/prompts/phase2-code-execution.md` + approved manifest into Claude Code
4. **Deploy**: Push to `main` triggers Cloudflare Pages auto-deploy

## Rules for Code Agents
- **NEVER modify HTML, CSS, or JS files** during data updates — data files only
- **NEVER fabricate data** — if something is unverified, flag it
- **Validate JSON** after every modification (`python3 -m json.tool`)
- **Preserve schema** — match field order and formatting of existing entries
- **Commit format**: `intel update: Day [N] — YYYY-MM-DD`
- Skip anything in the manifest's DISCREPANCIES section (Section 9)
- If an entry ID is not found, report as error — do not create a new entry

## Briefing Archive Architecture

The archive page (`public/archive.html`) dynamically loads briefings — no hardcoded HTML.

**How it works:**
1. `archive.html` fetches `data/briefings/index.json` on page load
2. Sorts entries by `day` descending (most recent first)
3. Renders each briefing as a collapsible card (day label + headline)
4. The latest briefing auto-expands and lazy-loads its HTML
5. Other briefings lazy-load their HTML on first expand (click)

**Daily update workflow for briefings:**
1. Create `public/data/briefings/day-[N].html` — the briefing content (HTML fragment, not a full page)
2. Append an entry to `public/data/briefings/index.json` with day, date, label, headline, and file path
3. Update the hardcoded briefing panel in `index.html` (the ONE exception to "never modify HTML")
4. That's it — `archive.html` picks up the new briefing automatically from `index.json`

**Briefing HTML files** are HTML fragments (not full pages). They use the dashboard's CSS classes:
- `briefing-header`, `briefing-date` — title block
- `briefing-section` with `<h3>` — each analytical section
- Standard `<ul><li>` for bullet lists

**index.json schema:**
```json
{
  "day": 21,
  "date": "2026-03-20",
  "label": "MARCH 20, 2026 — DAY 21",
  "headline": "Short headline summarizing the day's key developments",
  "file": "data/briefings/day-21.html"
}
```

## Tech Stack
- Pure HTML/CSS/JS (no framework, no build step)
- Leaflet.js (maps), Chart.js 4.x (charts)
- Cloudflare Pages (static hosting)
- Data: static JSON files versioned in git

## War Day Calculation
Day 1 = February 28, 2026. Use `./scripts/war-day.sh` or: `(today - 2026-02-28) + 1`
