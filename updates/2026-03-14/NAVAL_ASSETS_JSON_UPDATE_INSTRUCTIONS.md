# Naval Assets JSON — Audit & Update Instructions

**Context:** This JSON describes U.S. naval asset positions and metadata for a speculative fiction scenario ("Operation Epic Fury") set in March 2026. The scenario must be grounded in real-world plausibility. This document provides exact changes a coding agent should make.

---

## CRITICAL: Three Decommissioned Cruisers

All three Ticonderoga-class cruisers in the current JSON were decommissioned before the scenario date and must be replaced. As of early 2026, only three Ticos remain active: **USS Gettysburg (CG-64)**, **USS Chosin (CG-65)**, and **USS Cape St. George (CG-71)** — all received service life extensions to ~2029.

### Change 1 — CVN-72 Lincoln (CSG-3) Escorts

**Remove:** `"CG-52 USS Bunker Hill"` (decommissioned Sept 22, 2023)

**Replace with:** `"CG-65 USS Chosin"`

**Rationale:** Chosin completed modernization in FY2024, is active and San Diego–homeported — the natural Pacific Fleet cruiser for CSG-3.

### Change 2 — CVN-78 Ford (CSG-12) Escorts

**Remove:** `"CG-68 USS Anzio"` (decommissioned Sept 22, 2022)

**Replace with:** `"CG-64 USS Gettysburg"`

**Rationale:** Gettysburg completed modernization in FY2023, is Norfolk-homeported, and has recent real-world CSG deployment history (Truman CSG / Operation Prosperity Guardian). Natural Norfolk-based cruiser for the Ford.

### Change 3 — CVN-77 Bush (CSG-10) Escorts

**Remove:** `"CG-56 USS San Jacinto"` (decommissioned Sept 15, 2023)

**Replace with:** `"CG-71 USS Cape St. George"`

**Rationale:** Cape St. George is the youngest Tico (commissioned 1993), completed modernization and homeport shift to San Diego in FY2025. Third and final active cruiser.

---

## Schema Normalization Changes

### Change 4 — Submarine Aircraft Field

**Target object:** `id: "ssgn-728"` (USS Florida)

**Change:** `"aircraft": "N/A"` → `"aircraft": null`

**Rationale:** `"N/A"` as a string requires special-casing in rendering/filtering logic. `null` is semantically correct and programmatically clean.

### Change 5 — Add `operation_start_date` Field

**Add to every object in the array:**

```json
"operation_start_date": "2026-03-01"
```

**Rationale:** The `notes` fields reference "Day 14" without an anchor date. This field makes the day count resolvable. Place it after `deployed_since` for logical grouping. Adjust the date if the intended Day 0 differs from March 1 — the key requirement is that the field exists.

### Change 6 — Split `status` Into Enum + Free Text

**Rename** the current `status` field to `mission_summary`.

**Add a new `status` field** with one of three enum values: `"ENGAGED"`, `"DEPLOYED"`, `"STANDBY"`.

Mapping for each asset:

| id | new `status` | `mission_summary` (current `status` value) |
|---|---|---|
| cvn-72 | `"ENGAGED"` | `"Convoy escort and retaliatory strike operations"` |
| cvn-78 | `"ENGAGED"` | `"Supporting IDF Lebanon ground operation and Iran strikes"` |
| cvn-77 | `"ENGAGED"` | `"Convoy screen and southern interdiction"` |
| lha-6 | `"STANDBY"` | `"Mine countermeasures support, TRAP"` |
| ddg-117 | `"ENGAGED"` | `"Hormuz patrol, MCM escort"` |
| ssgn-728 | `"DEPLOYED"` | `"Tomahawk strike platform"` |
| ddg-113 | `"ENGAGED"` | `"Houthi threat interdiction"` |

**Rationale:** The original `status` field mixed operational state with mission description. Splitting enables programmatic filtering by readiness state while preserving descriptive context.

### Change 7 — Normalize `strike_group` for DDG-113

**Target object:** `id: "ddg-113"` (USS John Finn)

**Change:** `"strike_group": "CSG-3 detached — Red Sea"` →  `"strike_group": "CSG-3 (detached)"`

**Add field:** `"detachment_note": "Detached to Red Sea for Houthi missile defense and merchant shipping escort"`

**Rationale:** Embedding operational context in an organizational field breaks programmatic grouping. The new field preserves the information without polluting the strike group identifier.

---

## Geospatial Note (No Change Required, Confirm Intent)

`LHA-6` (USS America) at `26.05, 57.00` and `DDG-117` (USS Paul Ignatius) at `26.10, 57.10` are co-located within ~10km. This is plausible if both are escorting the same convoy through the Strait of Hormuz, but the agent should confirm this is intentional and not a copy-paste artifact. **If unintentional**, offset Paul Ignatius slightly east (e.g., `26.15, 57.30`) to position her at the strait's eastern approach.

---

## Summary Checklist

- [ ] Replace `CG-52 USS Bunker Hill` → `CG-65 USS Chosin` in cvn-72 escorts
- [ ] Replace `CG-68 USS Anzio` → `CG-64 USS Gettysburg` in cvn-78 escorts
- [ ] Replace `CG-56 USS San Jacinto` → `CG-71 USS Cape St. George` in cvn-77 escorts
- [ ] Change submarine `aircraft` from `"N/A"` to `null`
- [ ] Add `operation_start_date` field to all objects
- [ ] Split `status` into enum `status` + `mission_summary`
- [ ] Normalize `strike_group` on DDG-113 and add `detachment_note`
- [ ] Verify LHA-6 / DDG-117 co-location is intentional
