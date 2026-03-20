#!/usr/bin/env bash
# Calculate the current war day (Day 1 = Feb 28, 2026)
WAR_START="2026-02-28"
TODAY="${1:-$(date +%Y-%m-%d)}"
DAYS=$(( ( $(date -d "$TODAY" +%s) - $(date -d "$WAR_START" +%s) ) / 86400 + 1 ))
echo "$DAYS"
