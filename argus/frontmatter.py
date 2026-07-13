"""
YAML frontmatter read/write for markdown files.

Argus writes the TEF frontmatter schema (TEF-ARGUS-001 §2.4) to the top
of each vault document. This module keeps parsing/serialization in one
place and never destroys existing body content.
"""

from __future__ import annotations

import io
from pathlib import Path

import yaml

_DELIM = "---"


def split(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Empty dict if no frontmatter."""
    if not text.startswith(_DELIM):
        return {}, text
    lines = text.splitlines()
    # find closing delimiter
    for i in range(1, len(lines)):
        if lines[i].strip() == _DELIM:
            raw = "\n".join(lines[1:i])
            body = "\n".join(lines[i + 1:])
            try:
                data = yaml.safe_load(raw) or {}
            except yaml.YAMLError:
                data = {}
            if not isinstance(data, dict):
                data = {}
            return data, body.lstrip("\n")
    return {}, text


def _dump(data: dict) -> str:
    buf = io.StringIO()
    yaml.safe_dump(data, buf, sort_keys=False, allow_unicode=True,
                   default_flow_style=False, width=100)
    return buf.getvalue()


def render(frontmatter: dict, body: str) -> str:
    return f"{_DELIM}\n{_dump(frontmatter)}{_DELIM}\n\n{body.lstrip(chr(10))}"


def read(path: Path) -> tuple[dict, str]:
    return split(path.read_text(encoding="utf-8"))


def write(path: Path, frontmatter: dict, body: str) -> None:
    path.write_text(render(frontmatter, body), encoding="utf-8")
