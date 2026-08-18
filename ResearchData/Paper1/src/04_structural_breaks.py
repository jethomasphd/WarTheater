#!/usr/bin/env python3
"""
04 — Endogenous regime detection (multiple structural breaks in the mean).

We fit a mean-shift model to the daily strike-intensity series and select the
number and location of breakpoints by least-squares dynamic programming with a
BIC penalty (the Bai-Perron multiple-break model for a change in mean; Bai &
Perron 2003), implemented dependency-free. The data-driven breaks are compared
to the project's documented phase boundaries (Days 41, 130, 153) as an external
validation that the phases are not imposed but recovered from the data.

Outputs:
  output/tables/t04_breakpoints.csv
  output/figures/fig4_structural_breaks.(png|pdf)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import util

MIN_SEG = 6      # minimum regime length (days)
MAX_K = 6        # maximum number of segments considered


def _prefix_sums(x):
    n = len(x)
    s = np.concatenate([[0], np.cumsum(x)])
    s2 = np.concatenate([[0], np.cumsum(x * x)])
    return s, s2


def seg_cost(s, s2, i, j):
    """SSE of x[i:j] about its mean, via prefix sums (0<=i<j<=n)."""
    n = j - i
    if n <= 0:
        return 0.0
    tot = s[j] - s[i]
    tot2 = s2[j] - s2[i]
    return tot2 - tot * tot / n


def best_partition(x, K, min_seg):
    """Optimal partition of x into exactly K contiguous segments minimizing total
    SSE, with a minimum segment length. Returns (total_sse, breakpoints)."""
    n = len(x)
    s, s2 = _prefix_sums(x)
    NEG = np.inf
    # dp[k][j] = min SSE partitioning x[0:j] into k segments
    dp = np.full((K + 1, n + 1), NEG)
    back = np.full((K + 1, n + 1), -1, dtype=int)
    dp[0][0] = 0.0
    for k in range(1, K + 1):
        for j in range(k * min_seg, n + 1):
            # last segment [i:j], need i so that previous k-1 segs each >= min_seg
            lo = (k - 1) * min_seg
            hi = j - min_seg
            for i in range(lo, hi + 1):
                if dp[k - 1][i] == NEG:
                    continue
                c = dp[k - 1][i] + seg_cost(s, s2, i, j)
                if c < dp[k][j]:
                    dp[k][j] = c
                    back[k][j] = i
    # recover breakpoints for exactly K
    sse = dp[K][n]
    bps, j, k = [], n, K
    while k > 0:
        i = back[k][j]
        bps.append((i, j))
        j, k = i, k - 1
    bps.reverse()
    breaks = [seg[0] for seg in bps[1:]]  # interior break indices
    return sse, breaks


def main():
    print("=" * 68)
    print("Paper 1 · Step 04 · Structural-break / regime detection")
    print("=" * 68)
    p = util.load_panel()
    x = p["strikes"].astype(float).values
    n = len(x)

    # select K by BIC
    rows = []
    best = None
    for K in range(1, MAX_K + 1):
        sse, breaks = best_partition(x, K, MIN_SEG)
        # BIC for K-segment mean model (K means + 1 variance)
        rss = max(sse, 1e-9)
        bic = n * np.log(rss / n) + (K + 1) * np.log(n)
        rows.append({"n_segments": K, "n_breaks": K - 1, "sse": round(sse, 1),
                     "bic": round(bic, 2),
                     "break_days": ",".join(str(b + 1) for b in breaks)})
        if best is None or bic < best["bic"]:
            best = {"K": K, "bic": bic, "breaks": breaks, "sse": sse}
    sel = pd.DataFrame(rows)
    print(sel.to_string(index=False))

    kbest = int(best["K"])
    breaks = [int(b) for b in best["breaks"]]   # 0-based indices into x; day = idx+1
    break_days = [b + 1 for b in breaks]
    print(f"\nBIC-optimal: {kbest} segments, breaks at days {break_days}")

    documented = [41, 130, 153]
    # nearest documented boundary for each detected break
    match_rows = []
    for bd in break_days:
        nearest = min(documented, key=lambda d: abs(d - bd))
        match_rows.append({"detected_break_day": bd,
                           "detected_date": util.date_from_day(bd).isoformat(),
                           "nearest_documented": nearest,
                           "gap_days": bd - nearest})
    mt = pd.DataFrame(match_rows)
    print("\n--- Detected breaks vs. documented phase boundaries ---")
    print(mt.to_string(index=False))

    sel.to_csv(util.TAB_DIR / "t04_break_selection.csv", index=False)
    mt.to_csv(util.TAB_DIR / "t04_breakpoints.csv", index=False)

    # regime means
    seg_bounds = [0] + break_days + [n]  # in day-space edges (1-based day starts)
    # compute means per detected segment
    means = []
    edges = [0] + breaks + [n]
    for a, b in zip(edges[:-1], edges[1:]):
        means.append(x[a:b].mean())

    # ---------------- figure ------------------------------------------- #
    util.apply_style()
    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    days = p.index.values
    ax.plot(days, x, color=util.C_STRIKE, lw=1.2, alpha=0.75, label="strike tempo")
    # step function of regime means
    for (a, b), mu in zip(zip(edges[:-1], edges[1:]), means):
        ax.hlines(mu, a + 1 - 0.5, b + 0.5, color=util.C_RETAL, lw=2.6, zorder=5)
    for bd in break_days:
        ax.axvline(bd, color=util.C_RETAL, ls="-", lw=1.0, alpha=0.6)
    for d in documented:
        ax.axvline(d, color="0.3", ls="--", lw=1.0, alpha=0.8)
    ax.plot([], [], color=util.C_RETAL, lw=2.6, label="detected regime mean")
    ax.plot([], [], color="0.3", ls="--", label="documented phase boundary")
    ax.set_xlabel("Day of conflict (Day 1 = 2026-02-28)")
    ax.set_ylabel("Strikes per day\n(distinct locations)")
    ax.set_title(f"Endogenous regime detection: {kbest} BIC-optimal regimes; "
                 f"breaks at days {break_days}",
                 loc="left", fontweight="bold", fontsize=10.5)
    ax.legend(loc="upper right")
    util.savefig(fig, "fig4_structural_breaks")
    plt.close(fig)
    print(f"\nWrote tables + fig4 to {util.OUT_DIR}")


if __name__ == "__main__":
    main()
