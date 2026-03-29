---
phase: 04-scene-commands-test-suite-and-agent-discoverability
plan: 03
subsystem: testing
tags: [e2e, golden-files, headless-godot, terrain-validation]
dependency_graph:
  requires: [04-01, 04-02]
  provides: [e2e-test-suite, golden-file-validation, peering-bit-tests]
  affects: [tests/e2e/, tests/fixtures/golden/, tests/unit/test_golden_files.py]
tech_stack:
  added: []
  patterns: [requires_godot-marker-skip, golden-file-normalization, gdscript-validation-scripts]
key_files:
  created:
    - tests/e2e/__init__.py
    - tests/e2e/conftest.py
    - tests/e2e/test_e2e_spriteframes.py
    - tests/e2e/test_e2e_tileset.py
    - tests/e2e/test_e2e_scene.py
    - tests/fixtures/golden/spriteframes_simple.tres
    - tests/fixtures/golden/tileset_basic.tres
    - tests/fixtures/golden/scene_basic.tscn
    - tests/unit/test_golden_files.py
  modified: []
decisions:
  - "Extended normalization to cover ExtResource() and SubResource() value references, not just id= attributes"
  - "Golden files committed with all randomized IDs normalized to deterministic placeholders"
metrics:
  duration: 6min
  completed: 2026-03-29
---

# Phase 04 Plan 03: E2E Test Suite and Golden File Validation Summary

E2E test infrastructure with headless Godot validation for SpriteFrames, TileSet (including blob-47 terrain), and scenes; golden file comparison tests with UID/resource ID normalization for output stability verification.

## What Was Built

### Task 1: E2E Test Infrastructure (7a8a1fb)

Created the `tests/e2e/` directory with pytest infrastructure for headless Godot validation:

- **conftest.py**: `pytest_collection_modifyitems` hook that auto-skips tests marked `@pytest.mark.requires_godot` when Godot binary is not on PATH. Provides `godot_backend` fixture returning a `GodotBackend` instance.
- **test_e2e_spriteframes.py**: Parses aseprite_simple.json fixture, builds SpriteFrames via `build_spriteframes()`, serializes to .tres, creates GDScript that loads and validates the resource in headless Godot, checks for VALIDATION_OK output.
- **test_e2e_tileset.py**: Two tests: basic TileSet loads in Godot; TileSet with blob-47 terrain applied loads and validates terrain_sets count and mode.
- **test_e2e_scene.py**: Builds scene from JSON definition via `build_scene()`, serializes to .tscn, validates in headless Godot that the PackedScene loads, instantiates, and root type matches.

All E2E tests follow the generate-write-validate pattern with GDScript using structured VALIDATION_OK/VALIDATION_FAIL output.

### Task 2: Golden File References and Comparison Tests (86c9ff6)

Created golden reference files and comparison test suite:

- **tests/fixtures/golden/spriteframes_simple.tres**: Known-good SpriteFrames output from aseprite_simple.json (4 frames, idle animation, 10 FPS).
- **tests/fixtures/golden/tileset_basic.tres**: Known-good TileSet with 16x16 tiles and TileSetAtlasSource.
- **tests/fixtures/golden/scene_basic.tscn**: Known-good scene with Node2D root and Sprite2D child.
- **tests/unit/test_golden_files.py**: 11 tests total:
  - 3 golden comparison tests (SpriteFrames, TileSet, scene)
  - 6 normalization unit tests (uid patterns, resource IDs, ExtResource/SubResource refs, non-uid preservation)
  - 2 peering bit validation tests (blob-47: 47 tiles x 8 bits = 376 peering lines; minimal-16: 16 tiles x 4 side bits = 64 side bit lines)

The `normalize_for_comparison()` function handles 5 pattern types: uid= attributes, standalone uid://, id= attributes, ExtResource() value references, and SubResource() value references.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] Extended normalization for value references**
- **Found during:** Task 2
- **Issue:** The plan's normalization only covered `uid="uid://xxx"` and `id="Type_xxxxx"` patterns. Generated .tres files also contain `ExtResource("Type_xxxxx")` and `SubResource("Type_xxxxx")` inside property values, which would cause golden file mismatches.
- **Fix:** Added `_EXT_REF_PATTERN` and `_SUB_REF_PATTERN` regexes to `normalize_for_comparison()`.
- **Files modified:** tests/unit/test_golden_files.py
- **Commit:** 86c9ff6

## Test Results

- 4 E2E tests collected (all skip gracefully when Godot is absent)
- 11 golden file tests passing
- 648 total tests pass, 4 skipped (E2E requiring Godot), 0 failures

## Known Stubs

None. All tests are fully implemented and connected to real builders.

## Self-Check: PASSED

- All 9 created files exist on disk
- Commit 7a8a1fb found (Task 1: E2E test infrastructure)
- Commit 86c9ff6 found (Task 2: Golden file tests)
