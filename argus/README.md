# Argus — TEF Engine

The framework-independent core of Argus for The Extended Fractiverse:
classification, credit, and (soon) consistency + ontology logic. Frontends
(local CLI/Telegram, GitHub Action) wire onto this engine without changing it.

Specs: [`../docs/TEF-ARGUS-001_v1_0.md`](../docs/TEF-ARGUS-001_v1_0.md),
[`../docs/FI-ARGUS-001_v2.0.md`](../docs/FI-ARGUS-001_v2.0.md).

## What works now (first slice)

- **Lore classifier** — assigns each vault document a Lore Tier (T0–T4, IL) and
  Content Domain (CHAR, META, TECH, …) per TEF-ARGUS-001 §2, allocates a
  `TEF-<DOMAIN>-<NNN>` ID, and writes the §2.4 frontmatter schema.
  - *Seed match* for canonical entities (§11), *heuristic* keyword scoring as
    the no-model floor, and an *Ollama LLM* path used automatically when a
    local server is reachable.
- **Credit ledger** — SQLite store of documents + contributions (who/what/tier),
  graph-shaped for a future Neo4j mirror (§12.4).

## Setup

```bash
pip install -r ../requirements-argus.txt
```

Ollama is optional. Without it, classification uses the deterministic heuristic
path. With it (default model `mistral-nemo:latest` at `localhost:11434`), the
LLM path is used automatically.

## Usage

```bash
py -m argus classify            # dry run — print the classification plan
py -m argus classify --apply    # write frontmatter + record credit
py -m argus classify --no-llm   # force heuristic path
py -m argus status              # tier counts + credit summary
```

Config lives in `../argus_config.yaml` (optional; sensible defaults point at the
sibling `TheExtendedFractiverse` checkout).

## Layout

```
argus/
├── taxonomy.py     # Lore Tiers + Content Domains (§2.1, §2.2)
├── seeds.py        # canonical entity IDs (§11)
├── classify/       # heuristic + LLM orchestration (§2.3)
├── llm/            # backend abstraction (Ollama today)
├── frontmatter.py  # YAML frontmatter read/write (§2.4)
├── store.py        # SQLite: documents + credit ledger
├── pipeline.py     # scan → classify → allocate ID → apply
└── cli.py          # command-line face
```

## Not yet built

Consistency Sentinel (§6), Ontology Enforcer, Influence Library ingest (§4),
cross-vault discovery (§8), the Telegram and GitHub-Action frontends.
