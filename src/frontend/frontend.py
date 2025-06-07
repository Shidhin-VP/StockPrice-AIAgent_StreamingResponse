import streamlit as st
import requests

st.title("Chat Stream Demo")

# URL input field — user provides the full URL here
api_url = st.text_input("Enter the API URL")

# Prompt input field
prompt = st.text_input("Enter a prompt")

# Show and use api_url variable only if user has entered something
if st.button("Send") and prompt and api_url:
    try:
        # Use the variable api_url (user-provided)
        response = requests.post(
            api_url,
            json={"question": prompt},
            stream=True,
            headers={"Content-Type": "application/json"}
        )

        def generate_response():
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    yield chunk.decode("utf-8")

        st.write_stream(generate_response())

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
