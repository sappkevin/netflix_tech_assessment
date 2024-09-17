import os

# Netflix Source Google folder ID
SOURCE_FOLDER_ID = os.environ.get('SOURCE_FOLDER_ID', '1cpo-7jgKSMdde-QrEJGkGxN1QvYdzP9V')

# Destination Google folder ID
#Generate Folder if it does not exist
DESTINATION_FOLDER_NAME = 'Netflix_Tech_Assessment_ksapp'

#Get folder ID for Destination folder
DESTINATION_FOLDER_ID = os.environ.get('DESTINATION_FOLDER_ID', '1VLwkNFmnM7-a62k_N1sOCbTX46Utqm_V')

# Google Drive API credentials JSON file
CREDENTIALS_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', './credentials.json')

# Scopes required for the application
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']