#!/usr/bin/env python3
"""
03 — Reciprocity: bivariate VAR, Granger causality, IRFs, FEVD.

Tests the action-reaction (tit-for-tat / spiral) hypothesis on the daily
strike and retaliation tempo. Primary estimation is on the active-combat regime
(Days 1-40), where both series are stationary and reciprocity is operative
(step 02); the full sample is reported as a war-average with the ceasefire break
made explicit.

Model: VAR(p) on [strikes, retal], lag p chosen by AIC (BIC reported).
  - Granger causality in both directions (F-test).
  - Orthogonalized impulse responses with Monte-Carlo 95% error bands (seeded).
  - Forecast-error variance decomposition (FEVD).
  - Contemporaneous (same-day) coupling, which the cross-correlation flags as
    dominant, is reported separately.

Outputs:
  output/tables/t03_lag_selection.csv
  output/tables/t03_granger.csv
  output/tables/t03_fevd.csv
  output/tables/t03_contemporaneous.csv
  output/figures/fig3_irf_combat.(png|pdf)
  output/tables/t03_var_combat_summary.txt
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.api import VAR

import util

SEED = 42
H = 12            # IRF / FEVD horizon (days)
MAXLAGS_COMBAT = 5
MAXLAGS_FULL = 10
VARS = ["strikes", "retal"]
NAMES = {"strikes": "US/Israeli strikes", "retal": "Iranian retaliation"}


def select_and_fit(data: pd.DataFrame, maxlags: int):
    m = VAR(data)
    sel = m.select_order(maxlags=maxlags)
    orders = sel.selected_orders
    p = int(orders.get("aic", 1)) or 1
    res = m.fit(p)
    return res, p, orders


def granger_rows(res, sample_label: str, p: int) -> list[dict]:
    out = []
    for cause, effect in [("strikes", "retal"), ("retal", "strikes")]:
        gc = res.test_causality(effect, [cause], kind="f")
        out.append({
            "sample": sample_label, "lag": p,
            "direction": f"{cause} -> {effect}",
            "F": round(float(gc.test_statistic), 3),
            "df": str(gc.df),
            "p_value": round(float(gc.pvalue), 4),
            "granger_causal_05": bool(gc.pvalue < 0.05),
        })
    return out


def contemporaneous(data: pd.DataFrame, label: str) -> dict:
    x, y = data["strikes"].astype(float), data["retal"].astype(float)
    r, p = stats.pearsonr(x, y)
    return {"sample": label, "n": len(data),
            "pearson_r": round(r, 3), "p_value": round(p, 6)}


def main():
    print("=" * 68)
    print("Paper 1 · Step 03 · Reciprocity VAR / Granger / IRF / FEVD")
    print("=" * 68)
    np.random.seed(SEED)
    p_all = util.load_panel()
    combat = p_all.loc[p_all.index <= util.KINETIC_END, VARS].astype(float)
    full = p_all[VARS].astype(float)

    # ---- fit both samples -------------------------------------------------
    res_c, lag_c, orders_c = select_and_fit(combat, MAXLAGS_COMBAT)
    res_f, lag_f, orders_f = select_and_fit(full, MAXLAGS_FULL)
    print(f"Combat regime (Days 1-{util.KINETIC_END}): VAR lag (AIC) = {lag_c}  "
          f"[selected orders: {orders_c}]")
    print(f"Full sample   (Days 1-170):    VAR lag (AIC) = {lag_f}  "
          f"[selected orders: {orders_f}]")

    pd.DataFrame([
        {"sample": f"combat (1-{util.KINETIC_END})", **{k: int(v) for k, v in orders_c.items()}},
        {"sample": "full (1-170)", **{k: int(v) for k, v in orders_f.items()}},
    ]).to_csv(util.TAB_DIR / "t03_lag_selection.csv", index=False)

    # ---- Granger causality ------------------------------------------------
    grows = granger_rows(res_c, f"combat (1-{util.KINETIC_END})", lag_c) \
        + granger_rows(res_f, "full (1-170)", lag_f)
    gt = pd.DataFrame(grows)
    gt.to_csv(util.TAB_DIR / "t03_granger.csv", index=False)
    print("\n--- Granger causality (F-test) ---")
    print(gt.to_string(index=False))

    # ---- Contemporaneous coupling ----------------------------------------
    ct = pd.DataFrame([
        contemporaneous(combat, f"combat (1-{util.KINETIC_END})"),
        contemporaneous(full, "full (1-170)"),
    ])
    ct.to_csv(util.TAB_DIR / "t03_contemporaneous.csv", index=False)
    print("\n--- Contemporaneous (same-day) strike-retaliation correlation ---")
    print(ct.to_string(index=False))

    # ---- FEVD (combat regime), BOTH Cholesky orderings -------------------
    # The same-day coupling is strong (r~0.69), so the FEVD asymmetry is
    # ordering-dependent (an identification caveat we report explicitly). We
    # compute both orderings; a directional claim survives only if it is stable
    # across them (it is NOT here — hence directional inference rests on the
    # LAGGED evidence in steps 03/05, which is ordering-free).
    frows = []
    for ordering in ([VARS, VARS[::-1]]):
        res_o = VAR(combat[ordering]).fit(max(lag_c, 1))
        dec = res_o.fevd(H).decomp  # decomp[i,h,j]: var i explained by shock j
        for i, vi in enumerate(ordering):
            for j, vj in enumerate(ordering):
                frows.append({
                    "ordering": " -> ".join(ordering),
                    "variable": vi, "shock_source": vj,
                    "fevd_h1": round(float(dec[i, 0, j]), 3),
                    "fevd_h6": round(float(dec[i, min(5, H - 1), j]), 3),
                    "fevd_h12": round(float(dec[i, H - 1, j]), 3),
                })
    ft = pd.DataFrame(frows)
    ft.to_csv(util.TAB_DIR / "t03_fevd.csv", index=False)
    print(f"\n--- FEVD (combat regime, horizon {H}d), BOTH orderings "
          f"(asymmetry is ordering-dependent) ---")
    print(ft.to_string(index=False))

    # ---- IRF figure (combat regime, orthogonalized, MC bands) ------------
    irf = res_c.irf(H)
    irfs = irf.orth_irfs                      # (H+1, k, k)
    lo, up = irf.errband_mc(orth=True, repl=1000, signif=0.05, seed=SEED)

    util.apply_style()
    fig, axes = plt.subplots(2, 2, figsize=(9.0, 6.2), sharex=True)
    hx = np.arange(H + 1)
    for i, vi in enumerate(VARS):          # response variable (row)
        for j, vj in enumerate(VARS):      # shock variable (col)
            ax = axes[i, j]
            color = util.C_STRIKE if vj == "strikes" else util.C_RETAL
            ax.axhline(0, color="0.6", lw=0.8)
            ax.fill_between(hx, lo[:, i, j], up[:, i, j], color=color, alpha=0.18)
            ax.plot(hx, irfs[:, i, j], color=color, lw=2.0)
            ax.set_title(f"{NAMES[vj]} shock  →  {NAMES[vi]}", fontsize=9.5)
            if i == 1:
                ax.set_xlabel("Days after shock")
            if j == 0:
                ax.set_ylabel("Response\n(events/day)")
    fig.suptitle("Orthogonalized impulse responses, active-combat regime (Days 1–40)\n"
                 "shaded = 95% Monte-Carlo error band",
                 fontweight="bold", y=1.03, fontsize=11)
    util.savefig(fig, "fig3_irf_combat")
    plt.close(fig)

    # ---- save VAR summary for the appendix -------------------------------
    with open(util.TAB_DIR / "t03_var_combat_summary.txt", "w") as fh:
        fh.write(str(res_c.summary()))
    print(f"\nWrote VAR summary + tables + fig3 to {util.OUT_DIR}")

    # ---- console takeaways ------------------------------------------------
    print("\n=== KEY RESULTS ===")
    for _, r in gt.iterrows():
        verdict = "YES" if r["granger_causal_05"] else "no"
        print(f"  [{r['sample']:16s}] {r['direction']:22s} "
              f"F={r['F']:.2f} p={r['p_value']:.4f}  Granger-causal? {verdict}")
    cc = ct.iloc[0]
    print(f"  Same-day coupling (combat): r={cc['pearson_r']} (p={cc['p_value']})")


if __name__ == "__main__":
    main()
