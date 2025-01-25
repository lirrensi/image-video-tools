import os
from pathlib import Path
from datetime import datetime
import time
from PIL import Image
import pillow_heif
from PIL.ExifTags import TAGS
import ffmpeg

# Register HEIF format support
pillow_heif.register_heif_opener()

def get_media_date(file_path):
    """Extract date from media file based on type"""
    extension = file_path.suffix.lower()
    
    # Try to get EXIF date for images
    if extension in ['.jpg', '.jpeg', '.heic', '.png', '.tiff', '.bmp']:
        try:
            with Image.open(file_path) as img:
                exif = img.getexif()
                if exif:
                    # Try different EXIF date tags
                    for tag_id in [36867, 36868, 306, 50971]:  # DateTimeOriginal, DateTimeDigitized, DateTime, DateTimeCreated
                        if tag_id in exif:
                            date_str = exif[tag_id]
                            try:
                                # Parse EXIF date format (YYYY:MM:DD HH:MM:SS)
                                return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                            except ValueError:
                                continue
                            
        except Exception as e:
            print(f"EXIF read error for {file_path.name}: {e}")
    
    # Try to get creation date for videos
    elif extension in ['.mp4', '.mov', '.m4v', '.avi']:
        try:
            probe = ffmpeg.probe(str(file_path))
            creation_time = probe['format'].get('tags', {}).get('creation_time')
            if creation_time:
                return datetime.strptime(creation_time.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        except Exception as e:
            print(f"Video metadata read error for {file_path.name}: {e}")
    
    # Fallback to file modification time
    return datetime.fromtimestamp(os.path.getmtime(file_path))

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
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.heic', '.png', '.tiff', '.bmp', 
                          '.mp4', '.mov', '.m4v', '.avi'}
    
    # Function to process files in a directory
    def process_directory(directory):
        nonlocal renamed_files
        
        # Get all files in the directory
        files = list(directory.rglob('*') if recursive else directory.glob('*'))
        
        # Filter out directories and unsupported files
        files = [f for f in files if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS]
        
        print(f"\nFound {len(files)} supported files to process in {directory}")
        proceed = input("Proceed with renaming? (y/n): ").lower().startswith('y')
        
        if not proceed:
            print("Operation cancelled by user")
            return
        
        for file_path in files:
            try:
                # Get date from media file
                media_datetime = get_media_date(file_path)
                
                # Format the datetime
                date_str = media_datetime.strftime('%Y_%m_%d__%H_%M')
                
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