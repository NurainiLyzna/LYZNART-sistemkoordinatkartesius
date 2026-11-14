"""Lapisan database sederhana untuk LYZNART.

- Lokal  : SQLite (file instance/lyznart.db) - tanpa konfigurasi.
- Online : PostgreSQL bila env DATABASE_URL diisi (postgres://... atau postgresql://...).

Semua query ditulis memakai placeholder "?" lalu otomatis diubah ke "%s" untuk PostgreSQL.
"""
import os
import sqlite3

from flask import g

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
IS_POSTGRES = DATABASE_URL.startswith(("postgres://", "postgresql://"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_PATH = os.environ.get("SQLITE_PATH", os.path.join(BASE_DIR, "instance", "lyznart.db"))

SCHEMA = [
    """CREATE TABLE IF NOT EXISTS users (
        id {pk},
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        kelas TEXT NOT NULL DEFAULT '',
        sekolah TEXT NOT NULL DEFAULT '',
        avatar TEXT NOT NULL DEFAULT 'robot',
        password_hash TEXT NOT NULL,
        xp INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS results (
        id {pk},
        user_id INTEGER NOT NULL,
        kind TEXT NOT NULL,
        score INTEGER NOT NULL,
        correct INTEGER NOT NULL DEFAULT 0,
        total INTEGER NOT NULL DEFAULT 0,
        xp_gained INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS badges (
        user_id INTEGER NOT NULL,
        code TEXT NOT NULL,
        earned_at TEXT NOT NULL,
        PRIMARY KEY (user_id, code)
    )""",
    """CREATE TABLE IF NOT EXISTS progress (
        user_id INTEGER NOT NULL,
        item TEXT NOT NULL,
        done_at TEXT NOT NULL,
        PRIMARY KEY (user_id, item)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_results_user ON results (user_id, kind)",
]


def _connect():
    if IS_POSTGRES:
        import psycopg  # diimpor hanya saat memakai PostgreSQL
        from psycopg.rows import dict_row

        return psycopg.connect(DATABASE_URL, row_factory=dict_row, autocommit=False)
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _sql(query):
    return query.replace("?", "%s") if IS_POSTGRES else query


def get_db():
    if "db" not in g:
        g.db = _connect()
    return g.db


def close_db(_exc=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def query(sql, params=(), one=False):
    cur = get_db().cursor()
    cur.execute(_sql(sql), params)
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    return (rows[0] if rows else None) if one else rows


def execute(sql, params=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(_sql(sql), params)
    conn.commit()
    cur.close()


def init_db():
    conn = _connect()
    pk = "SERIAL PRIMARY KEY" if IS_POSTGRES else "INTEGER PRIMARY KEY AUTOINCREMENT"
    cur = conn.cursor()
    for stmt in SCHEMA:
        cur.execute(stmt.format(pk=pk))
    conn.commit()
    cur.close()
    conn.close()


def backend_name():
    return "PostgreSQL" if IS_POSTGRES else "SQLite"
