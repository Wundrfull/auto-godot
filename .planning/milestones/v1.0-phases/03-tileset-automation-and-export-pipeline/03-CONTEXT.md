# Phase 3: TileSet Automation and Export Pipeline - Context

**Gathered:** 2026-03-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver TileSet creation from sprite sheets, automatic terrain peering bit assignment for standard layouts, physics collision shape assignment, TileSet inspection, Tiled .tmx/.tmj import, and headless export/import commands with retry logic and auto-import. Builds on the Phase 1 parser/serializer and Phase 2 sprite patterns.

</domain>

<decisions>
## Implementation Decisions

### Terrain Layout Detection
- **D-01:** Explicit --layout flag required for auto-terrain. User must specify: --layout blob-47, --layout minimal-16, or --layout rpgmaker. No auto-detection. Fail with actionable error if flag is omitted.
- **D-02:** Built-in layouts only for v1. Support blob-47, minimal-16, and rpgmaker. No custom JSON layout mapping. Custom layouts deferred to future milestone.

### Collision Shape Assignment
- **D-03:** Range-based rules via CLI flags. Syntax: --physics 0-15:full --physics 16-31:none. Tile index ranges mapped to shape presets. Scriptable and agent-friendly.
- **D-04:** Two shape types only: full (full tile rectangle) and none (no collision). Half-tiles, slopes, and custom shapes deferred.

### Export Pipeline
- **D-05:** Auto-import before export. If Godot import cache is missing, automatically run godot --headless --import before the export operation. Seamless for CI/CD pipelines.
- **D-06:** Exponential backoff retry for import. Retry up to 3 times with exponential backoff (1s, 2s, 4s). Use --quit-after instead of --quit to avoid known Godot race condition.
- **D-07:** Stderr status lines for progress reporting. Print status updates ("Importing...", "Exporting...", "Done") to stderr. JSON output on stdout stays clean. Consistent with existing emit_error pattern.

### Tiled Import
- **D-08:** Basic tilemap conversion only. Parse .tmx/.tmj, extract tileset reference, tile size, and tile grid. Generate TileSet .tres with atlas source. No terrain sets, physics, or custom properties from Tiled.
- **D-09:** Support both .tmx (XML via stdlib xml.etree) and .tmj (JSON via stdlib json). Both are zero-dependency. Covers all Tiled users.

### Claude's Discretion
- Internal module organization for tileset commands (single module vs separate create/terrain/physics/inspect)
- Peering bit lookup table structure (dict, enum, or computed from position)
- TileSet .tres format details (sub-resource structure for atlas sources, terrain sets)
- Tiled format version handling and which fields to extract
- tileset inspect output structure and detail level
- Error messages and fix suggestions for all new commands

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### CLI Architecture
- `CLI-METHODOLOGY.md` -- Click CLI patterns, --json flag implementation, output conventions, error handling standards, backend wrapper pattern

### Godot Engine
- `GODOT-RESEARCH.md` -- TileSet structure (TileSetAtlasSource, terrain sets, peering bits), terrain peering bit system (Match Corners and Sides, Match Corners, Match Sides), standard tileset layouts (47-tile blob, 16-tile minimal, RPG Maker), headless export/import commands, known timing issues

### Project Requirements
- `.planning/REQUIREMENTS.md` -- Phase 3 requirements: TILE-01 through TILE-09, EXPT-01 through EXPT-05

### Prior Phase Context
- `.planning/phases/01-foundation-and-cli-infrastructure/01-CONTEXT.md` -- Parser model, CLI conventions, output style, error handling patterns
- `.planning/phases/02-aseprite-to-spriteframes-bridge/02-CONTEXT.md` -- Validation-as-separate-command pattern, Pillow optional dependency pattern, partial failure handling

### Existing Code
- `src/gdauto/formats/tres.py` -- GdResource, ExtResource, SubResource, serialize_tres_file: the .tres writer for TileSet generation
- `src/gdauto/formats/values.py` -- Vector2i (tile sizes), Rect2 (atlas regions), value serialization
- `src/gdauto/formats/uid.py` -- UID and resource ID generation
- `src/gdauto/backend.py` -- GodotBackend for headless export/import operations
- `src/gdauto/commands/tileset.py` -- Stub command group to populate
- `src/gdauto/commands/export.py` -- Stub command group to populate
- `src/gdauto/sprite/validator.py` -- Pattern for headless Godot validation (reusable for TileSet validation)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/gdauto/formats/tres.py` -- GdResource/SubResource/ExtResource dataclasses and serialize_tres_file() for writing valid .tres files. TileSet generation follows the same pattern as SpriteFrames.
- `src/gdauto/formats/values.py` -- Vector2i for tile sizes, Rect2 for atlas source regions, serialize_value() for property values
- `src/gdauto/formats/uid.py` -- generate_uid()/uid_to_text() for .tres UIDs, generate_resource_id() for sub-resource IDs
- `src/gdauto/backend.py` -- GodotBackend with binary discovery, version validation, timeout management. Used by sprite validate, will be used by export/import commands.
- `src/gdauto/output.py` -- emit()/emit_error() for JSON/human output. All new commands follow this pattern.
- `src/gdauto/sprite/validator.py` -- Pattern for headless Godot validation with structural pre-check + optional headless load. Reusable pattern for TileSet validation.

### Established Patterns
- Command stubs in `src/gdauto/commands/` with `@click.group(invoke_without_command=True)`
- Pillow guarded behind optional dependency with _require_pillow() pattern (from sprite split/atlas)
- Separate validation command rather than built-in validation (sprite validate pattern)
- Parse functions return dataclasses; serialize functions accept dataclasses
- Global flags inherited via Click context (--json, --verbose, --quiet, --godot-path)

### Integration Points
- `src/gdauto/commands/tileset.py` -- stub group, add create, auto-terrain, assign-physics, inspect, import-tiled
- `src/gdauto/commands/export.py` -- stub group, add release, debug, pack
- `src/gdauto/cli.py` -- import command at root level (gdauto import, not under export group)
- `pyproject.toml` -- Pillow already declared as optional [image] dependency

</code_context>

<specifics>
## Specific Ideas

- TileSet terrain peering bits are the key differentiator: no other CLI tool automates this
- The 47-tile blob layout is the most important (full corner+side matching, covers all neighbor combinations)
- Peering bit mappings are reverse-engineered from community conventions, not official Godot docs (noted as blocker/concern in STATE.md)
- Export commands are thin wrappers around GodotBackend but add retry logic and auto-import
- Tiled import is basic: just tileset extraction, not full map conversion

</specifics>

<deferred>
## Deferred Ideas

- Custom layout JSON mapping for auto-terrain (user-defined position-to-bit mappings)
- Half-tile, slope, and custom collision shapes for assign-physics
- Tiled terrain/Wang set conversion to Godot terrain peering bits
- Tiled custom properties import
- Full Tiled map-to-TileMap scene conversion

</deferred>

---

*Phase: 03-tileset-automation-and-export-pipeline*
*Context gathered: 2026-03-28*
