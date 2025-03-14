import streamlit as st
import requests
import json

# Vapi API Configuration
API_URL = "https://api.vapi.ai/call"
API_KEY = "a56e1c14-05a3-4d8a-860a-895433d0036a"  # Replace with your actual API key

# Streamlit UI
st.title("Outbound Demo Call")

phone_number_id = "6234efbc-5e43-41be-837d-598a322dfb01"
customer_number = st.text_input("Enter Customer's Phone Number:")

if st.button("Initiate Call"):
    if not phone_number_id or not customer_number:
        st.error("Customer Number is required!")
    else:
        # Payload based on updated request format
        data = {
            "assistantId": "c5a27224-a7b0-43da-8dbe-0ff8649316c0",
            "phoneNumberId": phone_number_id,
            "customer": {
                "number": customer_number
            }
        }

        # Send API request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(data))

        # Handle API response
        if response.status_code == 201:
            st.success("Call initiated successfully!")      
        else:
            st.error("Error initiating call")
            st.json(response.json())  # Display error details
