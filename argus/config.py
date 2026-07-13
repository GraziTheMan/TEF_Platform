"""
Configuration loader.

Reads argus_config.yaml if present, else uses defaults tuned for this repo
layout (vault as a sibling checkout of TheExtendedFractiverse).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent          # TEF_Platform/
DEFAULT_VAULT = REPO_ROOT.parent / "TheExtendedFractiverse"  # sibling checkout


@dataclass
class Config:
    vault_path: Path = DEFAULT_VAULT
    db_path: Path = REPO_ROOT / "argus" / "data" / "argus.db"
    prompt_path: Path = REPO_ROOT / "argus" / "prompts" / "lore_classifier.txt"
    consistency_prompt_path: Path = REPO_ROOT / "argus" / "prompts" / "consistency_sentinel.txt"
    consistency_rules_path: Path = REPO_ROOT / "argus" / "config" / "tef_consistency_rules.yaml"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral-nemo:latest"
    use_llm: bool = True
    ingest_dirs: list[str] = field(default_factory=lambda: ["-unsorted"])

    @classmethod
    def load(cls, path: Path | None = None) -> "Config":
        cfg = cls()
        path = path or (REPO_ROOT / "argus_config.yaml")
        if path.exists():
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if "vault_path" in data:
                cfg.vault_path = Path(data["vault_path"]).expanduser()
            if "db_path" in data:
                cfg.db_path = Path(data["db_path"]).expanduser()
            ollama = data.get("ollama", {})
            cfg.ollama_base_url = ollama.get("base_url", cfg.ollama_base_url)
            cfg.ollama_model = ollama.get("model", cfg.ollama_model)
            cfg.use_llm = data.get("use_llm", cfg.use_llm)
            cfg.ingest_dirs = data.get("ingest_dirs", cfg.ingest_dirs)
        return cfg
