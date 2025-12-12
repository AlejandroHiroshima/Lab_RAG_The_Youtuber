import streamlit as st
import requests
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
APP_DIR = Path(__file__).parent
IMAGE_PATH = APP_DIR / "image.png"
API_URL= "http://127.0.0.1:7071"
BASE_URL = f"https://ragtheyoutuber.azurewebsites.net/rag/query?code={os.getenv('APP_KEY')}"

def init_session_states():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# below function (call_rag_api) is from LLM
def call_rag_api(prompt: str) -> dict:
    try:
        response = requests.post(
            BASE_URL,
            json={"prompt": prompt},
            timeout=20
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error calling API: {e}")
        return None

def handle_user_input():
    if prompt := st.chat_input("Enter your data related question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = call_rag_api(prompt)
        response_text= "The Youtuber is busy, try again later!"
        filename= "Unknown"
        filepath = None
        if response:
            answer = response.get("answer", response_text)
            filename = response.get("filename", filename)
            filepath= response.get("filepath", filepath)
            response_text = f"**The Youtuber:** {answer}"
            st.markdown(f"""{response_text} \n
            Source transcript: *{filename}*
            """)
        else: 
            st.markdown(response_text)

        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_text, 
            "filename": filename, 
            "filepath": filepath})

def layout():
    st.image(str(IMAGE_PATH))
    st.markdown("# Consult the almighty Youtuber🙌")
    display_chat_messages()
    handle_user_input()

if __name__ == '__main__':
    init_session_states()
    layout()