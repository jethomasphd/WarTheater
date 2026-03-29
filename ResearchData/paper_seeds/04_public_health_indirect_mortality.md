# Paper Seed: Healthcare System Collapse Under Sustained Bombardment — Modeling Indirect Mortality from Infrastructure Destruction

## Field
Public Health / Global Health / Health Systems Research

## Target Journals
- *The Lancet*
- *BMJ Global Health*
- *Conflict and Health*
- *International Journal of Environmental Research and Public Health*

## Theoretical Framework

**Indirect Mortality Multiplier (Guha-Sapir & van Panhuis, 2004; Geneva Declaration, 2008)**

The indirect-to-direct mortality ratio in armed conflict typically ranges from 3:1 to 15:1 — for every person killed directly by violence, 3-15 die from disrupted healthcare, displacement, malnutrition, and disease. The Geneva Declaration Secretariat (2008) estimated that indirect deaths constitute the majority of conflict mortality globally. This framework predicts that the infrastructure destruction documented in the dataset — 29+ hospitals damaged, 12 rendered inactive, healthcare worker deaths, pharmaceutical supply chain disruption — will generate a mortality tail far exceeding direct casualty counts.

**Health System Resilience Framework (Kruk et al., 2015, 2017)**

Kruk et al.'s resilience framework identifies five capacities essential for health systems under shock: awareness, diversity, self-regulation, integration, and adaptiveness. Systematic destruction of hospital infrastructure (12 of 31 major facilities inactive), healthcare worker casualties (42 killed in Lebanon alone), and pharmaceutical blockade (Hormuz closure severing supply chains) degrades all five capacities simultaneously. The framework predicts a tipping point beyond which the system cannot provide even emergency care.

**Environmental Health Cascade (WHO, 2017; Levy & Sidel, 2008)**

Strikes on oil and chemical infrastructure produce secondary environmental health threats: toxic plumes, water contamination, and soil pollution. WHO warned of "toxic black rainfall" from oil infrastructure strikes. The dataset documents 44+ energy assets severely damaged across 9 countries, including refineries that produce toxic byproducts when destroyed.

## Research Questions

1. What is the estimated indirect mortality multiplier for the first 30 days, based on the rate and type of healthcare infrastructure destruction?
2. At what day of conflict did the healthcare system likely cross the resilience threshold (point of no return for emergency care capacity)?
3. How does the geographic distribution of hospital damage correlate with strike density and civilian casualty patterns?
4. What is the estimated additional disease burden from environmental contamination following energy infrastructure strikes?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `infrastructure_target_type = "healthcare"` | Hospital damage events | Filter from `infrastructure.json` rows |
| `infrastructure_damage_count` (healthcare row) | Count of damaged hospitals (29+) | Direct value |
| `infrastructure_target_type = "oil_infrastructure"` | Energy infrastructure damage | Filter — environmental health cascade |
| `infrastructure_damage_count` (oil/gas row) | Count of damaged energy assets (44+) | Direct value |
| `casualties_civilian` per day | Daily Iranian civilian killed | From `casualties.json` rows, `actor_target = "Iran (civilian)"` |
| `casualties_military` per day | Daily Iranian military killed | From `casualties.json` rows, `actor_target = "Iran (military)"` |
| `snapshot_displaced` | Cumulative displaced (healthcare access disruption) | From snapshot rows |
| `snapshot_iranian_killed` | Cumulative Iranian dead | From snapshot rows |
| `snapshot_children_killed` | Child mortality trajectory | From snapshot rows |
| `event_domain = "STRIKE"` + `infrastructure_target_type = "civilian"` | Strikes hitting civilian infrastructure | Combined filter |
| `event_description` containing "hospital" / "healthcare" / "WHO" / "Red Crescent" | Healthcare-related events across all sources | Text search on all rows |
| `event_type = "infrastructure_damage"` | All 7 infrastructure damage categories | Filter |
| `day_of_conflict` | Temporal trajectory of system degradation | All rows, group by day |
| `location_name`, `location_lat`, `location_lon` | Geographic mapping of healthcare destruction | From strike rows near known hospital coordinates |

## Proposed Analyses

### Analysis 1: Indirect Mortality Estimation
Apply the indirect mortality multiplier framework to the dataset. Using the daily civilian casualty trajectory (150 data points: 30 days x 5 factions), estimate total direct deaths. Apply region-appropriate multipliers from comparable conflicts (Iraq: 2.5x per Roberts et al., 2004; Syria: 6x per Guha-Sapir et al., 2015) to estimate indirect deaths. Construct confidence intervals reflecting multiplier uncertainty.

### Analysis 2: Healthcare System Resilience Curve
Construct a daily healthcare capacity index using: (a) cumulative hospitals damaged, (b) hospitals rendered inactive, (c) healthcare worker casualties, (d) displacement as a proxy for demand surge. Model the capacity curve and identify the inflection point where remaining capacity falls below estimated emergency demand. Cross-reference with the day_of_conflict timeline to identify when the tipping point likely occurred.

### Analysis 3: Strike-Healthcare Spatial Analysis
Using strike coordinates (`location_lat`, `location_lon`) and known hospital locations in Iran (from WHO EMRO facility database), measure the spatial correlation between strike density and healthcare facility damage. Test whether hospitals within N km of military targets face higher damage rates, consistent with collateral damage patterns vs. deliberate targeting.

### Analysis 4: Environmental Health Burden Estimation
The dataset documents 44+ energy assets damaged, Kharg Island oil terminal destruction, and WHO warnings of toxic rainfall. Using EPA/WHO exposure models for oil refinery destruction products (benzene, toluene, PM2.5, SO2), estimate the population exposed to acute and chronic environmental health hazards. Map the plume footprint against population density using strike coordinates near oil infrastructure.

## External Data Needed
- WHO EMRO health facility database for Iran (geo-coordinates of hospitals)
- Pre-war Iranian healthcare capacity data (beds per capita, physician density)
- Comparable indirect mortality ratios from Iraq (2003-2011), Syria, Yemen
- Air quality modeling tools (AERMOD or CALPUFF) for environmental analysis
- Iranian provincial population and demographic data

## Key Limitations
- Infrastructure damage counts are cumulative minimums (e.g., "29+" → 29)
- No direct data on healthcare utilization or pharmaceutical supply
- Environmental health estimates require atmospheric modeling beyond the dataset
- Indirect mortality estimation is inherently uncertain (wide confidence intervals)

## Key References

- Geneva Declaration Secretariat. (2008). *Global Burden of Armed Violence*. Geneva.
- Guha-Sapir, D., & van Panhuis, W. G. (2004). Conflict-related mortality: An analysis of 37 datasets. *Disasters*, 28(4), 418-428.
- Kruk, M. E., Myers, M., Varpilah, S. T., & Dahn, B. T. (2015). What is a resilient health system? Lessons from Ebola. *The Lancet*, 385(9980), 1910-1912.
- Levy, B. S., & Sidel, V. W. (2008). *War and Public Health* (2nd ed.). Oxford University Press.
- Roberts, L., Lafta, R., Garfield, R., et al. (2004). Mortality before and after the 2003 invasion of Iraq. *The Lancet*, 364(9448), 1857-1864.
