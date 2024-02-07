import io
import os.path

# google imports
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# project imports
from auth.scopes import SCOPES
from auth.auth import get_creds


def download_file(item, service):
    file = io.BytesIO()
    try:
        request = service.files().export_media(
            fileId=item['id'],
            mimeType="application/pdf"
        )
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Downloading: {item['name']}")
            print(f"Download {int(status.progress() * 100)}.")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    file.seek(0)

    with open(f"../downloaded_files/{item['name']}.pdf", 'wb') as f:
        f.write(file.read())
        f.close()


def main():
    credentials = None

    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        get_creds(credentials)
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)

    try:
        service = build("drive", "v3", credentials=credentials)
        results = (service.files().list().execute())
        items = results.get("files", [])
        if not items:
            print("No files found!")
        else:
            for item in items:
                download_file(item=item, service=service)
                break

    except HttpError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
