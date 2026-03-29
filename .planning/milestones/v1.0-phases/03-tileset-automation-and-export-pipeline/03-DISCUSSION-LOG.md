# Phase 3: TileSet Automation and Export Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md -- this log preserves the alternatives considered.

**Date:** 2026-03-28
**Phase:** 03-tileset-automation-and-export-pipeline
**Areas discussed:** Terrain layout detection, Collision shape assignment, Export pipeline behavior, Tiled import scope

---

## Terrain Layout Detection

| Option | Description | Selected |
|--------|-------------|----------|
| Explicit --layout flag | User must specify: --layout blob-47, minimal-16, rpgmaker. Fail with actionable error if omitted. | x |
| Auto-detect from grid dimensions | Infer layout from tile count and grid shape. Falls back to error if ambiguous. | |
| Both: detect with override | Auto-detect by default, --layout flag overrides. | |

**User's choice:** Explicit --layout flag
**Notes:** None

| Option | Description | Selected |
|--------|-------------|----------|
| Built-in layouts only | Support blob-47, minimal-16, rpgmaker. Custom layouts deferred. | x |
| Also allow custom JSON mapping | User provides JSON mapping of grid positions to peering bit values. | |

**User's choice:** Built-in layouts only
**Notes:** None

---

## Collision Shape Assignment

| Option | Description | Selected |
|--------|-------------|----------|
| Range-based rules | CLI flags like --physics 0-15:full --physics 16-31:none. Tile index ranges mapped to shape presets. | x |
| Row/column-based rules | --physics row:3=full --physics col:0=half-top. | |
| Named presets file | JSON/YAML file mapping tile indices to shapes. | |

**User's choice:** Range-based rules
**Notes:** None

| Option | Description | Selected |
|--------|-------------|----------|
| Full + none only | Full tile rectangle or no collision. 90% coverage. | x |
| Full, half-top, half-bottom, none | Four presets for common platformer needs. | |
| Full, halves, slopes, none | Also 45-degree slopes. | |

**User's choice:** Full + none only
**Notes:** None

---

## Export Pipeline Behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Auto-import before export | If import cache missing, auto-run godot --headless --import first. | x |
| Fail with instructions | Detect missing cache, fail with actionable message. | |
| Flag-controlled | --auto-import flag enables it, off by default. | |

**User's choice:** Auto-import before export
**Notes:** None

| Option | Description | Selected |
|--------|-------------|----------|
| Exponential backoff with limit | Retry up to 3 times (1s, 2s, 4s). Use --quit-after. | x |
| Single retry with timeout | Try once, retry once with longer timeout. | |
| No retry, fail fast | Run once, report failure. | |

**User's choice:** Exponential backoff with limit
**Notes:** None

| Option | Description | Selected |
|--------|-------------|----------|
| Stderr status lines | Print status updates to stderr. JSON on stdout stays clean. | x |
| Progress bar via rich | Rich progress bar on stderr. | |
| Silent unless --verbose | No progress by default. | |

**User's choice:** Stderr status lines
**Notes:** None

---

## Tiled .tmx/.tmj Import Scope

| Option | Description | Selected |
|--------|-------------|----------|
| Basic tilemap only | Parse .tmx/.tmj, extract tileset + tile size + grid. No terrain/physics/custom properties. | x |
| Tileset + terrain mapping | Also convert Tiled terrain/Wang sets to Godot peering bits. | |
| Defer entirely to Phase 4+ | Drop TILE-09 from Phase 3. | |

**User's choice:** Basic tilemap only
**Notes:** None

| Option | Description | Selected |
|--------|-------------|----------|
| Both .tmx and .tmj | XML via stdlib xml.etree, JSON via stdlib json. Zero dependency. | x |
| JSON (.tmj) only | Simpler, JSON already used elsewhere. | |
| XML (.tmx) only | Original and more common format. | |

**User's choice:** Both .tmx and .tmj
**Notes:** None

---

## Claude's Discretion

- Internal module organization for tileset commands
- Peering bit lookup table structure
- TileSet .tres format details
- Tiled format version handling
- tileset inspect output structure
- Error messages and fix suggestions

## Deferred Ideas

- Custom layout JSON mapping for auto-terrain
- Half-tile, slope, and custom collision shapes
- Tiled terrain/Wang set conversion
- Tiled custom properties import
- Full Tiled map-to-TileMap scene conversion
