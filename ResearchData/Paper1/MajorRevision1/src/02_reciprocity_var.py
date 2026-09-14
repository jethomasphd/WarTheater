#!/usr/bin/env python3
"""
02 — FINDING 1: reciprocity is same-day, not lagged.

In the sustained-combat regime (Days 1-40) the strike and retaliation series are strongly
correlated on the same day, yet every information criterion selects a zero-lag VAR and
no daily-lag Granger causality is present in either direction. The exchange runs faster
than the day.

Method, in plain terms
  * Same-day correlation: do the two series rise and fall together within the day?
  * Cross-correlation function: does the association peak at lag 0 or at some lag?
  * VAR lag selection (AIC/BIC/HQIC/FPE): how many days of history help predict today?
  * Granger causality (F-test on a VAR(1)): does yesterday's retaliation help predict
    today's strikes once today's own history is accounted for, and vice versa?
  * Orthogonalised impulse responses with seeded Monte-Carlo bands (appendix figure).

Outputs
  output/tables/t02_same_day.csv        same-day r with 95% CI (combat, full)
  output/tables/t02_lag_selection.csv   selected lag by each criterion
  output/tables/t02_granger.csv         Granger tests (combat VAR(1); full-sample naive)
  output/tables/t02_ccf_combat.csv      cross-correlation function, combat, lags -5..+5
  output/tables/t02_irf_summary.csv     impact and cumulative responses (combat)
  output/tables/t02_var_combat_summary.txt
  output/figures/fig2_same_day.(png|pdf)
  output/figures/figA1_irf_combat.(png|pdf)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.api import VAR

import util

H = 12
VARS = ["strikes", "retal"]
NAMES = {"strikes": "US/Israeli strikes", "retal": "Iranian retaliation"}


def mc_errband(res, steps: int, repl: int, seed: int, signif: float = 0.05):
    """Seeded Monte-Carlo error band for the orthogonalised impulse responses.

    Mirrors statsmodels' VARResults.irf_resim, but draws a fresh seed for every
    replication from one seeded generator. (statsmodels' errband_mc passes the same
    seed to every replication, which makes all simulated series identical and
    collapses the band to a line; the parent paper's Figure 3 inherited that defect.)
    Returns (lower, upper), each of shape (steps+1, k, k)."""
    from statsmodels.tsa.vector_ar import util as var_util
    rng = np.random.default_rng(seed)
    k_ar, neqs, nobs = res.k_ar, res.neqs, res.nobs
    burn = 100
    coll = np.zeros((repl, steps + 1, neqs, neqs))
    for i in range(repl):
        sim = var_util.varsim(res.coefs, res.intercept, res.sigma_u,
                              seed=int(rng.integers(0, 2**31 - 1)),
                              steps=nobs + k_ar + burn, initial_values=res.endog[:k_ar])
        sim = sim[burn:]
        fit = VAR(sim).fit(maxlags=k_ar, trend=res.trend)
        coll[i] = fit.orth_ma_rep(maxn=steps)
    lower = np.percentile(coll, 100 * signif / 2, axis=0)
    upper = np.percentile(coll, 100 * (1 - signif / 2), axis=0)
    return lower, upper


def granger_rows(res, label, lag, n_obs):
    out = []
    for cause, effect in [("strikes", "retal"), ("retal", "strikes")]:
        gc = res.test_causality(effect, [cause], kind="f")
        out.append({"sample": label, "lag": lag, "n_obs_used": n_obs,
                    "direction": f"{cause} -> {effect}",
                    "F": round(float(gc.test_statistic), 3), "df": str(gc.df),
                    "p_value": round(float(gc.pvalue), 4),
                    "significant_05": bool(gc.pvalue < 0.05)})
    return out


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 02 · Finding 1 — same-day reciprocity")
    print("=" * 70)
    np.random.seed(util.SEED)
    p = util.load_panel()
    combat = p.loc[p.index <= util.KINETIC_END, VARS].astype(float)
    full = p[VARS].astype(float)

    # ---- same-day correlation ------------------------------------------ #
    rows = []
    for label, d in [("combat (Days 1-40)", combat), ("full (Days 1-170)", full)]:
        r, pv = stats.pearsonr(d["strikes"], d["retal"])
        lo, hi = util.fisher_ci(r, len(d))
        rows.append({"sample": label, "n": len(d), "pearson_r": round(r, 3),
                     "ci95_low": round(lo, 3), "ci95_high": round(hi, 3),
                     "p_value": float(f"{pv:.2e}")})
    sd = pd.DataFrame(rows)
    print("\n--- Same-day correlation ---")
    print(sd.to_string(index=False))
    util.write_table(sd, "t02_same_day.csv")

    # ---- lag selection --------------------------------------------------- #
    sel_c = VAR(combat).select_order(maxlags=5).selected_orders
    sel_f = VAR(full).select_order(maxlags=10).selected_orders
    ls = pd.DataFrame([
        {"sample": "combat (Days 1-40)", "maxlags": 5, **{k: int(v) for k, v in sel_c.items()}},
        {"sample": "full (Days 1-170)", "maxlags": 10, **{k: int(v) for k, v in sel_f.items()}},
    ])
    print("\n--- Lag selected by each information criterion ---")
    print(ls.to_string(index=False))
    util.write_table(ls, "t02_lag_selection.csv")

    # ---- Granger: combat VAR(1) (lag 1 = minimum feasible; criteria chose 0) ---- #
    res_c = VAR(combat).fit(1)
    g = granger_rows(res_c, "combat (Days 1-40)", 1, int(res_c.nobs))
    # naive full-sample VAR at the AIC lag, reported for the record only (see step 08)
    lag_f = max(int(sel_f["aic"]), 1)
    res_f = VAR(full).fit(lag_f)
    g += granger_rows(res_f, "full (Days 1-170), naive", lag_f, int(res_f.nobs))
    gt = pd.DataFrame(g)
    print("\n--- Granger causality ---")
    print(gt.to_string(index=False))
    util.write_table(gt, "t02_granger.csv")
    with open(util.TAB_DIR / "t02_var_combat_summary.txt", "w") as fh:
        fh.write(str(res_c.summary()))

    # ---- cross-correlation function (combat) ---------------------------- #
    lags = list(range(-5, 6))
    cc = [util.ccf(combat["strikes"], combat["retal"], k) for k in lags]
    band = 1.96 / np.sqrt(len(combat))
    ct = pd.DataFrame({"lag_days": lags, "ccf": np.round(cc, 3),
                       "outside_95_band": [abs(v) > band for v in cc]})
    ct["note"] = "lag>0: strikes lead retaliation; lag<0: retaliation leads strikes"
    print(f"\n--- Cross-correlation, combat (95% band = ±{band:.3f}) ---")
    print(ct[["lag_days", "ccf", "outside_95_band"]].to_string(index=False))
    util.write_table(ct, "t02_ccf_combat.csv")

    # ---- impulse responses (combat) ------------------------------------- #
    irf = res_c.irf(H)
    o = irf.orth_irfs                                    # (H+1, response, shock)
    lo, up = mc_errband(res_c, H, repl=1000, seed=util.SEED)
    i_r, i_s = VARS.index("retal"), VARS.index("strikes")

    def irf_row(shock, response):
        j, i = VARS.index(shock), VARS.index(response)
        # first horizon at which the 95% band includes zero
        h_zero = next((h for h in range(H + 1) if lo[h, i, j] <= 0 <= up[h, i, j]), None)
        return {"shock": shock, "response": response,
                "impact_response_h0": round(float(o[0, i, j]), 2),
                "cumulative_7day": round(float(o[:7, i, j].sum()), 2),
                "first_horizon_band_includes_zero": h_zero,
                "impact_ci95_low": round(float(lo[0, i, j]), 2),
                "impact_ci95_high": round(float(up[0, i, j]), 2)}

    # cross-responses first (the rows the manuscript cites), then own-persistence responses
    ir = pd.DataFrame([irf_row("strikes", "retal"), irf_row("retal", "strikes"),
                       irf_row("strikes", "strikes"), irf_row("retal", "retal")])
    print("\n--- Orthogonalised IRF summary (combat; strikes ordered first) ---")
    print(ir.to_string(index=False))
    util.write_table(ir, "t02_irf_summary.csv")

    # ---- Figure 2: scatter + CCF ---------------------------------------- #
    util.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.9), gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axes[0]
    ax.scatter(combat["strikes"], combat["retal"], s=34, color=util.C_ACCENT, alpha=0.8,
               edgecolor="white", lw=0.5)
    b, a = np.polyfit(combat["strikes"], combat["retal"], 1)
    xs = np.linspace(0, combat["strikes"].max(), 50)
    ax.plot(xs, a + b * xs, color="0.3", lw=1.2)
    r_c = sd.loc[0, "pearson_r"]
    ax.text(0.04, 0.95, f"same-day r = {r_c:.2f}\n(n = {len(combat)} days)", transform=ax.transAxes,
            va="top", fontsize=9.5)
    ax.set_xlabel("US/Israeli strikes that day")
    ax.set_ylabel("Iranian/proxy retaliation that day")
    ax.set_title("A. Same-day pairing, Days 1–40", loc="left", fontweight="bold")

    ax = axes[1]
    ax.axhspan(-band, band, color="0.88", alpha=0.8, label="95% band under no association")
    ax.axhline(0, color="0.5", lw=0.8)
    colors = [util.C_ACCENT if k == 0 else util.C_GREY for k in lags]
    ax.bar(lags, cc, color=colors, width=0.7)
    ax.set_xticks(lags)
    ax.set_xlabel("Lag in days  (negative: retaliation leads;  positive: strikes lead)")
    ax.set_ylabel("Correlation")
    ax.set_title("B. Association by lag, Days 1–40", loc="left", fontweight="bold")
    ax.legend(loc="lower right", fontsize=8)
    util.savefig(fig, "fig2_same_day")
    plt.close(fig)

    # ---- Appendix figure: IRF grid -------------------------------------- #
    fig, axes = plt.subplots(2, 2, figsize=(9.0, 6.0), sharex=True)
    hx = np.arange(H + 1)
    for i, vi in enumerate(VARS):
        for j, vj in enumerate(VARS):
            ax = axes[i, j]
            color = util.C_STRIKE if vj == "strikes" else util.C_RETAL
            ax.axhline(0, color="0.6", lw=0.8)
            ax.fill_between(hx, lo[:, i, j], up[:, i, j], color=color, alpha=0.18)
            ax.plot(hx, o[:, i, j], color=color, lw=2.0)
            ax.set_title(f"{NAMES[vj]} shock  →  {NAMES[vi]}", fontsize=9.5)
            if i == 1:
                ax.set_xlabel("Days after shock")
            if j == 0:
                ax.set_ylabel("Response (events/day)")
    fig.suptitle("Orthogonalised impulse responses, combat regime (Days 1–40); "
                 "shaded = 95% Monte-Carlo band", fontweight="bold", fontsize=10.5, y=1.02)
    util.savefig(fig, "figA1_irf_combat")
    plt.close(fig)

    print("\n=== FINDING 1 ===")
    print(f"  same-day r (combat) = {sd.loc[0,'pearson_r']}; lag selected: "
          f"AIC={sel_c['aic']}, BIC={sel_c['bic']}, HQIC={sel_c['hqic']}, FPE={sel_c['fpe']}")
    for _, r in gt[gt["sample"].str.startswith("combat")].iterrows():
        print(f"  Granger {r['direction']:18s} F={r['F']:.2f}  p={r['p_value']:.3f}")


if __name__ == "__main__":
    main()
