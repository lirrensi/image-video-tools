import os
import shutil
from datetime import datetime

def filter_and_move_files(source_folder, target_folder=None, search_string=''):
    """
    Moves files from a source folder to a target folder if the filename contains a given search string.
    File timestamps are preserved during the move.
    
    Parameters:
    source_folder (str): The folder to search for files.
    target_folder (str, optional): The destination folder to move files to. If not provided, defaults to 'filtered' in the same directory as the source folder.
    search_string (str, optional): The string to search for in the filenames. If not provided, all files in the source folder will be moved.
    """
    if not target_folder:
        target_folder = os.path.join(os.path.dirname(source_folder), 'filtered')
        
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        
    for filename in os.listdir(source_folder):
        if search_string in filename:
            source_path = os.path.join(source_folder, filename)
            target_path = os.path.join(target_folder, filename)
            
            # Get file creation and modification times
            creation_time = os.path.getctime(source_path)
            modification_time = os.path.getmtime(source_path)
            
            # Move the file to the target folder
            shutil.move(source_path, target_path)
            
            # Set the creation and modification times of the moved file
            os.utime(target_path, (creation_time, modification_time))
            
            print(f"Moved '{filename}' to '{target_folder}'")


# Ask the user for the source folder
source_folder = input("Enter the source folder path: ")

# Ask the user for the search string (optional)
# search_string = input("Enter the search string (leave blank for all files): ")

# Call the filter_and_move_files function
filter_and_move_files(source_folder, search_string='vlcsnap-')