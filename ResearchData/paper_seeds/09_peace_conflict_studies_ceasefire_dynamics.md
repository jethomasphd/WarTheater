# Paper Seed: Why Ceasefires Fail — Bargaining, Information Asymmetry, and the Collapse of the 15-Point Plan

## Field
Peace and Conflict Studies / Conflict Resolution

## Target Journals
- *Journal of Peace Research*
- *Journal of Conflict Resolution*
- *International Negotiation*
- *Negotiation Journal*

## Theoretical Framework

**Bargaining Model of War (Fearon, 1995; Powell, 2006)**

Fearon's rationalist explanation for war identifies three mechanisms that prevent bargained settlements: private information with incentives to misrepresent, commitment problems, and issue indivisibilities. The 2026 ceasefire negotiations exhibit all three: Iran's actual missile stockpile depletion rate is private information (the dataset shows declining launch rates, but Iran has incentives to conceal this), the US commitment to stop strikes is non-credible (Trump's shifting deadlines: 48 hours → 5 days → 10 days), and Iran's nuclear program represents an issue both sides treat as indivisible.

**Ripeness Theory (Zartman, 2000)**

Zartman's "mutually hurting stalemate" theory predicts that negotiations succeed only when both sides perceive continued fighting as costlier than compromise. The dataset allows direct measurement of each side's pain trajectory: for Iran, cumulative strikes and economic devastation; for the US, war costs ($35.5B), domestic opposition (59% say war "gone too far"), and oil price disruption. The 15-point ceasefire plan's rejection on Day 26 suggests the stalemate was not yet "ripe" — at least one side still perceived fighting as preferable.

**Two-Level Game Theory (Putnam, 1988)**

Putnam's framework explains negotiation failure as a consequence of domestic politics constraining international bargaining. The dataset captures both levels: internationally, the 15-point plan and Iran's 5-point counterproposal; domestically, the Kaine-Paul war powers vote (47-53), Speaker Johnson's "almost done" framing, AP-NORC polls (59% oppose), and Iran's IRGC university ultimatum. Both leaders face domestic win-sets that may not overlap.

## Research Questions

1. Does the daily strike/retaliation data show convergence toward a mutually hurting stalemate, or does one side's pain curve plateau while the other's accelerates?
2. Can the failure of the 15-point ceasefire plan be explained by information asymmetry about Iranian military capability depletion?
3. Do Trump's shifting ultimatum deadlines (48hrs → 5 days → 10 days → Apr 6) represent rational updating or audience cost entrapment?
4. How does third-party mediation structure (Oman, Turkey, Egypt, Pakistan — the Islamabad quartet) compare to theoretical predictions about mediator characteristics?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `event_domain = "DIPLOMATIC"` | All 66 diplomatic events — the negotiation record | Filter |
| `event_description` containing "ceasefire" / "15-point" / "5-point" / "counterproposal" | Specific ceasefire proposal events | Text search |
| `event_description` containing "ultimatum" / "deadline" / "postpone" / "extend" | Commitment/credibility events | Text search |
| `event_description` containing "Pakistan" / "Oman" / "Turkey" / "Egypt" / "Islamabad" | Mediator activity | Text search |
| `event_domain = "STRIKE"`, count per day | US/Israeli pain infliction rate | Count per day |
| `event_domain = "RETALIATION"`, count per day | Iranian pain infliction rate | Count per day — declining trend = depletion signal |
| `financial_metric_name = "Daily US War Cost"` | US cost trajectory | From `war-costs.json` rows |
| `snapshot_total_cost_billions` | Cumulative US cost | From snapshot rows |
| `financial_metric_name = "Brent Crude"` | Oil price as global pain measure | From `oil-prices.json` rows |
| `event_description` containing "poll" / "protest" / "oppose" / "No Kings" | Domestic political pressure | Text search |
| `event_description` containing "Kaine" / "AUMF" / "war powers" / "Johnson" / "supplemental" | US legislative constraints | Text search |
| `event_type = "daily_briefing"` | Daily narrative evolution | 30 rows — track negotiation language over time |

## Proposed Analyses

### Analysis 1: Pain Curve Construction
Construct daily pain indices for both sides. US pain: cumulative war cost + oil price increase + domestic opposition indicators. Iranian pain: cumulative strikes + casualties + infrastructure destruction + economic isolation (tanker transits near zero). Plot both curves. Zartman predicts ceasefire ripeness where curves cross or converge. Test whether Day 26 (15-point plan rejection) corresponds to a point where one side's pain curve was still below threshold.

### Analysis 2: Information Revelation Through Retaliation Tempo
Iran's daily retaliation count is a signal of remaining military capability — observable to both sides but with noise. Construct the retaliation time series and fit a depletion model. If Iran's retaliation rate is declining (consistent with the "missile stock depletion" mentioned in Day 29 data), this represents gradual revelation of private information. Fearon's model predicts that settlement becomes more likely as private information is revealed. Test whether diplomatic event frequency increases as the information asymmetry narrows.

### Analysis 3: Credibility of Commitment Analysis
Track Trump's ultimatum deadlines as a time series: Day 23 (48-hour ultimatum), Day 24 (postponed 5 days), Day 28 (extended 10 days to Apr 6). Each extension reduces commitment credibility. Code each diplomatic event for escalatory vs. de-escalatory content. Test whether Iran's negotiating position (from rejection to counterproposal submission) shifts in response to perceived US commitment erosion.

### Analysis 4: Mediator Typology
Classify the four mediator states (Pakistan, Oman, Turkey, Egypt) by Touval & Zartman's (1985) mediator typology: leverage, impartiality, and acceptability to both sides. The dataset captures each mediator's activity timeline. Pakistan emerged as lead mediator (Islamabad summit); Oman served as initial back-channel; Turkey provided political cover; Egypt added regional legitimacy. Compare observed mediator behavior against theoretical predictions for each type.

## Key References

- Fearon, J. D. (1995). Rationalist explanations for war. *International Organization*, 49(3), 379-414.
- Powell, R. (2006). War as a commitment problem. *International Organization*, 60(1), 169-203.
- Putnam, R. D. (1988). Diplomacy and domestic politics: The logic of two-level games. *International Organization*, 42(3), 427-460.
- Touval, S., & Zartman, I. W. (1985). *International Mediation in Theory and Practice*. Westview Press.
- Zartman, I. W. (2000). Ripeness: The hurting stalemate and beyond. In P. Stern & D. Druckman (Eds.), *International Conflict Resolution After the Cold War*. National Academies Press.
