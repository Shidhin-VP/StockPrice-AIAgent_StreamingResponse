# import streamlit as st
# import requests
# import re
# import os
# from pathlib import Path

# S_accessCode=st.secrets['access_code']
# print(f"SAccess: {S_accessCode}")

# # --- Session State Setup ---
# if "authenticated" not in st.session_state:
#     st.session_state.authenticated = False

# if "api_url" not in st.session_state:
#     st.session_state.api_url = ""

# if "url_set" not in st.session_state:
#     st.session_state.url_set = False

# if "show_settings" not in st.session_state:
#     st.session_state.show_settings = True  

# # --- AUTH PAGE ---
# if not st.session_state.authenticated:
#     st.title("🔐 Enter Access Code to Continue")
#     access_code = st.text_input("Access Code", type="password")
#     if st.button("Unlock"):
#         if access_code == S_accessCode:  
#             st.session_state.authenticated = True
#             st.success("Access granted. Click Unlock again to be redirected")
#         else:
#             st.error("Invalid code.")
#     st.stop()

# # --- HEADER ---
# st.title("🤖 Stock Price Agent")


# if st.session_state.show_settings or not st.session_state.url_set:
#     with st.expander("🔧 Set API Endpoint (Required)", expanded=True):
#         new_url = st.text_input("Enter new API URL (Required):", value=st.session_state.api_url)
#         if st.button("Save Endpoint"):
#             if new_url.strip().startswith("http"):
#                 st.session_state.api_url = new_url.strip()
#                 st.session_state.url_set = True
#                 st.session_state.show_settings = False
#                 st.success("✅ Endpoint saved. Click Save Endpoint again to fold the Expander")
#             else:
#                 st.warning("⚠️ Please enter a valid URL starting with http or https.")
# else:
#     with st.container():
#         col1, col2 = st.columns([0.85, 0.15])
#         with col2:
#             if st.button("⚙️"):
#                 st.session_state.show_settings = True

# # --- MAIN CHAT INTERFACE ---
# if st.session_state.url_set:
#     prompt = st.text_input("💬 Enter your prompt")

#     if st.button("Submit"):
#         try:
#             response = requests.post(
#                 st.session_state.api_url,
#                 json={"prompt": prompt}
#             )

#             if response.ok:
#                 result = response.json()
#                 answer = result.get("AI Result", "No Result")
#                 cleanedAnswer = re.sub(r"<thinking>.*?</thinking>", "", answer, flags=re.DOTALL)
#                 st.write(cleanedAnswer.strip())
#             else:
#                 st.error(f"❌ Request failed: {response.status_code}")
#         except Exception as e:
#             st.error(f"⚠️ Error: {e}")
# else:
#     st.info("Please enter a valid API endpoint to continue.")



import streamlit as st
import requests
import re

# --- Secrets ---
S_accessCode = st.secrets['access_code']
print(f"SAccess: {S_accessCode}")

# --- Session State Setup ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "api_url" not in st.session_state:
    st.session_state.api_url = ""

if "url_set" not in st.session_state:
    st.session_state.url_set = False

if "show_settings" not in st.session_state:
    st.session_state.show_settings = True

if "username" not in st.session_state:
    st.session_state.username = ""

# --- AUTH PAGE ---
if not st.session_state.authenticated:
    st.title("🔐 Enter Access Code to Continue")
    access_code = st.text_input("Access Code", type="password")
    if st.button("Unlock"):
        if access_code == S_accessCode:
            st.session_state.authenticated = True
            st.success("Access granted. Click Unlock again to be redirected")
        else:
            st.error("Invalid code.")
    st.stop()

# --- HEADER ---
st.title("🤖 Stock Price Agent")

# --- SETTINGS SECTION ---
if st.session_state.show_settings or not st.session_state.url_set:
    with st.expander("🔧 Set API Endpoint and Username (Required)", expanded=True):
        new_url = st.text_input("Enter new API URL (Required):", value=st.session_state.api_url)
        username = st.text_input("Enter your name (Required):", value=st.session_state.username)

        if st.button("Save Endpoint"):
            if new_url.strip().startswith("http") and username.strip():
                st.session_state.api_url = new_url.strip()
                st.session_state.username = username.strip()
                st.session_state.url_set = True
                st.session_state.show_settings = False
                st.success("✅ Info saved. Click Save Endpoint again to fold the Expander")
            else:
                st.warning("⚠️ Please enter a valid URL and name.")
else:
    with st.container():
        col1, col2 = st.columns([0.85, 0.15])
        with col2:
            if st.button("⚙️"):
                st.session_state.show_settings = True

# --- MAIN CHAT INTERFACE ---
if st.session_state.url_set:
    prompt = st.text_input("💬 Enter your prompt")

    if st.button("Submit"):
        try:
            # Send request with stream=True
            response = requests.post(
                st.session_state.api_url,
                json={
                    "Stockquestion": prompt,  # adjust if API expects different key
                    "name": st.session_state.username
                },
                stream=True,
                headers={"Content-Type": "application/json"}
            )

            # Display the streaming content
            def generate_response():
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk.decode("utf-8")

            st.write_stream(generate_response())

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Request failed: {e}")
else:
    st.info("Please enter a valid API endpoint and username to continue.")
