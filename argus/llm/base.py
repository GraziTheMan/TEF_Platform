"""
LLM client protocol.

Any backend (Ollama today; a Claude-API client for the future GitHub-Action
face) implements `generate`. Keeping this narrow means the classifier and
future consistency sentinel never know which model answered.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass
class LLMResult:
    text: str
    model: str
    ok: bool = True
    error: str | None = None


@runtime_checkable
class LLMClient(Protocol):
    def available(self) -> bool:
        """True if the backend is reachable right now."""
        ...

    def generate(self, prompt: str, *, system: str | None = None,
                 format_json: bool = False) -> LLMResult:
        """Run a single completion."""
