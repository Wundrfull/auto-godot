# Phase 1: Foundation and CLI Infrastructure - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Phase Boundary

Deliver an installable CLI tool with a custom Godot file format parser, CLI skeleton with --json infrastructure, Godot backend wrapper, project management commands (info, validate, create), and resource inspection. This phase builds the foundation that all subsequent phases (Aseprite bridge, TileSet automation, scene commands) depend on.

</domain>

<decisions>
## Implementation Decisions

### Parser Data Model
- **D-01:** Section-based flat model. GdResource/GdScene at the top with ordered lists of ExtResource, SubResource, and property sections. Mirrors the .tres/.tscn file structure 1:1. Round-trip fidelity is the priority; feature modules handle their own lookups.
- **D-02:** Typed dataclasses for Godot value types (Vector2, Rect2, Color, Transform2D, etc.) with full arithmetic support (addition, subtraction, multiplication, dot product, length, contains, intersection, etc.).
- **D-03:** Godot-native string serialization in JSON output. Vector2(0, 0) becomes "Vector2(0, 0)" in JSON. Matches what Godot users see in .tres files.
- **D-04:** Lenient parser: preserve unknown sections and values as raw strings, warn on stderr. Forward-compatible with future Godot versions and custom resources.
- **D-05:** Preserve comments and blank lines for round-trip fidelity (FMT-06). Editing an existing file should not produce spurious diffs.
- **D-06:** Single module per format: tscn.py owns .tscn parse + serialize, tres.py owns .tres parse + serialize.
- **D-07:** Full load into memory (no streaming/lazy API). Godot files are typically small. Simple API, optimize later if a real bottleneck emerges.
- **D-08:** Match Godot's exact resource ID format (Type_xxxxx pattern with the same character set). Generated files should be indistinguishable from Godot-generated ones.

### Project Templates
- **D-09:** Opinionated built-in template with recommended folder structure: project.godot, main scene, icon.svg, plus folders (scenes/, scripts/, assets/, sprites/, tilesets/), .gitignore, .gdignore.
- **D-10:** Built-in template only for v1. No custom template support in this phase.
- **D-11:** Godot 4.5 defaults: config_version=5, format=3.
- **D-12:** Argument only, no interactive prompts. `gdauto project create my-game` creates the project. Fails if no name given. Agent-native.

### Human Output Style
- **D-13:** Rich formatted output via rich-click. Colored tables, tree views for node hierarchies. Degrades gracefully to plain text when piped or in no-color mode.
- **D-14:** Three verbosity levels: default (normal), --verbose/-v (extra detail: file paths, timing, parse stats), --quiet/-q (suppress all except errors).
- **D-15:** Always include fix suggestions in error messages. Every error has an actionable hint. Helps both humans and AI agents recover.

### CLI Global Options
- **D-16:** Short flags for common options: -j/--json, -v/--verbose, -q/--quiet, -o/--output.
- **D-17:** Godot binary discovery: auto-discover from PATH by default. GODOT_PATH environment variable as override. --godot-path flag as highest priority. Resolution order: flag > env > PATH.
- **D-18:** --json is a global flag on the main Click group, inherited by all subcommands via Click context. Single implementation point, guaranteed consistency.
- **D-19:** Both --no-color flag and NO_COLOR environment variable respected. Rich-click handles this natively.
- **D-20:** Validate Godot binary version (>= 4.5) on first use, cache result for the session. Subsequent commands skip the check.

### Claude's Discretion
- Shared bracket-section syntax organization: whether to extract common parsing logic into a base module or keep it per-format
- UID generation strategy: whether to generate UIDs for new resources or preserve-only
- Resource inspect metadata: whether JSON output includes a metadata wrapper (file path, format version, warnings) or raw resource data only
- Resource inspect human display: syntax-highlighted Godot format vs structured table/tree view

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### CLI Architecture
- `CLI-METHODOLOGY.md` -- Click CLI entry point patterns, --json flag implementation, backend wrapper pattern, PEP 420 namespace package structure, test strategy (unit/e2e split), error handling standards, SKILL.md format

### Godot Engine
- `GODOT-RESEARCH.md` -- Godot headless mode capabilities and limitations, .tscn/.tres file format specification, project.godot format, Aseprite JSON output structure, TileSet terrain system, known issues and gotchas

### Project Requirements
- `.planning/REQUIREMENTS.md` -- Phase 1 requirements: CLI-01 through CLI-05, FMT-01 through FMT-07, PROJ-01 through PROJ-05, TEST-01

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- No existing code. This is a greenfield project.

### Established Patterns
- No patterns established yet. This phase sets the patterns for all subsequent phases.

### Integration Points
- pyproject.toml entry point will register `gdauto` as the CLI command
- Click command groups (project, export, sprite, tileset, scene, resource) are registered in cli.py
- All subcommands inherit global --json, --verbose, --quiet, --no-color flags from the main group via Click context

</code_context>

<specifics>
## Specific Ideas

- Generated .tres/.tscn files must be indistinguishable from Godot-generated ones (exact ID format, exact value serialization)
- Parser should be forward-compatible: unknown content preserved as raw strings rather than rejected
- The CLI is agent-native first: every command works non-interactively, every command supports --json, every error is actionable

</specifics>

<deferred>
## Deferred Ideas

None -- discussion stayed within phase scope

</deferred>

---

*Phase: 01-foundation-and-cli-infrastructure*
*Context gathered: 2026-03-27*
