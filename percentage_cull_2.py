import os
import random

def delete_large_percentage_of_files():
    # Prompt for the path to the directory
    dir_path = input("Enter the directory path: ").strip()

    # Verify the directory exists
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
    total_files = len(all_files)

    # Calculate number of files to delete
    num_files_to_delete = int(total_files * (percent / 100))

    # Preview the number of files to delete
    print(f"Total files: {total_files}")
    print(f"Files to delete ({percent}%): {num_files_to_delete}")

    # Confirm before deletion
    confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Aborted.")
        return

    # Select random files to delete
    files_to_delete = random.sample(all_files, num_files_to_delete)
    
    # Delete each selected file in batches
    deleted_count = 0
    batch_size = 10000  # Adjust based on your system capacity
    
    for i in range(0, len(files_to_delete), batch_size):
        batch = files_to_delete[i:i + batch_size]
        for file_name in batch:
            file_path = os.path.join(dir_path, file_name)
            try:
                os.remove(file_path)
                deleted_count += 1
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    
    print(f"Deleted {deleted_count} out of {total_files} files.")

# Run the function
delete_large_percentage_of_files()
