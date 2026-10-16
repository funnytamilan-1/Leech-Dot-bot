"""Local verification state for Leech Dot Bot.

Made by @Code_Dots · Partner: @CodeRips.
The SQLite file is runtime data and must never be committed to source control.
"""

import hashlib
from contextlib import closing
import os
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(
    os.environ.get("CODE_DOT_DATA_DIR", "Code_dot/database")
) / "verification.sqlite3"


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS pending_tokens (
            token_hash TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at REAL NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS verified_users (
            user_id INTEGER PRIMARY KEY,
            expires_at REAL NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS completion_proofs (
            token_hash TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expires_at REAL NOT NULL
        )
        """
    )
    return connection


def issue_token(token: str, user_id: int, ttl: int) -> None:
    """Store only a hash of a user-bound, expiring verification token."""
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = time.time()
    with closing(_connect()) as connection, connection:
        connection.execute("DELETE FROM pending_tokens WHERE expires_at <= ?", (now,))
        connection.execute("DELETE FROM completion_proofs WHERE expires_at <= ?", (now,))
        connection.execute(
            "INSERT OR REPLACE INTO pending_tokens(token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (token_hash, int(user_id), now + max(60, int(ttl))),
        )


def record_completion_proof(token: str, user_id: int, ttl: int) -> bool:
    """Record provider-verified completion for a pending user-bound token.

    Call this only after a trusted provider callback/signature has been checked.
    A browser redirect or Telegram deep-link return is not a completion proof.
    """
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = time.time()
    with _connect() as connection:
        row = connection.execute(
            "SELECT user_id, expires_at FROM pending_tokens WHERE token_hash = ?",
            (token_hash,),
        ).fetchone()
        if not row or int(row[0]) != int(user_id) or float(row[1]) <= now:
            return False
        connection.execute(
            "INSERT OR REPLACE INTO completion_proofs(token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (token_hash, int(user_id), min(float(row[1]), now + max(60, int(ttl)))),
        )
        return True


def consume_token(token: str, user_id: int) -> bool:
    """Consume a token once, only after trusted completion proof for its owner."""
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = time.time()
    with _connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT user_id, expires_at FROM pending_tokens WHERE token_hash = ?",
            (token_hash,),
        ).fetchone()
        proof = connection.execute(
            "SELECT user_id, expires_at FROM completion_proofs WHERE token_hash = ?",
            (token_hash,),
        ).fetchone()
        if not row or not proof:
            return False
        if int(row[0]) != int(user_id) or int(proof[0]) != int(user_id):
            # A wrong user must not consume or invalidate the legitimate user's token.
            return False
        if float(row[1]) <= now or float(proof[1]) <= now:
            connection.execute("DELETE FROM pending_tokens WHERE token_hash = ?", (token_hash,))
            connection.execute("DELETE FROM completion_proofs WHERE token_hash = ?", (token_hash,))
            return False
        connection.execute("DELETE FROM pending_tokens WHERE token_hash = ?", (token_hash,))
        connection.execute("DELETE FROM completion_proofs WHERE token_hash = ?", (token_hash,))
        return True


def mark_verified(user_id: int, ttl: int) -> None:
    """Persist the verification window for a user."""
    with _connect() as connection:
        connection.execute(
            "INSERT OR REPLACE INTO verified_users(user_id, expires_at) VALUES (?, ?)",
            (int(user_id), time.time() + max(60, int(ttl))),
        )


def is_verified(user_id: int) -> bool:
    """Return whether a user's verification window is still active."""
    now = time.time()
    with _connect() as connection:
        row = connection.execute(
            "SELECT expires_at FROM verified_users WHERE user_id = ?", (int(user_id),)
        ).fetchone()
        if not row:
            return False
        if float(row[0]) <= now:
            connection.execute("DELETE FROM verified_users WHERE user_id = ?", (int(user_id),))
            return False
        return True
