#!/usr/bin/env python3
"""
Recalibrate the daily war-cost series in public/data/war-costs.json to official
cumulative anchors (Pentagon disclosures).

Method: shape-preserving piecewise scaling.
  - Between consecutive anchors, the dollar increment is fixed by the official
    figures (anchor_k - anchor_{k-1}).
  - That increment is distributed across the days of the segment in proportion
    to the LEGACY modeled daily series (kept in `legacy_daily_cost_millions`),
    so intensity patterns (combat surges vs. ceasefire lulls) are preserved.
  - Integer $M per day; rounding residual lands on the segment's last day so the
    cumulative hits each anchor exactly.
  - After the last anchor, the most recent official run-rate (last segment's
    increment / days) is carried forward until the next disclosure.

Re-run whenever a new official anchor is published: add it to ANCHORS, then
  python3 scripts/recalibrate-costs.py
It rewrites war-costs.json (daily series + metadata) and the hero-stats.json
history cost fields so every surface agrees.
"""
import json, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "public" / "data"
START = datetime.date(2026, 2, 28)   # Day 1

# (war_day, cumulative $B, as-of date, source) — keep sorted by war_day.
ANCHORS = [
    (6,   11.3, "2026-03-05", "Pentagon closed-door briefing to Congress: first six days $11.3B"),
    (61,  25.0, "2026-04-29", "Acting Pentagon Comptroller Jules Hurst, HASC testimony: ~$25B"),
    (74,  29.0, "2026-05-12", "Comptroller Hurst, House/Senate Appropriations: ~$29B"),
    (144, 37.5, "2026-07-21", "SecDef Hegseth, Senate Appropriations: $37.5B direct cost"),
    (188, 43.6, "2026-09-03", "Pentagon to Congress via Bloomberg Government: $43.6B ($28.1B munitions, $11.2B ops, $4.3B equipment; $45.1B incl. $1.5B fuel)"),
    (231, 47.1, "2026-10-16", "Pentagon via ABC News: $47.1B (~$29B munitions, $11.9B ops, $6B equipment losses)"),
    (259, 48.3, "2026-11-13", "Pentagon deputy comptroller Arthur Miller, Senate testimony Nov 19: 'As of Nov 13, it was $48.3 billion'"),
]

def main():
    wc_path = ROOT / "war-costs.json"
    wc = json.loads(wc_path.read_text())
    legacy = wc.get("legacy_daily_cost_millions") or list(wc["daily_cost_millions"])
    n = len(legacy)
    new = [0] * n

    prev_day, prev_cum = 0, 0.0
    for day, cum_b, _, _ in ANCHORS:
        seg = range(prev_day, day)                     # 0-based indices
        inc = round((cum_b - prev_cum) * 1000)         # $M
        shape = [max(legacy[i], 1) for i in seg]
        tot = sum(shape)
        vals = [int(round(inc * s / tot)) for s in shape]
        vals[-1] += inc - sum(vals)
        for i, v in zip(seg, vals):
            new[i] = v
        prev_day, prev_cum = day, cum_b

    # Carry forward the latest official run-rate.
    (d1, c1, _, _), (d0, c0, _, _) = ANCHORS[-1], ANCHORS[-2]
    run_rate = round((c1 - c0) * 1000 / (d1 - d0))
    for i in range(prev_day, n):
        new[i] = run_rate

    total_b = sum(new) / 1000
    wc["legacy_daily_cost_millions"] = legacy
    wc["daily_cost_millions"] = new
    wc["official_anchors"] = [
        {"war_day": d, "as_of": a, "cumulative_billions": c, "source": s} for d, c, a, s in ANCHORS
    ]
    wc["cost_methodology"] = (
        f"OFFICIAL-ANCHORED (recalibrated 2026-11-27). Daily values are scaled so the cumulative total passes exactly through each "
        f"official disclosure listed in official_anchors (Pentagon/comptroller figures only; CSIS's independent $16.5B through Day 12 is not used as an anchor). Within each segment the "
        f"dollars are distributed in proportion to the legacy modeled series (legacy_daily_cost_millions), preserving the shape of "
        f"combat surges and ceasefire lulls. After the latest anchor (Day {d1}), the most recent official run-rate "
        f"(${run_rate}M/day = ${c1 - c0:.1f}B over {d1 - d0} days) is carried forward until the next disclosure. "
        f"Cumulative at Day {n}: ${total_b:.1f}B. Official figures cover munitions, operations and equipment replacement and EXCLUDE "
        f"damage to US bases, a future supplemental, interest and economy-wide costs (Moody's: $132B+ consumer/taxpayer; Brown "
        f"Watson Institute fuel-cost tracker). CBO's independent $38.1B through Aug 1 is consistent with the Pentagon path. The legacy "
        f"model (flat $500M/day from Day 130, set during the July strike campaign) reached ${sum(legacy)/1000:.1f}B and is retained "
        f"only for audit."
    )
    wc["last_updated"] = "2026-11-27"
    wc_path.write_text(json.dumps(wc, indent=2, ensure_ascii=False) + "\n")

    # Sync hero-stats history cost fields.
    hs_path = ROOT / "hero-stats.json"
    hs = json.loads(hs_path.read_text())
    cums, s = [], 0
    for v in new:
        s += v; cums.append(s)
    for e in hs["history"]:
        wd = e.get("war_day")
        if isinstance(wd, int) and 1 <= wd <= n:
            e["daily_cost_millions"] = new[wd - 1]
            e["total_cost_billions"] = round(cums[wd - 1] / 1000, 2)
    hs_path.write_text(json.dumps(hs, indent=2, ensure_ascii=False) + "\n")

    print(f"run-rate ${run_rate}M/day; Day {n} cumulative ${total_b:.2f}B")
    for d, c, _, _ in ANCHORS:
        print(f"  check Day {d}: {cums[d-1]/1000:.2f} vs {c}")

if __name__ == "__main__":
    main()
