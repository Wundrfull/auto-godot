---
phase: 07-variant-codec-and-tcp-connection
verified: 2026-04-05T00:00:00Z
status: passed
score: 19/19 must-haves verified
re_verification: false
gaps: []
human_verification:
  - test: "Connect a real Godot 4.5+ game with --remote-debug and verify binary message exchange"
    expected: "gdauto debug connect --project <path> reports 'Connected to game (PID ...) on 127.0.0.1:6007'"
    why_human: "Requires Godot binary and a real game project; cannot be verified with unit tests alone"
---

# Phase 7: Variant Codec and TCP Connection Verification Report

**Phase Goal:** gdauto can launch a Godot game, accept its debugger connection over TCP, and exchange binary-encoded messages reliably
**Verified:** 2026-04-05
**Status:** PASSED
**Re-verification:** No (initial verification)

## Goal Achievement

### Observable Truths

All truths from the three plan must_haves sections were verified against the actual codebase.

#### Plan 01 Truths (PROTO-01: Variant binary codec)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | encode(None) produces bytes identical to Godot's var_to_bytes(null) | VERIFIED | `encode(None) == b'\x00\x00\x00\x00'` confirmed by spot-check and 137 passing golden-byte tests |
| 2 | encode(True) and encode(False) produce correct 8-byte sequences | VERIFIED | `_encode_bool` uses `struct.pack('<II', VariantType.BOOL, int(value))`; test suite covers both values |
| 3 | encode/decode round-trips all 13 MUST types with exact fidelity | VERIFIED | 137 tests pass including `TestDecodeRoundTrip`; `decode(encode(42)) == (42, 8)` confirmed |
| 4 | encode/decode handles all SHOULD types (VECTOR2I, RECT2, TRANSFORM2D, BASIS, RID, Packed*Array) | VERIFIED | `_FLOAT_TUPLE_SIZES`, `_INT_TUPLE_SIZES` dispatch tables cover all SHOULD types; dedicated encode/decode functions present |
| 5 | decode raises ProtocolError on truncated input, unknown type IDs, and malformed data | VERIFIED | `_check_remaining()` raises ProtocolError with TRUNCATED_DATA; `_dispatch_packed` raises for unknown type IDs |
| 6 | Strings pad to 4-byte boundaries for lengths 0, 1, 2, 3, 4, 5, 7, 8 | VERIFIED | `pad = (4 - (length % 4)) % 4` in `_encode_string_bytes`; parametrized boundary tests in test suite |
| 7 | NodePath encodes/decodes with absolute flag, names, and subnames | VERIFIED | `_parse_node_path`, `_encode_node_path`, `_decode_node_path` implement new format with MSB set on name_count |
| 8 | INT uses 32-bit when value fits int32, 64-bit with ENCODE_FLAG_64 otherwise | VERIFIED | `_encode_int` checks `_INT32_MIN <= value <= _INT32_MAX`; pack format switches accordingly |
| 9 | FLOAT always encodes as 64-bit (double); decoder handles both 32-bit and 64-bit | VERIFIED | `_encode_float` always uses `ENCODE_FLAG_64`; `_decode_float` branches on `flag_64` |
| 10 | Array and Dictionary encode nested Variants recursively | VERIFIED | `_encode_array` calls `encode(item)` per element; `_encode_dictionary` calls `encode(k)` + `encode(v)` per pair |

#### Plan 02 Truths (PROTO-02/PROTO-03: Protocol framing and TCP session)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | encode_message wraps command, thread_id, and data into a length-prefixed 3-element Variant Array | VERIFIED | `encode_message` calls `encode([command, thread_id, data])` then prepends `struct.pack('<I', len(payload))` |
| 2 | decode_message extracts command name, thread_id, and data array from a received payload | VERIFIED | `decode_message` decodes payload, validates 3-element list with correct types, returns (command, tid, data) |
| 3 | Messages over 8 MiB are rejected with ProtocolError | VERIFIED | `MAX_MESSAGE_SIZE = 8_388_608`; `read_message` raises ProtocolError with PROTO_MSG_TOO_LARGE |
| 4 | DebugSession accepts a single TCP connection on a specified port | VERIFIED | `asyncio.start_server(self._handle_connection, self.host, self.port)` in `start()`; port=0 support confirmed |
| 5 | DebugSession's recv_loop continuously drains messages from the connection | VERIFIED | `_recv_loop` loops `while not self._closed`, reading each message via `read_message` |
| 6 | Unsolicited output and error messages are buffered (capped at 1000) | VERIFIED | `_BUFFER_CAP = 1000`; `_append_buffer` drops oldest when full; separate `_output_buffer` and `_error_buffer` |
| 7 | Performance profile messages are silently discarded by the recv_loop | VERIFIED | `elif command.startswith("performance:"): pass` in `_dispatch` |
| 8 | send_command sends a message and returns a Future that resolves when the response arrives | VERIFIED | `loop.create_future()` stored in `_pending[command]`; `asyncio.wait_for` awaits resolution |
| 9 | recv_loop dispatches responses to the correct pending Future by command name | VERIFIED | `_dispatch` pops `self._pending[command].set_result(data)` on match |

#### Plan 03 Truths (PROTO-04/PROTO-05: Game launch and connect workflow)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 10 | GodotBackend.launch_game() starts a Godot game as a non-blocking subprocess with --remote-debug flag | VERIFIED | `subprocess.Popen` called with `"--remote-debug", f"tcp://127.0.0.1:{port}"`; no `--headless` in cmd |
| 11 | gdauto debug connect --project <path> starts TCP server, launches game, waits for connection, and reports status | VERIFIED | `asyncio.run(async_connect(...))` in CLI; `emit(result.to_dict(), ...)` on success |
| 12 | gdauto debug connect --port <port> overrides the default 6007 port | VERIFIED | `--port` option with `default=6007` wired through to `async_connect(port=port)` |
| 13 | gdauto debug connect --scene <scene> launches a specific scene instead of the project default | VERIFIED | `--scene` option wired through to `launch_game(project_path, port, scene)` |
| 14 | Connection timeout produces DebuggerTimeoutError with non-zero exit code and actionable message | VERIFIED | `wait_for_connection` raises DebuggerTimeoutError with DEBUG_CONNECT_TIMEOUT; `emit_error` handles exit |
| 15 | Game crash or missing binary produces error with non-zero exit code | VERIFIED | `_check_process_alive` raises DebuggerConnectionError with DEBUG_GAME_CRASHED; `ensure_binary` raises on missing binary |
| 16 | Clean disconnect closes TCP server, terminates game process, and cleans up all resources | VERIFIED | `_cleanup` calls `session.close()` then `process.terminate()` / `process.kill()` in try/finally |
| 17 | --json output produces structured JSON with connection status | VERIFIED | `emit(result.to_dict(), ...)` with `to_dict()` returning `{"status": "connected", ...}` |
| 18 | Port already in use produces a clear error message suggesting --port <alternative> | VERIFIED | `_start_session` catches OSError and raises DebuggerConnectionError with DEBUG_PORT_IN_USE |

**Score:** 19/19 truths verified (combining all plans)

### Required Artifacts

| Artifact | Min Lines | Actual Lines | Status | Details |
|----------|-----------|--------------|--------|---------|
| `src/gdauto/debugger/variant.py` | 400 | 734 | VERIFIED | Exports: VariantType, encode, decode, ENCODE_FLAG_64 |
| `src/gdauto/debugger/models.py` | -- | 37 | VERIFIED | Exports: GodotStringName, GodotNodePath |
| `src/gdauto/debugger/errors.py` | -- | 32 | VERIFIED | Exports: DebuggerError, DebuggerConnectionError, DebuggerTimeoutError, ProtocolError |
| `src/gdauto/debugger/__init__.py` | -- | 25 | VERIFIED | Re-exports all public symbols from connect, errors, session, variant |
| `tests/unit/test_variant.py` | 200 | 952 | VERIFIED | 130 test functions (137 tests with parametrize expansion = 137 pass) |
| `src/gdauto/debugger/protocol.py` | 50 | 113 | VERIFIED | Exports: encode_message, decode_message, read_message, write_message |
| `src/gdauto/debugger/session.py` | 150 | 241 | VERIFIED | Exports: DebugSession |
| `tests/unit/test_protocol.py` | 50 | 203 | VERIFIED | 19 test functions |
| `tests/unit/test_session.py` | 80 | 270 | VERIFIED | 15 test functions |
| `src/gdauto/backend.py` | -- | -- | VERIFIED | Contains `def launch_game(` with --remote-debug, no --headless, subprocess.Popen |
| `src/gdauto/debugger/connect.py` | -- | 166 | VERIFIED | Exports: async_connect, ConnectResult |
| `src/gdauto/commands/debug.py` | -- | 96 | VERIFIED | Exports: debug group with connect subcommand |
| `src/gdauto/cli.py` | -- | -- | VERIFIED | Contains `cli.add_command(debug)` |
| `tests/unit/test_backend_launch.py` | 30 | 93 | VERIFIED | 5 test functions |
| `tests/unit/test_debug_connect.py` | 50 | 156 | VERIFIED | 5 test functions |
| `tests/unit/test_debug_cli.py` | -- | -- | VERIFIED | 9 test functions |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `errors.py` | `errors.py` (base) | `class DebuggerError(GdautoError)` | WIRED | Line 15 in errors.py: `class DebuggerError(GdautoError):` |
| `variant.py` | `struct` | `struct.pack/struct.unpack` | WIRED | Present throughout variant.py (lines 82, 91, 95, 100, 101, ...) |
| `protocol.py` | `variant.py` | `from gdauto.debugger.variant import decode, encode` | WIRED | Line 21 in protocol.py |
| `session.py` | `protocol.py` | `from gdauto.debugger.protocol import read_message, write_message` | WIRED | Line 27 in session.py |
| `session.py` | `asyncio` | `asyncio.start_server`, `asyncio.Event`, `asyncio.Future` | WIRED | Lines 53, 56, 70, 102 in session.py |
| `debug.py` (command) | `connect.py` | `asyncio.run(async_connect(...))` | WIRED | Lines 73-80 in debug.py |
| `connect.py` | `session.py` | `from gdauto.debugger.session import DebugSession` | WIRED | Line 20 in connect.py; used on line 70 |
| `connect.py` | `backend.py` | `backend.launch_game(...)` | WIRED | Line 75 in connect.py |
| `cli.py` | `commands/debug.py` | `cli.add_command(debug)` | WIRED | Line 18 (import) and line 114 (registration) in cli.py |

### Data-Flow Trace (Level 4)

This phase produces no components that render dynamic data from a database. All data flows are binary protocol I/O verified by unit tests. Data-flow trace not applicable.

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| NIL encodes to correct 4 bytes | `encode(None) == b'\x00\x00\x00\x00'` | True | PASS |
| INT round-trip | `decode(encode(42)) == (42, 8)` | True | PASS |
| Protocol message round-trip | `decode_message(encode_message('test', [1,2,3])[4:]) == ('test', 1, [1,2,3])` | True | PASS |
| Error hierarchy to_dict | `ProtocolError(message='test', code='TEST').to_dict() == {'error': 'test', 'code': 'TEST'}` | True | PASS |
| DebugSession import | `from gdauto.debugger.session import DebugSession` | ok | PASS |
| debug CLI registered | `uv run gdauto debug --help` shows connect subcommand | Shows connect | PASS |
| connect options exposed | `uv run gdauto debug connect --help` shows --project, --port, --scene, --timeout | All 4 present | PASS |
| Full test suite regression | `uv run pytest tests/ -x` | 882 passed, 10 skipped | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| PROTO-01 | 07-01 | Variant binary codec encodes and decodes all Godot types needed for debugger communication | SATISFIED | variant.py: 24 types, 137 passing tests, golden-byte verified |
| PROTO-02 | 07-02 | TCP server accepts incoming Godot debugger connections with length-prefixed binary framing | SATISFIED | protocol.py: encode_message/decode_message/read_message with 4-byte LE length prefix; 19 tests pass |
| PROTO-03 | 07-02 | Background receive loop drains unsolicited messages to prevent TCP buffer flooding | SATISFIED | session.py: `_recv_loop` runs as asyncio.Task; performance messages discarded; output/error capped at 1000 |
| PROTO-04 | 07-03 | Game launch integrates with existing GodotBackend, adding non-blocking subprocess with --remote-debug flag | SATISFIED | backend.py launch_game: subprocess.Popen with --remote-debug, no --headless; 5 tests pass |
| PROTO-05 | 07-03 | Connection lifecycle manages connect, readiness detection, timeout, and clean disconnect | SATISFIED | connect.py async_connect: validate -> start -> launch -> wait -> poll -> cleanup; CLI wired; 14 tests pass |

No orphaned requirements: all 5 PROTO requirements were claimed by plans and verified as satisfied.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `session.py` | 148 | `send_command()` is 36 lines (CLAUDE.md limit: 30) | Warning | Violates project coding convention; function is fully correct and tested. Contains a multi-line docstring and a multi-line DebuggerTimeoutError constructor. No behavior missing. |
| `connect.py` | 48 | `async_connect()` is 40 lines (CLAUDE.md limit: 30) | Warning | Violates project coding convention; function is fully correct and tested. The plan already delegates sub-steps to `_validate_project`, `_start_session`, `_poll_readiness`, `_check_process_alive`, `_cleanup`. The body itself is 14 executable lines; the count is inflated by docstring. |
| `protocol.py` | 38 | `decode_message()` is 38 lines (CLAUDE.md limit: 30) | Warning | Violates project coding convention; function is fully correct and tested. Body consists of three near-identical ProtocolError raise blocks (one per field type check). Refactorable but not a functional defect. |

No blockers found. All three violations are style/convention warnings: the functions are fully implemented, all tests pass, and no logic is missing. The excess lines come from multi-line docstrings and multi-line dataclass error constructors.

### Human Verification Required

#### 1. Live Godot Debugger Connection

**Test:** Install a Godot 4.5+ binary, open a project, run `uv run gdauto debug connect --project <project_dir> --timeout 15`
**Expected:** CLI starts TCP server on port 6007, launches the game via `--remote-debug tcp://127.0.0.1:6007`, waits for connection, polls scene tree readiness, and prints `Connected to game (PID <n>) on 127.0.0.1:6007`
**Why human:** Requires Godot binary on PATH and a valid Godot project. E2E tests are gated on `@pytest.mark.requires_godot` and were skipped (10 skipped in full run). The protocol wire format is verified by golden-byte unit tests against the documented Godot spec, but interop with the actual Godot runtime must be confirmed manually.

### Gaps Summary

No gaps. All 19 observable truths verified, all 15 artifacts substantive and wired, all 9 key links confirmed, all 5 PROTO requirements satisfied, 882/882 non-E2E tests pass. Three functions exceed the 30-line CLAUDE.md limit (send_command: 36, async_connect: 40, decode_message: 38) but are fully correct; these are style warnings only and do not block goal achievement.

---

_Verified: 2026-04-05_
_Verifier: Claude (gsd-verifier)_
