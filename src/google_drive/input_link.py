# google_drive/input_link.py

import streamlit as st

def input_link():
    st.header("Connect to Google Drive Folder")
    folder_link = st.text_input("Enter the Google Drive Folder Link:")
    connect_button = st.button("Connect")
    return folder_link, connect_button