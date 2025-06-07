import streamlit as st
import requests

st.title("Chat Stream Demo")

prompt = st.text_input("Enter a prompt")

if st.button("Send") and prompt:
    response = requests.post(
        "https://mghptawlquy5nyskhlrwywrdqm0ptqni.lambda-url.us-east-1.on.aws/question",
        json={"Stockquestion": prompt},
        stream=True,
        headers={"Content-Type": "application/json"}
    )
    
    def generate_response():
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                yield chunk.decode("utf-8")
    
    st.write_stream(generate_response())