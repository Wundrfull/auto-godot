# Phase 1: Foundation and CLI Infrastructure - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md -- this log preserves the alternatives considered.

**Date:** 2026-03-27
**Phase:** 01-foundation-and-cli-infrastructure
**Areas discussed:** Parser data model, Project templates, Human output style, CLI global options

---

## Parser Data Model

### File representation in memory

| Option | Description | Selected |
|--------|-------------|----------|
| Section-based flat model | GdResource/GdScene with ordered lists of sections. Mirrors file 1:1. Simple, natural round-trip. | ✓ |
| Tree model with typed nodes | Resources as a tree with SubResources as children. More semantic but fights the flat file format. | |
| Hybrid: flat storage, semantic accessors | Flat storage with helper methods (get_sub, find_by_type, add_sub). Best of both. | |

**User's choice:** Section-based flat model
**Notes:** User requested a detailed pros/cons discussion before choosing. Chose flat model for simplicity and round-trip fidelity priority; feature modules handle their own lookups.

### Godot value type representation

| Option | Description | Selected |
|--------|-------------|----------|
| Typed dataclasses | Each Godot type gets a Python dataclass. Type-safe, IDE autocompletion. | ✓ |
| Plain tuples/dicts | Simpler, no custom classes, but no type safety. | |
| String-preserving | Store as raw strings, parse only when needed. | |

**User's choice:** Typed dataclasses
**Notes:** None

### JSON output for Godot-specific values

| Option | Description | Selected |
|--------|-------------|----------|
| Godot-native strings | Vector2(0, 0) becomes "Vector2(0, 0)". Familiar, compact. | ✓ |
| Expanded objects | Vector2(0, 0) becomes {"type": "Vector2", "x": 0, "y": 0}. More structured. | |
| You decide | Claude's discretion. | |

**User's choice:** Godot-native strings
**Notes:** None

### Parser strictness

| Option | Description | Selected |
|--------|-------------|----------|
| Lenient: preserve unknown, warn | Parse recognized content, pass through unknown as raw strings. | ✓ |
| Strict: reject malformed | Fail on unrecognized sections or value types. | |
| You decide | Claude's discretion. | |

**User's choice:** Lenient
**Notes:** None

### Comments and blank lines

| Option | Description | Selected |
|--------|-------------|----------|
| Preserve comments and blanks | Store as part of section data. Critical for FMT-06. | ✓ |
| Strip comments, normalize blanks | Simpler parser but produces diffs on existing files. | |
| You decide | Claude's discretion. | |

**User's choice:** Preserve comments and blanks
**Notes:** None

### Module organization

| Option | Description | Selected |
|--------|-------------|----------|
| Single module per format | tscn.py and tres.py each own parse + serialize. | ✓ |
| Separate parse and serialize | tscn_parser.py + tscn_writer.py per format. | |
| Unified core + format wrappers | One godot_format.py with thin wrappers. | |

**User's choice:** Single module per format
**Notes:** None

### Shared bracket-section syntax

| Option | Description | Selected |
|--------|-------------|----------|
| Shared base parser in formats/base.py | Extract common state machine into base module. | |
| Duplicate in each module | Each module has its own parser. Zero coupling. | |
| You decide | Claude's discretion. | ✓ |

**User's choice:** You decide
**Notes:** Claude's discretion on shared syntax organization.

### Value type arithmetic operations

| Option | Description | Selected |
|--------|-------------|----------|
| Serialize/deserialize only | Thin dataclasses. No math operations. | |
| Full arithmetic support | Vector2 +, -, *, dot(), length(). Rect2 contains(), etc. | ✓ |
| You decide | Claude's discretion. | |

**User's choice:** Full arithmetic support
**Notes:** None

### UID handling

| Option | Description | Selected |
|--------|-------------|----------|
| Generate UIDs for new resources | Auto-generate valid UIDs and .uid companion files. | |
| Preserve only, don't generate | Round-trip existing UIDs, let Godot assign new ones. | |
| You decide | Claude's discretion. | ✓ |

**User's choice:** You decide
**Notes:** Claude's discretion on UID generation strategy.

### File loading strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Full load into memory | Read entire file, parse all sections. Simple API. | ✓ |
| Streaming/section-at-a-time | Parse lazily. Handles huge TileMap files. | |
| You decide | Claude's discretion. | |

**User's choice:** Full load into memory
**Notes:** None

### Resource inspect metadata

| Option | Description | Selected |
|--------|-------------|----------|
| Include metadata wrapper | Wrap in {"file": ..., "format": ..., "warnings": ..., "resource": ...}. | |
| Raw resource data only | Just the resource content. | |
| You decide | Claude's discretion. | ✓ |

**User's choice:** You decide
**Notes:** Claude's discretion.

### Resource ID generation

| Option | Description | Selected |
|--------|-------------|----------|
| Match Godot's format exactly | Same Type_xxxxx pattern with same character set. Indistinguishable from Godot. | ✓ |
| Compatible but distinct | Valid IDs but different generation scheme. | |
| You decide | Claude's discretion. | |

**User's choice:** Match Godot's format exactly
**Notes:** None

---

## Project Templates

### Folder structure opinionatedness

| Option | Description | Selected |
|--------|-------------|----------|
| Minimal: bare essentials | Just project.godot + main scene + icon.svg. | |
| Opinionated: recommended structure | project.godot + main scene + recommended folders + .gitignore + .gdignore. | ✓ |
| Multiple built-in templates | Named templates: minimal, 2d-game, 3d-game, plugin. | |

**User's choice:** Opinionated: recommended structure
**Notes:** None

### Custom template support

| Option | Description | Selected |
|--------|-------------|----------|
| Built-in only for v1 | One opinionated template. Custom support is future work. | ✓ |
| Directory-as-template from day one | --template /path/to/dir with variable substitution. | |
| You decide | Claude's discretion. | |

**User's choice:** Built-in only for v1
**Notes:** None

### Godot version defaults

| Option | Description | Selected |
|--------|-------------|----------|
| Godot 4.5 defaults | config_version=5, format=3. Matches minimum supported version. | ✓ |
| Detect installed Godot version | Query binary version, fall back to 4.5. | |
| You decide | Claude's discretion. | |

**User's choice:** Godot 4.5 defaults
**Notes:** None

### Create UX

| Option | Description | Selected |
|--------|-------------|----------|
| Argument only, no prompts | `gdauto project create my-game`. Fails if no name. Agent-native. | ✓ |
| Argument with fallback prompt | Prompts if no argument provided. | |
| You decide | Claude's discretion. | |

**User's choice:** Argument only, no prompts
**Notes:** None

---

## Human Output Style

### Output format

| Option | Description | Selected |
|--------|-------------|----------|
| Rich formatted | Colored output, tables, tree views via rich-click. Degrades gracefully. | ✓ |
| Plain text with structure | Simple indented text. No colors, no tables. | |
| Minimal: just the data | Bare minimum. Optimized for piping. | |

**User's choice:** Rich formatted
**Notes:** None

### Resource inspect display

| Option | Description | Selected |
|--------|-------------|----------|
| Syntax-highlighted Godot format | Pretty-printed version of raw file with colors. | |
| Structured table/tree view | Rich tables and trees. More readable, less familiar. | |
| You decide | Claude's discretion. | ✓ |

**User's choice:** You decide
**Notes:** Claude's discretion on inspect display format.

### Verbosity levels

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, three levels | Default, --verbose/-v, --quiet/-q. Standard CLI convention. | ✓ |
| Default output only | No verbosity flags. | |
| You decide | Claude's discretion. | |

**User's choice:** Yes, three levels
**Notes:** None

### Error fix suggestions

| Option | Description | Selected |
|--------|-------------|----------|
| Always include fix suggestions | Every error has an actionable hint. | ✓ |
| Suggestions for common errors only | Only well-known failure modes get suggestions. | |
| You decide | Claude's discretion. | |

**User's choice:** Always include fix suggestions
**Notes:** None

---

## CLI Global Options

### Short flags

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, for common flags | -j, -v, -q, -o for frequently-used options. | ✓ |
| Long flags only | Always --json, --verbose, etc. More explicit. | |
| You decide | Claude's discretion. | |

**User's choice:** Yes, for common flags
**Notes:** None

### Godot binary specification

| Option | Description | Selected |
|--------|-------------|----------|
| PATH + --godot-path override | Auto-discover PATH, GODOT_PATH env, --godot-path flag. Priority: flag > env > PATH. | ✓ |
| PATH only | Only look on PATH. | |
| Config file + PATH | .gdautorc or pyproject.toml section for persistent path. | |

**User's choice:** PATH + --godot-path override
**Notes:** None

### --json scope

| Option | Description | Selected |
|--------|-------------|----------|
| Global flag | On main Click group, inherited by all subcommands. | ✓ |
| Per-command flag | Each command defines its own --json. | |
| Both: global with per-command override | Global sets default, commands can override. | |

**User's choice:** Global flag
**Notes:** None

### Color control

| Option | Description | Selected |
|--------|-------------|----------|
| Both --no-color and NO_COLOR env | Respect no-color.org standard and provide flag. | ✓ |
| NO_COLOR env only | Ecosystem standard only. | |
| You decide | Claude's discretion. | |

**User's choice:** Both --no-color and NO_COLOR env
**Notes:** None

### Godot version validation

| Option | Description | Selected |
|--------|-------------|----------|
| Validate on first use, cache result | Check >= 4.5 on first use, cache for session. | ✓ |
| Validate every time | Check on every Godot invocation. Safer but slower. | |
| You decide | Claude's discretion. | |

**User's choice:** Validate on first use, cache result
**Notes:** None

---

## Claude's Discretion

- Shared bracket-section syntax organization (base module vs per-format duplication)
- UID generation strategy (generate for new resources vs preserve-only)
- Resource inspect metadata wrapper (include file/format/warnings or raw data only)
- Resource inspect human display format (syntax-highlighted vs table/tree)

## Deferred Ideas

None -- discussion stayed within phase scope
