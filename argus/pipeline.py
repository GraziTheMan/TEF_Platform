"""
Classification pipeline — the glue for the first slice.

Scans configured vault directories for markdown, classifies each document,
allocates a TEF document ID, and (when applying) writes the TEF frontmatter
schema into the file and records a credit contribution in the store.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from . import frontmatter
from .classify import Classifier
from .config import Config
from .models import Classification, Contribution, today
from .store import Store

_H1 = re.compile(r"^#\s+(.+)$", re.MULTILINE)
# Generic headings that aren't real titles.
_GENERIC_TITLES = {"summary", "overview", "introduction", "abstract", "contents"}


def _clean_title(raw: str) -> str:
    return raw.strip().strip("*").strip().strip("#").strip()

# Filename markers → originating AI collaborator (for credit).
_AI_MARKERS = {
    "opus": "FractiClaude (Opus)", "claude": "FractiClaude",
    "grok": "FractiGrok", "deepseek": "FractiDeepSeek",
    "fractigpt": "FractiGPT", "gpt": "FractiGPT", "gemini": "FractiGemini",
}


@dataclass
class PlanItem:
    classification: Classification
    contributor: str
    originating_ai: str


def _title_of(path: Path, fm: dict, body: str) -> str:
    if fm.get("title"):
        return str(fm["title"])
    # First non-generic H1 heading.
    for m in _H1.finditer(body):
        title = _clean_title(m.group(1))
        if title and title.lower() not in _GENERIC_TITLES:
            return title
    return path.stem


def _git_author(vault: Path, path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(vault), "log", "-1", "--format=%an", "--", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        name = out.stdout.strip()
        return name or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _detect_ai(filename: str) -> str:
    low = filename.lower()
    for marker, name in _AI_MARKERS.items():
        if marker in low:
            return name
    return ""


class Pipeline:
    def __init__(self, config: Config, classifier: Classifier, store: Store):
        self.config = config
        self.classifier = classifier
        self.store = store

    def _iter_files(self):
        for d in self.config.ingest_dirs:
            root = self.config.vault_path / d
            if not root.exists():
                continue
            for p in sorted(root.rglob("*.md")):
                yield p

    def plan(self) -> list[PlanItem]:
        items: list[PlanItem] = []
        for path in self._iter_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            fm, body = frontmatter.split(text)
            title = _title_of(path, fm, body)
            c = self.classifier.classify(path, title, body)
            if not c.document_id:                       # non-seed: allocate
                c.document_id = self.store.allocate_id(c.domain_primary)
            contributor = _git_author(self.config.vault_path, path)
            originating_ai = _detect_ai(path.name)
            items.append(PlanItem(c, contributor, originating_ai))
        return items

    def apply(self, items: list[PlanItem]) -> None:
        for item in items:
            c = item.classification
            path = Path(c.source_path)
            text = path.read_text(encoding="utf-8", errors="replace")
            existing_fm, body = frontmatter.split(text)
            fm = _build_frontmatter(existing_fm, c, item.originating_ai)
            frontmatter.write(path, fm, body)
            self.store.upsert_document(c)
            self.store.record_contribution(Contribution(
                document_id=c.document_id, source_path=c.source_path,
                contributor=item.contributor, action="classified",
                tier=c.tier, domain=c.domain_primary,
                originating_ai=item.originating_ai,
            ))


def _build_frontmatter(existing: dict, c: Classification, ai: str) -> dict:
    """Merge Argus fields into any existing frontmatter (TEF §2.4 schema)."""
    from .taxonomy import TIERS
    fm = dict(existing)
    fm.update({
        "document_id": c.document_id,
        "title": c.title,
        "lore_tier": c.tier,
        "lore_tier_name": TIERS[c.tier].name,
        "domain_primary": c.domain_primary,
        "domain_secondary": c.domain_secondary,
        "development_status": c.development_status,
        "originating_ai": ai or existing.get("originating_ai", ""),
        "resonance_council_status": existing.get("resonance_council_status", "pending"),
        "consistency_status": existing.get("consistency_status", "pending"),
        "classification_method": c.method,
        "classification_confidence": c.confidence,
        "classification_flags": c.flags,
        "date_classified": today(),
    })
    return fm
