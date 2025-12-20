import streamlit as st
from database import create_tables
from auth import login_user, add_user, delete_user, get_all_users

st.set_page_config(page_title="Data Assistant", layout="wide")

create_tables()

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.markdown("## 🔐 Data Assistant Login")

    option = st.radio("", ["Sign In", "Forgot Password", "Register"])

    if option == "Sign In":
        email = st.text_input("📧 Email")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Sign In"):
            result = login_user(email, password)
            if result:
                st.session_state.logged_in = True
                st.session_state.role = result[0]
                st.session_state.email = email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

    elif option == "Forgot Password":
        st.info("Password recovery feature coming soon 🚧")

    elif option == "Register":
        st.warning("Account creation restricted. Contact Admin.")

# ---------------- WELCOME PAGE ----------------
def welcome_page():
    st.success(f"🎉 Welcome {st.session_state.email}")
    st.markdown("### 👋 You are logged into **Data Assistant AI Web App**")

    st.info("""
    🔹 Upload datasets  
    🔹 Analyze data  
    🔹 Download filtered results  
    🔹 Secure role-based access  
    """)

# ---------------- ADMIN PANEL ----------------
def admin_panel():
    st.subheader("🛠 Admin Panel")

    with st.form("add_user"):
        email = st.text_input("New User Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("➕ Add User")
        if submit:
            add_user(email, password)
            st.success("User added successfully")

    st.markdown("### 👥 Existing Users")
    users = get_all_users()
    for u in users:
        col1, col2, col3 = st.columns([3,2,2])
        col1.write(u[0])
        col2.write(u[1])
        if col3.button("❌ Remove", key=u[0]):
            delete_user(u[0])
            st.warning("User removed")
            st.rerun()

# ---------------- SIDEBAR ----------------
def sidebar():
    with st.sidebar:
        st.title("📊 Navigation")
        choice = st.radio(
            "Go to",
            ["Welcome", "Admin Panel", "Logout"]
            if st.session_state.role == "admin"
            else ["Welcome", "Logout"]
        )

    return choice

# ---------------- MAIN FLOW ----------------
if not st.session_state.logged_in:
    login_page()
else:
    page = sidebar()

    if page == "Welcome":
        welcome_page()

    elif page == "Admin Panel" and st.session_state.role == "admin":
        admin_panel()

    elif page == "Logout":
        st.session_state.clear()
        st.success("Logged out")
        st.rerun()
