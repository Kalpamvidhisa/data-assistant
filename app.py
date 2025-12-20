import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Data Assistant AI Web App",
    page_icon="🤖",
    layout="wide"
)

# ===============================
# DATABASE FUNCTIONS
# ===============================
def get_conn():
    return sqlite3.connect("users.db", check_same_thread=False)

def create_users_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)
    cur.execute("""
        INSERT OR IGNORE INTO users VALUES
        ('admin@gmail.com', 'admin123', 'admin')
    """)
    conn.commit()
    conn.close()

create_users_table()

# ===============================
# AUTH FUNCTIONS
# ===============================
def login_user(email, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cur.fetchone()
    conn.close()
    return user

def add_user(email, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?, 'user')",
        (email, password)
    )
    conn.commit()
    conn.close()

def delete_user(email):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE email=?", (email,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT email, role FROM users")
    data = cur.fetchall()
    conn.close()
    return data

# ===============================
# SESSION STATE
# ===============================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "email" not in st.session_state:
    st.session_state.email = None

if "role" not in st.session_state:
    st.session_state.role = None

# ===============================
# LOGIN PAGE
# ===============================
def login_page():
    st.markdown("""
    <div style="max-width:420px;margin:auto;padding:30px;
    border-radius:14px;box-shadow:0px 0px 18px #ddd">
    <h2 style="text-align:center">🔐 Data Assistant Login</h2>
    </div>
    """, unsafe_allow_html=True)

    option = st.radio("", ["Sign In", "Forgot Password", "Don't have an account?"])

    if option == "Sign In":
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Sign In"):
            user = login_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.email = email
                st.session_state.role = user[0]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid email or password")

    elif option == "Forgot Password":
        st.info("""
        🔒 Password recovery is disabled.

        📧 Contact Admin:
        admin@gmail.com
        """)

    else:
        st.warning("""
        🚫 Public registration disabled.

        📧 Contact Admin for access:
        admin@gmail.com
        """)

# ===============================
# LOGOUT
# ===============================
def logout():
    st.session_state.clear()
    st.rerun()

# ===============================
# MAIN APP
# ===============================
if not st.session_state.logged_in:
    login_page()

else:
    # -------- SIDEBAR --------
    st.sidebar.title("📊 Navigation")
    st.sidebar.write(f"👤 {st.session_state.email}")

    menu = [
        "Welcome",
        "Upload & Overview",
        "Dashboard",
        "Data Preview",
        "Filter & Download",
        "Advanced Charts",
        "Ask Your Data (AI)"
    ]

    if st.session_state.role == "admin":
        menu.append("Admin Panel")

    choice = st.sidebar.radio("Go to", menu)

    if st.sidebar.button("🚪 Logout"):
        logout()

    # -------- WELCOME PAGE --------
    if choice == "Welcome":
        st.success(f"🎉 Welcome {st.session_state.email}")
        st.markdown("""
        ### 🤖 Data Assistant AI Web App
        - Upload CSV files
        - Analyze data visually
        - Filter & download datasets
        - Role-based secure access
        """)

    # -------- DATA UPLOAD --------
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        num_cols = df.select_dtypes(include="number").columns
        cat_cols = df.select_dtypes(exclude="number").columns

        if choice == "Upload & Overview":
            c1, c2, c3 = st.columns(3)
            c1.metric("Rows", df.shape[0])
            c2.metric("Columns", df.shape[1])
            c3.metric("Missing Values", df.isnull().sum().sum())

        elif choice == "Dashboard" and len(num_cols) > 0:
            st.metric("Average Value", round(df[num_cols[0]].mean(), 2))

        elif choice == "Data Preview":
            st.dataframe(df, use_container_width=True)

        elif choice == "Filter & Download":
            col = st.selectbox("Select column", df.columns)
            val = st.selectbox("Select value", df[col].astype(str).unique())
            filtered_df = df[df[col].astype(str) == val]

            st.dataframe(filtered_df, use_container_width=True)

            st.download_button(
                "⬇️ Download Full Dataset",
                df.to_csv(index=False).encode(),
                "full_dataset.csv"
            )

            st.download_button(
                "⬇️ Download Filtered Dataset",
                filtered_df.to_csv(index=False).encode(),
                "filtered_dataset.csv"
            )

        elif choice == "Advanced Charts":
            chart = st.selectbox("Chart Type", ["Pie", "Histogram", "Box"])

            if chart == "Pie" and len(cat_cols) > 0:
                col = st.selectbox("Category Column", cat_cols)
                fig, ax = plt.subplots()
                df[col].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
                st.pyplot(fig)

            elif chart == "Histogram":
                col = st.selectbox("Numeric Column", num_cols)
                fig, ax = plt.subplots()
                ax.hist(df[col], bins=20)
                st.pyplot(fig)

            elif chart == "Box":
                col = st.selectbox("Numeric Column", num_cols)
                fig, ax = plt.subplots()
                ax.boxplot(df[col])
                st.pyplot(fig)

        elif choice == "Ask Your Data (AI)":
            q = st.text_input("Ask a question")

            if q:
                q = q.lower()
                if "rows" in q:
                    st.success(df.shape[0])
                elif "columns" in q:
                    st.success(df.shape[1])
                elif "average" in q:
                    for col in num_cols:
                        if col.lower() in q:
                            st.success(df[col].mean())
                else:
                    st.warning("Question not understood")

        # -------- ADMIN PANEL --------
        elif choice == "Admin Panel":
            st.subheader("🛠 Admin Panel")

            with st.form("add_user"):
                email = st.text_input("New User Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("➕ Add User"):
                    add_user(email, password)
                    st.success("User added")

            st.markdown("### 👥 Users")
            for u in get_all_users():
                if u[0] != "admin@gmail.com":
                    col1, col2, col3 = st.columns([3,2,2])
                    col1.write(u[0])
                    col2.write(u[1])
                    if col3.button("❌ Remove", key=u[0]):
                        delete_user(u[0])
                        st.rerun()

    else:
        if choice != "Welcome":
            st.info("⬆️ Upload a CSV file to begin")
