from database import get_connection

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE email=? AND password=?",
        (email, password)
    )
    result = cur.fetchone()
    conn.close()
    return result

def add_user(email, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?, 'user')",
        (email, password)
    )
    conn.commit()
    conn.close()

def delete_user(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT email, role FROM users")
    users = cur.fetchall()
    conn.close()
    return users
