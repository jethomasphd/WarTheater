#!/usr/bin/env python3
"""
04 — Mediation: does civilian-facing targeting carry the association between
military strike tempo and civilian deaths?

Model (single-mediator, day-level):
  X = strikes_milfac   (military-facing strike locations/day)
  M = strikes_civfac   (civilian-facing strike locations/day)
  Y = iran_civ         (Iranian civilian estimated killed/day)

Estimation: product-of-coefficients (a*b) with a seeded nonparametric
percentile bootstrap (10,000 resamples of days), plus the Sobel test for
reference. Estimated on the full sample and Major Combat only, and for the
secondary outcome killed_total.

The temporal-spillover logic: days of heavier military-target tempo are days
when the target set widens into civilian-facing infrastructure; the mediation
test asks whether that widening statistically carries the tempo-mortality
association. Same-day measurement means this is an associational
decomposition, not a causal identification (see METHODS §7).

Outputs:
  output/tables/t04_mediation.csv
  output/figures/fig5_mediation_paths.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

import util

N_BOOT = 10_000


def paths(x, m, y):
    """Return (a, b, c, c_prime) from the two mediation regressions."""
    Xa = sm.add_constant(x)
    a = np.asarray(sm.OLS(m, Xa).fit().params)[1]
    Xc = sm.add_constant(x)
    c = np.asarray(sm.OLS(y, Xc).fit().params)[1]
    Xb = sm.add_constant(np.column_stack([x, m]))
    fb = sm.OLS(y, Xb).fit()
    c_prime, b = np.asarray(fb.params)[1], np.asarray(fb.params)[2]
    return a, b, c, c_prime


def sobel(x, m, y):
    Xa = sm.add_constant(x)
    fa = sm.OLS(m, Xa).fit()
    a, sa = np.asarray(fa.params)[1], np.asarray(fa.bse)[1]
    Xb = sm.add_constant(np.column_stack([x, m]))
    fb = sm.OLS(y, Xb).fit()
    b, sb = np.asarray(fb.params)[2], np.asarray(fb.bse)[2]
    se = np.sqrt(b ** 2 * sa ** 2 + a ** 2 * sb ** 2)
    z = a * b / se
    from scipy import stats
    return z, 2 * stats.norm.sf(abs(z))


def run_mediation(d: pd.DataFrame, outcome: str, sample: str) -> dict:
    x = d["strikes_milfac"].values.astype(float)
    m = d["strikes_civfac"].values.astype(float)
    y = d[outcome].values.astype(float)
    n = len(d)

    a, b, c, c_prime = paths(x, m, y)
    ab = a * b
    z, p_sobel = sobel(x, m, y)

    rng = np.random.default_rng(util.SEED)
    boots = np.empty(N_BOOT)
    for i in range(N_BOOT):
        idx = rng.integers(0, n, n)
        ba, bb, _, _ = paths(x[idx], m[idx], y[idx])
        boots[i] = ba * bb
    lo, hi = np.percentile(boots, [2.5, 97.5])

    return {
        "sample": sample, "outcome": outcome, "n_days": n,
        "a_X_to_M": a, "b_M_to_Y": b, "c_total": c, "c_prime_direct": c_prime,
        "indirect_ab": ab, "boot_ci_lo": lo, "boot_ci_hi": hi,
        "boot_significant": bool(lo > 0 or hi < 0),
        "sobel_z": z, "sobel_p": p_sobel,
        "prop_mediated": ab / c if c else np.nan,
        "n_boot": N_BOOT, "seed": util.SEED,
    }


def main():
    util.apply_style()
    p = util.load_panel()
    combat = p.loc[1:40]

    results = [
        run_mediation(p, "iran_civ", "full"),
        run_mediation(combat, "iran_civ", "major_combat"),
        run_mediation(p, "killed_total", "full"),
        run_mediation(combat, "killed_total", "major_combat"),
    ]
    t04 = pd.DataFrame(results)
    t04.round(5).to_csv(util.TAB_DIR / "t04_mediation.csv", index=False)
    print("t04_mediation:")
    print(t04[["sample", "outcome", "a_X_to_M", "b_M_to_Y", "c_total",
               "c_prime_direct", "indirect_ab", "boot_ci_lo", "boot_ci_hi",
               "prop_mediated"]].round(3).to_string(index=False))

    # ---------------- Figure 5: annotated path diagram -------------------- #
    r = results[0]   # full sample, iran_civ — the headline model
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.axis("off")

    def box(xy, text):
        ax.annotate(text, xy, ha="center", va="center", fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.55", fc="#F2F6FB",
                              ec="0.35", lw=1.1))

    box((0.12, 0.28), "Military-facing\nstrike tempo\n(X)")
    box((0.50, 0.80), "Civilian-facing\nstrike tempo\n(M)")
    box((0.88, 0.28), "Iranian civilian\ndeaths/day\n(Y)")

    arrow = dict(arrowstyle="-|>", lw=1.6, color="0.25",
                 shrinkA=32, shrinkB=32)
    ax.annotate("", (0.50, 0.80), (0.12, 0.28), arrowprops=arrow)
    ax.annotate("", (0.88, 0.28), (0.50, 0.80), arrowprops=arrow)
    ax.annotate("", (0.88, 0.28), (0.12, 0.28), arrowprops=arrow)

    ax.text(0.245, 0.62, f"a = {r['a_X_to_M']:.3f}", fontsize=10,
            style="italic", ha="center")
    ax.text(0.755, 0.62, f"b = {r['b_M_to_Y']:.3f}", fontsize=10,
            style="italic", ha="center")
    ax.text(0.50, 0.205, f"c′ = {r['c_prime_direct']:.3f}   "
                          f"(c = {r['c_total']:.3f})", fontsize=10,
            style="italic", ha="center")
    ax.text(0.50, 0.035,
            f"Indirect effect a×b = {r['indirect_ab']:.3f}, "
            f"95% bootstrap CI [{r['boot_ci_lo']:.3f}, {r['boot_ci_hi']:.3f}]  "
            f"({N_BOOT:,} resamples, seed {util.SEED})",
            fontsize=9, ha="center", color="0.2")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Mediation: military tempo → civilian-facing targeting → "
                 "civilian deaths (full sample, Days 1–170)",
                 fontsize=10.5, loc="left", fontweight="bold")
    util.savefig(fig, "fig5_mediation_paths")
    plt.close(fig)

    print("\nwrote t04_mediation.csv + fig5")


if __name__ == "__main__":
    main()
