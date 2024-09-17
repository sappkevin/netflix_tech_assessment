import csv
from utils import get_drive_service, list_files_and_folders, is_folder
from config import SOURCE_FOLDER_ID

def count_items_in_folder(service, folder_id):
    """
    Recursively count items in a folder.
    
    Returns:
    tuple: (total_items, total_folders)
    """
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

def generate_folder_structure_report_csv():
    """
    Generate a CSV report on the folder structure.
    """
    service = get_drive_service()
    
    # Get top-level folders
    top_level_items = list_files_and_folders(service, SOURCE_FOLDER_ID)
    top_level_folders = [item for item in top_level_items if is_folder(item)]
    
    total_nested_folders = 0
    
    # Create CSV file report 
    with open('./reports/assessment2_report.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header
        csvwriter.writerow(['Folder_Name', 'Total_Child_Objects', 'Total_Nested_Folders'])
        
        for folder in top_level_folders:
            items, folders = count_items_in_folder(service, folder['id'])
            csvwriter.writerow([folder['name'], items, folders])
            
            total_nested_folders += folders
        
        # Count total items and folders in the source folder
        total_items, total_folders = count_items_in_folder(service, SOURCE_FOLDER_ID)
    
    print(f"Report generated: assessment2_report.csv")

if __name__ == "__main__":
    generate_folder_structure_report_csv()