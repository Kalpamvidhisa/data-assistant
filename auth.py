import sqlite3

def login_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT role FROM users WHERE email=? AND password=?",
        (email, password)
    )
    result = c.fetchone()
    conn.close()

    return result[0] if result else None


def signup_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT email FROM users WHERE email=?", (email,))
    if c.fetchone():
        conn.close()
        return False

    c.execute(
        "INSERT INTO users VALUES (?, ?, 'user')",
        (email, password)
    )
    conn.commit()
    conn.close()
    return True


def get_all_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT email, role FROM users")
    users = c.fetchall()
    conn.close()
    return users


def delete_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()
