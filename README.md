# THE WAR THEATER

**Public Intelligence Dashboard — Tracking the 2026 Iran War**

Live at: [iranwar.pages.dev](https://iranwar.pages.dev)

---

## What This Is

A real-time, open-source intelligence dashboard tracking the financial and humanitarian impact of Operation Epic Fury (the 2026 US-Iran War). Five panels of curated data — military operations, financial markets, humanitarian cost, AI briefings, and a chronological record — designed to give the public the same quality of intelligence that was once reserved for presidents and generals.

Every data point is sourced. Every number has context. Every euphemism is stripped away.

## Architecture

Static single-page application. No framework. No backend required.

```
public/
├── index.html              # SPA shell — all 5 panels
├── css/
│   ├── design-system.css   # Full design system (military dark aesthetic)
│   ├── animations.css      # Keyframe animations
│   └── responsive.css      # Tablet/mobile breakpoints
├── js/
│   ├── utils.js            # Utilities, formatters, chart defaults
│   ├── data.js             # Data fetching layer (JSON fallback + API)
│   ├── map.js              # Leaflet map — strikes, naval assets, bases
│   ├── financial.js        # Chart.js — oil, markets, Hormuz, daily cost
│   ├── humanitarian.js     # Casualties, infrastructure, historical comparison
│   ├── timeline.js         # The Record — chronological event timeline
│   ├── calculator.js       # Consumer impact calculator (gas cost by state)
│   ├── briefing.js         # AI briefing panel controller
│   └── app.js              # Main controller, navigation, boot sequence
└── data/
    ├── strikes-iran.json       # 16 US/Israel strike sites in Iran
    ├── strikes-retaliation.json # 14 Iranian retaliation / Hezbollah sites
    ├── carriers.json           # 7 US naval assets with positions
    ├── hormuz.json             # Strait geometry, shipping, impact data
    ├── timeline-events.json    # 20 chronological events (Feb 28 – Mar 10)
    ├── baselines.json          # Pre-war economic baselines (Feb 27)
    └── financial.json          # Market data for charts
```

## The Five Panels

| Panel | Name | Content |
|-------|------|---------|
| I | **The Theater** | Interactive Leaflet map. Strike sites, naval assets, Hormuz chokepoint, global US bases. News ticker at bottom. |
| II | **The Cost** | Oil prices, market impact, Hormuz tanker traffic, daily military cost, consumer impact calculator. |
| III | **The Toll** | Casualties, displaced persons, infrastructure damage, historical conflict comparison. |
| IV | **The Briefing** | AI-generated daily intelligence briefing with situation summary, key developments, outlook. |
| V | **The Record** | Chronological timeline of every significant event, filterable by category. |

## Deployment

Hosted on **Cloudflare Pages** as a static site.

### Deploy from scratch:
1. Fork or clone this repo
2. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
3. Create new project → Connect to Git
4. Set build output directory: `public`
5. No build command needed (static files)
6. Deploy

### Custom domain:
In Cloudflare Pages → Custom Domains → Add your domain.

## Daily Update Procedure (Human-in-the-Loop with Claude Code)

This dashboard is updated daily by an AI agent (Claude Code) with human review. No backend API infrastructure required — all data lives in curated JSON files.

### How it works:

1. **Human initiates**: Open Claude Code in the WarTheater repo
2. **Provide context**: Tell Claude the latest developments — new strikes, market data, casualties, diplomatic events
3. **Claude updates**:
   - `data/timeline-events.json` — Add new events with date, time, title, description, category, source, data_point
   - `data/strikes-iran.json` — Add new strike sites or update active_days on existing ones
   - `data/strikes-retaliation.json` — Add new retaliation events
   - `data/carriers.json` — Update naval asset positions and status
   - `data/hormuz.json` — Update tanker transit numbers, insurance costs
   - `data/baselines.json` — Generally static (pre-war snapshot)
   - `data/financial.json` — Update market data series
   - `index.html` — Update hero metrics (Brent, WTI, gas, S&P, daily cost, total cost)
   - `index.html` — Update the briefing section with new AI-generated analysis
4. **Human reviews**: Check the diff, verify data accuracy, approve
5. **Push to deploy**: `git push` triggers automatic Cloudflare Pages rebuild (< 1 minute)

### Update checklist:
- [ ] New events added to `timeline-events.json`
- [ ] Strike data updated (new sites or new active_days)
- [ ] Naval positions updated if changed
- [ ] Hero metrics updated in `index.html`
- [ ] Briefing rewritten for current day
- [ ] Hormuz transit numbers updated
- [ ] Financial chart data extended
- [ ] Day counter incremented throughout
- [ ] All sources cited
- [ ] `git push` to deploy

### Data sourcing:
All data points should cite sources. Primary sources used:
- **Military**: DoD press briefings, CENTCOM, IDF, ACLED
- **Financial**: ICE Futures (Brent), NYMEX (WTI), AAA (gas), NYSE (markets), Bloomberg
- **Humanitarian**: UNHCR, OCHA, Iranian Red Crescent, Lebanese Health Ministry, AP, Reuters
- **Diplomatic**: UN, White House, Iranian state media (IRNA/PressTV)

## Design Philosophy

- **Every pixel of light is earned by data.** Nothing decorative. Nothing wasted.
- **Anti-authoritarian by design.** This is the intelligence briefing the powerful don't want you to have.
- **No euphemisms.** "Collateral damage" means dead civilians. We say so.
- **Museum quality.** Every tooltip, every color, every word has purpose and sourcing.
- **The Flood vs. The Theater.** Information overload is a weapon. This dashboard is the antidote — structured, sourced, clear.

## Tech Stack

- Vanilla JavaScript (no framework)
- [Leaflet.js](https://leafletjs.com/) — Interactive map with CartoDB dark tiles
- [Chart.js](https://www.chartjs.org/) — Financial and humanitarian visualizations
- Fonts: Barlow Condensed (headings), JetBrains Mono (data), IBM Plex Sans (body)
- Cloudflare Pages (hosting)

## Optional: Cloudflare Worker API

A Cloudflare Worker is included in `worker/` for live API enrichment (real-time oil prices, auto-briefing generation). It's optional — the dashboard works fully from static JSON files without it.

## License

Open source. Built as a public utility.

---

*"The first casualty of war is truth. The second is the public's right to know."*
