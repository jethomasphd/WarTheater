# Paper Seed: Oil Shock Transmission Under Chokepoint Warfare — Event Study Evidence from the 2026 Hormuz Closure

## Field
Financial Economics / Energy Economics

## Target Journals
- *Journal of Financial Economics*
- *The Energy Journal*
- *Journal of International Economics*
- *Review of Financial Studies*

## Theoretical Framework

**Efficient Markets Hypothesis and Event Study Methodology (Fama, 1970; MacKinlay, 1997)**

The semi-strong form of EMH predicts that asset prices incorporate publicly available information rapidly. Event studies exploit this by measuring abnormal returns around discrete information events. The 2026 Hormuz closure provides an exceptionally rich event study setting: the dataset contains 293 time-stamped events that constitute information shocks — each with an identifiable category (military strike, diplomatic development, financial announcement) — alongside daily oil price and market index data.

**Oil Price Shock Transmission (Hamilton, 2003; Kilian, 2009)**

Kilian's (2009, *American Economic Review*) structural decomposition distinguishes three types of oil shocks: supply disruptions, aggregate demand shocks, and speculative demand (precautionary) shocks. The Hormuz closure is a textbook supply disruption — 20% of global oil transits eliminated — but the dataset allows us to test whether the observed price path reflects pure supply loss or whether precautionary demand (insurance cascades, inventory hoarding) amplifies the shock. The tanker transit data provides a direct physical measure of supply disruption intensity, independent of price.

**Geopolitical Risk Premium (Caldara & Iacoviello, 2022)**

Caldara and Iacoviello's GPR index demonstrates that geopolitical events generate persistent risk premiums in commodity and equity markets. Their framework predicts that escalatory events (new fronts opening, failed ceasefires) increase the premium, while de-escalatory events (ceasefire proposals, diplomatic talks) decrease it. The dataset's event-level classification allows direct measurement of escalation/de-escalation shocks.

## Research Questions

1. What is the abnormal return on crude oil around each category of military event (strike on Iran, Iranian retaliation, Hormuz vessel attack, diplomatic event)?
2. Does the physical supply disruption (tanker transit count) or the information shock (event frequency) better predict daily oil price movements?
3. Do ceasefire-related diplomatic events produce symmetric price decreases relative to escalatory military events?
4. How does the oil shock transmit to equity sectors (defense vs. airlines vs. broad market)?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `financial_metric_name = "Brent Crude"` | Dependent variable — daily oil price | Filter from `oil-prices.json` rows |
| `financial_metric_name = "WTI Crude"` | Secondary DV — US benchmark | Filter |
| `financial_metric_name = "Hormuz Tanker Transits"` | Physical supply disruption measure | Filter from `war-costs.json` rows |
| `event_domain = "STRIKE"` | Military event count — strikes on Iran | Count per day |
| `event_domain = "RETALIATION"` | Military event count — Iranian response | Count per day |
| `event_type = "missile_attack"` | Retaliation intensity subcategory | Count per day |
| `event_domain = "DIPLOMATIC"` | Diplomatic shock events | Count per day |
| `financial_metric_name` containing "S&P 500" | Equity market response | From `markets.json` rows |
| `financial_metric_name` containing "Defense" | Sector rotation — defense | From `markets.json` rows |
| `financial_metric_name` containing "Airlines" | Sector rotation — airlines | From `markets.json` rows |
| `financial_metric_name` containing "Oil Majors"` | Sector rotation — energy | From `markets.json` rows |
| `event_type = "daily_war_cost"` | Fiscal cost escalation | From `war-costs.json` rows |
| `snapshot_brent`, `snapshot_wti`, `snapshot_sp500` | Daily snapshot crosswalk | From `hero-stats.json` snapshot rows |
| `event_description` (text search for "ceasefire", "negotiate", "ultimatum") | Event-level escalation coding | Text analysis on DIPLOMATIC events |

## Proposed Analyses

### Analysis 1: Multi-Category Event Study
Construct event windows around each of the 293 timeline events. Categorize into escalatory (strikes, retaliations, Hormuz attacks, ultimatums) and de-escalatory (ceasefire proposals, diplomatic talks, sanctions relief). Estimate cumulative abnormal returns (CARs) in Brent crude for [-1, +1] day windows using a pre-war estimation period (Jan 2 – Feb 27) for the market model.

### Analysis 2: Physical vs. Information Channels
Regress daily Brent crude changes on (a) tanker transit count (physical supply proxy), (b) STRIKE event count, (c) RETALIATION event count, and (d) DIPLOMATIC event count. Test whether physical disruption or information flow dominates price formation. The tanker data (33 daily observations) provides a rare direct measure of supply flow that is independent of price.

### Analysis 3: Sector Rotation Dynamics
Using the normalized market indices (S&P 500, Defense, Oil Majors, Airlines — all indexed to 100 on Feb 27), estimate sector-level betas relative to oil price changes. Test whether defense stocks positively co-move with oil (both benefit from escalation) while airlines negatively co-move. Examine time variation: does the defense-oil correlation strengthen as the war progresses?

### Analysis 4: Asymmetric Response to Escalation vs. De-escalation
The dataset contains identifiable de-escalation events (Day 24: Trump postpones strikes, Brent drops 13.6%; Day 26: 15-point ceasefire plan, Brent drops 3.5%) and re-escalation (Day 27: Iran rejects ceasefire, Brent surges; Day 29: Houthis open third front, Brent +4.2%). Test for asymmetry: do escalatory shocks produce larger absolute price movements than de-escalatory ones of comparable magnitude?

## External Data Needed
- Intraday oil futures data from ICE/NYMEX (for higher-frequency event studies)
- VIX data (daily — partially available in baselines.json)
- OPEC+ production data (for supply counterfactuals)
- War risk insurance premium data (Lloyd's)

## Key Limitations to Acknowledge
- Oil prices in the dataset are daily chart-display values, not exact closing prices
- Market indices are normalized (Feb 27 = 100), not raw values — for raw S&P, use snapshot_sp500
- Only 21 trading days in the war period — limited statistical power for complex models
- Pre-war estimation period is short (9 weeks of weekly data)

## Key References

- Caldara, D., & Iacoviello, M. (2022). Measuring geopolitical risk. *American Economic Review*, 112(4), 1194-1225.
- Fama, E. F. (1970). Efficient capital markets: A review of theory and empirical work. *Journal of Finance*, 25(2), 383-417.
- Hamilton, J. D. (2003). What is an oil shock? *Journal of Econometrics*, 113(2), 363-398.
- Kilian, L. (2009). Not all oil price shocks are alike: Disentangling demand and supply shocks in the crude oil market. *American Economic Review*, 99(3), 1053-1069.
- MacKinlay, A. C. (1997). Event studies in economics and finance. *Journal of Economic Literature*, 35(1), 13-39.
