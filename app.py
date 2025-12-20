import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Data Assistant AI Web App",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Database Setup
# -------------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")
conn.commit()

# Create default admin
cur.execute("SELECT * FROM users WHERE email='admin@gmail.com'")
if not cur.fetchone():
    cur.execute(
        "INSERT INTO users VALUES (?, ?, ?)",
        ("admin@gmail.com", "admin123", "admin")
    )
    conn.commit()

# -------------------------------
# Session State
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "role" not in st.session_state:
    st.session_state.role = None

# -------------------------------
# LOGIN UI
# -------------------------------
def login_ui():
    st.markdown("""
    <div style="max-width:400px;margin:auto;padding:30px;
    border-radius:12px;box-shadow:0px 0px 15px #ddd">
    <h2 style="text-align:center">🔐 Data Assistant Login</h2>
    </div>
    """, unsafe_allow_html=True)

    option = st.radio("", ["Sign In", "Forgot Password", "Don't have an account?"])

    if option == "Sign In":
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Sign In"):
            cur.execute(
                "SELECT role FROM users WHERE email=? AND password=?",
                (email, password)
            )
            user = cur.fetchone()

            if user:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.session_state.role = user[0]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

    elif option == "Forgot Password":
        st.info(
            "🔒 Password reset is disabled.\n\n"
            "Please contact the Admin:\n\n"
            "📧 admin@gmail.com"
        )

    else:
        st.warning(
            "🚫 Public registration disabled.\n\n"
            "Please contact Admin for access."
        )

# -------------------------------
# LOGOUT
# -------------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.role = None
    st.rerun()

# -------------------------------
# LOGIN CHECK
# -------------------------------
if not st.session_state.logged_in:
    login_ui()

# ===============================
# SUCCESS WELCOME PAGE + APP
# ===============================
else:
    st.sidebar.title("📌 Navigation")
    st.sidebar.write(f"👤 {st.session_state.current_user}")

    menu = st.sidebar.radio(
        "Go to",
        ["Welcome", "Upload & Overview", "Data Preview", "Filter & Download"]
        + (["Admin Panel"] if st.session_state.role == "admin" else [])
    )

    if st.sidebar.button("🚪 Logout"):
        logout()

    # -------------------------------
    # WELCOME PAGE
    # -------------------------------
    if menu == "Welcome":
        st.success(f"🎉 Welcome {st.session_state.current_user}!")
        st.markdown("""
        ### 🤖 Data Assistant AI Web App
        - Upload CSV
        - Analyze data
        - Filter & download
        - Admin-controlled access
        """)

    uploaded_file = st.file_uploader("Upload CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if menu == "Upload & Overview":
            c1, c2, c3 = st.columns(3)
            c1.metric("Rows", df.shape[0])
            c2.metric("Columns", df.shape[1])
            c3.metric("Missing Values", df.isnull().sum().sum())

        elif menu == "Data Preview":
            st.dataframe(df, use_container_width=True)

        elif menu == "Filter & Download":
            col = st.selectbox("Select column", df.columns)
            val = st.selectbox("Select value", df[col].astype(str).unique())
            filtered = df[df[col].astype(str) == val]

            st.dataframe(filtered, use_container_width=True)

            st.download_button(
                "⬇️ Download Filtered Data",
                filtered.to_csv(index=False).encode(),
                "filtered_data.csv"
            )

    # -------------------------------
    # ADMIN PANEL
    # -------------------------------
    if menu == "Admin Panel":
        st.subheader("🛠 Admin Panel")

        st.markdown("### ➕ Add User")
        email = st.text_input("User Email")
        password = st.text_input("Password", type="password")

        if st.button("Add User"):
            try:
                cur.execute(
                    "INSERT INTO users VALUES (?, ?, ?)",
                    (email, password, "user")
                )
                conn.commit()
                st.success("User added")
            except:
                st.error("User already exists")

        st.markdown("### ❌ Remove User")
        cur.execute("SELECT email FROM users WHERE role='user'")
        users = [u[0] for u in cur.fetchall()]

        if users:
            u = st.selectbox("Select user", users)
            if st.button("Remove User"):
                cur.execute("DELETE FROM users WHERE email=?", (u,))
                conn.commit()
                st.success("User removed")
        st.rerun()
