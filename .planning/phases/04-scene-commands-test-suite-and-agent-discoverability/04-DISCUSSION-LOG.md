# Phase 4: Scene Commands, Test Suite, and Agent Discoverability - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md -- this log preserves the alternatives considered.

**Date:** 2026-03-28
**Phase:** 04-scene-commands-test-suite-and-agent-discoverability
**Areas discussed:** Scene definition format, E2E test strategy, SKILL.md generation, Scene list output

---

## Scene Definition Format

| Option | Description | Selected |
|--------|-------------|----------|
| JSON file input | Pass a .json file describing the node tree. Consistent with Aseprite JSON input pattern. | x |
| CLI flags for simple trees | gdauto scene create --root Node2D --child Sprite2D:player. Quick but limited. | |
| Both JSON and flags | JSON for complex, flags for simple. More implementation work. | |
| You decide | Claude picks the approach. | |

**User's choice:** JSON file input
**Notes:** Consistent with Aseprite import pattern established in Phase 2.

| Option | Description | Selected |
|--------|-------------|----------|
| Core properties only | Node type, name, children, script path, common properties. | |
| Full property passthrough | Any property as key-value pairs, serialized directly to .tscn. | x |
| You decide | Claude picks the right depth. | |

**User's choice:** Full property passthrough
**Notes:** Supports every Godot node type without hardcoding property lists.

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, via res:// paths | Generate ext_resource entries for any res:// path in JSON. | |
| Scripts only | Support script attachment but not other resources. | |
| You decide | Claude picks based on parser capabilities. | x |

**User's choice:** You decide (Claude's discretion)
**Notes:** Claude will decide based on existing parser capabilities.

---

## E2E Test Strategy

| Option | Description | Selected |
|--------|-------------|----------|
| Skip with pytest marker | @pytest.mark.requires_godot skips when no Godot binary. | x |
| Separate test directory | tests/e2e/ distinct from tests/unit/. | |
| Both marker and directory | Directory separation AND graceful skip. | |

**User's choice:** Skip with pytest marker
**Notes:** CI installs Godot for full suite. Local devs still run 587+ unit tests.

| Option | Description | Selected |
|--------|-------------|----------|
| All resource types | SpriteFrames, TileSet, and .tscn scenes in headless Godot. | x |
| SpriteFrames and TileSets only | Focus on .tres resources. | |
| You decide | Claude picks based on risk assessment. | |

**User's choice:** All resource types

| Option | Description | Selected |
|--------|-------------|----------|
| Committed fixtures | Known-good files in tests/fixtures/golden/. Byte-for-byte compare. | x |
| Generated on first run | First run creates, subsequent runs compare. --update-golden to refresh. | |
| You decide | Claude picks. | |

**User's choice:** Committed fixtures
**Notes:** Explicit, reviewable in PRs.

---

## SKILL.md Generation

| Option | Description | Selected |
|--------|-------------|----------|
| Auto-generated from Click introspection | Runtime command walks Click tree. Always in sync. | x |
| Build-time generation | Hatchling hook during package build. | |
| You decide | Claude picks. | |

**User's choice:** Auto-generated from Click introspection

| Option | Description | Selected |
|--------|-------------|----------|
| Structured markdown with tables | Command groups as headers, commands in table rows. | |
| YAML-like structured blocks | Each command as structured block. | |
| You decide | Claude picks what works best for LLM consumption. | x |

**User's choice:** You decide (Claude's discretion)

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, one example per command | Concrete usage example per command. | x |
| No, just signatures | Command name, arguments, options only. | |
| You decide | Claude picks. | |

**User's choice:** Yes, one example per command

---

## Scene List Output

| Option | Description | Selected |
|--------|-------------|----------|
| Full tree by default | Complete node hierarchy. --depth N to limit. | x |
| Root nodes only by default | Just scenes with root node type. --tree to expand. | |
| Two levels by default | Root plus direct children. --tree for full. | |

**User's choice:** Full tree by default

| Option | Description | Selected |
|--------|-------------|----------|
| Comprehensive | File path, root type, node count, scripts, resources, sub-scenes. | x |
| Essential only | File path, root type, node count. --verbose for more. | |
| You decide | Claude picks. | |

**User's choice:** Comprehensive

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, show dependency graph | Detect PackedScene references across all .tscn files. | x |
| No, per-scene only | List each scene independently. | |
| You decide | Claude picks. | |

**User's choice:** Yes, show dependency graph

---

## Claude's Discretion

- SKILL.md format (structured markdown vs YAML blocks)
- External resource reference support in scene create (res:// paths)
- Scene JSON schema details
- E2E test fixture design
- Golden file comparison/normalization logic
- Scene list human output format (tree rendering style)

## Deferred Ideas

None -- discussion stayed within phase scope.
