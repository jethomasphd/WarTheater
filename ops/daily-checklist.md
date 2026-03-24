# IranWar.ai — Daily Update Checklist

**Date:** __________ | **War Day:** ____

---

## Pre-flight (2 min)
- [ ] Calculate war day: (today - Feb 28, 2026) + 1 = Day ___
- [ ] Download today's snapshot from `snapshots/YYYY-MM-DD_DATABASE_SNAPSHOT.zip` (auto-generated at 3 AM CT)

## Phase 1: Deep Research (~25 min)
- [ ] Open Claude Deep Research (new conversation)
- [ ] Upload data files
- [ ] Paste Phase 1 prompt from `ops/prompts/phase1-deep-research.md` (fill in date + war day)
- [ ] Wait for research completion
- [ ] Download the Update Manifest (.md)

## QA Review (~15 min)

### Schema Compliance
- [ ] Every new JSON object has ALL required schema fields
- [ ] Field order matches existing entries in each file
- [ ] New hero-stats history entry has all required fields

### Geographic Data
- [ ] Strike coordinates are plausible (Iran: ~25-40°N, ~44-63°E)
- [ ] `active_days` arrays are consistent with `first_strike` dates
- [ ] Any new global-bases coordinates are reasonable

### Source Quality
- [ ] Source attributions are specific (not "various reports")
- [ ] Naval positions cite USNI Fleet Tracker or equivalent
- [ ] Casualty figures attribute to specific reporting body
- [ ] Financial data cites FRED, Yahoo Finance, ICE/NYMEX, or AAA

### Sanity Checks
- [ ] No fabricated ship names, hull numbers, or military units
- [ ] Oil prices are within plausible range of previous day
- [ ] S&P 500 value is within plausible range of previous day
- [ ] Casualty totals are monotonically increasing (not decreasing)
- [ ] War cost cumulative total >= previous day
- [ ] Discrepancies section is populated (zero = suspiciously clean)

### Final
- [ ] Remove or flag anything that fails QA
- [ ] Mark manifest as APPROVED

## Phase 2: Code Execution (~15 min)
- [ ] Open Claude Code (connected to this repo)
- [ ] Paste Phase 2 prompt from `ops/prompts/phase2-code-execution.md`
- [ ] Paste the approved Update Manifest
- [ ] Review the agent's post-execution summary
- [ ] Verify commit message format: `intel update: Day [N] — YYYY-MM-DD`
- [ ] Confirm push to `main`

## Verification (5 min)
- [ ] Check Cloudflare Pages deployment status
- [ ] Open iranwar.ai — spot check:
  - [ ] Hero stats show updated numbers
  - [ ] Map shows new strike markers (if any)
  - [ ] Timeline has today's events
  - [ ] Naval tracker reflects position changes
  - [ ] Financial charts have new data points
  - [ ] Casualty chart updated
  - [ ] Calculator reflects current gas price
  - [ ] Briefing panel dynamically loads today's briefing (from index.json → day-[N].html)
- [ ] Open iranwar.ai/archive — verify:
  - [ ] Today's briefing appears at the top with "Latest" badge
  - [ ] Briefing card auto-expands and content loads
  - [ ] Previous day's briefing is collapsed but loads on click
  - [ ] Briefing count is correct
- [ ] No console errors in browser dev tools

## Done
- [ ] Archive the Update Manifest in `updates/manifests/`
  - Filename: `manifest-YYYY-MM-DD-dayN.md`
