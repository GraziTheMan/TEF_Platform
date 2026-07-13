"""
SQLite store — classifications, document registry, and credit ledger.

Chosen for zero setup (a single file, stdlib driver). The schema is
deliberately graph-friendly (documents + contributions as edges) so it can
be mirrored into Neo4j later per TEF-ARGUS-001 §12.4 without reshaping data.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import Classification, Contribution
from .taxonomy import DOMAINS

_SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    document_id   TEXT PRIMARY KEY,
    title         TEXT,
    tier          TEXT,
    domain        TEXT,
    status        TEXT,
    source_path   TEXT,
    confidence    REAL,
    method        TEXT,
    flags         TEXT,
    updated_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS contributions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id   TEXT,
    source_path   TEXT,
    contributor   TEXT,
    action        TEXT,
    tier          TEXT,
    domain        TEXT,
    originating_ai TEXT,
    commit_sha    TEXT,
    timestamp     TEXT
);

CREATE TABLE IF NOT EXISTS id_counters (
    prefix        TEXT PRIMARY KEY,
    next_num      INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS consistency_findings (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id    TEXT,
    established_fact TEXT,
    document_claim TEXT,
    severity       TEXT,
    explanation    TEXT,
    checked_at     TEXT DEFAULT (datetime('now'))
);
"""


class Store:
    def __init__(self, db_path: Path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(_SCHEMA)
        self._migrate()
        self.conn.commit()

    def _migrate(self) -> None:
        # Add columns that may be missing on DBs created by earlier versions.
        cols = {r["name"] for r in self.conn.execute("PRAGMA table_info(documents)")}
        if "consistency_status" not in cols:
            self.conn.execute(
                "ALTER TABLE documents ADD COLUMN consistency_status TEXT DEFAULT 'pending'")

    # ── ID allocation ──────────────────────────────────────────────
    def allocate_id(self, domain_id: str) -> str:
        prefix = DOMAINS[domain_id].prefix
        cur = self.conn.execute("SELECT next_num FROM id_counters WHERE prefix=?", (prefix,))
        row = cur.fetchone()
        num = row["next_num"] if row else 1
        # skip past any reserved seed IDs already in documents
        while self._id_taken(f"{prefix}-{num:03d}"):
            num += 1
        self.conn.execute(
            "INSERT INTO id_counters(prefix, next_num) VALUES(?, ?) "
            "ON CONFLICT(prefix) DO UPDATE SET next_num=excluded.next_num",
            (prefix, num + 1),
        )
        self.conn.commit()
        return f"{prefix}-{num:03d}"

    def _id_taken(self, doc_id: str) -> bool:
        cur = self.conn.execute("SELECT 1 FROM documents WHERE document_id=?", (doc_id,))
        return cur.fetchone() is not None

    # ── Documents ──────────────────────────────────────────────────
    def upsert_document(self, c: Classification) -> None:
        self.conn.execute(
            """INSERT INTO documents
               (document_id, title, tier, domain, status, source_path,
                confidence, method, flags, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?, datetime('now'))
               ON CONFLICT(document_id) DO UPDATE SET
                 title=excluded.title, tier=excluded.tier, domain=excluded.domain,
                 status=excluded.status, source_path=excluded.source_path,
                 confidence=excluded.confidence, method=excluded.method,
                 flags=excluded.flags, updated_at=datetime('now')""",
            (c.document_id, c.title, c.tier, c.domain_primary, c.development_status,
             c.source_path, c.confidence, c.method, ",".join(c.flags)),
        )
        self.conn.commit()

    def record_contribution(self, c: Contribution) -> None:
        self.conn.execute(
            """INSERT INTO contributions
               (document_id, source_path, contributor, action, tier, domain,
                originating_ai, commit_sha, timestamp)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (c.document_id, c.source_path, c.contributor, c.action, c.tier,
             c.domain, c.originating_ai, c.commit, c.timestamp),
        )
        self.conn.commit()

    # ── Consistency ────────────────────────────────────────────────
    def list_documents(self) -> list[dict]:
        cur = self.conn.execute(
            "SELECT document_id, title, tier, domain, source_path FROM documents "
            "ORDER BY document_id")
        return [dict(r) for r in cur.fetchall()]

    def set_consistency_status(self, document_id: str, status: str) -> None:
        self.conn.execute(
            "UPDATE documents SET consistency_status=? WHERE document_id=?",
            (status, document_id))
        self.conn.commit()

    def record_consistency_findings(self, document_id: str, findings) -> None:
        # Replace prior findings for this document, then insert current ones.
        self.conn.execute("DELETE FROM consistency_findings WHERE document_id=?",
                          (document_id,))
        for f in findings:
            self.conn.execute(
                """INSERT INTO consistency_findings
                   (document_id, established_fact, document_claim, severity, explanation)
                   VALUES (?,?,?,?,?)""",
                (document_id, f.established_fact, f.document_claim, f.severity, f.explanation))
        self.conn.commit()

    def consistency_summary(self) -> dict[str, int]:
        cur = self.conn.execute(
            "SELECT consistency_status s, COUNT(*) n FROM documents GROUP BY consistency_status")
        return {r["s"] or "pending": r["n"] for r in cur.fetchall()}

    # ── Reads ──────────────────────────────────────────────────────
    def tier_counts(self) -> dict[str, int]:
        cur = self.conn.execute("SELECT tier, COUNT(*) n FROM documents GROUP BY tier")
        return {r["tier"]: r["n"] for r in cur.fetchall()}

    def credit_summary(self) -> list[tuple[str, int]]:
        cur = self.conn.execute(
            "SELECT contributor, COUNT(*) n FROM contributions GROUP BY contributor "
            "ORDER BY n DESC")
        return [(r["contributor"], r["n"]) for r in cur.fetchall()]

    def close(self) -> None:
        self.conn.close()
