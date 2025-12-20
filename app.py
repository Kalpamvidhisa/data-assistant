import streamlit as st
import pandas as pd

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
# Login / Public Access
# -------------------------------
def login_page():
    st.markdown("## 🔐 Login / Public Access")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👩‍💻 Admin / Registered Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter password (optional)")

        if st.button("Login"):
            if username:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"🎉 Logged in as **{username}**!")
                st.rerun()
            else:
                st.error("❌ Please enter a username")

    with col2:
        st.subheader("🌟 Public Access")
        st.write("Continue as a guest to use the app without login")
        if st.button("Continue as Guest"):
            st.session_state.logged_in = True
            st.session_state.username = "Guest"
            st.success("🎉 Continuing as **Guest**")
            st.rerun()

# -------------------------------
# Logout
# -------------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# -------------------------------
# Show login page if not logged in
# -------------------------------
if not st.session_state.logged_in:
    login_page()

# -------------------------------
# Main App After Login
# -------------------------------
else:
    # Sidebar with new creative emojis
    st.sidebar.title("🌐 Navigation Panel")
    st.sidebar.write(f"🧑‍🎓 Welcome: **{st.session_state.username}**")

    menu = st.sidebar.radio(
        "Choose your section ✨",
        [
            "🏡 Home",
            "🗂️ Upload & Overview",
            "📊 Analytics Dashboard",
            "📋 Data Preview",
            "🛠️ Filter & Download",
            "🎨 Visualizations"
        ]
    )

    if st.sidebar.button("🚪 Logout"):
        logout()

    st.sidebar.markdown("---")
    st.sidebar.info("💡 Mini Project: Data Assistant AI")

    # Creative main title
    st.markdown("""
        <h1 style='text-align: center; color: #4B0082;'>
            🤖✨ <span style='color:#FF4500;'>Data Assistant</span> AI Web App 🧠🎨
        </h1>
        <h3 style='text-align: center; color: #2E8B57;'>Welcome <span style='color:#FF6347;'>{username}</span>! Explore your data in a fun and interactive way 🚀</h3>
        """.format(username=st.session_state.username), unsafe_allow_html=True)

    # Upload CSV
    uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"], help="Drag & drop your CSV file here")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include="number").columns

        # Upload & Overview
        if menu == "🗂️ Upload & Overview":
            st.markdown("## 📊 Dataset Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("📝 Rows", df.shape[0])
            col2.metric("📐 Columns", df.shape[1])
            col3.metric("⚠️ Missing Values", df.isnull().sum().sum())

        # Dashboard
        elif menu == "📊 Analytics Dashboard":
            st.markdown("## 📈 Performance Dashboard")
            if len(numeric_cols) > 0:
                for col in numeric_cols:
                    st.metric(f"📊 Avg {col}", round(df[col].mean(), 2))

            if "gender" in df.columns:
                st.markdown("### 👩‍🎓👨‍🎓 Gender Analysis")
                st.bar_chart(df.groupby("gender")[numeric_cols].mean())

        # Data Preview
        elif menu == "📋 Data Preview":
            st.markdown("## 📂 Dataset Preview")
            st.dataframe(df, use_container_width=True)

        # Filter & Download
        elif menu == "🛠️ Filter & Download":
            st.markdown("## 🔍 Filter Dataset")
            filter_col = st.selectbox("Select column", df.columns)
            filter_val = st.selectbox("Select value", df[filter_col].astype(str).unique())
            filtered_df = df[df[filter_col].astype(str) == filter_val]
            st.dataframe(filtered_df, use_container_width=True)

            st.download_button("⬇️ Download Full Dataset", df.to_csv(index=False).encode(), "full_dataset.csv")
            st.download_button("⬇️ Download Filtered Dataset", filtered_df.to_csv(index=False).encode(), "filtered_dataset.csv")

        # Visualizations
        elif menu == "🎨 Visualizations":
            st.markdown("## 📈 Data Visualization")
            if len(numeric_cols) > 0:
                selected_col = st.selectbox("Select numeric column", numeric_cols)
                chart_type = st.radio("Select chart type", ["📈 Line Chart", "📊 Bar Chart"])
                if chart_type == "📈 Line Chart":
                    st.line_chart(df[selected_col])
                else:
                    st.bar_chart(df[selected_col])

    else:
        st.warning("⬆️ Please upload a CSV file to continue")
