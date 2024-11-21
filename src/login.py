# login.py

import streamlit as st
from dotenv import load_dotenv
import os
import json

def load_credentials():
    load_dotenv()

    # Option 2: Using CREDENTIALS variable
    credentials_str = os.getenv('CREDENTIALS') 
    credentials = json.loads(credentials_str)
    return credentials

def login():
    st.title("Login Page")

    credentials = load_credentials()

    # Input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in credentials and password == credentials[username]:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Logged in successfully as {username}!")
            st.rerun()  # Refresh the page
        else:
            st.error("Invalid username or password")
