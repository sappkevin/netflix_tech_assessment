import logging
import os
import time
from datetime import datetime
from utils import get_drive_service, list_files_and_folders, is_folder
from config import SOURCE_FOLDER_ID, DESTINATION_FOLDER_ID
from googleapiclient.errors import HttpError

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Set up logging
logging.basicConfig(filename='./reports/assessment3_report.log', level=logging.INFO, 
                    format='%(asctime)s,%(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

def log_action(action, source, destination, result):
    """
    Log an action to the log file.
    """
    logging.info(f"{action},{source},{destination},{result}")

def retry_on_failure(func):
    def wrapper(*args, **kwargs):
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except HttpError as error:
                if error.resp.status in [429, 500, 502, 503, 504] and attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    logging.error(f"HTTP error in {func.__name__}: {error}")
                    raise
            except Exception as error:
                logging.error(f"Unexpected error in {func.__name__}: {error}")
                raise
        raise Exception(f"Max retries exceeded in {func.__name__}")
    return wrapper

@retry_on_failure
def copy_folder(service, source_folder_id, destination_folder_id, folder_name, source_path):
    """
    Create a new folder in the destination and log the action.
    """
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [destination_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    new_folder_id = folder.get('id')
    destination_path = f"{source_path}/{folder_name}"
    log_action("copy", source_path, destination_path, "success")
    return new_folder_id

@retry_on_failure
def copy_file(service, file_id, file_name, destination_folder_id, source_path):
    """
    Copy a file to the destination folder and log the action.
    """
    try:
        file_metadata = {'name': file_name, 'parents': [destination_folder_id]}
        copied_file = service.files().copy(fileId=file_id, body=file_metadata).execute()
        destination_path = f"{source_path}/{file_name}"
        log_action("copy", source_path, destination_path, "success")
        return copied_file.get('id')
    except Exception as e:
        destination_path = f"{source_path}/{file_name}"
        log_action("copy", source_path, destination_path, f"failure: {str(e)}")
        raise

@retry_on_failure
def copy_folder_contents(service, source_folder_id, destination_folder_id, current_path=""):
    """
    Recursively copy the contents of a folder to the destination.
    """
    items = list_files_and_folders(service, source_folder_id)
    
    for item in items:
        source_path = f"{current_path}/{item['name']}"
        if is_folder(item):
            new_folder_id = copy_folder(service, item['id'], destination_folder_id, item['name'], source_path)
            copy_folder_contents(service, item['id'], new_folder_id, source_path)
        else:
            copy_file(service, item['id'], item['name'], destination_folder_id, source_path)

def copy_source_to_destination():
    """
    Main function to copy the entire source folder to the destination folder.
    """
    try:
        service = get_drive_service()
        copy_folder_contents(service, SOURCE_FOLDER_ID, DESTINATION_FOLDER_ID)
        print("Copy completed. Check assessment3.log for details.")
        return True
    except Exception as error:
        print(f"An error occurred during the copy process: {error}")
        return False

if __name__ == "__main__":
    copy_source_to_destination()