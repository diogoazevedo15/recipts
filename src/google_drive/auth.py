import streamlit as st
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import json

def authenticate():
    # Load environment variables
    load_dotenv()

    # Get the service account JSON string from the environment variable
    service_account_raw = os.getenv('SERVICE_ACCOUNT')

    if not service_account:
        st.error('Service account key not found in environment variables.')
        return None

    try:
        service_account_json = json.loads(service_account_raw)
        
    except json.JSONDecodeError as e:
        st.error(f'Failed to parse service account key JSON: {e}')
        return None

    # Create credentials using the service account info
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    try:
        credentials = service_account.Credentials.from_service_account_info(
            service_account_json, scopes=SCOPES)
    except Exception as e:
        st.error(f'Failed to create credentials: {e}')
        return None

    return credentials
