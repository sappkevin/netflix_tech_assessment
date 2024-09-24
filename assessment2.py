import csv
import os
import time
from utils import get_drive_service, list_files_and_folders, is_folder
from config import SOURCE_FOLDER_ID
from googleapiclient.errors import HttpError

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def count_items_in_folder(service, folder_id):
    """
    Recursively count items in a folder.
    """
    for attempt in range(MAX_RETRIES):
        try:
            total_items = 0
            total_folders = 0
            items = list_files_and_folders(service, folder_id)
            
            for item in items:
                total_items += 1
                if is_folder(item):
                    total_folders += 1
                    sub_items, sub_folders = count_items_in_folder(service, item['id'])
                    total_items += sub_items
                    total_folders += sub_folders
            
            return total_items, total_folders

        except HttpError as error:
            if error.resp.status in [429, 500, 502, 503, 504] and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue
            else:
                print(f"An error occurred while counting items: {error}")
                raise
        except Exception as error:
            print(f"An unexpected error occurred while counting items: {error}")
            raise

    raise Exception("Max retries exceeded")

def generate_folder_structure_report_csv():
    """
    Generate a CSV report on the folder structure.
    """
    for attempt in range(MAX_RETRIES):
        try:
            service = get_drive_service()
            top_level_items = list_files_and_folders(service, SOURCE_FOLDER_ID)
            top_level_folders = [item for item in top_level_items if is_folder(item)]
            
            total_nested_folders = 0
            
            os.makedirs('./reports', exist_ok=True)

            with open('./reports/assessment2_report.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Folder_Name', 'Total_Child_Objects', 'Total_Nested_Folders'])
                
                for folder in top_level_folders:
                    items, folders = count_items_in_folder(service, folder['id'])
                    csvwriter.writerow([folder['name'], items, folders])
                    total_nested_folders += folders
                
                total_items, total_folders = count_items_in_folder(service, SOURCE_FOLDER_ID)
            
            print(f"Report generated: assessment2_report.csv")
            return {
                'total_items': total_items,
                'total_folders': total_folders,
                'total_nested_folders': total_nested_folders
            }

        except HttpError as error:
            if error.resp.status in [429, 500, 502, 503, 504] and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (2 ** attempt))
                continue
            else:
                print(f"An error occurred: {error}")
                raise
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            raise

    raise Exception("Max retries exceeded")

if __name__ == "__main__":
    generate_folder_structure_report_csv()