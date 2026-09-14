#!/usr/bin/env python3
"""
04 — FINDING 3: "who set the tempo" in open combat is not identified at daily resolution.

A forecast-error variance decomposition (FEVD) splits the uncertainty in each series into
the part attributable to shocks in each series. When two series move together within the
same day, the decomposition must first decide which one moved first inside the day (the
Cholesky ordering). That decision is an assumption, not a finding. Here the answer flips
completely with the ordering, which is the paper's methodological contribution: the shared
same-day variance (the squared residual correlation) is handed to whichever series is
ordered first.

Outputs
  output/tables/t04_fevd_orderings.csv   FEVD shares at horizons 1, 6, 12 under both orderings
  output/tables/t04_residual_corr.csv    residual correlation and its square (the shared share)
  output/figures/fig4_identification.(png|pdf)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import VAR

import util

H = 12
VARS = ["strikes", "retal"]
LABEL = {"strikes": "strikes", "retal": "retaliation"}


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 04 · Finding 3 — under-identification (FEVD reversal)")
    print("=" * 70)
    p = util.load_panel()
    combat = p.loc[p.index <= util.KINETIC_END, VARS].astype(float)

    rows, cross = [], {}
    for ordering in (VARS, VARS[::-1]):
        res = VAR(combat[ordering]).fit(1)
        dec = res.fevd(H).decomp          # [variable, horizon, shock]
        olab = " first".join(["", ""]).join([LABEL[ordering[0]]]) + " first"
        for i, vi in enumerate(ordering):
            for j, vj in enumerate(ordering):
                row = {"ordering": f"{LABEL[ordering[0]]} first, then {LABEL[ordering[1]]}",
                       "variable": vi, "shock_source": vj,
                       "share_h1": round(float(dec[i, 0, j]), 3),
                       "share_h6": round(float(dec[i, 5, j]), 3),
                       "share_h12": round(float(dec[i, H - 1, j]), 3)}
                rows.append(row)
                if vi != vj:
                    cross[(ordering[0], vi, vj)] = float(dec[i, H - 1, j])
        rc = float(res.resid_corr[0, 1])
    ft = pd.DataFrame(rows)
    print("\n--- FEVD under both orderings (combat, VAR(1)) ---")
    print(ft.to_string(index=False))
    util.write_table(ft, "t04_fevd_orderings.csv")

    rr = pd.DataFrame([{"sample": "combat (Days 1-40), VAR(1)",
                        "residual_correlation": round(rc, 3),
                        "shared_same_day_share_rho2": round(rc ** 2, 3),
                        "note": "rho^2 equals the h=1 share credited to whichever series is "
                                "ordered first"}])
    print("\n--- Residual correlation ---")
    print(rr.to_string(index=False))
    util.write_table(rr, "t04_residual_corr.csv")

    # cross-explained shares at h=12 for the figure/text
    s_first_s_to_r = cross[("strikes", "retal", "strikes")]     # strikes first: strike shocks -> retal var
    s_first_r_to_s = cross[("strikes", "strikes", "retal")]     # strikes first: retal shocks -> strikes var
    r_first_r_to_s = cross[("retal", "strikes", "retal")]       # retal first: retal shocks -> strikes var
    r_first_s_to_r = cross[("retal", "retal", "strikes")]       # retal first: strike shocks -> retal var

    util.apply_style()
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    groups = ["Strikes ordered first", "Retaliation ordered first"]
    a = [100 * s_first_s_to_r, 100 * r_first_s_to_r]   # strike shocks -> retaliation variance
    b = [100 * s_first_r_to_s, 100 * r_first_r_to_s]   # retaliation shocks -> strikes variance
    x = np.arange(2); w = 0.36
    ax.bar(x - w / 2, a, w, color=util.C_STRIKE, label="strike shocks → share of retaliation variance")
    ax.bar(x + w / 2, b, w, color=util.C_RETAL, label="retaliation shocks → share of strike variance")
    pct = lambda v: f"{v:.1f}%" if v < 5 else f"{v:.0f}%"
    for xi, v in zip(x - w / 2, a):
        ax.text(xi, v + 1.2, pct(v), ha="center", fontsize=9.5)
    for xi, v in zip(x + w / 2, b):
        ax.text(xi, v + 1.2, pct(v), ha="center", fontsize=9.5)
    ax.set_xticks(x); ax.set_xticklabels(groups)
    ax.set_ylabel("Share of 12-day forecast-error variance (%)")
    ax.set_ylim(0, 58)
    ax.set_title("Which side 'explains' the other depends only on the ordering assumption "
                 f"(shared same-day variance ρ² = {rc**2:.2f})", loc="left", fontweight="bold",
                 fontsize=9.6)
    ax.legend(loc="upper center", ncol=2, fontsize=8.4, bbox_to_anchor=(0.5, -0.16))
    util.savefig(fig, "fig4_identification")
    plt.close(fig)

    print("\n=== FINDING 3 ===")
    print(f"  strikes first : strike→retal {100*s_first_s_to_r:.0f}%  vs  retal→strikes {100*s_first_r_to_s:.1f}%")
    print(f"  retal first   : retal→strikes {100*r_first_r_to_s:.0f}%  vs  strike→retal {100*r_first_s_to_r:.1f}%")
    print(f"  residual corr = {rc:.3f}; rho^2 = {rc**2:.3f}")


if __name__ == "__main__":
    main()
