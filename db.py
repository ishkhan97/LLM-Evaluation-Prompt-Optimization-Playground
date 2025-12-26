# db.py
import sqlite3
from datetime import datetime
from typing import Optional


DB_NAME = "llm_eval.db"


def get_connection():
    """Create a database connection."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            model TEXT NOT NULL,
            output TEXT NOT NULL,
            latency_ms REAL,
            tokens INTEGER,
            cost REAL,
            rating INTEGER,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def insert_run(
    prompt: str,
    model: str,
    output: str,
    latency_ms: float,
    tokens: int,
    cost: float,
    rating: Optional[int] = None,
):
    """Insert a single LLM run into the database."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO runs (
            prompt,
            model,
            output,
            latency_ms,
            tokens,
            cost,
            rating,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            prompt,
            model,
            output,
            latency_ms,
            tokens,
            cost,
            rating,
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def fetch_runs(limit: int = 100):
    """Fetch recent LLM runs."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            prompt,
            model,
            output,
            latency_ms,
            tokens,
            cost,
            rating,
            created_at
        FROM runs
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows
