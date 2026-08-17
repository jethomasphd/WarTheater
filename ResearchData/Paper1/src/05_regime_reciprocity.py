#!/usr/bin/env python3
"""
05 — Regime-dependent reciprocity and escalation asymmetry.

Questions:
  (a) Does the strike-retaliation coupling differ across the war's regimes?
  (b) Who drives escalation — is the relationship symmetric, or does one side
      set the tempo (asymmetric escalation)?
  (c) Is the full-sample "retaliation Granger-causes strikes" result (step 03)
      robust within regimes, or an artifact of the between-regime structure?

Methods:
  - Per-phase contemporaneous correlation + within-phase Granger (small-lag VAR).
  - Fisher r-to-z test comparing the combat vs. ceasefire coupling.
  - Rolling 21-day contemporaneous correlation (figure).
  - Escalation asymmetry: strike/retaliation ratio and lead-lag sign by phase.

Outputs:
  output/tables/t05_regime_reciprocity.csv
  output/tables/t05_asymmetry.csv
  output/figures/fig5_rolling_coupling.(png|pdf)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.api import VAR

import util

VARS = ["strikes", "retal"]


def fisher_z(r, n):
    return np.arctanh(r), 1.0 / np.sqrt(n - 3)


def compare_corr(r1, n1, r2, n2):
    """Two-sided Fisher r-to-z test that two correlations are equal."""
    z1, se1 = fisher_z(r1, n1)
    z2, se2 = fisher_z(r2, n2)
    z = (z1 - z2) / np.sqrt(se1 ** 2 + se2 ** 2)
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p


def within_granger(seg: pd.DataFrame, maxlag: int):
    """Return dict of Granger p-values in both directions for a phase segment."""
    data = seg[VARS].astype(float)
    if len(data) < 20 or data["strikes"].std() == 0 or data["retal"].std() == 0:
        return {"lag": None, "p_s_to_r": None, "p_r_to_s": None}
    try:
        m = VAR(data)
        sel = m.select_order(maxlag)
        p = int(sel.selected_orders.get("bic", 1)) or 1
        p = min(p, maxlag)
        res = m.fit(p)
        p_sr = float(res.test_causality("retal", ["strikes"], kind="f").pvalue)
        p_rs = float(res.test_causality("strikes", ["retal"], kind="f").pvalue)
        return {"lag": p, "p_s_to_r": round(p_sr, 4), "p_r_to_s": round(p_rs, 4)}
    except Exception as e:
        return {"lag": None, "p_s_to_r": None, "p_r_to_s": None, "err": str(e)}


def lead_lag_sign(seg: pd.DataFrame):
    """Cross-correlation at +/-1 day: does strike lead retaliation (+) or retal
    lead strike (-)? Returns (ccf_strike_leads, ccf_retal_leads)."""
    s = seg["strikes"].astype(float).values
    r = seg["retal"].astype(float).values
    if s.std() == 0 or r.std() == 0 or len(s) < 4:
        return (np.nan, np.nan)
    s = s - s.mean(); r = r - r.mean()
    strike_leads = np.corrcoef(s[:-1], r[1:])[0, 1]   # strike_t vs retal_{t+1}
    retal_leads = np.corrcoef(r[:-1], s[1:])[0, 1]    # retal_t  vs strike_{t+1}
    return (strike_leads, retal_leads)


def main():
    print("=" * 68)
    print("Paper 1 · Step 05 · Regime-dependent reciprocity & asymmetry")
    print("=" * 68)
    p = util.load_panel()

    rows, arows = [], []
    corr_store = {}
    for name, lo, hi in util.PHASES:
        seg = p[(p.index >= lo) & (p.index <= hi)]
        n = len(seg)
        x, y = seg["strikes"].astype(float), seg["retal"].astype(float)
        if x.std() > 0 and y.std() > 0:
            r, pr = stats.pearsonr(x, y)
        else:
            r, pr = np.nan, np.nan
        corr_store[name] = (r, n)
        gc = within_granger(seg, maxlag=min(4, n // 8))
        rows.append({
            "phase": name, "days": f"{lo}-{hi}", "n": n,
            "contemp_r": round(r, 3) if r == r else None,
            "contemp_p": round(pr, 5) if pr == pr else None,
            "granger_lag": gc["lag"],
            "p_strikes->retal": gc["p_s_to_r"],
            "p_retal->strikes": gc["p_r_to_s"],
        })
        sl, rl = lead_lag_sign(seg)
        arows.append({
            "phase": name, "days": f"{lo}-{hi}",
            "strikes_per_day": round(seg["strikes"].mean(), 2),
            "retal_per_day": round(seg["retal"].mean(), 2),
            "strike_retal_ratio": round(seg["strikes"].sum() / max(seg["retal"].sum(), 1), 3),
            "ccf_strike_leads_r+1": round(sl, 3) if sl == sl else None,
            "ccf_retal_leads_s+1": round(rl, 3) if rl == rl else None,
        })

    rt = pd.DataFrame(rows)
    at = pd.DataFrame(arows)
    rt.to_csv(util.TAB_DIR / "t05_regime_reciprocity.csv", index=False)
    at.to_csv(util.TAB_DIR / "t05_asymmetry.csv", index=False)
    print("\n--- Regime reciprocity ---")
    print(rt.to_string(index=False))
    print("\n--- Escalation asymmetry by phase ---")
    print(at.to_string(index=False))

    # Fisher r-to-z: combat vs ceasefire coupling
    (rc, nc) = corr_store["Major Combat"]
    (rf, nf) = corr_store["First Ceasefire"]
    z, pz = compare_corr(rc, nc, rf, nf)
    print(f"\nFisher r-to-z: combat r={rc:.3f} (n={nc}) vs ceasefire r={rf:.3f} "
          f"(n={nf}) -> z={z:.3f}, p={pz:.4f}")
    pd.DataFrame([{
        "comparison": "combat vs ceasefire contemporaneous coupling",
        "r_combat": round(rc, 3), "n_combat": nc,
        "r_ceasefire": round(rf, 3), "n_ceasefire": nf,
        "z": round(z, 3), "p_value": round(pz, 4),
    }]).to_csv(util.TAB_DIR / "t05_coupling_compare.csv", index=False)

    # ---------------- rolling coupling figure --------------------------- #
    win = 21
    s = p["strikes"].astype(float)
    r = p["retal"].astype(float)
    roll = s.rolling(win, center=True).corr(r)
    util.apply_style()
    fig, ax = plt.subplots(figsize=(9.2, 3.9))
    util.shade_phases(ax)
    ax.axhline(0, color="0.6", lw=0.8)
    ax.plot(p.index, roll, color=util.C_ACCENT, lw=2.0)
    ax.set_ylim(-1.05, 1.05)
    ax.set_xlabel("Day of conflict (center of 21-day window)")
    ax.set_ylabel("Contemporaneous\ncorrelation (strikes, retal)")
    ax.set_title("Rolling strike–retaliation coupling (21-day window)",
                 loc="left", fontweight="bold")
    for name, lo, hi in util.PHASES:
        ax.text((lo + hi) / 2, 0.92, name.upper(), fontsize=6.8, color="0.35",
                ha="center", va="center")
    util.savefig(fig, "fig5_rolling_coupling")
    plt.close(fig)
    print(f"\nWrote tables + fig5 to {util.OUT_DIR}")


if __name__ == "__main__":
    main()
