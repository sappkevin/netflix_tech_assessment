import logging
from datetime import datetime
from utils import get_drive_service, list_files_and_folders, is_folder
from config import SOURCE_FOLDER_ID, DESTINATION_FOLDER_ID
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import io

# Set up logging
logging.basicConfig(filename='./reports/assessment3_report.log', level=logging.INFO, 
                    format='%(asctime)s,%(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

def log_action(action, source, destination, result):
    """
    Log an action to the log file.
    """
    logging.info(f"{action},{source},{destination},{result}")

def copy_folder(service, source_folder_id, destination_folder_id, folder_name, source_path):
    """
    Create a new folder in the destination and log the action.
    
    Args:
    service: Google Drive API service instance
    source_folder_id: ID of the source folder
    destination_folder_id: ID of the destination folder
    folder_name: Name of the folder to create
    source_path: Full path of the source folder
    
    Returns:
    str: ID of the newly created folder
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

def copy_file(service, file_id, file_name, destination_folder_id, source_path):
    """
    Copy a file to the destination folder and log the action.
    """
    try:
        # use the Drive API's copy method
        file_metadata = {'name': file_name, 'parents': [destination_folder_id]}
        
        copied_file = service.files().copy(fileId=file_id, body=file_metadata).execute()
        
        destination_path = f"{source_path}/{file_name}"
        log_action("copy", source_path, destination_path, "success")
        return copied_file.get('id')
    except Exception as e:
        destination_path = f"{source_path}/{file_name}"
        log_action("copy", source_path, destination_path, f"failure: {str(e)}")
        return None

def copy_folder_contents(service, source_folder_id, destination_folder_id, current_path=""):
    """
    Recursively copy the contents of a folder to the destination.
    
    Args:
    service: Google Drive API service instance
    source_folder_id: ID of the source folder
    destination_folder_id: ID of the destination folder
    current_path: Current path in the folder structure (for logging purposes)
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
    service = get_drive_service()
    copy_folder_contents(service, SOURCE_FOLDER_ID, DESTINATION_FOLDER_ID)
    print("Copy completed. Check assessment3.log for details.")

if __name__ == "__main__":
    copy_source_to_destination()
