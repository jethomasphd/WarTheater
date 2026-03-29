# Paper Seed: The Hidden Bill — Estimating the Full Economic Burden of the 2026 Iran War Including Healthcare, Lost Productivity, and Intergenerational Costs

## Field
Health Economics / Public Policy / War Cost Analysis

## Target Journals
- *Health Affairs*
- *Journal of Health Economics*
- *The Milbank Quarterly*
- *Value in Health*

## Theoretical Framework

**Stiglitz-Bilmes Full Cost of War Framework (Stiglitz & Bilmes, 2008)**

Stiglitz and Bilmes's landmark analysis of the Iraq War demonstrated that direct military costs represent only 20-30% of the total economic burden. The full cost includes: veterans' healthcare and disability (the single largest long-term cost), macroeconomic disruption (oil price shock, interest rate effects), opportunity costs, and social costs (mental health treatment, family disruption). Their Iraq War estimate of $3 trillion — 6x the Pentagon's direct figure — established the methodology for comprehensive war cost accounting.

**Cost-of-Illness Methodology (WHO-CHOICE; Drummond et al., 2015)**

Health economics uses the cost-of-illness framework to estimate disease burden: direct medical costs (treatment), indirect costs (lost productivity from morbidity and mortality), and intangible costs (quality-of-life loss). Applied to war, this captures: US veteran healthcare costs (projected decades forward from 300+ wounded, 13 KIA), Iranian population healthcare costs (thousands of casualties, millions displaced), and global economic disruption (oil shock affecting all importing nations).

**Value of Statistical Life (VSL) Methodology (Viscusi & Aldy, 2003)**

VSL methods assign economic value to mortality risk reduction, enabling monetization of casualty costs. US EPA's current VSL (~$13M) applied to US military deaths (13 KIA); Iranian VSL estimates (adjusted for income: ~$1-3M) applied to Iranian civilian deaths. This framework makes the human cost commensurable with the military expenditure data already in the dataset.

## Research Questions

1. What is the estimated full economic cost of the first 30 days using the Stiglitz-Bilmes comprehensive framework?
2. What is the projected long-term veteran healthcare cost based on the wounded-to-treated ratio (300+ WIA, 13 KIA)?
3. What is the economic value of Iranian civilian mortality and morbidity using income-adjusted VSL?
4. How does the oil price shock translate to consumer welfare loss across oil-importing nations?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `event_type = "daily_war_cost"` | 30 daily cost estimates (Pentagon/CSIS-anchored) | Filter — direct military cost time series |
| `snapshot_total_cost_billions` | Cumulative military cost trajectory | From snapshot rows — $35.5B by Day 30 |
| `snapshot_us_kia` | US military deaths (for VSL + VA cost projection) | From snapshot rows — 13 by Day 30 |
| `snapshot_us_wia` | US wounded (for long-term healthcare cost) | From snapshot rows — 290+ by Day 30 |
| `snapshot_iranian_killed` | Iranian deaths (for VSL calculation) | From snapshot rows |
| `snapshot_children_killed` | Child deaths (adjusted VSL + lost lifetime productivity) | From snapshot rows |
| `snapshot_displaced` | Displaced persons (productivity loss, humanitarian aid cost) | From snapshot rows — 4.2M |
| `snapshot_flights_cancelled` | Aviation disruption cost | From snapshot rows — 52,000+ |
| `financial_metric_name = "Brent Crude"` | Oil price trajectory (macro disruption cost) | From `oil-prices.json` rows |
| `financial_metric_name = "Daily US War Cost"` | Pentagon estimate time series | From `war-costs.json` rows |
| `event_type = "baseline_metric"` | Pre-war economic baselines for difference calculation | From `baselines.json` rows |
| `financial_metric_name` containing "S&P 500" | Equity market loss | From `markets.json` rows |
| `event_type = "tanker_transit"` | Supply chain disruption (trade cost) | From `war-costs.json` rows |
| `event_type = "alternative_route"` | Hormuz bypass costs | From `hormuz.json` rows |
| `event_type = "historical_comparison"` | Iraq/Gulf War cost benchmarks | 4 reference rows |
| `event_description` containing "$200B supplemental" / "Penn Wharton" / "CSIS" | Official cost estimates referenced | Text search |

## Proposed Analyses

### Analysis 1: Direct Military Cost with Uncertainty
The dataset provides two anchor points ($11.3B Day 6, $16.5B Day 12) and daily estimates extrapolated to $35.5B. Construct confidence intervals using the Stiglitz-Bilmes methodology: budget authority vs. obligations vs. outlays. Compare the $200B supplemental request against projected burn rates.

### Analysis 2: Veteran Healthcare Cost Projection
Using VA cost data from Iraq/Afghanistan (average lifetime cost per wounded veteran: $800K-$2M), project 30-year discounted healthcare costs for 300+ WIA. Apply the Iraq War ratio of 7:1 healthcare-to-initial-treatment cost (Bilmes, 2013). This is the cost that doesn't appear in the $35.5B figure.

### Analysis 3: Oil Shock Consumer Welfare Loss
Brent crude rose from $71 to $112.57 (+58.6%). Using global oil consumption data (external) and price elasticity estimates, compute the consumer welfare loss across oil-importing nations. The dataset's daily oil price series enables welfare calculation at daily resolution. Compare against the 1973 and 1979 oil shock welfare estimates (inflation-adjusted).

### Analysis 4: Full Cost Synthesis
Sum: (a) direct military ($35.5B+), (b) projected veteran healthcare ($X B), (c) macroeconomic disruption (oil shock welfare loss + market loss), (d) humanitarian cost (VSL-valued casualties), (e) environmental remediation (44+ energy assets). Compare total against Stiglitz-Bilmes Iraq War ratio. Penn Wharton's cited range ($40-95B direct military, $50-210B economic) provides an institutional benchmark.

## Key References

- Bilmes, L. J. (2013). The financial legacy of Iraq and Afghanistan: How wartime spending decisions will constrain future national security budgets. *Faculty Research Working Paper*, RWP13-006, Harvard Kennedy School.
- Drummond, M. F., Sculpher, M. J., Claxton, K., et al. (2015). *Methods for the Economic Evaluation of Health Care Programmes* (4th ed.). Oxford University Press.
- Stiglitz, J. E., & Bilmes, L. J. (2008). *The Three Trillion Dollar War: The True Cost of the Iraq Conflict*. W.W. Norton.
- Viscusi, W. K., & Aldy, J. E. (2003). The value of a statistical life: A critical review of market estimates throughout the world. *Journal of Risk and Uncertainty*, 27(1), 5-76.
