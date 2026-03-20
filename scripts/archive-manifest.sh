#!/usr/bin/env bash
# Archive an update manifest after a successful daily update.
# Usage: ./scripts/archive-manifest.sh <path-to-manifest.md> [YYYY-MM-DD]
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANIFEST="$1"
TODAY="${2:-$(date +%Y-%m-%d)}"
WAR_DAY=$("$REPO_ROOT/scripts/war-day.sh" "$TODAY")
DEST="$REPO_ROOT/updates/manifests/manifest-${TODAY}-day${WAR_DAY}.md"

if [ ! -f "$MANIFEST" ]; then
  echo "Error: Manifest file not found: $MANIFEST"
  exit 1
fi

cp "$MANIFEST" "$DEST"
echo "Manifest archived to: $DEST"
