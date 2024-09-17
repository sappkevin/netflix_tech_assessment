import json
from utils import get_drive_service, list_files_and_folders, is_folder, is_file
from config import SOURCE_FOLDER_ID
import os

def generate_root_report():
    """
    Generate a JSON report of the root folder contents.
    
    This function connects to the Google Drive API, retrieves information about
    the files and folders in the root of the specified source folder, and 
    generates a JSON report with the total number of files, folders, and items.
    
    The report is both saved to a file and printed to the console.
    """
    # Connect to the Google Drive API
    service = get_drive_service()
    
    # Retrieve all items (files and folders) in the root of the source folder
    items = list_files_and_folders(service, SOURCE_FOLDER_ID)
    
    # Count the number of files and folders
    num_files = sum(1 for item in items if is_file(item))
    num_folders = sum(1 for item in items if is_folder(item))
    
    # Prepare the report data
    report_data = {
        "total_files": num_files,
        "total_folders": num_folders
    }

    # Save the report to a JSON file in the reports directory
    json_filename = './reports/assessment1_report.json'
    with open(json_filename, 'w') as jsonfile:
        json.dump(report_data, jsonfile, indent=2)

    print(f"Report generated: {json_filename}")
    
    # Print the report to console as well
    print(json.dumps(report_data, indent=2))

if __name__ == "__main__":
    generate_root_report()
