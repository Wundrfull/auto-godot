---
phase: 07-variant-codec-and-tcp-connection
plan: 02
subsystem: debugger
tags: [asyncio, tcp, protocol, variant, framing, session]

# Dependency graph
requires:
  - phase: 07-variant-codec-and-tcp-connection (plan 01)
    provides: Variant binary encoder/decoder (encode/decode functions)
provides:
  - Protocol message framing (encode_message, decode_message, read_message, write_message)
  - Async TCP session with background recv loop (DebugSession class)
  - Future-based command/response dispatch
  - Output/error message buffering with cap
affects: [07-03, debug-connect, debug-commands]

# Tech tracking
tech-stack:
  added: []
  patterns: [length-prefixed wire framing, asyncio TCP server with recv loop, Future-based RPC dispatch, capped message buffering]

key-files:
  created:
    - src/gdauto/debugger/protocol.py
    - src/gdauto/debugger/session.py
    - tests/unit/test_protocol.py
    - tests/unit/test_session.py
  modified: []

key-decisions:
  - "8 MiB max message size to catch protocol desynchronization early"
  - "Output/error buffers capped at 1000 entries with oldest-first eviction"
  - "Performance messages (arriving ~60/sec) silently discarded in recv loop"
  - "send_command uses asyncio.Future keyed by command name for response dispatch"
  - "DebugSession uses dataclass with port=0 support for OS-assigned ports in tests"

patterns-established:
  - "Wire framing: 4-byte LE length prefix + Variant-encoded 3-element Array [command, thread_id, data]"
  - "Async session lifecycle: start() -> wait_for_connection() -> send_command() -> close()"
  - "Mock TCP client pattern: asyncio.open_connection + encode_message for session testing"

requirements-completed: [PROTO-02, PROTO-03]

# Metrics
duration: 5min
completed: 2026-04-05
---

# Phase 7 Plan 2: Protocol and Session Summary

**Length-prefixed Variant wire framing and async TCP session with background recv loop, Future-based command dispatch, and capped output/error buffering**

## Performance

- **Duration:** 5 min
- **Started:** 2026-04-06T05:08:50Z
- **Completed:** 2026-04-06T05:13:34Z
- **Tasks:** 2
- **Files created:** 4

## Accomplishments
- Protocol layer correctly frames messages as 4-byte LE length prefix + 3-element Variant Array per Godot debugger wire format
- DebugSession accepts TCP connections, runs background recv_loop that continuously drains messages to prevent game buffer flooding
- send_command provides clean Future-based RPC with timeout handling
- Full test coverage: 19 protocol tests + 15 session tests (34 new tests, 171 total with variant)

## Task Commits

Each task was committed atomically:

1. **Task 1: Protocol message framing** - `9e9d0f9` (feat)
2. **Task 2: Async TCP session with background recv loop** - `a52bae7` (feat)

## Files Created/Modified
- `src/gdauto/debugger/protocol.py` - Message framing: encode_message, decode_message, read_message, write_message
- `src/gdauto/debugger/session.py` - Async TCP session: DebugSession with start, recv_loop, send_command, close
- `tests/unit/test_protocol.py` - 19 tests for wire format, round-trip, validation, size limits, async I/O
- `tests/unit/test_session.py` - 15 tests for lifecycle, connection, dispatch, buffering, timeouts, disconnection

## Decisions Made
- 8 MiB max message size catches protocol desync before memory exhaustion
- Output/error buffers capped at 1000 with oldest-first eviction balances memory use with debug utility
- Performance messages discarded without buffering since they carry profiling data irrelevant to debug commands
- send_command keys pending Futures by command name (simple, works for Godot's request/response model where commands have unique names)
- DebugSession supports port=0 for OS-assigned ports, enabling parallel test execution without port conflicts

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None - all functionality is fully wired.

## Next Phase Readiness
- Protocol framing and session management are complete; plan 07-03 (debug connect CLI command, game launch integration) can build directly on these
- DebugSession.start() + wait_for_connection() + send_command() provides the full API surface for higher-level debug commands
- Zero new pip dependencies added (all stdlib: asyncio, struct, socket, logging)

## Self-Check: PASSED

- [x] src/gdauto/debugger/protocol.py exists
- [x] src/gdauto/debugger/session.py exists
- [x] tests/unit/test_protocol.py exists
- [x] tests/unit/test_session.py exists
- [x] Commit 9e9d0f9 exists (Task 1: protocol framing)
- [x] Commit a52bae7 exists (Task 2: session with recv loop)

---
*Phase: 07-variant-codec-and-tcp-connection*
*Completed: 2026-04-05*
