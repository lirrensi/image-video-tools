import os
import shutil
from pathlib import Path

def organize_files():
    # Get current working directory
    current_dir = Path.cwd()
    
    # Ask for destination folder name
    dest_folder_name = input("Enter destination folder name (press Enter for 'collected_files'): ").strip()
    if not dest_folder_name:
        dest_folder_name = "collected_files"
    
    # Create destination folder if it doesn't exist
    dest_folder = current_dir / dest_folder_name
    dest_folder.mkdir(exist_ok=True)
    
    # Counter for moved files
    moved_files = 0
    
    # Recursively find all files in all subdirectories
    for root, dirs, files in os.walk(current_dir):
        root_path = Path(root)
        
        # Skip the destination folder itself
        if root_path == dest_folder:
            continue
            
        # Process each file in current directory
        for file in files:
            source_file = root_path / file
            dest_file = dest_folder / file
            
            # Handle duplicate filenames
            if dest_file.exists():
                base = dest_file.stem
                suffix = dest_file.suffix
                counter = 1
                while dest_file.exists():
                    dest_file = dest_folder / f"{base}_{counter}{suffix}"
                    counter += 1
            
            # Move the file
            try:
                shutil.move(str(source_file), str(dest_file))
                moved_files += 1
                print(f"Moved: {source_file} -> {dest_file}")
            except Exception as e:
                print(f"Error moving {source_file}: {e}")
    
    print(f"\nOperation completed! {moved_files} files moved to '{dest_folder_name}'")
    
if __name__ == "__main__":
    try:
        organize_files()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")