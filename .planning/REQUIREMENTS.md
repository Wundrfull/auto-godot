# Requirements: gdauto

**Defined:** 2026-03-27
**Core Value:** Aseprite-to-SpriteFrames bridge: read Aseprite's JSON export and generate valid Godot .tres SpriteFrames resources with named animations, correct frame durations, atlas texture regions, and loop settings, entirely in Python with no Godot binary required.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### CLI Foundation

- [ ] **CLI-01**: Click-based CLI entry point with command groups: project, export, sprite, tileset, scene, resource
- [ ] **CLI-02**: Every command supports `--json` flag that switches output from human-readable to structured JSON
- [ ] **CLI-03**: Every command has `--help` with descriptions that AI agents can parse for command discovery
- [ ] **CLI-04**: All errors produce non-zero exit codes
- [ ] **CLI-05**: With `--json`, errors produce `{"error": "message", "code": "ERROR_CODE"}` with actionable fix suggestions
- [ ] **CLI-06**: SKILL.md auto-generated from CLI command tree (names, arguments, options, help text)

### File Format Parser

- [ ] **FMT-01**: Custom state-machine parser for Godot 4.x .tscn files (format=3), handling bracket sections, nested structures, multi-line values
- [ ] **FMT-02**: Custom state-machine parser for Godot 4.x .tres files (format=3), handling sub_resources, ext_resources, and the resource section
- [ ] **FMT-03**: Godot value type serializer/deserializer covering Vector2, Vector2i, Vector3, Rect2, Color, Transform2D, StringName, arrays, dictionaries
- [ ] **FMT-04**: Resource ID generation matching Godot 4.x format (string-based alphanumeric IDs like `Type_xxxxx`)
- [ ] **FMT-05**: UID generation and .uid companion file support for Godot 4.4+
- [ ] **FMT-06**: Round-trip fidelity: parse a .tres/.tscn and re-serialize it without introducing spurious diffs
- [ ] **FMT-07**: `gdauto resource inspect` dumps any .tres or .tscn file as structured JSON

### Project Management

- [ ] **PROJ-01**: `gdauto project info` reads project.godot and outputs project name, Godot version, autoloads, input mappings, display settings as JSON
- [ ] **PROJ-02**: `gdauto project validate` checks project structure: verifies all `res://` paths resolve, detects missing resources, reports orphan scripts
- [ ] **PROJ-03**: `gdauto project validate` optionally runs Godot `--check-only` for script syntax validation when Godot binary is available
- [ ] **PROJ-04**: `gdauto project create` scaffolds new projects from built-in templates with project.godot, default scene, folder structure
- [ ] **PROJ-05**: Godot backend wrapper: discovers binary on PATH or via `--godot-path`, validates version >= 4.5, manages timeouts, parses stderr for structured error reporting

### Export Pipeline

- [ ] **EXPT-01**: `gdauto export release` exports using a named preset with structured error reporting
- [ ] **EXPT-02**: `gdauto export debug` exports a debug build using a named preset
- [ ] **EXPT-03**: `gdauto export pack` exports .pck files using a named preset
- [ ] **EXPT-04**: `gdauto import` forces re-import with retry logic (exponential backoff) to handle known Godot `--import` timing bugs, uses `--quit-after` instead of `--quit` to avoid race condition
- [ ] **EXPT-05**: Export commands auto-run import first if import cache is missing (handles "never opened in editor" gotcha)

### Sprite and Animation

- [ ] **SPRT-01**: `gdauto sprite import-aseprite` parses Aseprite JSON metadata (frame regions, durations, animation tags, slices)
- [ ] **SPRT-02**: Computes atlas texture regions (Rect2) from Aseprite frame x, y, w, h data
- [ ] **SPRT-03**: Converts Aseprite per-frame duration (milliseconds) to Godot animation speed (FPS), handling variable-duration frames via GCD-based base FPS with per-frame duration multipliers
- [ ] **SPRT-04**: Handles all four Aseprite animation directions: forward, reverse, ping-pong, ping-pong reverse
- [ ] **SPRT-05**: Handles loop settings from Aseprite repeat counts (0 = loop forever, N = play N times)
- [ ] **SPRT-06**: Handles trimmed sprites with spriteSourceSize offsets
- [ ] **SPRT-07**: Writes valid .tres SpriteFrames resource with named animations, AtlasTexture sub-resources, correct speed and loop settings
- [ ] **SPRT-08**: `gdauto sprite split` takes a sprite sheet image + optional JSON metadata and generates SpriteFrames (grid-based or JSON-defined regions)
- [ ] **SPRT-09**: `gdauto sprite create-atlas` batches multiple sprite images into a single atlas texture with companion metadata (bin-packing, power-of-two sizes)
- [ ] **SPRT-10**: Sprite validation pipeline: verifies generated SpriteFrames load in headless Godot, checks animation names exist, frame counts match, no broken texture references
- [ ] **SPRT-11**: Import guide documentation for users and AI agents: correct Aseprite export settings (grid size, pixel size, frame ordering, JSON format), common pitfalls, and recommended workflows
- [ ] **SPRT-12**: Researched common Aseprite-to-Godot import failures and built preventions into the tool (wrong frame order, mismatched dimensions, missing tags, incorrect trim data)

### TileSet

- [ ] **TILE-01**: `gdauto tileset create` accepts a sprite sheet image + tile size and generates a .tres TileSet with TileSetAtlasSource (supports margin and separation parameters)
- [ ] **TILE-02**: `gdauto tileset auto-terrain` auto-assigns terrain peering bits for the 47-tile blob layout (Match Corners and Sides, 8 bits)
- [ ] **TILE-03**: `gdauto tileset auto-terrain` auto-assigns terrain peering bits for the 16-tile minimal layout (Match Sides, 4 bits)
- [ ] **TILE-04**: `gdauto tileset auto-terrain` auto-assigns terrain peering bits for the RPG Maker layout
- [ ] **TILE-05**: `gdauto tileset assign-physics` batch assigns collision shapes (full, half-top, half-bottom, none) to tile ranges by pattern
- [ ] **TILE-06**: `gdauto tileset inspect` dumps an existing TileSet resource as structured JSON: atlas sources, terrain sets, peering bit configurations, physics layers
- [ ] **TILE-07**: TileSet validation: verifies generated TileSets load in headless Godot, terrain painting produces correct tile selection
- [ ] **TILE-08**: Researched common tileset import failures and built preventions into the tool (wrong tile size, misaligned grid, incorrect peering bits)
- [ ] **TILE-09**: `gdauto tileset import-tiled` reads Tiled .tmx (XML) and .tmj (JSON) files and converts to Godot TileSet/TileMap resources

### Scene

- [ ] **SCEN-01**: `gdauto scene list` enumerates all scenes in a project, dumps node trees, shows dependencies between scenes and scripts
- [ ] **SCEN-02**: `gdauto scene create` creates .tscn scene files from JSON/YAML node tree definitions with node hierarchy, property assignments, script references

### Testing

- [ ] **TEST-01**: Unit tests for all pure Python logic (parser, value types, Aseprite conversion, peering bit calculation) run without Godot binary
- [ ] **TEST-02**: E2E tests marked with `@pytest.mark.requires_godot` that load generated .tres/.tscn in headless Godot
- [ ] **TEST-03**: Validation tests that verify peering bit assignments match expected patterns for all supported layouts
- [ ] **TEST-04**: Generated .tres/.tscn files validated against known-good reference outputs

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Advanced Integration

- **ADV-01**: Live game interaction via Godot remote debugger protocol
- **ADV-02**: RL/ML training pipeline integration (Godot RL Agents bridge)
- **ADV-03**: Particle effect and shader preset generation
- **ADV-04**: Multiplayer server management and load testing
- **ADV-05**: Addon/plugin management wrapping the Asset Library API
- **ADV-06**: Session undo/redo state management

## Out of Scope

| Feature | Reason |
|---------|--------|
| GUI or TUI interface | Contradicts agent-native design; interactive elements break CI/CD |
| Godot version management | Well-solved by gdvm and GodotEnv; no value in reimplementing |
| Godot 3.x support | Different file format (format=2), different headless approach, shrinking user base |
| Binary .scn/.res file support | Underdocumented, version-specific; text formats are the standard for VCS |
| OAuth or web-based workflows | CLI-only tool |
| godot_parser library dependency | Inactive 2+ years, uncertain Godot 4 format=3 support, whitespace fidelity bugs |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLI-01 | TBD | Pending |
| CLI-02 | TBD | Pending |
| CLI-03 | TBD | Pending |
| CLI-04 | TBD | Pending |
| CLI-05 | TBD | Pending |
| CLI-06 | TBD | Pending |
| FMT-01 | TBD | Pending |
| FMT-02 | TBD | Pending |
| FMT-03 | TBD | Pending |
| FMT-04 | TBD | Pending |
| FMT-05 | TBD | Pending |
| FMT-06 | TBD | Pending |
| FMT-07 | TBD | Pending |
| PROJ-01 | TBD | Pending |
| PROJ-02 | TBD | Pending |
| PROJ-03 | TBD | Pending |
| PROJ-04 | TBD | Pending |
| PROJ-05 | TBD | Pending |
| EXPT-01 | TBD | Pending |
| EXPT-02 | TBD | Pending |
| EXPT-03 | TBD | Pending |
| EXPT-04 | TBD | Pending |
| EXPT-05 | TBD | Pending |
| SPRT-01 | TBD | Pending |
| SPRT-02 | TBD | Pending |
| SPRT-03 | TBD | Pending |
| SPRT-04 | TBD | Pending |
| SPRT-05 | TBD | Pending |
| SPRT-06 | TBD | Pending |
| SPRT-07 | TBD | Pending |
| SPRT-08 | TBD | Pending |
| SPRT-09 | TBD | Pending |
| SPRT-10 | TBD | Pending |
| SPRT-11 | TBD | Pending |
| SPRT-12 | TBD | Pending |
| TILE-01 | TBD | Pending |
| TILE-02 | TBD | Pending |
| TILE-03 | TBD | Pending |
| TILE-04 | TBD | Pending |
| TILE-05 | TBD | Pending |
| TILE-06 | TBD | Pending |
| TILE-07 | TBD | Pending |
| TILE-08 | TBD | Pending |
| TILE-09 | TBD | Pending |
| SCEN-01 | TBD | Pending |
| SCEN-02 | TBD | Pending |
| TEST-01 | TBD | Pending |
| TEST-02 | TBD | Pending |
| TEST-03 | TBD | Pending |
| TEST-04 | TBD | Pending |

**Coverage:**
- v1 requirements: 46 total
- Mapped to phases: 0
- Unmapped: 46

---
*Requirements defined: 2026-03-27*
*Last updated: 2026-03-27 after initial definition*
