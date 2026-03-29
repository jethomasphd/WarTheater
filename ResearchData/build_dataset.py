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
    """Phase 5a: Extract daily Brent/WTI oil prices."""
    data = load_json("oil-prices.json")
    if data is None:
        return []

    labels = data.get("labels", [])
    brent = data.get("brent", [])
    wti = data.get("wti", [])

    rows = []
    for i, label in enumerate(labels):
        d = parse_short_date(label, 2026)
        day_num = war_day(d)

        for metric_name, values in [("Brent Crude", brent), ("WTI Crude", wti)]:
            if i >= len(values) or values[i] is None:
                continue
            row = empty_row()
            row["event_id"] = next_event_id()
            row["date"] = d.isoformat()
            row["day_of_conflict"] = day_num
            row["event_domain"] = "FINANCIAL"
            row["event_type"] = "oil_price"
            row["event_description"] = f"{metric_name}: ${values[i]:.2f}/bbl on {label}"
            row["source_file"] = "oil-prices.json"
            row["financial_metric_name"] = metric_name
            row["financial_metric_value"] = values[i]
            row["financial_metric_unit"] = "USD/bbl"
            row["data_confidence"] = "HIGH"
            rows.append(row)

    print(f"  oil-prices.json: {len(rows)} price events extracted")
    return rows


def extract_markets() -> list[dict]:
    """Phase 5b: Extract daily market sector performance."""
    data = load_json("markets.json")
    if data is None:
        return []

    labels = data.get("labels", [])
    contexts = data.get("contexts", [])
    datasets = data.get("datasets", {})

    rows = []
    for i, label in enumerate(labels):
        d = parse_short_date(label, 2026)
        day_num = war_day(d)
        context = contexts[i] if i < len(contexts) else ""

        for sector_key, sector_data in datasets.items():
            values = sector_data.get("data", [])
            if i >= len(values) or values[i] is None:
                continue
            sector_label = sector_data.get("label", sector_key)

            row = empty_row()
            row["event_id"] = next_event_id()
            row["date"] = d.isoformat()
            row["day_of_conflict"] = day_num
            row["event_domain"] = "FINANCIAL"
            row["event_type"] = "market_index"
            row["event_description"] = f"{sector_label}: {values[i]:.1f} (indexed, Feb 27=100). {context}"
            row["source_file"] = "markets.json"
            row["financial_metric_name"] = sector_label
            row["financial_metric_value"] = values[i]
            row["financial_metric_unit"] = "index (Feb 27 = 100)"
            row["data_confidence"] = "HIGH"
            rows.append(row)

    print(f"  markets.json: {len(rows)} market events extracted")
    return rows


def extract_war_costs() -> list[dict]:
    """Phase 5c: Extract daily war costs + tanker transits."""
    data = load_json("war-costs.json")
    if data is None:
        return []

    rows = []

    # Daily costs
    cost_labels = data.get("labels", [])
    costs = data.get("daily_cost_millions", [])
    day_notes = data.get("day_notes", [])

    for i, label in enumerate(cost_labels):
        # Labels are "Day 1", "Day 2", etc.
        m = re.match(r"Day\s+(\d+)", label)
        if not m:
            continue
        day_num = int(m.group(1))
        d = date_from_war_day(day_num)

        if i < len(costs) and costs[i] is not None:
            row = empty_row()
            row["event_id"] = next_event_id()
            row["date"] = d.isoformat()
            row["day_of_conflict"] = day_num
            row["event_domain"] = "FINANCIAL"
            row["event_type"] = "daily_war_cost"
            note = day_notes[i] if i < len(day_notes) else ""
            row["event_description"] = f"Estimated daily US cost: ${costs[i]}M. {note}"
            row["source_file"] = "war-costs.json"
            row["financial_metric_name"] = "Daily US War Cost"
            row["financial_metric_value"] = costs[i]
            row["financial_metric_unit"] = "USD millions"
            row["data_confidence"] = "MEDIUM"
            rows.append(row)

    # Tanker transits
    tt = data.get("tanker_transits", {})
    tt_labels = tt.get("labels", [])
    tt_data = tt.get("data", [])

    for i, label in enumerate(tt_labels):
        d = parse_short_date(label, 2026)
        day_num = war_day(d)

        if i < len(tt_data) and tt_data[i] is not None:
            row = empty_row()
            row["event_id"] = next_event_id()
            row["date"] = d.isoformat()
            row["day_of_conflict"] = day_num
            row["event_domain"] = "FINANCIAL"
            row["event_type"] = "tanker_transit"
            row["event_description"] = (
                f"Strait of Hormuz tanker transits: {tt_data[i]} "
                f"(pre-war baseline: {tt.get('prewar_daily', 50)}/day)"
            )
            row["source_file"] = "war-costs.json"
            row["financial_metric_name"] = "Hormuz Tanker Transits"
            row["financial_metric_value"] = tt_data[i]
            row["financial_metric_unit"] = "transits/day"
            row["data_confidence"] = "HIGH"
            rows.append(row)

    print(f"  war-costs.json: {len(rows)} events extracted "
          f"({len(costs)} cost days + {len(tt_data)} tanker days)")
    return rows


def extract_baselines() -> list[dict]:
    """Phase 5d: Extract pre-war financial baseline as individual metric events."""
    data = load_json("baselines.json")
    if data is None:
        return []

    d = date.fromisoformat(data.get("date", "2026-02-27"))
    day_num = war_day(d)
    rows = []

    # Flatten all nested metrics
    metrics = [
        ("Brent Crude (baseline)", data.get("oil", {}).get("brent"), "USD/bbl"),
        ("WTI Crude (baseline)", data.get("oil", {}).get("wti"), "USD/bbl"),
        ("US Gas National Avg (baseline)", data.get("gas", {}).get("national_avg"), "USD/gallon"),
        ("S&P 500 (baseline)", data.get("markets", {}).get("sp500"), "index points"),
        ("Nasdaq (baseline)", data.get("markets", {}).get("nasdaq"), "index points"),
        ("DJIA (baseline)", data.get("markets", {}).get("djia"), "index points"),
        ("US 10Y Treasury Yield", data.get("treasury", {}).get("us_10yr_yield"), "percent"),
        ("Fed Funds Rate Upper", data.get("treasury", {}).get("fed_funds_rate_upper"), "percent"),
        ("Fed Funds Rate Lower", data.get("treasury", {}).get("fed_funds_rate_lower"), "percent"),
        ("DXY Dollar Index", data.get("treasury", {}).get("dxy"), "index points"),
        ("Gold (baseline)", data.get("commodities", {}).get("gold_oz"), "USD/oz"),
        ("Silver (baseline)", data.get("commodities", {}).get("silver_oz"), "USD/oz"),
        ("VIX (baseline)", data.get("commodities", {}).get("vix"), "index points"),
        ("National Debt", data.get("national_debt", {}).get("total_trillions"), "USD trillions"),
        ("Debt-to-GDP", data.get("national_debt", {}).get("debt_to_gdp_pct"), "percent"),
    ]

    # Defense stocks
    for ticker, val in data.get("defense_stocks", {}).items():
        if ticker == "source":
            continue
        if val is not None:
            metrics.append((f"{ticker} (baseline)", val, "USD/share"))

    # Oil stocks
    for ticker, val in data.get("oil_stocks", {}).items():
        if ticker == "source":
            continue
        if val is not None:
            metrics.append((f"{ticker} (baseline)", val, "USD/share"))

    # Airline stocks
    for ticker, val in data.get("airline_stocks", {}).items():
        if ticker == "source":
            continue
        if val is not None:
            metrics.append((f"{ticker} (baseline)", val, "USD/share"))

    # Hormuz baseline
    hormuz = data.get("hormuz", {})
    if hormuz.get("daily_tanker_transits"):
        metrics.append(("Hormuz Daily Tanker Transits (baseline)",
                        hormuz["daily_tanker_transits"], "transits/day"))
    if hormuz.get("daily_oil_flow_mbd"):
        metrics.append(("Hormuz Daily Oil Flow (baseline)",
                        hormuz["daily_oil_flow_mbd"], "million bbl/day"))

    # Audit confidence
    audit = data.get("audit", {})
    verified = set(audit.get("verified_closes", []))
    unverified = set(audit.get("unverified", []))

    for name, val, unit in metrics:
        if val is None:
            continue
        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = d.isoformat()
        row["day_of_conflict"] = day_num
        row["event_domain"] = "FINANCIAL"
        row["event_type"] = "baseline_metric"
        row["event_description"] = f"Pre-war baseline — {name}: {val} {unit}"
        row["source_file"] = "baselines.json"
        row["financial_metric_name"] = name
        row["financial_metric_value"] = val
        row["financial_metric_unit"] = unit

        # Confidence from audit
        ticker_lower = name.split(" ")[0].lower()
        if ticker_lower in verified:
            row["data_confidence"] = "HIGH"
        elif ticker_lower in unverified:
            row["data_confidence"] = "LOW"
        else:
            row["data_confidence"] = "MEDIUM"

        rows.append(row)

    print(f"  baselines.json: {len(rows)} baseline metric events extracted")
    return rows


def extract_hero_stats_history() -> list[dict]:
    """Phase 5e: Extract daily aggregate snapshots from hero-stats history."""
    data = load_json("hero-stats.json")
    if data is None:
        return []

    history = data.get("history", [])
    rows = []

    snapshot_fields = [
        ("brent", "snapshot_brent"),
        ("wti", "snapshot_wti"),
        ("gas", "snapshot_gas"),
        ("sp500", "snapshot_sp500"),
        ("daily_cost_millions", "snapshot_daily_cost_millions"),
        ("total_cost_billions", "snapshot_total_cost_billions"),
        ("targets_struck", "snapshot_targets_struck"),
        ("us_kia", "snapshot_us_kia"),
        ("us_wia", "snapshot_us_wia"),
        ("iranian_killed", "snapshot_iranian_killed"),
        ("lebanese_killed", "snapshot_lebanese_killed"),
        ("displaced", "snapshot_displaced"),
        ("flights_cancelled", "snapshot_flights_cancelled"),
        ("children_killed", "snapshot_children_killed"),
    ]

    for entry in history:
        d = date.fromisoformat(entry["date"])
        day_num = entry.get("war_day", war_day(d))

        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = d.isoformat()
        row["day_of_conflict"] = day_num
        row["event_domain"] = "OTHER"
        row["event_type"] = "daily_aggregate_snapshot"
        row["source_file"] = "hero-stats.json"

        # Build description from non-null values
        parts = [f"Day {day_num} snapshot"]
        for src_key, _ in snapshot_fields:
            val = entry.get(src_key)
            if val is not None:
                parts.append(f"{src_key}={val}")
        row["event_description"] = "; ".join(parts)

        # Map snapshot fields
        for src_key, dest_key in snapshot_fields:
            row[dest_key] = entry.get(src_key)

        row["data_confidence"] = "HIGH"
        rows.append(row)

    print(f"  hero-stats.json: {len(rows)} daily snapshot events extracted")
    return rows


def extract_hormuz() -> list[dict]:
    """Phase 6a: Extract Strait of Hormuz closure, maritime impacts, and day narratives."""
    data = load_json("hormuz.json")
    if data is None:
        return []

    rows = []
    strait = data.get("strait", {})
    impact = data.get("impact", {})
    geometry = data.get("geometry", {})

    # 1. Strait closure event
    closure_date = strait.get("closure_date")
    if closure_date:
        row = empty_row()
        row["event_id"] = next_event_id()
        d = date.fromisoformat(closure_date)
        row["date"] = d.isoformat()
        row["day_of_conflict"] = war_day(d)
        row["event_domain"] = "NAVAL"
        row["event_type"] = "strait_closure"
        row["event_description"] = (
            f"Strait of Hormuz effectively closed. "
            f"Type: {strait.get('closure_type', '')}. "
            f"Method: {strait.get('closure_method', '')}"
        )
        row["source_file"] = "hormuz.json"
        row["location_name"] = "Strait of Hormuz"
        row["location_lat"] = 26.55
        row["location_lon"] = 56.25
        row["country"] = "International Waters"
        row["actor_initiating"] = strait.get("closure_declared_by", "IRGC")
        row["data_confidence"] = "HIGH"
        rows.append(row)

    # 2. Vessel attack summary
    vessels_attacked = impact.get("vessels_attacked_total")
    if vessels_attacked:
        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = "2026-03-29"
        row["day_of_conflict"] = 30
        row["event_domain"] = "RETALIATION"
        row["event_type"] = "maritime_attack_summary"
        row["event_description"] = (
            f"{vessels_attacked} commercial vessels attacked in Strait of Hormuz. "
            f"{impact.get('vessels_attacked_note', '')}"
        )
        row["source_file"] = "hormuz.json"
        row["location_name"] = "Strait of Hormuz"
        row["location_lat"] = 26.35
        row["location_lon"] = 56.55
        row["country"] = "International Waters"
        row["actor_initiating"] = "IRGC Navy"
        row["casualties_reported"] = impact.get("seafarer_fatalities")
        row["data_confidence"] = "HIGH"
        rows.append(row)

    # 3. Alternative routes
    for route in impact.get("alternative_routes", []):
        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = "2026-03-29"
        row["day_of_conflict"] = 30
        row["event_domain"] = "FINANCIAL"
        row["event_type"] = "alternative_route"
        cap = route.get("capacity_mbd", "?")
        eff = route.get("effective_export_mbd", "?")
        row["event_description"] = (
            f"Alternative route: {route.get('name', '')}. "
            f"Capacity: {cap} mbd, Effective: {eff} mbd. "
            f"Status: {route.get('status', '')}"
        )
        row["source_file"] = "hormuz.json"
        row["location_name"] = route.get("name")
        row["financial_metric_name"] = f"{route.get('name', '')} throughput"
        if isinstance(eff, (int, float)):
            row["financial_metric_value"] = eff
        row["financial_metric_unit"] = "million bbl/day"
        row["data_confidence"] = "MEDIUM"
        rows.append(row)

    # 4. Islands (strategic geography)
    for island in geometry.get("islands", []):
        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = "2026-02-28"
        row["day_of_conflict"] = 1
        row["event_domain"] = "NAVAL"
        row["event_type"] = "strategic_geography"
        row["event_description"] = (
            f"Strategic island: {island.get('name', '')}. "
            f"Control: {island.get('control', '')}. "
            f"Military: {island.get('military', False)}"
        )
        row["source_file"] = "hormuz.json"
        row["location_name"] = island.get("name")
        row["location_lat"] = island.get("lat")
        row["location_lon"] = island.get("lng")
        row["country"] = "Iran" if "Iran" in str(island.get("control", "")) else "Disputed"
        row["data_confidence"] = "HIGH"
        rows.append(row)

    # 5. Day narrative events (day_22_events through day_30_events)
    for key, val in impact.items():
        m = re.match(r"day_(\d+)_events", key)
        if not m:
            continue
        day_num = int(m.group(1))
        d = date_from_war_day(day_num)
        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = d.isoformat()
        row["day_of_conflict"] = day_num
        row["event_domain"] = "NAVAL"
        row["event_type"] = "hormuz_daily_narrative"
        row["event_description"] = val
        row["source_file"] = "hormuz.json"
        row["location_name"] = "Strait of Hormuz"
        row["location_lat"] = 26.55
        row["location_lon"] = 56.25
        row["country"] = "International Waters"
        row["data_confidence"] = "HIGH"
        rows.append(row)

    print(f"  hormuz.json: {len(rows)} events extracted")
    return rows


def extract_historical_comparison() -> list[dict]:
    """Phase 6b: Extract historical conflict comparison records."""
    data = load_json("historical-comparison.json")
    if data is None:
        return []

    rows = []
    for rec in data.get("conflicts", []):
        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = "2026-03-29"  # reference date
        row["day_of_conflict"] = 30
        row["event_domain"] = "OTHER"
        row["event_type"] = "historical_comparison"
        row["event_description"] = (
            f"{rec.get('label', '')}: {rec.get('targets_struck', '?')} targets struck, "
            f"{rec.get('us_kia', '?')} US KIA, "
            f"${rec.get('daily_cost_millions', '?')}M/day. {rec.get('note', '')}"
        )
        row["source_file"] = "historical-comparison.json"
        row["financial_metric_name"] = f"{rec.get('label', '')} daily cost"
        row["financial_metric_value"] = rec.get("daily_cost_millions")
        row["financial_metric_unit"] = "USD millions"
        row["casualties_military"] = rec.get("us_kia")
        row["data_confidence"] = "HIGH"
        rows.append(row)

    print(f"  historical-comparison.json: {len(rows)} comparison records extracted")
    return rows


def extract_global_bases() -> list[dict]:
    """Phase 6c: Extract US military base reference records."""
    data = load_json("global-bases.json")
    if data is None:
        return []

    rows = []
    for rec in data:
        row = empty_row()
        row["event_id"] = next_event_id()
        row["date"] = "2026-02-28"  # context date
        row["day_of_conflict"] = 1
        row["event_domain"] = "MILITARY"
        row["event_type"] = "military_base"
        row["event_description"] = f"{rec.get('name', '')}: {rec.get('note', '')}"
        row["source_file"] = "global-bases.json"
        row["location_name"] = rec.get("name")
        row["location_lat"] = rec.get("lat")
        row["location_lon"] = rec.get("lng")
        row["infrastructure_target_type"] = "military_base"
        row["actor_initiating"] = "US"
        row["data_confidence"] = "HIGH"
        rows.append(row)

    print(f"  global-bases.json: {len(rows)} base reference records extracted")
    return rows


def extract_briefings() -> list[dict]:
    """Phase 6d: Extract daily briefing index entries."""
    data = load_json("briefings/index.json")
    if data is None:
        return []

    rows = []
    for rec in data:
        row = empty_row()
        row["event_id"] = next_event_id()
        d = date.fromisoformat(rec["date"])
        row["date"] = d.isoformat()
        row["day_of_conflict"] = rec.get("day", war_day(d))
        row["event_domain"] = "OTHER"
        row["event_type"] = "daily_briefing"
        row["event_description"] = (
            f"{rec.get('label', '')}: {rec.get('headline', '')}"
        )
        row["source_file"] = "briefings/index.json"
        row["source_record_id"] = rec.get("file")
        row["data_confidence"] = "HIGH"
        rows.append(row)

    print(f"  briefings/index.json: {len(rows)} briefing index entries extracted")
    return rows


# ---------------------------------------------------------------------------
# Codebook generation (Phase 7)
# ---------------------------------------------------------------------------
VARIABLE_METADATA = {
    "event_id": ("Unique Event Identifier", "string", "all", "Should not be missing",
                 "Sequential ID (EVT-0001...) assigned during extraction. Stable across re-runs if source data unchanged."),
    "date": ("Event Date (ISO 8601)", "date", "all", "Should not be missing",
             "YYYY-MM-DD. Pre-war oil prices go back to 2026-01-02. Conflict events start 2026-02-28."),
    "datetime_utc": ("Event Datetime", "datetime", "timeline-events.json", "Not available — only timeline events have timestamps",
                     "YYYY-MM-DDTHH:MM:SS. Times are approximate local time, not true UTC. Events span multiple time zones."),
    "day_of_conflict": ("Day of Conflict", "integer", "all", "Should not be missing",
                        "Day 0 = 2026-02-27 (pre-war baseline). Day 1 = 2026-02-28 (first strikes). Max = 30."),
    "event_domain": ("Event Domain", "categorical", "all", "Should not be missing",
                     "Primary classification. STRIKE = US/Israeli offensive. RETALIATION = Iranian/proxy response. MILITARY = other military. NAVAL = maritime/fleet. FINANCIAL = economic data. DIPLOMATIC = political/diplomatic. HUMANITARIAN = casualties/damage. CYBER = cyber ops. OTHER = reference/summary."),
    "event_type": ("Event Type (subcategory)", "categorical", "all", "Should not be missing",
                   "More specific than event_domain. 25 unique values. Key types: airstrike, missile_attack, rocket_attack, daily_casualty_report, oil_price, market_index, daily_war_cost, tanker_transit, baseline_metric, daily_aggregate_snapshot."),
    "event_description": ("Event Description", "text", "all", "Should not be missing",
                          "Free-text description. Format varies by source: timeline events = 'title: description'; strikes = 'city: target'; financial = metric summary."),
    "source_file": ("Source JSON File", "categorical", "all", "Should not be missing",
                    "Which JSON file in public/data/ this row was extracted from."),
    "source_record_id": ("Source Record ID", "string", "strikes-iran.json; strikes-retaliation.json; carriers.json; briefings/index.json", "Not available — source has no record ID",
                         "Original ID from source data (e.g., 'tehran-leadership', 'cvn-72'). NULL for timeline events, casualties, financial data."),
    "location_name": ("Location Name", "string", "strikes; carriers; hormuz; global-bases", "Not applicable (non-geographic event)",
                      "City, base, or area name. Granularity varies: city-level for strikes, operational area for naval assets."),
    "location_lat": ("Latitude", "float", "strikes; carriers; hormuz; global-bases", "Not applicable (non-geographic event)",
                     "WGS84 decimal degrees. Precision varies: strike locations ~4 decimal places, naval assets approximate."),
    "location_lon": ("Longitude", "float", "strikes; carriers; hormuz; global-bases", "Not applicable (non-geographic event)",
                     "WGS84 decimal degrees."),
    "country": ("Country", "categorical", "strikes; carriers; hormuz; global-bases", "Not applicable (non-geographic event)",
                "Extracted from city/location names via pattern matching. 'International Waters' for maritime events."),
    "actor_initiating": ("Initiating Actor", "string", "strikes; retaliation; carriers; global-bases", "Not applicable or not determinable",
                         "Who carried out the action. Values: US, Israel, US/Israel (joint), Hezbollah, Iran, IRGC Navy, various proxy groups, UK, France."),
    "actor_target": ("Target Actor/Entity", "string", "strikes; retaliation; casualties", "Not applicable",
                     "Who or what was targeted. For casualties, identifies the faction (e.g., 'Iran (military)', 'US (military)')."),
    "weapon_system": ("Weapon System", "string", "strikes-retaliation.json", "Not applicable (non-retaliation event or not recorded)",
                      "Weapon type from retaliation records. Examples: 'Ballistic missiles / cruise missiles / drones', 'Fattah hypersonic'."),
    "military_asset": ("Military Asset", "string", "carriers.json", "Not applicable (non-naval event)",
                       "Vessel name and hull number. Example: 'USS Abraham Lincoln (CVN-72)'."),
    "casualties_reported": ("Casualties Reported", "integer", "strikes; retaliation; casualties; hormuz", "Not recorded or not applicable",
                            "Numeric casualty count when parseable, or text description. For daily casualty reports, this is the estimated daily killed for one faction. For strikes, attached to first target only to avoid double-counting."),
    "casualties_civilian": ("Civilian Casualties", "integer", "casualties.json", "Not recorded or not applicable",
                            "Civilian killed count. Populated only for Iranian civilian daily casualty reports. These are daily estimates, not cumulative."),
    "casualties_military": ("Military Casualties", "integer", "casualties.json; historical-comparison.json", "Not recorded or not applicable",
                            "Military killed count. Populated for Iranian military, US military, and Israeli military daily reports. Daily estimates, not cumulative."),
    "infrastructure_target_type": ("Infrastructure Target Type", "categorical", "strikes-iran.json; infrastructure.json", "Not applicable (non-strike or non-infrastructure event)",
                                   "Inferred from target descriptions. Values: military_base, civilian, nuclear_facility, oil_infrastructure, air_defense, communications, healthcare, power_grid, transportation."),
    "financial_metric_name": ("Financial Metric Name", "string", "oil-prices; markets; war-costs; baselines; hormuz", "Not applicable (non-financial event)",
                              "Name of the financial indicator. Examples: 'Brent Crude', 'S&P 500', 'Daily US War Cost', 'Hormuz Tanker Transits'."),
    "financial_metric_value": ("Financial Metric Value", "float", "oil-prices; markets; war-costs; baselines; hormuz", "Not applicable (non-financial event)",
                               "Numeric value of the financial metric. Units vary — see financial_metric_unit."),
    "financial_metric_unit": ("Financial Metric Unit", "categorical", "oil-prices; markets; war-costs; baselines; hormuz", "Not applicable (non-financial event)",
                              "Unit of measurement. Examples: 'USD/bbl', 'index (Feb 27 = 100)', 'USD millions', 'transits/day'."),
    "escalation_level": ("Escalation Level", "string", "N/A", "Not available — no escalation scoring in source data",
                         "Reserved for future use. Not present in source data. Always NULL."),
    "data_confidence": ("Data Confidence", "categorical", "all", "Should not be missing",
                        "Assessment of data reliability. HIGH = from structured field with authoritative source. MEDIUM = inferred or from secondary sources. LOW = unverified, imputed, or from Wikipedia."),
    "timeline_source": ("Timeline Source Attribution", "string", "timeline-events.json", "Not applicable (non-timeline event)",
                        "Source attribution from timeline record. Examples: 'DoD / White House', 'CENTCOM / IDF'."),
    "timeline_data_point": ("Timeline Key Data Point", "string", "timeline-events.json", "Not applicable or no data point recorded",
                            "Quantitative highlight from the timeline event. Example: '3,000+ targets struck in first 72 hours'."),
    "strike_notes": ("Strike/Source Notes", "text", "strikes-iran.json; strikes-retaliation.json; infrastructure.json; carriers.json", "Not applicable (non-strike/naval event)",
                     "Detailed operational notes from source record. Often contains sourcing, context, and cross-references."),
    "strike_verified": ("Strike Verified", "boolean", "strikes-retaliation.json", "Not applicable (non-retaliation event)",
                        "Whether the retaliation strike was verified in open-source reporting. True/False. 4 of 72 retaliation locations are unverified."),
    "naval_strike_group": ("Naval Strike Group", "string", "carriers.json", "Not applicable (non-naval event)",
                           "Strike group or command assignment. Example: 'Carrier Strike Group 3'."),
    "naval_aircraft": ("Naval Aircraft Complement", "text", "carriers.json", "Not applicable (non-naval event)",
                       "Aircraft types embarked. Example: 'F/A-18E/F Super Hornets, F-35C Lightning II'."),
    "naval_escorts": ("Naval Escort Vessels", "text", "carriers.json", "Not applicable (non-naval event)",
                      "Escort vessels listed, semicolon-separated."),
    "infrastructure_damage_count": ("Infrastructure Damage Count", "integer", "infrastructure.json", "Not applicable (non-infrastructure event)",
                                    "Numeric count of damaged facilities. Parsed from text (e.g., '29+' → 29). Minimums; actual totals may be higher."),
    "snapshot_brent": ("Daily Snapshot: Brent Crude", "float", "hero-stats.json", "Not available for this day (weekend/holiday or not reported)",
                       "Brent crude price (USD/bbl) from daily aggregate snapshot. NULL on non-trading days."),
    "snapshot_wti": ("Daily Snapshot: WTI Crude", "float", "hero-stats.json", "Not available for this day",
                     "WTI crude price (USD/bbl) from daily aggregate snapshot."),
    "snapshot_gas": ("Daily Snapshot: US Gas Price", "float", "hero-stats.json", "Not available for this day",
                     "US national average gasoline price (USD/gallon). Reported intermittently."),
    "snapshot_sp500": ("Daily Snapshot: S&P 500", "float", "hero-stats.json", "Not available for this day",
                       "S&P 500 index close. NULL on weekends and holidays."),
    "snapshot_daily_cost_millions": ("Daily Snapshot: Est. Daily US Cost", "float", "hero-stats.json", "Not available for this day",
                                    "Estimated daily US operational cost in millions USD. Based on Pentagon and CSIS anchor points with interpolation."),
    "snapshot_total_cost_billions": ("Daily Snapshot: Est. Cumulative Cost", "float", "hero-stats.json", "Not available for this day",
                                    "Cumulative estimated US cost in billions USD since Feb 28."),
    "snapshot_targets_struck": ("Daily Snapshot: Targets Struck", "float", "hero-stats.json", "Not available — reported intermittently",
                                "Cumulative US/Israeli targets struck. Reported at irregular intervals by CENTCOM/IDF."),
    "snapshot_us_kia": ("Daily Snapshot: US KIA (cumulative)", "float", "hero-stats.json", "Not available for this day",
                        "Cumulative US military killed in action. NOTE: this is CUMULATIVE, unlike daily casualty reports which are daily estimates."),
    "snapshot_us_wia": ("Daily Snapshot: US WIA (cumulative)", "float", "hero-stats.json", "Not available — reported intermittently",
                        "Cumulative US military wounded in action."),
    "snapshot_iranian_killed": ("Daily Snapshot: Iranian Killed (cumulative)", "float", "hero-stats.json", "Not available — reported intermittently",
                                "Cumulative Iranian killed. Figures from Red Crescent/HRANA — independently difficult to verify."),
    "snapshot_lebanese_killed": ("Daily Snapshot: Lebanese Killed (cumulative)", "float", "hero-stats.json", "Not available — reported intermittently",
                                 "Cumulative Lebanese killed (all factions). Source: Lebanese Health Ministry."),
    "snapshot_displaced": ("Daily Snapshot: Displaced Persons (cumulative)", "float", "hero-stats.json", "Not available — reported intermittently",
                           "Cumulative displaced persons across all affected countries."),
    "snapshot_flights_cancelled": ("Daily Snapshot: Flights Cancelled (cumulative)", "float", "hero-stats.json", "Not available — reported intermittently",
                                   "Cumulative commercial flights cancelled due to conflict."),
    "snapshot_children_killed": ("Daily Snapshot: Children Killed (cumulative)", "float", "hero-stats.json", "Not available — reported intermittently",
                                 "Cumulative children killed across Iran and Lebanon. Figures from HRANA/Red Crescent."),
}


def generate_codebook(df: pd.DataFrame) -> pd.DataFrame:
    """Introspect the dataset and produce a codebook with researcher-oriented metadata."""
    codebook_rows = []
    for col in df.columns:
        series = df[col]
        non_null = series.dropna()

        meta = VARIABLE_METADATA.get(col)
        if meta:
            label, vtype, source_domain, missing, notes = meta
        else:
            label = col.replace("_", " ").title()
            vtype = "string"
            source_domain = "unknown"
            missing = "Not applicable or not available"
            notes = ""

        # Valid values — auto-generate from data
        if vtype == "categorical" and len(non_null) > 0:
            uniques = sorted(non_null.unique().tolist())
            valid = " | ".join(str(v) for v in uniques[:40])
        elif vtype in ("integer", "float") and len(non_null) > 0:
            try:
                nums = pd.to_numeric(non_null, errors="coerce").dropna()
                if len(nums) > 0:
                    valid = f"{nums.min():.4g} – {nums.max():.4g}"
                else:
                    valid = ""
            except Exception:
                valid = ""
        elif vtype == "boolean" and len(non_null) > 0:
            valid = " | ".join(str(v) for v in sorted(non_null.unique().tolist()))
        else:
            valid = ""

        # Completeness
        pct = non_null.shape[0] / len(df) * 100 if len(df) > 0 else 0

        codebook_rows.append({
            "variable_name": col,
            "variable_label": label,
            "variable_type": vtype,
            "valid_values": valid,
            "pct_non_null": f"{pct:.1f}%",
            "missing_code": missing,
            "source_domain": source_domain,
            "notes": notes,
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
