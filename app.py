import streamlit as st
import requests

# API Keys and URLs
BLAND_API_KEY = 'org_fcfd61ec9ebaa2fcfa5b6c3b225aa4dd603d0b587e1493e16003e3f8bed4db9f375dc3a57d2493367c2069'
BLAND_CALL_URL = "https://api.bland.ai/call"

# Task Script
TASK_SCRIPT = (
    "Say: Hello, how can I assist you today? "
    "Wait for the user's response and transcribe it in real time. "
    "Use the AI model (Grok) to analyze the user's query and generate a relevant response. "
    "Speak the AI-generated response to the user. "
    "Say: Would you like any more assistance? "
    "Say: Thank you for reaching out. Have a great day!"
)

# Streamlit UI
st.title("AI Call Assistant")
st.write("Initiate a call using Bland.AI")

# User Input
email = st.text_input("Email")
name = st.text_input("Name")
phone = st.text_input("Phone Number")

if st.button("Initiate Call"):
    if not email or not name or not phone:
        st.error("Please provide all required fields: Email, Name, and Phone Number.")
    else:
        call_data = {
            "phone_number": phone,
            "task": TASK_SCRIPT,
            "summarize": True,
            "record": True,
            "max_duration": "1"
        }

        headers = {"Authorization": f"Bearer {BLAND_API_KEY}", "Content-Type": "application/json"}
        
        try:
            response = requests.post(BLAND_CALL_URL, json=call_data, headers=headers)
            if response.status_code == 200:
                call_response = response.json()
                call_id = call_response.get("call_id")
                st.success(f"Call initiated successfully! Call ID: {call_id}")
            else:
                st.error(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {str(e)}")
