import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Data Assistant Web App", layout="wide")

# Title
st.title("📊 Data Assistant Web App")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ================= Dataset Overview =================
    st.markdown("## 🔍 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # ================= Data Preview =================
    st.markdown("## 📄 Data Preview")
    st.dataframe(df.head(10))

    # ================= Filter Data =================
    st.markdown("## 🔎 Filter Data")

    filter_column = st.selectbox("Select column to filter", df.columns)
    unique_values = df[filter_column].dropna().unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[filter_column] == selected_value]
    st.dataframe(filtered_df)

    # ================= Search Data =================
    st.markdown("## 🔍 Search in Dataset")

    search_text = st.text_input("Enter keyword to search")

    if search_text:
        search_df = df[df.astype(str).apply(
            lambda row: row.str.contains(search_text, case=False).any(),
            axis=1
        )]
        st.dataframe(search_df)

    # ================= Visualization =================
    st.markdown("## 📈 Visualization")

    viz_column = st.selectbox("Select column for visualization", df.columns)

    if df[viz_column].dtype != "object":
        fig, ax = plt.subplots()
        df[viz_column].hist(ax=ax)
        st.pyplot(fig)
    else:
        st.bar_chart(df[viz_column].value_counts())

    # ================= Download Section =================
    st.markdown("## ⬇️ Download Data")

    # Download full dataset
    csv_full = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Full Dataset",
        data=csv_full,
        file_name="full_dataset.csv",
        mime="text/csv"
    )

    # Download filtered dataset
    csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Dataset",
        data=csv_filtered,
        file_name="filtered_dataset.csv",
        mime="text/csv"
    )
