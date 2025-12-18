import streamlit as st
import pandas as pd
from PIL import Image
import openai
from gtts import gTTS
import speech_recognition as sr
import tempfile
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Data Assistant AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🤖 Data Assistant AI")
st.caption("Chat • CSV • Camera • Voice • AI")

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

# ---------------- SIDEBAR ----------------
st.sidebar.header("📂 Inputs")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / Image",
    type=["csv", "png", "jpg", "jpeg"]
)

camera_image = st.sidebar.camera_input("📷 Capture Image")

# ---------------- FILE HANDLING ----------------
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        st.session_state.df = pd.read_csv(uploaded_file)
        st.sidebar.success("CSV uploaded")
        st.sidebar.dataframe(st.session_state.df.head())
    else:
        img = Image.open(uploaded_file)
        st.sidebar.image(img, caption="Uploaded Image")

if camera_image:
    img = Image.open(camera_image)
    st.sidebar.image(img, caption="Camera Image")

# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- VOICE INPUT ----------------
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return None

col1, col2 = st.columns([5, 1])
with col2:
    if st.button("🎤"):
        voice_text = voice_input()
        if voice_text:
            st.session_state.messages.append(
                {"role": "user", "content": voice_text}
            )

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Ask me anything…")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # ---------------- CSV LOGIC ----------------
    if st.session_state.df is not None:
        df = st.session_state.df
        if "columns" in prompt.lower():
            reply = f"Columns: {', '.join(df.columns)}"
        elif "shape" in prompt.lower():
            reply = f"Shape: {df.shape}"
        elif "describe" in prompt.lower():
            reply = str(df.describe())
        else:
            reply = "📊 CSV loaded. Ask about columns, shape, describe."

    # ---------------- IMAGE AI ----------------
    elif uploaded_file or camera_image:
        reply = "🖼️ Image received. Image AI description can be enabled."

    # ---------------- AI CHAT ----------------
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful data assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content

    # ---------------- SAVE + DISPLAY ----------------
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write(reply)

        # ---------------- VOICE OUTPUT ----------------
        tts = gTTS(reply)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name)
            os.unlink(fp.name)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Data Assistant AI | Mobile Friendly | Powered by Streamlit")

