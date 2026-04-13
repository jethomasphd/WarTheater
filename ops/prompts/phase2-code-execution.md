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

**Step 1: Create the briefing HTML file — COPY-THEN-EDIT ONLY**

MANDATORY STRATEGY: Never draft the briefing HTML from scratch. Writing a full
briefing via `Write` or by generating a large block of HTML in a single tool
call is a known failure mode — it routinely times out and produces
structural regressions (missing `</div>`, wrong class names, broken entity
encoding, etc.). Use the copy-then-edit pattern below exactly as written.

1. **Copy the previous day's briefing as the scaffold:**
   ```
   cp public/data/briefings/day-[N-1].html public/data/briefings/day-[N].html
   ```
   This is the first action of briefing creation. The template already
   contains every class, div, entity, and structural convention the
   dashboard expects. Do not attempt to write the file with `Write`.

2. **Commit the scaffold immediately (checkpoint):**
   ```
   git add public/data/briefings/day-[N].html
   git commit -m "intel update: Day [N] — YYYY-MM-DD (briefing scaffold from day-[N-1])"
   git push origin <branch>
   ```
   This preserves the scaffold on the remote so that, if the session times
   out mid-edit, the next iteration can resume without redoing the copy.

3. **Edit the scaffold one section at a time using the `Edit` tool:**
   - Update the date line: `DAY [N-1]` → `DAY [N]`, and the month/day.
   - Replace the `Situation Summary` paragraphs (2–3 analytical paragraphs).
   - Replace the `Key Developments` bullet list (10–15 items, bold leads).
   - Replace / rename each thematic `briefing-section` (3–4 sections).
     Keep the wrapping `<div class="briefing-section">...</div>` and
     `<h3>` element; change only the heading text and the `<p>` content.
   - Replace the `What to Watch` bullet list (5–7 forward-looking items).
   - Refresh the sources footer to reflect Day [N]'s actual sources.
   - **Checkpoint commit after every 1–2 section replacements.** Push each
     commit. This prevents losing work if the session terminates.

4. **Structural rules that MUST hold:**
   - Exactly one `briefing-header` div, containing the `briefing-date`.
   - 5–7 `briefing-section` divs total (1 Summary + 1 Key Developments +
     3–4 Thematic + 1 What to Watch).
   - Sources footer at the bottom, styled with the same inline `style`
     attribute as the previous day.
   - Use HTML entities for special characters (`&amp; &mdash; &ldquo;
     &rdquo; &lsquo; &rsquo; &euro;` etc.) — copy the pattern from the
     scaffold; do not invent new encodings.
   - If a thematic section from Day [N-1] is no longer relevant, replace
     its content (heading + paragraphs) rather than deleting the div.
     If you need to remove a section, delete the entire
     `<div class="briefing-section">...</div>` block as a single `Edit`.

5. **Validation before final push:**
   ```
   grep -c 'briefing-section' public/data/briefings/day-[N].html
   ```
   Expect the count to match Day [N-1] ± your intentional additions/removals.
   Open the file and verify the top line is `<div class="briefing-header">`
   and the bottom closing `</div>` is intact.

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
