# Changelog — IranWar.ai Event-Level Research Dataset

All notable changes to the research dataset are documented here. Releases follow the
versioned, snapshotted cadence described in the manuscript (§2.1): the root files track
the latest release, and each `releases/vN/` directory is an immutable, reproducible
snapshot. Dataset versions are independent of the dashboard's daily update cadence.

---

## v1.2 — 2026-08-17 (data through Day 170, 2026-08-16)

**Summary.** Second scheduled extension. Rebuilds the dataset over the full Day 1–170
window (~70 additional days beyond v1.1). Source schemas were largely stable since Day 100:
the v1.1 classifiers already handle the great majority of the new records correctly. This
release adds four small, surgical refinements so that source values which first appeared
after Day 100 are coded correctly rather than dropped into fallback buckets. Relative to a
naive re-run of the v1.1 script on the Day-170 data, v1.2 changes exactly **30 cells**
(2 `event_type`, 1 `infrastructure_target_type`, 27 `strike_notes`); everything else is
byte-identical. v1.0 and v1.1 are preserved unchanged in `releases/`.

### Headline numbers
| | v1.1 | v1.2 |
|---|---|---|
| Rows | 3,587 | 4,612 |
| Columns | 52 | 52 |
| Coverage | Day 0–100 | Day 0–170 |
| Date range | 2026-01-02 → 2026-06-07 | 2026-01-02 → 2026-08-16 |
| event_type values | 44 | 46 |

### Source growth (records extracted)
timeline-events 937→1,050 · strikes-iran 735→902 · strikes-retaliation 421→480 ·
casualties 500→850 · markets 312→398 · war-costs 203→303 · oil-prices 178→275 ·
hero-stats 101→126 · briefings 94→107 · global-bases 15→25 · carriers 17→21 ·
infrastructure 7→8 · hormuz 34→34 · historical-comparison 5→5 · baselines 28→28.

### Row deltas by domain
FINANCIAL 879→1,178 (+299) · STRIKE 790→967 (+177) · HUMANITARIAN 561→915 (+354) ·
RETALIATION 551→622 (+71) · DIPLOMATIC 361→414 (+53) · OTHER 238→276 (+38) ·
MILITARY 123→152 (+29) · NAVAL 80→84 (+4) · CYBER 4→4 (+0).

### Added
- **No new columns** (schema stable at 52; v1.0/v1.1 column names and order preserved).
- **2 new `event_type` values** — `mine_countermeasures` and `unmanned_surface_vessel` —
  for two naval asset classes that entered `carriers.json` after Day 100. Added as explicit
  branches in `normalize_naval_type()` (the prior regex fallback already produced the same
  tokens, so this is a documentation/robustness change with no output delta).
- **New `infrastructure_target_type` value `water_infrastructure`** for the new
  `infrastructure.json` category "Water/Desalination Facilities Struck" (1 row that a naive
  re-run left as `other`). Parallels the existing `power_grid` / `oil_infrastructure` utility
  categories.

### Changed — classification (the substantive work)
- **Retaliation type `houthi_proxy_attack`** (new after Day 100: Houthi USV/missile strikes
  on Red Sea shipping, e.g. off Bab al-Mandeb and against a Saudi-aligned tanker) is now
  explicitly coded `RETALIATION` / `maritime_attack` (2 rows). Previously it fell to the
  token/weapon fallback, which returned `RETALIATION` / `missile_attack`; the domain was
  already correct, and this fixes the `event_type` to match the established
  `drone_strike_on_commercial_vessel` → `maritime_attack` convention.
- **`strikes-iran.json` `notes_addendum`** (new field after Day 100) is folded into
  `strike_notes`, alongside the existing `platform` / `outcome` handling, so no source text
  is discarded (Manuscript §3.1). Affects the 27 exploded rows of the `kharg-island` record
  (a Day-72 oil-spill addendum).
- **Codebook notes** refreshed: `day_of_conflict` now states "v1.2 covers Day 0-170";
  `strike_verified` now states "18 of 227 retaliation locations are unverified";
  `infrastructure_target_type` valid-values note lists `water_infrastructure`.
- **Codebook enumeration cap** raised (40 → 80) so every categorical's `valid_values` is
  listed in full — `event_type` now has 46 values and the codebook's own note promises the
  full list. Codebook-only change; the dataset CSV is byte-identical (same MD5).

### Not changed (verified stable)
- **Casualty factions** remain exactly 5 (iranian_military, iranian_civilian, us_military,
  lebanese, israeli_military) despite continued Houthi/Red Sea involvement. **Market sectors**
  remain 4 (handled dynamically regardless). **hero-stats** history carries no new fields.
- **Timeline categories** grew to 98 distinct values but all resolve correctly under the
  existing `classify_timeline()` + `TIMELINE_DOMAIN_KEYWORDS`. The residual `OTHER` bucket is
  38 rows: 35 intentional daily `summary` records + the 3 documented singletons
  (`aviation_civil`, `us_iran_direct`, `regional_disruption`), unchanged from v1.1.
- **As-of dating** is dynamic (`compute_as_of()`); cumulative/reference records
  (infrastructure, Hormuz summaries, historical comparison) date to Day 170 / 2026-08-16.

### Reproducibility
- The frozen `releases/v1.2/source_snapshot_2026-08-17_Day1-170.zip` regenerates the v1.2
  CSV and codebook **byte-for-byte** (verified; identical MD5). The daily snapshot in
  `snapshots/` was taken at a slightly different moment than extraction, so the frozen
  snapshot is built from the exact `public/data/` bytes used for the build.

### Notes for the next monthly maintainer
- New retaliation `type` / timeline `category` / infrastructure category / naval `type`
  values: extend `RET_TYPE_*`, `TIMELINE_DOMAIN_KEYWORDS`, `infra_type_map`, or
  `normalize_naval_type()` respectively (see `AGENT_PROTOCOL.md`).
- Watch `casualties.json` for new factions and `markets.json` for new sectors.
- `event_id` renumbers each build; it is not a stable cross-version key.

---

## v1.1 — 2026-06-09 (data through Day 100, 2026-06-07)

**Summary.** First scheduled extension after v1.0. Rebuilds the dataset over the full
Day 1–100 window (~70 additional days). The dashboard's source schemas drifted
substantially between Day 30 and Day 100; this release updates the extraction logic to
handle that drift correctly rather than re-running the v1.0 script naively (which would
have misclassified hundreds of events). v1.0 is preserved unchanged in `releases/v1.0/`.

### Headline numbers
| | v1.0 | v1.1 |
|---|---|---|
| Rows | 1,653 | 3,587 |
| Columns | 48 | 52 |
| Coverage | Day 0–30 | Day 0–100 |
| Date range | 2026-01-02 → 2026-03-29 | 2026-01-02 → 2026-06-07 |
| event_type values | ~36 | 44 |

### Source growth (records extracted)
timeline-events 293→937 · strikes-iran 620→735 · strikes-retaliation 237→421 ·
casualties 150→500 · markets 84→312 · war-costs 63→203 · oil-prices 60→178 ·
hero-stats 31→101 · briefings 30→94 · hormuz 20→34 · carriers 13→17 · global-bases 13→15 ·
historical-comparison 4→5 · baselines 28→28 · infrastructure 7→7.

### Added
- **4 columns** (appended; v1.0 columns keep their exact names and positions):
  - `timeline_category_raw` — verbatim source `category` for every timeline event.
  - `snapshot_nasdaq`, `snapshot_dow`, `snapshot_sp500_change_pct` — new fields that
    appeared in `hero-stats.json` history after Day 30 (Manuscript §3.1, no field discarded).
- **`weapon_system` now populated for `strikes-iran.json`** records that carry a `weapon`
  field (added to the source after Day 30); `platform` and `outcome` fields are folded
  into `strike_notes`. Previously `weapon_system` was NULL for all strike rows.
- **Validation block** in the build output: non-ISO date count, invalid-domain count,
  day_of_conflict↔date consistency, and a canonical sort-order check (all pass for v1.1).
- **Versioned release layout**: `releases/v1.0/` and `releases/v1.1/`, each with the frozen
  dataset, codebook, script, a source-data snapshot, and release notes. `CHANGELOG.md`.

### Changed — classification (the substantive work)
- **Timeline categories (9 → ~95).** Replaced the fixed 8-entry `CATEGORY_DOMAIN_MAP` with
  `classify_timeline()` + `TIMELINE_DOMAIN_KEYWORDS`, an ordered keyword classifier.
  Precedence (first match wins): explicit `retaliat*` token → CYBER → HUMANITARIAN → NAVAL →
  FINANCIAL → DIPLOMATIC → MILITARY; military events are then resolved to
  STRIKE/RETALIATION/MILITARY by description heuristics. Effect: ~200 timeline events that a
  naive re-run dropped into `OTHER` are now correctly domained. Selected mappings:
  `diplomacy/political/rhetoric/sanctions/congress/war_powers/attribution/*statement` →
  DIPLOMATIC · `markets/macro/cost/economic*/geoeconomic` → FINANCIAL ·
  `maritime/naval/hormuz/blockade/shipping/tanker` → NAVAL ·
  `casualties/collateral/environmental/health/displacement` → HUMANITARIAN ·
  `kinetic/force_posture/escalation/lebanon/intelligence/capability` → MILITARY (then split).
  Three singleton categories remain in OTHER (`aviation_civil`, `us_iran_direct`,
  `regional_disruption`); `timeline_category_raw` preserves all originals for re-coding.
- **Retaliation types (5 → ~32).** Added explicit `RET_TYPE_DOMAIN` / `RET_TYPE_EVENTTYPE`
  maps plus a token/weapon fallback. **Correctness fix:** Israeli/US offensive actions that
  now appear in this file (`idf_strike`, `israeli_strikes_lebanon`, `israel_kinetic_lebanon`,
  `israel_strike_lebanon`, `us_counter_action`) are classified `STRIKE`, not `RETALIATION`
  (12 rows). New buckets: Houthi/proxy attacks → RETALIATION (`drone_attack`/`proxy_attack`);
  maritime seizure/blockade/shipping incidents → NAVAL (`maritime_attack`); cross-border
  repression and ground-ops continuation → MILITARY. Initiating actor now taken from the
  source `actor`/`origin` fields where present.
- **Retaliation confidence** now also reads the new `confidence` / `verification_confidence`
  fields: `verified=false` or single-source/disputed → LOW; `verified=true` → HIGH;
  otherwise MEDIUM (was strictly verified→HIGH / else→LOW).
- **Naval (`carriers.json`) event_type normalized.** Free-text class strings
  (`Nimitz-class aircraft carrier`, `ballistic missile submarine`, `expeditionary sea base`,
  `pre_positioning`) are collapsed to a controlled vocabulary
  (carrier/submarine/destroyer/amphibious/littoral_combat_ship/support/air/ground).
- **As-of dating made dynamic.** Cumulative/reference records (infrastructure, Hormuz
  vessel-attack & alternative-route summaries, historical comparison) were hardcoded to
  `2026-03-29` / Day 30. They are now dated to the latest data day, computed from the data
  (`compute_as_of()` → Day 100 / 2026-06-07 for this release).

### Reproducibility
- The frozen `releases/v1.1/source_snapshot_2026-06-09_Day1-100.zip` regenerates the v1.1
  CSV **byte-for-byte** (verified).
- v1.0's exact source snapshot was identified as the `2026-03-30` database snapshot, which
  reproduces the 1,653-row v1.0 dataset exactly; it is stored in `releases/v1.0/`.

### Notes for the next monthly maintainer
- New timeline `category` or retaliation `type` values: extend `TIMELINE_DOMAIN_KEYWORDS`
  / the `RET_TYPE_*` maps (see `AGENT_PROTOCOL.md`).
- Watch `casualties.json` for new factions and `markets.json` for new sectors (markets are
  handled dynamically; factions are an explicit list).
- `event_id` renumbers each build; it is not a stable cross-version key.

---

## v1.0 — 2026-05 (data through Day 30, 2026-03-29)

Initial public release accompanying the preprint (2026-05-13). 1,653 rows × 48 columns,
Day 0–30. Frozen in `releases/v1.0/`. See `releases/v1.0/RELEASE_NOTES.md`.
