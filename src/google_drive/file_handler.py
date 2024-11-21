# google_drive/file_handler.py

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

def get_folder_id(folder_link):
    # Extract folder ID from the link
    match = re.search(r'/folders/([a-zA-Z0-9_-]+)', folder_link)
    if match:
        return match.group(1)
    else:
        return None

def list_images(credentials, folder_id):
    try:
        service = build('drive', 'v3', credentials=credentials)
        # Query to get image files in the folder
        query = f"'{folder_id}' in parents and (mimeType contains 'image/jpeg' or mimeType contains 'image/png')"
        results = service.files().list(
            q=query,
            pageSize=1000,
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        return items
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []
