import sqlite3
from pathlib import Path

DB_PATH = Path("subs.db")

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.touch(exist_ok=True)
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER UNIQUE NOT NULL,
            - TEXT,
            re_plast TEXT,
            re_battery TEXT,
            on_foot TEXT,
            sort TEXT,
            re_use TEXT,
            eco_action TEXT,
            ECO_friend TEXT
            score TEXT
        );
        """)
    
        conn.commit()
def add_sub(chat_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (tg_id) VALUES (?)", (int(chat_id),))
    conn.commit()
    conn.close()
def add_col(column, tg_id, value):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"UPDATE  users SET {column}=? WHERE tg_id=?", (value,tg_id))
    conn.commit()
    conn.close()
def del_sub(chat_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
    conn.commit()
    conn.close()
def all_sub():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT tg_id FROM users")
    rows = [row[0] for row in cur.fetchall()]
    conn.close()
    return rows
def all_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = len([row[0] for row in cur.fetchall()])
    conn.close()
    return rows
def count_subs():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM users")
    rows = len([row[0] for row in cur.fetchall()])
    conn.close()
    return rows
# init_db()