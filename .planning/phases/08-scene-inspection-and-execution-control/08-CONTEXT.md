# Phase 8: Scene Inspection and Execution Control - Context

**Gathered:** 2026-04-06
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the scene inspection and execution control commands on top of Phase 7's TCP session and Variant codec. Users can retrieve the live scene tree, read node properties, capture game output, and control execution timing (pause/resume/step/speed). This enables the deterministic testing pattern: pause + inspect + assert. No game state modification in this phase (that's Phase 9).

</domain>

<decisions>
## Implementation Decisions

### Connection Model
- **D-01:** Inspection commands (tree, get, output) auto-connect: launch game and connect if no session exists. Each command is independently runnable without requiring a prior `debug connect`.
- **D-02:** Sessions persist after command completion with an inactivity timeout. Follow-up commands reuse the existing session without relaunching the game.
- **D-03:** Session file lives in the project directory at `.gdauto/session.json`. Visible to agents, easy to discover.
- **D-04:** `.gdauto/` is auto-added to `.gitignore` when a session starts, preventing accidental commits of session state.

### Scene Tree Output
- **D-05:** `debug tree` returns a nested JSON hierarchy mirroring Godot's scene tree structure: `{"name": "Main", "type": "Node2D", "path": "/root/Main", "children": [...]}`.
- **D-06:** Each node includes: type (Node2D, Label, etc.), class_name (if custom script), instance_id (Godot object ID), script_path (attached GDScript, if any), groups (list of group names).
- **D-07:** `debug tree` supports `--depth N` flag to limit tree traversal depth. Default: unlimited.

### Output Capture
- **D-08:** `debug output` defaults to snapshot mode (return buffered output, then exit). `--follow` flag streams continuously (like `tail -f`).
- **D-09:** Claude's Discretion: whether to separate print() from errors (--errors flag) or combine them with a type field in --json output. Claude picks the approach that best serves debugging workflows.

### Execution Control
- **D-10:** Claude's Discretion: whether `debug step` auto-pauses the running game first or requires the game to already be paused. Claude picks based on ergonomics for the agent workflow.
- **D-11:** Claude's Discretion: speed command interface (multiplier flag vs positional argument). Claude picks the most practical approach.
- **D-12:** All execution control commands (pause, resume, step, speed) return current game state in their --json output: `{"paused": true, "speed": 1.0, "frame": 1234}`. Agents always know current state without a separate query.

### Carried Forward from Phase 7
- **D-13:** `--project` flag on subcommands, not global (D-01 from Phase 7).
- **D-14:** Short verb names for commands: tree, get, output, pause, resume, step, speed (D-04 from Phase 7).
- **D-15:** Default port 6007 matching Godot editor (D-03 from Phase 7).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Protocol and Architecture
- `.planning/research/STACK.md` -- Wire protocol format, Variant type IDs, message framing details
- `.planning/research/ARCHITECTURE.md` -- TCP server architecture, session lifecycle, async/sync bridge pattern, command inventory
- `.planning/research/PITFALLS.md` -- 12 critical pitfalls including scene tree response binary layout (undocumented)

### Phase 7 Implementation (build on these)
- `src/gdauto/debugger/session.py` -- DebugSession class: TCP server, recv loop, send_command, output/error buffers
- `src/gdauto/debugger/connect.py` -- async_connect workflow, ConnectResult dataclass
- `src/gdauto/debugger/protocol.py` -- Message framing: encode_message, decode_message, read_message, write_message
- `src/gdauto/debugger/variant.py` -- Variant codec: encode/decode for 24+ Godot types
- `src/gdauto/debugger/errors.py` -- DebuggerError hierarchy: ConnectionError, TimeoutError, ProtocolError, CodecError
- `src/gdauto/commands/debug.py` -- Existing debug CLI group with connect subcommand

### Existing Codebase Patterns
- `src/gdauto/output.py` -- emit()/emit_error() with GlobalConfig for --json switching
- `src/gdauto/errors.py` -- GdautoError base class with code/fix/to_dict()
- `src/gdauto/backend.py` -- GodotBackend with find_binary, validate_version, run_headless, launch_game

### External References
- [Godot SceneDebugger](https://github.com/godotengine/godot/blob/master/scene/debugger/scene_debugger.h) -- Scene tree request/response message types
- [Godot RemoteDebugger](https://github.com/godotengine/godot/blob/master/core/debugger/remote_debugger.cpp) -- Command names for pause, resume, step, speed

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `DebugSession.send_command()` -- Send debugger commands and await responses. Used by all Phase 8 commands.
- `DebugSession.output_buffer` / `DebugSession.error_buffer` -- Already capture game output and errors. `debug output` reads from these.
- `async_connect()` -- Full connect workflow. Phase 8 commands call this for auto-connect.
- `ConnectResult` -- Dataclass with session, process, port. Phase 8 commands use this to access the session.
- `emit()` / `emit_error()` -- JSON/human output switching. All new commands use these.

### Established Patterns
- All CLI commands: `import rich_click as click`, `@click.pass_context`, `GlobalConfig` for --json.
- Error handling: catch domain errors, call `emit_error()`, `ctx.exit(1)`.
- Data models: `@dataclass` with `to_dict()` for JSON serialization.
- Async bridge: `asyncio.run()` at the Click boundary; internal logic is async.

### Integration Points
- `commands/debug.py`: Add tree, get, output, pause, resume, step, speed as subcommands to existing debug group.
- `debugger/session.py`: May need new methods for scene tree parsing, property access, execution control.
- Session persistence: New `.gdauto/session.json` file for session reuse across commands.

</code_context>

<specifics>
## Specific Ideas

- The user confirmed that Claude Code can change game speed retroactively via the CLI during a debug session. This is core to the idle clicker testing workflow: speed up to fast-forward timers, slow down to verify state.
- All execution control commands must return full game state in --json, not just their own result. This eliminates the need for agents to query state separately.

</specifics>

<deferred>
## Deferred Ideas

None -- discussion stayed within phase scope.

</deferred>

---

*Phase: 08-scene-inspection-and-execution-control*
*Context gathered: 2026-04-06*
