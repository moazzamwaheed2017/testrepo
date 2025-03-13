import streamlit as st
import requests
import json
from requests.auth import HTTPBasicAuth
from difflib import get_close_matches

# Twilio Credentials
account_sid = "AC9488694acbfe88b387a96e3f5850690d"
auth_token = "5735ff71c6db7b7ba0ab0dea485ecbfb"
twilio_phone_number = "+19566954595"

# Load JSON Data
def load_data():
    try:
        with open("scraped_data1.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return []

data = load_data()

# Enhanced search function to find closest matching answer
def search_query(query, data):
    questions = [entry["content"] for entry in data if "content" in entry]
    matches = get_close_matches(query, questions, n=1, cutoff=0.6)  # Adjust cutoff for better accuracy
    return matches[0] if matches else "I couldn't find relevant information. Can you rephrase?"

# Generate Twiml for Interactive Call
def generate_twiml():
    return (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<Response>"
        "<Gather input='speech' timeout='5' speechTimeout='auto' action='/process-query' method='GET'>"
        "<Say>Hello! Please ask your question.</Say>"
        "</Gather>"
        "<Redirect>/process-query</Redirect>"
        "</Response>"
    )

# Generate Twiml response based on caller's question
def generate_twiml_with_response(query):
    response_text = search_query(query, data)
    return (
        "<?xml version='1.0' encoding='UTF-8'?>"
        f"<Response><Say>{response_text}</Say><Redirect>/</Redirect></Response>"
    )

# Streamlit UI
st.title("AI Call Assistant")
st.write("Initiate an AI-powered call with real-time question answering")

# User Input
recipient_phone_number = st.text_input("Recipient Phone Number")

if st.button("Initiate Call"):
    if not recipient_phone_number:
        st.error("Please provide the recipient's phone number.")
    else:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls.json"
        
        data = {
            "From": twilio_phone_number,
            "To": recipient_phone_number,
            "Twiml": generate_twiml()
        }
        
        try:
            response = requests.post(url, data=data, auth=HTTPBasicAuth(account_sid, auth_token))
            if response.status_code == 201:
                call_response = response.json()
                call_sid = call_response.get("sid")
                st.success(f"Call initiated successfully! Call SID: {call_sid}")
            else:
                st.error(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {str(e)}")
