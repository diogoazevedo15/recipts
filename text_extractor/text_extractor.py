from google.cloud import vision
from googleapiclient.http import MediaIoBaseDownload
import io
import pandas as pd

def extract_text_from_image(image_content, credentials):
    """Extracts text and page confidence from image content using Google Vision API."""
    # Create a Vision client using the credentials
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Prepare the image
    image = vision.Image(content=image_content)

    # Perform document text detection
    response = client.document_text_detection(image=image)

    # Check for errors
    if response.error.message:
        raise Exception(
            f"Vision API Error: {response.error.message}\n"
            "For more info on error messages, check: https://cloud.google.com/apis/design/errors"
        )

    # Get the full text and page confidence
    annotation = response.full_text_annotation
    text = annotation.text if annotation.text else ''
    page_confidence = 0.0

    if annotation.pages:
        page_confidence = annotation.pages[0].confidence or 0.0

    return text, page_confidence

def process_files(db_df, credentials):
    """Processes files and extracts text and confidence."""
    from googleapiclient.discovery import build

    service = build('drive', 'v3', credentials=credentials)
    results = []

    for file_id, row in db_df.iterrows():
        mime_type = row['Type']

        # Only process image files
        if 'image/' in mime_type:
            # Download the image content from Google Drive
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

            # Reset the file handle position
            fh.seek(0)
            image_content = fh.read()

            # Extract text and confidence
            text, page_confidence = extract_text_from_image(image_content, credentials)

            # Append the result
            results.append({
                'Id': file_id,
                'Text': text,
                'Confidence': page_confidence
            })
        else:
            # Handle non-image files (e.g., PDFs)
            results.append({
                'Id': file_id,
                'Text': '',
                'Confidence': None
            })

    # Convert results to DataFrame and set 'Id' as index
    extracted_df = pd.DataFrame(results).set_index('Id')
    return extracted_df