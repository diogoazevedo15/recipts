# google_drive/display_table.py

import streamlit as st
import pandas as pd

def display_table(image_files):
    # Create a DataFrame with the image names and empty columns
    if 'edited_df' in st.session_state and st.session_state['edited_df'] is not None:
        df = st.session_state['edited_df']
    else:
        df = pd.DataFrame({
            'Name': [file['name'] for file in image_files],
            'NIF': ['' for _ in image_files],
            'IVA': ['' for _ in image_files],
            'Value': ['' for _ in image_files]
        })

    # Display the DataFrame as an editable table
    edited_df = st.data_editor(df, num_rows="dynamic", key='data_editor')
    return edited_df
