import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)

    # Create default admin if not exists
    c.execute("SELECT * FROM users WHERE email='admin@gmail.com'")
    if not c.fetchone():
        c.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            ("admin@gmail.com", "admin123", "admin")
        )

    conn.commit()
    conn.close()
