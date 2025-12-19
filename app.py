import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Assistant", layout="wide")

st.title("📊 Data Assistant Web App")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Dataset Preview")
    st.dataframe(df.head())

    st.subheader("📈 Dataset Information")
    st.write("Shape:", df.shape)
    st.write("Columns:", df.columns.tolist())

    st.subheader("📊 Summary Statistics")
    st.write(df.describe())

    st.subheader("📉 Column Visualization")
    column = st.selectbox("Select a column", df.columns)

    if df[column].dtype != "object":
        fig, ax = plt.subplots()
        df[column].hist(ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Please select a numeric column")

