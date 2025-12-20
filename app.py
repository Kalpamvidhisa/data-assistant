import streamlit as st
import pandas as pd

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Data Assistant AI Web App",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("📌 Navigation")
menu = st.sidebar.radio(
    "Go to",
    [
        "Upload & Overview",
        "Dashboard",
        "Data Preview",
        "Filter & Download",
        "Visualizations"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 Data Assistant Mini Project")

# -------------------------------
# Main Title
# -------------------------------
st.title("🤖 Data Assistant AI Web App")

# -------------------------------
# Upload CSV
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    numeric_cols = df.select_dtypes(include="number").columns

    # ===============================
    # PAGE 1: Upload & Overview
    # ===============================
    if menu == "Upload & Overview":
        st.markdown("## 📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

    # ===============================
    # PAGE 2: Dashboard (Boards)
    # ===============================
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

    # ===============================
    # PAGE 3: Data Preview
    # ===============================
    elif menu == "Data Preview":
        st.markdown("## 📄 Dataset Preview")
        st.dataframe(df, use_container_width=True)

    # ===============================
    # PAGE 4: Filter & Download
    # ===============================
    elif menu == "Filter & Download":
        st.markdown("## 🔎 Filter Dataset")

        filter_col = st.selectbox("Select column", df.columns)
        filter_val = st.selectbox(
            "Select value",
            df[filter_col].astype(str).unique()
        )

        filtered_df = df[df[filter_col].astype(str) == filter_val]

        st.write("### Filtered Data")
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

    # ===============================
    # PAGE 5: Visualizations
    # ===============================
    elif menu == "Visualizations":
        st.markdown("## 📈 Data Visualization")

        selected_col = st.selectbox("Select numeric column", numeric_cols)
        chart_type = st.radio("Select chart type", ["Line Chart", "Bar Chart"])

        if chart_type == "Line Chart":
            st.line_chart(df[selected_col])
        else:
            st.bar_chart(df[selected_col])

else:
    st.warning("⬆️ Please upload a CSV file to start using the app")
