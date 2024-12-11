import streamlit as st
import pandas as pd

def display_table(db_df):
    # Prepare the DataFrame for display
    display_df = db_df.reset_index()[['Id', 'Name', 'Link', 'IVA', 'Value', 'Confidence']]
    display_df.set_index('Id', inplace=True)

    # Map confidence values to emojis
    def get_confidence_emoji(confidence):
        if pd.notnull(confidence):
            if confidence >= 0.94:
                return '✅'  # Green checkmark
            else:
                return '⚠️'  # Warning emoji
        else:
            return ''  # Empty string if confidence is None

    display_df['Confidence'] = display_df['Confidence'].apply(get_confidence_emoji)

    # Configure the columns
    column_config = {
        'Link': st.column_config.LinkColumn(
            "File Link",
            help="Click to open the file in Google Drive",
            max_chars=20,
            validate=None,
            display_text="Open File",
        ),
        'Confidence': st.column_config.TextColumn(
            "Confidence",
            help="Confidence level of the text extraction",
            width="small",
        ),
        'Id': None  # Hide the index column
    }

    # Display the DataFrame as an editable table
    edited_df = st.data_editor(
        display_df,
        num_rows="dynamic",
        key='data_editor',
        column_config=column_config,
    )
    return edited_df