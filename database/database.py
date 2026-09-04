"""SQLite connection helper + schema initialization for RecoverAI."""

import sqlite3
import os
from config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS audit_trail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_time TEXT,
    payment_id TEXT,
    customer_id TEXT,
    amount REAL,
    risk_score REAL,
    risk_level TEXT,
    root_cause TEXT,
    recovery_probability REAL,
    model_used TEXT,
    recommended_action TEXT,
    expected_value REAL,
    policy_approved INTEGER,
    final_action TEXT,
    policy_reasons TEXT,
    outcome TEXT
);
"""


def get_connection():
    os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    conn = sqlite3.connect(settings.DB_PATH)
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized -> {settings.DB_PATH}")
