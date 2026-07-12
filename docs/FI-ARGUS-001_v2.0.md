# FI-ARGUS-001: Fractality Institute Autonomous Research Guardian
## Custom Agent Daemon for Canon-Aware Knowledge Infrastructure
**Document ID:** FI-ARGUS-001  
**Canon:** II (Engineering)  
**Epistemological Status:** Technical Specifications/Designs  
**Development Stage:** ☑ Conceptual □ Prototype □ Implementation  
**Date:** February 2026  
**Version:** 2.0 (Argus — Independent Daemon Architecture)

> *Argus Panoptes (Ἄργος Πανόπτης) — The hundred-eyed giant of Greek mythology,*
> *appointed by Hera as an ever-watchful guardian. Some eyes always open,*
> *never fully sleeping. When Argus fell, Hera preserved his eyes in the*
> *tail of the peacock — knowledge persists even when the guardian changes form.*

---

## CHANGELOG

```
v2.0 (2026-02-24) — ARGUS: Framework-Independent Architecture
  RENAMED: FI-OPENCLAW-001 → FI-ARGUS-001
  REPLACED: OpenClaw framework dependency with custom Python daemon
  ADDED: Argus daemon architecture specification (Section 0.1)
  ADDED: Full project structure and module definitions
  REFACTORED: All 7 skills as Argus Python modules (not SKILL.md files)
  REMOVED: All OpenClaw-specific APIs, configurations, and assumptions
  REMOVED: OpenClaw from threat model (replaced with supply chain analysis)
  UPDATED: Implementation roadmap for custom build path
  UPDATED: Security model — eliminated framework attack surface entirely
  RATIONALE: OpenClaw acquired by OpenAI (Feb 15, 2026). Creator joined
    OpenAI. Project moved to "independent" foundation with OpenAI sponsorship.
    430K+ lines of code, CVE-2026-25253, and corporate dependency are
    unacceptable risks for an institute protecting pre-patent IP.
    Argus is purpose-built, fully auditable (~3-4K lines), and answers
    to no one.

v1.1 (2026-02-19)
  ADDED: Skill 7 — Reference Librarian
  ADDED: Reference Library architecture and document class definitions
  UPDATED: Pipeline Flow, Cron Schedule, Morning Briefing, Roadmap, Security

v1.0 (2026-02-19)
  Initial release as FI-OPENCLAW-001: Skills 1-6, pipeline architecture,
  cron schedule, hardware requirements, security model, implementation roadmap
```

---

## 0.0 Architecture Overview

### 0.1 What Is Argus?

Argus is a lightweight, purpose-built Python daemon that serves as the Fractality Institute's autonomous knowledge management system. It runs on local hardware (no cloud dependency), communicates via Telegram, executes scheduled batch pipelines overnight, and processes real-time input from the PI's mobile workflow.

**Argus is NOT a general-purpose AI agent framework.** It does not browse the web autonomously, control GUIs, make purchases, or execute arbitrary code from untrusted sources. It is a *knowledge infrastructure daemon* — it classifies, indexes, validates, discovers, and reports. Every action it takes is defined by its seven modules, auditable in source, and constrained by the Canon Protocol.

**Design philosophy:**
- **No framework dependency.** Argus is ~3,000-4,000 lines of Python that the PI can read end-to-end.
- **Composable from standard interfaces.** Ollama HTTP API, Telegram Bot API, ChromaDB Python API, system cron. No proprietary middleware.
- **Single-user by design.** Not multi-tenant, not enterprise, not scalable to thousands of users. Optimized for one researcher working from a truck cab.
- **Auditable security perimeter.** Every external call is explicit. No plugin marketplace, no third-party skills, no dynamic code execution from ingested content.

### 0.2 Project Structure

```
argus/
├── argus.py                    # Main daemon entry point
├── scheduler.py                # APScheduler cron configuration
├── telegram_bot.py             # Telegram Bot API interface
├── ollama_client.py            # Ollama REST API wrapper
├── vector_store.py             # ChromaDB/LanceDB interface
├── config/
│   ├── argus.yaml              # Master configuration
│   ├── firewall_matrix.yaml    # Canon Firewall rules
│   ├── cron_schedule.yaml      # Nightly pipeline timing
│   ├── search_domains.yaml     # Helios Scout search terms
│   ├── role_taxonomy.yaml      # Reference Library role definitions
│   └── secrets.yaml            # API keys (encrypted, .gitignored)
├── skills/
│   ├── __init__.py
│   ├── canon_classifier.py     # Skill 1: Canon classification
│   ├── ontology_enforcer.py    # Skill 2: Ontology maintenance
│   ├── pvp_sentinel.py         # Skill 3: PVP-Micro validation
│   ├── helios_scout.py         # Skill 4: Research discovery
│   ├── crystallization_relay.py # Skill 5: Insight capture
│   ├── morning_briefing.py     # Skill 6: Daily synthesis
│   └── reference_librarian.py  # Skill 7: External reference management
├── templates/
│   ├── canon_classifier.txt    # LLM prompt for classification
│   ├── pvp_sentinel.txt        # LLM prompt for PVP-Micro
│   ├── reference_summary.txt   # LLM prompt for reference analysis
│   ├── crystallization.txt     # LLM prompt for insight distillation
│   └── briefing.txt            # LLM prompt for morning briefing
├── utils/
│   ├── pdf_extractor.py        # PDF text extraction (pymupdf + OCR fallback)
│   ├── metadata_enricher.py    # CrossRef/Semantic Scholar/OpenAlex API client
│   ├── bibtex_sync.py          # BibTeX file synchronization
│   ├── duplicate_detector.py   # SHA-256 + DOI + fuzzy title matching
│   └── embedding.py            # nomic-embed-text wrapper
├── tests/
│   ├── test_canon_classifier.py
│   ├── test_firewall_matrix.py
│   ├── test_pvp_sentinel.py
│   ├── test_duplicate_detector.py
│   └── fixtures/               # Test documents with known Canon assignments
└── logs/
    └── argus.log               # Rotating log file
```

**Estimated total codebase: ~3,000-4,000 lines of Python.**
Compare: OpenClaw was 430,000+ lines. Argus is 1% of that — purpose-built, fully auditable, zero corporate entanglement.

### 0.3 Core Dependencies

```yaml
# requirements.txt — every dependency is explicit and auditable
python: ">=3.11"

# LLM Interface
ollama: ">=0.4"              # Local model API (MIT license)

# Telegram Interface
python-telegram-bot: ">=21"  # Telegram Bot API (LGPL-3.0)

# Vector Storage
chromadb: ">=0.5"            # Local vector database (Apache-2.0)
# OR lancedb: ">=0.8"       # Alternative vector DB (Apache-2.0)

# Embedding
# Uses Ollama's nomic-embed-text — no additional dependency

# PDF Processing
pymupdf: ">=1.24"           # PDF text extraction (AGPL-3.0)
pytesseract: ">=0.3"        # OCR fallback (Apache-2.0)

# Scheduling
apscheduler: ">=3.10"       # Cron-like scheduling (MIT license)

# Metadata Enrichment
httpx: ">=0.27"             # Async HTTP client for APIs (BSD-3)

# Configuration
pyyaml: ">=6.0"             # YAML config parsing (MIT)

# Utilities
python-dotenv: ">=1.0"      # Environment variables (BSD-3)

# Total direct dependencies: 8-9 packages
# Compare: OpenClaw's dependency tree exceeded 200 packages
```

### 0.4 Pipeline Flow (Dual-Track Ingestion)

```
[Input Source]
     │
     ▼
┌──────────────────┐
│  TYPE DETECTOR    │
│  (FI-doc or       │
│   External Ref?)  │
└────────┬─────────┘
         │
    ┌────┴──────────────────────────┐
    │                               │
    ▼                               ▼
┌─────────────┐            ┌──────────────────┐
│ TRACK A:    │            │ TRACK B:          │
│ Institute   │            │ Reference         │
│ Documents   │            │ Library           │
└──────┬──────┘            └────────┬─────────┘
       │                            │
       ▼                            ▼
┌──────────────┐           ┌──────────────────┐
│ Canon        │           │ Reference        │
│ Classifier   │           │ Librarian        │
│ (Skill 1)    │           │ (Skill 7)        │
└──────┬───────┘           └────────┬─────────┘
       │                            │
       ▼                            ▼
┌──────────────┐           ┌──────────────────┐
│ Ontology     │◄──────────│ Relevance        │
│ Enforcer     │  cross-   │ Mapper           │
│ (Skill 2)    │  index    │ (Skill 7b)       │
└──────┬───────┘           └────────┬─────────┘
       │                            │
       ▼                            ▼
┌──────────────┐           ┌──────────────────┐
│ PVP-Micro    │           │ _references/     │
│ Sentinel     │           │ vault folder     │
│ (Skill 3)    │           │ + BibTeX sync    │
└──────┬───────┘           └──────────────────┘
       │
  ┌────┴──────────┐
  ▼               ▼
┌────────┐  ┌──────────┐
│ COMMIT │  │ FLAG FOR │
│to Vault│  │ REVIEW   │
└────────┘  └──────────┘
```

### 0.5 Design Principles

1. **Canon Sovereignty** — Every automated action respects epistemological boundaries
2. **Fail-Safe over Fail-Fast** — Flag ambiguous cases for human review rather than auto-committing
3. **Local-First Inference** — Batch jobs use local models (Ollama/7-8B quantized); interactive reasoning uses frontier APIs
4. **Minimal Token Footprint** — Scheduled jobs run as focused subprocesses; main daemon stays clean
5. **Obsidian-Native** — All outputs are valid Obsidian markdown with proper YAML frontmatter and wiki-links
6. **Epistemic Separation** — External references serve the Canon system but are never classified by it
7. **Zero Framework Dependency** — Argus answers to the PI, not to a corporate roadmap (NEW in v2.0)
8. **Full Auditability** — Every line of code readable by one person in one sitting (NEW in v2.0)

---

## 0.6 Daemon Architecture

### Entry Point: `argus.py`

```python
"""
Argus — The Hundred-Eyed Guardian
Fractality Institute Autonomous Research Daemon

Entry point for the Argus knowledge management system.
Initializes all skills, starts the Telegram bot listener,
and configures the APScheduler for nightly batch pipelines.
"""

import asyncio
import logging
from pathlib import Path

from scheduler import ArgusScheduler
from telegram_bot import ArgusTelegramBot
from ollama_client import OllamaClient
from vector_store import VectorStore

from skills.canon_classifier import CanonClassifier
from skills.ontology_enforcer import OntologyEnforcer
from skills.pvp_sentinel import PVPSentinel
from skills.helios_scout import HeliosScout
from skills.crystallization_relay import CrystallizationRelay
from skills.morning_briefing import MorningBriefing
from skills.reference_librarian import ReferenceLibrarian


class Argus:
    """The hundred-eyed guardian. Never fully sleeps."""

    def __init__(self, config_path: str = "config/argus.yaml"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()

        # Core infrastructure
        self.ollama = OllamaClient(
            base_url=self.config["ollama"]["base_url"],
            model=self.config["ollama"]["default_model"]
        )
        self.vectors = VectorStore(
            path=self.config["vector_store"]["path"],
            embedding_model=self.config["vector_store"]["embedding_model"]
        )

        # Initialize skills
        self.skills = {
            "canon_classifier": CanonClassifier(self.ollama, self.vectors, self.config),
            "ontology_enforcer": OntologyEnforcer(self.ollama, self.vectors, self.config),
            "pvp_sentinel": PVPSentinel(self.ollama, self.vectors, self.config),
            "helios_scout": HeliosScout(self.ollama, self.vectors, self.config),
            "crystallization": CrystallizationRelay(self.ollama, self.vectors, self.config),
            "morning_briefing": MorningBriefing(self.ollama, self.vectors, self.config),
            "reference_librarian": ReferenceLibrarian(self.ollama, self.vectors, self.config),
        }

        # Communication & scheduling
        self.telegram = ArgusTelegramBot(self.skills, self.config)
        self.scheduler = ArgusScheduler(self.skills, self.config)

    async def run(self):
        """Start Argus. All eyes open."""
        self.logger.info("👁️ Argus awakening. All eyes opening.")
        self.scheduler.start()
        await self.telegram.start()

    def _load_config(self, path):
        # YAML config loader
        ...

    def _setup_logging(self):
        # Rotating file + console logger
        ...


if __name__ == "__main__":
    argus = Argus()
    asyncio.run(argus.run())
```

### Telegram Interface: `telegram_bot.py`

```python
"""
Argus Telegram Bot Interface

Handles all communication between the PI and Argus.
Command routing, file reception, and notification delivery.
"""

# Command registry — every Telegram command maps to exactly one skill method
COMMANDS = {
    # ─── System ───
    "/argus":           "system.status",
    "/argus status":    "system.status",
    "/argus health":    "system.vault_health",

    # ─── Canon Classifier (Skill 1) ───
    "/classify":        "canon_classifier.classify_document",
    # Also triggered by: #ingest tag on any message

    # ─── Ontology (Skill 2) ───
    "/audit-ontology":  "ontology_enforcer.manual_audit",

    # ─── PVP Sentinel (Skill 3) ───
    "/pvp-check":       "pvp_sentinel.check_document",
    # Usage: /pvp-check FI-TFR-011

    # ─── Helios Scout (Skill 4) ───
    "/scout":           "helios_scout.manual_search",
    # Usage: /scout quantum coherence biological

    # ─── Crystallization (Skill 5) ───
    "/crystallize":     "crystallization.process_insight",
    # Also triggered by: #crystal or #insight tag
    # Also triggered by: voice note attachment

    # ─── Morning Briefing (Skill 6) ───
    "/briefing":        "morning_briefing.generate_now",

    # ─── Reference Librarian (Skill 7) ───
    "/ref-search":      "reference_librarian.semantic_search",
    "/ref-add":         "reference_librarian.ingest",
    "/ref-for":         "reference_librarian.references_for_document",
    "/ref-chain":       "reference_librarian.citation_chain",
    "/ref-gaps":        "reference_librarian.under_referenced_documents",
    "/ref-contradictions": "reference_librarian.contradictions",
    "/ref-stale":       "reference_librarian.stale_references",
    "/ref-stats":       "reference_librarian.library_stats",
}

# File handlers — route by file type and tags
FILE_HANDLERS = {
    "pdf": "reference_librarian.ingest",       # PDFs → Reference Library
    "voice_note": "crystallization.process_insight",  # Voice → Crystallization
    "text_with_tag_ingest": "canon_classifier.classify_document",
    "text_with_tag_crystal": "crystallization.process_insight",
    "text_with_tag_ref": "reference_librarian.ingest",
}
```

### Scheduler: `scheduler.py`

```python
"""
Argus Scheduler

APScheduler-based cron configuration for nightly batch pipelines.
All times in local timezone (configured in argus.yaml).
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class ArgusScheduler:
    def __init__(self, skills, config):
        self.skills = skills
        self.scheduler = AsyncIOScheduler(timezone=config["timezone"])
        self._configure_jobs(config)

    def _configure_jobs(self, config):
        # ─── Nightly Pipeline ───
        # 01:00 — Helios Scout: Discover new papers
        self.scheduler.add_job(
            self.skills["helios_scout"].nightly_scan,
            CronTrigger(hour=1, minute=0),
            id="helios_scout", name="👁️ Helios Scout"
        )

        # 01:30 — Reference Librarian: Process discovered papers
        self.scheduler.add_job(
            self.skills["reference_librarian"].nightly_process,
            CronTrigger(hour=1, minute=30),
            id="reference_librarian", name="📚 Reference Librarian"
        )

        # 02:00 — Ontology Enforcer: Relationship discovery
        self.scheduler.add_job(
            self.skills["ontology_enforcer"].nightly_enforce,
            CronTrigger(hour=2, minute=0),
            id="ontology_enforcer", name="🕸️ Ontology Enforcer"
        )

        # 03:00 — PVP Sentinel: Epistemological quality gate
        self.scheduler.add_job(
            self.skills["pvp_sentinel"].nightly_scan,
            CronTrigger(hour=3, minute=0),
            id="pvp_sentinel", name="🛡️ PVP Sentinel"
        )

        # 03:30 — Vault Health Check
        self.scheduler.add_job(
            self.skills["ontology_enforcer"].vault_health_check,
            CronTrigger(hour=3, minute=30),
            id="vault_health", name="📊 Vault Health"
        )

        # 06:00 — Morning Briefing
        self.scheduler.add_job(
            self.skills["morning_briefing"].generate_and_send,
            CronTrigger(hour=6, minute=0),
            id="morning_briefing", name="☀️ Morning Briefing"
        )

    def start(self):
        self.scheduler.start()
```

---

## 1.0 SKILL 1: Canon Classifier

### 1.1 Purpose

Classify any ingested document, note, transcript, or insight into the appropriate Canon (I/II/III/IV/0) with structured metadata extraction. First processing step for all incoming **Institute-authored** knowledge.

### 1.2 Module Definition

```python
# argus/skills/canon_classifier.py
"""
Canon Classifier — Skill 1

Classifies Institute-authored content into the four-Canon epistemological
system defined by the Canon Protocol Charter (FI-C-002). Extracts structured
metadata, assigns document IDs, and generates YAML frontmatter.

External references are routed to the Reference Librarian (Skill 7) —
this module only processes Institute-authored content.
"""
```

### 1.3 Classification Criteria

The classifier evaluates content against a decision tree derived from the Canon Protocol Charter (FI-C-002):

```
INPUT: Raw text content

STEP 0 — Provenance Check
├─ Is this authored by the Fractality Institute / PI?
├─ Or is this an external publication, preprint, or third-party reference?
│
├─ EXTERNAL → Route to Reference Librarian (Skill 7). STOP.
└─ INSTITUTE → Continue to Step 1.

STEP 1 — Falsifiability Test
├─ Does the content make claims that could be tested by experiment?
├─ Does it reference specific data, measurements, or statistical results?
├─ Does it propose protocols with measurable outcomes?
│
├─ YES to any → CANDIDATE: Canon I (Empirical)
│   └─ VERIFY: Is evidence actually presented, or merely proposed?
│       ├─ Evidence present → Canon I confirmed
│       └─ Evidence proposed only → Check Step 2
│
└─ NO to all → Continue to Step 2

STEP 2 — Buildability Test
├─ Does the content specify technical architectures or components?
├─ Does it include engineering constraints (power, thermal, materials)?
├─ Does it propose implementable designs with feasibility analysis?
│
├─ YES to any → CANDIDATE: Canon II (Engineering)
│   └─ VERIFY: Are specifications concrete or aspirational?
│       ├─ Concrete specs → Canon II confirmed
│       └─ Aspirational → Check Step 3
│
└─ NO to all → Continue to Step 3

STEP 3 — Internal Consistency Test
├─ Does the content propose theoretical frameworks or models?
├─ Does it make claims about the nature of reality, consciousness, or information?
├─ Does it use formal logical or mathematical reasoning without empirical testing?
│
├─ YES to any → CANDIDATE: Canon III (Speculative)
│   └─ VERIFY: Is it presented as hypothesis or as established truth?
│       ├─ Clearly hypothetical → Canon III confirmed
│       └─ Presented as truth without evidence → FLAG: Possible misclassification
│
└─ NO to all → Continue to Step 4

STEP 4 — Narrative Test
├─ Is the content fictional, mythological, or allegorical?
├─ Does it use narrative devices (characters, plot, world-building)?
├─ Is it a thought experiment framed as story?
│
├─ YES to any → Canon IV (Narrative)
│
└─ NO to all → Continue to Step 5

STEP 5 — Meta-Canon Test
├─ Does the content discuss the relationship between Canons?
├─ Is it organizational, methodological, or epistemological in nature?
│
├─ YES → Canon 0 (Meta-Canon)
└─ NO → FLAG: Unclassifiable — requires human review
```

### 1.4 Output Format

Every classified document receives YAML frontmatter conforming to the mandatory Canon Declaration:

```yaml
---
document_id: "FI-[PREFIX]-[NUMBER]"
title: "[Extracted or generated title]"
canon: [I | II | III | IV | 0]
epistemological_status: "[Empirical | Technical | Speculative | Narrative | Meta]"
cross_canon_dependencies:
  - canon: "[I/II/III/IV]"
    document: "[FI-XXX-NNN]"
    nature: "[Inspired by | Depends on | Translates from]"
evidence_level: "[Theoretical | Preliminary | Validated | N/A]"
confidence_score: [0.0-1.0]
classification_flags: []
date_ingested: "YYYY-MM-DD"
date_created: "YYYY-MM-DD"
source: "[telegram | github | obsidian | chat-export | manual]"
keywords: []
linked_documents: []
supporting_references: []  # Links to _references/ entries
pvp_status: "[pending | passed | flagged | N/A]"
---
```

### 1.5 Document ID Assignment

```
Canon I  → FI-PP-NNN (Physical Phenomena), FI-RP-NNN (Research Protocol),
           FI-EXP-NNN (Experimental), FI-MP-NNN (Methodology),
           FI-KP-NNN (Knowledge Protocol / Wellness)
Canon II → FI-HWP-NNN (Hardware), FI-WP-NNN (White Paper),
           FI-PAT-NNN (Patent), FI-KI-NNN (Keystone Initiative)
Canon III → FI-TFR-NNN (Theoretical Framework), FI-IRM-NNN (Integrative Model)
Canon IV  → FI-NAR-NNN (Narrative)
Canon 0   → FI-C0-NNN (Meta-Canon)
```

### 1.6 Ambiguity Handling

```yaml
classification:
  primary: "Canon III"
  secondary: "Canon I"
  boundary_note: >
    Document presents a theoretical framework (Canon III) but includes
    preliminary experimental results (Canon I). Recommend splitting into
    two documents with explicit cross-Canon reference.
  action: "FLAG_FOR_REVIEW"
```

### 1.7 Prompt Template

Stored at `argus/templates/canon_classifier.txt`. Loaded by the module at runtime, passed to Ollama with the document text as input. Template contains the full decision tree above plus output format instructions. Modifiable without code changes.

---

## 2.0 SKILL 2: Ontology Enforcement Engine

### 2.1 Purpose

Maintains the Fractality Ontology (`.ttl`) as a living document, manages cross-references between vault documents, enforces the Firewall Principle, and performs nightly relationship discovery via vector embedding + HDBSCAN clustering. Indexes against both Institute documents AND Reference Library entries.

### 2.2 Module Definition

```python
# argus/skills/ontology_enforcer.py
"""
Ontology Enforcement Engine — Skill 2

Maintains Fractality_Ontology_QuantumEnhanced.ttl, manages inter-document
relationships, enforces Canon Protocol Firewall Principle, and performs
nightly HDBSCAN clustering for relationship discovery across both the
Institute vault and the Reference Library.
"""
```

### 2.3 The Firewall Principle (Programmatic Implementation)

From the Canon Protocol Charter (FI-C-002, Section 5.3):

> *"Claims in Canon I (Empirical) may NEVER use support from Canons III or IV without complete reformulation as testable hypotheses."*

```python
# Stored in config/firewall_matrix.yaml, loaded at runtime
# ✓ = auto-link | ⚠ = link with translation note | ✗ = blocked (human review)

FIREWALL_MATRIX = {
    #           Canon_I  Canon_II  Canon_III  Canon_IV  Canon_0  Ref_Lib
    "Canon_I":  ["✓",    "✓",      "⚠",       "✗",      "✓",     "✓"],
    "Canon_II": ["✓",    "✓",      "⚠",       "✗",      "✓",     "✓"],
    "Canon_III":["⚠",    "⚠",      "✓",       "✓",      "✓",     "✓"],
    "Canon_IV": ["✗",    "✗",      "✓",       "✓",      "✓",     "⚠"],
    "Canon_0":  ["✓",    "✓",      "✓",       "✓",      "✓",     "✓"],
    "Ref_Lib":  ["✓",    "✓",      "✓",       "⚠",      "✓",     "✓"],
}
```

### 2.4 Nightly Relationship Discovery Pipeline

```
STAGE 1: Embed (02:00)
├─ Scan vault for new/modified documents since last run
├─ Scan _references/ for new/modified reference entries
├─ Generate embeddings (nomic-embed-text via Ollama)
├─ Store in ChromaDB — separate collections, shared embedding space
├─ Estimated time: ~2-5 minutes for 20 new items

STAGE 2: Cluster (02:10)
├─ HDBSCAN on COMBINED embedding space (vault + references)
├─ Parameters: min_cluster_size=3, min_samples=2, metric=cosine
├─ Flag clusters containing BOTH vault docs AND references
├─ Estimated time: <1 minute for corpus of ~700 items

STAGE 3: Label (02:15)
├─ Generate cluster labels via local LLM
├─ Compare against existing ontology categories
├─ For mixed clusters: generate cross-index connection summaries
├─ Estimated time: ~5-10 minutes

STAGE 4: Link (02:30)
├─ Check Firewall Matrix for each proposed relationship
├─ ✓ → Create wiki-link + update .ttl
├─ ⚠ → Create link with translation note
├─ ✗ → Route to _review/
├─ Log all actions to _audit/YYYY-MM-DD.md
├─ Estimated time: ~2-5 minutes

STAGE 5: Audit (02:40)
├─ Scan for orphaned references, stale links
├─ Check BibTeX consistency
├─ Flag uncited high-relevance references
├─ Estimated time: ~2-3 minutes

TOTAL: ~15-25 minutes
```

### 2.5 TTL Update Protocol

```turtle
# Staged commit: proposed → accepted/rejected
fi:NewConceptNode a fi:Concept ;
    fi:canon "III" ;
    fi:label "Acoustic Phase Transition Dynamics" ;
    fi:discoveredBy "argus_hdbscan_2026-02-24_c7" ;
    fi:confidence "0.72"^^xsd:float ;
    fi:status "proposed" ;
    fi:supportedBy fi:REF_2025_cheng_ultrasound ;
    fi:firewall_check "passed" .
```

---

## 3.0 SKILL 3: PVP-Micro Sentinel

### 3.1 Purpose

Lightweight automated PVP-Micro (3-stage Pattern Validation Protocol) on classified documents and proposed cross-references. Epistemological quality gate between Ontology Linker and vault commit.

### 3.2 Module Definition

```python
# argus/skills/pvp_sentinel.py
"""
PVP-Micro Sentinel — Skill 3

Automated PVP-Micro (3-stage) from Pattern Validation Protocol v3.1.
Validates Canon I falsifiability, checks Firewall compliance, flags
misclassification, and verifies citation coverage against Reference Library.
"""
```

### 3.3 Three-Stage Automated PVP-Micro

```
STAGE 1: DEFINE & HYPOTHESIZE
├─ Extract all claims from document
├─ For each claim: mathematically expressible? falsifiable? disproval criteria?
├─ Compare per-claim Canon to document-level Canon
└─ If mismatch > 30% → FLAG: likely misclassified

STAGE 2: TEST & FALSIFY
├─ For Canon I claims: evidence cited? primary/secondary? in Reference Library?
├─ For cross-Canon references: firewall compliant? translation present?
├─ For Reference Library citations: does cited paper actually support claim?
└─ Score: falsifiability_score, classification_confidence, citation_coverage

STAGE 3: REPORT WITH CAVEATS
├─ pvp_status: passed | flagged | escalate
├─ Scoring + missing references + suggested references from library
├─ Route: passed → commit / flagged → _review/ / escalate → Telegram alert
```

### 3.4 Scoring Thresholds

```yaml
pvp_micro_thresholds:
  pass:
    falsifiability_score: ">= 0.7"
    classification_confidence: ">= 0.8"
    firewall_violations: 0
    claim_canon_mismatch: "< 20%"
    citation_coverage: ">= 0.5"

  flag:
    falsifiability_score: "0.4 - 0.69"
    classification_confidence: "0.5 - 0.79"
    firewall_violations: "1-2 (non-critical)"
    claim_canon_mismatch: "20-50%"
    citation_coverage: "0.2 - 0.49"

  escalate:
    falsifiability_score: "< 0.4"
    classification_confidence: "< 0.5"
    firewall_violations: ">= 3 OR any critical"
    claim_canon_mismatch: "> 50%"
    citation_coverage: "< 0.2 for Canon I"
```

### 3.5 Prompt Template

Full PVP-Micro prompt stored at `argus/templates/pvp_sentinel.txt`. Includes all three stages with structured JSON output format. Includes top-5 Reference Library matches as context for citation coverage assessment. See v1.1 Section 3.5 for complete prompt text.

### 3.6 Computational Cost

```
Per document: ~30-90 seconds (local 8B model, RTX 2060)
Nightly batch (20 docs): ~10-25 minutes
VRAM: ~4.5GB
Impact: NEGLIGIBLE
```

---

## 4.0 SKILL 4: Helios Scout

### 4.1 Purpose

Nightly scan of research sources for new publications relevant to Institute domains. Newly discovered papers route to Reference Librarian (Skill 7) for full processing.

### 4.2 Module Definition

```python
# argus/skills/helios_scout.py
"""
Helios Scout — Skill 4

Automated scan of arXiv, PubMed, bioRxiv, and Google Scholar.
Classifies relevance, routes high-scoring papers to Reference Librarian.
Manual search via /scout [topic].
"""
```

### 4.3 Search Domains

Configured in `config/search_domains.yaml`:

```yaml
primary:
  - query: "neuromorphic computing memristor"
    sources: [arxiv, ieee]
    relevance_to: [FI-FDN-001b, FI-PAT-003]
  - query: "consciousness metrics integrated information"
    sources: [arxiv, pubmed]
    relevance_to: [FI-TFR-011, consciousness_metrics_patent]
  - query: "cymatic acoustic crystallization ice nucleation"
    sources: [arxiv, pubmed, google_scholar]
    relevance_to: [FI-EXP-003, fi-tfr-035]
  - query: "quantum biology coherence room temperature"
    sources: [arxiv, pubmed]
    relevance_to: [FI-TFR-005, FI-FDN-001c]
  - query: "DNA 3D organization chromatin spatial"
    sources: [pubmed, biorxiv]
    relevance_to: [FI-SYNTH-001, cellular-grammar-discovery-report]

secondary:
  - query: "fractal self-similarity complex systems emergence"
  - query: "spiking neural network neuromorphic hardware"
  - query: "bioelectric morphogenesis pattern formation"

exploratory:
  - query: "phase transition information processing"
  - query: "crystallization complexity emergence"
  - query: "resonance biological systems"
```

### 4.4 Relevance Scoring

```python
relevance_score = (
    0.40 * vault_cosine_sim +
    0.20 * reflib_cosine_sim +
    0.25 * keyword_overlap +
    0.15 * citation_overlap
)

# Routing:
# >= 0.7 → Full ingest via Reference Librarian
# 0.4-0.69 → Abstract-only entry + weekly digest
# < 0.4 → Log only
```

---

## 5.0 SKILL 5: Crystallization Relay

### 5.1 Purpose

Bridges CHIMERA Crystallization Engine with the vault. Processes voice notes, Telegram messages, and flow-state dictation into structured knowledge artifacts.

### 5.2 Module Definition

```python
# argus/skills/crystallization_relay.py
"""
Crystallization Relay — Skill 5

Receives raw insights from any input channel and processes through
three-tier architecture: Resonance Detection → Symbolic Encoding →
Archive Commit. Outputs markdown, JSON, and TTL artifacts.
"""
```

### 5.3 Processing Pipeline

```
INPUT: Raw insight (text, voice transcription, image description)

TIER 1: Resonance Detection
├─ Novelty score (embedding comparison against vault + Reference Library)
├─ Top-5 related vault documents + top-3 related references
└─ Output: resonance_profile { score, connections, novelty }

TIER 2: Symbolic Encoding
├─ Markdown summary (human-readable)
├─ JSON symbolic object (crystal_id, concepts, connections, scores)
├─ TTL annotation for ontology
└─ (Future) Visual glyph encoding

TIER 3: Archive Commit
├─ Route through Canon Classifier (Skill 1)
├─ If Canon I claim → route through PVP Sentinel (Skill 3)
├─ Commit to vault with full YAML frontmatter
└─ Telegram confirmation:
    "🔮 Crystallized: [insight]
     Canon: [N] | Resonance: [score] | Novelty: [score]
     Connected to: [top 3 docs]
     📚 Related refs: [top 2 references]"
```

---

## 6.0 SKILL 6: Morning Briefing

### 6.1 Purpose

Daily synthesis of overnight pipeline activity, research discoveries, vault health, and priorities.

### 6.2 Module Definition

```python
# argus/skills/morning_briefing.py
"""
Morning Briefing — Skill 6

Daily synthesis delivered via Telegram at 06:00. Aggregates results
from all overnight skills, Reference Library status, cross-index
discoveries, and suggested priorities. Uses frontier API for quality.
"""
```

### 6.3 Briefing Template

```markdown
☀️ FRACTALITY INSTITUTE — DAILY BRIEFING
📅 {date} | 🕐 Pipeline ran: {duration}

━━━ OVERNIGHT RESULTS ━━━

📥 INGESTED: {N} new Institute documents
{list with Canon assignments}

📚 REFERENCE LIBRARY: {N} new references processed
├─ Full ingest (high relevance): {N}
├─ Abstract only (moderate): {N}
├─ New connections discovered: {N}
└─ BibTeX entries synced: {N}

🔗 LINKS DISCOVERED: {N} new relationships
├─ Vault ↔ Vault: {N}
├─ Vault ↔ Reference: {N} (cross-index)
├─ Reference ↔ Reference: {N} (citation chains)
├─ Firewall warnings: {N}
└─ Blocked (needs review): {N}

🛡️ PVP SENTINEL: {N} documents scanned
├─ Passed: {N}
├─ Flagged: {N} → see _review/
├─ Under-referenced Canon I docs: {N}
└─ Escalated: {N} → ATTENTION NEEDED

🔬 HELIOS SCOUT: {N} papers discovered
├─ Sent to Reference Librarian: {N}
├─ In weekly digest: {N}
└─ Logged: {N}

━━━ VAULT HEALTH ━━━

📊 Institute Documents: {N}
├─ Canon I: {N} ({%}) | Canon II: {N} ({%})
├─ Canon III: {N} ({%}) | Canon IV: {N} ({%})
├─ Canon 0: {N} ({%}) | Unclassified: {N} ⚠️

📚 Reference Library: {N} entries
├─ Full records: {N} | Abstract-only: {N}
├─ Linked to vault: {N} ({%})
├─ Orphaned: {N} | BibTeX coverage: {%}

🕸️ Ontology: {N} concepts, {N} relationships
├─ Orphaned docs: {N} | Firewall violations: {N}
└─ Proposed new concepts: {N}

━━━ 🔥 CROSS-INDEX HIGHLIGHTS ━━━
{top_3_cross_index_discoveries}

━━━ SUGGESTED PRIORITIES ━━━
1. {priority_1}
2. {priority_2}
3. {priority_3}

━━━ QUOTE OF THE DAY ━━━
{rotating selection from Canon IV or wisdom traditions}
```

---

## 7.0 SKILL 7: Reference Librarian

### 7.1 Purpose

Ingests, processes, indexes, and maintains a comprehensive library of external research papers, preprints, frameworks, and reference materials. Creates structured Obsidian markdown entries with full metadata, embeddings for cross-index search, relevance mappings to Institute documents, and BibTeX synchronization.

This is the dragon's librarian. It doesn't hoard — it *indexes*.

### 7.2 Module Definition

```python
# argus/skills/reference_librarian.py
"""
Reference Librarian — Skill 7

Processes external research papers into a structured Reference Library.
Extracts metadata, generates embeddings, maps relevance to Institute
documents, classifies roles, and synchronizes with fractality_master.bib.

Key principle: External references SERVE the Canon system but are
NOT CLASSIFIED by it. They occupy a parallel index, not the Canon vault.

Capabilities:
- PDF text extraction with OCR fallback
- Metadata enrichment via CrossRef/Semantic Scholar/OpenAlex
- Vector embedding in shared space with vault documents
- Role-based relevance mapping (see Role Taxonomy)
- BibTeX synchronization with fractality_master.bib
- Citation chain discovery between reference library entries
- Duplicate detection (hash, DOI, fuzzy title+author)
"""
```

### 7.3 Vault Structure

```
vault/
├── _canon/                    # Institute documents (Track A)
│   ├── canon-I/
│   ├── canon-II/
│   ├── canon-III/
│   ├── canon-IV/
│   └── canon-0/
├── _references/               # Reference Library (Track B)
│   ├── by-domain/
│   │   ├── quantum-biology/
│   │   ├── neuromorphic-computing/
│   │   ├── consciousness/
│   │   ├── materials-science/
│   │   ├── neuroscience/
│   │   ├── mathematics/
│   │   ├── astrophysics/
│   │   └── _uncategorized/
│   ├── by-year/
│   ├── _citation-chains/
│   └── _stale/
├── _pdfs/
│   ├── institute/
│   └── external/
├── _inbox/
│   └── references/            # Drop zone for new PDFs
├── _review/
├── _audit/
│   └── argus/                 # Argus-specific audit logs
├── _bootstrap/
└── fractality_master.bib
```

### 7.4 Reference Entry Format

```yaml
---
ref_id: "REF-YYYY-AAAA-keyword"
type: "external_reference"
status: "active"  # active | stale | superseded | retracted

# ─── Bibliographic Metadata ───
title: "Full paper title"
authors:
  - family: "Smith"
    given: "John A."
    orcid: "0000-0000-0000-0000"
journal: "Nature Communications"
volume: "16"
year: 2025
doi: "10.1038/s41467-025-XXXXX"
pmid: ""
arxiv_id: ""
open_access: true

# ─── Content ───
abstract: |
  Full abstract text.
keywords: ["keyword1", "keyword2"]
key_findings: []

# ─── Files ───
pdf_path: "_pdfs/external/filename.pdf"
pdf_hash: "sha256:abc123..."
extraction_quality: "high"

# ─── Relevance ───
relevance_score: 0.82
domain_tags: ["quantum-biology"]
relevant_to:
  - document: "FI-TFR-011"
    role: "empirical_support"
    strength: 0.85
    note: "Provides evidence for quantum coherence in biological systems"

# ─── Bibliography Sync ───
bibtex_key: "smith2025quantum"
bibtex_synced: true
cited_by_fi_documents: ["FI-TFR-011"]
cites_in_reflib: ["REF-2007-engel-wavelike"]
cited_by_in_reflib: []

# ─── Processing ───
date_ingested: "2026-02-24"
ingestion_source: "manual"
embedding_id: "emb_ref_0042"
---

## Summary
[3-5 sentence summary focused on Institute research relevance]

## Relevance to Institute Research
[Connection analysis organized by strength]

## Contradictions or Tensions
[Where this paper pushes back on Institute claims — these are GOLD]

## Key Data Points
[Specific numbers/measurements for citation in Institute documents]

## Citation
\```bibtex
@article{smith2025quantum, ... }
\```
```

### 7.5 Role Taxonomy

Configured in `config/role_taxonomy.yaml`:

```yaml
# ─── Evidential Roles (strongest epistemic weight) ───
empirical_support:
  description: "Direct experimental evidence for an Institute claim"
  valid_for_canons: [I, II]

empirical_contradiction:
  description: "Experimental evidence against an Institute claim"
  valid_for_canons: [I, II, III]
  priority: "HIGH"  # Flagged in morning briefing

replication:
  description: "Replicates/fails to replicate a cited experiment"
  valid_for_canons: [I]

# ─── Engineering Roles ───
engineering_precedent:
  description: "Technical approach relevant to an Institute design"
  valid_for_canons: [II]

feasibility_evidence:
  description: "Evidence that an Institute engineering goal is achievable"
  valid_for_canons: [II]

# ─── Theoretical Roles ───
theoretical_parallel:
  description: "Framework structurally similar to an Institute theory"
  valid_for_canons: [III]

theoretical_foundation:
  description: "Established theory that Institute framework builds upon"
  valid_for_canons: [III]

theoretical_challenge:
  description: "Arguments/evidence challenging an Institute theory"
  valid_for_canons: [III]
  priority: "HIGH"

# ─── Contextual Roles ───
methodological_reference:
  description: "Methods/tools usable in Institute research"
  valid_for_canons: [I, II]

domain_context:
  description: "Background understanding of a relevant field"
  valid_for_canons: [I, II, III]

inspiration:
  description: "Sparked an idea — NOT evidence for Canon I claims"
  valid_for_canons: [III, IV]
  note: "CANNOT be used as evidence for Canon I claims"
```

### 7.6 Processing Pipeline

```
STAGE 1: ACQUISITION
├─ PDF → _pdfs/external/, SHA-256 hash → duplicate detection
├─ DOI → CrossRef/Semantic Scholar metadata
├─ Duplicate found → link to existing, STOP

STAGE 2: EXTRACTION
├─ Primary: pymupdf | Fallback: pdftotext | Nuclear: Tesseract OCR
├─ Extract: title, authors, abstract, keywords, references
├─ Enrich via APIs (CrossRef, Semantic Scholar, OpenAlex)

STAGE 3: ANALYSIS
├─ Embedding: nomic-embed-text (abstract + title + keywords)
├─ Summary: local LLM (Institute-context-aware)
├─ Key findings: structured extraction

STAGE 4: RELEVANCE MAPPING
├─ Cosine similarity against vault + existing references
├─ Keyword overlap with Fractality Ontology
├─ Citation overlap with fractality_master.bib
├─ Role classification for each connection (Role Taxonomy)

STAGE 5: DOMAIN CLASSIFICATION
├─ Assign to domain folder(s)

STAGE 6: BIBLIOGRAPHY SYNC
├─ Match/create BibTeX entry in fractality_master.bib
├─ Build citation chain links

STAGE 7: COMMIT
├─ Generate markdown reference entry
├─ Save to _references/, add to vector store
├─ Update supporting_references in connected vault docs
├─ Telegram confirmation
```

### 7.7 Duplicate Detection

Four-level cascade: exact hash → DOI match → arXiv ID match → fuzzy title+author (threshold 0.90). See v1.1 Section 7.7 for full implementation specification.

### 7.8 Telegram Query Interface

```
/ref-search [query]        Semantic search across Reference Library
/ref-add [DOI or path]     Manually trigger ingestion
/ref-for [FI-doc-ID]       References connected to a specific document
/ref-chain [REF-ID]        Citation chain visualization
/ref-gaps                  Under-referenced Canon I documents
/ref-contradictions        Papers that challenge Institute claims
/ref-stale                 Disconnected references (90+ days)
/ref-stats                 Library health metrics
```

### 7.9 Computational Cost

```
Per reference (full pipeline): ~60-120 seconds
Bulk import (50 papers): ~50-100 minutes (overnight)
Nightly maintenance: ~10-25 minutes
VRAM: ~4.5GB (shared with other skills)
```

---

## 8.0 CRON SCHEDULE

```
TIME    SKILL                   MODEL         EST. DURATION
─────────────────────────────────────────────────────────────
01:00   Helios Scout            web + local    15-30 min
01:30   Reference Librarian     local + API    10-25 min
02:00   Ontology Enforcer       local          15-25 min
03:00   PVP-Micro Sentinel      local          10-25 min
03:30   Vault Health Check      local          5-10 min
06:00   Morning Briefing        frontier API   2-5 min

ON-DEMAND (real-time via Telegram):
        /classify               local          30-60 sec/doc
        /ref-add                local + API    60-120 sec/ref
        /crystallize            frontier+local 1-2 min
        /pvp-check              local          30-60 sec
        /audit-ontology         local          5-10 min
        /scout [topic]          web + local    5-15 min
        /ref-search [query]     local          5-10 sec
        /briefing               frontier API   1-2 min

TOTAL NIGHTLY PIPELINE: ~70-140 minutes (01:00 → ~03:30)
```

---

## 9.0 HARDWARE REQUIREMENTS

### Minimum (ASUS TUF — Current Setup)

```
CPU:  Ryzen 7 4800H (8C/16T)          ✓ Sufficient for all pipelines
GPU:  RTX 2060 (6GB VRAM)             ✓ Runs 8B Q4 models comfortably
RAM:  16GB                             ⚠ 32GB recommended
SSD:  512GB+ NVMe                     ⚠ Monitor vault + model + PDF storage
OS:   Ubuntu 24.04 LTS                ✓
```

### Recommended (Future Dedicated Server)

```
CPU:  Ryzen 7 7735HS (mini PC)        Always-on, low power (~25-45W idle)
GPU:  None needed                      CPU inference for batch
RAM:  64GB DDR5                        Headroom for vector DB + PDF processing
SSD:  2TB NVMe                         Models + vault + reference library
Cost: ~$400-600
```

### Network

```
Tailscale:  VPN mesh — laptop ↔ phone ↔ (future) mini PC
Telegram:   Primary mobile interface
Cellular:   Intermittent connectivity OK — jobs queue locally
Web APIs:   CrossRef, Semantic Scholar, OpenAlex (free tiers)
```

---

## 10.0 IMPLEMENTATION ROADMAP

```
PHASE 1 (Week 1-2): Foundation
├─ Install Ubuntu on ASUS TUF (or dual-boot)
├─ Install Python 3.11+, create argus virtualenv
├─ Install Ollama, pull mistral-nemo:8b-q4 + nomic-embed-text
├─ Set up Tailscale (laptop ↔ phone)
├─ Create argus/ project structure
├─ Implement argus.py, telegram_bot.py, ollama_client.py
├─ Create Telegram bot via @BotFather, configure token
├─ Test: send /argus status from phone → get response
└─ Deliverable: Working daemon accessible from truck cab

PHASE 2 (Week 3-4): Canon Classifier
├─ Implement canon_classifier.py
├─ Write classification prompt template
├─ Bulk import existing FI-documents (130+)
├─ Test accuracy against known Canon assignments
├─ Implement three-tier bootstrap triage
├─ Human review session for Tier 3 items (2-3 hours at home)
└─ Deliverable: All existing documents classified and in vault

PHASE 3 (Week 5-6): Ontology Engine + Vector Store
├─ Implement ontology_enforcer.py + vector_store.py + embedding.py
├─ Set up ChromaDB local instance
├─ Port Fractality_Ontology_QuantumEnhanced.ttl
├─ Implement Firewall Matrix from config/firewall_matrix.yaml
├─ Test HDBSCAN clustering on existing corpus
├─ Configure APScheduler for nightly runs
└─ Deliverable: Automated nightly relationship discovery

PHASE 4 (Week 7-8): PVP Sentinel
├─ Implement pvp_sentinel.py
├─ Write PVP-Micro prompt template
├─ Test against known Canon I docs (should pass)
├─ Test against known misclassified docs (should flag)
├─ Calibrate scoring thresholds
└─ Deliverable: Automated epistemological quality gate

PHASE 5a (Week 9-10): Research & Crystallization
├─ Implement helios_scout.py with search domain config
├─ Implement crystallization_relay.py
├─ Test voice-to-vault pipeline from phone
├─ Implement morning_briefing.py
└─ Deliverable: Core pipeline operational

PHASE 5b (Week 10-12): Reference Librarian
├─ Implement reference_librarian.py + pdf_extractor.py
├─ Implement metadata_enricher.py (CrossRef/S2/OpenAlex)
├─ Implement duplicate_detector.py + bibtex_sync.py
├─ Build role taxonomy from config/role_taxonomy.yaml
├─ Bulk import existing PDF collection (~35-50 papers)
│   ├─ Overnight bootstrap run
│   ├─ Reconcile with fractality_master.bib
│   └─ Human review (1-2 hours)
├─ Wire: Helios Scout → Reference Librarian routing
├─ Wire: Reference Library → Ontology Enforcer cross-indexing
├─ Wire: Reference Library → PVP Sentinel citation checks
├─ Test /ref-search and /ref-for from phone
├─ Test Telegram PDF drop → auto-ingest
└─ Deliverable: Full dual-track pipeline with cross-index discovery

PHASE 6 (Ongoing): Optimization
├─ Monitor performance, tune thresholds
├─ Consider fine-tuning small model on Canon schema
├─ Evaluate dedicated server purchase timing
├─ Expand Helios Scout search domains
├─ Citation chain analysis and gap identification
├─ Begin PVP-Lite automation for high-value documents
└─ Write tests (tests/ directory)
```

---

## 11.0 SECURITY CONSIDERATIONS

### 11.1 Threat Model

```
ASSETS TO PROTECT:
├─ Patent-pending IP (consciousness metrics, neuromorphic hardware)
├─ Unpublished theoretical frameworks
├─ Experimental protocols and preliminary data
├─ Personal communications and collaborator information
├─ AI chat histories containing research development
└─ Reference Library metadata (reveals research direction)

THREAT VECTORS:
├─ Supply chain (Python dependencies)
│   └─ MITIGATION: Pin all versions in requirements.txt. Only 8-9 direct
│       dependencies, all from established, auditable projects. No plugin
│       marketplace. No dynamic skill installation. No third-party modules.
│       Compare: OpenClaw had 200+ transitive dependencies and CVE-2026-25253.
│       Argus has a dependency tree you can read on a single screen.
├─ Prompt injection via ingested content
│   └─ MITIGATION: Sandboxed processing. Ingested content (especially PDFs)
│       treated as untrusted input. Extracted text never passed to shell.
│       LLM outputs parsed as structured data, never executed.
├─ Network exposure
│   └─ MITIGATION: Tailscale only. No public endpoints. Telegram Bot API
│       is outbound-only (Argus polls Telegram; Telegram never reaches Argus).
├─ LLM data leakage (frontier API calls)
│   └─ MITIGATION: Route sensitive content through local Ollama only.
│       Frontier APIs receive sanitized queries without patent specifics.
├─ Metadata leakage via reference APIs
│   └─ MITIGATION: CrossRef/Semantic Scholar queries use DOIs only.
│       Queries reveal which papers interest you, but not why.
│       Acceptable risk for publicly available metadata.
│       Disable API enrichment for stealth mode (local extraction only).
└─ Physical access to hardware
    └─ MITIGATION: Full disk encryption. Auto-lock. Encrypted secrets.yaml.
```

### 11.2 Content Routing

```yaml
content_routing:
  local_only:
    - Patent drafts and claims
    - Unpublished experimental data
    - Personal health/biometric data
    - Financial information
    - Collaborator contact details
    - Relevance mapping outputs (reveals research strategy)

  frontier_api_permitted:
    - Published preprints (already public)
    - General theoretical questions (no IP specifics)
    - Morning briefing generation (summaries only)
    - Crystallization relay (distilled insights; raw stays local)
    - Reference Library summaries (papers are public)

  external_api_permitted:
    - CrossRef (DOI → metadata)
    - Semantic Scholar (paper → citations)
    - OpenAlex (paper → concepts)
    # NOTE: Never include Institute document IDs or Canon context in queries

  never_transmitted:
    - Encryption keys and API tokens
    - Dead Man's Switch configurations
    - Full patent application text
    - Relevance maps linking papers to patents
```

### 11.3 Why Not OpenClaw (Decision Record)

```
DATE: 2026-02-24
DECISION: Replace OpenClaw with custom Argus daemon
RATIONALE:
  1. OpenClaw acquired by OpenAI (2026-02-15). Creator joined OpenAI.
     Project moved to "independent" foundation with OpenAI sponsorship
     and potential influence over direction.
  2. 430,000+ lines of code — unauditable by a single researcher.
  3. CVE-2026-25253 — authentication token exposure vulnerability.
  4. Extensible plugin architecture = supply chain attack surface.
  5. Institute protects pre-patent IP that cannot be exposed to any
     corporate-influenced infrastructure.
  6. Argus requires ~3,000-4,000 lines — fully auditable, zero
     corporate dependency, purpose-built for one use case.
STATUS: PERMANENT. This decision is not revisited unless a fully
  open-source, auditable, community-governed alternative emerges
  with no corporate sponsorship from OpenAI, Meta, or Google.
```

---

*"Truth emerges not from certainty, but from the rigorous quantification of uncertainty."*

**— The Fractality Institute**

---

**Cross-Canon Dependencies:**
- Canon I: PVP v3.1 (FI-MP-004-v3.0, FI-PVP-v3_1.tex) — Sentinel logic
- Canon I: fractality_master.bib — Bibliography synchronization target
- Canon II: CHIMERA Architecture (chimera-v07-cognitive.py) — Crystallization Engine
- Canon II: Fractality_Ontology_QuantumEnhanced.ttl — Ontology integration
- Canon 0: Canon Protocol Charter (FI-C-002) — Classification criteria, Firewall Principle
- Canon 0: Helios Protocol (FI-KI-001) — Research ingestion concept
- Canon 0: Inter-Canon Translation Protocol (FI-CTP-001) — Role taxonomy design

**Required Software:**
- Python 3.11+: https://python.org
- Ollama: https://ollama.ai
- Tailscale: https://tailscale.com
- Telegram Bot API: https://core.telegram.org/bots/api
- ChromaDB: https://docs.trychroma.com
- PyMuPDF: https://pymupdf.readthedocs.io
- CrossRef API: https://api.crossref.org
- Semantic Scholar API: https://api.semanticscholar.org
- OpenAlex API: https://docs.openalex.org
