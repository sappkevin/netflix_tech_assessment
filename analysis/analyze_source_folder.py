import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_drive_service, list_files_and_folders, is_folder, get_mimetype
from config import SOURCE_FOLDER_ID

# Set up logging
logging.basicConfig(filename='./reports/analyze_source_folder_structure.log', level=logging.INFO, 
                    format='%(asctime)s,%(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

def log_item(item_type,mime_type, path):
    """
    Log an item to the log file.
    """
    logging.info(f"{item_type},{mime_type},{path}")

def view_folder_contents(service, folder_id, current_path=""):
    """
    Recursively view the contents of a folder.
    
    Args:
    service: Google Drive API service instance
    folder_id: ID of the folder to view
    current_path: Current path in the folder structure (for logging purposes)
    """
    items = list_files_and_folders(service, folder_id)
    
    for item in items:
        item_path = f"{current_path}/{item['name']}"
        mimetype = get_mimetype(item)
        if is_folder(item):
            log_item("folder",mimetype, item_path)
            view_folder_contents(service, item['id'], item_path)
        else:
            log_item("file",mimetype,item_path)

def view_source_structure():
    """
    Main function to view the entire source folder structure.
    """
    service = get_drive_service()
    view_folder_contents(service, SOURCE_FOLDER_ID)
    print("Structure viewing completed. Check view_structure.log for details.")

if __name__ == "__main__":
    view_source_structure()