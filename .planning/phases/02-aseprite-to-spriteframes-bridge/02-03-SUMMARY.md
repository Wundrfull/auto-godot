---
phase: 02-aseprite-to-spriteframes-bridge
plan: 03
subsystem: sprite
tags: [sprite-split, atlas-creation, shelf-packing, pillow, spriteframes]

# Dependency graph
requires:
  - phase: 02-aseprite-to-spriteframes-bridge
    plan: 01
    provides: GdResource/ExtResource/SubResource dataclasses, serialize_tres_file, Rect2/StringName/ExtResourceRef/SubResourceRef value types, generate_uid/uid_to_text/generate_resource_id
provides:
  - Sprite sheet splitter (split_sheet_grid, split_sheet_json) for grid-based and JSON-defined frame extraction
  - Atlas creator (create_atlas, next_power_of_two) with shelf-packing compositor
  - CLI commands sprite split and sprite create-atlas
affects: [02-04, sprite-cli]

# Tech tracking
tech-stack:
  added: [Pillow (optional, for image dimension reading and atlas compositing)]
  patterns: [pillow-import-guard, shelf-packing-algorithm, mock-image-testing]

key-files:
  created:
    - src/gdauto/sprite/splitter.py
    - src/gdauto/sprite/atlas.py
    - tests/unit/test_sprite_split.py
    - tests/unit/test_sprite_atlas.py
  modified:
    - src/gdauto/commands/sprite.py

key-decisions:
  - "Pillow import guard pattern: try/except at module level with _require_pillow() function and PILLOW_NOT_INSTALLED error code"
  - "Shelf packing uses sqrt(total_area)*1.5 as initial width estimate, tallest-first sorting"
  - "Grid splitter only reads image dimensions (no pixel manipulation), closes image immediately"
  - "All tests mock PIL.Image to avoid requiring Pillow in test environment"

patterns-established:
  - "Optional dependency guard: try/except import + _require_pillow() + GdautoError with install instructions"
  - "Shelf packing: sort by height descending, fill left-to-right, new shelf when row full"
  - "CLI dispatch: thin command functions that delegate to library modules via lazy imports"

requirements-completed: [SPRT-08, SPRT-09]

# Metrics
duration: 7min
completed: 2026-03-28
---

# Phase 02 Plan 03: Sprite Sheet Splitting and Atlas Creation Summary

**Grid-based and JSON-defined sprite sheet splitter plus shelf-packing atlas compositor, both with Pillow import guards and CLI subcommands**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-28T06:24:44Z
- **Completed:** 2026-03-28T06:31:53Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Sprite sheet splitter handles grid-based splitting (WxH frame size) and JSON-defined regions
- Grid splitter validates frame size against image dimensions and warns on non-divisible sizes
- Atlas creator uses shelf packing (tallest-first, left-to-right) with power-of-two rounding by default
- Both modules use Pillow import guards that produce actionable GdautoError with install instructions
- CLI sprite split accepts --frame-size, --json-meta, --output, --res-path, --fps options
- CLI sprite create-atlas accepts multiple image files, -o, --tres-output, --res-path, --no-pot options
- 31 new tests (13 split + 18 atlas) all passing; 406 total suite tests pass with zero regressions

## Task Commits

Each task was committed atomically (TDD: red then green):

1. **Task 1: Sprite sheet splitter module and CLI command**
   - `32a23d3` (test: failing tests for splitting)
   - `c6185cb` (feat: splitter implementation + split CLI command)
2. **Task 2: Atlas creator module and CLI command**
   - `d0b051f` (test: failing tests for atlas creation)
   - `1d3629f` (feat: atlas implementation + create-atlas CLI command)

## Files Created/Modified
- `src/gdauto/sprite/splitter.py` - Grid-based and JSON-defined sprite sheet splitting with Pillow guard
- `src/gdauto/sprite/atlas.py` - Shelf-packing atlas compositor with next_power_of_two utility
- `src/gdauto/commands/sprite.py` - Added split and create-atlas subcommands with option parsing and error handling
- `tests/unit/test_sprite_split.py` - 13 tests (grid regions, validation, warnings, JSON, CLI, Pillow missing)
- `tests/unit/test_sprite_atlas.py` - 18 tests (POT utility, shelf packing, dimensions, non-overlap, CLI)

## Decisions Made
- Pillow import guard pattern: try/except at module level, _require_pillow() callable, GdautoError with code PILLOW_NOT_INSTALLED
- Shelf packing uses sqrt(total_area)*1.5 as initial shelf width estimate; sorts images tallest-first for better packing
- Grid splitter only reads image dimensions (width, height) then closes; no pixel manipulation needed
- All tests mock PIL.Image to avoid requiring Pillow as a test dependency
- split command returns non-zero exit when neither --frame-size nor --json-meta is provided (SPRITE_SPLIT_NO_SIZE)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required. Pillow is optional and only needed when running the actual commands (not for tests).

## Known Stubs

None - all data paths are fully wired.

## Next Phase Readiness
- sprite split and create-atlas commands are available for Plan 04 integration testing
- Both commands produce valid SpriteFrames GdResources via the same builder pattern as import-aseprite

## Self-Check: PASSED
