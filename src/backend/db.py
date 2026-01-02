import sqlite3
from pathlib import Path

def get_conn(db_path: Path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS rom_bytes (
        offset INTEGER PRIMARY KEY,
        value INTEGER NOT NULL,
        modified INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS byte_tags (
        offset INTEGER,
        tag TEXT,
        PRIMARY KEY (offset, tag)
    );
    """)
