# Research Paper Seeds

Each file in this directory is a detailed research paper proposal grounded in disciplinary theory, with explicit variable mappings to the `iranwar_event_dataset.csv` dataset. These are designed to help researchers across fields quickly identify viable projects and get to analysis.

## Index

| # | File | Field | Core Theory | Key Dataset Variables |
|---|------|-------|-------------|---------------------|
| 01 | `01_clinical_psychology_cumulative_trauma.md` | Clinical Psychology | Dose-response model (Mollica/Steel), Conservation of Resources (Hobfoll), Continuous Traumatic Stress (Eagle & Kaminer) | STRIKE events by day/location, casualties_civilian, snapshot_displaced, infrastructure damage |
| 02 | `02_financial_economics_oil_shock.md` | Financial Economics | EMH/Event study (Fama/MacKinlay), Oil shock transmission (Kilian), Geopolitical risk premium (Caldara & Iacoviello) | Brent/WTI prices, tanker transits, STRIKE/RETALIATION counts, market indices |
| 03 | `03_political_science_escalation_dynamics.md` | Political Science | Spiral model (Jervis), Escalation ladder (Kahn), Tit-for-tat (Axelrod/Goldstein), Audience costs (Fearon) | Daily STRIKE vs RETALIATION counts, DIPLOMATIC events, infrastructure_target_type progression |
| 04 | `04_public_health_indirect_mortality.md` | Public Health | Indirect mortality multiplier (Guha-Sapir), Health system resilience (Kruk), Environmental health cascade (WHO) | Infrastructure damage (healthcare), civilian casualties, displaced, energy facility strikes |
| 05 | `05_military_studies_air_campaign_effectiveness.md` | Military Studies | Five Rings (Warden), Denial vs Punishment (Pape), Effects-Based Operations (Deptula) | All 620 STRIKE rows with infrastructure_target_type, RETALIATION tempo decline, historical comparisons |
| 06 | `06_developmental_psychology_children_in_conflict.md` | Developmental Psychology | Developmental psychopathology (Cicchetti), Toxic stress/ACE (Shonkoff/Felitti), War-affected children (Boothby) | snapshot_children_killed, Minab school records, civilian infrastructure strikes, snapshot_displaced |
| 07 | `07_international_relations_alliance_fragmentation.md` | International Relations | Alliance reliability (Leeds), Burden-sharing (Olson & Zeckhauser), Institutional binding (Ikenberry) | actor_initiating distribution, NAVAL assets by country, DIPLOMATIC events mentioning allies/institutions |
| 08 | `08_psychiatry_mass_bereavement.md` | Psychiatry | Prolonged Grief Disorder (Prigerson/ICD-11), Dual Process Model (Stroebe & Schut), Meaning-making (Neimeyer) | Daily casualty trajectories, mass casualty events (Minab, Beit Shemesh), snapshot_children_killed, healthcare destruction |
| 09 | `09_peace_conflict_studies_ceasefire_dynamics.md` | Peace & Conflict Studies | Bargaining model (Fearon), Ripeness theory (Zartman), Two-level games (Putnam) | DIPLOMATIC events (ceasefire/ultimatum text), STRIKE/RETALIATION tempo, war costs, domestic opposition events |
| 10 | `10_environmental_health_toxic_exposure.md` | Environmental Health | Conflict environmental damage (UNEP), Source-Pathway-Receptor model (WHO) | Oil infrastructure strike coordinates, infrastructure_damage_count, WHO warning events |
| 11 | `11_media_studies_information_warfare.md` | Media/Communication | Framing theory (Entman), Propaganda model (Herman & Chomsky), Strategic narrative (Miskimmon) | timeline_source attribution, event_description text, daily briefing headlines, event_domain shifts over time |
| 12 | `12_health_economics_war_cost_burden.md` | Health Economics | Stiglitz-Bilmes full cost framework, Cost-of-illness (WHO-CHOICE), Value of Statistical Life (Viscusi) | daily_war_cost, snapshot totals (cost, KIA, WIA, displaced), oil prices, baseline metrics, historical comparisons |

## Structure of Each Seed

Every paper seed includes:
1. **Field and target journals**
2. **Theoretical framework** — specific named theories with citations
3. **Research questions** — 3-4 testable questions
4. **Dataset variable mapping** — exact column names, filters, and operations needed
5. **Proposed analyses** — concrete analytical steps
6. **External data needed** — what's not in the dataset
7. **Key limitations**
8. **References**

## How to Use

1. Pick a seed that matches your expertise
2. Review the variable mapping table — these link directly to columns in `iranwar_event_dataset.csv`
3. Load the dataset: `pd.read_csv('iranwar_event_dataset.csv')`
4. Filter using the operations described in the mapping table
5. Bring your own external data where noted
6. Cite the dataset using the format in `dataset_README.md`
