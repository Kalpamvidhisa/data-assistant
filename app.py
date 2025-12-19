import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Data Assistant AI", layout="wide")

st.title("🤖 Data Assistant AI Web App")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ================= Dataset Overview =================
    st.markdown("## 📌 Dataset Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", df.isnull().sum().sum())

    st.markdown("## 📄 Data Preview")
    st.dataframe(df.head())

    # ================= Filter Data =================
    st.markdown("## 🔎 Filter Data")

    filter_col = st.selectbox("Select column to filter", df.columns)
    filter_val = st.selectbox(
        "Select value",
        df[filter_col].dropna().unique()
    )

    filtered_df = df[df[filter_col] == filter_val]
    st.dataframe(filtered_df)

    # ================= Ask Your Data =================
    st.markdown("## 🧠 Ask Your Data")

    question = st.selectbox(
        "Choose a question",
        [
            "Show column names",
            "Show data types",
            "Show missing values",
            "Show top values of a column",
            "Show correlation"
        ]
    )

    if question == "Show column names":
        st.write(df.columns.tolist())

    elif question == "Show data types":
        st.dataframe(df.dtypes.astype(str))

    elif question == "Show missing values":
        st.dataframe(df.isnull().sum())

    elif question == "Show top values of a column":
        col = st.selectbox("Select column", df.columns)
        st.dataframe(df[col].value_counts().head(10))

    elif question == "Show correlation":
        num_df = df.select_dtypes(include="number")
        if num_df.shape[1] > 1:
            st.dataframe(num_df.corr())
        else:
            st.warning("Not enough numeric columns")

    # ================= Visualization =================
    st.markdown("## 📊 Visualization")

    chart_col = st.selectbox("Select column for chart", df.columns)

    if df[chart_col].dtype != "object":
        fig, ax = plt.subplots()
        df[chart_col].hist(ax=ax)
        st.pyplot(fig)
    else:
        st.bar_chart(df[chart_col].value_counts())

    # ================= Download Section =================
    st.markdown("## ⬇️ Download Data")

    # Full dataset download
    st.download_button(
        "Download Full Dataset",
        df.to_csv(index=False),
        file_name="full_dataset.csv",
        mime="text/csv"
    )

    # Filtered dataset download
    st.download_button(
        "Download Filtered Dataset",
        filtered_df.to_csv(index=False),
        file_name="filtered_dataset.csv",
        mime="text/csv"
    )
