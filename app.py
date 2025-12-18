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
st.caption("Chat • CSV • Image • Camera • Voice")

# ---------------- SESSION STATE ----------------
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

# ---------------- QUICK CHAT BUTTONS ----------------
st.markdown("### ⚡ Quick Actions")

b1, b2, b3, b4 = st.columns(4)

if b1.button("1️⃣ Analyze CSV"):
    st.session_state.messages.append(
        {"role": "user", "content": "Analyze the uploaded CSV file"}
    )

if b2.button("2️⃣ Describe Data"):
    st.session_state.messages.append(
        {"role": "user", "content": "Describe the data and give insights"}
    )

if b3.button("3️⃣ Analyze Image"):
    st.session_state.messages.append(
        {"role": "user", "content": "Analyze the uploaded or camera image"}
    )

if b4.button("4️⃣ AI Chat"):
    st.session_state.messages.append(
        {"role": "user", "content": "Hello AI, help me"}
    )

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
    if st.button("🎤 Voice"):
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

# ---------------- RESPONSE LOGIC ----------------
if len(st.session_state.messages) > 0:
    last_msg = st.session_state.messages[-1]

    if last_msg["role"] == "user":

        user_text = last_msg["content"]

        # CSV logic
        if st.session_state.df is not None:
            df = st.session_state.df

            if "analyze" in user_text.lower():
                reply = f"Dataset has {df.shape[0]} rows and {df.shape[1]} columns."

            elif "describe" in user_text.lower():
                reply = str(df.describe())

            elif "columns" in user_text.lower():
                reply = "Columns: " + ", ".join(df.columns)

            else:
                reply = "📊 CSV loaded. Try: analyze, describe, columns."

        # Image logic
        elif uploaded_file or camera_image:
            reply = "🖼️ Image received. Image AI analysis can be expanded."

        # AI Chat
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_text}
                ]
            )
            reply = response.choices[0].message.content

        # Save assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        with st.chat_message("assistant"):
            st.write(reply)

            # Voice output
            tts = gTTS(reply)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name)
                os.unlink(fp.name)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 Data Assistant AI | Streamlit Cloud")
