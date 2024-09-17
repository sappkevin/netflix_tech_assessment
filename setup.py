'''
Purpose: This setup script creates the Google Drive destination folder and gets the folder ID needed for assessments1-3.py.
          It also creates the token.json needed to connect to the Google Drive API

'''

import os
from config import DESTINATION_FOLDER_NAME, CREDENTIALS_FILE, SCOPES
from utils import get_google_drive_creds, create_folder

def main():
    # Get Google Drive credentials
    creds = get_google_drive_creds(SCOPES, token_file='token.json', credentials_file=CREDENTIALS_FILE)

    # Create the destination folder
    folder_id = create_folder(DESTINATION_FOLDER_NAME, creds)

    if folder_id:
        print(f"Destination folder '{DESTINATION_FOLDER_NAME}' created or found with ID: {folder_id}")
        # Set the folder_id as an environment variable for future use
        os.environ['DESTINATION_FOLDER_ID'] = folder_id
        return folder_id
    else:
        print("Failed to create or find the destination folder.")
        return None

if __name__ == "__main__":
    main()