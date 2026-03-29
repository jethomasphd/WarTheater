# Paper Seed: Competing Narratives Under Fire — Source Attribution, Information Asymmetry, and Narrative Control in the First Month of the Iran War

## Field
Media Studies / Communication / Information Warfare

## Target Journals
- *Political Communication*
- *Journal of Communication*
- *Media, War & Conflict*
- *Digital Journalism*

## Theoretical Framework

**Framing Theory (Entman, 1993; Reese, 2001)**

Entman's cascading activation model describes how conflict frames flow from administration to media to public. Frames define problems, diagnose causes, make moral judgments, and suggest remedies. The dataset captures 293 timeline events, each with source attribution (`timeline_source`) and narrative framing (`event_description`). Systematic analysis can reveal which actors' frames dominate at different conflict phases, how framing shifts from "decisive action" (Day 1) to "humanitarian crisis" (Day 11+) to "negotiation" (Day 24+).

**Manufacturing Consent and the Propaganda Model (Herman & Chomsky, 1988)**

The propaganda model predicts that official sources dominate early coverage, with critical frames emerging only as elite consensus fractures. The dataset's `timeline_source` field tracks source attribution: DoD/White House dominate early events, while humanitarian organizations (Red Crescent, WHO), international bodies (IAEA, IMO), and independent investigators (Bellingcat, BBC Verify) gain prominence as the conflict progresses. The Minab school incident represents a critical inflection — Pentagon preliminary investigation acknowledged US responsibility, breaking the official frame.

**Strategic Narrative Theory (Miskimmon, Leira, & O'Loughlin, 2017)**

Strategic narrative theory examines how states project coherent narratives of identity, system, and policy. The US narrative ("preventing nuclear Iran"), Iran's counter-narrative (victimhood, resistance), and third-party narratives (humanitarian concern, economic disruption) compete for international legitimacy. The dataset's 66 diplomatic events and 30 daily briefing headlines capture this narrative competition at daily resolution.

## Research Questions

1. How does source attribution in the timeline events shift over the 30-day period — do official military sources dominate early and yield to humanitarian/international sources later?
2. Can distinct framing phases be identified (security frame → humanitarian frame → negotiation frame) and dated?
3. Does the Minab school incident function as a "frame break" event that disrupts the dominant narrative?
4. How do the daily briefing headlines reflect narrative competition between military progress and humanitarian cost?

## Dataset Variables — Direct Mapping

| Variable | Use | Filter/Operation |
|----------|-----|-----------------|
| `timeline_source` | Source attribution for 293 events | From timeline rows — classify as official-military, official-diplomatic, humanitarian-NGO, media, independent-investigative |
| `event_domain` | Domain distribution over time | Track which domains dominate each week |
| `event_description` | Framing analysis — keyword extraction | Full text of all 1,653 rows |
| `event_type = "daily_briefing"` + `event_description` | Daily headline framing | 30 briefing rows — code for dominant frame |
| `day_of_conflict` | Temporal dimension for frame shift analysis | All rows |
| `event_description` containing "Minab" / "school" / "children" / "civilian" / "war crime" | Humanitarian frame events | Text search |
| `event_description` containing "target" / "degraded" / "destroyed" / "eliminated" / "neutralized" | Military progress frame events | Text search |
| `event_description` containing "ceasefire" / "negotiate" / "talks" / "peace" / "diplomacy" | Negotiation frame events | Text search |
| `data_confidence` | Confidence as proxy for information quality | All rows |

## Key References

- Entman, R. M. (1993). Framing: Toward clarification of a fractured paradigm. *Journal of Communication*, 43(4), 51-58.
- Herman, E. S., & Chomsky, N. (1988). *Manufacturing Consent*. Pantheon.
- Miskimmon, A., O'Loughlin, B., & Roselle, L. (2017). *Forging the World: Strategic Narratives and International Relations*. University of Michigan Press.
