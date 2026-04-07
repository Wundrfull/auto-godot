"""Session file persistence for .gdauto/session.json.

Manages writing, reading, and cleaning up the session file that tracks
active debugger connections. Also ensures .gdauto/ is in .gitignore
to prevent committing session state (D-04).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from gdauto.debugger.models import SessionInfo

logger = logging.getLogger(__name__)

_GDAUTO_DIR = ".gdauto"
_SESSION_FILE = "session.json"
_GITIGNORE_ENTRY = ".gdauto/"


def write_session_file(project_path: Path, info: SessionInfo) -> None:
    """Write session info to .gdauto/session.json.

    Creates the .gdauto/ directory if needed and ensures .gdauto/
    is listed in .gitignore.
    """
    gdauto_dir = project_path / _GDAUTO_DIR
    gdauto_dir.mkdir(exist_ok=True)
    session_path = gdauto_dir / _SESSION_FILE
    session_path.write_text(json.dumps(info.to_dict(), indent=2) + "\n")
    _ensure_gitignore(project_path)


def read_session_file(project_path: Path) -> SessionInfo | None:
    """Read session info from .gdauto/session.json.

    Returns None if the file does not exist or contains invalid data.
    """
    session_path = project_path / _GDAUTO_DIR / _SESSION_FILE
    if not session_path.exists():
        return None
    try:
        data = json.loads(session_path.read_text())
        return SessionInfo.from_dict(data)
    except (json.JSONDecodeError, TypeError, KeyError) as exc:
        logger.debug("Invalid session file, ignoring: %s", exc)
        return None


def cleanup_session(project_path: Path) -> None:
    """Remove session.json and .gdauto/ directory if empty."""
    session_path = project_path / _GDAUTO_DIR / _SESSION_FILE
    if session_path.exists():
        session_path.unlink()
    gdauto_dir = project_path / _GDAUTO_DIR
    if gdauto_dir.exists() and not any(gdauto_dir.iterdir()):
        gdauto_dir.rmdir()


def _ensure_gitignore(project_path: Path) -> None:
    """Ensure .gdauto/ is listed in .gitignore.

    Creates .gitignore if it does not exist. Appends .gdauto/ if not
    already present. Adds a leading newline if the file does not end
    with one.
    """
    gitignore_path = project_path / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text(_GITIGNORE_ENTRY + "\n")
        return
    content = gitignore_path.read_text()
    # Check if already present (line-level match)
    for line in content.splitlines():
        if line.strip() == _GITIGNORE_ENTRY:
            return
    # Append entry, ensuring a newline separator
    prefix = "" if content.endswith("\n") else "\n"
    gitignore_path.write_text(content + prefix + _GITIGNORE_ENTRY + "\n")
