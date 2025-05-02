import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

st.set_page_config(page_title="Ram's Chat Box ", layout="centered")

st.markdown("""
    <style>
    .user-msg {
        background-color: black;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        max-width: 70%;
        align-self: flex-end;
        text-align: right;
    }
    .bot-msg {
        background-color: black;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        max-width: 70%;
        align-self: flex-start;
        text-align: left;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    </style>
""", unsafe_allow_html=True)

# Session state for storing chat
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_gemini_response(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }
    try:
        response = requests.post(
            f"{GEMINI_URL}?key={API_KEY}",
            headers=headers,
            json=data
        )
        json_data = response.json()
        if "candidates" not in json_data:
            return f"❌ Gemini Error: {json_data.get('error', {}).get('message', 'Unknown error')}"
        return json_data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"❌ Exception: {str(e)}"

st.title("💬Chat Box ")

# Display chat messages
for chat in st.session_state.messages:
    role = chat["role"]
    msg = chat["content"]
    class_name = "user-msg" if role == "user" else "bot-msg"
    st.markdown(f'<div class="chat-container"><div class="{class_name}">{msg}</div></div>', unsafe_allow_html=True)

# Input area
# user_input = st.text_input("Type your message...", key="input")

# Input area with enter-to-submit
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", key="input", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_reply = get_gemini_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.rerun()

# if st.button("Send") and user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     bot_reply = get_gemini_response(user_input)
#     st.session_state.messages.append({"role": "bot", "content": bot_reply})
#     st.rerun()
 