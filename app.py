import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Assistant", layout="wide")

st.title("📊 Data Assistant Web App")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.markdown("## 🔍 Dataset Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.markdown("## 📄 Data Preview")
    st.dataframe(df.head(10))

    st.markdown("## 🧬 Data Types")
    st.dataframe(df.dtypes.astype(str))

    st.markdown("## 🚫 Missing Values per Column")
    missing_df = df.isnull().sum()
    st.dataframe(missing_df[missing_df > 0])

    st.markdown("## 📊 Summary Statistics")
    st.dataframe(df.describe())

    st.markdown("## 📈 Visualize a Column")
    column = st.selectbox("Select a column to visualize", df.columns)

    if df[column].dtype != "object":
        fig, ax = plt.subplots()
        df[column].hist(ax=ax)
        st.pyplot(fig)
    else:
        value_counts = df[column].value_counts()
        st.bar_chart(value_counts)
