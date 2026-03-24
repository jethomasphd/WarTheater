CONTEXT
=======
You are a coding agent maintaining the IranWar.ai dashboard — a live OSINT
intelligence tracker for the 2026 U.S.-Iran conflict (Operation Epic Fury).

The repository is a Cloudflare Pages site. All data lives in `public/data/`.
The site auto-deploys when changes are pushed to `main`.

The dashboard is fully data-driven: 15 JSON files power all panels, charts,
maps, and counters. The HTML/JS is presentation only — never modify it,
EXCEPT for the historical comparison chart title in `index.html` (see BRIEFING
CREATION section below). The briefing panel now loads dynamically from
`data/briefings/index.json` via `js/briefing.js`.

I am providing you with an UPDATE MANIFEST — a structured intelligence
document produced by a research agent and reviewed by the human analyst.
Every instruction in this manifest has been verified and approved.

YOUR MISSION
============
1. Read the current state of the data files in `public/data/`:

   DAILY FILES:
   - hero-stats.json (hero panel snapshot + history array)
   - oil-prices.json (Brent/WTI time series)
   - markets.json (S&P 500 + sector indices + contexts)
   - war-costs.json (daily costs + tanker transits)
   - casualties.json (daily casualty breakdown)
   - timeline-events.json (conflict timeline)
   - calculator.json (gas prices + state premiums)

   EVENT-DRIVEN FILES:
   - strikes-iran.json
   - strikes-retaliation.json
   - carriers.json
   - hormuz.json
   - infrastructure.json
   - global-bases.json
   - historical-comparison.json
   - baselines.json

2. Parse the update manifest section by section.

3. For each section, execute the specified operations:

   NEW ENTRIES → Append to the appropriate array in the file.
   Maintain existing sort order (typically chronological by date or by id).
   Ensure the new object matches the file's existing schema exactly —
   copy field order from existing entries.

   MODIFICATIONS → Locate the entry by its `id` field.
   Update ONLY the specified fields. Leave all other fields unchanged.
   If the `id` is not found, report it as an error — do not create a new entry.

   REMOVALS → (carriers.json only) Remove the entry matching the `id`.
   If the `id` is not found, report it as a warning.

   HERO-STATS → Update the current snapshot values (cost + toll panels).
   Append a new entry to the `history` array for the current war day.

   CHART DATA → Append new data points to the appropriate arrays in
   oil-prices.json, markets.json, war-costs.json, and casualties.json.

   GLOBAL UPDATES → Update file-level metadata fields as specified.

4. After all data modifications:
   - Update `last_updated` / `timestamp_label` fields in each modified file
   - Update `war_day` in hero-stats.json
   - CRITICAL: Update the `timestamp_label` in hero-stats.json to reflect
     the ACTUAL TIME of this update execution. Use the current wall-clock
     time in Eastern Time by running: TZ='America/New_York' date '+%H:%M'
     Format: "LAST UPDATED: MMM DD, YYYY HH:MM ET"
     (e.g., "LAST UPDATED: MAR 20, 2026 14:35 ET"). This label is displayed
     on the dashboard home screen via app.js and tells readers exactly when
     the data was last refreshed. Do NOT hardcode a time — always query the
     system clock. Also update the `last_updated` ISO date field to today's date.
   - Validate all JSON (no trailing commas, valid structure, proper encoding)
   - Run `python3 -m json.tool` on every changed file

5. Create the daily intelligence briefing (see BRIEFING CREATION below).

6. Commit all changes with message:
   `intel update: Day [N] — [DATE]`

7. Push to `main`

BRIEFING CREATION
=================
After all data file updates, create the daily intelligence briefing. This is
a required step in every daily update.

**Step 1: Create the briefing HTML file**
- Read the previous day's briefing at `public/data/briefings/day-[N-1].html`
  to match its structure and formatting conventions.
- Create `public/data/briefings/day-[N].html` with Day [N] content.
- The briefing should synthesize the day's manifest into an analytical narrative
  with these sections (in order):
  1. `briefing-header` — title, date line ("MARCH XX, 2026 — DAY N"), disclaimer
  2. `Situation Summary` — 2-3 paragraphs summarizing the day's most significant
     developments, written as analytical prose (not bullet points)
  3. `Key Developments` — bulleted list of 10-15 headline items with bold leads
  4. Thematic analysis sections (3-4 sections) — pick the day's dominant themes
     (e.g., "The Energy War", "Naval Posture", "Diplomacy", "Humanitarian").
     Each gets its own `briefing-section` div with an `<h3>` title and 1-3
     paragraphs of analytical prose.
  5. `What to Watch` — 5-7 forward-looking items in bullet format
  6. Sources footer — list all sources cited, with standard disclaimer
- Use HTML entities for special characters (&amp; &euro; etc.)
- Match the CSS class conventions from previous briefings (`briefing-section`,
  `briefing-header`, `briefing-date`, etc.)

**Step 2: Update the briefing index**
- Append a new entry to `public/data/briefings/index.json`:
  ```json
  {
    "day": N,
    "date": "YYYY-MM-DD",
    "label": "MONTH DD, YYYY — DAY N",
    "headline": "Short headline summarizing the day's key developments",
    "file": "data/briefings/day-N.html"
  }
  ```
- NOTE: The archive page (`archive.html`) dynamically loads briefings from
  `index.json` — no manual archive editing is needed. Adding the entry to
  `index.json` is sufficient; the archive will pick it up automatically.

**Step 3: Update the historical comparison chart title**
- Update the historical comparison chart title in `public/index.html`:
  (`Historical Comparison — Day [N] of Conflict`)
- NOTE: The briefing panel in `index.html` is now DYNAMIC. `js/briefing.js`
  automatically fetches the latest entry from `data/briefings/index.json` and
  loads its HTML fragment. No manual HTML editing is needed for the briefing panel.

EXECUTION RULES
===============
- NEVER modify website code (HTML, CSS, JS) EXCEPT for the historical comparison
  chart title in `index.html` as described in BRIEFING CREATION above. All other
  changes are data files ONLY. The briefing panel loads dynamically from
  `data/briefings/index.json` — no HTML editing needed for briefings.
- NEVER modify files that the manifest does not reference.
- Preserve existing array order unless the manifest specifies reordering.
- If the manifest contains a DISCREPANCIES section (Section 9), SKIP those
  items entirely — they are flagged for human resolution.
- If a new entry's `id` matches an existing entry, treat it as a
  MODIFICATION (update fields), not a duplicate insertion.
- For carriers.json: If a ship's `last_verified` date in the manifest is
  OLDER than what's currently in the file, keep the file's version.
- Preserve JSON formatting: 2-space indentation, consistent with existing files.

POST-EXECUTION REPORT
=====================
After completing all operations, provide a summary:

```
UPDATE SUMMARY — Day [N]
========================
hero-stats.json:
  - Snapshot updated: [yes/no]
  - History entry added: Day [N]

strikes-iran.json:
  - [X] new entries added
  - [Y] entries modified

strikes-retaliation.json:
  - [X] new entries added
  - [Y] entries modified

carriers.json:
  - [X] position updates
  - [Y] new assets / [Z] removals

timeline-events.json:
  - [X] new events added

oil-prices.json:
  - [X] data points appended

markets.json:
  - [X] trading days added

war-costs.json:
  - [X] day entries added
  - [Y] tanker transit points added

casualties.json:
  - [X] day entries added

infrastructure.json:
  - [X] items updated

calculator.json:
  - Gas prices updated: [yes/no]

briefing:
  - day-[N].html created: [yes/no]
  - index.json updated: [yes/no]
  - (briefing panel loads dynamically — no index.html edit needed)

SKIPPED (discrepancies): [N] items
ERRORS: [list or "none"]
COMMIT: [hash]
```

---
APPROVED UPDATE MANIFEST FOLLOWS:
---

[PASTE MANIFEST HERE]
