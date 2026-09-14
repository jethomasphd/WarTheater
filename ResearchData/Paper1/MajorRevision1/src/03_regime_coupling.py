#!/usr/bin/env python3
"""
03 — FINDING 2: the same-day coupling switches on and off with the political regime.

Same-day correlation by phase — strong in combat, statistically absent in the ceasefire,
back at the resumption — with Fisher r-to-z comparisons between phases (Holm-adjusted for
the three pairwise tests) and a rolling 21-day correlation.

Outputs
  output/tables/t03_regime_coupling.csv     r, 95% CI, p by phase
  output/tables/t03_fisher_pairwise.csv     pairwise Fisher z tests (raw and Holm-adjusted p)
  output/tables/t03_rolling_r.csv           rolling 21-day correlation series
  output/figures/fig3_regime_coupling.(png|pdf)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

import util

WIN = 21


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 03 · Finding 2 — regime-contingent coupling")
    print("=" * 70)
    p = util.load_panel()

    rows, store = [], {}
    for name, lo, hi in util.PHASES:
        seg = p[(p.index >= lo) & (p.index <= hi)]
        x, y = seg["strikes"].astype(float), seg["retal"].astype(float)
        n = len(seg)
        if x.std() > 0 and y.std() > 0:
            r, pv = stats.pearsonr(x, y)
            cl, ch = util.fisher_ci(r, n)
            store[name] = (float(r), n)
            rows.append({"phase": name, "days": f"{lo}-{hi}", "n": n,
                         "pearson_r": round(r, 3), "ci95_low": round(cl, 3),
                         "ci95_high": round(ch, 3), "p_value": round(pv, 5),
                         "note": ""})
        else:
            rows.append({"phase": name, "days": f"{lo}-{hi}", "n": n,
                         "pearson_r": np.nan, "ci95_low": np.nan, "ci95_high": np.nan,
                         "p_value": np.nan, "note": "not estimable: no strikes in phase"})
    rt = pd.DataFrame(rows)
    print("\n--- Same-day coupling by phase ---")
    print(rt.to_string(index=False))
    util.write_table(rt, "t03_regime_coupling.csv")

    pairs = [("Major Combat", "First Ceasefire"),
             ("First Ceasefire", "Resumption"),
             ("Major Combat", "Resumption")]
    prow = []
    for a, b in pairs:
        (ra, na), (rb, nb) = store[a], store[b]
        z, pv = util.fisher_compare(ra, na, rb, nb)
        prow.append({"comparison": f"{a} vs {b}", "r_a": round(ra, 3), "n_a": na,
                     "r_b": round(rb, 3), "n_b": nb, "z": round(z, 3), "p_raw": round(pv, 4)})
    pt = pd.DataFrame(prow)
    pt["p_holm"] = np.round(util.holm(pt["p_raw"].values), 4)
    print("\n--- Fisher r-to-z comparisons ---")
    print(pt.to_string(index=False))
    util.write_table(pt, "t03_fisher_pairwise.csv")

    # rolling correlation
    s, r_ = p["strikes"].astype(float), p["retal"].astype(float)
    roll = s.rolling(WIN, center=True).corr(r_)
    util.write_table(pd.DataFrame({"day": p.index, "rolling_r_21d": np.round(roll.values, 3)}),
                     "t03_rolling_r.csv")

    # ---- Figure 3 -------------------------------------------------------- #
    util.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.9), gridspec_kw={"width_ratios": [1.7, 1]})
    ax = axes[0]
    util.shade_phases(ax)
    ax.axhline(0, color="0.6", lw=0.8)
    ax.plot(p.index, roll, color=util.C_ACCENT, lw=2.0)
    ax.set_ylim(-1.05, 1.05)
    util.label_phases(ax, 0.93)
    ax.set_xlabel("Day of conflict (centre of 21-day window)")
    ax.set_ylabel("Same-day correlation\n(strikes, retaliation)")
    ax.set_title("A. Rolling 21-day same-day correlation", loc="left", fontweight="bold")

    ax = axes[1]
    est = rt[rt["pearson_r"].notna()]
    xs = np.arange(len(est))
    ax.axhline(0, color="0.6", lw=0.8)
    ax.errorbar(xs, est["pearson_r"], yerr=[est["pearson_r"] - est["ci95_low"],
                                             est["ci95_high"] - est["pearson_r"]],
                fmt="o", color=util.C_ACCENT, ecolor=util.C_ACCENT, capsize=4, ms=7, lw=1.5)
    for i, (_, row) in enumerate(est.iterrows()):
        ax.text(i, row["ci95_high"] + 0.05, f"r = {row['pearson_r']:.2f}\n(n = {row['n']})",
                ha="center", fontsize=8.2)
    ax.set_xticks(xs)
    ax.set_xticklabels([n.replace(" ", "\n") for n in est["phase"]], fontsize=8.5)
    ax.set_xlim(-0.6, len(est) - 0.4)
    ax.set_ylim(-0.35, 1.25)
    ax.set_ylabel("Same-day correlation (95% CI)")
    ax.set_title("B. By phase", loc="left", fontweight="bold")
    util.savefig(fig, "fig3_regime_coupling")
    plt.close(fig)

    print("\n=== FINDING 2 ===")
    print("  " + " | ".join(f"{k}: r={v[0]:.2f} (n={v[1]})" for k, v in store.items()))
    print(f"  combat vs ceasefire: z={pt.loc[0,'z']}, p={pt.loc[0,'p_raw']}")


if __name__ == "__main__":
    main()
