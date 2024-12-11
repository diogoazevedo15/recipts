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
    from googleapiclient.discovery import build
    service = build('drive', 'v3', credentials=credentials)

    query = f"'{folder_id}' in parents and trashed = false"
    fields = "nextPageToken, files(id, name, mimeType, webViewLink)"
    files = []
    page_token = None

    while True:
        response = service.files().list(
            q=query,
            fields=fields,
            pageToken=page_token
        ).execute()

        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    return files