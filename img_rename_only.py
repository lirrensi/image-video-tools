import os
from pathlib import Path
from datetime import datetime
import time

def rename_files():
    # Ask for target directory
    while True:
        target_dir = input("Enter the folder path to process: ").strip()
        target_path = Path(target_dir).expanduser().resolve()
        
        if not target_path.exists():
            print(f"Error: Folder '{target_dir}' does not exist")
            continue
        if not target_path.is_dir():
            print(f"Error: '{target_dir}' is not a directory")
            continue
        break
    
    # Ask for prefix
    prefix = input("Enter prefix for files (press Enter for 'iph'): ").strip()
    if not prefix:
        prefix = 'iph'
    
    # Counter for renamed files
    renamed_files = 0
    
    # Ask if user wants to process files recursively
    recursive = input("Process files in subfolders too? (y/n): ").lower().startswith('y')
    
    # Function to process files in a directory
    def process_directory(directory):
        nonlocal renamed_files
        
        # Get all files in the directory
        files = list(directory.rglob('*') if recursive else directory.glob('*'))
        
        # Filter out directories
        files = [f for f in files if f.is_file()]
        
        print(f"\nFound {len(files)} files to process in {directory}")
        proceed = input("Proceed with renaming? (y/n): ").lower().startswith('y')
        
        if not proceed:
            print("Operation cancelled by user")
            return
        
        for file_path in files:
            try:
                # Get file modification timestamp
                mod_time = os.path.getmtime(file_path)
                mod_datetime = datetime.fromtimestamp(mod_time)
                
                # Format the modification datetime
                date_str = mod_datetime.strftime('%Y_%m_%d__%H_%M')
                
                # Get original filename and extension
                original_name = file_path.stem
                original_ext = file_path.suffix
                
                # Generate new filename
                new_name = f"{prefix}__{date_str}__{original_name}{original_ext}"
                new_path = file_path.parent / new_name
                
                # Handle duplicate filenames
                counter = 1
                while new_path.exists():
                    new_name = f"{prefix}__{date_str}__{original_name}_{counter}{original_ext}"
                    new_path = file_path.parent / new_name
                    counter += 1
                
                # Rename the file
                file_path.rename(new_path)
                renamed_files += 1
                print(f"Renamed: {file_path.name} -> {new_name}")
                
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
    
    # Start processing
    try:
        print(f"\nProcessing folder: {target_path}")
        process_directory(target_path)
        print(f"\nOperation completed! {renamed_files} files renamed")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    rename_files()