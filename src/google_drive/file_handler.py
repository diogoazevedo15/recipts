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

def list_files(credentials, folder_id):
    try:
        service = build('drive', 'v3', credentials=credentials)
        # Query to get image and PDF files in the folder
        query = (
            f"'{folder_id}' in parents and "
            f"(mimeType contains 'image/jpeg' or "
            f"mimeType contains 'image/png' or "
            f"mimeType='application/pdf')"
        )
        results = service.files().list(
            q=query,
            pageSize=1000,
            fields="nextPageToken, files(id, name, webViewLink)"
        ).execute()
        items = results.get('files', [])
        return items
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None