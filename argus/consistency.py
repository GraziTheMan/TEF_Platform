"""
Lore Consistency Sentinel — TEF-ARGUS-001 §6.

Checks a document against the established canonical facts
(config/tef_consistency_rules.yaml) and reports contradictions with
severity. Scores into pass | flag | block per the §6.4 thresholds.

This first slice checks against the static rule anchors (the T1/T2 canon
facts). Cross-document contradiction discovery via embeddings is a later
addition once the vector store lands.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .llm.base import LLMClient

SEVERITY_ORDER = {"MINOR": 0, "MODERATE": 1, "MAJOR": 2, "CRITICAL": 3}

# Stage-2 verifier: confirm each candidate is a REAL direct contradiction.
# Filters the false positives a single-shot pass produces on weak local models.
_VERIFY_PROMPT = """A story's established fact and a claim from a new document are below.

ESTABLISHED FACT: {fact}

DOCUMENT CLAIM: {claim}

Does the DOCUMENT CLAIM directly state the OPPOSITE of the ESTABLISHED FACT, so
that both cannot be true at once? Agreement, restatement, a broader/narrower but
compatible term, or an unrelated statement is NOT a contradiction.

Return ONLY JSON: {{"contradicts": true or false}}"""


@dataclass
class Contradiction:
    established_fact: str
    document_claim: str
    severity: str
    explanation: str
    category: str = ""


@dataclass
class ConsistencyResult:
    document_id: str
    source_path: str
    status: str                      # passed | flagged | blocked | error
    verdict: str = "aligned"         # aligned | diverges | contradicts
    contradictions: list[Contradiction] = field(default_factory=list)
    notes: str = ""

    def counts(self) -> dict[str, int]:
        out = {k: 0 for k in SEVERITY_ORDER}
        for c in self.contradictions:
            if c.severity in out:
                out[c.severity] += 1
        return out


def load_rules(path: Path) -> tuple[str, dict[str, str]]:
    """Return (facts_block_for_prompt, {fact_text: default_severity})."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    lines: list[str] = []
    severities: dict[str, str] = {}
    for category, spec in data.items():
        sev = spec.get("default_severity", "MODERATE")
        lines.append(f"\n[{category.upper()} — severity {sev}]")
        for fact in spec.get("facts", []):
            lines.append(f"- {fact}")
            severities[fact.strip().lower()] = sev
    return "\n".join(lines), severities


def _score(contradictions: list[Contradiction]) -> str:
    """§6.4 thresholds."""
    counts = {k: 0 for k in SEVERITY_ORDER}
    for c in contradictions:
        counts[c.severity] = counts.get(c.severity, 0) + 1
    if counts["CRITICAL"] >= 1 or counts["MAJOR"] >= 1:
        return "blocked"
    if counts["MODERATE"] >= 1:
        return "flagged"
    return "passed"


class ConsistencySentinel:
    def __init__(self, llm: LLMClient, rules_path: Path, prompt_path: Path,
                 verify: bool = True):
        self.llm = llm
        self.rules_path = rules_path
        self.prompt_path = prompt_path
        self.verify = verify
        self._facts_block, self._severities = load_rules(rules_path)
        self._template = prompt_path.read_text(encoding="utf-8")

    def _confirm(self, contradiction: "Contradiction") -> bool:
        """Stage-2: focused yes/no verification of one candidate."""
        prompt = _VERIFY_PROMPT.format(fact=contradiction.established_fact,
                                       claim=contradiction.document_claim)
        res = self.llm.generate(prompt, format_json=True)
        if not res.ok or not res.text.strip():
            return True  # fail open: keep candidate for human review
        try:
            return bool(json.loads(res.text).get("contradicts", True))
        except (ValueError, TypeError):
            return True

    def _severity_for(self, fact: str, fallback: str) -> str:
        return self._severities.get((fact or "").strip().lower(), fallback)

    def check(self, document_id: str, title: str, body: str,
              source_path: str = "") -> ConsistencyResult:
        prompt = (self._template
                  .replace("{{FACTS}}", self._facts_block)
                  .replace("{{TITLE}}", title)
                  .replace("{{CONTENT}}", body[:8000]))
        res = self.llm.generate(prompt, format_json=True)
        if not res.ok or not res.text.strip():
            return ConsistencyResult(document_id, source_path, "error",
                                     notes=res.error or "empty LLM response")
        try:
            data = json.loads(res.text)
        except (ValueError, TypeError):
            return ConsistencyResult(document_id, source_path, "error",
                                     notes="unparseable LLM JSON")
        contradictions: list[Contradiction] = []
        for c in data.get("contradictions", []):
            fact = str(c.get("established_fact", ""))
            sev = str(c.get("severity", "")).upper()
            if sev not in SEVERITY_ORDER:
                sev = self._severity_for(fact, "MODERATE")
            else:
                # Trust the rule's own severity over the model's guess.
                sev = self._severity_for(fact, sev)
            contradictions.append(Contradiction(
                established_fact=fact,
                document_claim=str(c.get("document_claim", "")),
                severity=sev,
                explanation=str(c.get("explanation", "")),
            ))
        # Stage 2: verify each candidate; drop the ones that don't survive.
        if self.verify and contradictions:
            contradictions = [c for c in contradictions if self._confirm(c)]
        status = _score(contradictions)
        return ConsistencyResult(
            document_id=document_id, source_path=source_path, status=status,
            verdict=str(data.get("verdict", "aligned")),
            contradictions=contradictions, notes=str(data.get("notes", "")),
        )
