# WarTheater — Claude Code Agent Context

## What This Is
IranWar.ai — a public OSINT intelligence dashboard tracking the 2026 U.S.-Iran conflict.
Live at https://iranwar.ai. Hosted on Cloudflare Pages (auto-deploys on push to `main`).

## Repository Structure
```
WarTheater/
├── public/              # Static site (Cloudflare Pages deploy root)
│   ├── index.html       # Main dashboard (single-page app)
│   ├── archive.html     # Briefing archive
│   ├── css/             # design-system.css, animations.css, responsive.css
│   ├── js/              # app.js, map.js, financial.js, timeline.js, etc.
│   ├── data/            # THE DATA FILES (your primary target)
│   │   ├── strikes-iran.json
│   │   ├── strikes-retaliation.json
│   │   ├── carriers.json
│   │   ├── timeline-events.json
│   │   ├── baselines.json
│   │   ├── hormuz.json
│   │   └── briefings/   # Daily HTML briefings + index.json
│   └── img/             # SVG assets
├── ops/                 # Operational protocol and prompts
│   ├── protocol.md      # Full daily update protocol
│   ├── daily-checklist.md
│   └── prompts/
│       ├── phase1-deep-research.md   # Template for Claude Deep Research
│       └── phase2-code-execution.md  # Template for Claude Code (you)
├── scripts/             # Automation helpers
│   ├── prep-update.sh   # Prepare daily update (renders prompts, validates)
│   ├── validate-data.sh # Validate all JSON data files
│   ├── war-day.sh       # Calculate current war day number
│   └── archive-manifest.sh  # Archive a completed manifest
├── updates/             # Historical update tracking (ISO-dated)
│   ├── manifests/       # Archived update manifests
│   └── YYYY-MM-DD*/     # Per-day update logs and corrections
├── worker/              # Cloudflare Worker API (future live data feeds)
└── README.md
```

## Daily Update Workflow
1. **Prep**: Run `./scripts/prep-update.sh` — calculates war day, validates data, renders Phase 1 prompt
2. **Phase 1**: Operator pastes prompt into Claude Deep Research with the 5 JSON files → gets Update Manifest
3. **QA**: Operator reviews manifest against `ops/daily-checklist.md`
4. **Phase 2**: Operator pastes `ops/prompts/phase2-code-execution.md` + approved manifest into Claude Code
5. **Deploy**: Push to `main` triggers Cloudflare Pages auto-deploy
6. **Archive**: Run `./scripts/archive-manifest.sh <manifest.md>`

## Rules for Code Agents
- **NEVER modify HTML, CSS, or JS files** during data updates — data files only
- **NEVER fabricate data** — if something is unverified, flag it
- **Validate JSON** after every modification (`python3 -m json.tool`)
- **Preserve schema** — match field order and formatting of existing entries
- **Commit format**: `intel update: Day [N] — YYYY-MM-DD`
- Skip anything in the manifest's DISCREPANCIES section (Section 6)
- If an entry ID is not found, report as error — do not create a new entry

## Tech Stack
- Pure HTML/CSS/JS (no framework, no build step)
- Leaflet.js (maps), Chart.js 4.x (charts)
- Cloudflare Pages (static hosting)
- Data: static JSON files versioned in git

## War Day Calculation
Day 1 = February 28, 2026. Use `./scripts/war-day.sh` or: `(today - 2026-02-28) + 1`
