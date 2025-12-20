import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Data Assistant AI Web App",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Simple User Database (Demo)
# -------------------------------
USERS = {
    "admin": "admin123",
    "vidhisa": "data123"
}

# -------------------------------
# Session State
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

# -------------------------------
# Login Page
# -------------------------------
def login():
    st.title("🔐 Login to Data Assistant")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Login successful! Welcome {username}")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# -------------------------------
# Logout
# -------------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# -------------------------------
# If NOT logged in → show login
# -------------------------------
if not st.session_state.logged_in:
    login()

# -------------------------------
# MAIN APP (After Login)
# -------------------------------
else:
    # Sidebar
    st.sidebar.title("📌 Navigation")
    st.sidebar.write(f"👤 User: **{st.session_state.username}**")
    
    menu = st.sidebar.radio(
        "Go to",
        [
            "Welcome",
            "Upload & Overview",
            "Dashboard",
            "Data Preview",
            "Filter & Download",
            "Visualizations"
        ]
    )
    
    if st.sidebar.button("🚪 Logout"):
        logout()
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 Data Assistant AI Web App")
    
    # -------------------------------
    # Welcome Page
    # -------------------------------
    if menu == "Welcome":
        st.success(f"👋 Welcome {st.session_state.username}!")
        st.write("This is your Data Assistant Web App. Use the sidebar to navigate.")
    
    # -------------------------------
    # Upload CSV
    # -------------------------------
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        numeric_cols = df.select_dtypes(include="number").columns
        
        # -------------------------------
        # Upload & Overview
        # -------------------------------
        if menu == "Upload & Overview":
            st.markdown("## 📊 Dataset Overview")
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows", df.shape[0])
            col2.metric("Columns", df.shape[1])
            col3.metric("Missing Values", df.isnull().sum().sum())
        
        # -------------------------------
        # Dashboard
        # -------------------------------
        elif menu == "Dashboard":
            st.markdown("## 📌 Performance Dashboard")
            if len(numeric_cols) >= 3:
                c1, c2, c3 = st.columns(3)
                c1.metric("📘 Avg Score 1", round(df[numeric_cols[0]].mean(), 2))
                c2.metric("📗 Avg Score 2", round(df[numeric_cols[1]].mean(), 2))
                c3.metric("📕 Avg Score 3", round(df[numeric_cols[2]].mean(), 2))
            if "gender" in df.columns:
                st.markdown("### 👩‍🎓👨‍🎓 Gender-wise Analysis")
                st.bar_chart(df.groupby("gender")[numeric_cols].mean())
        
        # -------------------------------
        # Data Preview
        # -------------------------------
        elif menu == "Data Preview":
            st.markdown("## 📄 Dataset Preview")
            st.dataframe(df, use_container_width=True)
        
        # -------------------------------
        # Filter & Download
        # -------------------------------
        elif menu == "Filter & Download":
            st.markdown("## 🔎 Filter Dataset")
            filter_col = st.selectbox("Select column", df.columns)
            filter_val = st.selectbox("Select value", df[filter_col].astype(str).unique())
            
            filtered_df = df[df[filter_col].astype(str) == filter_val]
            st.dataframe(filtered_df, use_container_width=True)
            
            st.markdown("## ⬇️ Download")
            st.download_button(
                "Download Full Dataset",
                df.to_csv(index=False).encode("utf-8"),
                "full_dataset.csv",
                "text/csv"
            )
            st.download_button(
                "Download Filtered Dataset",
                filtered_df.to_csv(index=False).encode("utf-8"),
                "filtered_dataset.csv",
                "text/csv"
            )
        
        # -------------------------------
        # Visualizations
        # -------------------------------
        elif menu == "Visualizations":
            st.markdown("## 📈 Data Visualization")
            selected_col = st.selectbox("Select numeric column", numeric_cols)
            chart_type = st.radio("Select chart type", ["Line Chart", "Bar Chart"])
            
            if chart_type == "Line Chart":
                st.line_chart(df[selected_col])
            else:
                st.bar_chart(df[selected_col])
    
    else:
        if menu != "Welcome":
            st.warning("⬆️ Please upload a CSV file to continue")
