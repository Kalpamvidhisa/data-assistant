import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import os
import io
from datetime import datetime

# ---------- OPTIONAL REAL LLM ----------
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    LLM_AVAILABLE = True
except:
    LLM_AVAILABLE = False

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Data Assistant AI",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------
# Database (SQLite)
# -------------------------------
conn = sqlite3.connect("data_assistant.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    question TEXT,
    answer TEXT,
    time TEXT
)
""")
conn.commit()

# -------------------------------
# Session State
# -------------------------------
for key in ["logged_in", "username"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else ""

# -------------------------------
# Login
# -------------------------------
def login():
    st.title("🔐 Login")
    u = st.text_input("Username")
    if st.button("Login"):
        if u:
            st.session_state.logged_in = True
            st.session_state.username = u
            st.rerun()

# -------------------------------
# LLM Chat Function
# -------------------------------
def llm_chat(question, df):
    if not LLM_AVAILABLE:
        return "⚠️ LLM not configured. Add API key."

    schema = f"Columns: {list(df.columns)}"
    prompt = f"""
You are a data assistant.
Dataset info: {schema}
Question: {question}
Give a clear answer.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# -------------------------------
# App Start
# -------------------------------
if not st.session_state.logged_in:
    login()

else:
    st.sidebar.title("⚙️ Menu")
    st.sidebar.write(f"👤 {st.session_state.username}")

    menu = st.sidebar.radio(
        "Navigate",
        [
            "🏡 Home",
            "📂 Upload Data",
            "🧑‍💻 Code Editor",
            "🤖 AI Chatbot (LLM)",
            "📜 Chat History (DB)"
        ]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🤖 Data Assistant AI (LLM + SQLite)")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # -------------------------------
        if menu == "📂 Upload Data":
            st.metric("Rows", df.shape[0])
            st.metric("Columns", df.shape[1])
            st.dataframe(df, use_container_width=True)

        # -------------------------------
        elif menu == "🧑‍💻 Code Editor":
            code = st.text_area("Python Code (use df)", height=250)
            if st.button("Run Code"):
                try:
                    fig = plt.figure()
                    exec(code, {"df": df, "pd": pd, "np": np, "plt": plt, "st": st})
                    st.pyplot(fig)
                    plt.clf()
                except Exception as e:
                    st.error(e)

        # -------------------------------
        elif menu == "🤖 AI Chatbot (LLM)":
            q = st.text_input("Ask about your dataset")
            if st.button("Ask"):
                ans = llm_chat(q, df)

                cursor.execute(
                    "INSERT INTO chat_logs VALUES (NULL, ?, ?, ?, ?)",
                    (st.session_state.username, q, ans, datetime.now().strftime("%d-%m-%Y %H:%M"))
                )
                conn.commit()

                st.success(ans)

        # -------------------------------
        elif menu == "📜 Chat History (DB)":
            rows = cursor.execute(
                "SELECT question, answer, time FROM chat_logs WHERE username=?",
                (st.session_state.username,)
            ).fetchall()

            for q, a, t in rows:
                st.markdown(f"**🕒 {t}**")
                st.write(f"**Q:** {q}")
                st.write(f"**A:** {a}")
                st.markdown("---")

    else:
        st.info("Upload a CSV file to begin")
