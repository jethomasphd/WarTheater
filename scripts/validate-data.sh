#!/usr/bin/env bash
# Validate all JSON data files in public/data/
set -euo pipefail

DATA_DIR="$(cd "$(dirname "$0")/../public/data" && pwd)"
ERRORS=0

FILES=(
  "strikes-iran.json"
  "strikes-retaliation.json"
  "carriers.json"
  "timeline-events.json"
  "baselines.json"
  "hormuz.json"
)

for f in "${FILES[@]}"; do
  FILE="$DATA_DIR/$f"
  if [ ! -f "$FILE" ]; then
    echo "WARN: $f not found — skipping"
    continue
  fi
  if python3 -m json.tool "$FILE" > /dev/null 2>&1; then
    echo "  OK: $f"
  else
    echo "FAIL: $f — invalid JSON"
    ERRORS=$((ERRORS + 1))
  fi
done

# Validate briefings index
BRIEFINGS="$DATA_DIR/briefings/index.json"
if [ -f "$BRIEFINGS" ]; then
  if python3 -m json.tool "$BRIEFINGS" > /dev/null 2>&1; then
    echo "  OK: briefings/index.json"
  else
    echo "FAIL: briefings/index.json — invalid JSON"
    ERRORS=$((ERRORS + 1))
  fi
fi

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "$ERRORS file(s) failed validation."
  exit 1
else
  echo ""
  echo "All data files valid."
fi
