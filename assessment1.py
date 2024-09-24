import json
import os
import time
from utils import get_drive_service, list_files_and_folders, is_folder, is_file
from config import SOURCE_FOLDER_ID
from googleapiclient.errors import HttpError

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def generate_root_report():
    """
    Generate a JSON report of the root folder contents.
    """
    for attempt in range(MAX_RETRIES):
        try:
            service = get_drive_service()
            items = list_files_and_folders(service, SOURCE_FOLDER_ID)
            
            num_files = sum(1 for item in items if not is_folder(item))  # Changed this line
            num_folders = sum(1 for item in items if is_folder(item))
            
            report_data = {
                "total_files": num_files,
                "total_folders": num_folders
            }

            os.makedirs('./reports', exist_ok=True)
            json_filename = './reports/assessment1_report.json'
            with open(json_filename, 'w') as jsonfile:
                json.dump(report_data, jsonfile, indent=2)

            print(f"Report generated: {json_filename}")
            print(json.dumps(report_data, indent=2))
            
            return report_data

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
    generate_root_report()
