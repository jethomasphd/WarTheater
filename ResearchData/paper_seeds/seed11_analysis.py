#!/usr/bin/env python3
"""
Seed 11 Analysis: Competing Narratives Under Fire
Media Studies / Communication / Information Warfare

Performs all analyses described in the paper seed:
1. Source attribution shift over 30 days
2. Framing phase identification (security → humanitarian → negotiation)
3. Minab school incident as frame-break event
4. Daily briefing headline narrative analysis
5. Event domain distribution over time
"""

import pandas as pd
import numpy as np
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

# ─────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────
DATA_PATH = Path(__file__).resolve().parent.parent / "iranwar_event_dataset.csv"
df = pd.read_csv(DATA_PATH, low_memory=False)
df['date'] = pd.to_datetime(df['date'])

print(f"Dataset: {len(df)} rows, {len(df.columns)} columns")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Day range: {df['day_of_conflict'].min()} to {df['day_of_conflict'].max()}")
print()

# ─────────────────────────────────────────────
# 1. SOURCE ATTRIBUTION CLASSIFICATION
# ─────────────────────────────────────────────
print("=" * 70)
print("ANALYSIS 1: SOURCE ATTRIBUTION CLASSIFICATION")
print("=" * 70)

timeline_df = df[df['timeline_source'].notna()].copy()
print(f"\nTimeline events with source attribution: {len(timeline_df)}")

# Classify sources into categories
def classify_source(source):
    if pd.isna(source):
        return "UNATTRIBUTED"
    s = str(source).lower()

    # Official military sources
    if any(k in s for k in ['centcom', 'dod', 'pentagon', 'us military', 'joint chiefs',
                             'defense department', 'us navy', 'usaf', 'air force',
                             'idf', 'israeli defense', 'israeli military']):
        return "OFFICIAL_MILITARY"

    # Official government/diplomatic
    if any(k in s for k in ['white house', 'state department', 'president', 'congress',
                             'national security', 'cia', 'intelligence', 'dni',
                             'un security council', 'un secretary', 'eu ', 'european union',
                             'foreign ministry', 'prime minister', 'government',
                             'treasury', 'federal reserve', 'senate', 'house speaker']):
        return "OFFICIAL_GOVERNMENT"

    # Iranian state sources
    if any(k in s for k in ['iran', 'irgc', 'tehran', 'khamenei', 'irna', 'press tv',
                             'hezbollah', 'houthi', 'ansar allah', 'resistance',
                             'islamic republic', 'iranian']):
        return "IRANIAN_STATE"

    # International organizations
    if any(k in s for k in ['iaea', 'who', 'unhcr', 'unicef', 'icrc', 'red cross',
                             'red crescent', 'imo', 'imf', 'world bank',
                             'amnesty', 'human rights watch', 'hrw', 'msf',
                             'doctors without', 'médecins']):
        return "INTL_ORGANIZATION"

    # Independent/investigative
    if any(k in s for k in ['bellingcat', 'bbc verify', 'osint', 'satellite imagery',
                             'planet labs', 'maxar', 'sentinel', 'acled',
                             'airwars', 'forensic', 'investigation']):
        return "INDEPENDENT_INVESTIGATIVE"

    # Wire services and major media
    if any(k in s for k in ['reuters', 'ap ', 'associated press', 'afp',
                             'bloomberg', 'nyt', 'new york times', 'washington post',
                             'bbc', 'cnn', 'al jazeera', 'guardian', 'wsj',
                             'wall street', 'financial times', 'abc', 'nbc', 'cbs',
                             'fox news', 'msnbc']):
        return "MAJOR_MEDIA"

    # Financial/industry
    if any(k in s for k in ['eia', 'ice', 'nymex', 'goldman', 'morgan stanley',
                             'opec', 'tanker', 'shipping', 'lloyd', 'maritime',
                             'market', 'trading', 'oil', 'commodity']):
        return "FINANCIAL_INDUSTRY"

    # Social media / unverified
    if any(k in s for k in ['social media', 'telegram', 'twitter', 'x.com',
                             'unverified', 'unconfirmed', 'rumor']):
        return "SOCIAL_MEDIA"

    return "OTHER_MEDIA"

timeline_df['source_category'] = timeline_df['timeline_source'].apply(classify_source)

# Overall distribution
print("\n--- Source Category Distribution (all timeline events) ---")
source_dist = timeline_df['source_category'].value_counts()
for cat, count in source_dist.items():
    print(f"  {cat:30s} {count:4d}  ({100*count/len(timeline_df):.1f}%)")

# ─────────────────────────────────────────────
# Source attribution by conflict week
# ─────────────────────────────────────────────
print("\n--- Source Attribution by Conflict Week ---")
def get_week(day):
    if day <= 0:
        return "Pre-war"
    elif day <= 7:
        return "Week 1 (Day 1-7)"
    elif day <= 14:
        return "Week 2 (Day 8-14)"
    elif day <= 21:
        return "Week 3 (Day 15-21)"
    else:
        return "Week 4 (Day 22-30)"

timeline_df['conflict_week'] = timeline_df['day_of_conflict'].apply(get_week)

week_order = ["Pre-war", "Week 1 (Day 1-7)", "Week 2 (Day 8-14)",
              "Week 3 (Day 15-21)", "Week 4 (Day 22-30)"]

source_by_week = pd.crosstab(timeline_df['conflict_week'], timeline_df['source_category'])
source_by_week = source_by_week.reindex(week_order)

# Calculate percentages
source_by_week_pct = source_by_week.div(source_by_week.sum(axis=1), axis=0) * 100

print("\nRaw counts:")
print(source_by_week.to_string())
print("\nPercentages:")
print(source_by_week_pct.round(1).to_string())

# Track "official" vs "critical" voice ratio
official_cats = ['OFFICIAL_MILITARY', 'OFFICIAL_GOVERNMENT']
critical_cats = ['INTL_ORGANIZATION', 'INDEPENDENT_INVESTIGATIVE']

print("\n--- Official vs Critical Source Ratio by Week ---")
for week in week_order:
    if week in source_by_week.index:
        row = source_by_week.loc[week].fillna(0)
        official = int(sum(row.get(c, 0) for c in official_cats))
        critical = int(sum(row.get(c, 0) for c in critical_cats))
        total = int(row.sum())
        if total == 0:
            continue
        ratio = official / critical if critical > 0 else float('inf')
        print(f"  {week:25s}  Official: {official:3d} ({100*official/total:.1f}%)  "
              f"Critical: {critical:3d} ({100*critical/total:.1f}%)  "
              f"Ratio: {ratio:.2f}")

# ─────────────────────────────────────────────
# 2. FRAMING PHASE ANALYSIS
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("ANALYSIS 2: FRAMING PHASE IDENTIFICATION")
print("=" * 70)

# Define frame keyword dictionaries
FRAMES = {
    'SECURITY': [
        'target', 'targets', 'degraded', 'destroyed', 'eliminated', 'neutralized',
        'strike', 'struck', 'bombing', 'operation', 'sortie', 'mission',
        'military objective', 'air campaign', 'precision', 'capability',
        'weapons of mass', 'nuclear', 'enrichment', 'threat', 'defense',
        'deterrence', 'force', 'offensive'
    ],
    'HUMANITARIAN': [
        'civilian', 'civilians', 'children', 'child', 'school', 'hospital',
        'refugee', 'displaced', 'humanitarian', 'aid', 'crisis', 'casualt',
        'killed', 'dead', 'death', 'wound', 'injur', 'victim', 'suffer',
        'war crime', 'atrocity', 'massacre', 'genocide', 'famine',
        'water', 'electricity', 'power outage', 'medical', 'red cross',
        'red crescent', 'who', 'unicef', 'unhcr', 'msf'
    ],
    'NEGOTIATION': [
        'ceasefire', 'cease-fire', 'negotiate', 'negotiation', 'talks',
        'peace', 'diplomacy', 'diplomatic', 'resolution', 'agreement',
        'propose', 'proposal', 'mediate', 'mediation', 'envoy',
        'de-escalat', 'off-ramp', 'ultimatum', 'demand', 'condition',
        'framework', 'deal', 'compromise', 'withdrawal', 'truce'
    ],
    'ECONOMIC': [
        'oil', 'crude', 'brent', 'wti', 'gas price', 'market', 'stock',
        'economic', 'sanctions', 'trade', 'cost', 'billion', 'trillion',
        'recession', 'inflation', 'supply chain', 'shipping', 'tanker',
        'hormuz', 'strait', 'commodity', 'energy'
    ]
}

def count_frame_keywords(text, frame_keywords):
    if pd.isna(text):
        return 0
    text_lower = str(text).lower()
    return sum(1 for kw in frame_keywords if kw in text_lower)

# Score every event for each frame
for frame_name, keywords in FRAMES.items():
    df[f'frame_{frame_name.lower()}'] = df['event_description'].apply(
        lambda x: count_frame_keywords(x, keywords)
    )

# Assign dominant frame per event
frame_cols = [f'frame_{f.lower()}' for f in FRAMES.keys()]
df['dominant_frame'] = df[frame_cols].idxmax(axis=1).str.replace('frame_', '').str.upper()
# If all scores are 0, mark as UNFRAMED
df.loc[df[frame_cols].sum(axis=1) == 0, 'dominant_frame'] = 'UNFRAMED'

# Daily frame distribution
print("\n--- Frame Distribution by Day ---")
daily_frames = df.groupby('day_of_conflict')[['frame_security', 'frame_humanitarian',
                                                'frame_negotiation', 'frame_economic']].sum()

# Normalize to percentages per day
daily_frames_pct = daily_frames.div(daily_frames.sum(axis=1), axis=0) * 100
daily_frames_pct = daily_frames_pct.fillna(0)

print("\nDaily frame percentages (security / humanitarian / negotiation / economic):")
for day in range(0, 31):
    if day in daily_frames_pct.index:
        row = daily_frames_pct.loc[day]
        sec = row['frame_security']
        hum = row['frame_humanitarian']
        neg = row['frame_negotiation']
        eco = row['frame_economic']
        bar_s = "█" * int(sec / 5)
        bar_h = "█" * int(hum / 5)
        bar_n = "█" * int(neg / 5)
        print(f"  Day {day:2d}: SEC {sec:5.1f}% {bar_s:20s} HUM {hum:5.1f}% {bar_h:20s} NEG {neg:5.1f}% {bar_n:20s} ECO {eco:5.1f}%")

# Identify phase transitions
print("\n--- Phase Transition Analysis ---")
# Weekly aggregation
weekly_frames = pd.DataFrame()
for week_label, day_range in [("Week 1", (1, 7)), ("Week 2", (8, 14)),
                               ("Week 3", (15, 21)), ("Week 4", (22, 30))]:
    mask = (df['day_of_conflict'] >= day_range[0]) & (df['day_of_conflict'] <= day_range[1])
    week_data = df[mask][['frame_security', 'frame_humanitarian', 'frame_negotiation', 'frame_economic']].sum()
    total = week_data.sum()
    week_pct = (week_data / total * 100).round(1)
    weekly_frames[week_label] = week_pct

print("\nWeekly frame distribution (%):")
print(weekly_frames.to_string())

# ─────────────────────────────────────────────
# 3. MINAB SCHOOL INCIDENT — FRAME BREAK ANALYSIS
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("ANALYSIS 3: MINAB SCHOOL INCIDENT — FRAME BREAK EVENT")
print("=" * 70)

minab_mask = df['event_description'].str.contains('Minab|minab', na=False, case=False)
school_mask = df['event_description'].str.contains('school', na=False, case=False)
minab_events = df[minab_mask | (school_mask & df['event_description'].str.contains('girl|child|student', na=False, case=False))]

print(f"\nMinab/school-related events: {len(minab_events)}")
print("\nKey Minab events:")
for _, row in minab_events.iterrows():
    desc = str(row['event_description'])[:150]
    print(f"  Day {row['day_of_conflict']:2.0f} | {row['event_domain']:15s} | {row['source_file']:30s} | {desc}")

# Pre/post Minab frame comparison
# Minab happened Day 1 — so compare Day 1 pre-strike context vs Day 2+ aftermath
print("\n--- Frame Composition: Day 1 vs Days 2-7 (immediate aftermath) ---")
day1 = df[df['day_of_conflict'] == 1][frame_cols].sum()
days2_7 = df[(df['day_of_conflict'] >= 2) & (df['day_of_conflict'] <= 7)][frame_cols].sum()

day1_pct = (day1 / day1.sum() * 100).round(1)
days2_7_pct = (days2_7 / days2_7.sum() * 100).round(1)

print(f"\n  Day 1:     {day1_pct.to_dict()}")
print(f"  Days 2-7:  {days2_7_pct.to_dict()}")

# Track humanitarian frame over each day following Minab
print("\n--- Humanitarian Frame Intensity (Day 1-10) ---")
for d in range(1, 11):
    day_data = df[df['day_of_conflict'] == d]
    hum_score = day_data['frame_humanitarian'].sum()
    sec_score = day_data['frame_security'].sum()
    total_events = len(day_data)
    hum_events = len(day_data[day_data['frame_humanitarian'] > 0])
    print(f"  Day {d:2d}: {total_events:3d} events, humanitarian_score={hum_score:3.0f}, "
          f"security_score={sec_score:3.0f}, "
          f"hum/sec ratio={hum_score/sec_score:.2f}" if sec_score > 0 else
          f"  Day {d:2d}: {total_events:3d} events, humanitarian_score={hum_score:3.0f}, "
          f"security_score={sec_score:3.0f}")

# ─────────────────────────────────────────────
# 4. DAILY BRIEFING HEADLINE ANALYSIS
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("ANALYSIS 4: DAILY BRIEFING HEADLINE NARRATIVE ANALYSIS")
print("=" * 70)

briefings = df[df['event_type'] == 'daily_briefing'].sort_values('day_of_conflict').copy()
print(f"\nDaily briefings: {len(briefings)}")

# Score each briefing headline for frames
for frame_name, keywords in FRAMES.items():
    briefings[f'bf_{frame_name.lower()}'] = briefings['event_description'].apply(
        lambda x: count_frame_keywords(x, keywords)
    )

# Assign dominant frame to each briefing
bf_cols = [f'bf_{f.lower()}' for f in FRAMES.keys()]
briefings['briefing_dominant_frame'] = briefings[bf_cols].idxmax(axis=1).str.replace('bf_', '').str.upper()
briefings.loc[briefings[bf_cols].sum(axis=1) == 0, 'briefing_dominant_frame'] = 'UNFRAMED'

print("\n--- Daily Briefing Dominant Frames ---")
for _, row in briefings.iterrows():
    desc = str(row['event_description'])[:120]
    print(f"  Day {row['day_of_conflict']:2.0f} | {row['briefing_dominant_frame']:15s} | {desc}...")

print("\n--- Briefing Frame Distribution ---")
bf_dist = briefings['briefing_dominant_frame'].value_counts()
for frame, count in bf_dist.items():
    print(f"  {frame:15s} {count:3d} ({100*count/len(briefings):.1f}%)")

# Frame transition in briefings
print("\n--- Briefing Frame Transitions (consecutive day pairs) ---")
prev_frame = None
transitions = []
for _, row in briefings.iterrows():
    curr_frame = row['briefing_dominant_frame']
    if prev_frame and prev_frame != curr_frame:
        transitions.append((row['day_of_conflict'], prev_frame, curr_frame))
    prev_frame = curr_frame

for day, from_f, to_f in transitions:
    print(f"  Day {day:2.0f}: {from_f} → {to_f}")

# ─────────────────────────────────────────────
# 5. EVENT DOMAIN DISTRIBUTION OVER TIME
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("ANALYSIS 5: EVENT DOMAIN DISTRIBUTION OVER TIME")
print("=" * 70)

domain_by_day = pd.crosstab(df['day_of_conflict'], df['event_domain'])
domain_by_week = pd.DataFrame()
for week_label, day_range in [("Week 1", (1, 7)), ("Week 2", (8, 14)),
                               ("Week 3", (15, 21)), ("Week 4", (22, 30))]:
    mask = (df['day_of_conflict'] >= day_range[0]) & (df['day_of_conflict'] <= day_range[1])
    week_sum = df[mask]['event_domain'].value_counts()
    domain_by_week[week_label] = week_sum

print("\nEvent domain counts by week:")
print(domain_by_week.fillna(0).astype(int).to_string())

domain_by_week_pct = domain_by_week.div(domain_by_week.sum(axis=0), axis=1) * 100
print("\nEvent domain percentages by week:")
print(domain_by_week_pct.fillna(0).round(1).to_string())

# ─────────────────────────────────────────────
# 6. DIPLOMATIC EVENT NARRATIVE ANALYSIS
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("ANALYSIS 6: DIPLOMATIC EVENTS — NARRATIVE COMPETITION")
print("=" * 70)

diplomatic = df[df['event_domain'] == 'DIPLOMATIC'].sort_values('day_of_conflict')
print(f"\nDiplomatic events: {len(diplomatic)}")

print("\n--- Diplomatic Events by Day ---")
for _, row in diplomatic.iterrows():
    desc = str(row['event_description'])[:140]
    print(f"  Day {row['day_of_conflict']:2.0f} | {desc}")

# Classify diplomatic events
def classify_diplomatic(desc):
    d = str(desc).lower()
    if any(k in d for k in ['ceasefire', 'peace', 'negotiate', 'talks', 'mediat', 'truce']):
        return 'PEACE_SEEKING'
    elif any(k in d for k in ['condemn', 'sanction', 'protest', 'oppose', 'withdraw', 'recall']):
        return 'OPPOSITION'
    elif any(k in d for k in ['support', 'coalition', 'ally', 'endorse', 'authorize']):
        return 'SUPPORT'
    elif any(k in d for k in ['ultimatum', 'demand', 'threat', 'warn']):
        return 'COERCION'
    elif any(k in d for k in ['humanitarian', 'aid', 'corridor', 'evacuate']):
        return 'HUMANITARIAN_DIPLOMATIC'
    return 'OTHER_DIPLOMATIC'

diplomatic['diplo_type'] = diplomatic['event_description'].apply(classify_diplomatic)
print("\n--- Diplomatic Event Classification ---")
diplo_dist = diplomatic['diplo_type'].value_counts()
for dt, count in diplo_dist.items():
    print(f"  {dt:30s} {count:3d}")

# ─────────────────────────────────────────────
# 7. DATA CONFIDENCE AS INFORMATION QUALITY PROXY
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("ANALYSIS 7: DATA CONFIDENCE AS INFORMATION QUALITY PROXY")
print("=" * 70)

conf_by_domain = pd.crosstab(df['event_domain'], df['data_confidence'])
print("\nData confidence by event domain:")
print(conf_by_domain.to_string())

conf_by_week = pd.DataFrame()
for week_label, day_range in [("Week 1", (1, 7)), ("Week 2", (8, 14)),
                               ("Week 3", (15, 21)), ("Week 4", (22, 30))]:
    mask = (df['day_of_conflict'] >= day_range[0]) & (df['day_of_conflict'] <= day_range[1])
    week_conf = df[mask]['data_confidence'].value_counts()
    conf_by_week[week_label] = week_conf

print("\nData confidence by week:")
print(conf_by_week.fillna(0).astype(int).to_string())

# ─────────────────────────────────────────────
# 8. SUMMARY STATISTICS FOR PAPER
# ─────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY STATISTICS FOR PAPER")
print("=" * 70)

print(f"\nTotal events: {len(df)}")
print(f"Events with source attribution: {len(timeline_df)}")
print(f"Unique sources: {timeline_df['timeline_source'].nunique()}")
print(f"Source categories: {timeline_df['source_category'].nunique()}")
print(f"Diplomatic events: {len(diplomatic)}")
print(f"Daily briefings: {len(briefings)}")
print(f"Minab-related events: {len(minab_events)}")

# Frame dominance summary
print(f"\nOverall frame distribution:")
dom_frames = df['dominant_frame'].value_counts()
for f, c in dom_frames.items():
    print(f"  {f:15s} {c:5d} ({100*c/len(df):.1f}%)")

# Key narrative turning points
print("\n--- Key Narrative Turning Points ---")
# Find days where humanitarian overtakes security
for d in range(1, 31):
    day_data = df[df['day_of_conflict'] == d]
    hum = day_data['frame_humanitarian'].sum()
    sec = day_data['frame_security'].sum()
    neg = day_data['frame_negotiation'].sum()
    if hum > sec and sec > 0:
        print(f"  Day {d}: Humanitarian ({hum:.0f}) > Security ({sec:.0f})")
    if neg > sec and sec > 0:
        print(f"  Day {d}: Negotiation ({neg:.0f}) > Security ({sec:.0f})")
    if neg > hum and hum > 0 and d > 20:
        print(f"  Day {d}: Negotiation ({neg:.0f}) > Humanitarian ({hum:.0f}) [late-conflict]")

print("\n--- ANALYSIS COMPLETE ---")
