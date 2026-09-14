#!/usr/bin/env python3
"""
Paper 1 — Major Revision 1: shared utilities.

Data pinning (with an integrity hash), daily-panel construction, the structural-break
engine, small statistical helpers, and the plotting style. Every analysis script imports
from here so that the panel and the estimators are built identically everywhere.

Reproducibility contract
------------------------
* The analysis is pinned to the FROZEN v1.2 research release
  (ResearchData/releases/v1.2/iranwar_event_dataset.csv). Its MD5 is checked on load, so
  the pipeline fails loudly if the input is not the exact frozen file. Override the input
  with IRANWAR_DATASET=/path/to.csv (the hash check is then skipped and a notice printed).
* Every stochastic step (IRF Monte-Carlo bands, bootstrap ratios, placebo permutations)
  is seeded with SEED. There is no network and no wall-clock dependence.
* The daily panel built here is identical, cell for cell, to the parent paper's panel
  (ResearchData/Paper1/data/panel_daily.csv); 00_build_panel.py asserts this when the
  parent panel is present.
"""
from __future__ import annotations

import hashlib
import os
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
SRC_DIR = Path(__file__).resolve().parent
PAPER_DIR = SRC_DIR.parent                        # ResearchData/Paper1/MajorRevision1
PARENT_DIR = PAPER_DIR.parent                     # ResearchData/Paper1
RESEARCH_DIR = PARENT_DIR.parent                  # ResearchData
DATA_DIR = PAPER_DIR / "data"
OUT_DIR = PAPER_DIR / "output"
FIG_DIR = OUT_DIR / "figures"
TAB_DIR = OUT_DIR / "tables"
for _d in (DATA_DIR, FIG_DIR, TAB_DIR):
    _d.mkdir(parents=True, exist_ok=True)

PINNED_DATASET = RESEARCH_DIR / "releases" / "v1.2" / "iranwar_event_dataset.csv"
ROOT_DATASET = RESEARCH_DIR / "iranwar_event_dataset.csv"
PINNED_MD5 = "9a2ac6b3afb7fbc2203ff248bac824fd"   # md5 of the frozen v1.2 CSV


def dataset_path() -> Path:
    env = os.environ.get("IRANWAR_DATASET")
    if env:
        return Path(env)
    if PINNED_DATASET.exists():
        return PINNED_DATASET
    return ROOT_DATASET


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_dataset(path: Path) -> None:
    """Fail loudly unless the input is the exact frozen v1.2 file (or an explicit override)."""
    if os.environ.get("IRANWAR_DATASET"):
        print(f"  [notice] IRANWAR_DATASET override in use: {path} (hash check skipped)")
        return
    if os.environ.get("IRANWAR_SKIP_HASH"):
        print("  [notice] IRANWAR_SKIP_HASH set: hash check skipped")
        return
    got = md5_of(path)
    if got != PINNED_MD5:
        raise RuntimeError(
            f"Dataset integrity check failed for {path}\n"
            f"  expected md5 {PINNED_MD5}\n  got      md5 {got}\n"
            "  The analysis is pinned to the frozen v1.2 release. Set IRANWAR_DATASET to "
            "analyse a different file deliberately.")


# --------------------------------------------------------------------------- #
# Conflict constants (identical to the parent paper)
# --------------------------------------------------------------------------- #
DATASET_VERSION = "1.2"
CONFLICT_START = date(2026, 2, 28)   # Day 1
BASELINE_DATE = date(2026, 2, 27)    # Day 0
LAST_DAY = 170                        # v1.2 coverage horizon (2026-08-16)
DAYS = list(range(1, LAST_DAY + 1))

# Documented phases (narrative boundaries from strikes-iran.json `_metadata.phase`).
# They are corroborated, not imposed, by the structural-break analysis (07).
PHASES = [
    ("Major Combat",     1,   40),   # 2026-02-28 .. 2026-04-08
    ("First Ceasefire",  41,  129),  # 2026-04-09 .. 2026-07-06
    ("Resumption",       130, 152),  # 2026-07-07 .. 2026-07-29
    ("Diplomatic Pause", 153, 170),  # 2026-07-30 .. 2026-08-16
]
PHASE_ORDER = [p[0] for p in PHASES]
KINETIC_END = 40                       # last day of the sustained-combat regime
DOCUMENTED_BREAKS = [41, 130, 153]     # first day of each documented new phase


def date_from_day(day: int) -> date:
    return BASELINE_DATE + timedelta(days=int(day))


def phase_of(day: int) -> str:
    for name, lo, hi in PHASES:
        if lo <= day <= hi:
            return name
    return "Unknown"


def phase_slice(panel: pd.DataFrame, name: str) -> pd.DataFrame:
    lo, hi = next((lo, hi) for n, lo, hi in PHASES if n == name)
    return panel[(panel.index >= lo) & (panel.index <= hi)]


# --------------------------------------------------------------------------- #
# Panel construction (identical to the parent paper)
# --------------------------------------------------------------------------- #
STRIKE_FILES = ("strikes-iran.json", "strikes-retaliation.json")


def load_events() -> pd.DataFrame:
    path = dataset_path()
    verify_dataset(path)
    return pd.read_csv(path)


def _domain_daily_dedup(conf: pd.DataFrame, domain: str) -> pd.Series:
    """Daily tempo for a domain, de-duplicating the strike-file target x active-day
    explosion: distinct source locations active per day, plus discrete non-strike-file
    rows (timeline events, which carry no source_record_id)."""
    d = conf[conf.event_domain == domain]
    sf = d[d.source_file.isin(STRIKE_FILES)]
    loc = sf.groupby("day_of_conflict")["source_record_id"].nunique()
    other = d[~d.source_file.isin(STRIKE_FILES)].groupby("day_of_conflict").size()
    s = loc.add(other, fill_value=0)
    return s.reindex(DAYS, fill_value=0).astype(int)


def _domain_daily_rows(conf: pd.DataFrame, domain: str) -> pd.Series:
    d = conf[conf.event_domain == domain]
    return d.groupby("day_of_conflict").size().reindex(DAYS, fill_value=0).astype(int)


def _timeline_daily(conf: pd.DataFrame, domain: str) -> pd.Series:
    d = conf[(conf.source_file == "timeline-events.json") & (conf.event_domain == domain)]
    return d.groupby("day_of_conflict").size().reindex(DAYS, fill_value=0).astype(int)


def build_panel() -> pd.DataFrame:
    """Daily analysis panel, Day 1..170. See docs/CODEBOOK_panel.md for definitions."""
    df = load_events()
    conf = df[df.day_of_conflict >= 1].copy()

    panel = pd.DataFrame({"day": DAYS})
    panel["date"] = [date_from_day(d).isoformat() for d in DAYS]
    panel["phase"] = [phase_of(d) for d in DAYS]

    panel["strikes"] = _domain_daily_dedup(conf, "STRIKE").values
    panel["retal"] = _domain_daily_dedup(conf, "RETALIATION").values
    panel["strikes_rows"] = _domain_daily_rows(conf, "STRIKE").values
    panel["retal_rows"] = _domain_daily_rows(conf, "RETALIATION").values
    panel["strikes_tl"] = _timeline_daily(conf, "STRIKE").values
    panel["retal_tl"] = _timeline_daily(conf, "RETALIATION").values

    cas = conf[conf.source_file == "casualties.json"].copy()
    cas["v"] = pd.to_numeric(cas["casualties_reported"], errors="coerce")
    killed = cas.groupby("day_of_conflict")["v"].sum().reindex(DAYS, fill_value=0)
    panel["killed"] = killed.values

    panel["diplomatic"] = _domain_daily_rows(conf, "DIPLOMATIC").values
    panel["naval"] = _domain_daily_rows(conf, "NAVAL").values

    ret = conf[conf.event_domain == "RETALIATION"].copy()
    ret = ret[ret["country"].notna() & (ret["country"] != "Unknown")]
    rc = ret.groupby("day_of_conflict")["country"].nunique().reindex(DAYS, fill_value=0)
    panel["retal_countries"] = rc.values
    seen, cum = set(), []
    for d in DAYS:
        seen.update(ret[ret.day_of_conflict == d]["country"].unique())
        cum.append(len(seen))
    panel["cum_countries"] = cum

    return panel.set_index("day")


def load_panel() -> pd.DataFrame:
    p = DATA_DIR / "panel_daily.csv"
    if not p.exists():
        raise FileNotFoundError(f"{p} not found — run 00_build_panel.py first.")
    return pd.read_csv(p).set_index("day")


def write_table(df: pd.DataFrame, name: str, index: bool = False) -> Path:
    out = TAB_DIR / name
    df.to_csv(out, index=index)
    print(f"  wrote output/tables/{name}")
    return out


# --------------------------------------------------------------------------- #
# Statistical helpers
# --------------------------------------------------------------------------- #
def fisher_ci(r: float, n: int, level: float = 0.95):
    """Fisher-z confidence interval for a Pearson correlation."""
    from scipy import stats
    z = np.arctanh(r)
    se = 1.0 / np.sqrt(n - 3)
    q = stats.norm.ppf(0.5 + level / 2)
    return float(np.tanh(z - q * se)), float(np.tanh(z + q * se))


def fisher_compare(r1: float, n1: int, r2: float, n2: int):
    """Two-sided Fisher r-to-z test that two independent correlations are equal."""
    from scipy import stats
    z = (np.arctanh(r1) - np.arctanh(r2)) / np.sqrt(1.0 / (n1 - 3) + 1.0 / (n2 - 3))
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return float(z), float(p)


def holm(pvals):
    """Holm step-down adjusted p-values (controls family-wise error)."""
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        val = min(1.0, (m - rank) * p[idx])
        running = max(running, val)
        adj[idx] = running
    return adj


def ccf(x, y, lag: int) -> float:
    """corr(x_t, y_{t+lag}); lag > 0 means x leads y."""
    x = np.asarray(x, float) - np.mean(x)
    y = np.asarray(y, float) - np.mean(y)
    if lag > 0:
        a, b = x[:-lag], y[lag:]
    elif lag < 0:
        a, b = x[-lag:], y[:lag]
    else:
        a, b = x, y
    if a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


# --------------------------------------------------------------------------- #
# Structural-break engine (Bai–Perron change-in-mean model, exact DP, vectorised)
# --------------------------------------------------------------------------- #
def best_partition(x, K: int, min_seg: int):
    """Optimal partition of x into exactly K contiguous segments minimising the total
    within-segment sum of squares, subject to a minimum segment length. Returns
    (total_sse, break_indices) where a break index b means the new segment starts at
    x[b] (0-based). Exact dynamic programme; O(K n^2) with vectorised inner loop."""
    x = np.asarray(x, float)
    n = len(x)
    s = np.concatenate([[0.0], np.cumsum(x)])
    s2 = np.concatenate([[0.0], np.cumsum(x * x)])
    dp = np.full((K + 1, n + 1), np.inf)
    back = np.full((K + 1, n + 1), -1, dtype=int)
    dp[0, 0] = 0.0
    for k in range(1, K + 1):
        lo = (k - 1) * min_seg
        for j in range(k * min_seg, n + 1):
            i = np.arange(lo, j - min_seg + 1)
            prev = dp[k - 1, i]
            L = (j - i).astype(float)
            tot = s[j] - s[i]
            cost = (s2[j] - s2[i]) - tot * tot / L
            c = prev + cost
            b = int(np.argmin(c))
            dp[k, j] = c[b]
            back[k, j] = i[b]
    sse = float(dp[K, n])
    breaks, j, k = [], n, K
    while k > 1:
        i = back[k, j]
        breaks.append(int(i))
        j, k = i, k - 1
    breaks.reverse()
    return sse, breaks


def penalty(name: str, n: int, K: int) -> float:
    """Model-selection penalty for a K-segment mean-shift model.
    parent : (K+1) log n            — the penalty used in the parent paper (K means + 1 variance)
    yao    : (2K-1) log n           — Yao (1988) / Bai–Perron BIC counting break dates as parameters
    lwz    : 0.299 (2K-1) (log n)^2.1 — Liu, Wu & Zidek (1997) modified criterion (stricter)
    """
    if name == "parent":
        return (K + 1) * np.log(n)
    if name == "yao":
        return (2 * K - 1) * np.log(n)
    if name == "lwz":
        return 0.299 * (2 * K - 1) * (np.log(n)) ** 2.1
    raise ValueError(name)


def select_segments(x, min_seg: int = 6, max_k: int = 6, crit: str = "parent"):
    """Fit K = 1..max_k and choose K by the requested criterion. Returns
    (rows, best) where rows is a list of dicts (one per K) and best is the chosen row."""
    x = np.asarray(x, float)
    n = len(x)
    rows, best = [], None
    for K in range(1, max_k + 1):
        sse, breaks = best_partition(x, K, min_seg)
        rss = max(sse, 1e-9)
        ic = n * np.log(rss / n) + penalty(crit, n, K)
        row = {"n_segments": K, "n_breaks": K - 1, "sse": sse, "ic": ic,
               "break_days": [b + 1 for b in breaks]}   # day = index + 1
        rows.append(row)
        if best is None or ic < best["ic"]:
            best = row
    return rows, best


# --------------------------------------------------------------------------- #
# Plotting (matplotlib only; Okabe–Ito colour-blind-safe palette)
# --------------------------------------------------------------------------- #
C_STRIKE = "#0072B2"   # blue      — US/Israeli strikes
C_RETAL = "#D55E00"    # vermilion — Iranian/proxy retaliation
C_DIPL = "#009E73"     # green     — diplomacy
C_ACCENT = "#CC79A7"   # purple    — derived quantities
C_GOLD = "#E69F00"     # orange    — secondary emphasis
C_GREY = "#7F7F7F"
PHASE_SHADE = ["#ECECEC", "#F7F7F7", "#ECECEC", "#F7F7F7"]


def apply_style():
    import matplotlib as mpl
    mpl.rcParams.update({
        "figure.dpi": 120, "savefig.dpi": 220,
        "font.size": 10, "font.family": "DejaVu Sans",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
        "legend.frameon": False, "figure.autolayout": True,
    })


def shade_phases(ax):
    for i, (name, lo, hi) in enumerate(PHASES):
        ax.axvspan(lo - 0.5, hi + 0.5, color=PHASE_SHADE[i % 4], zorder=0, alpha=0.8)


def label_phases(ax, y, fontsize=6.8):
    """Phase names along the top of a day-indexed axis. Short phases (< 30 days) are
    written on two lines at a smaller size so neighbouring labels never collide."""
    for name, lo, hi in PHASES:
        short = (hi - lo) < 30
        label = name.upper().replace(" ", "\n") if short else name.upper()
        ax.text((lo + hi) / 2, y, label, fontsize=fontsize * (0.72 if short else 1.0),
                color="0.35", ha="center", va="center", linespacing=1.0)


def savefig(fig, name: str):
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"{name}.{ext}", bbox_inches="tight")
    print(f"  wrote output/figures/{name}.png (+.pdf)")
