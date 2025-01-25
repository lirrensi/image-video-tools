import os
import shutil
from datetime import datetime

def get_creation_date(file_path):
    return os.path.getctime(file_path)

def create_folder_structure(base_path, year, month):
    year_path = os.path.join(base_path, str(year))
    month_path = os.path.join(year_path, str(month).zfill(2))  # Ensure the month is two digits
    os.makedirs(month_path, exist_ok=True)
    return month_path

def move_files_to_date_folders():
    current_directory = os.getcwd()
    current_script_name = os.path.basename(__file__)
    files = [f for f in os.listdir(current_directory) if os.path.isfile(f) and f != current_script_name]
    total_files = len(files)
    if total_files == 0:
        print("No files to process.")
        return

    for index, file_name in enumerate(files):
        file_path = os.path.join(current_directory, file_name)
        creation_date = datetime.fromtimestamp(get_creation_date(file_path))
        year = creation_date.year
        month = creation_date.month

        destination_folder = create_folder_structure(current_directory, year, month)
        shutil.move(file_path, os.path.join(destination_folder, file_name))

        # Print progress
        progress = (index + 1) / total_files * 100
        print(f"Processed {index + 1}/{total_files} files ({progress:.2f}%)")

if __name__ == "__main__":
    move_files_to_date_folders()
