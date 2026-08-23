#!/usr/bin/env python3
"""
07 — The flood extension: source divergence as political fact, and
confidence-weighted sensitivity analysis.

Two demonstrations of "counter-technology" analysis (Thomas et al. 2026,
§6.4-§6.5, §7.3.2): the dataset's transparency artifacts (source attribution,
data_confidence ratings) are used as ANALYTIC INPUTS rather than treated as
nuisance.

(A) Source-divergence register: cumulative Iranian casualty claims by named
    source, extracted from anchored dataset events and verified at run time.
    Divergence ratios (max/min at comparable moments) quantify the epistemic
    spread the manuscript calls "discrepancies as political facts."

(B) Confidence-weighted sensitivity: the core regression (M3: iran_civ ~
    strikes_milfac + strikes_civfac + retal) re-estimated with the exposure
    series rebuilt (i) from all rows, (ii) from HIGH-confidence rows only,
    (iii) confidence-weighted (HIGH=1.0, MEDIUM=0.7, LOW=0.4 — documented,
    admittedly arbitrary weights; the point is the sensitivity, not the
    weights). Raw and weighted variants are reported in parallel, exactly as
    manuscript §7.3.2 recommends.

Outputs:
  output/tables/t07_source_claims.csv
  output/tables/t07_divergence.csv
  output/tables/t07_confidence_sensitivity.csv
  output/figures/fig8_source_divergence.(png|pdf)
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

import util

HAC_LAGS = 7

# Cumulative Iranian-toll claims by named source. Every row is anchored to a
# dataset event id + anchor text and verified below before use.
#   (day, source, scope, value, event_id, anchor_text)
CLAIMS = [
    (7,   "Iranian Red Crescent / state media", "civilian", 400,  "EVT-0043", "over 400 civilian deaths"),
    (15,  "Iran Health Ministry",               "total",    1444, "EVT-0094", "1,444 killed"),
    (20,  "Hengaw (5th report)",                "total",    5300, "EVT-0157", "5,300 killed"),
    (20,  "Hengaw (5th report)",                "civilian", 511,  "EVT-0157", "511 civilians"),
    (20,  "Hengaw (5th report)",                "children", 120,  "EVT-0157", "120"),
    (29,  "Iran deputy UN representative",      "total",    1750, "EVT-0287", "1,750"),
    (29,  "HRANA (as of Mar 17)",               "total",    3114, "EVT-0287", "3,114 deaths"),
    (29,  "HRANA (as of Mar 17)",               "civilian", 1354, "EVT-0287", "1,354 civilians"),
    (29,  "HRANA (as of Mar 17)",               "children", 217,  "EVT-0287", "217 children"),
    (45,  "Iran Health Ministry",               "total",    2000, "EVT-0455", "~2,000+ killed"),
    (45,  "HRANA (Apr 7)",                      "total",    3636, "EVT-0455", "3,636 total"),
    (45,  "HRANA (Apr 7)",                      "civilian", 1701, "EVT-0455", "1,701 civilians"),
    (45,  "Hengaw (Apr 8)",                     "total",    7650, "EVT-0455", "7,650 total"),
    (45,  "Hengaw (Apr 8)",                     "civilian", 1030, "EVT-0455", "1,030 civilians"),
    (45,  "IDF claim",                          "military", 6000, "EVT-0455", "6,000+ IRGC killed"),
    (53,  "Iran Legal Medicine Organization",   "total",    3375, "EVT-0521", "3,375 killed"),
    (53,  "Iran Legal Medicine Organization",   "children", 383,  "EVT-0521", "383 children"),
]

CONF_W = {"HIGH": 1.0, "MEDIUM": 0.7, "LOW": 0.4}


def star(pv):
    return "***" if pv < 0.001 else "**" if pv < 0.01 else "*" if pv < 0.05 else ""


def verify_claims(df: pd.DataFrame):
    idx = df.set_index("event_id")["event_description"].fillna("")
    for day, source, scope, value, eid, anchor in CLAIMS:
        assert eid in idx.index, f"claim anchor {eid} missing"
        assert anchor.lower() in idx.loc[eid].lower(), \
            f"claim anchor '{anchor}' not in {eid}"


def weighted_exposures(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    """Rebuild daily exposure series (strikes_milfac, strikes_civfac, retal)
    under a confidence filter/weighting. mode in {'all','high_only','weighted'}.

    De-duplication note: distinct-location counting collapses each location-
    day to one unit; under 'weighted', a location-day contributes the MAX
    weight among its rows (a location partially confirmed at HIGH counts as
    HIGH). Non-strike-file rows contribute their own row weight.
    """
    conf = df[df.day_of_conflict >= 1].copy()
    conf["w"] = conf.data_confidence.map(CONF_W).fillna(0.7)
    if mode == "high_only":
        conf = conf[conf.data_confidence == "HIGH"]
    use_w = mode == "weighted"

    out = pd.DataFrame(index=util.DAYS)

    # Retaliation tempo (Paper 1 dedup: locations + discrete rows).
    d = conf[conf.event_domain == "RETALIATION"]
    sf = d[d.source_file.isin(util.STRIKE_FILES) & d.source_record_id.notna()]
    if use_w:
        loc = sf.groupby(["day_of_conflict", "source_record_id"])["w"].max() \
                .groupby("day_of_conflict").sum()
        other = d[~d.source_file.isin(util.STRIKE_FILES)] \
            .groupby("day_of_conflict")["w"].sum()
    else:
        loc = sf.groupby("day_of_conflict")["source_record_id"].nunique()
        other = d[~d.source_file.isin(util.STRIKE_FILES)] \
            .groupby("day_of_conflict").size()
    out["retal"] = loc.add(other, fill_value=0).reindex(util.DAYS, fill_value=0).values

    # Civilian- vs military-facing strike locations.
    stk, civ_mask = util._strike_civfac_masks(conf)
    locday = (stk.assign(civ=civ_mask)
              .groupby(["day_of_conflict", "source_record_id"])
              .agg(civ=("civ", "any"), w=("w", "max")).reset_index())
    val = locday["w"] if use_w else 1.0
    locday["unit"] = val
    civ = locday[locday.civ].groupby("day_of_conflict")["unit"].sum()
    mil = locday[~locday.civ].groupby("day_of_conflict")["unit"].sum()
    out["strikes_civfac"] = civ.reindex(util.DAYS, fill_value=0).values
    out["strikes_milfac"] = mil.reindex(util.DAYS, fill_value=0).values
    return out


def fit_m3(y, X, variant):
    m = sm.OLS(y, sm.add_constant(X)).fit(cov_type="HAC",
                                          cov_kwds={"maxlags": HAC_LAGS})
    rows = []
    for name in m.params.index:
        rows.append({"variant": variant, "term": name, "coef": m.params[name],
                     "se_hac": m.bse[name], "p": m.pvalues[name],
                     "sig": star(m.pvalues[name])})
    rows.append({"variant": variant, "term": "_R2", "coef": m.rsquared,
                 "se_hac": np.nan, "p": np.nan, "sig": ""})
    return rows


def main():
    util.apply_style()
    df = util.load_events()
    p = util.load_panel()
    verify_claims(df)

    # ---------------- (A) claims register + divergence -------------------- #
    t_claims = pd.DataFrame(CLAIMS, columns=[
        "day", "source", "scope", "value", "event_id", "anchor_text"])
    # Dataset's own tracking series for context.
    t_claims.to_csv(util.TAB_DIR / "t07_source_claims.csv", index=False)

    div_rows = []
    for day in (29, 45):
        tot = t_claims[(t_claims.day == day) & (t_claims.scope == "total")]
        div_rows.append({
            "day": day, "scope": "total", "n_sources": len(tot),
            "min_value": int(tot.value.min()), "min_source": tot.loc[tot.value.idxmin(), "source"],
            "max_value": int(tot.value.max()), "max_source": tot.loc[tot.value.idxmax(), "source"],
            "divergence_ratio": tot.value.max() / tot.value.min(),
        })
    civ45 = t_claims[(t_claims.day == 45) & (t_claims.scope == "civilian")]
    div_rows.append({
        "day": 45, "scope": "civilian", "n_sources": len(civ45),
        "min_value": int(civ45.value.min()), "min_source": civ45.loc[civ45.value.idxmin(), "source"],
        "max_value": int(civ45.value.max()), "max_source": civ45.loc[civ45.value.idxmax(), "source"],
        "divergence_ratio": civ45.value.max() / civ45.value.min(),
    })
    # Dataset-internal divergence: daily-series cumulative vs snapshot.
    for pop, cum_col, snap_col in [("Iran", "cum_iran_daily", "snap_iranian_killed"),
                                   ("Lebanon", "cum_leb_daily", "snap_lebanese_killed")]:
        div_rows.append({
            "day": 170, "scope": f"dataset-internal ({pop})", "n_sources": 2,
            "min_value": int(p[cum_col].iloc[-1]), "min_source": "daily series (sum)",
            "max_value": int(p[snap_col].iloc[-1]), "max_source": "dashboard snapshot",
            "divergence_ratio": p[snap_col].iloc[-1] / p[cum_col].iloc[-1],
        })
    # The re-anchoring event: the dashboard's cumulative Iranian-killed metric
    # peaked at 9,226 (Day 56) and re-anchored to 3,375 on Day 57 — the Legal
    # Medicine Organization figure reported on Day 53 (EVT-0521). The largest
    # single epistemic revision inside the dataset (-63% in one day).
    peak = float(p.snap_iranian_killed.max())
    peak_day = int(p.index[p.snap_iranian_killed == peak].max())  # last day at peak
    post = float(p.snap_iranian_killed.loc[peak_day + 1])
    assert peak == 9226.0 and post == 3375.0, \
        f"re-anchoring signature changed: peak {peak} (D{peak_day}) -> {post}"
    div_rows.append({
        "day": peak_day + 1, "scope": "dashboard re-anchoring (Iran)",
        "n_sources": 2,
        "min_value": int(post), "min_source": "post-re-anchor (LMO-aligned)",
        "max_value": int(peak), "max_source": f"pre-re-anchor peak (Day {peak_day})",
        "divergence_ratio": peak / post,
    })
    t_div = pd.DataFrame(div_rows)
    t_div.round(3).to_csv(util.TAB_DIR / "t07_divergence.csv", index=False)
    print("t07_divergence:")
    print(t_div.round(2).to_string(index=False))

    # ---------------- (B) confidence-weighted sensitivity ------------------ #
    y = p["iran_civ"].astype(float)
    sens_rows = []
    for mode in ("all", "high_only", "weighted"):
        X = weighted_exposures(df, mode)[["strikes_milfac", "strikes_civfac", "retal"]]
        sens_rows.extend(fit_m3(y, X.astype(float), mode))
    t_sens = pd.DataFrame(sens_rows)
    t_sens.round(5).to_csv(util.TAB_DIR / "t07_confidence_sensitivity.csv",
                           index=False)
    print("\nt07_confidence_sensitivity (civfac coefficient across variants):")
    print(t_sens[t_sens.term == "strikes_civfac"][
        ["variant", "coef", "se_hac", "p", "sig"]].round(4).to_string(index=False))

    # ---------------- Figure 8 --------------------------------------------- #
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.5),
                             gridspec_kw={"width_ratios": [1.5, 1]})
    ax = axes[0]
    util.shade_phases(ax)
    ax.plot(p.index, p.cum_iran_daily, color="0.15", lw=1.6,
            label="Dataset daily series (cumulative)")
    ax.plot(p.index, p.snap_iranian_killed, color="0.45", lw=1.3, ls="--",
            label="Dashboard snapshot")
    src_style = {
        "Iran Health Ministry": ("o", util.C_STRIKE),
        "Iran deputy UN representative": ("v", util.C_STRIKE),
        "Iran Legal Medicine Organization": ("s", util.C_STRIKE),
        "HRANA (as of Mar 17)": ("D", util.C_RETAL),
        "HRANA (Apr 7)": ("D", util.C_RETAL),
        "Hengaw (5th report)": ("^", util.C_GOLD),
        "Hengaw (Apr 8)": ("^", util.C_GOLD),
    }
    seen = set()
    for _, r in t_claims[t_claims.scope == "total"].iterrows():
        mk, col = src_style[r.source]
        fam = ("Iranian official" if col == util.C_STRIKE else
               "HRANA (diaspora NGO)" if col == util.C_RETAL else
               "Hengaw (diaspora NGO)")
        lab = fam if fam not in seen else None
        seen.add(fam)
        ax.scatter(r.day, r.value, marker=mk, s=64, color=col, zorder=6,
                   edgecolor="white", linewidth=0.9, label=lab)
    ax.annotate("Day-45 spread: 3.8×", xy=(45, 7650), xytext=(62, 6600),
                fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.9, color="0.3"))
    ax.annotate("Day-57 re-anchoring:\n9,226 → 3,375 (−63%)", xy=(57, 6200),
                xytext=(75, 8300), fontsize=8.5,
                arrowprops=dict(arrowstyle="->", lw=0.9, color="0.3"))
    ax.set_xlabel("Day of conflict")
    ax.set_ylabel("Cumulative Iranian killed (claimed)")
    ax.set_title("A. Cumulative-toll claims by source family vs the dataset series",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=7.8, loc="center right")
    ax.set_xlim(0, 171)

    ax = axes[1]
    terms = ["strikes_milfac", "strikes_civfac", "retal"]
    xpos = np.arange(len(terms))
    off = {"all": -0.22, "high_only": 0.0, "weighted": 0.22}
    colors = {"all": util.C_STRIKE, "high_only": util.C_RETAL,
              "weighted": util.C_GOLD}
    for mode in ("all", "high_only", "weighted"):
        sub = t_sens[(t_sens.variant == mode) & t_sens.term.isin(terms)]
        sub = sub.set_index("term").loc[terms]
        ax.errorbar(xpos + off[mode], sub.coef, yerr=1.96 * sub.se_hac,
                    fmt="o", ms=5.5, capsize=3.5, lw=1.4,
                    color=colors[mode], label=mode.replace("_", " "))
    ax.axhline(0, color="0.4", lw=0.8)
    ax.set_xticks(xpos)
    ax.set_xticklabels(["military-\nfacing", "civilian-\nfacing", "retaliation"],
                       fontsize=8.5)
    ax.set_ylabel("Coefficient (Iranian civilian killed/day)")
    ax.set_title("B. Core model under confidence variants",
                 loc="left", fontweight="bold", fontsize=9.5)
    ax.legend(fontsize=8)
    util.savefig(fig, "fig8_source_divergence")
    plt.close(fig)

    print("\nwrote t07 tables + fig8")


if __name__ == "__main__":
    main()
