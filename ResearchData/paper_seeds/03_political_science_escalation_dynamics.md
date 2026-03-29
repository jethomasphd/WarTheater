# Paper Seed: Escalation Dynamics and the Spiral Model — Testing Action-Reaction Sequences in the 2026 US-Iran Conflict

## Field
Political Science / International Relations / Security Studies

## Target Journals
- *Journal of Conflict Resolution*
- *International Security*
- *American Political Science Review*
- *Journal of Peace Research*

## Theoretical Framework

**Conflict Spiral Model (Jervis, 1976; Glaser, 1997)**

The spiral model predicts that adversaries locked in a security dilemma interpret defensive actions as offensive, triggering reciprocal escalation. Each retaliatory act confirms the adversary's hostile intentions, producing a self-reinforcing escalation cycle. Jervis (1976) argues this is especially likely when offense and defense are indistinguishable — precisely the ambiguity present in air campaigns (are strikes degrading offensive capability or punishing civilian populations?). The dataset's parallel STRIKE and RETALIATION event streams provide a rare opportunity to test spiral dynamics with daily granularity.

**Escalation Ladder Theory (Kahn, 1965; Morgan et al., 2008)**

Kahn's escalation ladder theorizes that conflicts progress through discrete thresholds — each crossed threshold opens a new tier of violence. Morgan et al. (2008) updated this framework for modern asymmetric conflicts. Key thresholds observable in this dataset include: initial strikes (Day 1), Hormuz closure (Day 5), oil infrastructure targeting (Day 8), nuclear facility re-strikes (Day 22), third front opening (Day 29), and ground force deployment (Day 26+).

**Tit-for-Tat and Reciprocity (Axelrod, 1984; Goldstein, 1991)**

Goldstein's (1991) reciprocity analysis of US-Soviet and US-China interactions demonstrated that interstate conflict events follow tit-for-tat patterns with measurable lags. The action-reaction hypothesis predicts that Iranian retaliation frequency and intensity should correlate with US strike intensity at a characteristic lag (days). The dataset's day-level granularity permits lag analysis.

**Audience Costs and Escalation Commitment (Fearon, 1994)**

Fearon's audience cost theory predicts that public commitments (ultimatums, red lines) create domestic political costs for backing down, locking leaders into escalation paths. The dataset captures multiple such commitment events: Trump's 48-hour ultimatum (Day 23), the power plant strike deadline (Days 24-28), and Iran's formal rejection of the 15-point ceasefire plan (Day 26).

## Research Questions

1. Does US strike intensity predict subsequent Iranian retaliation intensity at a measurable lag, consistent with tit-for-tat dynamics?
2. Can discrete escalation thresholds be identified in the strike and retaliation time series, consistent with the escalation ladder framework?
3. Do public commitment events (ultimatums, ceasefire rejections) predict subsequent escalation spikes, consistent with audience cost theory?
4. Is the conflict spiral symmetric (both sides reciprocate equally) or asymmetric (one side drives escalation)?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `event_domain = "STRIKE"`, count per day | Daily US/Israeli offensive intensity | `day_of_conflict` groupby, count |
| `event_domain = "RETALIATION"`, count per day | Daily Iranian response intensity | `day_of_conflict` groupby, count |
| `event_type = "airstrike"`, count per day | Strike subcategory intensity | Count per day |
| `event_type = "missile_attack"`, count per day | Retaliation subcategory intensity | Count per day |
| `event_type = "rocket_attack"`, count per day | Hezbollah front intensity | Count per day |
| `event_domain = "DIPLOMATIC"` | Diplomatic events (ceasefire, ultimatum) | Filter + text classify |
| `infrastructure_target_type` | Target category escalation (military → nuclear → civilian → energy) | Track first appearance of each type over time |
| `country` | Geographic spread of retaliation | Count unique countries per day |
| `actor_initiating` | Which actor is driving escalation | Group by actor per day |
| `casualties_reported` (daily totals) | Violence intensity measure | Sum per day |
| `snapshot_targets_struck` | Cumulative US/Israeli tempo | From snapshot rows |
| `event_description` containing "ceasefire" / "ultimatum" / "deadline" / "reject" | Commitment events | Text search |
| `event_description` containing "nuclear" / "power plant" / "Kharg" | Threshold-crossing events | Text search |
| `day_of_conflict` | Temporal ordering for lag analysis | All rows |

## Proposed Analyses

### Analysis 1: Granger Causality / VAR Model
Construct daily time series of (a) STRIKE count, (b) RETALIATION count, (c) civilian casualty count. Estimate a vector autoregression (VAR) model and test for Granger causality: does yesterday's STRIKE count predict today's RETALIATION count (and vice versa)? Examine impulse response functions to estimate the lag and decay of reciprocal violence.

### Analysis 2: Threshold Detection
Construct a composite daily escalation index (weighted sum of strike count, retaliation count, new country targeted, new weapon type used, new infrastructure category struck). Apply structural break detection (Bai-Perron tests) to identify discrete threshold-crossing dates. Compare detected breakpoints against theoretically expected thresholds: first strikes, Hormuz closure, oil targeting, nuclear re-strikes, ground deployment, third front.

### Analysis 3: Commitment Event Impact
Identify commitment events from diplomatic domain events (text search for ultimatum, deadline, ceasefire, reject). Measure whether commitment events predict escalation spikes in the 48 hours following. Compare the escalation response to commitment events vs. matched military events of similar day_of_conflict.

### Analysis 4: Asymmetric Escalation
Decompose the action-reaction sequence by actor. For each day, compute the ratio of STRIKE to RETALIATION events. If the spiral is symmetric, this ratio should be approximately constant. If one side is driving escalation, the ratio should trend. Track how Iran's retaliation shifts across domains (missiles → maritime → proxy fronts → energy infrastructure targeting) as a form of horizontal escalation.

## External Data Needed
- ACLED micro-data for event validation and triangulation
- Pre-war US-Iran hostile event counts (for baseline comparison)
- Public opinion data (for audience cost analysis — AP-NORC polls mentioned in dataset)

## Key Limitations
- 30-day time series is short for VAR models — consider Bayesian estimation
- Event counts are based on OSINT reporting, not ground truth
- The dataset captures reported events, not all events — underreporting bias is possible
- Escalation is multi-dimensional; any single index is a simplification

## Key References

- Axelrod, R. (1984). *The Evolution of Cooperation*. Basic Books.
- Fearon, J. D. (1994). Domestic political audiences and the escalation of international disputes. *American Political Science Review*, 88(3), 577-592.
- Glaser, C. L. (1997). The security dilemma revisited. *World Politics*, 50(1), 171-201.
- Goldstein, J. S. (1991). Reciprocity in superpower relations: An empirical analysis. *International Studies Quarterly*, 35(2), 195-209.
- Jervis, R. (1976). *Perception and Misperception in International Politics*. Princeton University Press.
- Kahn, H. (1965). *On Escalation: Metaphors and Scenarios*. Praeger.
- Morgan, P. M., et al. (2008). *Deterrence Now*. Cambridge University Press.
