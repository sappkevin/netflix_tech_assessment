import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import os

from config import CREDENTIALS_FILE # Get cred file

SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']


# Ensure the reports directory exists
os.makedirs('reports/', exist_ok=True)

"""
Get or refresh Google Drive credentials.
"""
def get_google_drive_creds(scopes, token_file='token.json', credentials_file='credentials.json'):
    
    creds = None
    
    # Check if token file exists and load credentials
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    
    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    return creds

"""
Initialize the Google Drive v3 resource object
"""
def get_drive_service():
    creds = get_google_drive_creds(SCOPES, token_file='token.json', credentials_file=CREDENTIALS_FILE)
    return build('drive', 'v3', credentials=creds)

"""
List the files and folders
"""
def list_files_and_folders(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name, mimeType)"
    ).execute()
    return results.get('files', [])

"""
Check if Google Drive item is a folder 
"""
def is_folder(item):
    return item['mimeType'] == 'application/vnd.google-apps.folder'
'''
Check if Google Drive item is a file
'''
def is_file(item):
    return item['mimeType'] == 'application/vnd.google-apps.file'

'''
Get object mime type
'''
def get_mimetype(item):
    return item['mimeType']

"""
Create a folder if it doesn't exist and print the folder ID.
"""
#Source: https://developers.google.com/drive/api/guides/folder#python

def create_folder(foldername, creds):
    
    try:
        # If creds is None, use default credentials
        if creds is None:
            creds = get_google_drive_creds(SCOPES, token_file='token.json', credentials_file=CREDENTIALS_FILE)

        # Create drive api client
        service = build("drive", "v3", credentials=creds)

        # Check if folder already exists
        response = service.files().list(
            q=f"mimeType='application/vnd.google-apps.folder' and name='{foldername}' and trashed=false",
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        if response['files']:
            # Folder exists, return its ID
            folder_id = response['files'][0]['id']
            print(f'Folder "{foldername}" already exists with ID: "{folder_id}".')
            return folder_id
        else:
            # Folder doesn't exist, create it
            file_metadata = {
                "name": foldername,
                "mimeType": "application/vnd.google-apps.folder"
            }
            file = service.files().create(body=file_metadata, fields="id").execute()
            folder_id = file.get("id")
            print(f'Folder "{foldername}" created with ID: "{folder_id}".')
            return folder_id

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None