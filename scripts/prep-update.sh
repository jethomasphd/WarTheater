#!/usr/bin/env bash
# Prepare a daily update session.
# Usage: ./scripts/prep-update.sh [YYYY-MM-DD]
#
# This script:
#   1. Calculates the war day
#   2. Pulls the latest data from main
#   3. Renders the Phase 1 prompt with today's date and war day filled in
#   4. Prints instructions for the operator
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TODAY="${1:-$(date +%Y-%m-%d)}"
WAR_DAY=$("$REPO_ROOT/scripts/war-day.sh" "$TODAY")

echo "========================================"
echo "  IranWar.ai Daily Update — Day $WAR_DAY"
echo "  Date: $TODAY"
echo "========================================"
echo ""

# Pull latest
echo "Pulling latest from origin/main..."
git -C "$REPO_ROOT" pull origin main --ff-only 2>/dev/null || echo "  (already up to date or not on main)"
echo ""

# Validate current data
echo "Validating current data files..."
"$REPO_ROOT/scripts/validate-data.sh"
echo ""

# Render Phase 1 prompt
PHASE1="$REPO_ROOT/ops/prompts/phase1-deep-research.md"
echo "========================================"
echo "  PHASE 1 PROMPT (copy into Deep Research)"
echo "========================================"
echo ""
sed -e "s/Today is ________\./Today is $TODAY./" \
    -e "s/Today is Day ___\./Today is Day $WAR_DAY./" \
    "$PHASE1"
echo ""

echo "========================================"
echo "  NEXT STEPS"
echo "========================================"
echo "  1. Copy the Phase 1 prompt above into Claude Deep Research"
echo "  2. Upload these 5 files from public/data/:"
echo "     - strikes-iran.json"
echo "     - strikes-retaliation.json"
echo "     - carriers.json"
echo "     - timeline-events.json"
echo "     - baselines.json"
echo "  3. Wait for the Update Manifest"
echo "  4. QA review (see ops/daily-checklist.md)"
echo "  5. Run Phase 2: paste ops/prompts/phase2-code-execution.md + manifest"
echo "  6. Save manifest to: updates/manifests/manifest-${TODAY}-day${WAR_DAY}.md"
echo ""
