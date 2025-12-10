import streamlit as st
import requests
from pathlib import Path

APP_DIR = Path(__file__).parent
IMAGE_PATH = APP_DIR / "image.png"

def layout():
    st.image(str(IMAGE_PATH))
    st.markdown("#🙌Ask the almighty Youtuber🙌")
    input = st.text_input(label= "Enter your data related question")

    if st.button("Send") and input != "":
        repsonse = requests.post('http://127.0.0.1:8000/rag/query', json={"prompt": input})

        data = repsonse.json()

        st.markdown("##Question:")
        st.markdown(input)

        st.markdown("## Answer:")
        st.markdown(data["answer"])

        st.markdown("## Source:")
        st.markdown(data["filepath"])

if __name__ == '__main__':
    layout()