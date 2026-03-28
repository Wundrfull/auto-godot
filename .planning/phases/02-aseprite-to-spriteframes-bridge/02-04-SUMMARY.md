---
phase: 02-aseprite-to-spriteframes-bridge
plan: 04
subsystem: sprite
tags: [validation, spriteframes, tres, gdscript, headless-godot]

requires:
  - phase: 02-aseprite-to-spriteframes-bridge
    provides: "tres parser (parse_tres_file), GodotBackend, error hierarchy, output helpers"
provides:
  - "validate_spriteframes() for structural .tres validation"
  - "validate_spriteframes_headless() for Godot-confirmed validation"
  - "CLI sprite validate subcommand with --godot and --json flags"
affects: [e2e-testing, phase-03, phase-04]

tech-stack:
  added: []
  patterns:
    - "Separation of fatal issues vs non-fatal warnings in validation results"
    - "GDScript generation and output parsing for headless Godot integration"
    - "Graceful fallback from headless to structural validation on missing binary"

key-files:
  created:
    - src/gdauto/sprite/validator.py
  modified:
    - src/gdauto/commands/sprite.py
    - src/gdauto/formats/values.py
    - tests/unit/test_sprite_validate.py

key-decisions:
  - "Separated fatal issues from non-fatal warnings (load_steps mismatch) so valid=True when only warnings exist"
  - "Fixed _split_args and _find_colon in values.py to respect nested braces/brackets for correct dict-in-array parsing"

patterns-established:
  - "Validation result dict shape: {valid, animations, issues, warnings, ext_resource_count, sub_resource_count}"
  - "Headless validation via temp GDScript with VALIDATION_OK/VALIDATION_FAIL protocol"

requirements-completed: [SPRT-10]

duration: 10min
completed: 2026-03-28
---

# Phase 02 Plan 04: SpriteFrames Validation Summary

**Structural and headless SpriteFrames .tres validator with CLI command, catching broken references, wrong types, and missing animations**

## Performance

- **Duration:** 10 min
- **Started:** 2026-03-28T06:37:12Z
- **Completed:** 2026-03-28T06:47:16Z
- **Tasks:** 1 (TDD: test + feat commits)
- **Files modified:** 4

## Accomplishments
- Structural validation checks resource type, animations property, frame SubResource refs, atlas ExtResource refs, and load_steps
- Headless validation generates GDScript, runs in Godot, parses VALIDATION_OK/VALIDATION_FAIL output, falls back gracefully
- CLI `gdauto sprite validate` exits 0/1 based on validity, supports --json and --godot flags
- Fixed parser bug in values.py where nested dicts/arrays within arrays were incorrectly split on commas
- All 439 tests pass including 14 new validation tests

## Task Commits

Each task was committed atomically (TDD: RED then GREEN):

1. **Task 1 (RED): Failing tests for validation** - `f3bfda4` (test)
2. **Task 1 (GREEN): Validator module, CLI command, parser fix** - `73f84d0` (feat)

_TDD task with RED and GREEN commits._

## Files Created/Modified
- `src/gdauto/sprite/validator.py` - Structural and headless SpriteFrames validation
- `src/gdauto/commands/sprite.py` - Added validate subcommand to sprite group
- `src/gdauto/formats/values.py` - Fixed _split_args and _find_colon for nested brace/bracket support
- `tests/unit/test_sprite_validate.py` - 14 tests: structural, headless, CLI

## Decisions Made
- Separated validation issues (fatal, affect valid flag) from warnings (non-fatal, like load_steps mismatch) to avoid false negatives on files that Godot would accept
- Fixed parser's _split_args to track `([{` as openers and `)]}` as closers (was only tracking parens), enabling correct parsing of Godot's dict-in-array syntax used by SpriteFrames animations property

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Fixed _split_args in values.py to handle nested braces/brackets**
- **Found during:** Task 1 (GREEN phase, validator implementation)
- **Issue:** The `_split_args` function in values.py only tracked parentheses `()` for nesting depth, not braces `{}` or brackets `[]`. This caused complex values like `[{"frames": [...], "loop": true}]` to be incorrectly split on commas inside the dicts, producing unparseable fragments instead of parsed dict objects.
- **Fix:** Updated `_split_args` and `_find_colon` to track all three delimiter pairs `([{` / `)]}` for nesting depth.
- **Files modified:** src/gdauto/formats/values.py
- **Verification:** All 439 tests pass (no regressions); sample.tres now parses correctly with animations as list of dicts
- **Committed in:** 73f84d0 (part of GREEN commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Parser fix was essential for the validator to parse .tres animation data. No scope creep; the fix is minimal and targeted.

## Issues Encountered
- The sample.tres fixture has load_steps=3 but the formula yields 4 (1 ext + 2 sub + 1 resource = 4). Resolved by treating load_steps mismatch as a non-fatal warning rather than an error, since Godot itself is lenient about this value.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- All 4 sprite subcommands complete: import-aseprite, split, create-atlas, validate
- Phase 02 (Aseprite-to-SpriteFrames bridge) is now fully implemented
- Parser improvement (nested delimiter support) benefits all future commands that parse complex .tres values

## Known Stubs

None - all functions are fully implemented with no placeholder logic.

## Self-Check: PASSED

- FOUND: src/gdauto/sprite/validator.py
- FOUND: src/gdauto/commands/sprite.py
- FOUND: tests/unit/test_sprite_validate.py
- FOUND: .planning/phases/02-aseprite-to-spriteframes-bridge/02-04-SUMMARY.md
- FOUND: commit f3bfda4 (test)
- FOUND: commit 73f84d0 (feat)

---
*Phase: 02-aseprite-to-spriteframes-bridge*
*Completed: 2026-03-28*
