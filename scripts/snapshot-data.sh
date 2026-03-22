#!/usr/bin/env bash
# snapshot-data.sh — Bundle all dashboard JSON data files into a dated zip archive.
# Usage: ./scripts/snapshot-data.sh [YYYY-MM-DD]
# If no date is provided, uses today's date.
# Output: snapshots/YYYY-MM-DD_DATABASE_SNAPSHOT.zip

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$REPO_ROOT/public/data"
SNAP_DIR="$REPO_ROOT/snapshots"

DATE="${1:-$(date +%Y-%m-%d)}"
FILENAME="${DATE}_DATABASE_SNAPSHOT.zip"
OUTPATH="$SNAP_DIR/$FILENAME"

mkdir -p "$SNAP_DIR"

# Collect all top-level JSON files + briefings/index.json
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Copy data files preserving directory structure
for f in "$DATA_DIR"/*.json; do
    cp "$f" "$TMPDIR/$(basename "$f")"
done

# Include briefings index (not the HTML fragments — just the metadata)
if [ -f "$DATA_DIR/briefings/index.json" ]; then
    mkdir -p "$TMPDIR/briefings"
    cp "$DATA_DIR/briefings/index.json" "$TMPDIR/briefings/index.json"
fi

# Create zip
(cd "$TMPDIR" && zip -r "$OUTPATH" . -x '.*') > /dev/null

echo "Snapshot created: $OUTPATH"
echo "Contains $(find "$TMPDIR" -name '*.json' | wc -l) JSON files"
echo "Size: $(du -h "$OUTPATH" | cut -f1)"
