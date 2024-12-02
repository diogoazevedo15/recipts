import streamlit as st
import pandas as pd

def display_table(files):
    # Create a DataFrame with the file names, links, and other columns
    if 'edited_df' in st.session_state and st.session_state['edited_df'] is not None:
        df = st.session_state['edited_df']
    else:
        df = pd.DataFrame({
            'Name': [file['name'] for file in files],
            'Link': [file['webViewLink'] for file in files],
            'NIF': ['' for _ in files],
            'IVA': ['' for _ in files],
            'Value': ['' for _ in files]
        })

    # Configure the 'Link' column to be displayed as clickable hyperlinks
    column_config = {
        'Link': st.column_config.LinkColumn(
            "File Link",
            help="Click to open the file in Google Drive",
            validate=None,  # No need to validate URLs if they are from known sources
            max_chars=20,  # Display the full URL or set a limit
            # Optionally, display custom text instead of the URL
            # For example, display 'Open File' instead of the full URL
            # hide_link_text=False displays the URL; set to True to hide it
            # display_text can be a string or regex pattern
            display_text="Open File",
            # hide_link_text=True,
        )
    }

    # Display the DataFrame as an editable table with column configuration
    edited_df = st.data_editor(
        df,
        width=500000, # High width to fill full page width
        num_rows="dynamic",
        key='data_editor',
        column_config=column_config,
        hide_index=True,
    )
    return edited_df