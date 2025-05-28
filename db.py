import sqlite3

DB_PATH = "worktime.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            username TEXT PRIMARY KEY,
            firstname TEXT,
            lastname TEXT,
            chat_id TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            firstname TEXT,
            lastname TEXT,
            login_time TEXT,
            logout_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_chat_id(username, default_chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT chat_id FROM employees WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else default_chat_id

def mark_login(user, now):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO attendance (username, firstname, lastname, login_time) VALUES (?, ?, ?, ?)",
              (user['username'], user['firstname'], user['lastname'], now))
    conn.commit()
    conn.close()

def mark_logout(user, now):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE attendance SET logout_time = ? 
        WHERE username = ? AND logout_time IS NULL
        ORDER BY login_time DESC LIMIT 1
    ''', (now, user['username']))
    conn.commit()
    conn.close()
