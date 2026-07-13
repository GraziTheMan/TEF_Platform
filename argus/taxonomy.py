"""
TEF taxonomy — Lore Tiers and Content Domains.

Codifies the classification vocabulary from TEF-ARGUS-001 sections 2.1
(Lore Tiers) and 2.2 (Content Domains). Kept as data so both the
heuristic classifier and the LLM prompt draw from one source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Tier:
    id: str            # T0, T1, T2, T3, T4, IL
    key: str           # machine slug
    name: str          # human name
    authority: str
    description: str


@dataclass(frozen=True)
class Domain:
    id: str            # CHAR, FACT, ...
    key: str
    name: str
    prefix: str        # TEF-CHAR, ...
    description: str
    # Lowercase keyword signals used by the heuristic classifier.
    signals: tuple[str, ...] = field(default_factory=tuple)


# ─── Lore Tiers (TEF-ARGUS-001 §2.1) ────────────────────────────────────────
TIERS: dict[str, Tier] = {
    "T1": Tier("T1", "core_canon", "Core Canon", "highest",
               "Foundational, Council-approved lore. Highest authority."),
    "T2": Tier("T2", "established_lore", "Established Lore", "high",
               "Reviewed, integrated content. Consistent and developed."),
    "T3": Tier("T3", "draft_lore", "Draft / Proposed Lore", "provisional",
               "Work in progress, unreviewed, may contain contradictions."),
    "T4": Tier("T4", "story_content", "Story Content", "expressive",
               "Narrative prose/dialogue. Expresses lore, does not define it."),
    "T0": Tier("T0", "meta_canon", "Meta-Canon", "governance",
               "Documents about the project itself: governance, methodology."),
    "IL": Tier("IL", "influence_library", "Influence Library", "reference",
               "External material that informs TEF but is not part of it."),
}

# ─── Content Domains (TEF-ARGUS-001 §2.2) ───────────────────────────────────
DOMAINS: dict[str, Domain] = {
    "CHAR": Domain("CHAR", "character", "Character", "TEF-CHAR",
                   "Character definitions, backstories, abilities, relationships.",
                   ("character profile", "protagonist", "backstory", "personality",
                    "corvin", "barnaby", "kreg", "glyph", "squeakerton")),
    "FACT": Domain("FACT", "faction", "Faction", "TEF-FACT",
                   "Faction definitions, politics, territories, leadership.",
                   ("faction", "mechanists", "alliance", "coalition", "territory",
                    "politics", "leadership", "army", "regime")),
    "META": Domain("META", "metaphysics", "Metaphysics", "TEF-META",
                   "Universe rules, dimensional structure, consciousness, cosmology.",
                   ("consciousness", "metaphysic", "cosmology", "dimension", "reality",
                    "the ether", "substrate", "trr", "thought-responsive", "fibonacci",
                    "phase", "resonance", "universe rules")),
    "TECH": Domain("TECH", "technology", "Technology", "TEF-TECH",
                   "In-universe technologies, augmentations, artifacts.",
                   ("technology", "device", "artifact", "augmentation", "css",
                    "composite superorganism", "mask", "machine", "engineered")),
    "ABIL": Domain("ABIL", "ability", "Ability", "TEF-ABIL",
                   "Character abilities, mechanisms, limitations, evolution.",
                   ("ability", "phase shift", "phase-shift", "power", "mechanism",
                    "asmr", "conduit", "limitation")),
    "LOC": Domain("LOC", "location", "Location", "TEF-LOC",
                  "Places, empirical bubbles, realms, geography.",
                  ("location", "realm", "region", "geography", "akashic", "lima ohio",
                   "place", "bubble", "landscape")),
    "SPEC": Domain("SPEC", "species", "Species", "TEF-SPEC",
                   "Species definitions, biology, culture, hierarchy.",
                   ("species", "angels", "demons", "biology", "organism", "hierarchy",
                    "holobiont", "microbiome", "symbiont")),
    "EVNT": Domain("EVNT", "event", "Event", "TEF-EVNT",
                   "Historical events, the cataclysm, battles, turning points.",
                   ("cataclysm", "reset event", "battle", "war", "ice age", "poop wars",
                    "turning point", "onset", "event")),
    "NARR": Domain("NARR", "narrative", "Narrative", "TEF-NARR",
                   "Story arcs, plot structures, narrative connections, themes.",
                   ("story arc", "saga", "plot", "narrative", "chapter", "homecoming",
                    "rebellion", "theme", "story codex", "poop wars", "expansion core")),
    "CULT": Domain("CULT", "cultural", "Cultural", "TEF-CULT",
                   "In-universe cultural systems, languages, music, timekeeping.",
                   ("culture", "cultural", "language", "music", "timekeeping",
                    "calendar", "ritual", "tradition")),
    "PHIL": Domain("PHIL", "philosophy", "Philosophy", "TEF-PHIL",
                   "Fractiverism principles, PEACE Initiative values, cosmic themes.",
                   ("fractiverism", "peace initiative", "philosophy", "love as",
                    "cosmic theme", "values", "principle")),
}


def tier(id_: str) -> Tier:
    return TIERS[id_]


def domain(id_: str) -> Domain:
    return DOMAINS[id_]
