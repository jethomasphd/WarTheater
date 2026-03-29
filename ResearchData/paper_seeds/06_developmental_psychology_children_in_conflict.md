# Paper Seed: The Minab Generation — Estimating Child Trauma Exposure and Developmental Risk in the 2026 Iran Air Campaign

## Field
Developmental Psychology / Child and Adolescent Psychiatry

## Target Journals
- *Development and Psychopathology*
- *Journal of Child Psychology and Psychiatry*
- *Journal of the American Academy of Child & Adolescent Psychiatry*
- *Child Development*

## Theoretical Framework

**Developmental Psychopathology Framework (Cicchetti & Cohen, 2006; Masten & Narayan, 2012)**

War exposure during sensitive developmental periods produces differential effects depending on the child's age. Infants and toddlers (0-3) are affected primarily through disrupted attachment with traumatized caregivers. Preschool children (3-6) manifest behavioral regression and separation anxiety. School-age children (7-12) — the age group of the Minab school victims — develop persistent fear, somatic complaints, and academic deterioration. Adolescents (13-18) show increased risk for conduct problems, substance use, and political radicalization. The developmental psychopathology framework predicts that the same stressor (air strikes) produces qualitatively different outcomes depending on developmental stage.

**Toxic Stress and the ACE Framework (Shonkoff et al., 2012; Felitti et al., 1998)**

The Adverse Childhood Experiences (ACE) framework, extended to conflict settings by Shonkoff's ecobiodevelopmental model, predicts that sustained exposure to threat without adequate buffering relationships produces "toxic stress" — prolonged activation of the stress response system that permanently alters brain architecture. A 30-day air campaign affecting children across 26 provinces generates population-level toxic stress exposure. The key moderating variable is the availability of buffering relationships (caregivers), which is itself degraded by displacement (4.2M displaced), caregiver death, and family separation.

**Boothby's Model of War-Affected Children (Boothby et al., 2006)**

Boothby's longitudinal work with Mozambican child soldiers and war-affected children demonstrates that children's outcomes depend on: (a) nature of exposure, (b) duration, (c) proximity, (d) loss of caregivers, and (e) post-conflict support. The dataset allows estimation of (a)-(d) at the population level using strike density, campaign duration, geographic proximity to population centers, and displacement/casualty data.

## Research Questions

1. How many Iranian children (estimated) experienced direct conflict exposure (strikes within 10km of their location) during the first 30 days?
2. What is the estimated cumulative ACE burden for children in the most heavily struck provinces?
3. Does the Minab school incident (165+ children killed) represent an outlier or a predictable outcome of the strike pattern?
4. What is the projected PTSD and developmental disorder prevalence for Iranian children ages 0-18 based on exposure estimates and comparable conflict data?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `snapshot_children_killed` | Cumulative child mortality trajectory | From snapshot rows — time series across 30 days |
| `source_record_id = "minab-school"` | The index incident — school strike | Filter from strikes-iran.json rows |
| `infrastructure_target_type = "civilian"` | Strikes on civilian infrastructure (schools, residential) | Filter — proxy for child exposure |
| `event_description` containing "school" / "children" / "girls" / "residential" | Child-proximate events across all sources | Text search on all 1,653 rows |
| `location_lat`, `location_lon` for STRIKE events | Geographic exposure mapping | Spatial analysis against population density |
| `day_of_conflict` | Duration of exposure — 30 continuous days | All rows |
| `snapshot_displaced` | Family displacement trajectory (caregiver disruption) | From snapshot rows |
| `casualties_civilian` per day | Daily civilian deaths (proxy for caregiver loss) | From `casualties.json` rows |
| `infrastructure_damage_count` (schools, hospitals) | Institutional support destruction | From `infrastructure.json` rows |
| `event_type = "infrastructure_damage"`, label = "Schools Destroyed" | School-specific damage | Filter |
| `event_description` containing "Minab" | All mentions of the school incident across sources | Text search |

## Proposed Analyses

### Analysis 1: Population Exposure Estimation
Using strike coordinates and Iranian provincial population data (external, from UN Population Division), estimate the number of children aged 0-18 within 10km, 25km, and 50km of at least one strike site. Use the 30-day temporal dimension to compute exposure-days (child-days under active bombardment). This is the denominator for all subsequent prevalence estimates.

### Analysis 2: Cumulative ACE Burden
Construct a conflict-specific ACE index for Iranian children incorporating: (a) living within a strike zone, (b) displacement, (c) loss of caregiver (estimated from adult casualty rates), (d) healthcare system collapse (hospital damage), (e) school destruction, (f) witnessing violence. Map the daily ACE accumulation trajectory using the time-series data. Compare against Felitti et al.'s dose-response curves for long-term health outcomes.

### Analysis 3: Minab as Case Study
Extract all dataset rows mentioning Minab (`source_record_id = "minab-school"` and text matches). Reconstruct the full event narrative using timeline events, strike records, and diplomatic responses. Analyze within Boothby's framework: nature of exposure (direct strike on school), proximity (zero — children were at the impact point), loss of caregivers (teachers killed, parents arriving during triple-tap), and post-incident support (healthcare system degraded, access blocked). Test whether the Minab targeting pattern (IRGC naval base adjacent to school, outdated intelligence) is replicated at other dual-use sites in the dataset.

### Analysis 4: Projected Developmental Impact
Using PTSD prevalence data from comparable child populations (Gaza: Thabet et al., 2004 — 41% PTSD; Syria: Perkins et al., 2018 — 45-60% PTSD; Iraq: Razokhi et al., 2006 — 47% PTSD) and the estimated exposure population from Analysis 1, project the expected PTSD, depression, and developmental disorder prevalence for Iranian children. Model uncertainty using Monte Carlo simulation with ranges from comparable conflict data.

## External Data Needed
- Iranian provincial population by age group (UN Population Division)
- School enrollment data by province (UNESCO/UNICEF)
- Comparable PTSD prevalence in children from Iraq, Syria, Gaza, Yemen
- Pre-war Iranian child mental health baseline (WHO Atlas)

## Key References

- Boothby, N., Strang, A., & Wessells, M. (2006). *A World Turned Upside Down: Social Ecological Approaches to Children in War Zones*. Kumarian Press.
- Cicchetti, D., & Cohen, D. J. (Eds.). (2006). *Developmental Psychopathology* (2nd ed.). Wiley.
- Felitti, V. J., Anda, R. F., Nordenberg, D., et al. (1998). Relationship of childhood abuse and household dysfunction to many of the leading causes of death in adults. *American Journal of Preventive Medicine*, 14(4), 245-258.
- Masten, A. S., & Narayan, A. J. (2012). Child development in the context of disaster, war, and terrorism. *Annual Review of Psychology*, 63, 227-257.
- Shonkoff, J. P., Garner, A. S., et al. (2012). The lifelong effects of early childhood adversity and toxic stress. *Pediatrics*, 129(1), e232-e246.
- Thabet, A. A., Abed, Y., & Vostanis, P. (2004). Comorbidity of PTSD and depression among refugee children during war conflict. *Journal of Child Psychology and Psychiatry*, 45(3), 533-542.
