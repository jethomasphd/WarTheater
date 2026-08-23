#!/usr/bin/env python3
"""
Paper 2 — shared utilities: data pinning, health-system event extraction,
daily-panel construction, and plotting style.

Every analysis script imports from here so the panel and the health-system
event register are built identically everywhere.

Reproducibility contract
------------------------
The analysis is pinned to the *frozen* v1.2 research release
(`ResearchData/releases/v1.2/iranwar_event_dataset.csv`), NOT the moving root
dataset. This guarantees the paper reproduces byte-for-byte no matter how the
dashboard/dataset evolve in later releases. Override with IRANWAR_DATASET if
needed. All stochastic steps (bootstrap resampling) are seeded with SEED.
"""
from __future__ import annotations

import os
import re
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42  # global seed for every bootstrap in the paper

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
SRC_DIR = Path(__file__).resolve().parent
PAPER_DIR = SRC_DIR.parent                       # ResearchData/Paper2
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
# Conflict constants (identical to Paper 1 so the two papers are comparable)
# --------------------------------------------------------------------------- #
DATASET_VERSION = "1.2"
CONFLICT_START = date(2026, 2, 28)   # Day 1
BASELINE_DATE = date(2026, 2, 27)    # Day 0
LAST_DAY = 170                        # v1.2 coverage horizon (2026-08-16)
DAYS = list(range(1, LAST_DAY + 1))

# Documented conflict phases (see Paper 1 docs/METHODS.md §3: narrative
# boundaries corroborated by Bai–Perron structural breaks at Days 40/131/147).
PHASES = [
    ("Major Combat",     1,   40),   # 2026-02-28 .. 2026-04-08
    ("First Ceasefire",  41,  129),  # 2026-04-09 .. 2026-07-06
    ("Resumption",       130, 152),  # 2026-07-07 .. 2026-07-29
    ("Diplomatic Pause", 153, 170),  # 2026-07-30 .. 2026-08-16
]
PHASE_ORDER = [p[0] for p in PHASES]


def date_from_day(day: int) -> date:
    return BASELINE_DATE + timedelta(days=int(day))


def phase_of(day: int) -> str:
    for name, lo, hi in PHASES:
        if lo <= day <= hi:
            return name
    return "Unknown"


# --------------------------------------------------------------------------- #
# Event-classification vocabulary
# --------------------------------------------------------------------------- #
STRIKE_FILES = ("strikes-iran.json", "strikes-retaliation.json")

# Event types whose descriptions merely *echo* the day's headline narrative
# (cost rows, market rows, briefings, snapshots, per-faction casualty rows all
# carry the same day-context string). Text search on these would count the same
# reported health-system event many times, so they are excluded from the
# health-system register. The underlying discrete events are captured once via
# the timeline / strike / humanitarian rows.
ECHO_TYPES = {
    "daily_casualty_report", "daily_war_cost", "market_index", "oil_price",
    "tanker_transit", "daily_aggregate_snapshot", "daily_briefing", "summary",
    "hormuz_daily_narrative", "baseline_metric", "historical_comparison",
}

# Domains searched for health-system events. FINANCIAL / OTHER / NAVAL /
# CYBER / DIPLOMATIC rows either echo headlines or record activity with no
# direct health-system content; genuinely health-relevant developments in
# those spheres (e.g. the WHO logistics-hub hold) are recorded as
# HUMANITARIAN timeline events and enter through that domain.
HEALTH_DOMAINS = {"STRIKE", "RETALIATION", "MILITARY", "HUMANITARIAN"}

# Core health-system vocabulary. A row must match this pattern to enter the
# health-system event register at all. `hospital(?!i)` deliberately excludes
# "hospitalized"/"hospitalization" (harm to people, not to facilities).
HEALTH_PAT = re.compile(
    r"hospital(?!i[sz])|health\s*facilit|health[\s-]*care|healthcare|health\s+workers?|"
    r"clinic\b|ambulance|paramedic|nurses?\b|physician|"
    r"medical\s+(?:center|centre|research|supplies|care|clinic)|"
    r"medicines?\b|pharmac|dialysis|insulin|"
    r"Red\s+Crescent|Red\s+Cross|\bWHO\b|\bMoPH\b|Health\s+Ministry|"
    r"Legal\s+Medicine|"
    r"cholera|epidemi|disease\s+outbreak|"
    r"desalination|drinking\s+water|water\s+treatment|water/electrical\s+plant|"
    r"sanitation",
    re.I,
)

# Reference-data source files (static context rows, not conflict events).
REFERENCE_FILES = {"global-bases.json", "historical-comparison.json"}

# Ordered category rules (first match wins). `insult` marks events that are
# *physical or material blows to the health system* (attacks on facilities,
# workforce, supplies, WASH infrastructure, or humanitarian-access channels)
# as opposed to surveillance reports that *document* system state. Only
# insults accumulate into the HSSI.
HEALTH_CATEGORIES = [
    # (category, insult, pattern)
    ("wash_disruption", True, re.compile(
        r"desalination|drinking\s+water|water\s+treatment|water/electrical\s+plant|sanitation", re.I)),
    ("workforce_harm", True, re.compile(
        r"nurses?\s+killed|paramedic|health(?:\s*care)?\s+workers?\s+killed|medics?\s+killed", re.I)),
    ("supply_disruption", True, re.compile(
        r"pharmaceutical|medical\s+supplies|medicines?\b|insulin|dialysis", re.I)),
    ("facility_attack", True, re.compile(
        r"(hospital|clinic\b|ambulance|medical\s+(?:center|centre|research)|health\s*facilit)", re.I)),
    ("system_report", False, re.compile(r".", re.I)),  # fallback: surveillance/report
]

# Report-flavoured rows: even when a facility keyword is present, rows from
# the HUMANITARIAN timeline that are cumulative situation reports (WHO tolls,
# ministry bulletins, damage inventories) are surveillance signals, not new
# discrete insults. They are classified `system_report` by this override.
REPORT_PAT = re.compile(
    r"(WHO\s+(?:reports?|verified|:)|Ministry|MoPH|Legal\s+Medicine|"
    r"Red\s+Crescent\s+(?:reports?|:|issued)|toll|cumulative|figures|"
    r"bulletin|damage\s+assessment\s*:|infrastructure\s*:)", re.I)

# --------------------------------------------------------------------------- #
# Manual audit layer for the health-system register.
#
# The keyword rules above were applied to the v1.2 dataset and every matching
# row was then read and audited by the authors. Three kinds of corrections
# were required; each is recorded here BY EVENT ID with its reason, so the
# audit is fully reproducible and contestable. `00_build_panel.py` verifies at
# run time that each audited event still exists and still contains the
# anchoring text, so silent upstream drift fails loudly.
# --------------------------------------------------------------------------- #

# (1) Reclassifications: rule category was wrong for these rows.
#     event_id -> (category, insult, anchor_text, reason)
AUDIT_RECLASS = {
    "EVT-0207": ("system_report", False, "31 healthcare workers killed",
                 "HRW cumulative toll report; documents workforce harm, is not itself a new insult"),
    "EVT-0273": ("system_report", False, "25 hospitals damaged in Iran",
                 "ICRC facility-damage inventory report (25 damaged / 9 out of service)"),
    "EVT-0418": ("system_report", False, "50+ strikes in Lebanon",
                 "Strike-tempo report; health terms appear in an appended situation note"),
    "EVT-0498": ("system_report", False, "French chief warrant officer",
                 "UNIFIL peacekeeper fatality; health terms come from an appended MoPH toll citation"),
    "EVT-0457": ("access_disruption", True, "WHO Dubai hub ON HOLD",
                 "WHO emergency logistics hub suspended - humanitarian access insult, not a facility attack"),
    "EVT-0548": ("access_disruption", True, "lifesaving medical supplies",
                 "Medical-supply cargo seized under blockade - access/supply-chain insult"),
}

# (2) Exclusions: keyword match is incidental; row is not a health-system event.
#     event_id -> (anchor_text, reason)
AUDIT_EXCLUDE = {
    "EVT-0322": ("Sheba Medical", "Receiving hospital treating the wounded; health system is not the target"),
    "EVT-0468": ("considering limited military strikes", "Deliberation/threat reporting; no health-system event occurred"),
    "EVT-0335": ("170 targets", "Narrative summary duplicating Day 33-34 strike-file rows (Qeshm plant, medical research center, pharmaceutical facilities)"),
    "EVT-1012": ("Muwaffaq Salti", "US KIA event; Bonji desalination mention duplicates strike-file record EVT-1854"),
    "EVT-0191": ("Dimona and Arad", "Receiving hospital (Soroka mass-casualty declaration); demand-surge signal, not an attack on the health system"),
    "EVT-2169": ("Soroka Hospital", "Duplicate of EVT-0191 (strike-file row); same receiving-hospital rationale"),
}

# Benchmark anchors for the Iranian health-facility damage curve: cumulative
# "health facilities damaged" figures reported by named institutions inside
# dataset events. Verified at run time against their anchor rows. The ICRC
# Day-28 figure (25 damaged / 9 out of service, EVT-0273) is *lower* than the
# Day-15 ministry-linked figure and is therefore excluded from the monotone
# curve; the divergence is analyzed as a political fact in 07.
#   (day, cumulative facilities damaged, event_id, anchor_text, source label)
FACILITY_BENCHMARKS = [
    (15, 31, "EVT-0094", "31 major hospitals damaged", "Iran Health Ministry / Red Crescent reporting"),
    (39, 307, "EVT-0390", "307 health facilities damaged", "WHO"),
    (170, 309, "EVT-3304", "309 health facilities", "Iranian Red Crescent Society (IRCS)"),
]

# (3) Merges: rows describing the same physical incident. The first-listed id
#     is canonical (counts once in the HSSI); the rest are flagged duplicates.
#     group -> ([canonical_id, dup_id, ...], anchor_text, reason)
AUDIT_MERGE = {
    "tofigh-daru": (["EVT-0324", "EVT-1765"], "Tofigh Daru",
                    "Same incident: pharmaceutical factory strike killing 10 nurses (timeline + strike-file rows)"),
    "qeshm-desal": (["EVT-1769", "EVT-1775"], "Qeshm",
                    "Same facility struck on consecutive days (two strike-file records); counted once, conservatively"),
    "kuwait-desal-jul": (["EVT-1019", "EVT-2417"], "desalination",
                         "Same incident: Kuwaiti power-and-desalination plants struck Jul 17-18 (timeline + strike-file rows)"),
    "habbaniyah-clinic": (["EVT-2185", "EVT-0238"], "Habbaniyah",
                          "Same incident: US strike on the Habbaniyah Military Clinic (strike-file + timeline rows)"),
    "lebanon-sunday-apr19": (["EVT-0506", "EVT-2297"], "Red Cross paramedic",
                             "Same incident: Apr 19 Lebanon Sunday toll incl. Red Cross paramedic (Day-51 timeline + Day-52 strike-file rows)"),
}

# Civilian-facing strike classification. A strike-file location is
# civilian-facing when its coded target type is civilian-facing or its target
# description names civilian-facing infrastructure. Everything else in the
# STRIKE domain is treated as military-facing.
CIVFAC_TYPES = {"civilian", "oil_infrastructure", "communications", "water_infrastructure"}
CIVFAC_PAT = re.compile(
    r"hospital|clinic|medical|pharmac|school|residential|civilian|"
    r"desalination|water|power\s+plant|electric|refinery|oil|gas\b|petrochemical|"
    r"IRIB|broadcast|airport", re.I)


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def load_events() -> pd.DataFrame:
    """Load the pinned event dataset (conflict days only kept downstream)."""
    df = pd.read_csv(dataset_path(), low_memory=False)
    return df


# --------------------------------------------------------------------------- #
# Health-system event register
# --------------------------------------------------------------------------- #
def classify_health_event(desc: str, event_type: str = "") -> tuple[str, bool]:
    """Return (rule category, insult) for a health-matching description."""
    if event_type == "infrastructure_damage":
        # Cumulative as-of damage inventories, not discrete events.
        return "system_report", False
    if REPORT_PAT.search(desc) and not re.search(
            r"struck|strike\s+on|hit\b|destroyed|ablaze|killed\s+by", desc, re.I):
        # Cumulative reports/bulletins that do not themselves describe a strike.
        return "system_report", False
    for cat, insult, pat in HEALTH_CATEGORIES:
        if pat.search(desc):
            return cat, insult
    return "system_report", False


def verify_audit_anchors(df: pd.DataFrame) -> None:
    """Assert every audited event id still exists and contains its anchor
    text, so the manual audit cannot silently drift from the dataset."""
    idx = df.set_index("event_id")["event_description"].fillna("")
    checks = (
        [(eid, a) for eid, (_, _, a, _) in AUDIT_RECLASS.items()]
        + [(eid, a) for eid, (a, _) in AUDIT_EXCLUDE.items()]
        + [(eid, a) for _, (ids, a, _) in AUDIT_MERGE.items() for eid in ids]
        + [(eid, a) for _, _, eid, a, _ in FACILITY_BENCHMARKS]
    )
    for eid, anchor in checks:
        assert eid in idx.index, f"audited event {eid} missing from dataset"
        assert anchor.lower() in idx.loc[eid].lower(), \
            f"audit anchor '{anchor}' not found in {eid}"


def extract_health_events(df: pd.DataFrame) -> pd.DataFrame:
    """Build the health-system event register: one row per *distinct* reported
    health-system event, dated to its onset day, with the manual audit applied.

    Construction:
    1. Keyword screen (HEALTH_PAT) over STRIKE/RETALIATION/MILITARY/
       HUMANITARIAN rows, excluding headline-echo types and reference files.
    2. Strike-file locations de-duplicated on source_record_id (a location
       active on many days is one event, dated to its first active day).
    3. Rule classification into categories, then the documented manual audit
       (AUDIT_RECLASS / AUDIT_EXCLUDE / AUDIT_MERGE).

    Every screened row is RETAINED in the output with `audit_action` and
    `audit_note` columns; `counted` marks the rows that accumulate into the
    HSSI (insult events, net of exclusions and merge duplicates). Excluded
    and duplicate rows stay visible so the audit is inspectable.
    """
    verify_audit_anchors(df)

    conf = df[df.day_of_conflict >= 1].copy()
    conf = conf[conf.event_domain.isin(HEALTH_DOMAINS)]
    conf = conf[~conf.event_type.isin(ECHO_TYPES)]
    conf = conf[~conf.source_file.isin(REFERENCE_FILES)]
    desc = conf.event_description.fillna("")
    hits = conf[desc.str.contains(HEALTH_PAT)].copy()

    # De-duplicate the strike-file target x active-day explosion: keep the
    # first (onset) row per source location.
    sf_mask = hits.source_file.isin(STRIKE_FILES) & hits.source_record_id.notna()
    sf = (hits[sf_mask].sort_values("day_of_conflict")
          .drop_duplicates(subset=["source_record_id"], keep="first"))
    other = hits[~sf_mask]
    reg = pd.concat([sf, other], ignore_index=True).sort_values(
        ["day_of_conflict", "event_id"])

    cats = [classify_health_event(d, t) for d, t in
            zip(reg.event_description.fillna(""), reg.event_type.fillna(""))]
    reg["health_category"] = [c for c, _ in cats]
    reg["insult"] = [i for _, i in cats]
    reg["audit_action"] = "rule"
    reg["audit_note"] = ""
    reg["counted"] = reg["insult"]

    dup_ids = {d: (grp, reason) for grp, (ids, _, reason) in AUDIT_MERGE.items()
               for d in ids[1:]}
    canon_ids = {ids[0]: (grp, reason) for grp, (ids, _, reason) in AUDIT_MERGE.items()}

    for i, row in reg.iterrows():
        eid = row.event_id
        if eid in AUDIT_RECLASS:
            cat, insult, _, reason = AUDIT_RECLASS[eid]
            reg.loc[i, ["health_category", "insult", "counted"]] = cat, insult, insult
            reg.loc[i, ["audit_action", "audit_note"]] = "reclassified", reason
        elif eid in AUDIT_EXCLUDE:
            _, reason = AUDIT_EXCLUDE[eid]
            reg.loc[i, ["insult", "counted"]] = False, False
            reg.loc[i, ["audit_action", "audit_note"]] = "excluded", reason
        elif eid in dup_ids:
            grp, reason = dup_ids[eid]
            reg.loc[i, "counted"] = False
            reg.loc[i, ["audit_action", "audit_note"]] = \
                "merged_duplicate", f"[{grp}] {reason}"
        elif eid in canon_ids:
            grp, reason = canon_ids[eid]
            reg.loc[i, ["audit_action", "audit_note"]] = \
                "merged_canonical", f"[{grp}] {reason}"

    cols = ["event_id", "day_of_conflict", "date", "event_domain", "event_type",
            "health_category", "insult", "counted", "audit_action", "audit_note",
            "data_confidence", "country", "location_name", "source_file",
            "event_description"]
    return reg[cols].reset_index(drop=True)


# --------------------------------------------------------------------------- #
# Daily-panel construction
# --------------------------------------------------------------------------- #
def _domain_daily_dedup(conf: pd.DataFrame, domain: str) -> pd.Series:
    """Daily tempo count for a domain, de-duplicating the strike-file
    target x active_day explosion (Paper 1's primary operationalization):
    distinct source locations active per day plus discrete non-strike-file
    rows."""
    d = conf[conf.event_domain == domain]
    sf = d[d.source_file.isin(STRIKE_FILES)]
    loc = sf.groupby("day_of_conflict")["source_record_id"].nunique()
    other = d[~d.source_file.isin(STRIKE_FILES)].groupby("day_of_conflict").size()
    s = loc.add(other, fill_value=0)
    return s.reindex(DAYS, fill_value=0).astype(int)


def _strike_civfac_masks(conf: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """STRIKE-domain strike-file rows plus a boolean civilian-facing mask."""
    stk = conf[(conf.event_domain == "STRIKE")
               & conf.source_file.isin(STRIKE_FILES)
               & conf.source_record_id.notna()].copy()
    m_type = stk.infrastructure_target_type.isin(CIVFAC_TYPES)
    m_text = stk.event_description.fillna("").str.contains(CIVFAC_PAT)
    return stk, (m_type | m_text)


def build_panel() -> pd.DataFrame:
    """Construct the daily analysis panel (Day 1..170).

    Columns (full definitions in docs/CODEBOOK_panel.md)
    ---------------------------------------------------
    day, date, phase
    strikes          : offensive strike tempo (distinct locations + discrete events)
    retal            : retaliation tempo (same operationalization)
    strikes_civfac   : distinct civilian-facing strike locations active that day
    strikes_milfac   : distinct military-facing strike locations active that day
    health_insults   : new distinct health-system insult events with onset that day
    hssi             : cumulative health-system insult count through day t
    hssi_pct         : hssi min-max normalized to 0-100 over Days 1-170
    iran_civ, iran_mil, us_mil, leb_all, isr_mil : daily estimated killed by faction
    killed_total     : sum across the five factions
    cum_iran_daily   : running sum of iran_civ + iran_mil (daily-series cumulative)
    cum_leb_daily    : running sum of leb_all
    snap_iranian_killed, snap_lebanese_killed, snap_displaced, snap_children_killed :
                       dashboard cumulative snapshots, linearly interpolated
                       between observed snapshot days (raw coverage 107-126/170)
    conf_high_share  : share of that day's STRIKE+RETALIATION+casualty rows
                       rated data_confidence == HIGH
    strike_day       : 1 if strikes > 0
    kinetic_day      : 1 if strikes > 0 or retal > 0
    """
    df = load_events()
    conf = df[df.day_of_conflict >= 1].copy()

    panel = pd.DataFrame({"day": DAYS})
    panel["date"] = [date_from_day(d).isoformat() for d in DAYS]
    panel["phase"] = [phase_of(d) for d in DAYS]

    panel["strikes"] = _domain_daily_dedup(conf, "STRIKE").values
    panel["retal"] = _domain_daily_dedup(conf, "RETALIATION").values

    # Civilian-facing vs military-facing strike tempo. Classified at the
    # location-day level: a location counts as civilian-facing on day t if ANY
    # of its target rows that day is civilian-facing (multi-target locations
    # would otherwise be double-counted across the two series).
    stk, civ_mask = _strike_civfac_masks(conf)
    locday = (stk.assign(civ=civ_mask)
              .groupby(["day_of_conflict", "source_record_id"])["civ"].any()
              .reset_index())
    civ = locday[locday.civ].groupby("day_of_conflict").size()
    mil = locday[~locday.civ].groupby("day_of_conflict").size()
    panel["strikes_civfac"] = civ.reindex(DAYS, fill_value=0).astype(int).values
    panel["strikes_milfac"] = mil.reindex(DAYS, fill_value=0).astype(int).values

    # Health-system insult accumulation (the HSSI): audited insult events
    # only (`counted` excludes reports, audit exclusions, merge duplicates).
    hreg = extract_health_events(df)
    ins = hreg[hreg.counted].groupby("day_of_conflict").size()
    panel["health_insults"] = ins.reindex(DAYS, fill_value=0).astype(int).values
    panel["hssi"] = panel["health_insults"].cumsum()
    rng = panel["hssi"].max() - panel["hssi"].min()
    panel["hssi_pct"] = 100.0 * (panel["hssi"] - panel["hssi"].min()) / (rng if rng else 1)

    # Benchmark-anchored facility-damage curve (Iran): piecewise-linear
    # interpolation through institutionally reported cumulative counts,
    # starting from 0 on Day 0 and flat after the last benchmark.
    bench = pd.Series(np.nan, index=DAYS, dtype=float)
    prev_day, prev_val = 0, 0.0
    for bday, bval, _, _, _ in FACILITY_BENCHMARKS:
        span = bday - prev_day
        for d in range(prev_day + 1, bday + 1):
            bench.loc[d] = prev_val + (bval - prev_val) * (d - prev_day) / span
        prev_day, prev_val = bday, float(bval)
    bench.loc[prev_day:] = prev_val
    panel["facil_damage_bench"] = bench.values
    panel["facil_damage_pct"] = 100.0 * bench.values / bench.max()

    # Daily estimated killed by faction (casualties.json; not cumulative).
    cas = conf[conf.source_file == "casualties.json"].copy()
    cas["v"] = pd.to_numeric(cas["casualties_reported"], errors="coerce")
    piv = cas.pivot_table(index="day_of_conflict", columns="actor_target",
                          values="v", aggfunc="sum").reindex(DAYS, fill_value=0)
    faction_cols = {
        "Iran (civilian)": "iran_civ", "Iran (military)": "iran_mil",
        "US (military)": "us_mil", "Lebanon (all)": "leb_all",
        "Israel (military)": "isr_mil",
    }
    for src, col in faction_cols.items():
        panel[col] = piv[src].fillna(0).astype(int).values
    panel["killed_total"] = panel[list(faction_cols.values())].sum(axis=1)
    panel["cum_iran_daily"] = (panel["iran_civ"] + panel["iran_mil"]).cumsum()
    panel["cum_leb_daily"] = panel["leb_all"].cumsum()

    # Dashboard cumulative snapshots, interpolated across unobserved days.
    snap = (conf[conf.event_type == "daily_aggregate_snapshot"]
            .sort_values("day_of_conflict").set_index("day_of_conflict"))
    for src, col in [("snapshot_iranian_killed", "snap_iranian_killed"),
                     ("snapshot_lebanese_killed", "snap_lebanese_killed"),
                     ("snapshot_displaced", "snap_displaced"),
                     ("snapshot_children_killed", "snap_children_killed")]:
        s = pd.to_numeric(snap[src], errors="coerce").dropna()
        s = s[~s.index.duplicated(keep="last")].reindex(DAYS)
        panel[col] = s.interpolate(method="linear", limit_direction="forward").values

    # Confidence mix of the day's kinetic + casualty evidence base.
    ev = conf[conf.event_domain.isin(("STRIKE", "RETALIATION"))
              | (conf.source_file == "casualties.json")]
    hi = (ev.assign(hi=(ev.data_confidence == "HIGH").astype(float))
          .groupby("day_of_conflict")["hi"].mean())
    panel["conf_high_share"] = hi.reindex(DAYS).fillna(np.nan).values

    panel["strike_day"] = (panel["strikes"] > 0).astype(int)
    panel["kinetic_day"] = ((panel["strikes"] > 0) | (panel["retal"] > 0)).astype(int)

    return panel.set_index("day")


def load_panel() -> pd.DataFrame:
    """Load the pre-built panel (built by 00_build_panel.py)."""
    p = DATA_DIR / "panel_daily.csv"
    if not p.exists():
        raise FileNotFoundError(f"{p} not found — run 00_build_panel.py first.")
    return pd.read_csv(p).set_index("day")


def load_health_register() -> pd.DataFrame:
    p = DATA_DIR / "health_system_events.csv"
    if not p.exists():
        raise FileNotFoundError(f"{p} not found — run 00_build_panel.py first.")
    return pd.read_csv(p)


# --------------------------------------------------------------------------- #
# Small statistics helpers shared across scripts
# --------------------------------------------------------------------------- #
def hedges_g(a: np.ndarray, b: np.ndarray) -> float:
    """Hedges' g (bias-corrected standardized mean difference)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    if sp == 0:
        return 0.0
    d = (a.mean() - b.mean()) / sp
    J = 1 - 3 / (4 * (na + nb) - 9)          # small-sample correction
    return float(d * J)


def welch_anova(groups: list[np.ndarray]) -> tuple[float, float, float]:
    """Welch's heteroscedasticity-robust one-way ANOVA.
    Returns (F, df2, p). df1 = k - 1."""
    from scipy import stats
    k = len(groups)
    ns = np.array([len(g) for g in groups], float)
    ms = np.array([np.mean(g) for g in groups])
    vs = np.array([np.var(g, ddof=1) for g in groups])
    w = ns / vs
    mw = np.sum(w * ms) / np.sum(w)
    A = np.sum(w * (ms - mw) ** 2) / (k - 1)
    B = 1 + (2 * (k - 2) / (k ** 2 - 1)) * np.sum((1 - w / np.sum(w)) ** 2 / (ns - 1))
    F = A / B
    df2 = (k ** 2 - 1) / (3 * np.sum((1 - w / np.sum(w)) ** 2 / (ns - 1)))
    p = stats.f.sf(F, k - 1, df2)
    return float(F), float(df2), float(p)


def holm(pvals: list[float]) -> list[float]:
    """Holm step-down adjusted p-values."""
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (m - rank) * pvals[idx]
        running = max(running, val)
        adj[idx] = min(running, 1.0)
    return adj.tolist()


# --------------------------------------------------------------------------- #
# Plotting (matplotlib; Okabe-Ito colorblind-safe palette; matches Paper 1)
# --------------------------------------------------------------------------- #
C_STRIKE = "#0072B2"   # blue  — strikes / kinetic exposure
C_RETAL = "#D55E00"    # vermilion — retaliation
C_KILLED = "#000000"   # black — casualties
C_HEALTH = "#009E73"   # green — health system
C_ACCENT = "#CC79A7"   # purple accent
C_GOLD = "#E69F00"     # orange — projections / scenarios
C_SKY = "#56B4E9"      # sky blue — secondary series
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


def shade_phases(ax):
    """Shade the four documented phases behind a day-indexed axis."""
    for i, (name, lo, hi) in enumerate(PHASES):
        ax.axvspan(lo - 0.5, hi + 0.5, color=PHASE_SHADE[i % len(PHASE_SHADE)],
                   zorder=0, alpha=0.7)


def phase_labels(ax, y, fontsize=7.0):
    for name, lo, hi in PHASES:
        ax.text((lo + hi) / 2, y, name.upper(), fontsize=fontsize, color="0.35",
                ha="center", va="center")


def savefig(fig, name: str):
    """Save a figure to both PNG and PDF in output/figures."""
    for ext in ("png", "pdf"):
        fig.savefig(FIG_DIR / f"{name}.{ext}", bbox_inches="tight")
    print(f"  wrote output/figures/{name}.png (+.pdf)")
