# Paper Seed: Alliance Fragmentation Under Stress — Coalition Behavior and Burden-Sharing in the 2026 Gulf War

## Field
International Relations / Alliance Theory

## Target Journals
- *International Organization*
- *European Journal of International Relations*
- *Security Studies*
- *International Affairs*

## Theoretical Framework

**Alliance Reliability Theory (Leeds, 2003; Berkemeier & Fuhrmann, 2018)**

Leeds' research on alliance treaty reliability shows that formal allies honor commitments approximately 75% of the time. However, reliability drops sharply in offensive wars lacking UN authorization. The 2026 conflict tests this: the US launched offensive strikes without AUMF (failed 47-53 in the Senate), and key allies (France, UK, Gulf states) faced domestic pressure to distance. The dataset captures the G7 fracture (Day 28, no communiqué), French/Italian independent diplomacy (Day 15), and varying Gulf state cooperation levels.

**Burden-Sharing Theory (Olson & Zeckhauser, 1966; Sandler & Hartley, 1999)**

The exploitation hypothesis predicts that in alliances, large states bear disproportionate costs while small states free-ride. The dataset enables direct measurement: US strike share vs. Israeli strike share, coalition naval contributions (UK 2 ships, France 1 carrier, vs. US 13+ assets), and Gulf state defensive contributions (intercepting missiles at their own bases vs. offensive participation).

**Institutional Binding Theory (Ikenberry, 2001)**

Ikenberry argues that institutions constrain hegemonic behavior by raising the costs of unilateral action. The dataset captures multiple institutional friction points: UNSC ceasefire negotiations (Bahrain Chapter VII draft, French alternative), IAEA demands for nuclear strike restraint, IMO emergency sessions on seafarer safety, and WHO condemnations. These represent institutional resistance to the US campaign.

## Research Questions

1. How is the offensive burden distributed between US, Israeli, and other coalition actors over the 30-day period?
2. Does the alliance fracture along predictable lines (offensive contributors vs. defensive-only vs. diplomatic dissenters)?
3. Do institutional pressure events (UNSC votes, IAEA statements, G7 summits) correlate with changes in strike patterns or diplomatic concessions?
4. How do Gulf host-nation states balance between hosting US forces and responding to domestic/Iranian pressure?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `actor_initiating` on STRIKE events | Burden distribution: US vs. Israel vs. joint | Group by actor, count per day |
| `actor_initiating` on NAVAL events | Coalition naval contributions by country | Filter from `carriers.json` rows |
| `country` on RETALIATION events | Which host nations are absorbing retaliation | Group by country |
| `event_domain = "DIPLOMATIC"` | Institutional pressure events | Filter all 66 diplomatic rows |
| `event_description` containing "G7" / "UNSC" / "IAEA" / "IMO" / "WHO" / "NATO" | International organization actions | Text search |
| `event_description` containing "France" / "UK" / "Germany" / "Japan" / "Korea" | Allied state behavior | Text search |
| `event_description` containing "Kuwait" / "Qatar" / "UAE" / "Bahrain" / "Saudi" | Gulf state behavior | Text search on diplomatic events |
| `day_of_conflict` | Temporal evolution of alliance cohesion | All rows, group by day |
| `event_type = "daily_briefing"` | Daily headline narrative — track alliance language | 30 briefing rows |
| `military_asset` | Naval asset nationality | From carriers.json rows — UK, France, US |

## Key References

- Ikenberry, G. J. (2001). *After Victory: Institutions, Strategic Restraint, and the Rebuilding of Order After Major Wars*. Princeton University Press.
- Leeds, B. A. (2003). Do alliances deter aggression? The influence of military alliances on the initiation of militarized interstate disputes. *American Journal of Political Science*, 47(3), 427-439.
- Olson, M., & Zeckhauser, R. (1966). An economic theory of alliances. *Review of Economics and Statistics*, 48(3), 266-279.
- Sandler, T., & Hartley, K. (1999). *The Political Economy of NATO*. Cambridge University Press.
