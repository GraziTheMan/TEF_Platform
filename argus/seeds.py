"""
Seed data — known TEF entities with fixed IDs and tiers.

From TEF-ARGUS-001 §11 (Genesis Record Ingestion). When a source file
clearly corresponds to one of these, the classifier assigns the canonical
ID/tier directly rather than guessing. Matching is by lowercase substring
against the filename and/or title.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Seed:
    document_id: str
    tier: str
    domain: str
    title: str
    # substrings (lowercase) that identify this entity in a filename/title
    match: tuple[str, ...]


# §11.1 Core Canon (T1) + §11.2 Draft dormant threads (T3) + §11.3 Influence (IL)
SEEDS: list[Seed] = [
    # ── T1 Core Canon ──
    Seed("TEF-CHAR-001", "T1", "CHAR", "Joe Corvin", ("joe corvin",)),
    Seed("TEF-CHAR-002", "T1", "CHAR", "Rob Corvin", ("rob corvin",)),
    Seed("TEF-CHAR-003", "T1", "CHAR", "Barnaby 'Wavelength' Finch",
         ("barnaby", "wavelength finch")),
    Seed("TEF-CHAR-004", "T1", "CHAR", "Kreg", ("kreg",)),
    Seed("TEF-CHAR-005", "T1", "CHAR", "GLYPH", ("glyph",)),
    Seed("TEF-CHAR-006", "T1", "CHAR", "General Squeakerton", ("squeakerton",)),
    Seed("TEF-TECH-001", "T1", "TECH", "Composite Superorganism Swarm (CSS)",
         ("composite superorganism", "css (")),
    Seed("TEF-ABIL-001", "T1", "ABIL", "Phase Shifting", ("phase shifting", "phase-shift")),
    Seed("TEF-META-001", "T1", "META", "Thought-Responsive Reality (TRR)",
         ("thought-responsive", "trr")),
    Seed("TEF-META-002", "T1", "META", "Consciousness as substrate-independent",
         ("substrate-independent", "consciousness bridge")),
    Seed("TEF-FACT-001", "T1", "FACT", "The Mechanists", ("mechanists",)),
    Seed("TEF-LOC-001", "T1", "LOC", "The Ether", ("the ether",)),
    Seed("TEF-EVNT-001", "T1", "EVNT", "The Cataclysm / Reset Event",
         ("cataclysm", "reset event")),

    # ── Master/index docs → Meta-Canon or Core codex ──
    # Matches only the master Core Codex (versioned), not the template or the
    # story-specific codices (e.g. Ashen Winter), which get their own IDs.
    Seed("TEF-C0-CODEX", "T1", "META", "TEF Core Codex", ("core codex v1",)),
    Seed("TEF-C0-NEXUS", "T0", "META", "TEF Core Nexus", ("corenexus", "core nexus")),

    # ── IL Influence Library ──
    Seed("IL-SCI-002", "IL", "SPEC", "Holobiont theory", ("holobiont",)),
]


def match_seed(filename: str, title: str = "") -> Seed | None:
    """Return the first seed whose match tokens appear in filename or title."""
    hay = f"{filename}\n{title}".lower()
    for seed in SEEDS:
        if any(tok in hay for tok in seed.match):
            return seed
    return None
