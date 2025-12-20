import streamlit as st
from database import init_db
from auth import login_user, signup_user, get_all_users, delete_user

st.set_page_config(page_title="Data Assistant", layout="wide")
init_db()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN & SIGNUP ---------------- #
if not st.session_state.logged_in:

    st.title("🔐 Data Assistant Login")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role = login_user(email, password)
            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.email = email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

    with tab2:
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if signup_user(new_email, new_password):
                st.success("Account created! Please login.")
            else:
                st.warning("Email already exists")

    st.markdown("🔒 **Forgot Password?** Contact Admin")

# ---------------- AFTER LOGIN ---------------- #
else:
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Welcome", "Dataset Overview", "Admin Panel", "Logout"]
        if st.session_state.role == "admin"
        else ["Welcome", "Dataset Overview", "Logout"]
    )

    if page == "Welcome":
        st.success(f"Welcome {st.session_state.email} 👋")
        st.write("This is your Data Assistant Web App")

    elif page == "Dataset Overview":
        st.header("📁 Dataset Overview")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

        if uploaded_file:
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)

            st.download_button(
                "Download Dataset",
                df.to_csv(index=False),
                "filtered_data.csv",
                "text/csv"
            )

    elif page == "Admin Panel" and st.session_state.role == "admin":
        st.header("🛠 Admin Panel")

        users = get_all_users()
        st.table(users)

        delete_email = st.text_input("User email to delete")
        if st.button("Delete User"):
            delete_user(delete_email)
            st.success("User deleted")
            st.rerun()

    elif page == "Logout":
        st.session_state.clear()
        st.rerun()
