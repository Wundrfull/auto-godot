---
phase: 07-variant-codec-and-tcp-connection
plan: 03
subsystem: debugger
tags: [asyncio, tcp, subprocess, click, cli]

# Dependency graph
requires:
  - phase: 07-01
    provides: Variant binary codec (encode/decode), error hierarchy, models
  - phase: 07-02
    provides: Protocol message framing, DebugSession async TCP server
provides:
  - GodotBackend.launch_game() for non-blocking game subprocess with --remote-debug
  - async_connect() workflow orchestrating TCP server, game launch, and readiness polling
  - ConnectResult dataclass with to_dict() for structured JSON output
  - gdauto debug connect CLI command with --project, --port, --scene, --timeout
  - Full error handling for port-in-use, missing project, game crash, scene not ready
affects: [08-scene-tree-queries, 09-input-injection, 10-e2e-workflow]

# Tech tracking
tech-stack:
  added: []
  patterns: [asyncio.run() at Click boundary, non-blocking subprocess.Popen for game lifecycle]

key-files:
  created:
    - src/gdauto/debugger/connect.py
    - src/gdauto/commands/debug.py
    - tests/unit/test_backend_launch.py
    - tests/unit/test_debug_connect.py
    - tests/unit/test_debug_cli.py
  modified:
    - src/gdauto/backend.py
    - src/gdauto/debugger/__init__.py
    - src/gdauto/cli.py

key-decisions:
  - "asyncio.run() used at Click boundary; async_connect is fully async internally"
  - "Readiness polling uses exponential backoff (0.5s to 16s, 6 retries) for scene tree"
  - "launch_game() uses Popen (not run) and omits --headless for windowed game"

patterns-established:
  - "Async-to-sync bridge: asyncio.run() in Click commands wrapping async workflows"
  - "Cleanup pattern: try/finally in async_connect ensures session.close() and process.terminate()"
  - "Error codes: DEBUG_NO_PROJECT, DEBUG_PORT_IN_USE, DEBUG_GAME_CRASHED, DEBUG_SCENE_NOT_READY"

requirements-completed: [PROTO-04, PROTO-05]

# Metrics
duration: 8min
completed: 2026-04-06
---

# Phase 7 Plan 3: Debug Connect Command Summary

**Game launch via subprocess.Popen with --remote-debug, async connect workflow with readiness polling, and gdauto debug connect CLI command**

## Performance

- **Duration:** 8 min
- **Started:** 2026-04-06T05:21:20Z
- **Completed:** 2026-04-06T05:29:28Z
- **Tasks:** 2
- **Files modified:** 8

## Accomplishments
- GodotBackend.launch_game() launches game as non-blocking subprocess with --remote-debug flag (no --headless)
- async_connect() orchestrates full lifecycle: validate project, start TCP server, launch game, wait for connection, poll scene tree readiness, cleanup on failure
- `gdauto debug connect` CLI command with --project, --port, --scene, --timeout options, --json output, and structured error reporting
- 19 new tests (5 backend launch, 5 connect workflow, 9 CLI) all passing; 882 total tests pass with zero regressions

## Task Commits

Each task was committed atomically:

1. **Task 1: GodotBackend.launch_game() and connect workflow** - `72a32b1` (feat)
2. **Task 2: CLI debug command group and connect command** - `07f9a5a` (feat)

## Files Created/Modified
- `src/gdauto/backend.py` - Added launch_game() method using subprocess.Popen with --remote-debug
- `src/gdauto/debugger/connect.py` - ConnectResult dataclass and async_connect() workflow
- `src/gdauto/debugger/__init__.py` - Updated with public exports for connect module
- `src/gdauto/commands/debug.py` - debug group and connect subcommand with asyncio.run() bridge
- `src/gdauto/cli.py` - Registered debug command group
- `tests/unit/test_backend_launch.py` - 5 tests for launch_game() args, port, scene, no-headless
- `tests/unit/test_debug_connect.py` - 5 tests for ConnectResult, no-project, port-in-use, crash, cleanup
- `tests/unit/test_debug_cli.py` - 9 tests for help, options, JSON output, error codes, registration

## Decisions Made
- asyncio.run() at Click boundary per D-02 (connect is one combined command, not separate launch/connect)
- Readiness polling with exponential backoff (6 retries, 0.5s to 16s) to handle variable game startup times
- launch_game() deliberately omits --headless since the game needs its window for visual output

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed backend test fixture to bypass version check**
- **Found during:** Task 1 (test_backend_launch.py)
- **Issue:** Setting binary_path alone does not skip the version check in ensure_binary(), causing subprocess.run to fail on a fake path
- **Fix:** Set _version cache on the backend fixture to skip the check, matching the existing test_backend.py pattern
- **Files modified:** tests/unit/test_backend_launch.py
- **Verification:** All 5 backend launch tests pass
- **Committed in:** 72a32b1 (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor test fixture fix. No scope creep.

## Issues Encountered
- Worktree was behind main branch (missing Wave 1 and 2 commits); resolved with git merge
- pytest not installed in worktree venv; resolved with uv pip install

## Known Stubs
None. All functionality is fully wired.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Full Phase 7 infrastructure is now complete: Variant codec, protocol framing, TCP session, connect workflow, and CLI command
- Ready for Phase 8 (scene tree queries) which will use send_command("scene:request_scene_tree") through the established session
- The debug connect command is the entry point for all subsequent live interaction features

## Self-Check: PASSED

All 8 created/modified files verified present. Both task commits (72a32b1, 07f9a5a) verified in git log. 882 tests pass with zero regressions.

---
*Phase: 07-variant-codec-and-tcp-connection*
*Completed: 2026-04-06*
