import streamlit as st
from . import input_link
from . import auth
from . import file_handler
from . import display_table

def app():
    st.title("Google Drive Integration")

    # Initialize session state variables
    if 'credentials' not in st.session_state:
        st.session_state['credentials'] = None
    if 'folder_id' not in st.session_state:
        st.session_state['folder_id'] = None
    if 'files' not in st.session_state:
        st.session_state['files'] = None
    if 'edited_df' not in st.session_state:
        st.session_state['edited_df'] = None
    if 'folder_link' not in st.session_state:
        st.session_state['folder_link'] = ''
    if 'show_toast' not in st.session_state:
        st.session_state['show_toast'] = False

    # Step 1: Input link and connect
    folder_link, connect_button = input_link.input_link()

    # Check if the connect button is pressed
    if connect_button and folder_link:
        # Reset session state variables
        for key in ['credentials', 'folder_id', 'files', 'edited_df']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state['folder_link'] = folder_link

        # Re-run the script to apply changes
        st.rerun()

    # After rerun, check if folder_link is in session_state
    if 'folder_link' in st.session_state and st.session_state['folder_link']:
        folder_link = st.session_state['folder_link']

        # If credentials are not loaded, authenticate
        if st.session_state['credentials'] is None:
            credentials = auth.authenticate()
            if credentials:
                st.session_state['credentials'] = credentials
            else:
                st.stop()  # Stop execution if authentication fails

        # If folder_id is not loaded, get it from the folder link
        if st.session_state['folder_id'] is None:
            folder_id = file_handler.get_folder_id(folder_link)
            if folder_id:
                st.session_state['folder_id'] = folder_id
            else:
                st.error("Invalid folder link. Please make sure you have entered the correct link.")
                st.stop()

        # If files are not loaded, list files
        if st.session_state['files'] is None:
            files = file_handler.list_files(st.session_state['credentials'], st.session_state['folder_id'])
            if files:
                st.session_state['files'] = files
                # Set the flag to show the toast notification
                st.session_state['show_toast'] = True
                st.session_state['toast_message'] = f"Found {len(files)} file(s) in the folder."
            else:
                st.warning("No files found in the folder.")
                st.stop()
    else:
        st.info("Please enter a Google Drive folder link and click Connect.")

    # Display the table if files are available
    if st.session_state['files'] is not None:
        edited_df = display_table.display_table(st.session_state['files'])
        st.session_state['edited_df'] = edited_df

    # Display the toast notification if the flag is set
    if st.session_state.get('show_toast', False):
        st.toast(
            st.session_state.get('toast_message', ''),
            icon="✅"
        )