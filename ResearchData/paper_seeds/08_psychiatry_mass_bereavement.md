# Paper Seed: Mass Bereavement Under Bombardment — Modeling Prolonged Grief Disorder Risk in Populations Exposed to Sustained Air Campaigns

## Field
Psychiatry / Bereavement Research

## Target Journals
- *World Psychiatry*
- *JAMA Psychiatry*
- *Psychological Medicine*
- *European Journal of Psychotraumatology*

## Theoretical Framework

**Prolonged Grief Disorder (PGD; Prigerson et al., 2009; WHO ICD-11)**

PGD was codified in ICD-11 (2019) and DSM-5-TR (2022) as a distinct diagnostic entity characterized by persistent, pervasive longing for the deceased and functional impairment lasting >6 months (ICD-11) or >12 months (DSM-5-TR). Prevalence following violent or unexpected death is 2-5x higher than after natural death (Lundorff et al., 2017). Key risk factors include: sudden/violent death, loss of a child, loss of multiple family members simultaneously, inability to perform death rituals, and lack of social support — all of which are systematically produced by sustained air campaigns.

**Complicated Grief and Continuing Bonds (Stroebe & Schut, 1999; Klass et al., 1996)**

The Dual Process Model of bereavement predicts that healthy grieving oscillates between loss-oriented coping (confronting grief) and restoration-oriented coping (rebuilding daily life). Sustained bombardment collapses the restoration-oriented pathway — there is no "daily life" to rebuild when strikes continue daily. This predicts that populations under sustained air attack will show disproportionately high rates of loss-oriented rumination and PGD.

**Collective Bereavement and Meaning-Making (Neimeyer, 2001; Smid et al., 2015)**

Meaning-making theory posits that grief becomes complicated when the death violates the bereaved person's "assumptive world" — their fundamental beliefs about justice, safety, and predictability. The Minab school incident (165+ children killed by a Tomahawk missile due to outdated intelligence) maximally violates assumptive worlds: children are supposed to be safe at school, and precision weapons are supposed to discriminate. Smid et al.'s (2015) work on disaster bereavement demonstrates that deaths perceived as preventable generate more severe PGD.

## Research Questions

1. What is the estimated population at risk for PGD in Iran and Lebanon based on the daily casualty trajectory and known PGD risk ratios?
2. How do specific event characteristics documented in the dataset (sudden mass casualty events, child deaths, hospital destruction preventing body recovery) map to established PGD risk factors?
3. Does the 30-day continuous bombardment pattern create conditions that systematically prevent the restoration-oriented coping pathway predicted by the Dual Process Model?
4. Which specific events in the dataset represent maximum PGD risk multipliers (Minab school, Beit Shemesh synagogue, residential area strikes)?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `casualties_civilian` per day (Iranian) | Daily new bereavement events | From `casualties.json` rows |
| `casualties_military` per day (all factions) | Military bereavement | From `casualties.json` rows |
| `snapshot_children_killed` | Child death trajectory (highest PGD risk factor) | From snapshot rows |
| `snapshot_iranian_killed` | Cumulative death toll (total bereavement pool) | From snapshot rows |
| `snapshot_lebanese_killed` | Lebanese bereavement pool | From snapshot rows |
| `event_description` containing "killed" / "dead" / "KIA" / "fatalities" | Mass casualty incident identification | Text search across all rows |
| `source_record_id = "minab-school"` | Index case: maximum PGD risk event | Filter |
| `source_record_id = "beit-shemesh-israel"` | Israeli mass casualty event (9 killed including 3 siblings) | Filter |
| `source_record_id = "tehran-east-residential"` | Residential mass casualty (40+ killed, 1 AM Ramadan) | Filter |
| `infrastructure_target_type = "healthcare"` | Hospital destruction (prevents body recovery, death rituals) | Filter |
| `day_of_conflict` | Duration of continuous threat (blocks restoration coping) | All rows |
| `snapshot_displaced` | Displacement (disrupts grief communities and burial practices) | From snapshot rows |

## Proposed Analyses

### Analysis 1: PGD Population Risk Estimation
Using daily casualty data and established multipliers (each violent death affects 5-10 close bereaved; PGD prevalence 10-20% after violent loss per Lundorff et al., 2017), estimate the number of individuals at risk for PGD by Day 30. Construct daily cumulative curves. Factor in elevated risk for child loss (2-3x multiplier per Li et al., 2003) using `snapshot_children_killed`.

### Analysis 2: Event-Level PGD Risk Profiling
Score each mass casualty event in the dataset against Lobb et al.'s (2010) PGD risk factor checklist: (a) sudden/violent death, (b) loss of child, (c) multiple losses, (d) inability to recover body, (e) perceived preventability. The Minab school incident scores maximum on all five factors. Identify how many events in the dataset score 4/5 or 5/5.

### Analysis 3: Dual Process Model Disruption Analysis
The Dual Process Model requires oscillation between grief and daily-life restoration. Compute the longest continuous bombardment period per major population center (using strike data grouped by location). For Tehran (struck on 25 of 30 days per `active_days`), the restoration pathway is effectively eliminated. Compare against CTS literature predictions.

### Analysis 4: Cross-National Bereavement Comparison
The dataset contains casualties for 5 factions across 3 primary countries (Iran, Lebanon, Israel). Compare the bereavement profile: Iran faces sustained air campaign (high volume, continuous), Lebanon faces ground-plus-air campaign (displacement-dominant), Israel faces missile attacks (sudden, intermittent). The Dual Process Model predicts different PGD profiles for each pattern.

## External Data Needed
- PGD prevalence data from comparable conflicts (Gaza, Syria, Iraq)
- Iranian funeral/burial practice data (Shia rituals disrupted by continuous bombing)
- Family size and household composition data for Iran (to estimate bereaved per death)

## Key References

- Lundorff, M., Holmgren, H., Zachariae, R., et al. (2017). Prevalence of prolonged grief disorder in adult bereavement: A systematic review and meta-analysis. *Journal of Affective Disorders*, 212, 138-149.
- Neimeyer, R. A. (2001). *Meaning Reconstruction and the Experience of Loss*. American Psychological Association.
- Prigerson, H. G., Horowitz, M. J., Jacobs, S. C., et al. (2009). Prolonged grief disorder: Psychometric validation of criteria proposed for DSM-V and ICD-11. *PLoS Medicine*, 6(8), e1000121.
- Smid, G. E., Kleber, R. J., de la Rie, S. M., et al. (2015). Brief eclectic psychotherapy for traumatic grief (BEP-TG): Toward integrated treatment of symptoms related to traumatic loss. *European Journal of Psychotraumatology*, 6, 27324.
- Stroebe, M., & Schut, H. (1999). The Dual Process Model of coping with bereavement: Rationale and description. *Death Studies*, 23(3), 197-224.
