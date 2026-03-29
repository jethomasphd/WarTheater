# Paper Seed: Cumulative Trauma Exposure and Population-Level Psychological Distress in Modern Air Campaigns

## Field
Clinical Psychology / Trauma Psychology

## Target Journals
- *Journal of Traumatic Stress*
- *Psychological Trauma: Theory, Research, and Practice*
- *Clinical Psychological Science*

## Theoretical Framework

**Dose-Response Model of Cumulative Trauma Exposure (Mollica et al., 1998; Steel et al., 2009)**

The dose-response model posits that PTSD prevalence in conflict-affected populations scales with the number, severity, and duration of traumatic exposures — not merely with the occurrence of a single index trauma. Each additional traumatic event (bombing, displacement, loss of family, infrastructure destruction) functions as an additive "dose" that increases the probability of clinical-threshold symptomatology. Meta-analyses of refugee populations (Steel et al., 2009, *JAMA*) demonstrate a robust linear relationship between cumulative trauma exposure and PTSD prevalence, with each additional trauma type increasing odds of PTSD by approximately 1.2-1.5x.

**Conservation of Resources Theory (Hobfoll, 1989, 2001)**

COR theory predicts that psychological distress accelerates when individuals experience rapid, cascading resource loss — loss of home, employment, healthcare access, social networks, and safety. The "loss spiral" corollary holds that initial losses make individuals more vulnerable to subsequent losses, creating compounding psychological impact. A sustained air campaign that simultaneously destroys housing (16,000+ residential units), healthcare infrastructure (29+ hospitals damaged), and economic livelihoods (Hormuz closure, oil facility destruction) represents a multi-vector resource depletion event.

**Continuous Traumatic Stress (CTS; Eagle & Kaminer, 2013)**

Unlike PTSD — which theorizes response to past trauma — CTS describes populations living under ongoing, realistic threat. CTS predicts hypervigilance, difficulty with future orientation, and disrupted attachment as adaptive responses to continuous danger. A 30-day air campaign with daily strikes across 26 provinces creates conditions precisely matching CTS theory: the threat is not past but continuously present and unpredictable.

## Research Questions

1. How does cumulative strike exposure (measured by daily strike frequency and geographic proximity to population centers) relate to estimated population-level trauma burden across the first 30 days?
2. Does the dose-response relationship between cumulative strike events and casualty rates show acceleration (consistent with COR loss spirals) or habituation over time?
3. How do distinct trauma vectors (direct strike exposure, displacement, healthcare system collapse, economic disruption) interact to predict cumulative trauma dose in different Iranian provinces?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `event_domain = "STRIKE"` | Strike events on Iranian territory | Filter `source_file = "strikes-iran.json"` |
| `day_of_conflict` | Temporal dimension — track cumulative exposure over 30 days | Group by day |
| `location_lat`, `location_lon` | Geographic proximity analysis — which population centers face highest density | Spatial clustering |
| `active_days` (via row counts per location per day) | Daily strike tempo per location | Count rows per `location_name` per `day_of_conflict` |
| `infrastructure_target_type = "civilian"` | Direct civilian exposure events | Filter |
| `infrastructure_target_type = "healthcare"` | Healthcare system destruction as resource loss | Filter from `infrastructure.json` rows |
| `casualties_civilian` | Daily civilian casualty estimates | From `casualties.json` rows where `actor_target = "Iran (civilian)"` |
| `casualties_military` | Military casualties (separate trauma vector) | From `casualties.json` rows where `actor_target = "Iran (military)"` |
| `snapshot_displaced` | Cumulative displacement (resource loss indicator) | From `hero-stats.json` snapshot rows |
| `snapshot_children_killed` | Child mortality (indicator of family-level trauma) | From snapshot rows |
| `infrastructure_damage_count` | Cumulative infrastructure destruction | From `infrastructure.json` rows |
| `event_type = "daily_casualty_report"` | Daily faction-level toll | 150 rows (30 days x 5 factions) |

## Proposed Analyses

### Analysis 1: Cumulative Trauma Dose Curve
Construct a daily cumulative trauma exposure index by summing weighted events:
- Direct strike events within 50km of population centers (weight = 1.0)
- Civilian casualties (weight = 1.5)
- Healthcare facility damage events (weight = 2.0, per COR — healthcare loss amplifies vulnerability)
- Displacement (weight = 0.5 per 100,000 displaced)

Plot the dose curve over 30 days. Test whether the slope accelerates (COR loss spiral prediction) or decelerates (habituation/adaptation prediction).

### Analysis 2: Province-Level Exposure Mapping
Using `location_lat`/`location_lon`, map strike density to Iranian provinces. Cross-reference with pre-war population data (external) to estimate per-capita exposure rates. Identify provinces where cumulative dose exceeds thresholds associated with >30% PTSD prevalence in comparable populations (Bosnia: Priebe et al., 2010; Syria: Charlson et al., 2019).

### Analysis 3: Multi-Vector Resource Loss Model
Use the infrastructure damage data, displacement trajectory, and casualty data to construct a COR-informed resource loss index. Test whether provinces experiencing simultaneous military strikes + healthcare damage + displacement show nonlinear increases in casualty rates (consistent with loss spiral acceleration).

### Analysis 4: Temporal Pattern of Continuous Traumatic Stress
Examine whether the strike tempo data shows patterns consistent with CTS conditions: sustained, unpredictable threat with no safe period. Calculate the longest strike-free interval per province. CTS theory predicts that populations experiencing no 48-hour respite will show different symptom profiles than those with intermittent safety.

## External Data Needed (Not in Dataset)
- Iranian provincial population estimates (pre-war census or UN estimates)
- Comparable PTSD prevalence data from prior air campaigns (Iraq 2003, Gaza, Syria)
- WHO mental health gap estimates for Iran (pre-war baseline)

## Key Limitations to Acknowledge
- No direct psychological measurement — all analyses are ecological (population-level inference from exposure data)
- Casualty figures are estimates from initial reports; ground truth unavailable
- Strike locations represent city-level coordinates, not exact impact points
- Internet blackout in Iran prevents real-time survey data collection

## Estimated Timeline
- Data preparation: 1 week (the dataset is ready; need external population data)
- Analysis: 2-3 weeks
- Writing: 2-3 weeks
- Total: ~6-8 weeks to submission-ready manuscript

## Key References

- Eagle, G., & Kaminer, D. (2013). Continuous traumatic stress: Expanding the lexicon of traumatic stress. *Peace and Conflict: Journal of Peace Psychology*, 19(2), 85-99.
- Hobfoll, S. E. (1989). Conservation of resources: A new attempt at conceptualizing stress. *American Psychologist*, 44(3), 513-524.
- Hobfoll, S. E. (2001). The influence of culture, community, and the nested-self in the stress process. *Applied Psychology*, 50(3), 337-421.
- Mollica, R. F., McInnes, K., Pham, T., et al. (1998). The dose-effect relationships between torture and psychiatric symptoms in Vietnamese ex-political detainees. *Journal of Nervous and Mental Disease*, 186(9), 543-553.
- Steel, Z., Chey, T., Silove, D., Marnane, C., Bryant, R. A., & van Ommeren, M. (2009). Association of torture and other potentially traumatic events with mental health outcomes among populations exposed to mass conflict and displacement: A systematic review and meta-analysis. *JAMA*, 302(5), 537-549.
- Charlson, F., van Ommeren, M., Flaxman, A., et al. (2019). New WHO prevalence estimates of mental disorders in conflict settings: A systematic review and meta-analysis. *The Lancet*, 394(10194), 240-248.
- Priebe, S., Bogic, M., Ajdukovic, D., et al. (2010). Mental disorders following war in the Balkans: A study in 5 countries. *Archives of General Psychiatry*, 67(5), 518-528.
