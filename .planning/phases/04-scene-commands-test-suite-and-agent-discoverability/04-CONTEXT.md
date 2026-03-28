# Phase 4: Scene Commands, Test Suite, and Agent Discoverability - Context

**Gathered:** 2026-03-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Complete the tool with scene manipulation commands (scene list with full node trees and dependency graphs, scene create from JSON definitions), comprehensive E2E testing that loads all generated resource types in headless Godot, golden file validation against committed reference outputs, and a SKILL.md auto-generated from the CLI command tree for AI agent discovery. This is the final phase: the tool becomes feature-complete and fully validated.

</domain>

<decisions>
## Implementation Decisions

### Scene Definition Format
- **D-01:** JSON file input for scene create. Pass a .json file describing the node tree. Consistent with Aseprite JSON input pattern from Phase 2. Agent-friendly (agents generate JSON easily).
- **D-02:** Full property passthrough. Any property as key-value pairs in JSON, serialized directly to .tscn node properties. Supports every Godot node type without hardcoding property lists.
- **D-03:** No CLI flags for simple trees. JSON-only input keeps the interface consistent and avoids a second code path.

### Scene List Output
- **D-04:** Full node tree by default. Show complete node hierarchy for each scene. --depth N flag available to limit tree depth for large scenes.
- **D-05:** Comprehensive metadata per scene: file path, root node type, node count, script references, resource dependencies, sub-scene (PackedScene) references.
- **D-06:** Cross-scene dependency graph. Detect PackedScene references across all .tscn files. Show which scenes instance other scenes for full project structure understanding.

### E2E Test Strategy
- **D-07:** @pytest.mark.requires_godot marker on all E2E tests. Tests skip gracefully when no Godot binary is found. CI installs Godot to run full suite. Local devs without Godot still run all unit tests.
- **D-08:** Validate all resource types in headless Godot: SpriteFrames .tres, TileSet .tres, and .tscn scenes. Full confidence that every generated file loads without modification.
- **D-09:** Committed golden files in tests/fixtures/golden/. Known-good .tres/.tscn reference outputs checked into the repo. Tests compare generated output byte-for-byte (ignoring UIDs). Explicit, reviewable in PRs.

### SKILL.md Generation
- **D-10:** Auto-generated from Click introspection at runtime. `gdauto skill generate` command walks the Click command tree, extracts all command names, arguments, options, help text. Always in sync with CLI.
- **D-11:** One usage example per command in SKILL.md. Agents can copy-paste concrete examples. More useful for agent workflows than signatures alone.

### Claude's Discretion
- SKILL.md format (structured markdown vs YAML blocks): pick what works best for LLM consumption
- External resource reference support in scene create: pick based on existing parser capabilities (res:// paths, ext_resource generation)
- Scene JSON schema details: node tree structure, property naming convention, how children are expressed
- E2E test fixture design: which specific resources to generate and validate
- Golden file comparison logic: how to normalize UIDs and timestamps for stable comparison
- scene list human output format: tree rendering style (indentation, connectors, colors)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### CLI Architecture
- `CLI-METHODOLOGY.md` -- Click CLI patterns, --json flag implementation, output conventions, error handling standards, SKILL.md generation guidance

### Project Requirements
- `.planning/REQUIREMENTS.md` -- Phase 4 requirements: SCEN-01, SCEN-02, CLI-06, TEST-02, TEST-03, TEST-04

### Prior Phase Context
- `.planning/phases/01-foundation-and-cli-infrastructure/01-CONTEXT.md` -- Parser model, CLI conventions, output style, error handling patterns
- `.planning/phases/02-aseprite-to-spriteframes-bridge/02-CONTEXT.md` -- Validation-as-separate-command pattern, JSON input file pattern, partial failure handling
- `.planning/phases/03-tileset-automation-and-export-pipeline/03-CONTEXT.md` -- Export pipeline patterns, backend wrapper usage

### Existing Code
- `src/gdauto/formats/tscn.py` -- GdScene parser and serializer: the .tscn reader/writer for scene operations
- `src/gdauto/formats/tres.py` -- GdResource parser and serializer: reference for file format patterns
- `src/gdauto/commands/scene.py` -- Stub command group to populate with list and create
- `src/gdauto/cli.py` -- Root CLI group, command registration pattern
- `src/gdauto/backend.py` -- GodotBackend for headless Godot operations (E2E tests)
- `src/gdauto/output.py` -- emit()/emit_error() for JSON/human output
- `src/gdauto/sprite/validator.py` -- Pattern for headless Godot validation (reusable for E2E tests)
- `tests/fixtures/` -- Existing test fixtures directory (golden files go in tests/fixtures/golden/)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/gdauto/formats/tscn.py` -- GdScene dataclass with nodes list, ext_resources, sub_resources. parse_tscn_file() and serialize_tscn_file() for reading/writing .tscn files. Scene create builds a GdScene and serializes it.
- `src/gdauto/formats/values.py` -- All Godot value types (Vector2, Rect2, Color, etc.) with serialization. Scene create uses these for property values in the JSON definition.
- `src/gdauto/formats/uid.py` -- UID and resource ID generation for new scenes and resources.
- `src/gdauto/backend.py` -- GodotBackend with binary discovery, version validation, timeout management. E2E tests use this to load resources in headless Godot.
- `src/gdauto/output.py` -- emit()/emit_error() for JSON/human output. Scene list uses this.
- `src/gdauto/sprite/validator.py` -- Pattern for headless Godot validation with GDScript generation. E2E tests can follow this pattern.

### Established Patterns
- Command stubs in `src/gdauto/commands/` with `@click.group(invoke_without_command=True)`
- JSON input file pattern from sprite import-aseprite (read JSON, parse into dataclass, generate output)
- Validation pattern: structural check in Python, then optional headless Godot load
- Global flags inherited via Click context (--json, --verbose, --quiet, --godot-path)
- emit() for structured output, emit_error() for errors with codes and fix suggestions

### Integration Points
- `src/gdauto/commands/scene.py` -- stub group, add list and create subcommands
- `src/gdauto/cli.py` -- skill command group or standalone command for SKILL.md generation
- `pyproject.toml` -- pytest markers configuration for requires_godot
- `tests/fixtures/golden/` -- new directory for golden file test references

</code_context>

<specifics>
## Specific Ideas

- Scene create JSON input follows the same pattern as Aseprite JSON import: file path argument, parse to dataclass, generate output
- SKILL.md generation uses Click's introspection API (command.params, command.help, etc.) to walk the full command tree
- E2E tests should cover the "happy path" for each major command: import-aseprite, tileset create + auto-terrain, scene create, export
- Golden file comparison should strip or normalize UIDs since they are randomly generated
- Scene list dependency graph requires scanning all .tscn files in the project, which means the command needs a project root (discovered from project.godot)

</specifics>

<deferred>
## Deferred Ideas

None -- discussion stayed within phase scope

</deferred>

---

*Phase: 04-scene-commands-test-suite-and-agent-discoverability*
*Context gathered: 2026-03-28*
