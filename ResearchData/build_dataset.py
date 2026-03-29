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


def extract_strikes_retaliation() -> list[dict]:
    """Phase 3 — TODO"""
    return []


def extract_carriers() -> list[dict]:
    """Phase 4a — TODO"""
    return []


def extract_casualties() -> list[dict]:
    """Phase 4b — TODO"""
    return []


def extract_infrastructure() -> list[dict]:
    """Phase 4c — TODO"""
    return []


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
