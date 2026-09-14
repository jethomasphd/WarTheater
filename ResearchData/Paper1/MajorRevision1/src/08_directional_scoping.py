#!/usr/bin/env python3
"""
08 — Directional evidence, scoped.

Two directional claims in the parent paper need scoping before a political-science referee
sees them (reviewer memo):
  (a) The resumption-phase result "retaliation Granger-causes strikes" rests on 23 daily
      observations. It is re-reported here with the number of usable observations, under
      two operationalisations, and labelled suggestive.
  (b) The full-sample Granger result was estimated across the regime mean shifts that the
      paper itself gives as the reason to prefer the combat-regime model. It is re-estimated
      on regime-demeaned series (each series minus its phase mean), under every information
      criterion's lag choice, and with the six detected regimes as a sensitivity.

Outputs
  output/tables/t08_resumption.csv       resumption-phase Granger and lead-lag correlations
  output/tables/t08_full_sample.csv      naive vs regime-demeaned full-sample Granger tests
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from statsmodels.tsa.api import VAR

import util

warnings.filterwarnings("ignore")


def granger(data, lag, label, extra):
    res = VAR(data).fit(lag)
    out = []
    for cause, effect in [("strikes", "retal"), ("retal", "strikes")]:
        gc = res.test_causality(effect, [cause], kind="f")
        out.append({"sample": label, **extra, "lag": lag, "n_obs_used": int(res.nobs),
                    "direction": f"{cause} -> {effect}",
                    "F": round(float(gc.test_statistic), 3), "df": str(gc.df),
                    "p_value": round(float(gc.pvalue), 4),
                    "significant_05": bool(gc.pvalue < 0.05)})
    return out


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 08 · Directional evidence, scoped")
    print("=" * 70)
    p = util.load_panel()

    # ---- (a) resumption phase ------------------------------------------- #
    rows = []
    seg = util.phase_slice(p, "Resumption")
    for label, sc, rc in [("primary (distinct locations)", "strikes", "retal"),
                          ("raw event rows", "strikes_rows", "retal_rows")]:
        d = seg[[sc, rc]].astype(float).rename(columns={sc: "strikes", rc: "retal"})
        sel = VAR(d).select_order(2).selected_orders
        lag = max(int(sel["bic"]), 1)
        for r in granger(d, lag, "Resumption (Days 130-152)",
                         {"measure": label, "n_days": len(d), "lag_criterion": "BIC (min 1)"}):
            r["ccf_retal_leads_strikes_1d"] = round(util.ccf(d["retal"], d["strikes"], 1), 3)
            r["ccf_strikes_lead_retal_1d"] = round(util.ccf(d["strikes"], d["retal"], 1), 3)
            r["status"] = "suggestive: 23 days, ~22 usable observations"
            rows.append(r)
    rt = pd.DataFrame(rows)
    print("\n--- (a) Resumption-phase directional evidence ---")
    print(rt.to_string(index=False))
    util.write_table(rt, "t08_resumption.csv")

    # ---- (b) full sample: naive vs regime-demeaned ---------------------- #
    full = p[["strikes", "retal"]].astype(float)
    rows = []
    sel = VAR(full).select_order(10).selected_orders
    for crit in ("aic", "bic"):
        lag = max(int(sel[crit]), 1)
        rows += granger(full, lag, "Full sample, naive (levels)",
                        {"lag_criterion": f"{crit.upper()} = {int(sel[crit])}",
                         "demeaning": "none"})

    dm4 = full.copy()
    for name in util.PHASE_ORDER:
        idx = util.phase_slice(p, name).index
        dm4.loc[idx] = dm4.loc[idx] - dm4.loc[idx].mean()
    sel4 = VAR(dm4).select_order(10).selected_orders
    for crit in ("aic", "hqic", "bic"):
        lag = max(int(sel4[crit]), 1)
        note = f"{crit.upper()} = {int(sel4[crit])}" + (" (lag 1 used: minimum feasible)" if int(sel4[crit]) == 0 else "")
        rows += granger(dm4, lag, "Full sample, regime-demeaned (4 documented phases)",
                        {"lag_criterion": note, "demeaning": "4 documented phases"})

    # six detected regimes (from step 07) as sensitivity
    bp = pd.read_csv(util.TAB_DIR / "t07_breakpoints.csv")
    breaks = sorted(int(b) for b in bp["detected_break_day"])
    edges = [1] + breaks + [util.LAST_DAY + 1]
    dm6 = full.copy()
    for a, b in zip(edges[:-1], edges[1:]):
        idx = full.index[(full.index >= a) & (full.index < b)]
        dm6.loc[idx] = dm6.loc[idx] - dm6.loc[idx].mean()
    sel6 = VAR(dm6).select_order(10).selected_orders
    for crit in ("aic", "bic"):
        lag = max(int(sel6[crit]), 1)
        note = f"{crit.upper()} = {int(sel6[crit])}" + (" (lag 1 used: minimum feasible)" if int(sel6[crit]) == 0 else "")
        rows += granger(dm6, lag, "Full sample, regime-demeaned (6 detected regimes)",
                        {"lag_criterion": note, "demeaning": f"6 detected regimes (breaks {breaks})"})
    ft = pd.DataFrame(rows)
    print("\n--- (b) Full-sample directional evidence: naive vs regime-demeaned ---")
    print(ft.to_string(index=False))
    util.write_table(ft, "t08_full_sample.csv")

    print("\n=== SCOPING ===")
    r1 = rt[(rt["measure"].str.startswith("primary")) & (rt["direction"] == "retal -> strikes")].iloc[0]
    print(f"  resumption retal->strikes: F={r1['F']}, p={r1['p_value']} on {r1['n_obs_used']} usable obs")
    for _, r in ft[ft["direction"] == "retal -> strikes"].iterrows():
        print(f"  {r['sample'][:52]:52s} {r['lag_criterion'][:24]:24s} p={r['p_value']}")


if __name__ == "__main__":
    main()
