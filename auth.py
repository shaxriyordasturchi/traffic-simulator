import sqlite3
from config import DB_PATH

def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM employees WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def register_user(username, firstname, lastname, chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO employees (username, firstname, lastname, chat_id) VALUES (?, ?, ?, ?)",
              (username, firstname, lastname, chat_id))
    conn.commit()
    conn.close()
