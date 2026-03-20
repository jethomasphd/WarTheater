# IranWar.ai — Daily Intelligence Update Protocol

**Author:** Jacob E. Thomas, PhD  
**Version:** 1.0  
**Last updated:** 2026-03-19  
**Status:** Operational

---

## Overview

This document formalizes the daily intelligence update workflow for [IranWar.ai](https://iranwar.ai), a free, open-source intelligence dashboard tracking the 2026 U.S.-Iran conflict (Operation Epic Fury).

The workflow has two phases:

1. **PHASE 1 — Deep Research** → Claude Deep Research ingests the current data state, conducts verified research, and produces a structured update manifest (`.md`)
2. **PHASE 2 — Code Execution** → Claude Code (or equivalent coding agent) consumes the update manifest and implements changes against the live data files, then pushes to the GitHub repo

The update manifest is the contract between phases. It must be structured enough for a coding agent to execute without ambiguity, and sourced enough for the analyst (you) to audit before execution.

---

## Data Architecture

### The 5 JSON Files

| File | Contents | Schema Notes |
|------|----------|--------------|
| `strikes-iran.json` | U.S./Israeli strikes on Iranian territory | `id`, `city`, `lat`/`lng`, `type`, `weapon`, `actor`, `first_strike`, `casualties_reported`, `casualties_source`, `active_days`, `notes` |
| `strikes-retaliation.json` | Iranian retaliation strikes on U.S. bases, Gulf states, Israel | Same schema as strikes-iran but `origin: "Iran"` and includes proxy strikes |
| `carriers.json` | U.S. naval force disposition — carrier strike groups, ARGs, independent surface combatants | `name`, `hull_number`, `type`, `location`, `lat`/`lng`, `status`, `escorts[]`, `mission`, `last_verified`, `source` |
| `timeline-events.json` | Chronological event timeline of the conflict | `id`, `date`, `war_day`, `title`, `description`, `category`, `sources[]` |
| `financial-metrics.json` | Economic/market impact data — oil prices, shipping costs, defense spending, humanitarian costs | `metric`, `date`, `value`, `baseline_value`, `pct_change`, `source` |

### GitHub Repository

- **Repo:** `jethomasphd/WarTheater` (or current repo name)
- **Data path:** `public/data/`
- **Deploy:** Cloudflare Pages (auto-deploys on push to `main`)

---

## PHASE 1 — Deep Research Prompt Protocol

### Pre-flight

1. Pull the 5 JSON files from the GitHub repo (`public/data/`)
2. Open Claude Deep Research
3. Upload all 5 files
4. Paste the prompt below

### The Prompt

```
SYSTEM CONTEXT
==============
You are the intelligence analyst for IranWar.ai — a free, open-source OSINT
dashboard tracking the 2026 U.S.-Iran conflict (Operation Epic Fury).

Today is [DATE]. The war began February 28, 2026 (Day 1). Today is Day [N].

I am providing you with the current state of my 5 data files. Your mission:
1. Identify the most recent entry/date in each file
2. Rigorously research everything that has happened SINCE that date
3. Cross-verify across multiple high-quality sources
4. Produce a single structured UPDATE MANIFEST that a coding agent can
   execute against the live data files

OPERATIONAL RULES
=================
- NEVER fabricate intelligence. If unverifiable, flag it as UNVERIFIED.
- Cite sources for every claim. Prefer: CENTCOM statements, USNI Fleet Tracker,
  Reuters, AP, BBC, Al Jazeera live blogs, The War Zone, Defense One,
  Breaking Defense, Stars and Stripes, Navy Times, ACLED.
- When sources conflict, note the discrepancy — do not silently pick one.
- For naval positions: USNI Fleet Tracker is the gold standard. Satellite
  imagery (Planet Labs, Maxar via journalists) is secondary. Social media
  geolocations are tertiary.
- For casualty figures: Always attribute to the reporting body (Iranian Health
  Ministry, CENTCOM, ACLED, Hengaw, etc.). Never synthesize a single number
  from incompatible sources.
- For strikes: Cross-reference Wikipedia's running article, Al Jazeera's
  live tracker, and ACLED event data where available.

RESEARCH DOMAINS
================
For each domain, identify what has changed since the last update in the data:

1. STRIKES ON IRAN (strikes-iran.json)
   - New strike targets (cities, facilities, infrastructure)
   - Updated casualty figures for existing targets
   - New weapons systems employed
   - New actors (e.g., if UK or other allies join strikes)
   - Changes to existing entries (corrections, updated coordinates)

2. IRANIAN RETALIATION (strikes-retaliation.json)
   - New IRGC strikes on U.S. bases, Gulf states, Israel
   - Proxy actions: Houthi, Hezbollah, Iraqi militia strikes
   - Strait of Hormuz incidents (mines, fast boat encounters, shipping attacks)
   - Changes to existing entries

3. NAVAL FORCE DISPOSITION (carriers.json)
   - Carrier strike group repositioning
   - New deployments or withdrawals
   - Escort composition changes (verify against USNI Fleet Tracker)
   - Ship incidents (fires, collisions, casualties)
   - Convoy escort status through Strait of Hormuz

4. TIMELINE EVENTS (timeline-events.json)
   - Major political/diplomatic developments
   - Significant military escalations or de-escalations
   - Humanitarian milestones (refugee numbers, aid access)
   - Economic milestones (oil price records, sanctions changes)
   - Congressional/legal actions related to the war

5. FINANCIAL METRICS (financial-metrics.json)
   - Oil prices (Brent, WTI) — current vs. pre-war baseline (Feb 27)
   - Shipping/insurance costs through Strait of Hormuz
   - U.S. war spending (cumulative DoD cost estimates)
   - Market indicators (defense stocks, volatility)
   - Humanitarian cost estimates

OUTPUT FORMAT — THE UPDATE MANIFEST
====================================
Produce a single markdown document with the following structure.
This document will be consumed by a coding agent — precision matters.

# IranWar.ai Update Manifest
## Date: [DATE] | War Day: [N]
## Coverage: Events since [LAST_UPDATE_DATE]

### METADATA
- Last update found in data: [date per file]
- Sources consulted: [list]
- Research confidence: [HIGH/MEDIUM/LOW per domain]

---

### 1. STRIKES-IRAN UPDATES

#### 1a. NEW ENTRIES
For each new strike target, provide a COMPLETE JSON object matching the schema:

```json
{
  "id": "city-name-lowercase",
  "city": "City Name, Province",
  "lat": 00.0000,
  "lng": 00.0000,
  "type": "us_strike" | "israeli_strike" | "joint_strike",
  "weapon": "Tomahawk / JDAM / GBU-39 / etc.",
  "actor": "US" | "Israel" | "US/Israel",
  "first_strike": "2026-MM-DD",
  "casualties_reported": "X killed, Y injured (source)",
  "casualties_source": "Source Name",
  "active_days": [1, 2, 3],
  "notes": "Contextual notes with sourcing."
}
```

#### 1b. MODIFICATIONS TO EXISTING ENTRIES
For each correction or update to an existing entry:

```
ENTRY ID: [id]
FIELD: [field_name]
OLD VALUE: [current value]
NEW VALUE: [corrected value]
REASON: [why, with source]
```

#### 1c. GLOBAL UPDATES
Any file-level metadata changes (e.g., `last_updated`, `total_casualties` summary fields).

---

### 2. STRIKES-RETALIATION UPDATES
[Same structure as Section 1]

---

### 3. CARRIERS UPDATES

#### 3a. POSITION/STATUS CHANGES
For each ship with updated information:

```
SHIP: [name] ([hull_number])
FIELD: location
OLD VALUE: [current]
NEW VALUE: [updated]
SOURCE: [USNI Fleet Tracker / CENTCOM / etc.]
VERIFIED: [date]
```

#### 3b. NEW ASSETS
Complete JSON objects for any newly deployed ships.

#### 3c. ESCORT COMPOSITION CHANGES
List verified escort changes per CSG.

#### 3d. REMOVALS
Any ships that have left theater or been decommissioned.

---

### 4. TIMELINE-EVENTS UPDATES

#### 4a. NEW EVENTS
For each new event, provide a COMPLETE JSON object:

```json
{
  "id": "YYYY-MM-DD-short-slug",
  "date": "2026-MM-DD",
  "war_day": N,
  "title": "Short descriptive title",
  "description": "2-3 sentence description with key facts.",
  "category": "military" | "diplomatic" | "humanitarian" | "economic" | "political",
  "sources": ["Source 1", "Source 2"]
}
```

---

### 5. FINANCIAL-METRICS UPDATES

#### 5a. UPDATED VALUES
For each metric with new data:

```
METRIC: [metric_name]
DATE: [date]
VALUE: [new value]
SOURCE: [source]
```

---

### 6. DISCREPANCIES & UNVERIFIED INTELLIGENCE
Items that require human judgment before inclusion:
- [item + context + competing sources]

### 7. ANALYST NOTES
Patterns, emerging trends, or structural observations that don't
fit neatly into the data files but inform the next update cycle.
```

### Post-Research QA Checklist

Before accepting the Deep Research output:
- [ ] Every new JSON object has all required schema fields
- [ ] Coordinates are plausible (not 0,0 or obviously wrong hemisphere)
- [ ] `active_days` arrays are consistent with `first_strike` dates
- [ ] Source attributions are specific (not "various reports")
- [ ] Naval positions cite USNI Fleet Tracker or equivalent
- [ ] Casualty figures attribute to a specific reporting body
- [ ] No fabricated ship names, hull numbers, or military units
- [ ] Discrepancies section is populated (zero discrepancies = suspiciously clean)

---

## PHASE 2 — Code Execution Prompt

### Pre-flight

1. Review and approve the update manifest from Phase 1
2. Open Claude Code (or equivalent coding agent with repo access)
3. Ensure the agent has access to the IranWar.ai GitHub repo
4. Provide the approved manifest

### The Prompt

```
CONTEXT
=======
You are a coding agent maintaining the IranWar.ai dashboard — a live OSINT
intelligence tracker for the 2026 U.S.-Iran conflict.

The repository is a Cloudflare Pages site. The data lives in `public/data/`.
The site auto-deploys when changes are pushed to `main`.

I am providing you with an UPDATE MANIFEST — a structured intelligence
document produced by a research agent. This manifest has been reviewed and
approved by the human analyst.

YOUR MISSION
============
1. Read the current state of all 5 JSON files in `public/data/`
2. Parse the update manifest section by section
3. For each section:
   a. NEW ENTRIES → Append to the appropriate array, maintaining sort order
   b. MODIFICATIONS → Locate the entry by `id`, update the specified fields
   c. REMOVALS → Remove the entry by `id` (carriers only)
   d. GLOBAL UPDATES → Update file-level metadata fields
4. Validate all JSON after modification (no trailing commas, valid structure)
5. Update `last_updated` field in each modified file to today's date
6. Commit with message: "intel update: Day [N] — [DATE]"
7. Push to `main`

EXECUTION RULES
===============
- NEVER modify the website code (HTML, CSS, JS). Data files only.
- Preserve existing entry order unless the manifest specifies reordering.
- If the manifest contains a DISCREPANCIES section, SKIP those items —
  they require human resolution.
- If a new entry's `id` already exists, treat it as a MODIFICATION,
  not a duplicate insertion.
- For carriers.json: If a ship's `last_verified` date in the manifest
  is OLDER than what's in the file, keep the file's version.
- After all modifications, run a JSON lint pass on every changed file.
- Report a summary of changes made:
  - X new entries added to strikes-iran.json
  - Y entries modified in strikes-retaliation.json
  - Z position updates in carriers.json
  - etc.

PROVIDE the update manifest below:
---
[PASTE MANIFEST HERE]
```

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────┐
│                  DAILY CYCLE                     │
│                                                  │
│  06:00  Pull 5 JSONs from GitHub                 │
│         ↓                                        │
│  06:05  Upload to Claude Deep Research           │
│         + Phase 1 Prompt                         │
│         ↓                                        │
│  06:30  Deep Research returns Update Manifest    │
│         ↓                                        │
│  06:45  HUMAN REVIEW — QA checklist              │
│         Approve / flag discrepancies             │
│         ↓                                        │
│  07:00  Open Claude Code                         │
│         + Phase 2 Prompt                         │
│         + Approved Manifest                      │
│         ↓                                        │
│  07:15  Agent updates JSON files                 │
│         Agent commits + pushes to main           │
│         ↓                                        │
│  07:20  Cloudflare Pages auto-deploys            │
│         ↓                                        │
│  07:25  VERIFY — spot check live dashboard       │
│         ↓                                        │
│  DONE   Dashboard reflects Day [N] intelligence  │
└─────────────────────────────────────────────────┘
```

---

## Evolution Path

This protocol is the **manual-but-formalized** version. The next stages:

### Stage 2 — Semi-Automated Collection
- Script the GitHub pull + file upload step
- Pre-populate the date and war day number in the prompt
- Add a `diff` report after Phase 2 for faster QA

### Stage 3 — Corpus of War Integration
- Daily corpus collection pipeline feeds Phase 1 (replacing raw web research)
- Deep Research operates on corpus + current data state
- Historical corpus enables trend detection and temporal queries
- LangGraph orchestration chains Claude + GPT-5 + Gemini for cross-validation

### Stage 4 — Full Automation
- Cron-triggered daily pipeline
- Collection agents → Corpus → Multi-LLM extraction → Update manifest → Auto-PR
- Human review is the only manual step (approve PR)
- Slack notification on completion

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

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-19 | Initial formalization of daily update workflow |
