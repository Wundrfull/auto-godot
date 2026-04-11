"""GDScript documentation extractor.

Regex-based declaration extraction from .gd files. Produces structured
dicts for JSON output and Markdown for human-readable docs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Regex patterns for GDScript declarations
_CLASS_NAME = re.compile(r"^class_name\s+(\w+)")
_EXTENDS = re.compile(r"^extends\s+(\w+)")
_SIGNAL = re.compile(r"^signal\s+(\w+)(?:\(([^)]*)\))?")
_CONST = re.compile(r"^const\s+(\w+)(?:\s*:\s*\w+)?\s*=\s*(.+)")
_EXPORT = re.compile(r"^@export(?:_\w+(?:\([^)]*\))?)?\s+var\s+(\w+)\s*(?::\s*([^=]+?))?\s*(?:=\s*(.+))?$")
_VAR = re.compile(r"^var\s+(\w+)\s*(?::\s*([^=]+?))?\s*(?:=\s*(.+))?$")
_FUNC = re.compile(r"^(static\s+)?func\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(\w+))?")
_ENUM_START = re.compile(r"^enum\s+(\w+)\s*\{(.*)")
_DOC_COMMENT = re.compile(r"^##\s?(.*)")


def _collect_doc(lines: list[str], end: int) -> str:
    """Collect consecutive ## lines above index end (exclusive)."""
    parts: list[str] = []
    i = end - 1
    while i >= 0:
        m = _DOC_COMMENT.match(lines[i].strip())
        if m:
            parts.append(m.group(1))
            i -= 1
        else:
            break
    parts.reverse()
    return "\n".join(parts).strip()


def _parse_enum_values(lines: list[str], start: int, initial: str) -> list[str]:
    """Parse enum values from braces, handling multi-line."""
    combined = initial
    i = start + 1
    while "}" not in combined and i < len(lines):
        combined += " " + lines[i].strip()
        i += 1
    body = combined.split("}", 1)[0]
    return [v.strip() for v in body.split(",") if v.strip()]


@dataclass
class ScriptDoc:
    """Documentation extracted from a single GDScript file."""
    path: str
    class_name: str | None = None
    extends: str | None = None
    description: str = ""
    signals: list[dict[str, Any]] = field(default_factory=list)
    constants: list[dict[str, Any]] = field(default_factory=list)
    enums: list[dict[str, Any]] = field(default_factory=list)
    exports: list[dict[str, Any]] = field(default_factory=list)
    variables: list[dict[str, Any]] = field(default_factory=list)
    functions: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"path": self.path}
        if self.class_name:
            result["class_name"] = self.class_name
        if self.extends:
            result["extends"] = self.extends
        if self.description:
            result["description"] = self.description
        for key in ("signals", "constants", "enums", "exports", "variables", "functions"):
            items = getattr(self, key)
            if items:
                result[key] = items
        return result


def parse_gdscript(text: str, file_path: str = "") -> ScriptDoc:
    """Parse a GDScript file and extract documentation."""
    doc = ScriptDoc(path=file_path)
    lines = text.split("\n")

    # File-level doc comment (## lines before class_name/extends)
    file_doc: list[str] = []
    for line in lines:
        stripped = line.strip()
        m = _DOC_COMMENT.match(stripped)
        if m:
            file_doc.append(m.group(1))
        elif stripped == "":
            if file_doc:
                break
        else:
            break
    doc.description = "\n".join(file_doc).strip()

    i = 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        top = raw == s or raw == ""

        if top and (m := _CLASS_NAME.match(s)):
            doc.class_name = m.group(1)
        elif top and (m := _EXTENDS.match(s)):
            doc.extends = m.group(1)
        elif top and (m := _ENUM_START.match(s)):
            vals = _parse_enum_values(lines, i, m.group(2))
            entry: dict[str, Any] = {"name": m.group(1), "values": vals, "line": i + 1}
            comment = _collect_doc(lines, i)
            if comment:
                entry["doc"] = comment
            doc.enums.append(entry)
        elif top and (m := _SIGNAL.match(s)):
            entry = {"name": m.group(1), "signature": s, "line": i + 1}
            comment = _collect_doc(lines, i)
            if comment:
                entry["doc"] = comment
            doc.signals.append(entry)
        elif top and (m := _CONST.match(s)):
            entry = {"name": m.group(1), "signature": s, "line": i + 1}
            comment = _collect_doc(lines, i)
            if comment:
                entry["doc"] = comment
            doc.constants.append(entry)
        elif top and (m := _EXPORT.match(s)):
            entry = {"name": m.group(1), "signature": s, "line": i + 1}
            comment = _collect_doc(lines, i)
            if comment:
                entry["doc"] = comment
            doc.exports.append(entry)
        elif top and (m := _VAR.match(s)):
            entry = {"name": m.group(1), "signature": s, "line": i + 1}
            comment = _collect_doc(lines, i)
            if comment:
                entry["doc"] = comment
            doc.variables.append(entry)
        elif top and (m := _FUNC.match(s)):
            entry = {
                "name": m.group(2), "params": m.group(3).strip(),
                "return_type": m.group(4) or "void", "line": i + 1,
            }
            if m.group(1):
                entry["static"] = True
            comment = _collect_doc(lines, i)
            if comment:
                entry["doc"] = comment
            doc.functions.append(entry)
        i += 1
    return doc


def format_markdown(sd: ScriptDoc) -> str:
    """Format a ScriptDoc as Markdown."""
    p: list[str] = []
    title = sd.class_name or Path(sd.path).stem
    p.append(f"# {title}\n")
    if sd.extends:
        p.append(f"**Extends:** `{sd.extends}`\n")
    if sd.description:
        p.append(sd.description + "\n")
    if sd.signals:
        p.append("## Signals\n")
        for sig in sd.signals:
            p.append(f"### `{sig['signature']}`\n")
            if sig.get("doc"):
                p.append(sig["doc"] + "\n")
    if sd.enums:
        p.append("## Enums\n")
        for en in sd.enums:
            p.append(f"### {en['name']}\n")
            if en.get("doc"):
                p.append(en["doc"] + "\n")
            for val in en["values"]:
                p.append(f"- `{val}`")
            p.append("")
    if sd.constants:
        p.append("## Constants\n")
        for c in sd.constants:
            line = f"- `{c['signature']}`"
            if c.get("doc"):
                line += f"\n  {c['doc']}"
            p.append(line + "\n")
    if sd.exports:
        p.append("## Exported Properties\n")
        p.append("| Name | Declaration | Description |")
        p.append("|------|-------------|-------------|")
        for exp in sd.exports:
            doc_cell = exp.get("doc", "").replace("\n", " ")
            p.append(f"| {exp['name']} | `{exp['signature']}` | {doc_cell} |")
        p.append("")
    if sd.variables:
        p.append("## Variables\n")
        for v in sd.variables:
            line = f"- `{v['signature']}`"
            if v.get("doc"):
                line += f"\n  {v['doc']}"
            p.append(line + "\n")
    if sd.functions:
        p.append("## Functions\n")
        for fn in sd.functions:
            static = "static " if fn.get("static") else ""
            p.append(f"### `{static}func {fn['name']}({fn['params']}) -> {fn['return_type']}`\n")
            if fn.get("doc"):
                p.append(fn["doc"] + "\n")
    return "\n".join(p).rstrip() + "\n"
