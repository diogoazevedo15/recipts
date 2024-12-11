import streamlit as st
from . import input_link
from . import auth
from . import file_handler
from . import display_table
from text_extractor import text_extractor
import pandas as pd

def create_db_dataframe(files):
    # Create a DataFrame with file details
    df = pd.DataFrame({
        'Name': [file['name'] for file in files],
        'Id': [file['id'] for file in files],
        'Link': [file['webViewLink'] for file in files],
        'Type': [file['mimeType'] for file in files],
        'NIF': ['' for _ in files],
        'IVA': ['' for _ in files],
        'Value': ['' for _ in files],
        'Confidence': [None for _ in files],
        'Text': ['' for _ in files]
    })
    df.set_index('Id', inplace=True)
    return df

def app():
    st.title("Google Drive Integration")

    # Initialize session state variables
    if 'credentials' not in st.session_state:
        st.session_state['credentials'] = None
    if 'folder_id' not in st.session_state:
        st.session_state['folder_id'] = None
    if 'files' not in st.session_state:
        st.session_state['files'] = None
    if 'db_df' not in st.session_state:
        st.session_state['db_df'] = None
    if 'folder_link' not in st.session_state:
        st.session_state['folder_link'] = ''
    if 'show_toast' not in st.session_state:
        st.session_state['show_toast'] = False
    if 'extracted_data' not in st.session_state:
        st.session_state['extracted_data'] = None

    # Step 1: Input link and connect
    folder_link, connect_button = input_link.input_link()

    # Check if the connect button is pressed
    if connect_button and folder_link:
        # Reset session state variables
        for key in ['credentials', 'folder_id', 'files', 'db_df', 'extracted_data']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state['folder_link'] = folder_link

        # Re-run the script to apply changes
        st.rerun()

    # After rerun, check if folder_link is in session_state
    if st.session_state.get('folder_link', ''):
        folder_link = st.session_state['folder_link']

        # Authenticate if credentials are not loaded
        if st.session_state['credentials'] is None:
            credentials = auth.authenticate()
            if credentials:
                st.session_state['credentials'] = credentials
            else:
                st.stop()  # Stop execution if authentication fails

        # Get folder_id if not loaded
        if st.session_state['folder_id'] is None:
            folder_id = file_handler.get_folder_id(folder_link)
            if folder_id:
                st.session_state['folder_id'] = folder_id
            else:
                st.error("Invalid folder link. Please make sure you have entered the correct link.")
                st.stop()

        # List files if not loaded
        if st.session_state['files'] is None:
            files = file_handler.list_files(st.session_state['credentials'], st.session_state['folder_id'])
            if files:
                st.session_state['files'] = files
                # Create db_df
                st.session_state['db_df'] = create_db_dataframe(st.session_state['files'])
                # Show toast notification
                st.session_state['show_toast'] = True
                st.session_state['toast_message'] = f"Found {len(files)} file(s) in the folder."
            else:
                st.warning("No files found in the folder.")
                st.stop()
    else:
        st.info("Please enter a Google Drive folder link and click Connect.")

    # Display the table if db_df is available
    if st.session_state.get('db_df') is not None:
        # Display the table
        edited_df = display_table.display_table(st.session_state['db_df'])
        # Update 'IVA' and 'Value' back to db_df
        st.session_state['db_df'].loc[edited_df.index, ['IVA', 'Value']] = edited_df[['IVA', 'Value']]

        # Add a button to extract text and confidence
        if st.button("Extract Text and Confidence"):
            with st.spinner('Processing files...'):
                # Process the files to extract text and confidence
                extracted_df = text_extractor.process_files(
                    st.session_state['db_df'],
                    st.session_state['credentials']
                )
                st.session_state['extracted_data'] = extracted_df

                # Update 'Text' and 'Confidence' in db_df
                st.session_state['db_df'].update(extracted_df)

                # Re-render the table with updated data
                st.rerun()

    # Display the toast notification if the flag is set
    if st.session_state.get('show_toast', False):
        st.success(st.session_state.get('toast_message', ''))