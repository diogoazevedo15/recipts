# app.py

import streamlit as st
from login import login

def main_app():
    st.title("Main Application")
    st.write(f"Welcome to the main app, {st.session_state.get('username', '')}!")

    # Logout button
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.rerun()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''

    if st.session_state['logged_in']:
        main_app()
    else:
        login()

if __name__ == "__main__":
    main()
