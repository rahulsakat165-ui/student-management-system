import sqlite3

def connect_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Login table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # Student table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT,
        course TEXT,
        marks INTEGER,
        performance TEXT
    )
    """)

    # Default login
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES('admin','admin123')"
    )

    conn.commit()
    conn.close()
