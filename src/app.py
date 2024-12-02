import streamlit as st
from login import login
from google_drive import main as google_drive_page

def main_app():
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Google Drive", "Local"])

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        # Clear all session state variables
        st.session_state.clear()
        st.rerun()

    # Load the appropriate page/module
    if page == "Google Drive":
        google_drive_page.app()

def main():
    # Initialize session state variables if not present
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''

    if st.session_state['logged_in']:
        main_app()
    else:
        login()

if __name__ == "__main__":
    main()