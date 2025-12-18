import streamlit as st
import pandas as pd
from PIL import Image
import speech_recognition as sr

st.set_page_config(page_title="Data Assistant", layout="wide")

st.title("🤖 Data Assistant Chatbot")

# -------------------- SIDEBAR --------------------
st.sidebar.header("📂 Inputs")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV / Image",
    type=["csv", "png", "jpg", "jpeg"]
)

camera_image = st.sidebar.camera_input("📷 Capture Image")

st.sidebar.markdown("---")
st.sidebar.info("You can chat, upload data, capture images, or use voice input.")

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "df" not in st.session_state:
    st.session_state.df = None

# -------------------- FILE HANDLING --------------------
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        st.session_state.df = pd.read_csv(uploaded_file)
        st.sidebar.success("CSV uploaded successfully")
        st.sidebar.dataframe(st.session_state.df.head())

    else:
        image = Image.open(uploaded_file)
        st.sidebar.image(image, caption="Uploaded Image")

if camera_image:
    image = Image.open(camera_image)
    st.sidebar.image(image, caption="Camera Image")

# -------------------- CHAT HISTORY --------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------- VOICE INPUT --------------------
def voice_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return "Sorry, I could not understand."

col1, col2 = st.columns([4, 1])
with col2:
    if st.button("🎤 Voice"):
        voice_text = voice_to_text()
        st.session_state.messages.append(
            {"role": "user", "content": voice_text}
        )

# -------------------- CHAT INPUT --------------------
user_input = st.chat_input("Ask me about your data, image, or anything...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # -------------------- BOT LOGIC --------------------
    reply = ""

    if st.session_state.df is not None:
        df = st.session_state.df

        if "head" in user_input.lower():
            reply = str(df.head())

        elif "columns" in user_input.lower():
            reply = f"Columns are: {', '.join(df.columns)}"

        elif "shape" in user_input.lower():
            reply = f"Dataset shape: {df.shape}"

        elif "describe" in user_input.lower():
            reply = str(df.describe())

        else:
            reply = "📊 CSV detected. Try: head, columns, shape, describe"

    elif uploaded_file or camera_image:
        reply = "🖼️ Image received. Image AI can be added next."

    else:
        reply = f"You said: {user_input}"

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write(reply)

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("🚀 Data Assistant | Chat • CSV • Camera • Voice")


