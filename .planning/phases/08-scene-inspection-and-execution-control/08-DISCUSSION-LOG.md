# Phase 8: Scene Inspection and Execution Control - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md -- this log preserves the alternatives considered.

**Date:** 2026-04-06
**Phase:** 08-scene-inspection-and-execution-control
**Areas discussed:** Connection model, Scene tree output, Output capture mode, Execution control UX

---

## Connection Model

| Option | Description | Selected |
|--------|-------------|----------|
| Auto-connect (Recommended) | Each command launches a game and connects if no session exists | x |
| Session-required | User must run debug connect first | |
| You decide | Claude picks | |

**User's choice:** Auto-connect
**Notes:** Matches the agent workflow where each command should be independently runnable.

| Option | Description | Selected |
|--------|-------------|----------|
| Persist with timeout | Session stays alive after command for follow-up commands | x |
| Disconnect after each command | Each command connects, works, disconnects | |
| You decide | Claude picks | |

**User's choice:** Persist with timeout

| Option | Description | Selected |
|--------|-------------|----------|
| Project directory (.gdauto/session.json) | Visible in project, easy for agents to find | x |
| Temp directory | System temp dir, auto-cleaned, invisible | |
| You decide | Claude picks | |

**User's choice:** Project directory

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, auto-add to .gitignore | Prevents accidental commits | x |
| No, leave to user | User manages .gitignore | |
| You decide | Claude picks | |

**User's choice:** Auto-add to .gitignore

---

## Scene Tree Output

| Option | Description | Selected |
|--------|-------------|----------|
| Nested hierarchy (Recommended) | Mirrors Godot's scene tree with children arrays | x |
| Flat list with paths | Every node as flat array entry | |
| Both (--flat flag) | Default nested, --flat for flat list | |

**User's choice:** Nested hierarchy

**Metadata per node (multiselect):**

| Option | Description | Selected |
|--------|-------------|----------|
| Type and class (Recommended) | Node type and class_name | x |
| Instance ID | Godot's internal object ID | x |
| Groups | Node group membership | x |
| Script path | Path to attached GDScript | x |

**User's choice:** All four metadata fields selected.

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, with --depth flag | debug tree --depth 2 limits traversal | x |
| No depth limiting | Always return full tree | |
| You decide | Claude picks | |

**User's choice:** --depth flag

---

## Output Capture Mode

| Option | Description | Selected |
|--------|-------------|----------|
| Snapshot (Recommended) | Returns buffer contents, then exits | |
| Follow mode with --follow | Default snapshot; --follow streams continuously | x |
| You decide | Claude picks | |

**User's choice:** Follow mode with --follow (snapshot default, --follow for streaming)

| Option | Description | Selected |
|--------|-------------|----------|
| Separate with --errors flag | debug output for print(), --errors for errors, --all for both | |
| Combined with type field | All mixed chronologically with type field in --json | |
| You decide | Claude picks | x |

**User's choice:** Claude's Discretion

---

## Execution Control UX

| Option | Description | Selected |
|--------|-------------|----------|
| Auto-pause then step (Recommended) | debug step pauses automatically if running | |
| Require paused state | Errors if not paused | |
| You decide | Claude picks | x |

**User's choice:** Claude's Discretion

**Speed command:**
User asked about retroactive speed changes. Confirmed: `Engine.time_scale` takes effect immediately on next frame. User deferred interface choice to Claude.

| Option | Description | Selected |
|--------|-------------|----------|
| Yes, include state (Recommended) | All exec commands return {paused, speed, frame} | x |
| Minimal output | Each returns only its specific result | |
| You decide | Claude picks | |

**User's choice:** Include full game state in all execution control --json output

---

## Claude's Discretion

- Output separation strategy (print() vs errors): flag-based or type-field-based
- Step auto-pause behavior
- Speed command interface (multiplier flag vs positional)

## Deferred Ideas

None
