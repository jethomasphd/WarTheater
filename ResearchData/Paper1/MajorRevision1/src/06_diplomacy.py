#!/usr/bin/env python3
"""
06 — FINDING 5: diplomacy and violence move at the regime level, not week to week.

Weekly violence and weekly diplomacy are uncorrelated and neither Granger-causes the other,
yet diplomatic activity differs sharply across regimes (highest in the ceasefire, collapsing
at the resumption). Fighting and talking ran as parallel tracks that shifted together at
regime boundaries.

Outputs
  output/tables/t06_diplomacy_phase.csv     violence and diplomacy by phase
  output/tables/t06_weekly.csv              weekly aggregates and the weekly correlation
  output/tables/t06_crosscorr.csv           daily cross-correlation, lags -10..+10
  output/tables/t06_granger.csv             Granger tests, violence <-> diplomacy
  output/tables/t06_regime_test.csv         Kruskal-Wallis tests across phases
  output/figures/fig6_diplomacy.(png|pdf)
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


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 06 · Finding 5 — diplomacy and violence")
    print("=" * 70)
    p = util.load_panel().copy()
    p["violence"] = p["strikes"] + p["retal"]

    rows = []
    for name, lo, hi in util.PHASES:
        seg = p[(p.index >= lo) & (p.index <= hi)]
        rows.append({"phase": name, "days": f"{lo}-{hi}", "n_days": len(seg),
                     "violence_per_day": round(seg["violence"].mean(), 2),
                     "diplomatic_per_day": round(seg["diplomatic"].mean(), 2),
                     "share_days_with_diplomacy": round((seg["diplomatic"] > 0).mean(), 3)})
    dt = pd.DataFrame(rows)
    print("\n--- Diplomacy vs violence by phase ---")
    print(dt.to_string(index=False))
    util.write_table(dt, "t06_diplomacy_phase.csv")

    # weekly aggregates
    wk = p.copy(); wk["week"] = (wk.index - 1) // 7
    wa = wk.groupby("week")[["violence", "diplomatic"]].sum()
    wa["n_days"] = wk.groupby("week").size()
    r_w, p_w = stats.pearsonr(wa["violence"], wa["diplomatic"])
    rho_w, p_rho = stats.spearmanr(wa["violence"], wa["diplomatic"])
    full_weeks = wa[wa["n_days"] == 7]
    r_wf, p_wf = stats.pearsonr(full_weeks["violence"], full_weeks["diplomatic"])
    wt = wa.reset_index()
    wt["pearson_r_all_weeks"] = round(r_w, 3); wt["p_all_weeks"] = round(p_w, 4)
    wt["spearman_rho_all_weeks"] = round(rho_w, 3); wt["p_spearman"] = round(p_rho, 4)
    wt["pearson_r_full_weeks_only"] = round(r_wf, 3); wt["p_full_weeks_only"] = round(p_wf, 4)
    print(f"\nWeekly violence vs diplomacy: r={r_w:.3f} (p={p_w:.3f}, n={len(wa)} weeks); "
          f"Spearman rho={rho_w:.3f} (p={p_rho:.3f}); full weeks only r={r_wf:.3f} (n={len(full_weeks)})")
    util.write_table(wt, "t06_weekly.csv")

    # daily cross-correlation
    lags = list(range(-10, 11))
    cc_full = [util.ccf(p["violence"], p["diplomatic"], k) for k in lags]
    band = 1.96 / np.sqrt(len(p))
    cct = pd.DataFrame({"lag_days": lags, "ccf_full": np.round(cc_full, 3),
                        "outside_95_band": [abs(v) > band for v in cc_full]})
    util.write_table(cct, "t06_crosscorr.csv")
    print(f"  daily CCF: max |r| = {np.nanmax(np.abs(cc_full)):.3f} (band ±{band:.3f})")

    # Granger both directions, lag by BIC
    data = p[["violence", "diplomatic"]].astype(float)
    m = VAR(data)
    lag = max(int(m.select_order(10).selected_orders.get("bic", 2)), 1)
    res = m.fit(lag)
    grows = []
    for cause, effect in [("violence", "diplomatic"), ("diplomatic", "violence")]:
        gc = res.test_causality(effect, [cause], kind="f")
        grows.append({"sample": "full (Days 1-170)", "lag": lag,
                      "direction": f"{cause} -> {effect}",
                      "F": round(float(gc.test_statistic), 3), "p_value": round(float(gc.pvalue), 4),
                      "significant_05": bool(gc.pvalue < 0.05)})
    gt = pd.DataFrame(grows)
    print("\n--- Granger: violence <-> diplomacy ---")
    print(gt.to_string(index=False))
    util.write_table(gt, "t06_granger.csv")

    # regime-level test: do daily diplomacy / violence differ across phases?
    groups_d = [util.phase_slice(p, n)["diplomatic"].values for n in util.PHASE_ORDER]
    groups_v = [util.phase_slice(p, n)["violence"].values for n in util.PHASE_ORDER]
    kd = stats.kruskal(*groups_d); kv = stats.kruskal(*groups_v)
    # epsilon-squared effect size for Kruskal-Wallis: H / (n - 1)
    n = len(p)
    kt = pd.DataFrame([
        {"series": "diplomatic per day", "test": "Kruskal-Wallis across 4 phases",
         "H": round(float(kd.statistic), 2), "p_value": float(f"{kd.pvalue:.2e}"),
         "epsilon_squared": round(float(kd.statistic) / (n - 1), 3)},
        {"series": "violence per day", "test": "Kruskal-Wallis across 4 phases",
         "H": round(float(kv.statistic), 2), "p_value": float(f"{kv.pvalue:.2e}"),
         "epsilon_squared": round(float(kv.statistic) / (n - 1), 3)},
    ])
    print("\n--- Regime-level differences ---")
    print(kt.to_string(index=False))
    util.write_table(kt, "t06_regime_test.csv")

    # ---- Figure 6 -------------------------------------------------------- #
    util.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.9), gridspec_kw={"width_ratios": [1, 1.1]})
    ax = axes[0]
    ax.scatter(wa["violence"], wa["diplomatic"], s=40, color=util.C_DIPL, alpha=0.85,
               edgecolor="white", lw=0.5)
    ax.text(0.97, 0.95, f"weekly r = {r_w:.2f} (n = {len(wa)} weeks)", transform=ax.transAxes,
            ha="right", va="top", fontsize=9.5)
    ax.set_xlabel("Violence events per week (strikes + retaliation)")
    ax.set_ylabel("Diplomatic events per week")
    ax.set_title("A. Week to week: no association", loc="left", fontweight="bold")

    ax = axes[1]
    x = np.arange(len(dt)); w = 0.38
    ax.bar(x - w / 2, dt["violence_per_day"], w, color=util.C_STRIKE, label="violence / day")
    ax2 = ax.twinx()
    ax2.bar(x + w / 2, dt["diplomatic_per_day"], w, color=util.C_DIPL, label="diplomacy / day")
    ax2.grid(False)
    ax.set_ylabel("Violence events per day", color=util.C_STRIKE)
    ax2.set_ylabel("Diplomatic events per day", color=util.C_DIPL)
    ax.set_xticks(x); ax.set_xticklabels([n.replace(" ", "\n") for n in dt["phase"]], fontsize=8.5)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=8.5)
    ax.set_title("B. Regime to regime: the tracks shift together", loc="left", fontweight="bold")
    util.savefig(fig, "fig6_diplomacy")
    plt.close(fig)

    print("\n=== FINDING 5 ===")
    print(f"  weekly r = {r_w:.2f} (n.s.); Kruskal-Wallis diplomacy across phases p = {kd.pvalue:.2e}")


if __name__ == "__main__":
    main()
