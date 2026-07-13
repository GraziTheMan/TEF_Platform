"""
Argus CLI — first-slice commands.

  py -m argus classify           # dry run: show the classification plan
  py -m argus classify --apply   # write frontmatter + record credit
  py -m argus classify --no-llm  # force heuristic path
  py -m argus status             # tier counts + credit summary
"""

from __future__ import annotations

import argparse
import sys

from .classify import Classifier
from .config import Config
from .llm import OllamaClient
from .pipeline import Pipeline
from .store import Store
from .taxonomy import TIERS


def _build(config: Config, use_llm: bool) -> tuple[Classifier, Store]:
    llm = None
    if use_llm and config.use_llm:
        candidate = OllamaClient(config.ollama_base_url, config.ollama_model)
        llm = candidate if candidate.available() else None
    classifier = Classifier(llm=llm, prompt_path=config.prompt_path)
    store = Store(config.db_path)
    return classifier, store


def _print_plan(items) -> None:
    print(f"\n{'ID':<16} {'TIER':<4} {'DOMAIN':<6} {'CONF':<5} {'METHOD':<9} TITLE")
    print("-" * 92)
    for it in items:
        c = it.classification
        flag = " [!]" if c.flags else ""
        print(f"{c.document_id:<16} {c.tier:<4} {c.domain_primary:<6} "
              f"{c.confidence:<5.2f} {c.method:<9} {c.title[:40]}{flag}")
    # tier tally
    tally: dict[str, int] = {}
    for it in items:
        tally[it.classification.tier] = tally.get(it.classification.tier, 0) + 1
    print("-" * 92)
    print("Tier tally: " + "  ".join(f"{t}={tally.get(t,0)}" for t in TIERS))
    print(f"Total: {len(items)} documents")


def cmd_classify(args) -> int:
    config = Config.load()
    classifier, store = _build(config, use_llm=not args.no_llm)
    backend = "LLM (Ollama)" if classifier.llm else "heuristic (no Ollama)"
    print(f"Argus classify — vault: {config.vault_path}")
    print(f"Backend: {backend}")
    if not config.vault_path.exists():
        print(f"ERROR: vault path does not exist: {config.vault_path}", file=sys.stderr)
        return 2
    pipeline = Pipeline(config, classifier, store)
    items = pipeline.plan()
    _print_plan(items)
    if args.apply:
        pipeline.apply(items)
        print(f"\n✅ Applied. Wrote frontmatter to {len(items)} files and recorded credit.")
        print(f"   DB: {config.db_path}")
    else:
        print("\n(dry run — no files changed. Re-run with --apply to write.)")
    store.close()
    return 0


def cmd_status(args) -> int:
    config = Config.load()
    store = Store(config.db_path)
    print(f"Argus status — DB: {config.db_path}\n")
    counts = store.tier_counts()
    if not counts:
        print("No documents classified yet. Run: py -m argus classify --apply")
    else:
        print("Documents by tier:")
        for t, tier in TIERS.items():
            print(f"  {t} {tier.name:<22} {counts.get(t, 0)}")
        print("\nCredit (contributions by contributor):")
        for name, n in store.credit_summary():
            print(f"  {name:<28} {n}")
    store.close()
    return 0


def main(argv=None) -> int:
    # Windows consoles default to cp1252; force UTF-8 so glyphs don't crash.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(prog="argus", description="Argus TEF engine")
    sub = parser.add_subparsers(dest="command", required=True)

    p_classify = sub.add_parser("classify", help="classify vault documents")
    p_classify.add_argument("--apply", action="store_true",
                            help="write frontmatter and record credit")
    p_classify.add_argument("--no-llm", action="store_true",
                            help="force the heuristic path even if Ollama is up")
    p_classify.set_defaults(func=cmd_classify)

    p_status = sub.add_parser("status", help="show tier counts and credit")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
