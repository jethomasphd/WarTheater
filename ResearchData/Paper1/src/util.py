#!/usr/bin/env python3
"""
Paper 1 — shared utilities: data location, daily-panel construction, plotting style.

Every analysis script imports from here so the panel is built identically everywhere.

Reproducibility contract
------------------------
The analysis is pinned to the *frozen* v1.2 research release
(`ResearchData/releases/v1.2/iranwar_event_dataset.csv`), NOT the moving root
dataset. This guarantees the paper reproduces byte-for-byte no matter how the
dashboard/dataset evolve in later releases. Override with IRANWAR_DATASET if needed.
"""
from __future__ import annotations

import os
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
SRC_DIR = Path(__file__).resolve().parent
PAPER_DIR = SRC_DIR.parent                       # ResearchData/Paper1
RESEARCH_DIR = PAPER_DIR.parent                  # ResearchData
DATA_DIR = PAPER_DIR / "data"
OUT_DIR = PAPER_DIR / "output"
FIG_DIR = OUT_DIR / "figures"
TAB_DIR = OUT_DIR / "tables"
for _d in (DATA_DIR, FIG_DIR, TAB_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# Pinned, frozen source dataset (immutable release). Env override allowed.
PINNED_DATASET = RESEARCH_DIR / "releases" / "v1.2" / "iranwar_event_dataset.csv"
ROOT_DATASET = RESEARCH_DIR / "iranwar_event_dataset.csv"


def dataset_path() -> Path:
    env = os.environ.get("IRANWAR_DATASET")
    if env:
        return Path(env)
    if PINNED_DATASET.exists():
        return PINNED_DATASET
    return ROOT_DATASET


# --------------------------------------------------------------------------- #
# Conflict constants
# --------------------------------------------------------------------------- #
DATASET_VERSION = "1.2"
CONFLICT_START = date(2026, 2, 28)   # Day 1
BASELINE_DATE = date(2026, 2, 27)    # Day 0
LAST_DAY = 170                        # v1.2 coverage horizon (2026-08-16)
DAYS = list(range(1, LAST_DAY + 1))

# Documented conflict phases. Boundaries come from the project's own phase
# narrative (strikes-iran.json `_metadata.phase`, mapped to war-days) and are
# corroborated empirically by the structural-break analysis (04). War-day N =
# 2026-02-27 + N days.
#   Day 130 = 2026-07-07 (documented resumption / "ceasefire collapsed").
#   Day 153 = 2026-07-30 (documented start of "no US strikes on Iranian territory").
PHASES = [
    ("Major Combat",         1,   40),   # 2026-02-28 .. 2026-04-08
    ("First Ceasefire",      41,  129),   # 2026-04-09 .. 2026-07-06
    ("Resumption",           130, 152),   # 2026-07-07 .. 2026-07-29
    ("Diplomatic Pause",     153, 170),   # 2026-07-30 .. 2026-08-16
]
PHASE_ORDER = [p[0] for p in PHASES]

# A coarser 2-regime split used for the core reciprocity comparison
# (heavy-combat vs. everything after the first collapse in strike tempo).
KINETIC_END = 40   # last day of the sustained heavy-combat regime


def date_from_day(day: int) -> date:
    return BASELINE_DATE + timedelta(days=int(day))


def phase_of(day: int) -> str:
    for name, lo, hi in PHASES:
        if lo <= day <= hi:
            return name
    return "Unknown"


# --------------------------------------------------------------------------- #
# Panel construction
# --------------------------------------------------------------------------- #
STRIKE_FILES = ("strikes-iran.json", "strikes-retaliation.json")


def load_events() -> pd.DataFrame:
    """Load the pinned event dataset (conflict days only kept downstream)."""
    df = pd.read_csv(dataset_path())
    return df


def _domain_daily_dedup(conf: pd.DataFrame, domain: str) -> pd.Series:
    """Daily 'tempo' count for a domain that de-duplicates the strike-file
    target x active_day explosion: distinct source locations active per day
    (from the strike/retaliation files) plus discrete non-strike-file rows
    (e.g. timeline events, which carry no source_record_id)."""
    d = conf[conf.event_domain == domain]
    sf = d[d.source_file.isin(STRIKE_FILES)]
    loc = sf.groupby("day_of_conflict")["source_record_id"].nunique()
    other = d[~d.source_file.isin(STRIKE_FILES)].groupby("day_of_conflict").size()
    s = loc.add(other, fill_value=0)
    return s.reindex(DAYS, fill_value=0).astype(int)


def _domain_daily_rows(conf: pd.DataFrame, domain: str) -> pd.Series:
    """Raw event-row count per day for a domain (includes strike explosion)."""
    d = conf[conf.event_domain == domain]
    return d.groupby("day_of_conflict").size().reindex(DAYS, fill_value=0).astype(int)


def _timeline_daily(conf: pd.DataFrame, domain: str) -> pd.Series:
    """Discrete timeline-events count per day for a domain (no explosion; the
    cleanest 'one reported event = one count' operationalization)."""
    d = conf[(conf.source_file == "timeline-events.json") & (conf.event_domain == domain)]
    return d.groupby("day_of_conflict").size().reindex(DAYS, fill_value=0).astype(int)


def build_panel() -> pd.DataFrame:
    """Construct the daily analysis panel (Day 1..170).

    Columns
    -------
    day, date, phase
    strikes        : primary US/Israeli offensive tempo (distinct locations/day + discrete offensive events)
    retal          : primary Iranian/proxy retaliation tempo (distinct locations/day + discrete events)
    strikes_rows   : raw STRIKE event-rows/day (robustness; includes target explosion)
    retal_rows     : raw RETALIATION event-rows/day (robustness)
    strikes_tl     : timeline-only STRIKE events/day (robustness)
    retal_tl       : timeline-only RETALIATION events/day (robustness)
    killed         : summed daily estimated killed across factions (casualties.json)
    diplomatic     : DIPLOMATIC events/day
    naval          : NAVAL events/day
    retal_countries: distinct countries hit by retaliation that day (horizontal spread)
    cum_countries  : cumulative distinct retaliation-target countries through day t
    """
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

    # Casualties: summed daily estimated killed across the 5 factions.
    cas = conf[conf.source_file == "casualties.json"].copy()
    cas["v"] = pd.to_numeric(cas["casualties_reported"], errors="coerce")
    killed = cas.groupby("day_of_conflict")["v"].sum().reindex(DAYS, fill_value=0)
    panel["killed"] = killed.values

    panel["diplomatic"] = _domain_daily_rows(conf, "DIPLOMATIC").values
    panel["naval"] = _domain_daily_rows(conf, "NAVAL").values

    # Horizontal spread: distinct countries absorbing retaliation per day.
    ret = conf[conf.event_domain == "RETALIATION"].copy()
    ret = ret[ret["country"].notna() & (ret["country"] != "Unknown")]
    rc = ret.groupby("day_of_conflict")["country"].nunique().reindex(DAYS, fill_value=0)
    panel["retal_countries"] = rc.values
    # cumulative distinct countries
    seen, cum = set(), []
    for d in DAYS:
        todays = ret[ret.day_of_conflict == d]["country"].unique()
        seen.update(todays)
        cum.append(len(seen))
    panel["cum_countries"] = cum

    panel = panel.set_index("day")
    return panel


def load_panel() -> pd.DataFrame:
    """Load the pre-built panel from data/panel_daily.csv (built by 00_build_panel.py)."""
    p = DATA_DIR / "panel_daily.csv"
    if not p.exists():
        raise FileNotFoundError(f"{p} not found — run 00_build_panel.py first.")
    return pd.read_csv(p).set_index("day")


# --------------------------------------------------------------------------- #
# Plotting (matplotlib, no seaborn; consistent, colorblind-safe palette)
# --------------------------------------------------------------------------- #
# Okabe-Ito colorblind-safe palette
C_STRIKE = "#0072B2"   # blue  — US/Israeli strikes
C_RETAL = "#D55E00"    # vermilion — Iranian/proxy retaliation
C_KILLED = "#000000"   # black — casualties
C_DIPL = "#009E73"     # green — diplomacy
C_ACCENT = "#CC79A7"   # purple accent
PHASE_SHADE = ["#EDEDED", "#F7F7F7", "#EDEDED", "#F7F7F7"]


def apply_style():
    import matplotlib as mpl
    mpl.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 200,
        "font.size": 10,
        "font.family": "DejaVu Sans",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.5,
        "legend.frameon": False,
        "figure.autolayout": True,
    })


def shade_phases(ax, y=None):
    """Shade the four documented phases behind a day-indexed time-series axis."""
    for i, (name, lo, hi) in enumerate(PHASES):
        ax.axvspan(lo - 0.5, hi + 0.5, color=PHASE_SHADE[i % len(PHASE_SHADE)],
                   zorder=0, alpha=0.7)


def savefig(fig, name: str):
    """Save a figure to both PNG and PDF in output/figures."""
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"{name}.{ext}", bbox_inches="tight")
    print(f"  wrote output/figures/{name}.png (+.pdf)")
