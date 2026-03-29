#!/usr/bin/env python3
"""
IranWar.ai Research Dataset Builder
====================================
Transforms structured JSON data from the WarTheater dashboard into a single
event-level CSV dataset for quantitative research.

See seed.md for full specification.

Usage:
    cd ResearchData/
    python3 build_dataset.py
"""

import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CONFLICT_START = date(2026, 2, 28)   # Day 1
BASELINE_DATE = date(2026, 2, 27)    # Day 0
DATA_DIR = Path(__file__).resolve().parent.parent / "public" / "data"
OUT_DIR = Path(__file__).resolve().parent

# Global event counter
_event_counter = 0


def next_event_id() -> str:
    global _event_counter
    _event_counter += 1
    return f"EVT-{_event_counter:04d}"


def war_day(d: date) -> int:
    """Return day-of-conflict integer. Day 0 = pre-war baseline, Day 1 = Feb 28."""
    delta = (d - BASELINE_DATE).days
    return max(delta, 0)


def date_from_war_day(day: int) -> date:
    return BASELINE_DATE + timedelta(days=day)


def parse_short_date(label: str, year: int = 2026) -> date:
    """Parse labels like 'Mar 27', 'Feb 5', 'Jan 2' into date objects."""
    label = label.strip()
    for fmt in ("%b %d", "%B %d"):
        try:
            dt = datetime.strptime(f"{label} {year}", f"{fmt} %Y")
            return dt.date()
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date label: '{label}'")


def load_json(filename: str):
    """Load a JSON file from the data directory. Returns None on failure."""
    path = DATA_DIR / filename
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading {filename}: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Output schema — every row has these columns (NULL where not applicable)
# ---------------------------------------------------------------------------
REQUIRED_COLS = [
    "event_id", "date", "datetime_utc", "day_of_conflict",
    "event_domain", "event_type", "event_description",
    "source_file", "source_record_id",
]

DOMAIN_COLS = [
    "location_name", "location_lat", "location_lon", "country",
    "actor_initiating", "actor_target",
    "weapon_system", "military_asset",
    "casualties_reported", "casualties_civilian", "casualties_military",
    "infrastructure_target_type",
    "financial_metric_name", "financial_metric_value", "financial_metric_unit",
    "escalation_level", "data_confidence",
]

EXTRA_COLS = [
    "timeline_source", "timeline_data_point",
    "strike_notes", "strike_verified",
    "naval_strike_group", "naval_aircraft", "naval_escorts",
    "infrastructure_damage_count",
    "snapshot_brent", "snapshot_wti", "snapshot_gas", "snapshot_sp500",
    "snapshot_daily_cost_millions", "snapshot_total_cost_billions",
    "snapshot_targets_struck", "snapshot_us_kia", "snapshot_us_wia",
    "snapshot_iranian_killed", "snapshot_lebanese_killed",
    "snapshot_displaced", "snapshot_flights_cancelled",
    "snapshot_children_killed",
]

ALL_COLS = REQUIRED_COLS + DOMAIN_COLS + EXTRA_COLS


def empty_row() -> dict:
    return {c: None for c in ALL_COLS}


# ---------------------------------------------------------------------------
# Phase 1: timeline-events.json
# ---------------------------------------------------------------------------
RETALIATION_PATTERNS = re.compile(
    r"Iran retaliates|Iranian.*(?:launch|fire|strike)|Hezbollah|IRGC launch|"
    r"Houthi|Iraqi militia|proxy.*attack|Shahed|ballistic missile.*(?:salvo|wave)|"
    r"retaliatory|counter-?strike",
    re.IGNORECASE,
)
STRIKE_PATTERNS = re.compile(
    r"US strike|U\.S\. strike|Israeli.*strike|B-2|B-52|Tomahawk|CENTCOM.*strike|"
    r"IDF.*strike|coalition strike|GBU-57|Operation Epic Fury begins|"
    r"air campaign|bombing|airstrike|munitions|sortie",
    re.IGNORECASE,
)

CATEGORY_DOMAIN_MAP = {
    "financial": "FINANCIAL",
    "economic": "FINANCIAL",
    "diplomatic": "DIPLOMATIC",
    "humanitarian": "HUMANITARIAN",
    "cyber": "CYBER",
    "political": "DIPLOMATIC",
    "domestic": "DIPLOMATIC",
    "summary": "OTHER",
}


def classify_military_event(title: str, desc: str) -> str:
    text = f"{title} {desc}"
    if RETALIATION_PATTERNS.search(text):
        return "RETALIATION"
    if STRIKE_PATTERNS.search(text):
        return "STRIKE"
    return "MILITARY"


def extract_timeline_events() -> list[dict]:
    data = load_json("timeline-events.json")
    if data is None:
        return []

    rows = []
    for rec in data:
        row = empty_row()
        row["event_id"] = next_event_id()

        # Date
        d = date.fromisoformat(rec["date"])
        row["date"] = d.isoformat()
        row["day_of_conflict"] = war_day(d)

        # Datetime — time field is like "02:00", "14:00". Store as local time
        # with note that timezone is approximate (events span multiple zones).
        t = rec.get("time")
        if t:
            row["datetime_utc"] = f"{d.isoformat()}T{t}:00"

        # Domain mapping
        cat = rec.get("category", "other").lower()
        if cat == "military":
            row["event_domain"] = classify_military_event(
                rec.get("title", ""), rec.get("description", "")
            )
        else:
            row["event_domain"] = CATEGORY_DOMAIN_MAP.get(cat, "OTHER")

        row["event_type"] = cat
        row["event_description"] = f"{rec.get('title', '')}: {rec.get('description', '')}"
        row["source_file"] = "timeline-events.json"
        row["source_record_id"] = None
        row["data_confidence"] = "HIGH"

        # Extra columns
        row["timeline_source"] = rec.get("source")
        row["timeline_data_point"] = rec.get("data_point")

        rows.append(row)

    print(f"  timeline-events.json: {len(rows)} events extracted")
    return rows


# ---------------------------------------------------------------------------
# Placeholder stubs for Phases 2–7 (to be implemented in later phases)
# ---------------------------------------------------------------------------
def infer_infrastructure_type(target_text: str, subtype: str | None = None) -> str | None:
    """Infer infrastructure_target_type from target description or subtype."""
    if subtype in ("civilian_casualty", "civilian_casualties", "civilian_infrastructure"):
        return "civilian"
    if subtype == "energy_infrastructure":
        return "oil_infrastructure"
    if subtype == "targeted_killing":
        return "military_base"
    text = target_text.lower()
    if any(k in text for k in ("nuclear", "enrichment", "reactor", "uranium",
                                "heavy water", "yellowcake", "fordow", "natanz")):
        return "nuclear_facility"
    if any(k in text for k in ("oil", "refinery", "gas", "kharg", "petrochemical",
                                "fuel", "south pars", "pipeline", "lng")):
        return "oil_infrastructure"
    if any(k in text for k in ("school", "residential", "civilian", "hospital",
                                "bazaar", "palace", "stadium", "mosque", "university")):
        return "civilian"
    if any(k in text for k in ("radar", "air defense", "s-300", "s-200", "sam site")):
        return "air_defense"
    if any(k in text for k in ("irib", "broadcaster", "communications", "radio",
                                "transmitter", "cyber")):
        return "communications"
    if any(k in text for k in ("airbase", "air base", "runway", "naval", "irgc",
                                "missile", "military", "command", "drone base",
                                "submarine", "hangar", "weapon", "munition",
                                "artillery", "fast attack", "leadership")):
        return "military_base"
    return None


def assess_strike_confidence(rec: dict) -> str:
    """Assess data confidence for a strike record."""
    src = (rec.get("casualties_source") or "").lower()
    if rec.get("verified") is False:
        return "LOW"
    if any(k in src for k in ("dod", "centcom", "idf", "iaea", "pentagon")):
        return "HIGH"
    if any(k in src for k in ("acled", "satellite")):
        return "MEDIUM"
    if any(k in src for k in ("wikipedia", "unconfirmed", "unverified")):
        return "LOW"
    return "MEDIUM"


def extract_strikes_iran() -> list[dict]:
    """Phase 2: Extract US/Israeli strikes on Iran, exploded by target x active_day."""
    data = load_json("strikes-iran.json")
    if data is None:
        return []

    records = [r for r in data if r.get("id") != "_metadata"]
    rows = []

    for rec in records:
        targets = rec.get("targets", [])
        active_days = rec.get("active_days", [])
        subtype = rec.get("subtype")
        confidence = assess_strike_confidence(rec)

        for day_num in active_days:
            d = date_from_war_day(day_num)
            for target_desc in targets:
                row = empty_row()
                row["event_id"] = next_event_id()
                row["date"] = d.isoformat()
                row["datetime_utc"] = None
                row["day_of_conflict"] = day_num
                row["event_domain"] = "STRIKE"
                row["event_type"] = "airstrike"
                row["event_description"] = f"{rec.get('city', '')}: {target_desc}"
                row["source_file"] = "strikes-iran.json"
                row["source_record_id"] = rec.get("id")

                row["location_name"] = rec.get("city")
                row["location_lat"] = rec.get("lat")
                row["location_lon"] = rec.get("lng")
                row["country"] = "Iran"

                # Normalize actor
                actor = rec.get("actor", "")
                actor_map = {
                    "us": "US",
                    "israel": "Israel",
                    "us_israel_joint": "US/Israel (joint)",
                    "israel_us_coordinated": "US/Israel (coordinated)",
                    "unknown": "Unknown",
                }
                row["actor_initiating"] = actor_map.get(actor, actor)
                row["actor_target"] = "Iran"

                row["infrastructure_target_type"] = infer_infrastructure_type(
                    target_desc, subtype
                )

                # Casualties — attach to first target only to avoid double-counting
                if target_desc == targets[0]:
                    row["casualties_reported"] = rec.get("casualties_reported")

                row["data_confidence"] = confidence
                row["strike_notes"] = rec.get("notes")

                rows.append(row)

    print(f"  strikes-iran.json: {len(rows)} events extracted "
          f"({len(records)} locations x targets x active_days)")
    return rows


COUNTRY_PATTERNS = [
    ("Israel", re.compile(r"Israel|Tel Aviv|Haifa|Nevatim|Dimona|Beit Shemesh|Beersheba|Jerusalem|Netanya|Eilat|Nahariya|Ramat Gan|Kafr Qasim|Ganei Tikva|Kiryat Ata", re.I)),
    ("Kuwait", re.compile(r"Kuwait", re.I)),
    ("Qatar", re.compile(r"Qatar|Al Udeid|Doha", re.I)),
    ("UAE", re.compile(r"UAE|Dubai|Abu Dhabi|Fujairah|Al Dhafra|Umm Al Quwain|Jebel Ali|Ruwais|Habshan", re.I)),
    ("Bahrain", re.compile(r"Bahrain|NAVCENT|Bapco", re.I)),
    ("Iraq", re.compile(r"Iraq|Erbil|Ain al-Asad|Habbaniyah|Baghdad|Kurdistan", re.I)),
    ("Saudi Arabia", re.compile(r"Saudi|Prince Sultan|Ras Tanura|SAMREF|Yanbu|Al-Kharj", re.I)),
    ("Lebanon", re.compile(r"Lebanon|Beirut|Tyre|Litani|Sidon|Jezzine|Nabatieh", re.I)),
    ("Jordan", re.compile(r"Jordan", re.I)),
    ("Cyprus", re.compile(r"Cyprus|Akrotiri", re.I)),
    ("Oman", re.compile(r"Oman|Duqm|Salalah|Sohar", re.I)),
    ("International Waters", re.compile(r"Hormuz|maritime|Gulf of Oman|Arabian Sea", re.I)),
    ("Diego Garcia", re.compile(r"Diego Garcia", re.I)),
]


def extract_country(city: str) -> str:
    """Extract country from city/location string."""
    for country, pattern in COUNTRY_PATTERNS:
        if pattern.search(city):
            return country
    return "Unknown"


def extract_strikes_retaliation() -> list[dict]:
    """Phase 3: Extract Iranian retaliation / Hezbollah / operational loss events."""
    data = load_json("strikes-retaliation.json")
    if data is None:
        return []

    type_to_event_type = {
        "iran_retaliation": "missile_attack",
        "hezbollah_front": "rocket_attack",
        "hezbollah": "rocket_attack",
        "operational_loss": "operational_loss",
        "us_strike_on_militia": "airstrike",
    }

    type_to_domain = {
        "iran_retaliation": "RETALIATION",
        "hezbollah_front": "RETALIATION",
        "hezbollah": "RETALIATION",
        "operational_loss": "MILITARY",
        "us_strike_on_militia": "STRIKE",
    }

    rows = []
    for rec in data:
        active_days = rec.get("active_days", [])
        rec_type = rec.get("type", "iran_retaliation")
        confidence = "HIGH" if rec.get("verified") else "LOW"
        country = extract_country(rec.get("city", ""))

        # Determine initiating actor from origin or type
        if rec_type == "us_strike_on_militia":
            actor_init = "US"
            actor_tgt = rec.get("city", "")
        elif rec_type in ("hezbollah_front", "hezbollah"):
            actor_init = "Hezbollah"
            actor_tgt = country
        elif rec_type == "operational_loss":
            actor_init = None
            actor_tgt = None
        else:
            actor_init = rec.get("origin", "Iran")
            actor_tgt = country

        for day_num in active_days:
            d = date_from_war_day(day_num)
            row = empty_row()
            row["event_id"] = next_event_id()
            row["date"] = d.isoformat()
            row["datetime_utc"] = None
            row["day_of_conflict"] = day_num
            row["event_domain"] = type_to_domain.get(rec_type, "RETALIATION")
            row["event_type"] = type_to_event_type.get(rec_type, "missile_attack")
            row["event_description"] = (
                f"{rec.get('city', '')}: {rec.get('weapon', 'Unknown weapon')} — "
                f"{rec.get('casualties_reported', 'No casualty data')}"
            )
            row["source_file"] = "strikes-retaliation.json"
            row["source_record_id"] = rec.get("id")

            row["location_name"] = rec.get("city")
            row["location_lat"] = rec.get("lat")
            row["location_lon"] = rec.get("lng")
            row["country"] = country

            row["actor_initiating"] = actor_init
            row["actor_target"] = actor_tgt
            row["weapon_system"] = rec.get("weapon")

            # Casualties on first active day only to avoid double-counting
            if day_num == active_days[0]:
                row["casualties_reported"] = rec.get("casualties_reported")

            row["data_confidence"] = confidence
            row["strike_notes"] = rec.get("notes")
            row["strike_verified"] = rec.get("verified")

            rows.append(row)

    print(f"  strikes-retaliation.json: {len(rows)} events extracted "
          f"({len(data)} locations x active_days)")
    return rows


def extract_carriers() -> list[dict]:
    """Phase 4a: Extract naval asset deployment/positioning events."""
    data = load_json("carriers.json")
    if data is None:
        return []

    rows = []
    for rec in data:
        row = empty_row()
        row["event_id"] = next_event_id()

        # Use operation_start_date, fall back to deployed_since, then conflict start
        d_str = rec.get("operation_start_date") or rec.get("deployed_since")
        if d_str:
            d = date.fromisoformat(d_str)
        else:
            d = CONFLICT_START
        row["date"] = d.isoformat()
        row["datetime_utc"] = None
        row["day_of_conflict"] = war_day(d)

        row["event_domain"] = "NAVAL"
        row["event_type"] = rec.get("type", "naval_asset")
        row["event_description"] = (
            f"{rec.get('name', '')} ({rec.get('hull') or 'N/A'}) — "
            f"{rec.get('status', '')} — {rec.get('mission_summary', '')}"
        )
        row["source_file"] = "carriers.json"
        row["source_record_id"] = rec.get("id")

        row["location_name"] = rec.get("area")
        row["location_lat"] = rec.get("lat")
        row["location_lon"] = rec.get("lng")
        row["military_asset"] = f"{rec.get('name', '')} ({rec.get('hull') or 'N/A'})"

        # Determine actor
        name = (rec.get("name") or "").lower()
        hull = (rec.get("hull") or "").lower()
        if "hms" in name or hull.startswith("s1") or hull.startswith("d3"):
            row["actor_initiating"] = "UK"
        elif name.startswith("fs "):
            row["actor_initiating"] = "France"
        elif "82nd airborne" in name.lower():
            row["actor_initiating"] = "US"
        else:
            row["actor_initiating"] = "US"

        row["data_confidence"] = "HIGH"

        # Extra naval columns
        row["naval_strike_group"] = rec.get("strike_group")
        row["naval_aircraft"] = rec.get("aircraft") if isinstance(rec.get("aircraft"), str) else None
        escorts = rec.get("escorts", [])
        if escorts:
            row["naval_escorts"] = "; ".join(escorts)

        row["strike_notes"] = rec.get("notes")
        rows.append(row)

    print(f"  carriers.json: {len(rows)} naval asset events extracted")
    return rows


def extract_casualties() -> list[dict]:
    """Phase 4b: Extract daily casualty reports (day x faction)."""
    data = load_json("casualties.json")
    if data is None:
        return []

    labels = data.get("labels", [])
    day_contexts = data.get("day_contexts", [])
    datasets = data.get("datasets", {})

    faction_meta = {
        "iranian_military": ("Iran (military)", "military"),
        "iranian_civilian": ("Iran (civilian)", "civilian"),
        "us_military": ("US (military)", "military"),
        "lebanese": ("Lebanon (all)", "all"),
        "israeli_military": ("Israel (military)", "military"),
    }

    rows = []
    for i, label in enumerate(labels):
        d = parse_short_date(label, 2026)
        day_num = war_day(d)
        context = day_contexts[i] if i < len(day_contexts) else ""

        for faction_key, (actor_label, cas_type) in faction_meta.items():
            ds = datasets.get(faction_key, {})
            values = ds.get("data", [])
            if i >= len(values):
                continue
            value = values[i]

            row = empty_row()
            row["event_id"] = next_event_id()
            row["date"] = d.isoformat()
            row["datetime_utc"] = None
            row["day_of_conflict"] = day_num
            row["event_domain"] = "HUMANITARIAN"
            row["event_type"] = "daily_casualty_report"
            row["event_description"] = (
                f"Day {day_num} estimated killed — {actor_label}: {value}. "
                f"Context: {context}"
            )
            row["source_file"] = "casualties.json"
            row["source_record_id"] = None
            row["actor_target"] = actor_label
            row["casualties_reported"] = value

            if cas_type == "military":
                row["casualties_military"] = value
            elif cas_type == "civilian":
                row["casualties_civilian"] = value

            row["data_confidence"] = "MEDIUM"
            rows.append(row)

    print(f"  casualties.json: {len(rows)} daily casualty events extracted "
          f"({len(labels)} days x {len(faction_meta)} factions)")
    return rows


def extract_infrastructure() -> list[dict]:
    """Phase 4c: Extract cumulative infrastructure damage records."""
    data = load_json("infrastructure.json")
    if data is None:
        return []

    infra_type_map = {
        "Hospitals Damaged": "healthcare",
        "Schools Destroyed": "civilian",
        "Power Plants Hit": "power_grid",
        "Oil/Gas Facilities Hit": "oil_infrastructure",
        "Nuclear Facilities Struck": "nuclear_facility",
        "Airports Damaged": "air_defense",
        "Bridges Destroyed": "transportation",
    }

    rows = []
    for rec in data:
        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = "2026-03-29"  # cumulative as-of date
        row["datetime_utc"] = None
        row["day_of_conflict"] = 30
        row["event_domain"] = "HUMANITARIAN"
        row["event_type"] = "infrastructure_damage"
        row["event_description"] = rec.get("detail", rec.get("note", ""))
        row["source_file"] = "infrastructure.json"
        row["source_record_id"] = None

        label = rec.get("label", "")
        row["infrastructure_target_type"] = infra_type_map.get(label, "other")

        # Parse count — strip non-numeric chars like "+" and "~"
        count_str = str(rec.get("count", "")).strip()
        count_num = re.sub(r"[^\d]", "", count_str)
        if count_num:
            row["infrastructure_damage_count"] = int(count_num)

        row["data_confidence"] = "HIGH"
        row["strike_notes"] = rec.get("source")
        rows.append(row)

    print(f"  infrastructure.json: {len(rows)} infrastructure damage events extracted")
    return rows


def extract_oil_prices() -> list[dict]:
    """Phase 5a — TODO"""
    return []


def extract_markets() -> list[dict]:
    """Phase 5b — TODO"""
    return []


def extract_war_costs() -> list[dict]:
    """Phase 5c — TODO"""
    return []


def extract_baselines() -> list[dict]:
    """Phase 5d — TODO"""
    return []


def extract_hero_stats_history() -> list[dict]:
    """Phase 5e — TODO"""
    return []


def extract_hormuz() -> list[dict]:
    """Phase 6a — TODO"""
    return []


def extract_historical_comparison() -> list[dict]:
    """Phase 6b — TODO"""
    return []


def extract_global_bases() -> list[dict]:
    """Phase 6c — TODO"""
    return []


def extract_briefings() -> list[dict]:
    """Phase 6d — TODO"""
    return []


# ---------------------------------------------------------------------------
# Codebook generation (Phase 7)
# ---------------------------------------------------------------------------
def generate_codebook(df: pd.DataFrame) -> pd.DataFrame:
    """Introspect the dataset and produce a codebook."""
    codebook_rows = []
    for col in df.columns:
        series = df[col]
        non_null = series.dropna()

        # Determine type
        if col in ("date",):
            vtype = "date"
        elif col in ("datetime_utc",):
            vtype = "datetime"
        elif col in ("day_of_conflict", "casualties_reported", "casualties_civilian",
                      "casualties_military", "infrastructure_damage_count"):
            vtype = "integer"
        elif col in ("location_lat", "location_lon", "financial_metric_value",
                      "snapshot_brent", "snapshot_wti", "snapshot_gas",
                      "snapshot_sp500", "snapshot_daily_cost_millions",
                      "snapshot_total_cost_billions", "snapshot_targets_struck",
                      "snapshot_us_kia", "snapshot_us_wia", "snapshot_iranian_killed",
                      "snapshot_lebanese_killed", "snapshot_displaced",
                      "snapshot_flights_cancelled", "snapshot_children_killed"):
            vtype = "float"
        elif col in ("event_domain", "event_type", "data_confidence",
                      "infrastructure_target_type", "country",
                      "financial_metric_unit", "source_file"):
            vtype = "categorical"
        elif col in ("strike_verified",):
            vtype = "boolean"
        elif col in ("event_description", "strike_notes", "naval_aircraft",
                      "naval_escorts"):
            vtype = "text"
        else:
            vtype = "string"

        # Valid values
        if vtype == "categorical" and len(non_null) > 0:
            uniques = sorted(non_null.unique().tolist())
            valid = " | ".join(str(v) for v in uniques[:30])
        elif vtype in ("integer", "float") and len(non_null) > 0:
            try:
                nums = pd.to_numeric(non_null, errors="coerce").dropna()
                if len(nums) > 0:
                    valid = f"{nums.min():.4g} – {nums.max():.4g}"
                else:
                    valid = ""
            except Exception:
                valid = ""
        else:
            valid = ""

        # Missing meaning
        if col in REQUIRED_COLS:
            missing = "Should not be missing"
        elif col.startswith("snapshot_"):
            missing = "Not available for this day"
        elif col.startswith("timeline_"):
            missing = "Not applicable (non-timeline event)"
        elif col.startswith("strike_"):
            missing = "Not applicable (non-strike event)"
        elif col.startswith("naval_"):
            missing = "Not applicable (non-naval event)"
        elif col in ("financial_metric_name", "financial_metric_value",
                      "financial_metric_unit"):
            missing = "Not applicable (non-financial event)"
        elif col in ("casualties_civilian", "casualties_military",
                      "casualties_reported"):
            missing = "Not recorded or not applicable"
        else:
            missing = "Not applicable or not available"

        # Source domain
        source_domains = set()
        if col in REQUIRED_COLS:
            source_domains.add("all")
        if col.startswith("timeline_"):
            source_domains.add("timeline-events.json")
        if col.startswith("strike_"):
            source_domains.add("strikes-iran.json, strikes-retaliation.json")
        if col.startswith("naval_"):
            source_domains.add("carriers.json")
        if col.startswith("snapshot_"):
            source_domains.add("hero-stats.json")
        if col.startswith("financial_"):
            source_domains.add("oil-prices.json, markets.json, war-costs.json, baselines.json")
        if col.startswith("infrastructure_"):
            source_domains.add("infrastructure.json, strikes-iran.json")
        if not source_domains:
            source_domains.add("multiple")

        codebook_rows.append({
            "variable_name": col,
            "variable_label": col.replace("_", " ").title(),
            "variable_type": vtype,
            "valid_values": valid,
            "missing_code": missing,
            "source_domain": "; ".join(sorted(source_domains)),
            "notes": "",
        })

    return pd.DataFrame(codebook_rows)


# ---------------------------------------------------------------------------
# Summary statistics (Phase 7)
# ---------------------------------------------------------------------------
def print_summary(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print("DATASET SUMMARY STATISTICS")
    print("=" * 70)
    print(f"Total rows: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Columns: {len(df.columns)}")

    print("\n--- Row counts by event_domain ---")
    domain_counts = df["event_domain"].value_counts().sort_index()
    for dom, cnt in domain_counts.items():
        print(f"  {dom}: {cnt}")

    print("\n--- Row counts by event_type (top 25) ---")
    type_counts = df["event_type"].value_counts().head(25)
    for typ, cnt in type_counts.items():
        print(f"  {typ}: {cnt}")

    print("\n--- Column completeness (% non-null) ---")
    for col in df.columns:
        pct = df[col].notna().mean() * 100
        if pct > 0:
            print(f"  {col}: {pct:.1f}%")

    print("\n--- Data quality notes ---")
    dupes = df["event_id"].duplicated().sum()
    print(f"  Duplicate event_ids: {dupes}")
    null_dates = df["date"].isna().sum()
    print(f"  Missing dates: {null_dates}")
    null_domains = df["event_domain"].isna().sum()
    print(f"  Missing event_domain: {null_domains}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("IranWar.ai Research Dataset Builder")
    print("=" * 40)
    print(f"Data directory: {DATA_DIR}")
    print(f"Output directory: {OUT_DIR}\n")

    all_rows = []

    # Phase 1: Timeline events
    print("Phase 1: Extracting timeline events...")
    all_rows.extend(extract_timeline_events())

    # Phase 2: Strikes on Iran
    print("Phase 2: Extracting strikes on Iran...")
    all_rows.extend(extract_strikes_iran())

    # Phase 3: Retaliation strikes
    print("Phase 3: Extracting retaliation strikes...")
    all_rows.extend(extract_strikes_retaliation())

    # Phase 4: Naval, casualties, infrastructure
    print("Phase 4: Extracting naval assets, casualties, infrastructure...")
    all_rows.extend(extract_carriers())
    all_rows.extend(extract_casualties())
    all_rows.extend(extract_infrastructure())

    # Phase 5: Financial data
    print("Phase 5: Extracting financial data...")
    all_rows.extend(extract_oil_prices())
    all_rows.extend(extract_markets())
    all_rows.extend(extract_war_costs())
    all_rows.extend(extract_baselines())
    all_rows.extend(extract_hero_stats_history())

    # Phase 6: Hormuz, historical, bases, briefings
    print("Phase 6: Extracting Hormuz, historical, bases, briefings...")
    all_rows.extend(extract_hormuz())
    all_rows.extend(extract_historical_comparison())
    all_rows.extend(extract_global_bases())
    all_rows.extend(extract_briefings())

    # Build DataFrame
    df = pd.DataFrame(all_rows, columns=ALL_COLS)

    # Sort by date, then event_domain
    df = df.sort_values(["date", "event_domain"], na_position="first").reset_index(drop=True)

    # Write main dataset
    csv_path = OUT_DIR / "iranwar_event_dataset.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"\nWrote {csv_path} ({len(df)} rows, {len(df.columns)} columns)")

    # Generate and write codebook
    codebook = generate_codebook(df)
    cb_path = OUT_DIR / "codebook.csv"
    codebook.to_csv(cb_path, index=False, encoding="utf-8")
    print(f"Wrote {cb_path} ({len(codebook)} rows)")

    # Summary stats
    print_summary(df)

    return df


if __name__ == "__main__":
    main()
