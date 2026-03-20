# IranWar.ai — Daily Update Checklist

**Date:** __________ | **War Day:** ____

---

## Pre-flight (2 min)
- [ ] Calculate war day: (today - Feb 28, 2026) + 1 = Day ___
- [ ] Pull latest 5 JSONs from `public/data/` in GitHub repo
- [ ] Fill in date + war day in Phase 1 prompt

## Phase 1: Deep Research (~25 min)
- [ ] Open Claude Deep Research (new conversation)
- [ ] Upload all 5 JSON files
- [ ] Paste Phase 1 prompt (with date/day filled in)
- [ ] Wait for research completion
- [ ] Download the Update Manifest (.md)

## QA Review (~15 min)
- [ ] Every new JSON object has ALL required schema fields
- [ ] Coordinates are plausible (Iran: ~25-40°N, ~44-63°E)
- [ ] `active_days` arrays match `first_strike` dates
- [ ] Source attributions are specific (not "various reports")
- [ ] Naval positions cite USNI Fleet Tracker or equivalent
- [ ] Casualty figures attribute to specific reporting body
- [ ] No fabricated ship names, hull numbers, or units
- [ ] Discrepancies section is populated (zero = suspicious)
- [ ] Remove or flag anything that fails QA

## Phase 2: Code Execution (~15 min)
- [ ] Open Claude Code (connected to iranwar repo)
- [ ] Paste Phase 2 prompt
- [ ] Paste the approved Update Manifest
- [ ] Review the agent's post-execution summary
- [ ] Verify commit message format: `intel update: Day [N] — [DATE]`
- [ ] Confirm push to `main`

## Verification (5 min)
- [ ] Check Cloudflare Pages deployment status
- [ ] Open iranwar.ai — spot check:
  - [ ] Map shows new strike markers (if any)
  - [ ] Timeline has today's events
  - [ ] Naval tracker reflects position changes
  - [ ] Financial panel shows current figures
- [ ] No console errors in browser dev tools

## Done
- [ ] Archive the Update Manifest in local `manifests/` directory
  - Filename: `manifest-YYYY-MM-DD-dayN.md`
