---
phase: 03-tileset-automation-and-export-pipeline
plan: 02
subsystem: tileset
tags: [tileset, terrain, peering-bits, physics, collision, blob-47, rpgmaker, cli]

requires:
  - phase: 01-foundation-and-cli-infrastructure
    provides: "Custom .tres parser/serializer, value type dataclasses, CLI skeleton, error handling"
  - phase: 03-tileset-automation-and-export-pipeline
    provides: "TileSet GdResource builder, PackedVector2Array, tileset create/inspect CLI commands"
provides:
  - "Terrain peering bit lookup tables (blob-47, minimal-16, RPG Maker)"
  - "apply_terrain_to_atlas() for assigning peering bits to TileSetAtlasSource"
  - "add_terrain_set_to_resource() for terrain set declaration in resource properties"
  - "Physics collision shape assignment (full-tile rectangles)"
  - "tileset auto-terrain CLI command with --layout flag"
  - "tileset assign-physics CLI command with --physics range:shape syntax"
affects: [03-04, 04-01]

tech-stack:
  added: []
  patterns: ["Algorithmic layout generation from bitmask enumeration with constraint validation", "Range-based physics rule parsing with validated shape types"]

key-files:
  created:
    - src/gdauto/tileset/terrain.py
    - src/gdauto/tileset/physics.py
    - tests/unit/test_tileset_terrain.py
    - tests/unit/test_tileset_physics.py
  modified:
    - src/gdauto/commands/tileset.py

key-decisions:
  - "Algorithmic blob-47 generation over hand-coded lookup table: enumerate all 256 bitmask combinations and filter by corner constraint (corner set only if both adjacent sides set), producing exactly 47 valid patterns"
  - "RPG Maker layout uses density-sorted ordering (descending popcount, then descending value) with one duplicate full-terrain tile to fill 48 positions"
  - "Physics rules use rsplit(':',1) parsing to handle potential edge cases in range format"

patterns-established:
  - "Bitmask-to-peering-bit pattern: generate valid tile patterns algorithmically rather than hand-coding, then validate via constraint assertions"
  - "Terrain mode mapping: layout name string maps to Godot TerrainMode integer via TERRAIN_MODES dict"

requirements-completed: [TILE-02, TILE-03, TILE-04, TILE-05]

duration: 6min
completed: 2026-03-28
---

# Phase 3 Plan 2: Terrain Auto-Assignment and Physics Collision Summary

**Algorithmic peering bit generation for blob-47/minimal-16/RPG Maker layouts with range-based physics collision assignment, 59 unit tests**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-28T21:31:27Z
- **Completed:** 2026-03-28T21:37:58Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Blob-47 layout generated algorithmically (47 valid 8-bit patterns from 256 combinations, filtered by corner adjacency constraint)
- Minimal-16 layout covers all 16 combinations of 4 side bits in a 4x4 grid
- RPG Maker layout produces 48 tiles (47 unique + 1 duplicate) in density-sorted 2-column arrangement
- Physics module parses range:shape rules and applies PackedVector2Array collision rectangles
- Both CLI commands integrated with existing tileset group, following established error handling and output patterns
- 59 unit tests covering layout table structure, constraint validation, function behavior, and CLI integration

## Task Commits

Each task was committed atomically:

1. **Task 1: Terrain peering bit lookup tables and apply_terrain_to_atlas (TDD)** - `daf0689` (feat)
2. **Task 2: Physics assignment module and auto-terrain/assign-physics CLI commands** - `7255319` (feat)

## Files Created/Modified
- `src/gdauto/tileset/terrain.py` - Peering bit lookup tables (BLOB_47_LAYOUT, MINIMAL_16_LAYOUT, RPGMAKER_LAYOUT), apply_terrain_to_atlas(), add_terrain_set_to_resource()
- `src/gdauto/tileset/physics.py` - parse_physics_rule(), apply_physics_to_atlas() with full-tile collision shapes
- `src/gdauto/commands/tileset.py` - Added auto-terrain (--layout required, click.Choice) and assign-physics (--physics multiple, --columns) subcommands
- `tests/unit/test_tileset_terrain.py` - 33 tests for layout tables, constants, apply functions, terrain set declaration
- `tests/unit/test_tileset_physics.py` - 26 tests for physics parsing, application, CLI auto-terrain, CLI assign-physics, help output

## Decisions Made
- Algorithmic blob-47 generation: enumerate all 256 bitmask values, apply corner adjacency constraint (corner requires both adjacent sides), producing exactly 47 valid patterns. This is provably correct versus hand-coding.
- RPG Maker layout uses density-sorted ordering (most terrain neighbors first) with one duplicate full-terrain tile at position 47 to fill the standard 48-tile A2 autotile grid.
- Physics rule parsing uses rsplit(':', 1) to safely handle the format and validates shape types against an explicit allowlist (full, none per D-04).

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Known Stubs
None - all data pipelines are fully wired.

## Next Phase Readiness
- Terrain and physics commands are complete, ready for Tiled import (03-04) or E2E validation
- The tileset command group now has create, inspect, auto-terrain, and assign-physics subcommands
- Generated .tres files contain proper terrain_set declarations, peering bits, and physics layers

## Self-Check: PASSED

All 5 created/modified files verified present. Both task commits (daf0689, 7255319) verified in git log.

---
*Phase: 03-tileset-automation-and-export-pipeline*
*Completed: 2026-03-28*
