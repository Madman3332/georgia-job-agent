import sqlite3

DB_NAME = "jobs.db"


# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table for sent jobs (duplicate prevention)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sent_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# SETTINGS TABLE
# -----------------------------

def init_settings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table for bot settings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # Default values (only inserted if they don’t exist)
    cursor.execute("""
        INSERT OR IGNORE INTO settings (key, value)
        VALUES ('min_salary', '4500')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO settings (key, value)
        VALUES ('keywords', 'manager,analyst,finance,procurement,HR')
    """)

    conn.commit()
    conn.close()


# -----------------------------
# SETTINGS HELPERS
# -----------------------------

def get_setting(key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM settings WHERE key=?", (key,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def update_setting(key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE settings
        SET value=?
        WHERE key=?
    """, (value, key))

    conn.commit()
    conn.close()


# -----------------------------
# JOB DUPLICATE CHECK
# -----------------------------

def job_already_sent(link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM sent_jobs WHERE link=?", (link,))
    result = cursor.fetchone()

    conn.close()

    return result is not None


def mark_job_as_sent(link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO sent_jobs (link)
        VALUES (?)
    """, (link,))

    conn.commit()
    conn.close()