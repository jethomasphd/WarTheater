# IranWar.ai — Daily Intelligence Update Protocol

**Author:** Jacob E. Thomas, PhD
**Version:** 2.0
**Last updated:** 2026-03-20
**Status:** Operational

---

## Overview

This document formalizes the daily intelligence update workflow for [IranWar.ai](https://iranwar.ai), a free, open-source OSINT dashboard tracking the 2026 U.S.-Iran conflict (Operation Epic Fury).

The workflow has two phases:

1. **PHASE 1 — Deep Research** → Claude Deep Research ingests the current data state, conducts verified research, and produces a structured Update Manifest (`.md`)
2. **PHASE 2 — Code Execution** → Claude Code consumes the Update Manifest and updates the JSON data files, then commits and pushes

The Update Manifest is the contract between phases. It must be structured enough for a coding agent to execute without ambiguity, and sourced enough for the analyst to audit before execution.

---

## Data Architecture

### The 15 Data Files

All dashboard data lives in `public/data/`. The HTML/JS is presentation only.

| File | Contents | Update Frequency |
|------|----------|-----------------|
| `hero-stats.json` | Hero panel metrics — cost + toll counters, tooltips, labels, history | Daily |
| `strikes-iran.json` | U.S./Israeli strikes on Iranian territory | As events occur |
| `strikes-retaliation.json` | Iranian retaliation strikes on U.S. bases, Gulf states, Israel | As events occur |
| `carriers.json` | U.S. naval force disposition — CSGs, ARGs, surface combatants | Daily |
| `timeline-events.json` | Chronological event timeline | Daily |
| `baselines.json` | Pre-war financial baselines (Feb 27 snapshot) | Rarely (corrections only) |
| `hormuz.json` | Strait of Hormuz incidents and status | As events occur |
| `oil-prices.json` | Oil price time series (Brent, WTI) | Daily |
| `markets.json` | S&P 500 + sector indices, trading day contexts | Daily (trading days) |
| `war-costs.json` | Daily war cost estimates + tanker transit data | Daily |
| `casualties.json` | Daily casualty breakdown by nationality | Daily |
| `infrastructure.json` | Infrastructure damage grid (hospitals, schools, etc.) | As events occur |
| `historical-comparison.json` | Comparison with past conflicts | Weekly or as needed |
| `global-bases.json` | US military base locations for map | As events occur |
| `calculator.json` | Gas cost calculator config (prices, state premiums) | Daily |

### Files Updated Daily (Core Set)

These files change every update cycle:

1. `hero-stats.json` — all hero panel numbers, add history entry
2. `oil-prices.json` — append day's Brent/WTI prices
3. `markets.json` — append day's market data + context
4. `war-costs.json` — append day's cost + tanker transits
5. `casualties.json` — append day's casualty estimates
6. `timeline-events.json` — new events
7. `calculator.json` — update gas prices if changed

### Files Updated As-Needed

These change only when new events occur:

8. `strikes-iran.json` — new strike entries
9. `strikes-retaliation.json` — new retaliation entries
10. `carriers.json` — position/status updates
11. `hormuz.json` — new incidents
12. `infrastructure.json` — damage count updates
13. `global-bases.json` — new base markers
14. `historical-comparison.json` — revised comparisons
15. `baselines.json` — corrections only

### GitHub Repository

- **Repo:** `jethomasphd/WarTheater`
- **Data path:** `public/data/`
- **Deploy:** Cloudflare Pages (auto-deploys on push to `main`)

---

## PHASE 1 — Deep Research

### Pre-flight

1. Calculate war day: `(today - Feb 28, 2026) + 1`
2. Download today's snapshot from `snapshots/YYYY-MM-DD_DATABASE_SNAPSHOT.zip` (auto-generated at 3 AM CT by GitHub Action; can also be triggered manually from the Actions tab, or run `./scripts/snapshot-data.sh` locally)
3. Open Claude Deep Research (new conversation)
4. Upload the snapshot zip
5. Paste the Phase 1 prompt from `ops/prompts/phase1-deep-research.md` (fill in date and war day)

### What the Research Agent Produces

A structured Update Manifest (`.md`) containing:
- Metadata (data horizon per file, sources, confidence levels)
- New entries as complete JSON objects matching existing schemas
- Modifications to existing entries (identified by `id`)
- File-level metadata updates (e.g., `last_updated`, hero-stats snapshot)
- Discrepancies requiring human judgment
- Analyst notes on trends

### Post-Research QA

Review the manifest against `ops/daily-checklist.md`:
- Every JSON object has all required schema fields
- Coordinates are plausible (Iran: ~25-40°N, ~44-63°E)
- Source attributions are specific
- Naval positions cite USNI Fleet Tracker
- Casualty figures attribute to specific reporting bodies
- Discrepancies section is populated (zero = suspiciously clean)

---

## PHASE 2 — Code Execution

### Pre-flight

1. Review and approve the Update Manifest from Phase 1
2. Open Claude Code (connected to this repo)
3. Paste the Phase 2 prompt from `ops/prompts/phase2-code-execution.md`
4. Paste the approved Update Manifest

### What the Code Agent Does

1. Reads current state of all data files in `public/data/`
2. Parses the manifest section by section
3. Executes operations:
   - **NEW ENTRIES** → Appends to appropriate arrays
   - **MODIFICATIONS** → Locates by `id`, updates specified fields
   - **REMOVALS** → Removes by `id` (carriers only)
   - **GLOBAL UPDATES** → Updates metadata fields
   - **HERO-STATS** → Updates current snapshot + appends to history array
4. Validates all JSON after modification
5. Commits: `intel update: Day [N] — YYYY-MM-DD`
6. Pushes to `main`

### Briefing Archive

The archive page (`archive.html`) is fully dynamic — it reads from `data/briefings/index.json`
and lazy-loads individual briefing HTML files on demand. **No manual archive.html editing is needed.**

During Phase 2, the code agent:
1. Creates `public/data/briefings/day-[N].html` (HTML fragment matching previous briefings)
2. Appends an entry to `public/data/briefings/index.json`
3. Updates the hardcoded briefing panel in `index.html`

The archive page automatically picks up the new briefing from `index.json`.

### Post-Execution

- Review the agent's change summary
- Verify Cloudflare Pages deployment
- Spot-check live dashboard
- Verify archive page shows the new briefing at the top

---

## Source Hierarchy

When sources conflict, prefer in this order:

1. **Official statements** — CENTCOM press releases, DoD briefings, Pentagon spokesman
2. **Wire services** — Reuters, AP, AFP
3. **Defense media** — USNI News Fleet Tracker, The War Zone, Defense One, Breaking Defense
4. **Quality broadsheets** — NYT, WSJ, BBC, Al Jazeera
5. **Regional media** — Stars and Stripes, Navy Times, Times of Israel, Tehran Times
6. **Tracking bodies** — ACLED, HRANA/Hengaw (Iranian casualties), WHO
7. **OSINT community** — Verified accounts on X, r/CredibleDefense, Oryx-style trackers
8. **Wikipedia** — Good for event aggregation, unreliable for breaking details

---

## Data Sources by Domain

- **Financial**: FRED, Yahoo Finance, Bloomberg, ICE, NYMEX, AAA, GasBuddy
- **Military/Conflict**: ACLED, CENTCOM, DoD press releases, USNI Fleet Tracker
- **Humanitarian**: UNHCR, OCHA, ICRC, Iranian Red Crescent
- **News Wire**: Reuters, AP, Al Jazeera, Times of Israel

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-19 | Initial formalization of daily update workflow |
| 2.0 | 2026-03-20 | Expanded to cover all 15 data files; removed legacy 5-file references; aligned with data-driven architecture |
