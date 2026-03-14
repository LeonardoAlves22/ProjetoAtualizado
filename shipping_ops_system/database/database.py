import sqlite3
from pathlib import Path

DB_PATH = Path("shipping_ops.db")


def get_connection():

    conn = sqlite3.connect(
        "shipping_ops.db",
        timeout=30,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # VESSELS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vessels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        branch TEXT
    )
    """)

    # PROSPECTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prospects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vessel_id INTEGER,
        date TEXT,
        prospect_morning INTEGER,
        prospect_afternoon INTEGER,
        eta TEXT,
        etb TEXT,
        etd TEXT,
        email_id TEXT,
        FOREIGN KEY(vessel_id) REFERENCES vessels(id)
    )
    """)

    # ALERTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vessel_id INTEGER,
        branch TEXT,
        alert_type TEXT,
        created_at TEXT,
        resolved INTEGER DEFAULT 0,
        FOREIGN KEY(vessel_id) REFERENCES vessels(id)
    )
    """)

    conn.commit()
    conn.close()