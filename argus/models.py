"""Core data models: classification results and contribution/credit records."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime


@dataclass
class Classification:
    """Result of classifying one document."""
    source_path: str
    document_id: str
    title: str
    tier: str                       # T0/T1/T2/T3/T4/IL
    domain_primary: str             # CHAR/FACT/...
    domain_secondary: list[str] = field(default_factory=list)
    development_status: str = "active"
    confidence: float = 0.0
    method: str = "heuristic"       # heuristic | llm | seed
    flags: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Contribution:
    """A credit record: who contributed which document, and how."""
    document_id: str
    source_path: str
    contributor: str                # git author / handle / AI collaborator
    action: str                     # created | edited | classified | reviewed
    tier: str
    domain: str
    originating_ai: str = ""        # FractiGemini | FractiClaude | ... | human
    commit: str = ""                # git sha if known
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))


def today() -> str:
    return date.today().isoformat()
