"""
Heuristic (no-LLM) classifier.

Implements the deterministic parts of the TEF classification decision tree
(TEF-ARGUS-001 §2.3): tier inference from provenance/authority signals and
domain inference from the §2.2 keyword signals. Runs with zero model
dependency so the vault can be classified before Ollama is installed.

When an Ollama backend is available, the Classifier uses the LLM instead and
falls back to this only on failure.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..models import Classification
from ..seeds import match_seed
from ..taxonomy import DOMAINS

# Filename / title signals for tier inference.
_META_SIGNALS = ("argus", "genesis", "corenexus", "core nexus", "codextemplate",
                 "template", "council", "charter", "protocol", "collaboration")
_STORY_SIGNALS = ("poopwars", "poop wars", "pw_", "homecoming", "ashenwinter",
                  "storycodex", "story_", "chapter", "rebellion", "arc")
_INFLUENCE_SIGNALS = ("holobiont", "wikipedia", "arxiv", "et al", "doi:")
_ESTABLISHED_SIGNALS = ("tefcores_", "expansion", "ec_", "metaphysicslore",
                        "abilitymechanism", "storyarc")

# Detect prose-heavy story content by dialogue density.
_DIALOGUE_RE = re.compile(r'[""].{2,}?[""]|"[^"]{4,}?"')


def _score_domains(text: str) -> list[tuple[str, int]]:
    low = text.lower()
    scored: list[tuple[str, int]] = []
    for dom_id, dom in DOMAINS.items():
        hits = sum(low.count(sig) for sig in dom.signals)
        if hits:
            scored.append((dom_id, hits))
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored


def _infer_tier(filename: str, title: str, body: str) -> tuple[str, str, str]:
    """Return (tier, development_status, reason)."""
    hay = f"{filename} {title}".lower()
    if any(s in hay for s in _INFLUENCE_SIGNALS):
        return "IL", "stable", "matched influence-library signal"
    if any(s in hay for s in _META_SIGNALS):
        return "T0", "stable", "matched meta/governance signal"
    # Dialogue-dense body → story content
    dialogue_hits = len(_DIALOGUE_RE.findall(body))
    if any(s in hay for s in _STORY_SIGNALS) or dialogue_hits >= 8:
        return "T4", "active", f"story signal / dialogue density={dialogue_hits}"
    if any(s in hay for s in _ESTABLISHED_SIGNALS):
        return "T2", "stable", "matched established-lore (Core) signal"
    return "T3", "active", "default: unreviewed draft"


def classify(path: Path, title: str, body: str) -> Classification:
    filename = path.name
    src = str(path)

    # 1) Known-entity seed match wins outright.
    seed = match_seed(filename, title)
    if seed:
        return Classification(
            source_path=src, document_id=seed.document_id, title=title or seed.title,
            tier=seed.tier, domain_primary=seed.domain, development_status="stable",
            confidence=0.95, method="seed",
            reasons=[f"seed match: {seed.match}"],
        )

    # 2) Tier from provenance/authority signals.
    tier, status, tier_reason = _infer_tier(filename, title, body)

    # 3) Domain from keyword signals (title + body).
    scored = _score_domains(f"{title}\n{title}\n{body}")
    if scored:
        domain_primary = scored[0][0]
        secondary = [d for d, _ in scored[1:3]]
        total = sum(h for _, h in scored)
        confidence = round(min(0.9, 0.45 + scored[0][1] / max(total, 1) * 0.45), 2)
        dom_reason = f"top signals: {scored[:3]}"
    else:
        domain_primary = "META"
        secondary = []
        confidence = 0.25
        dom_reason = "no domain signals; defaulted to META"

    flags = [] if scored else ["low_confidence_domain"]
    if tier == "T3":
        flags.append("needs_review")

    return Classification(
        source_path=src, document_id="", title=title or path.stem,
        tier=tier, domain_primary=domain_primary, domain_secondary=secondary,
        development_status=status, confidence=confidence, method="heuristic",
        flags=flags, reasons=[tier_reason, dom_reason],
    )
