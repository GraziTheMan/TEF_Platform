"""
Classifier orchestration.

Prefers the LLM backend when reachable (richer reasoning over the full
decision tree); otherwise falls back to the deterministic heuristic. Either
way it returns a `Classification`. Document-ID allocation is left to the
caller (the pipeline), which owns the counter in the store.
"""

from __future__ import annotations

import json
from pathlib import Path

from ..llm.base import LLMClient
from ..models import Classification
from ..taxonomy import DOMAINS, TIERS
from . import heuristic


class Classifier:
    def __init__(self, llm: LLMClient | None = None, prompt_path: Path | None = None):
        self.llm = llm
        self.prompt_path = prompt_path
        self._template: str | None = None

    def _prompt(self) -> str:
        if self._template is None and self.prompt_path and self.prompt_path.exists():
            self._template = self.prompt_path.read_text(encoding="utf-8")
        return self._template or ""

    def classify(self, path: Path, title: str, body: str) -> Classification:
        # Seeds and the no-LLM path both live in the heuristic module; run it
        # first so a seed match short-circuits regardless of LLM availability.
        base = heuristic.classify(path, title, body)
        if base.method == "seed":
            return base
        if self.llm is not None and self.llm.available() and self._prompt():
            llm_result = self._classify_llm(path, title, body)
            if llm_result is not None:
                return llm_result
        return base

    def _classify_llm(self, path: Path, title: str, body: str) -> Classification | None:
        excerpt = body[:6000]
        prompt = self._prompt().replace("{{TITLE}}", title).replace("{{CONTENT}}", excerpt)
        res = self.llm.generate(prompt, format_json=True)
        if not res.ok or not res.text.strip():
            return None
        try:
            data = json.loads(res.text)
        except (ValueError, TypeError):
            return None
        tier = str(data.get("tier", "")).upper()
        domain = str(data.get("domain_primary", "")).upper()
        if tier not in TIERS or domain not in DOMAINS:
            return None
        confidence = float(data.get("confidence", 0.6))
        flags = list(data.get("flags", []))
        if confidence < 0.4:
            flags.append("low_confidence")
        if tier == "T3":
            flags.append("needs_review")
        return Classification(
            source_path=str(path),
            document_id="",
            title=title or path.stem,
            tier=tier,
            domain_primary=domain,
            domain_secondary=[d.upper() for d in data.get("domain_secondary", [])
                              if str(d).upper() in DOMAINS],
            development_status=data.get("development_status", "active"),
            confidence=confidence,
            method="llm",
            flags=flags,
            reasons=[data.get("reason", "llm classification")],
        )
