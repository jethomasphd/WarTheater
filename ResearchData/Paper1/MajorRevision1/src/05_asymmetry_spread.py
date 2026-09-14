#!/usr/bin/env python3
"""
05 — FINDING 4: the balance of the exchange flipped, and retaliation's reach saturated early.

The strike:retaliation ratio rises from 0.68 in combat (Iran out-paced recorded strikes) to
1.42 at the resumption (strikes outnumbered responses), with seeded bootstrap intervals; and
retaliation reached its full geographic reach (13 countries) by Day 22 with no new country
struck afterwards. The paper reads these as consistent with depletion while naming the live
alternatives (deliberate restraint, proxy rather than direct action, reporting attention).

Outputs
  output/tables/t05_ratio_by_phase.csv     ratio with bootstrap 95% CI, lead-lag correlations
  output/tables/t05_spread.csv             geographic reach summary
  output/figures/fig5_asymmetry_spread.(png|pdf)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import util

B = 2000


def boot_ratio(s, r, rng):
    n = len(s)
    out = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        rs = r[idx].sum()
        out.append(s[idx].sum() / rs if rs > 0 else np.nan)
    out = np.array(out)
    return np.nanpercentile(out, 2.5), np.nanpercentile(out, 97.5)


def main():
    print("=" * 70)
    print("Major Revision 1 · Step 05 · Finding 4 — asymmetry and geographic reach")
    print("=" * 70)
    rng = np.random.default_rng(util.SEED)
    p = util.load_panel()

    rows = []
    for name, lo, hi in util.PHASES:
        seg = p[(p.index >= lo) & (p.index <= hi)]
        s = seg["strikes"].astype(float).values
        r = seg["retal"].astype(float).values
        ratio = s.sum() / max(r.sum(), 1)
        cl, ch = boot_ratio(s, r, rng)
        sl = util.ccf(s, r, +1) if s.std() > 0 and r.std() > 0 else np.nan   # strikes_t vs retal_{t+1}
        rl = util.ccf(r, s, +1) if s.std() > 0 and r.std() > 0 else np.nan   # retal_t vs strikes_{t+1}
        rows.append({"phase": name, "days": f"{lo}-{hi}", "n_days": len(seg),
                     "strikes_total": int(s.sum()), "retal_total": int(r.sum()),
                     "strikes_per_day": round(s.mean(), 2), "retal_per_day": round(r.mean(), 2),
                     "strike_retal_ratio": round(ratio, 2),
                     "ratio_ci95_low": round(cl, 2), "ratio_ci95_high": round(ch, 2),
                     "ccf_strikes_lead_1d": round(sl, 3) if sl == sl else np.nan,
                     "ccf_retal_lead_1d": round(rl, 3) if rl == rl else np.nan})
    rt = pd.DataFrame(rows)
    print(f"\n--- Strike:retaliation ratio by phase (bootstrap 95% CI, B={B}) ---")
    print(rt.to_string(index=False))
    util.write_table(rt, "t05_ratio_by_phase.csv")

    cc = p["cum_countries"]
    max_c = int(cc.max()); day_max = int(cc.idxmax())
    new_after = int((cc.diff().fillna(0).loc[day_max + 1:] > 0).sum())
    days_to_half = int(cc[cc >= max_c / 2].index.min())
    st = pd.DataFrame([{"max_distinct_countries": max_c,
                        "first_day_reaching_max": day_max,
                        "date_reaching_max": util.date_from_day(day_max).isoformat(),
                        "new_countries_after_that_day": new_after,
                        "days_observed_after": int(util.LAST_DAY - day_max),
                        "first_day_reaching_half": days_to_half,
                        "retal_days_with_any_country_after_max":
                            int((p.loc[day_max + 1:, "retal_countries"] > 0).sum())}])
    print("\n--- Geographic reach of retaliation ---")
    print(st.to_string(index=False))
    util.write_table(st, "t05_spread.csv")

    # ---- Figure 5 -------------------------------------------------------- #
    util.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.9), gridspec_kw={"width_ratios": [1, 1.25]})
    ax = axes[0]
    act = rt[rt["retal_total"] > 0]
    x = np.arange(len(act)); w = 0.38
    ax.bar(x - w / 2, act["strikes_per_day"], w, color=util.C_STRIKE, label="strikes / day")
    ax.bar(x + w / 2, act["retal_per_day"], w, color=util.C_RETAL, label="retaliation / day")
    top = max(act["strikes_per_day"].max(), act["retal_per_day"].max())
    for i, (_, row) in enumerate(act.iterrows()):
        ax.text(i, max(row["strikes_per_day"], row["retal_per_day"]) + top * 0.04,
                f"ratio {row['strike_retal_ratio']:.2f}", ha="center", fontsize=8.6)
    ax.set_xticks(x); ax.set_xticklabels([n.replace(" ", "\n") for n in act["phase"]], fontsize=8.5)
    ax.set_ylim(0, top * 1.22)
    ax.set_ylabel("Events per day")
    ax.set_title("A. Strike:retaliation ratio by phase", loc="left", fontweight="bold")
    ax.legend(loc="upper right", fontsize=8.5)

    ax = axes[1]
    util.shade_phases(ax)
    ax.plot(p.index, cc, color=util.C_ACCENT, lw=2.2)
    ax.axvline(day_max, color="0.3", ls="--", lw=1.0)
    ax.text(day_max + 2, max_c * 0.35, f"all {max_c} countries reached\nby Day {day_max};"
            f"\nnone added in the next {util.LAST_DAY - day_max} days", fontsize=8.6, va="center")
    util.label_phases(ax, max_c * 1.06)
    ax.set_ylim(0, max_c * 1.15)
    ax.set_xlabel("Day of conflict")
    ax.set_ylabel("Cumulative distinct countries\nhit by retaliation")
    ax.set_title("B. Geographic reach of retaliation", loc="left", fontweight="bold")
    util.savefig(fig, "fig5_asymmetry_spread")
    plt.close(fig)

    print("\n=== FINDING 4 ===")
    print(f"  ratio combat {rt.loc[0,'strike_retal_ratio']} -> resumption {rt.loc[2,'strike_retal_ratio']}; "
          f"{max_c} countries by Day {day_max}, {new_after} added after")


if __name__ == "__main__":
    main()
