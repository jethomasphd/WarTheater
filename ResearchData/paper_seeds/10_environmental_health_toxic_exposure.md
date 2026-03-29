# Paper Seed: Black Rain — Estimating Population-Level Toxic Exposure from Deliberate Destruction of Oil and Chemical Infrastructure

## Field
Environmental Health / Toxicology / Occupational and Environmental Medicine

## Target Journals
- *Environmental Health Perspectives*
- *International Journal of Environmental Research and Public Health*
- *Environment International*
- *Journal of Exposure Science & Environmental Epidemiology*

## Theoretical Framework

**Environmental Dimensions of Armed Conflict (UNEP, 2009; Weir & McQuillan, 2020)**

UNEP's post-conflict environmental assessments (Kosovo, Iraq, Gaza, Lebanon) demonstrate that deliberate destruction of industrial infrastructure produces acute and chronic environmental health hazards extending far beyond the immediate blast zone. The Iraq oil well fires (1991) produced PM2.5, SO2, and polycyclic aromatic hydrocarbons (PAHs) affecting populations across the Gulf. The dataset documents 44+ energy assets "severely damaged" across 9 countries — a destruction footprint exceeding both the 1991 Kuwait oil fires and the 2006 Lebanon Jiyeh power plant spill.

**Source-Pathway-Receptor Model (WHO Environmental Health Criteria)**

The SPR model traces contamination from release (destroyed refinery) through environmental pathway (atmospheric plume, water contamination, soil deposition) to human receptor (inhalation, dermal contact, ingestion). The dataset provides the "source" component: specific coordinates and types of destroyed energy infrastructure. WHO's "toxic black rainfall" warning validates atmospheric pathway activation.

## Research Questions

1. What is the total industrial hazardous material release implied by the 44+ energy assets documented as severely damaged?
2. Using atmospheric dispersion modeling, what population is within the acute exposure zone of major refinery/oil terminal destruction events?
3. What are the expected acute and chronic health outcomes (respiratory, carcinogenic, reproductive) for exposed populations?
4. How does this environmental release compare to historical industrial disasters and prior conflict-related environmental damage?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `infrastructure_target_type = "oil_infrastructure"` | All energy infrastructure strike events | Filter from STRIKE rows |
| `infrastructure_damage_count` (oil/gas row = 44) | Cumulative damaged energy assets | From `infrastructure.json` |
| `location_lat`, `location_lon` for oil/energy strikes | Source coordinates for plume modeling | Filter STRIKE rows where `infrastructure_target_type = "oil_infrastructure"` |
| `source_record_id` containing "kharg" / "abadan" / "south-pars" | Major energy facility strikes | Filter |
| `event_description` containing "refinery" / "oil" / "toxic" / "smoke" / "fire" / "chemical" / "rainfall" | Environmental contamination events | Text search across all rows |
| `event_description` containing "WHO" / "black rain" / "environmental" | Official warnings | Text search |
| `day_of_conflict` | Temporal sequence of infrastructure destruction | All energy-related rows by day |
| `snapshot_displaced` | Displaced populations (potentially moving through contaminated zones) | From snapshot rows |

## Key References

- UNEP. (2009). *Protecting the Environment During Armed Conflict: An Inventory and Analysis of International Law*. UNEP.
- Weir, D., & McQuillan, D. (2020)."; *Conflict and the Environment*. Palgrave Macmillan.
- Levy, B. S., & Sidel, V. W. (2008). *War and Public Health* (2nd ed.). Oxford University Press.
