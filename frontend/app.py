import streamlit as st
import requests
from pathlib import Path

APP_DIR = Path(__file__).parent
IMAGE_PATH = APP_DIR / "image.png"

def init_session_states():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    if prompt := st.chat_input("Enter your data related question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        bot_response = st.session_state.bot.chat(prompt).get("bot")
        response = f"The Youtuber: {bot_response}"

        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

def layout():
    st.image(str(IMAGE_PATH))
    st.markdown("#🙌Ask the almighty Youtuber🙌")
    display_chat_messages()
    handle_user_input()

if __name__ == '__main__':
    init_session_states()
    layout()