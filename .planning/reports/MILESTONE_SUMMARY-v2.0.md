# Milestone v2.0 -- Project Summary

**Generated:** 2026-04-06
**Purpose:** Team onboarding and project review

---

## 1. Project Overview

**gdauto** is an agent-native command-line tool for the Godot game engine. Built in Python on Click, it wraps Godot's headless mode and directly manipulates Godot's text-based file formats (.tscn, .tres, project.godot) to automate workflows that currently require the Godot editor GUI.

**Core value:** The Aseprite-to-SpriteFrames bridge: read Aseprite's JSON export and generate valid Godot .tres SpriteFrames resources with named animations, correct frame durations, atlas texture regions, and loop settings, entirely in Python with no Godot binary required.

**Current state:** v1.0 and v1.1 are shipped. The tool has 28 commands across 8 command groups, 7,700+ lines of source code, and 683 tests. v2.0 (Live Game Interaction) is in planning; Phase 7 context has been gathered but no code has been written yet.

**v2.0 Milestone Goal:** Enable Claude Code to connect to a running Godot instance via the remote debugger protocol, read game state, inject player input, and verify behavior, closing the write-code-to-test-it loop without a human in the middle.

### Shipped Milestones

| Milestone | Phases | Plans | Tests | Shipped |
|-----------|--------|-------|-------|---------|
| v1.0 MVP | 4 (Phases 1-4) | 16 | 648 | 2026-03-29 |
| v1.1 Godot 4.6 Compatibility | 2 (Phases 5-6) | 4 | 676 | 2026-03-29 |

## 2. Architecture & Technical Decisions

### Tech Stack

- **Runtime:** Python 3.12+, Click 8.3.x (rich-click for formatted help)
- **Parser:** Custom hand-rolled state machine for .tscn/.tres (no external dependency)
- **Data models:** stdlib dataclasses (no Pydantic)
- **Image processing:** Pillow (optional, for atlas creation and sheet splitting only)
- **Testing:** pytest 9.x with @pytest.mark.requires_godot for E2E tests
- **Packaging:** uv + hatchling + pyproject.toml

### Key Decisions

- **Decision:** Custom .tscn/.tres parser over stevearc/godot_parser
  - **Why:** Inactive 2+ years, Godot 4 issues, whitespace bugs. Hand-rolled gives full control, round-trip fidelity, zero upstream risk.
  - **Phase:** 1

- **Decision:** Python + Click over Rust/Go
  - **Why:** Rapid iteration, rich ecosystem for text parsing, target audience familiar with pip. Produced 7,200+ LOC with fast dev velocity.
  - **Phase:** 1

- **Decision:** dataclasses over Pydantic for internal models
  - **Why:** Internal data already validated by parser; 6x faster instantiation, no dependency overhead.
  - **Phase:** 1

- **Decision:** GCD-based frame timing for Aseprite animations
  - **Why:** Variable-duration frames need base FPS with per-frame multipliers for exact timing preservation.
  - **Phase:** 2

- **Decision:** Algorithmic peering bit generation (256 bitmask combinations filtered by adjacency constraints)
  - **Why:** Produces exact 47/16 valid terrain patterns; eliminates manual lookup table maintenance.
  - **Phase:** 3

- **Decision:** load_steps=None unconditionally in all generators
  - **Why:** Godot 4.6.1 stopped emitting load_steps; Godot 4.5 tolerates omission. Single code path for both.
  - **Phase:** 5

### v2.0 Architecture Decisions (from research/context)

- **Decision:** gdauto is TCP server, not client; game connects TO gdauto
  - **Why:** Matches Godot's --remote-debug flag behavior where the engine connects outward.
  - **Phase:** 7 (planned)

- **Decision:** Zero new pip dependencies for v2.0; all stdlib (asyncio, struct, subprocess)
  - **Why:** Protocol codec and TCP server are well within stdlib capabilities.
  - **Phase:** 7 (planned)

- **Decision:** asyncio.run() at Click boundary; existing 28 commands stay synchronous
  - **Why:** Isolates async TCP/protocol logic from existing sync CLI surface.
  - **Phase:** 7 (planned)

- **Decision:** GDScript autoload bridge for input injection (no custom Godot fork)
  - **Why:** Must work with stock Godot 4.5+; autoload injection is reversible and crash-recoverable.
  - **Phase:** 9 (planned)

## 3. Phases Delivered

| Phase | Name | Milestone | Status | One-Liner |
|-------|------|-----------|--------|-----------|
| 1 | Foundation and CLI Infrastructure | v1.0 | Complete | File format parser, CLI skeleton, Godot backend wrapper, project commands |
| 2 | Aseprite-to-SpriteFrames Bridge | v1.0 | Complete | Core value: Aseprite JSON to valid Godot .tres SpriteFrames |
| 3 | TileSet Automation and Export Pipeline | v1.0 | Complete | TileSet create, auto-terrain, export/import pipeline |
| 4 | Scene Commands, Test Suite, and Agent Discoverability | v1.0 | Complete | Scene list/create, E2E tests, golden files, SKILL.md generation |
| 5 | Format Compatibility and Backwards Safety | v1.1 | Complete | Godot 4.6.1 file format compatibility, backwards safety |
| 6 | E2E Validation and Ecosystem Audit | v1.1 | Complete | E2E tests for 4.6.1 validation, ecosystem position documented |
| 7 | Variant Codec and TCP Connection | v2.0 | Context gathered | Binary protocol codec, TCP server, game launch, connection lifecycle |
| 8 | Scene Inspection and Execution Control | v2.0 | Not started | Read live scene tree, node properties; pause/resume/step/speed |
| 9 | Game Interaction and Bridge System | v2.0 | Not started | Modify properties, inject input, invoke methods via autoload bridge |
| 10 | Verification Layer and End-to-End Validation | v2.0 | Not started | Assert/wait conditions, E2E test workflow, --json contract |

## 4. Requirements Coverage

### v1.0 Requirements (50 total -- all validated)

- [x] CLI-01 through CLI-06: Click CLI with command groups, --json, --help, SKILL.md
- [x] FMT-01 through FMT-07: Custom parser with round-trip fidelity
- [x] PROJ-01 through PROJ-05: Project info, validate, create commands
- [x] SPRT-01 through SPRT-12: Full Aseprite import, sprite split, atlas creation, validation
- [x] TILE-01 through TILE-09: TileSet create, auto-terrain, physics, inspect, Tiled import, validate
- [x] EXPT-01 through EXPT-05: Headless export, import with retry, auto-import
- [x] SCEN-01, SCEN-02: Scene list and create
- [x] TEST-01 through TEST-04: Unit tests, E2E tests, golden files

### v1.1 Requirements (11 total -- all validated, audit: PASSED)

- [x] COMPAT-01 through COMPAT-04: Godot 4.6.1 format changes (load_steps, unique_id, format=4)
- [x] BACK-01, BACK-02: Backwards compatibility with Godot 4.5
- [x] VAL-01 through VAL-03: E2E validation for format changes
- [x] ECO-01, ECO-02: Ecosystem position and compatibility claims

### v2.0 Requirements (19 total -- all pending)

- [ ] PROTO-01 through PROTO-05: Variant codec, TCP server, message draining, game launch, connection lifecycle
- [ ] SCENE-01 through SCENE-03: Live scene tree, node properties, game output capture
- [ ] EXEC-01 through EXEC-03: Pause/resume, frame stepping, game speed control
- [ ] INTERACT-01 through INTERACT-04: Property modification, input injection, method invocation, bridge management
- [ ] VERIFY-01 through VERIFY-04: Assertions, wait conditions, E2E test workflow, --json contract

## 5. Key Decisions Log

### From v1.0/v1.1 Implementation

| ID | Decision | Phase | Rationale |
|----|----------|-------|-----------|
| -- | Custom parser over godot_parser | 1 | Inactive, Godot 4 bugs, whitespace issues |
| -- | State machine parser over regex | 1 | Nested structures make regex fragile |
| -- | Python + Click over Rust/Go | 1 | Rapid iteration, familiar ecosystem |
| -- | dataclasses over Pydantic | 1 | No runtime re-validation needed; 6x faster |
| -- | GCD-based frame timing | 2 | Exact timing preservation for variable-duration animations |
| -- | Algorithmic peering bit generation | 3 | 256 bitmask combinations, no manual tables |
| -- | Apache-2.0 license | 1 | Permissive, compatible with Godot's MIT |
| -- | load_steps=None unconditionally | 5 | Godot 4.5 tolerates omission; single code path |
| -- | Normalization regex for golden files | 5 | Leading-space-anchored for load_steps/unique_id stripping |

### From v2.0 Context Gathering

| ID | Decision | Phase | Rationale |
|----|----------|-------|-----------|
| D-01 | --project flag on subcommands (not global) | 7 | Consistent with existing command patterns |
| D-02 | Combined connect command (no separate launch/connect) | 7 | Simpler agent workflow |
| D-03 | Default port 6007 (matches Godot editor) | 7 | Familiar to Godot developers |
| D-07 | Session model: Claude's discretion (hybrid) | 7 | Self-contained MVP, background server later |
| D-14 | Comprehensive Variant codec (25+ of 39 types) | 7 | Future-proof for game state inspection |
| D-15 | Golden byte tests vs Godot's var_to_bytes() | 7 | Catches encoding bugs round-trip tests miss |

## 6. Tech Debt & Deferred Items

### Known Tech Debt (from v1.1 audit)

- **COMPAT-03 test gap:** No unit test exercises `parse_tscn()` with a `format=4` header. Implementation is correct; gap is test coverage only.
- **BACK-01 E2E limitation:** E2E tests run against whatever Godot binary is on PATH (>= 4.5). No fixture specifically tests against 4.5.x separately. Acknowledged design limitation.
- **ROADMAP.md stale entry:** v1.0 progress table had stale Phase 5 status (cosmetic only).

### v2.0 Known Risks and Concerns

- **Variant encoding byte alignment:** Silent message drops with no diagnostic from Godot if encoding is wrong.
- **Bridge script cleanup on crash:** Orphaned autoload entries could corrupt user's project.godot.
- **Input injection timing:** Events queue for next frame; immediate assertions are flaky.
- **Scene tree response binary layout:** Undocumented by Godot; needs empirical reverse-engineering.

### Deferred to Future Milestones

- Visual observation and Computer Use integration (VISUAL-01, VISUAL-02)
- Replay/record gameplay sessions (AUTO-01)
- Signal monitoring (AUTO-02)
- Custom GDScript expression evaluation (AUTO-03)
- Multi-instance debugger (AUTO-04)
- RL/ML pipeline scaffolding (RLML-01, RLML-02)
- Particle/shader generation (PARTICLE-01, SHADER-01)
- Full Tiled .tmx map-to-TileMap conversion (basic tileset extraction done)

## 7. Getting Started

### Installation

```bash
# Clone and install
git clone <repo-url> && cd gdauto
uv sync              # core dependencies
uv sync --extra image  # optional: Pillow for atlas/split commands
```

### Run the Project

```bash
gdauto --help                          # see all command groups
gdauto project info                    # inspect a Godot project
gdauto sprite import-aseprite --help   # core feature
gdauto resource inspect <file.tres>    # dump any .tres/.tscn as JSON
```

### Key Directories

| Path | Purpose |
|------|---------|
| `src/gdauto/cli.py` | CLI entry point, command group registration |
| `src/gdauto/formats/` | Custom .tscn/.tres parser, value types, project.godot parser |
| `src/gdauto/sprite/` | Aseprite import, sprite split, atlas creation |
| `src/gdauto/tileset/` | TileSet builder, terrain peering, Tiled import |
| `src/gdauto/scene/` | Scene list/create commands |
| `src/gdauto/backend.py` | Godot binary discovery and headless invocation |
| `src/gdauto/commands/` | CLI command definitions (one file per group) |
| `src/gdauto/errors.py` | Error hierarchy (GdautoError with code/fix/to_dict) |
| `src/gdauto/output.py` | Output abstraction (emit/emit_error, --json switching) |
| `tests/` | 683 tests (unit + E2E with @pytest.mark.requires_godot) |

### Tests

```bash
uv run pytest                                  # all unit tests
uv run pytest -m requires_godot                # E2E tests (needs Godot on PATH)
uv run pytest tests/test_sprite_import.py -v   # specific module
```

### Where to Look First

1. `src/gdauto/cli.py` -- command registration pattern (add_command for each group)
2. `src/gdauto/formats/parser.py` -- the custom .tscn/.tres parser (core infrastructure)
3. `src/gdauto/sprite/aseprite.py` -- Aseprite import pipeline (core value)
4. `src/gdauto/commands/sprite.py` -- CLI command wiring pattern

---

## Stats

- **Timeline:** 2026-03-27 to 2026-03-29 (v1.0 + v1.1); v2.0 planning started 2026-03-29
- **Phases:** 6 complete / 10 total (4 remaining in v2.0)
- **Plans:** 20 complete / 20 executed (v1.0: 16, v1.1: 4)
- **Commits:** 144 total
- **Files changed:** 192 (+38,961 / -32)
- **Source code:** 7,708 lines across 8 command groups, 28 commands
- **Tests:** 683 test functions
- **Contributors:** Noah Peloquin, wundrfull
- **Requirements:** 61 validated (v1.0: 50, v1.1: 11), 19 pending (v2.0)
