import os
import sqlite3
from datetime import datetime


DB_PATH = "database/audit.db"


def initialize_database():
    """Create audit database and transaction table."""

    os.makedirs("database", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaction_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            amount REAL,
            hour INTEGER,
            transactions_last_hour INTEGER,
            is_new_device INTEGER,
            is_international INTEGER,
            failed_attempts INTEGER,
            ml_probability REAL,
            risk_score REAL,
            decision TEXT
        )
    """)

    connection.commit()
    connection.close()


def log_transaction(
    amount,
    hour,
    transactions_last_hour,
    is_new_device,
    is_international,
    failed_attempts,
    ml_probability,
    risk_score,
    decision
):
    """Save analyzed transaction into audit database."""

    initialize_database()

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transaction_audit (
            timestamp,
            amount,
            hour,
            transactions_last_hour,
            is_new_device,
            is_international,
            failed_attempts,
            ml_probability,
            risk_score,
            decision
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        amount,
        hour,
        transactions_last_hour,
        is_new_device,
        is_international,
        failed_attempts,
        ml_probability,
        risk_score,
        decision
    ))

    connection.commit()
    connection.close()


def get_recent_transactions(limit=10):
    """Fetch recent analyzed transactions."""

    initialize_database()

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            amount,
            risk_score,
            decision
        FROM transaction_audit
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    connection.close()

    return rows
