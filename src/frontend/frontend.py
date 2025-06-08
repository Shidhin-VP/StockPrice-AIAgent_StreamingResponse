# import streamlit as st
# import requests

# st.title("Chat Stream Demo")

# prompt = st.text_input("Enter a prompt")

# if st.button("Send") and prompt:
#     response = requests.post(
#         "https://taqs2mkiv2vlpbwvwik7quxfnm0mtnee.lambda-url.us-east-1.on.aws/question",
#         json={"Stockquestion": prompt},
#         stream=True,
#         headers={"Content-Type": "application/json"}
#     )
    
#     def generate_response():
#         for chunk in response.iter_content(chunk_size=None):
#             if chunk:
#                 yield chunk.decode("utf-8")
    
#     st.write_stream(generate_response())

import streamlit as st
import requests

st.title("Chat Stream Demo")

# Initialize session state for name
if "name_entered" not in st.session_state:
    st.session_state.name_entered = False

# Prompt for name if not already entered
if not st.session_state.name_entered:
    name = st.text_input("Please enter your name to continue")
    
    if name:
        st.session_state.name_entered = True
        st.session_state.user_name = name
        st.rerun()

# After name is entered, show prompt input
else:
    st.write(f"Hello **{st.session_state.user_name}**, you can now enter a prompt below.")

    prompt = st.text_input("Enter a prompt")

    if st.button("Send") and prompt:
        response = requests.post(
            "https://daz2tpt3nxzbcgnfboc5nmmvay0xuqqt.lambda-url.us-east-1.on.aws/question",
            json={
                "Stockquestion": prompt,
                "name": st.session_state.user_name
            },
            stream=True,
            headers={"Content-Type": "application/json"}
        )

        def generate_response():
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    yield chunk.decode("utf-8")

        st.write_stream(generate_response())
