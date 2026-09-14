#!/usr/bin/env python3
"""
07 — Regimes recovered from the data, plus the placebo check a referee will ask for.

Part A. Bai–Perron change-in-mean detection on the daily strike series (exact dynamic
programme, minimum segment 6 days, number of segments chosen by BIC as in the parent paper).
The three documented macro-transitions (Days 41, 130, 153) are recovered to within 1, 1 and
6 days without the detector being told where to look.

Part B. Is "six regimes" structure or noise? Two placebo nulls, each run 1,000 times with
a fixed seed, ask how often the same detector finds as much structure when there is none:
  (1) Shuffle placebo   — the 170 daily values are randomly re-ordered, destroying all time
                          structure but keeping the exact marginal distribution of counts.
  (2) Persistent placebo — a stationary Gaussian AR(1) series with the observed mean,
                          variance and lag-1 autocorrelation (0.71) is simulated. This null
                          has strong day-to-day persistence but no level shifts; because the
                          autocorrelation is estimated on a series that does have shifts,
                          the null is conservative (persistence is over-stated).
For each placebo we record the number of segments BIC selects and the BIC improvement of
the selected model over a single regime, and compare with the observed improvement.

Part C. Stability of the break dates under stricter penalties (Yao/Bai–Perron BIC that
counts break dates as parameters; the Liu–Wu–Zidek criterion) and longer minimum segment
lengths, and replication on the retaliation and combined series.

Outputs
  output/tables/t07_break_selection.csv    BIC by K (parent criterion), strike series
  output/tables/t07_breakpoints.csv        detected vs documented boundaries
  output/tables/t07_placebo_summary.csv    placebo results (both nulls)
  output/tables/t07_placebo_draws.csv      per-draw K and BIC gain (both nulls)
  output/tables/t07_sensitivity.csv        break days by penalty x minimum segment length
  output/tables/t07_other_series.csv       detector applied to retaliation and combined series
  output/figures/fig7_breaks_placebo.(png|pdf)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import util

MIN_SEG = 6
MAX_K = 6
N_PLACEBO = 1000


def gain_of(rows, best):
    return rows[0]["ic"] - best["ic"]


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 07 · Regime detection and placebo check")
    print("=" * 70)
    rng = np.random.default_rng(util.SEED)
    p = util.load_panel()
    x = p["strikes"].astype(float).values
    n = len(x)

    # ---- Part A: observed detection ------------------------------------- #
    rows, best = util.select_segments(x, MIN_SEG, MAX_K, "parent")
    sel = pd.DataFrame([{"n_segments": r["n_segments"], "n_breaks": r["n_breaks"],
                         "sse": round(r["sse"], 1), "bic": round(r["ic"], 2),
                         "break_days": ",".join(map(str, r["break_days"]))} for r in rows])
    print("\n--- BIC by number of segments (strike tempo) ---")
    print(sel.to_string(index=False))
    util.write_table(sel, "t07_break_selection.csv")
    obs_k = best["n_segments"]; obs_breaks = best["break_days"]; obs_gain = gain_of(rows, best)
    print(f"\nBIC-optimal: {obs_k} segments, breaks at days {obs_breaks}; "
          f"BIC gain over one regime = {obs_gain:.1f}")

    mrows = []
    for bd in obs_breaks:
        nearest = min(util.DOCUMENTED_BREAKS, key=lambda d: abs(d - bd))
        mrows.append({"detected_break_day": bd, "detected_date": util.date_from_day(bd).isoformat(),
                      "nearest_documented_boundary": nearest, "gap_days": bd - nearest,
                      "macro_transition": abs(bd - nearest) <= 7})
    mt = pd.DataFrame(mrows)
    print("\n--- Detected breaks vs documented phase boundaries ---")
    print(mt.to_string(index=False))
    util.write_table(mt, "t07_breakpoints.csv")

    # ---- Part B: placebo nulls ------------------------------------------ #
    mu, sd = x.mean(), x.std(ddof=1)
    phi = float(pd.Series(x).autocorr(1))            # lag-1 autocorrelation, whole series
    # within-regime persistence: lag-1 autocorrelation after removing each documented
    # phase's mean (the persistence that remains once the level shifts are taken out)
    xd = pd.Series(x, index=p.index).astype(float)
    for name in util.PHASE_ORDER:
        idx = util.phase_slice(p, name).index
        xd.loc[idx] = xd.loc[idx] - xd.loc[idx].mean()
    phi_within = float(xd.autocorr(1))
    draws = []
    print(f"\n--- Placebo nulls ({N_PLACEBO} draws each; seed {util.SEED}) ---")
    print(f"    lag-1 autocorrelation: whole series {phi:.2f}; within regimes {phi_within:.2f}")
    for null in ("shuffle", "ar1", "ar1_within"):
        ph = phi if null == "ar1" else phi_within
        for b in range(N_PLACEBO):
            if null == "shuffle":
                z = rng.permutation(x)
            else:
                e = rng.normal(0.0, sd * np.sqrt(1 - ph ** 2), n + 200)
                z = np.empty(n + 200); z[0] = e[0]
                for t in range(1, n + 200):
                    z[t] = ph * z[t - 1] + e[t]
                z = z[200:] + mu
            r_, b_ = util.select_segments(z, MIN_SEG, MAX_K, "parent")
            gain6 = r_[0]["ic"] - r_[MAX_K - 1]["ic"]
            draws.append({"null": null, "draw": b, "k_selected": b_["n_segments"],
                          "bic_gain_selected": gain_of(r_, b_), "bic_gain_k6": gain6})
    dd = pd.DataFrame(draws)
    util.write_table(dd.round(3), "t07_placebo_draws.csv")

    srows = []
    for null, lab in [("shuffle", "shuffled days (no time structure)"),
                      ("ar1", f"persistent AR(1), phi={phi:.2f} (whole-series), no level shifts"),
                      ("ar1_within", f"persistent AR(1), phi={phi_within:.2f} (within-regime), no level shifts")]:
        d = dd[dd["null"] == null]
        srows.append({
            "null": lab, "n_draws": len(d),
            "observed_k": obs_k, "observed_bic_gain": round(obs_gain, 1),
            "share_selecting_k1": round((d["k_selected"] == 1).mean(), 3),
            "share_selecting_k6": round((d["k_selected"] == MAX_K).mean(), 3),
            "median_k_selected": float(d["k_selected"].median()),
            "median_bic_gain": round(float(d["bic_gain_selected"].median()), 1),
            "p95_bic_gain": round(float(d["bic_gain_selected"].quantile(0.95)), 1),
            "max_bic_gain": round(float(d["bic_gain_selected"].max()), 1),
            "p_value_gain_ge_observed":
                round(float(((d["bic_gain_selected"] >= obs_gain).sum() + 1) / (len(d) + 1)), 4),
        })
    st = pd.DataFrame(srows)
    print(st.to_string(index=False))
    util.write_table(st, "t07_placebo_summary.csv")

    # ---- Part C: sensitivity of the break dates ------------------------- #
    srow = []
    for crit in ("parent", "yao", "lwz"):
        for ms in (6, 8, 10, 14):
            _, b_ = util.select_segments(x, ms, MAX_K, crit)
            bd = b_["break_days"]
            macro = [any(abs(d - m) <= 7 for d in bd) for m in util.DOCUMENTED_BREAKS]
            srow.append({"criterion": crit, "min_segment_days": ms, "k_selected": b_["n_segments"],
                         "break_days": ",".join(map(str, bd)),
                         "recovers_day41": macro[0], "recovers_day130": macro[1],
                         "recovers_day153": macro[2],
                         "n_macro_recovered_within_7d": int(sum(macro))})
    sens = pd.DataFrame(srow)
    print("\n--- Break dates by criterion x minimum segment length ---")
    print(sens.to_string(index=False))
    util.write_table(sens, "t07_sensitivity.csv")

    orow = []
    for label, series in [("strikes", x), ("retal", p["retal"].astype(float).values),
                          ("strikes + retal", (p["strikes"] + p["retal"]).astype(float).values)]:
        _, b_ = util.select_segments(series, MIN_SEG, MAX_K, "parent")
        bd = b_["break_days"]
        macro = [any(abs(d - m) <= 7 for d in bd) for m in util.DOCUMENTED_BREAKS]
        orow.append({"series": label, "k_selected": b_["n_segments"],
                     "break_days": ",".join(map(str, bd)),
                     "n_macro_recovered_within_7d": int(sum(macro))})
    ot = pd.DataFrame(orow)
    print("\n--- Detector applied to other series (parent BIC, min segment 6) ---")
    print(ot.to_string(index=False))
    util.write_table(ot, "t07_other_series.csv")

    # ---- Figure 7 -------------------------------------------------------- #
    util.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 4.0), gridspec_kw={"width_ratios": [1.5, 1]})
    ax = axes[0]
    days = p.index.values
    ax.plot(days, x, color=util.C_STRIKE, lw=1.1, alpha=0.7, label="strike tempo")
    edges = [0] + [b - 1 for b in obs_breaks] + [n]
    for a, b in zip(edges[:-1], edges[1:]):
        ax.hlines(x[a:b].mean(), a + 0.5, b + 0.5, color=util.C_RETAL, lw=2.6, zorder=5)
    for bd in obs_breaks:
        ax.axvline(bd, color=util.C_RETAL, lw=1.0, alpha=0.6)
    for d in util.DOCUMENTED_BREAKS:
        ax.axvline(d, color="0.3", ls="--", lw=1.0, alpha=0.9)
    ax.plot([], [], color=util.C_RETAL, lw=2.6, label="detected regime mean")
    ax.plot([], [], color="0.3", ls="--", label="documented boundary")
    ax.set_xlabel("Day of conflict"); ax.set_ylabel("Strikes per day")
    ax.set_title(f"A. {obs_k} regimes found by BIC; breaks at days {', '.join(map(str, obs_breaks))}",
                 loc="left", fontweight="bold", fontsize=9.6)
    ax.legend(loc="upper right", fontsize=8.2)

    ax = axes[1]
    for null, col, lab in [("shuffle", util.C_GREY, "shuffled-days placebo"),
                           ("ar1_within", util.C_DIPL, f"AR(1) placebo, within-regime φ = {phi_within:.2f}"),
                           ("ar1", util.C_GOLD, f"AR(1) placebo, whole-series φ = {phi:.2f}")]:
        ax.hist(dd[dd["null"] == null]["bic_gain_selected"], bins=30, alpha=0.55, color=col, label=lab)
    ax.axvline(obs_gain, color=util.C_RETAL, lw=2.0)
    ax.text(obs_gain - 3, ax.get_ylim()[1] * 0.45, f"observed\ngain = {obs_gain:.0f}", color=util.C_RETAL,
            fontsize=8.6, ha="right", va="center")
    ax.set_xlabel("BIC improvement over a single regime")
    ax.set_ylabel(f"Placebo draws (of {N_PLACEBO})")
    ax.set_title("B. How much structure does noise produce?", loc="left", fontweight="bold", fontsize=9.6)
    ax.legend(loc="upper center", fontsize=8.0, bbox_to_anchor=(0.56, 0.98))
    util.savefig(fig, "fig7_breaks_placebo")
    plt.close(fig)

    print("\n=== BREAKS / PLACEBO ===")
    for _, r in st.iterrows():
        print(f"  {r['null']}: median K={r['median_k_selected']}, share K=6: {r['share_selecting_k6']}, "
              f"max gain {r['max_bic_gain']} vs observed {r['observed_bic_gain']} (p={r['p_value_gain_ge_observed']})")


if __name__ == "__main__":
    main()
