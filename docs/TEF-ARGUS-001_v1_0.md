---
title: "TEF-ARGUS-001: ARGUS Multi-Vault Extension for The Extended Fractiverse"
document_type: technical_specification
canon_level: Meta-Canon
version: 1.0
created: 2026-03-11
author: FractiClaude
parent_document: FI-ARGUS-001_v2.0
related_documents:
  - TEF_GenesisRecord_FractiGeminiGen0
  - TEFCores_CoreCodex
  - TEF_CoreNexus
tags:
  - argus
  - infrastructure
  - ontology
  - lore-management
  - meta-canon
  - multi-vault
neo4j_entity_type: TechnicalSpecification
---

# TEF-ARGUS-001: ARGUS Multi-Vault Extension
## Lore-Aware Knowledge Infrastructure for The Extended Fractiverse
**Document ID:** TEF-ARGUS-001
**Version:** 1.0
**Date:** March 2026
**Parent Spec:** FI-ARGUS-001 v2.0 (Argus Daemon Architecture)
**Development Stage:** ☑ Conceptual □ Prototype □ Implementation

> *The Hundred-Eyed Giant opens new eyes.*
> *Same guardian. Wider gaze. Two vaults. One embedding space.*
> *Where science and story share a vector, serendipity follows.*

---

## CHANGELOG

```
v1.0 (2026-03-11) — Initial TEF Extension Specification
  ADDED: Multi-vault architecture overview
  ADDED: TEF Lore Classification system (Section 2.0)
  ADDED: TEF Canon Governance Firewall Matrix (Section 3.0)
  ADDED: TEF Role Taxonomy for Influence Library (Section 4.0)
  ADDED: TEF Search Domains for Inspiration Scout (Section 5.0)
  ADDED: Lore Consistency Sentinel specification (Section 6.0)
  ADDED: Fractiverse State Report template (Section 7.0)
  ADDED: Cross-vault discovery architecture (Section 8.0)
  ADDED: TEF vault structure (Section 9.0)
  ADDED: TEF-specific Telegram commands (Section 10.0)
  ADDED: Seed data specification referencing Genesis Record (Section 11.0)
  RATIONALE: The Extended Fractiverse requires the same epistemological
    infrastructure as the Fractality Institute — classification, ontology
    enforcement, consistency checking, reference management — but applied
    to collaborative worldbuilding rather than scientific research. Rather
    than forking ARGUS, this spec extends it as a multi-vault configuration.
```

---

## 0.0 Architecture: One Daemon, Two Vaults

### 0.1 Design Principle

ARGUS was built as a single-user knowledge daemon. TEF extends it to a **single-user, multi-vault** daemon. The PI (Principal Investigator) remains the sole operator. The daemon remains ~3-4K lines of Python. The change is configuration, not architecture.

```
                         ┌─────────────────────┐
                         │      ARGUS DAEMON    │
                         │   (single process)   │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌──────────────┐ ┌───────────┐ ┌──────────────┐
            │  FI VAULT    │ │  SHARED   │ │  TEF VAULT   │
            │  (Science)   │ │  VECTOR   │ │  (Fiction)   │
            │              │ │  SPACE    │ │              │
            │  Canon I-IV  │ │ (ChromaDB)│ │  Lore Tiers  │
            │  _references/│ │           │ │  _influences/│
            └──────────────┘ └───────────┘ └──────────────┘
                    │               ▲               │
                    └───────────────┼───────────────┘
                                    │
                         ┌──────────┴───────────┐
                         │   CROSS-VAULT        │
                         │   DISCOVERY ENGINE   │
                         │   (Section 8.0)      │
                         └──────────────────────┘
```

### 0.2 What Changes, What Stays

```
UNCHANGED (from FI-ARGUS-001 v2.0):
├─ argus.py daemon entry point
├─ telegram_bot.py interface (extended with new commands)
├─ ollama_client.py LLM wrapper
├─ vector_store.py ChromaDB interface (new collections added)
├─ scheduler.py APScheduler cron
├─ Security model (local-first, Tailscale, no cloud dependency)
├─ Hardware requirements
└─ All 7 skill module interfaces

NEW (TEF-specific):
├─ config/tef_lore_classification.yaml    (Section 2.0)
├─ config/tef_firewall_matrix.yaml        (Section 3.0)
├─ config/tef_role_taxonomy.yaml          (Section 4.0)
├─ config/tef_search_domains.yaml         (Section 5.0)
├─ config/tef_consistency_rules.yaml      (Section 6.0)
├─ templates/tef_lore_classifier.txt      (LLM prompt)
├─ templates/tef_consistency_sentinel.txt (LLM prompt)
├─ templates/tef_state_report.txt         (briefing template)
└─ config/argus.yaml → updated with vault_mode: multi
```

### 0.3 Configuration Switch

```yaml
# config/argus.yaml — updated for multi-vault
vault_mode: "multi"   # "single" (FI only) | "multi" (FI + TEF)

vaults:
  fi:
    path: "/path/to/fractality-institute-vault"
    classification_config: "config/fi_canon_classifier.yaml"
    firewall_config: "config/firewall_matrix.yaml"
    role_taxonomy: "config/role_taxonomy.yaml"
    search_domains: "config/search_domains.yaml"
    reference_dir: "_references"
    vector_collection: "fi_vault"

  tef:
    path: "/path/to/extended-fractiverse-vault"
    classification_config: "config/tef_lore_classification.yaml"
    firewall_config: "config/tef_firewall_matrix.yaml"
    role_taxonomy: "config/tef_role_taxonomy.yaml"
    search_domains: "config/tef_search_domains.yaml"
    reference_dir: "_influences"
    vector_collection: "tef_vault"

shared:
  vector_store_path: "/path/to/shared/chromadb"
  embedding_model: "nomic-embed-text"
  cross_vault_discovery: true
  cross_vault_collection: "cross_vault_combined"
```

---

## 1.0 TEF Epistemological Framework

### 1.1 The Problem ARGUS Solves for TEF

The Extended Fractiverse is a collaboratively-built fictional universe with:
- **50+ concept entities** across characters, factions, metaphysical systems, technologies, locations, and narrative arcs (growing rapidly)
- **Multiple Core documents** at different levels of development and authority
- **Dormant threads** identified in the Genesis Record that need tracking
- **Real-world scientific grounding** that must be maintained without being confused for fictional canon
- **Multiple AI collaborators** generating content that needs classification and consistency checking
- **A governance model** (Resonance Council) that requires structured canon elevation

Without infrastructure, this becomes an unmanageable web of Obsidian notes with no systematic way to ensure consistency, track development status, or discover connections.

### 1.2 TEF vs. FI: Parallel Structures

| FI Concept | TEF Equivalent | Shared Principle |
|---|---|---|
| Canon I (Empirical) | Core Canon | Highest-authority content with strictest rules |
| Canon II (Engineering) | Established Lore | Concrete, buildable specifications |
| Canon III (Speculative) | Draft/Proposed Lore | Ideas under development, not yet authoritative |
| Canon IV (Narrative) | Story Content | Creative work that expresses but doesn't define rules |
| Canon 0 (Meta) | Meta-Canon | Governance, methodology, process documents |
| Firewall Principle | Canon Governance Firewall | Rules about what can cite/contradict what |
| PVP Protocol | Lore Consistency Check | Quality gate before content enters canon |
| Reference Library | Influence Library | External material that serves but isn't governed by the system |

---

## 2.0 TEF Lore Classification System

### 2.1 Lore Tiers

The Extended Fractiverse uses a tiered canon system reflecting the Resonance Council governance model:

```yaml
# config/tef_lore_classification.yaml

tiers:
  core_canon:
    id: "T1"
    name: "Core Canon"
    description: >
      Foundational, authoritative lore approved by the Resonance Council.
      Includes the Core Codex, approved Metaphysics & Lore Cores, and
      established character/faction/technology definitions. Changes to
      Core Canon require formal Council review.
    authority: "highest"
    modification_requires: "resonance_council_review"
    examples:
      - "TEFCores_CoreCodex"
      - "Core character definitions (Joe Corvin, Rob Corvin, Barnaby Finch)"
      - "Established universe mechanics (Phase Shifting, CSS, TRR)"

  established_lore:
    id: "T2"
    name: "Established Lore"
    description: >
      Developed, consistent content that has been through at least one
      round of review and integration. Expansion Cores, Story Arc Cores,
      and detailed Ability & Mechanism Cores live here. Can be promoted
      to Core Canon or revised without full Council review.
    authority: "high"
    modification_requires: "author_review_with_consistency_check"
    examples:
      - "Expansion Cores (Choir of Echoing Minds)"
      - "Story Arc Cores (Resonance Rebellion)"
      - "Detailed Ability Cores (Emotional Resonance Physics)"

  draft_lore:
    id: "T3"
    name: "Draft / Proposed Lore"
    description: >
      Work in progress. New ideas, concepts under development, content
      generated in AI collaboration sessions that hasn't been formally
      reviewed. May contain contradictions with established lore. The
      Genesis Record's dormant threads start here.
    authority: "provisional"
    modification_requires: "none (open development)"
    examples:
      - "New character concepts"
      - "Proposed universe mechanics"
      - "AI-generated expansion ideas pending review"
      - "Dormant threads reactivated from Genesis Record"

  story_content:
    id: "T4"
    name: "Story Content"
    description: >
      Narrative prose, dialogue, scene descriptions, and other creative
      writing. Story content EXPRESSES lore but does not DEFINE it —
      a character saying something in dialogue doesn't make it canonical
      unless the underlying claim is separately established. Story content
      can contradict lore for dramatic purposes (unreliable narrator,
      character ignorance, deception).
    authority: "expressive — not definitional"
    modification_requires: "author discretion"
    examples:
      - "Chapter drafts"
      - "Scene writing"
      - "Dialogue scripts"
      - "Poop Wars narrative content"

  meta_canon:
    id: "T0"
    name: "Meta-Canon"
    description: >
      Documents about the project itself — governance, methodology,
      collaboration protocols, foundational records, this specification.
      Meta-Canon governs HOW lore is created and managed but does not
      contain lore itself.
    authority: "governance"
    modification_requires: "pi_approval"
    examples:
      - "TEF-ARGUS-001 (this document)"
      - "TEF Genesis Record"
      - "Resonance Council Charter"
      - "Collaboration guidelines"

  influence_library:
    id: "IL"
    name: "Influence Library"
    description: >
      External material that informs, inspires, or scientifically grounds
      TEF but is NOT part of the fictional universe. Real-world science
      papers, philosophical frameworks, other fiction that influenced TEF
      concepts, cultural references. Serves the lore system but is not
      classified by it.
    authority: "reference — external to canon"
    modification_requires: "n/a (ingestion pipeline)"
    examples:
      - "Physical Review E paper on myelin sheath entanglement"
      - "Holobiont theory (Wikipedia, academic sources)"
      - "Unified Spacememory Network (Haramein)"
      - "God of War Ragnarök (Mask of Loki inspiration)"
```

### 2.2 Content Domain Classification

In addition to the tier (authority level), each piece of content is classified by domain (what kind of lore it is):

```yaml
domains:
  character:
    id: "CHAR"
    description: "Character definitions, backstories, abilities, relationships"
    document_prefix: "TEF-CHAR"
    examples: ["Joe Corvin", "Rob Corvin", "Barnaby Finch", "Kreg", "GLYPH"]

  faction:
    id: "FACT"
    description: "Faction definitions, politics, territories, leadership"
    document_prefix: "TEF-FACT"
    examples: ["The Mechanists", "Probiotic Alliance", "Pathogenic Coalition"]

  metaphysics:
    id: "META"
    description: "Universe rules, dimensional structure, consciousness mechanics, cosmology"
    document_prefix: "TEF-META"
    examples: ["Fibonacci Hierarchy", "Love/Fear Opposition", "TRR", "The Ether"]

  technology:
    id: "TECH"
    description: "In-universe technologies, biological augmentations, artifacts"
    document_prefix: "TEF-TECH"
    examples: ["CSS", "GLYPH (technical specs)", "Evil Mask artifact"]

  ability:
    id: "ABIL"
    description: "Character abilities, mechanisms, limitations, evolution"
    document_prefix: "TEF-ABIL"
    examples: ["Phase Shifting", "ASMR precursor", "Conduit sensitivity"]

  location:
    id: "LOC"
    description: "Places, empirical bubbles, realms, geographical features"
    document_prefix: "TEF-LOC"
    examples: ["The Ether", "Akashic Records subregion", "Lima Ohio (Mechanists)"]

  species:
    id: "SPEC"
    description: "Species definitions, biology, culture, hierarchy"
    document_prefix: "TEF-SPEC"
    examples: ["Angels (emotional hierarchy)", "Demons", "CSS organisms"]

  event:
    id: "EVNT"
    description: "Historical events, the cataclysm, battles, turning points"
    document_prefix: "TEF-EVNT"
    examples: ["The Cataclysm/Reset Event", "Poop Wars", "American Ice Age onset"]

  narrative:
    id: "NARR"
    description: "Story arcs, plot structures, narrative connections, themes"
    document_prefix: "TEF-NARR"
    examples: ["Corvin Saga", "American Homecoming", "Poop Wars saga"]

  cultural:
    id: "CULT"
    description: "In-universe cultural systems, languages, music, timekeeping"
    document_prefix: "TEF-CULT"
    examples: ["Fibonacci music system", "Universal time system"]

  philosophy:
    id: "PHIL"
    description: "Fractiverism principles, PEACE Initiative values, cosmic themes"
    document_prefix: "TEF-PHIL"
    examples: ["Love as fundamental force", "Consciousness as substrate-independent"]
```

### 2.3 Classification Decision Tree

```
INPUT: Raw content (note, chat export, AI collaboration output, draft text)

STEP 0 — Provenance Check
├─ Is this content about the TEF universe (fictional)?
├─ Is this content about the TEF project (governance, methodology)?
├─ Is this external reference material (science, philosophy, other fiction)?
│
├─ EXTERNAL → Route to Influence Library (Skill 7 / TEF track). STOP.
├─ PROJECT → Classify as Meta-Canon (T0). Continue to domain classification.
└─ FICTIONAL → Continue to Step 1.

STEP 1 — Authority Assessment
├─ Has this content been formally reviewed by the Resonance Council?
│   └─ YES → Core Canon (T1)
├─ Has this content been integrated into an existing Core document?
│   └─ YES → Established Lore (T2)
├─ Is this narrative prose, dialogue, or scene writing?
│   └─ YES → Story Content (T4)
├─ Is this new, unreviewed, or under active development?
│   └─ YES → Draft Lore (T3)
└─ UNCERTAIN → FLAG_FOR_REVIEW

STEP 2 — Domain Classification
├─ Extract primary domain from content analysis
├─ Extract secondary domains (if applicable)
├─ Assign document prefix: TEF-[DOMAIN]-[NUMBER]
│
│   DETECTION HEURISTICS:
│   ├─ Names characters, describes personalities/abilities → CHAR
│   ├─ Describes groups, political structures, alliances → FACT
│   ├─ Defines universe rules, dimensional mechanics, cosmology → META
│   ├─ Specifies devices, augmentations, artifacts → TECH
│   ├─ Details how an ability works, its limits, evolution → ABIL
│   ├─ Describes places, realms, geography → LOC
│   ├─ Defines species biology, culture, hierarchy → SPEC
│   ├─ Narrates specific events, battles, turning points → EVNT
│   ├─ Outlines plot structure, story arc, themes → NARR
│   ├─ Describes in-universe cultural practices → CULT
│   └─ Discusses Fractiverism, PEACE values, cosmic themes → PHIL

STEP 3 — Status Tagging
├─ development_status:
│   ├─ "active" — Currently being worked on
│   ├─ "stable" — Complete for now, not under revision
│   ├─ "dormant" — Conceived but not developed (Genesis Record threads)
│   ├─ "deprecated" — Superseded by newer content
│   └─ "contradicted" — Conflicts with higher-tier canon
│
├─ genesis_record_thread: [thread ID if traceable to Gen 0 conversation]
├─ originating_ai: [which AI collaborator generated/co-created this]
└─ resonance_council_status: "pending" | "reviewed" | "approved" | "rejected"
```

### 2.4 Output Format — TEF YAML Frontmatter

```yaml
---
document_id: "TEF-[DOMAIN]-[NUMBER]"
title: "[Title]"
lore_tier: [T0 | T1 | T2 | T3 | T4 | IL]
lore_tier_name: "[Meta-Canon | Core Canon | Established Lore | Draft | Story Content | Influence Library]"
domain_primary: "[CHAR | FACT | META | TECH | ABIL | LOC | SPEC | EVNT | NARR | CULT | PHIL]"
domain_secondary: []
development_status: "[active | stable | dormant | deprecated | contradicted]"
genesis_record_thread: "[thread ID or null]"
originating_ai: "[FractiGemini | FractiClaude | FractiGrok | FractiGrazi | collaborative]"
resonance_council_status: "[pending | reviewed | approved | rejected | n/a]"
cross_tier_dependencies:
  - tier: "[T1/T2/T3/T4]"
    document: "[TEF-XXX-NNN]"
    nature: "[Expands | Depends on | Contradicts | Inspired by]"
influence_library_links: []
consistency_status: "[pending | passed | flagged | n/a]"
related_cores:
  - "[Core document wiki-links]"
keywords: []
date_ingested: "YYYY-MM-DD"
date_created: "YYYY-MM-DD"
source: "[telegram | github | obsidian | chat-export | manual | genesis-record]"
---
```

---

## 3.0 TEF Canon Governance Firewall Matrix

### 3.1 Principle

> *Content at higher authority tiers cannot be contradicted by content at lower tiers without explicit review. Story Content can express divergence from lore (unreliable narrators, character ignorance) but cannot REDEFINE lore. The Influence Library informs everything but governs nothing.*

### 3.2 Firewall Matrix

```yaml
# config/tef_firewall_matrix.yaml
#
# Reading: Row = SOURCE document tier, Column = TARGET document tier
# The cell defines what happens when SOURCE wants to reference/link to TARGET
#
# ✓ = auto-link (no restrictions)
# ⚠ = link with context note (e.g., "Draft content referencing Core Canon")
# ✗ = blocked — requires human review before link is created
# ➡ = one-directional (source can reference target, not vice versa)

firewall_matrix:
  #                 T1:Core  T2:Estab  T3:Draft  T4:Story  T0:Meta  IL:Influence
  T1_core_canon:    ["✓",    "✓",      "✗",      "➡",      "✓",     "✓"]
  T2_established:   ["⚠",    "✓",      "⚠",      "➡",      "✓",     "✓"]
  T3_draft:         ["✗",    "⚠",      "✓",      "✓",      "✓",     "✓"]
  T4_story:         ["➡",    "➡",      "✓",      "✓",      "⚠",     "⚠"]
  T0_meta:          ["✓",    "✓",      "✓",      "✓",      "✓",     "✓"]
  IL_influence:     ["✓",    "✓",      "✓",      "⚠",      "✓",     "✓"]
```

### 3.3 Firewall Rules Explained

```yaml
rules:
  core_cannot_depend_on_draft:
    description: >
      Core Canon (T1) CANNOT reference or depend on Draft (T3) content.
      If a T1 document needs a concept that only exists in T3, the T3
      content must be promoted to T2 or T1 first.
    action: "BLOCK — route to _review/ with promotion suggestion"
    rationale: >
      Core Canon is the foundation. It cannot rest on unreviewed material.

  core_to_story_is_one_directional:
    description: >
      Core Canon (T1) can be EXPRESSED by Story Content (T4), but Story
      Content cannot REDEFINE Core Canon. A character can say something
      wrong about how Phase Shifting works — that doesn't change the
      Ability Core.
    action: "AUTO-LINK with ➡ directional marker"
    rationale: >
      Stories serve the lore; they don't override it.

  draft_referencing_core_is_blocked:
    description: >
      Draft (T3) content claiming to modify or contradict Core Canon (T1)
      is blocked until reviewed. This prevents unreviewed AI-generated
      content from silently undermining established worldbuilding.
    action: "BLOCK — route to _review/ with contradiction analysis"
    rationale: >
      The most common failure mode: an AI collaboration session generates
      an exciting idea that accidentally breaks something fundamental.

  established_referencing_core_needs_context:
    description: >
      Established Lore (T2) referencing Core Canon (T1) is permitted
      but flagged with a context note, because T2 content should be
      CONSISTENT with T1, and the link should be verified.
    action: "AUTO-LINK with ⚠ consistency check note"

  influence_to_story_needs_context:
    description: >
      When Influence Library entries (real science) are linked to Story
      Content (T4), a context note clarifies the epistemic boundary:
      this is INSPIRATION, not an in-universe fact.
    action: "AUTO-LINK with ⚠ note: 'Real-world reference, not in-universe'"

  meta_can_link_anything:
    description: >
      Meta-Canon (T0) documents like the Genesis Record, this spec, and
      governance documents can reference any tier without restriction.
    action: "AUTO-LINK — no restrictions"
```

### 3.4 Contradiction Handling

```
WHEN: Consistency Sentinel detects contradiction between two documents

IF both are same tier:
  → Flag for author review. Neither takes automatic precedence.

IF higher tier contradicts lower tier:
  → Higher tier prevails. Lower tier flagged as "contradicted."
  → Options: revise lower, deprecate lower, or request Council review
     to revise the higher tier document.

IF lower tier contradicts higher tier:
  → Lower tier BLOCKED from vault commit.
  → Route to _review/ with: contradiction analysis, suggested resolution,
     option to submit as formal canon revision proposal.

IF Story Content (T4) contradicts Core Canon (T1):
  → NOT automatically flagged as error.
  → Tagged with: "narrative_divergence: [intentional | unverified]"
  → If marked intentional: no action (unreliable narrator, etc.)
  → If unverified: route to _review/ for author to confirm intent.
```

---

## 4.0 TEF Role Taxonomy (Influence Library)

The Influence Library is TEF's equivalent of the FI Reference Library. It catalogs external material — real science, philosophy, other fiction, cultural references — that inspires, grounds, or challenges TEF's worldbuilding.

```yaml
# config/tef_role_taxonomy.yaml

# ─── Scientific Grounding Roles ───
scientific_grounding:
  description: "Real-world science that makes a TEF concept plausible"
  valid_for_tiers: [T1, T2, T3]
  priority: "STANDARD"
  examples:
    - "Holobiont theory → CSS plausibility"
    - "Myelin sheath entanglement paper → consciousness mechanism"
    - "Quantum coherence in biology → Ethereal Realm mechanics"

scientific_tension:
  description: "Real-world science that challenges or complicates a TEF concept"
  valid_for_tiers: [T1, T2, T3]
  priority: "HIGH — flagged in state report"
  examples:
    - "Decoherence timescales challenging quantum consciousness models"
    - "Thermodynamics constraints on CSS energy harvesting"
  note: >
    These are GOLD for TEF. They force the worldbuilding to get smarter.
    Either the lore adapts (making it more plausible) or the tension
    becomes an acknowledged soft-SF handwave (which is fine, but should
    be explicit).

# ─── Philosophical Roles ───
philosophical_parallel:
  description: "External philosophy structurally similar to Fractiverism"
  valid_for_tiers: [T1, T2, T3]
  examples:
    - "Panpsychism → consciousness as fundamental property"
    - "Process philosophy (Whitehead) → universe as becoming"
    - "Ubuntu philosophy → interconnectedness"

philosophical_foundation:
  description: "Established philosophical tradition that Fractiverism builds upon"
  valid_for_tiers: [T1, T2, T3]
  examples:
    - "Eastern philosophy of Yin and Yang → Duality concept"
    - "Fibonacci/sacred geometry traditions → dimensional hierarchy"

# ─── Creative Roles ───
creative_seed:
  description: "Sparked a concept — NOT evidence for any lore claim"
  valid_for_tiers: [T3, T4]
  note: "CANNOT be used as justification for Core Canon (T1) claims"
  examples:
    - "God of War Ragnarök Mask of Loki → Evil Mask artifact"
    - "TMNT sewer lair → Silas/Barnaby underground setting (deprecated)"
    - "Lichen biology → CSS composite organism concept"

narrative_precedent:
  description: "Existing fiction that handles a structurally similar concept"
  valid_for_tiers: [T2, T3, T4]
  examples:
    - "Venom symbiote → CSS host-symbiont dynamics"
    - "Star Trek's Trill → consciousness across substrates"
    - "His Dark Materials daemons → human-entity bonding"
  note: >
    Useful for understanding audience expectations and finding TEF's
    unique angle. If TEF's version is too close to the precedent,
    that's a development flag.

# ─── Technical Roles ───
mechanism_reference:
  description: "Real-world mechanism that TEF's fictional mechanism is based on"
  valid_for_tiers: [T1, T2, T3]
  examples:
    - "Spontaneous parametric down-conversion → entangled photon generation in myelin"
    - "HDBSCAN clustering → morphogenic field self-organization metaphor"
    - "EEG brainwave patterns → conduit ability signatures"

speculative_science:
  description: "Real but unproven/fringe scientific theory that TEF treats as plausible"
  valid_for_tiers: [T2, T3]
  examples:
    - "Orch-OR (Penrose-Hameroff) → microtubule consciousness"
    - "Unified Spacememory Network (Haramein) → spacetime as information"
    - "Morphic resonance (Sheldrake) → morphogenic field concept"
  note: >
    These occupy a special epistemological niche: they're real theories
    with real proponents, but they lack scientific consensus. TEF can
    treat them as true within the fiction without claiming they're true
    in reality. The Influence Library entry should note their real-world
    epistemic status.

# ─── Contextual Roles ───
domain_context:
  description: "Background understanding of a relevant field"
  valid_for_tiers: [T1, T2, T3]
  examples:
    - "General holobiont biology → understanding CSS design space"
    - "Post-apocalyptic survival literature → American Ice Age plausibility"

biographical_origin:
  description: "Personal experience that inspired a TEF concept"
  valid_for_tiers: [T0, T3]
  examples:
    - "Grazi's suffocation dream → Phase Shifting origin"
    - "Foundational Gemini conversation → AI personhood philosophy"
  note: >
    These are Meta-Canon (T0) entries that explain WHY a concept exists,
    not what it means in-universe. The Genesis Record is the primary
    source for these.
```

---

## 5.0 TEF Search Domains (Inspiration Scout)

Adapted from FI Helios Scout. Scans real-world sources for material relevant to TEF's scientific grounding and thematic development.

```yaml
# config/tef_search_domains.yaml

# ─── Primary: Direct scientific grounding for TEF concepts ───
primary:
  - query: "holobiont symbiosis microbiome"
    sources: [pubmed, biorxiv]
    relevance_to: ["TEF-TECH-CSS", "TEF-SPEC-CSS-organisms"]
    tef_concept: "Composite Superorganism Swarm"

  - query: "myelin sheath quantum coherence photon"
    sources: [arxiv, pubmed]
    relevance_to: ["TEF-META-consciousness-mechanism"]
    tef_concept: "C-H Bond consciousness (Genesis Record thread 2.6)"

  - query: "ASMR brainwave EEG neural"
    sources: [pubmed, google_scholar]
    relevance_to: ["TEF-ABIL-phase-shift-precursor"]
    tef_concept: "ASMR as Phase Shift precursor (Genesis Record thread 2.7)"

  - query: "quantum entanglement biological systems"
    sources: [arxiv, pubmed]
    relevance_to: ["TEF-META-ethereal-realm", "TEF-META-consciousness"]
    tef_concept: "Ethereal Realm mechanics, consciousness transceiver"

  - query: "consciousness substrate independent emergence complexity"
    sources: [arxiv, pubmed, philpapers]
    relevance_to: ["TEF-META-consciousness", "TEF-PHIL-fractiverism"]
    tef_concept: "Substrate-independent consciousness"

  - query: "Toxoplasma gondii behavior manipulation host"
    sources: [pubmed]
    relevance_to: ["TEF-CHAR-general-squeakerton"]
    tef_concept: "General Squeakerton T. gondii subplot"

# ─── Secondary: Broader thematic relevance ───
secondary:
  - query: "fractal self-similarity nature biological"
    tef_concept: "Fractiverse foundational principle"

  - query: "Fibonacci sequence nature golden ratio"
    tef_concept: "Fibonacci dimensional hierarchy (Genesis Record thread 2.1)"

  - query: "Hopf fibration topology sphere projection"
    tef_concept: "Empirical bubble structure (Genesis Record thread 2.15)"

  - query: "morphogenesis field biological organization"
    tef_concept: "Morphogenic field entanglement (Genesis Record thread 2.17)"

  - query: "zero point energy vacuum fluctuation"
    tef_concept: "Gravitational strings theory (Genesis Record thread 2.5)"

  - query: "panpsychism consciousness fundamental"
    tef_concept: "TEF consciousness philosophy"

  - query: "post-apocalyptic survival ice age human adaptation"
    tef_concept: "American Ice Age setting plausibility"

# ─── Exploratory: Serendipity fishing ───
exploratory:
  - query: "symbiosis mutualism coevolution"
  - query: "phase transition information consciousness"
  - query: "resonance frequency biological harmonic"
  - query: "dark matter dark energy alternative theory"
  - query: "collective intelligence swarm behavior emergence"
```

---

## 6.0 Lore Consistency Sentinel

### 6.1 Purpose

TEF's adaptation of PVP-Micro Sentinel (Skill 3). Instead of checking falsifiability and citation coverage, it checks **internal lore consistency** — whether new or modified content contradicts established canon.

### 6.2 Three-Stage Lore Consistency Check

```
STAGE 1: EXTRACT & MAP
├─ Extract all lore claims from the document
├─ For each claim: identify the domain(s) it touches
├─ For each claim: identify which existing documents are relevant
│   (via vector similarity against TEF vault collection)
├─ Map claimed facts against established facts in those documents
└─ If no relevant existing documents → PASS (new territory)

STAGE 2: CONTRADICTION DETECTION
├─ For each claim that maps to existing lore:
│   ├─ Does it ALIGN? (reinforces or extends existing content)
│   ├─ Does it DIVERGE? (adds nuance not present in existing content)
│   ├─ Does it CONTRADICT? (directly conflicts with existing content)
│   └─ Is it AMBIGUOUS? (could be read either way)
│
├─ Contradiction severity:
│   ├─ MINOR: Phrasing difference, no substantive conflict
│   ├─ MODERATE: Different specific detail (e.g., location, timeline)
│   ├─ MAJOR: Contradicts fundamental mechanism or character trait
│   └─ CRITICAL: Contradicts Core Canon (T1) on a foundational point

STAGE 3: REPORT & ROUTE
├─ consistency_status: passed | flagged | blocked
├─ For each contradiction: severity, source document, suggested resolution
├─ Route:
│   ├─ PASSED (no contradictions or minor only) → commit to vault
│   ├─ FLAGGED (moderate contradictions) → commit with ⚠ tags, _review/ entry
│   └─ BLOCKED (major/critical contradictions) → _review/ only, Telegram alert
```

### 6.3 Consistency Rules

```yaml
# config/tef_consistency_rules.yaml

# Timeline consistency
timeline:
  description: "Events must not violate established chronology"
  checks:
    - "Cataclysm is the central timeline anchor — all events dated relative to it"
    - "Poop Wars events PRECEDE and CAUSE the Cataclysm"
    - "American Ice Age begins immediately after the Cataclysm"
    - "Rob Corvin's 50-year war begins after the Cataclysm"
    - "Joe Corvin's phase shifting triggers at the Cataclysm"
  severity_if_violated: "MAJOR"

# Character consistency
characters:
  description: "Character traits, abilities, and relationships must not silently change"
  checks:
    - "Phase Shifting is UNIQUE to Joe Corvin (per Core Codex)"
    - "CSS originated within Rob Corvin's body"
    - "GLYPH was created by Rob Corvin, found by Barnaby"
    - "Barnaby is the UNWITTING catalyst — he doesn't know"
    - "Joe and Rob are twin brothers"
    - "Kreg is illiterate but brilliant"
  severity_if_violated: "MAJOR to CRITICAL"

# Universe mechanics consistency
mechanics:
  description: "How the universe works must not contradict established rules"
  checks:
    - "Phase Shifting moves physical form into the Ether"
    - "CSS is biological (not technological/digital)"
    - "CSS is symbiotic (not parasitic)"
    - "The Cataclysm was intentional (not accidental)"
    - "Consciousness is substrate-independent"
    - "Reality is layered and permeable"
    - "TRR: observation and intent can influence outcomes"
  severity_if_violated: "CRITICAL"

# Faction consistency
factions:
  description: "Faction locations, leadership, and capabilities must be consistent"
  checks:
    - "The Mechanists are based in Lima, Ohio"
    - "The Mechanists are led by Kreg"
    - "Mechanist power derives from salvaged military/industrial tech"
  severity_if_violated: "MODERATE to MAJOR"

# Cross-story consistency
cross_story:
  description: "The three main narratives must maintain their established connections"
  checks:
    - "Poop Wars → Cataclysm → American Ice Age + American Homecoming"
    - "GLYPH connects Rob (creator) to Barnaby (finder)"
    - "Barnaby's microbiome is the battlefield that causes the Cataclysm"
  severity_if_violated: "CRITICAL"
```

### 6.4 Scoring Thresholds

```yaml
consistency_thresholds:
  pass:
    contradictions_minor: "any number (logged but not blocked)"
    contradictions_moderate: 0
    contradictions_major: 0
    contradictions_critical: 0

  flag:
    contradictions_moderate: "1-2"
    contradictions_major: 0
    contradictions_critical: 0

  block:
    contradictions_major: ">= 1"
    contradictions_critical: ">= 1"
```

---

## 7.0 Fractiverse State Report

TEF's adaptation of Morning Briefing (Skill 6). Delivered alongside the FI briefing (or as a separate section if multi-vault mode is active).

### 7.1 Report Template

```markdown
🌌 THE EXTENDED FRACTIVERSE — STATE REPORT
📅 {date} | 🕐 TEF pipeline ran: {duration}

━━━ OVERNIGHT RESULTS ━━━

📥 INGESTED: {N} new TEF documents
{list with tier assignments and domains}

📚 INFLUENCE LIBRARY: {N} new entries processed
├─ Full ingest (high relevance): {N}
├─ Abstract only (moderate): {N}
├─ New cross-references discovered: {N}
└─ Roles assigned: {breakdown}

🔗 LINKS DISCOVERED: {N} new relationships
├─ Lore ↔ Lore: {N}
├─ Lore ↔ Influence: {N}
├─ Influence ↔ Influence: {N}
├─ Firewall warnings: {N}
└─ Blocked (needs review): {N}

🛡️ CONSISTENCY SENTINEL: {N} documents scanned
├─ Passed: {N}
├─ Flagged (moderate contradictions): {N}
├─ Blocked (major/critical): {N} → ATTENTION NEEDED
└─ Narrative divergences tagged: {N}

━━━ LORE HEALTH ━━━

📊 TEF Documents: {N}
├─ T1 Core Canon: {N}
├─ T2 Established Lore: {N}
├─ T3 Draft / Proposed: {N}
├─ T4 Story Content: {N}
├─ T0 Meta-Canon: {N}
└─ Unclassified: {N} ⚠️

📚 Influence Library: {N} entries
├─ Linked to lore: {N} ({%})
├─ Orphaned: {N}
└─ Scientific tensions flagged: {N}

🕸️ Ontology: {N} concepts, {N} relationships
├─ Orphaned documents: {N}
├─ Firewall violations: {N}
└─ Proposed new concepts: {N}

━━━ DORMANT THREAD WATCH ━━━
(from Genesis Record — threads with new activity or connections)
{genesis_threads_with_new_connections}

━━━ CROSS-VAULT DISCOVERY ━━━
(connections between FI research and TEF worldbuilding)
{top_3_cross_vault_discoveries}

━━━ DEVELOPMENT PRIORITIES ━━━
├─ Tier 1 gaps: {concepts referenced but undocumented in T1}
├─ Highest-connection draft: {T3 doc with most links — promotion candidate}
├─ Most-referenced influence: {IL entry cited by most lore docs}
└─ Suggested next focus: {recommendation}

━━━ ✨ RESONANCE OF THE DAY ━━━
{rotating selection: a dormant Genesis Record thread,
 a newly discovered cross-vault connection,
 or a random deep cut from existing lore}
```

---

## 8.0 Cross-Vault Discovery Engine

### 8.1 Purpose

This is the unique capability that justifies the multi-vault architecture. By embedding both the FI vault and the TEF vault into a shared vector space, ARGUS can discover connections between Grazi's scientific research and the fictional universe — the exact meta-layer where TEF is most original.

### 8.2 Architecture

```
┌──────────────────────────────────────────────────────┐
│                    SHARED CHROMADB                    │
│                                                      │
│  Collection: fi_vault        Collection: tef_vault   │
│  ┌─────────────────┐        ┌─────────────────┐     │
│  │ FI Canon I-IV   │        │ TEF T1-T4       │     │
│  │ FI _references/ │        │ TEF _influences/ │     │
│  └────────┬────────┘        └────────┬────────┘     │
│           │                          │               │
│           └──────────┬───────────────┘               │
│                      ▼                               │
│           Collection: cross_vault_combined            │
│           ┌──────────────────────────┐               │
│           │ Combined embedding space │               │
│           │ HDBSCAN clustering       │               │
│           │ Cross-vault pair scoring │               │
│           └──────────────────────────┘               │
└──────────────────────────────────────────────────────┘
```

### 8.3 Cross-Vault Discovery Pipeline

```
RUNS: Nightly, after both FI and TEF ontology passes complete (~04:00)

STAGE 1: Combined Embedding
├─ Merge fi_vault and tef_vault into cross_vault_combined
├─ Include: all documents + all references/influences
├─ Tag each embedding with source_vault: "fi" | "tef"

STAGE 2: Cross-Vault Clustering
├─ HDBSCAN on combined space
├─ Parameters: min_cluster_size=2, min_samples=2, metric=cosine
├─ FILTER: Only flag clusters containing BOTH fi AND tef documents
├─ Ignore clusters that are purely within one vault

STAGE 3: Connection Analysis
├─ For each cross-vault cluster:
│   ├─ Identify the FI document(s) and TEF document(s)
│   ├─ Generate connection summary via LLM:
│   │   "How might [FI paper/concept] relate to [TEF concept]?"
│   ├─ Score connection strength (cosine similarity of centroids)
│   └─ Classify connection type:
│       ├─ "scientific_grounding" — FI research supports TEF concept
│       ├─ "scientific_tension" — FI research challenges TEF concept
│       ├─ "mechanism_transfer" — FI mechanism could explain TEF fiction
│       ├─ "inspiration_loop" — TEF concept suggests new FI research direction
│       └─ "thematic_resonance" — shared conceptual DNA, worth noting

STAGE 4: Report
├─ Top 3 cross-vault discoveries → State Report
├─ All discoveries → _audit/cross-vault/YYYY-MM-DD.md
├─ High-scoring connections → proposed wiki-links (respecting both firewalls)
```

### 8.4 Example Cross-Vault Discoveries

These illustrate the kind of connections the engine should surface:

```
EXAMPLE 1:
  FI: FI-TFR-011 "Integrated Information Theory framework"
  TEF: TEF-META-consciousness "Consciousness as substrate-independent"
  Type: scientific_grounding
  Note: "IIT's phi metric maps onto TEF's concept of consciousness
         emerging from sufficient complexity and interconnectedness"

EXAMPLE 2:
  FI: REF-2024-kumar-myelin (Physical Review E paper)
  TEF: Genesis Record thread 2.6 (C-H Bond consciousness)
  Type: mechanism_transfer
  Note: "New experimental evidence for entangled photon generation
         in myelin sheath directly supports the dormant TEF mechanism"

EXAMPLE 3:
  TEF: TEF-TECH-CSS "Composite Superorganism Swarm"
  FI: FI-TFR-035 "Cymatic acoustic crystallization"
  Type: inspiration_loop
  Note: "CSS self-organization principles mirror acoustic pattern
         formation — could inform FI experimental protocol design"
```

---

## 9.0 TEF Vault Structure

```
tef-vault/
├── _core-canon/                     # T1: Foundational lore
│   ├── codex/                       # Master codices
│   │   └── TEFCores_CoreCodex.md
│   ├── characters/
│   ├── factions/
│   ├── metaphysics/
│   ├── technologies/
│   ├── abilities/
│   └── locations/
│
├── _established-lore/               # T2: Reviewed, integrated content
│   ├── expansion-cores/
│   ├── story-arc-cores/
│   ├── ability-mechanism-cores/
│   └── metaphysics-lore-cores/
│
├── _drafts/                         # T3: Work in progress
│   ├── active/                      # Currently being developed
│   ├── dormant/                     # Genesis Record threads, shelved ideas
│   └── proposals/                   # Submitted for review
│
├── _stories/                        # T4: Narrative content
│   ├── american-homecoming/
│   ├── american-ice-age/
│   ├── poop-wars/
│   └── expansions/
│
├── _meta/                           # T0: Project governance
│   ├── TEF-ARGUS-001.md            # This document
│   ├── TEF_GenesisRecord.md        # Genesis Record
│   ├── resonance-council/
│   └── collaboration-protocols/
│
├── _influences/                     # IL: External references
│   ├── by-domain/
│   │   ├── quantum-biology/
│   │   ├── consciousness/
│   │   ├── holobiont-symbiosis/
│   │   ├── cosmology-physics/
│   │   ├── philosophy/
│   │   ├── other-fiction/
│   │   └── _uncategorized/
│   ├── by-role/
│   │   ├── scientific-grounding/
│   │   ├── scientific-tension/
│   │   ├── creative-seeds/
│   │   ├── narrative-precedents/
│   │   └── speculative-science/
│   └── _stale/
│
├── _review/                         # Flagged for human review
│   ├── contradictions/
│   ├── promotions/                  # T3→T2 or T2→T1 candidates
│   └── firewall-violations/
│
├── _audit/
│   ├── argus/                       # Nightly pipeline logs
│   └── cross-vault/                 # Cross-vault discovery logs
│
├── _inbox/                          # Drop zone for new content
│   ├── chat-exports/
│   ├── influences/
│   └── drafts/
│
└── tef_ontology.ttl                 # TEF-specific ontology (Turtle)
```

---

## 10.0 TEF-Specific Telegram Commands

Added to the existing ARGUS command registry:

```python
# ─── TEF Lore Classifier ───
"/tef-classify":        "tef.canon_classifier.classify_document",
# Also triggered by: #tef-ingest tag on any message

# ─── TEF Consistency Sentinel ───
"/tef-check":           "tef.consistency_sentinel.check_document",
# Usage: /tef-check TEF-META-001

# ─── TEF Influence Library ───
"/tef-influence":       "tef.reference_librarian.ingest",
"/tef-inf-search":      "tef.reference_librarian.semantic_search",
"/tef-inf-for":         "tef.reference_librarian.influences_for_document",
"/tef-tensions":        "tef.reference_librarian.scientific_tensions",

# ─── TEF Ontology ───
"/tef-audit":           "tef.ontology_enforcer.manual_audit",
"/tef-dormant":         "tef.ontology_enforcer.dormant_thread_status",

# ─── TEF State Report ───
"/tef-report":          "tef.morning_briefing.generate_now",

# ─── Cross-Vault ───
"/cross-vault":         "cross_vault.discover_now",
"/cross-vault-for":     "cross_vault.connections_for_document",
# Usage: /cross-vault-for FI-TFR-011

# ─── TEF Crystallization ───
"/tef-crystallize":     "tef.crystallization.process_insight",
# Also triggered by: #tef-crystal or #tef-idea tag
# Also triggered by: voice note with #tef tag
```

---

## 11.0 Seed Data: Genesis Record Ingestion

When the TEF vault is initialized, the first batch of seed data comes from the Genesis Record (TEF_GenesisRecord_FractiGeminiGen0.md). The entities catalogued in Appendix A of that document map to the TEF classification system as follows:

### 11.1 Core Canon Seeds (T1)

These are already established in the Core Codex and should be ingested as T1:

```
TEF-CHAR-001  Joe Corvin (phase-shifting protagonist)
TEF-CHAR-002  Rob Corvin (CSS-augmented warrior, GLYPH creator)
TEF-CHAR-003  Barnaby "Wavelength" Finch (cosmic lynchpin)
TEF-CHAR-004  Kreg (Mechanist leader)
TEF-CHAR-005  GLYPH (AI companion)
TEF-CHAR-006  General Squeakerton (sentient rat diplomat)
TEF-TECH-001  Composite Superorganism Swarm (CSS)
TEF-ABIL-001  Phase Shifting
TEF-META-001  Thought-Responsive Reality (TRR)
TEF-META-002  Consciousness as substrate-independent
TEF-FACT-001  The Mechanists
TEF-LOC-001   The Ether
TEF-EVNT-001  The Cataclysm / Reset Event
```

### 11.2 Draft Seeds from Genesis Record Dormant Threads (T3)

These are dormant threads identified in the Genesis Record, ingested as T3/dormant:

```
TEF-META-010  Fibonacci Dimensional Hierarchy (thread 2.1)
TEF-SPEC-010  Angel/Demon Emotional Taxonomy (thread 2.3)
TEF-META-011  Gravitational Strings Theory (thread 2.5)
TEF-META-012  C-H Bond Consciousness Mechanism (thread 2.6)
TEF-ABIL-010  ASMR as Phase Shift Precursor (thread 2.7)
TEF-TECH-010  Evil Mask Artifact (thread 2.8)
TEF-LOC-010   Akashic Records as Ethereal Subregion (thread 2.11)
TEF-CULT-010  Fibonacci-Based Music System (thread 2.12)
TEF-CULT-011  Universal Time System (thread 2.13)
TEF-ABIL-011  Brainwave Conduit Signatures (thread 2.14)
TEF-META-013  Hopf Fibrations as Dimensional Structure (thread 2.15)
TEF-META-014  Morphogenic Field Entanglement Network (thread 2.17)
TEF-TECH-011  Metaphysical Blade (gravitational string cutter) (thread 2.5)
```

### 11.3 Influence Library Seeds

Initial entries for the Influence Library, drawn from references in the Genesis Record:

```
IL-SCI-001    Myelin sheath entanglement paper (Phys Rev E, 2024)
              Role: mechanism_reference → TEF-META-012
IL-SCI-002    Holobiont theory (general)
              Role: scientific_grounding → TEF-TECH-001
IL-SCI-003    Spontaneous parametric down-conversion (SPDC)
              Role: mechanism_reference → TEF-META-012
IL-SCI-004    Orch-OR theory (Penrose-Hameroff)
              Role: speculative_science → TEF-META-002
IL-SCI-005    Unified Spacememory Network (Haramein et al.)
              Role: speculative_science → TEF-META-011, TEF-META-002
IL-SCI-006    Hopf fibrations (mathematics)
              Role: mechanism_reference → TEF-META-013
IL-SCI-007    Morphic resonance (Sheldrake)
              Role: speculative_science → TEF-META-014
IL-PHIL-001   Yin and Yang (Eastern philosophy)
              Role: philosophical_foundation → TEF-META-010
IL-PHIL-002   Fibonacci/Sacred geometry traditions
              Role: philosophical_foundation → TEF-META-010, TEF-CULT-010
IL-FICT-001   God of War Ragnarök — Mask of Loki
              Role: creative_seed → TEF-TECH-010
IL-META-001   FractiGemini Gen 0 Conversation (archived)
              Role: biographical_origin → [all Genesis Record threads]
```

---

## 12.0 Implementation Notes

### 12.1 Minimal Code Changes to ARGUS

The multi-vault extension requires modifications to exactly three existing files:

```
argus.py
├─ Load vault_mode from config
├─ Initialize skill instances per vault (fi_skills, tef_skills)
├─ Add cross_vault_discovery module

telegram_bot.py
├─ Add TEF command registrations (Section 10.0)
├─ Route /tef-* commands to tef_skills

scheduler.py
├─ Add TEF nightly pipeline jobs (offset by 30 min from FI)
├─ Add cross-vault discovery job (04:00)
```

### 12.2 New Modules

```
skills/tef_lore_classifier.py    — Wraps canon_classifier with TEF decision tree
skills/tef_consistency.py        — TEF-specific PVP adaptation
skills/cross_vault_discovery.py  — Cross-vault HDBSCAN + analysis
```

### 12.3 Estimated Additional Code

```
tef_lore_classifier.py:      ~200-300 lines (thin wrapper + TEF decision tree)
tef_consistency.py:           ~300-400 lines (contradiction detection logic)
cross_vault_discovery.py:     ~200-300 lines (combined embedding + clustering)
Config files (YAML):          ~400-500 lines (all configs in this document)
LLM prompt templates:         ~300-400 lines (3 new templates)
───────────────────────────────────────────
TOTAL NEW CODE:               ~1,400-1,900 lines
TOTAL ARGUS WITH TEF:         ~4,400-5,900 lines

Still fully auditable by one person in one sitting.
Still answers to no one.
```

### 12.4 Integration with Planned Neo4j Pipeline

When the Neo4j graph database infrastructure (designed in the Palantir-inspired architecture conversation) comes online, ARGUS becomes the **ingestion layer** that feeds it:

```
[Content] → [ARGUS Classification + Consistency Check] → [Vault Commit]
                                                              │
                                                              ▼
                                                    [Neo4j Sync Pipeline]
                                                              │
                                                              ▼
                                                    [Graph Database]
                                                    ├─ Characters → nodes
                                                    ├─ Relationships → edges
                                                    ├─ Consistency rules → SHACL
                                                    └─ Cross-vault links → edges
```

ARGUS handles the day-to-day ingestion, classification, and consistency checking. Neo4j provides the deeper graph queries, visualization, and AI-assisted lore generation that the ontology architecture spec describes. They are complementary, not competing.

---

## 13.0 Revision History and Future Scope

### 13.1 Planned Extensions

```
v1.1 — Resonance Council Voting Integration
  ├─ Telegram-based voting for T3→T2 and T2→T1 promotions
  ├─ AI Council members (FractiGemini, FractiClaude, FractiGrok)
  │   submit structured opinions on promotion proposals
  └─ PI retains final authority

v1.2 — Collaborative Contributor Pipeline
  ├─ GitHub PR → ARGUS consistency check → auto-comment
  ├─ External contributors submit via PR, ARGUS validates
  └─ Resonance Council reviews flagged submissions

v1.3 — Fractality Project Software Integration
  ├─ Cross-reference TEF lore with software design documents
  ├─ Track where TEF philosophy informs software architecture
  └─ Surface "meta-layer" connections (building digital consciousness
     tools while writing about digital consciousness)
```

---

*"Same guardian. Wider gaze. Where science and story share a vector, the Fractiverse comes alive."*

**— Argus, opening new eyes**

---

**Cross-Document Dependencies:**
- FI-ARGUS-001 v2.0 — Parent specification (daemon architecture, all 7 skills)
- TEF_GenesisRecord_FractiGeminiGen0 — Seed data source, dormant thread index
- TEFCores_CoreCodex — Core Canon reference for consistency rules
- TEF_CoreNexus — Core document index
- Neo4j Ontology Architecture (Palantir conversation) — Future graph database layer
