import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="🤖🧠 Data Assistant AI",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------
# Session State
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------------
# Login Page
# -------------------------------
def login_page():
    st.markdown("## 🔐 Login / Public Access")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👩‍💻 Admin / Registered Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Logged in as {username}")
                st.rerun()
            else:
                st.error("Please enter username")

    with col2:
        st.subheader("🌟 Public Access")
        if st.button("Continue as Guest"):
            st.session_state.logged_in = True
            st.session_state.username = "Guest"
            st.rerun()

# -------------------------------
# Logout
# -------------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# -------------------------------
# Show Login
# -------------------------------
if not st.session_state.logged_in:
    login_page()

# -------------------------------
# Main App
# -------------------------------
else:
    # Sidebar
    st.sidebar.title("🌐 Navigation Panel")
    st.sidebar.write(f"👋 Welcome: **{st.session_state.username}**")

    menu = st.sidebar.radio(
        "Choose your section ✨",
        [
            "🏡 Home",
            "🗂️ Upload & Overview",
            "📊 Analytics Dashboard",
            "📋 Data Preview",
            "🛠️ Filter & Download",
            "🎨 Visualizations",
            "🧑‍💻 Code Editor"
        ]
    )

    if st.sidebar.button("🚪 Logout"):
        logout()

    st.sidebar.markdown("---")
    st.sidebar.info("💡 Mini Project: Data Assistant AI")

    # Main Title
    st.markdown(
        f"""
        <h1 style="text-align:center;color:#4B0082;">
        🤖✨ <span style="color:#FF4500;">Data Assistant</span> AI Web App 🧠
        </h1>
        <h3 style="text-align:center;color:#2E8B57;">
        Welcome <span style="color:#FF6347;">{st.session_state.username}</span>!
        Explore your data interactively 🚀
        </h3>
        """,
        unsafe_allow_html=True
    )

    # Upload CSV
    uploaded_file = st.file_uploader(
        "📂 Upload your CSV file",
        type=["csv"],
        help="Upload a CSV file"
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include="number").columns

        # -------------------------------
        # Upload & Overview
        # -------------------------------
        if menu == "🗂️ Upload & Overview":
            st.subheader("📊 Dataset Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])
            col3.metric("Missing Values", df.isnull().sum().sum())

        # -------------------------------
        # Analytics Dashboard
        # -------------------------------
        elif menu == "📊 Analytics Dashboard":
            st.subheader("📈 Analytics Dashboard")

            if len(numeric_cols) > 0:
                for col in numeric_cols:
                    st.metric(f"Average {col}", round(df[col].mean(), 2))

        # -------------------------------
        # Data Preview
        # -------------------------------
        elif menu == "📋 Data Preview":
            st.subheader("📂 Dataset Preview")
            st.dataframe(df, use_container_width=True)

        # -------------------------------
        # Filter & Download
        # -------------------------------
        elif menu == "🛠️ Filter & Download":
            st.subheader("🔍 Filter Dataset")

            filter_col = st.selectbox("Select column", df.columns)
            filter_val = st.selectbox(
                "Select value",
                df[filter_col].astype(str).unique()
            )

            filtered_df = df[df[filter_col].astype(str) == filter_val]
            st.dataframe(filtered_df, use_container_width=True)

            st.download_button(
                "⬇️ Download Full Dataset",
                df.to_csv(index=False),
                "full_dataset.csv"
            )

            st.download_button(
                "⬇️ Download Filtered Dataset",
                filtered_df.to_csv(index=False),
                "filtered_dataset.csv"
            )

        # -------------------------------
        # Visualizations
        # -------------------------------
        elif menu == "🎨 Visualizations":
            st.subheader("📊 Data Visualization")

            if len(numeric_cols) > 0:
                col = st.selectbox("Select numeric column", numeric_cols)
                chart = st.radio("Chart type", ["Line", "Bar"])

                if chart == "Line":
                    st.line_chart(df[col])
                else:
                    st.bar_chart(df[col])

        # -------------------------------
        # Python Code Editor
        # -------------------------------
        elif menu == "🧑‍💻 Code Editor":
            st.subheader("🧑‍💻 Python Code Editor")
            st.info("You can use: df, pandas, numpy, matplotlib")

            default_code = """
# Example: Histogram of first numeric column

import matplotlib.pyplot as plt

column = df.select_dtypes(include='number').columns[0]
plt.hist(df[column], bins=10)
plt.title(f"Histogram of {column}")
plt.xlabel(column)
plt.ylabel("Frequency")
plt.show()
"""

            user_code = st.text_area(
                "✍️ Write Python code below:",
                value=default_code,
                height=300
            )

            if st.button("▶️ Run Code"):
                try:
                    local_env = {
                        "df": df,
                        "pd": pd,
                        "np": np,
                        "plt": plt,
                        "st": st
                    }
                    exec(user_code, local_env)
                    st.success("✅ Code executed successfully")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    else:
        st.warning("⬆️ Please upload a CSV file to continue")
