#!/usr/bin/env python3
"""
07 — Diplomacy and violence (military-diplomatic cross-domain).

Do strike clusters precede, follow, or co-occur with diplomatic activity?
  - Phase-level substitution: diplomacy vs. violence intensity by regime.
  - Weekly-aggregate correlation (low-frequency substitution).
  - Cross-correlation function of daily violence vs. daily diplomacy (lead-lag).
  - Granger test: does violence Granger-cause diplomacy, or the reverse?

Outputs:
  output/tables/t07_diplomacy_phase.csv
  output/tables/t07_crosscorr.csv
  output/tables/t07_granger_diplo.csv
  output/figures/fig6_diplomacy_violence.(png|pdf)
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.api import VAR

import util

warnings.filterwarnings("ignore")


def ccf(x, y, lag):
    """corr(x_t, y_{t+lag}); lag>0 => x leads y."""
    x = np.asarray(x, float) - np.mean(x)
    y = np.asarray(y, float) - np.mean(y)
    if lag > 0:
        a, b = x[:-lag], y[lag:]
    elif lag < 0:
        a, b = x[-lag:], y[:lag]
    else:
        a, b = x, y
    if a.std() == 0 or b.std() == 0:
        return np.nan
    return np.corrcoef(a, b)[0, 1]


def main():
    print("=" * 68)
    print("Paper 1 · Step 07 · Diplomacy and violence")
    print("=" * 68)
    p = util.load_panel()
    p = p.copy()
    p["violence"] = p["strikes"] + p["retal"]

    # ---- phase-level substitution ------------------------------------- #
    rows = []
    for name, lo, hi in util.PHASES:
        seg = p[(p.index >= lo) & (p.index <= hi)]
        rows.append({"phase": name, "days": f"{lo}-{hi}",
                     "violence_per_day": round(seg["violence"].mean(), 2),
                     "diplomatic_per_day": round(seg["diplomatic"].mean(), 2),
                     "share_days_diplomacy": round((seg["diplomatic"] > 0).mean(), 3)})
    dt = pd.DataFrame(rows)
    dt.to_csv(util.TAB_DIR / "t07_diplomacy_phase.csv", index=False)
    print("\n--- Diplomacy vs. violence by phase ---")
    print(dt.to_string(index=False))

    # ---- weekly-aggregate correlation --------------------------------- #
    wk = p.copy()
    wk["week"] = ((wk.index - 1) // 7)
    wa = wk.groupby("week")[["violence", "diplomatic"]].sum()
    r_w, p_w = stats.pearsonr(wa["violence"], wa["diplomatic"])
    print(f"\nWeekly violence vs weekly diplomacy: r={r_w:.3f} (p={p_w:.4f}, n={len(wa)} weeks)")

    # ---- cross-correlation function ----------------------------------- #
    lags = list(range(-10, 11))
    cc_full = [ccf(p["violence"], p["diplomatic"], k) for k in lags]
    combat = p[p.index <= util.KINETIC_END]
    cc_combat = [ccf(combat["violence"], combat["diplomatic"], k) for k in lags]
    cct = pd.DataFrame({"lag_days": lags,
                        "ccf_full": np.round(cc_full, 3),
                        "ccf_combat": np.round(cc_combat, 3)})
    cct.to_csv(util.TAB_DIR / "t07_crosscorr.csv", index=False)
    kmax_full = lags[int(np.nanargmax(np.abs(cc_full)))]
    print(f"\nViolence-diplomacy cross-correlation (full): peak |r| at lag "
          f"{kmax_full}d (lag>0 => violence leads diplomacy)")

    # ---- Granger: violence <-> diplomacy (full sample) ---------------- #
    grows = []
    data = p[["violence", "diplomatic"]].astype(float)
    m = VAR(data)
    lag = int(m.select_order(10).selected_orders.get("bic", 2)) or 2
    res = m.fit(lag)
    for cause, effect in [("violence", "diplomatic"), ("diplomatic", "violence")]:
        gc = res.test_causality(effect, [cause], kind="f")
        grows.append({"sample": "full 1-170", "lag": lag,
                      "direction": f"{cause} -> {effect}",
                      "F": round(float(gc.test_statistic), 3),
                      "p_value": round(float(gc.pvalue), 4),
                      "granger_causal_05": bool(gc.pvalue < 0.05)})
    gt = pd.DataFrame(grows)
    gt.to_csv(util.TAB_DIR / "t07_granger_diplo.csv", index=False)
    print("\n--- Granger: violence <-> diplomacy (full sample) ---")
    print(gt.to_string(index=False))

    # ---- figure ------------------------------------------------------- #
    util.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0),
                             gridspec_kw={"width_ratios": [1.35, 1]})

    # left: weekly violence vs diplomacy dual axis
    ax = axes[0]
    weeks = wa.index * 7 + 4
    ax.bar(weeks, wa["violence"], width=6.0, color=util.C_STRIKE, alpha=0.45,
           label="violence (strikes+retal)/week")
    ax.set_ylabel("Violence events / week", color=util.C_STRIKE)
    ax.tick_params(axis="y", labelcolor=util.C_STRIKE)
    ax.set_xlabel("Day of conflict")
    ax2 = ax.twinx()
    ax2.plot(weeks, wa["diplomatic"], color=util.C_DIPL, lw=2.2,
             label="diplomatic events/week")
    ax2.set_ylabel("Diplomatic events / week", color=util.C_DIPL)
    ax2.tick_params(axis="y", labelcolor=util.C_DIPL)
    ax2.grid(False)
    ax.set_title(f"A. Weekly substitution (r={r_w:.2f})", loc="left", fontweight="bold")

    # right: cross-correlation function
    ax = axes[1]
    ax.axhline(0, color="0.6", lw=0.8)
    ax.axvline(0, color="0.8", lw=0.8, ls=":")
    ci = 1.96 / np.sqrt(len(p))
    ax.axhspan(-ci, ci, color="0.85", alpha=0.5)
    ax.stem(lags, cc_full, linefmt=util.C_ACCENT, markerfmt="o", basefmt=" ")
    ax.set_xlabel("Lag (days); lag>0 = violence leads diplomacy")
    ax.set_ylabel("Cross-correlation")
    ax.set_title("B. Violence → diplomacy CCF", loc="left", fontweight="bold")
    util.savefig(fig, "fig6_diplomacy_violence")
    plt.close(fig)
    print(f"\nWrote tables + fig6 to {util.OUT_DIR}")


if __name__ == "__main__":
    main()
