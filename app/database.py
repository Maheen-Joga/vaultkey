import sqlite3
import click
from flask import g, current_app


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # Enforce foreign keys and WAL mode for safety
        g.db.execute("PRAGMA foreign_keys = ON")
        g.db.execute("PRAGMA journal_mode = WAL")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    app.teardown_appcontext(close_db)

    with app.app_context():
        db = get_db()
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                username  TEXT    NOT NULL UNIQUE,
                email     TEXT    NOT NULL UNIQUE,
                password  TEXT    NOT NULL,
                salt      TEXT    NOT NULL,
                created   TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS vault_entries (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                site_name   TEXT    NOT NULL,
                site_url    TEXT,
                username    TEXT    NOT NULL,
                password    BLOB    NOT NULL,
                iv          BLOB    NOT NULL,
                notes       BLOB,
                notes_iv    BLOB,
                created     TEXT    DEFAULT (datetime('now')),
                updated     TEXT    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS audit_log (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER REFERENCES users(id) ON DELETE SET NULL,
                action    TEXT    NOT NULL,
                detail    TEXT,
                ip        TEXT,
                timestamp TEXT    DEFAULT (datetime('now'))
            );
        """)
        db.commit()
