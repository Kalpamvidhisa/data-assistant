import sqlite3

def get_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    # Default admin
    cur.execute("""
    INSERT OR IGNORE INTO users (email, password, role)
    VALUES ('admin@gmail.com', 'admin123', 'admin')
    """)

    conn.commit()
    conn.close()
