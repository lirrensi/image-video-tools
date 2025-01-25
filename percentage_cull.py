import os
import random

def delete_random_files_in_directory():
    # Prompt for the path to the directory
    dir_path = input("Enter the directory path: ").strip()
    
    # Check if directory exists
    if not os.path.isdir(dir_path):
        print("Directory does not exist. Please enter a valid path.")
        return
    
    # Get the percentage of files to delete
    try:
        percent = float(input("Enter the percentage of files to delete (0-100): ").strip())
        if percent < 0 or percent > 100:
            raise ValueError("Percentage out of range.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    # List all files in the directory
    all_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    # Calculate the number of files to delete
    num_files_to_delete = int(len(all_files) * (percent / 100))
    
    # Select random files to delete
    files_to_delete = random.sample(all_files, num_files_to_delete)
    
    # Delete each selected file
    for file_name in files_to_delete:
        file_path = os.path.join(dir_path, file_name)
        os.remove(file_path)
        print(f"Deleted: {file_path}")

    print(f"Deleted {num_files_to_delete} out of {len(all_files)} files.")

# Run the function
delete_random_files_in_directory()
