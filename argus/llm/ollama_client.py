"""
Ollama HTTP client.

Talks to a local Ollama server (default http://localhost:11434) via its
REST API. No SDK dependency — just httpx. If Ollama isn't running,
`available()` returns False and callers fall back to the heuristic path.
"""

from __future__ import annotations

import httpx

from .base import LLMResult


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434",
                 model: str = "mistral-nemo:latest", timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def available(self) -> bool:
        try:
            r = httpx.get(f"{self.base_url}/api/tags", timeout=3.0)
            return r.status_code == 200
        except (httpx.HTTPError, OSError):
            return False

    def generate(self, prompt: str, *, system: str | None = None,
                 format_json: bool = False) -> LLMResult:
        payload: dict = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system
        if format_json:
            payload["format"] = "json"
        try:
            r = httpx.post(f"{self.base_url}/api/generate", json=payload,
                           timeout=self.timeout)
            r.raise_for_status()
            data = r.json()
            return LLMResult(text=data.get("response", ""), model=self.model)
        except (httpx.HTTPError, OSError, ValueError) as exc:
            return LLMResult(text="", model=self.model, ok=False, error=str(exc))
