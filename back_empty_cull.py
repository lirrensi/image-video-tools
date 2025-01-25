import os
from PIL import Image
import glob
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import random
from typing import List, Tuple

def get_random_pixel_coordinates(width: int, height: int, sample_size: int = 1000) -> List[Tuple[int, int]]:
    """Generate random pixel coordinates for checking."""
    total_pixels = width * height
    sample_size = min(sample_size, total_pixels)
    coordinates = [(random.randint(0, width-1), random.randint(0, height-1)) 
                  for _ in range(sample_size)]
    return coordinates

def is_image_all_black(image_path: str) -> Tuple[str, bool]:
    """Check if image is all black using random sampling. Returns tuple of (path, result)."""
    try:
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            pixels = img.load()
            width, height = img.size
            
            # Random sampling first
            coordinates = get_random_pixel_coordinates(width, height)
            for x, y in coordinates:
                r, g, b = pixels[x, y]
                if r != 0 or g != 0 or b != 0:
                    return (image_path, False)
            
            # Full check only if random sample is all black
            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y]
                    if r != 0 or g != 0 or b != 0:
                        return (image_path, False)
            return (image_path, True)
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return (image_path, False)

def process_chunk(image_paths: List[str]) -> List[Tuple[str, bool]]:
    """Process a chunk of images and return results."""
    return [is_image_all_black(path) for path in image_paths]

def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split a list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def process_images(folder_path: str) -> List[str]:
    """Find all black images in the given folder using process pool."""
    # Get all images
    image_types = ('*.jpg', '*.jpeg', '*.png', '*.gif')
    images = []
    for ext in image_types:
        images.extend(glob.glob(os.path.join(folder_path, ext)))
    
    if not images:
        return []
    
    # Calculate optimal number of processes and chunk size
    num_processes = multiprocessing.cpu_count()
    chunk_size = max(1, len(images) // (num_processes * 2))  # Ensure enough chunks for all processes
    image_chunks = chunk_list(images, chunk_size)
    
    black_images = []
    processed_count = 0
    total_images = len(images)
    
    # Process images in parallel using ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # Submit all chunks for processing
        future_to_chunk = {executor.submit(process_chunk, chunk): chunk 
                          for chunk in image_chunks}
        
        # Process results as they complete
        for future in future_to_chunk:
            try:
                results = future.result()
                for image_path, is_black in results:
                    processed_count += 1
                    if is_black:
                        black_images.append(image_path)
                    print(f"Progress: {processed_count}/{total_images} - Checked: {os.path.basename(image_path)}")
            except Exception as e:
                print(f"Error processing chunk: {str(e)}")
    
    return black_images

def main():
    # Get folder path from user
    folder_path = input("Enter folder path: ").strip()
    
    # Validate folder
    if not os.path.isdir(folder_path):
        print("Error: Invalid folder path")
        return
    
    print(f"\nAnalyzing images using {multiprocessing.cpu_count()} processes...")
    black_images = process_images(folder_path)
    
    # If no images to delete
    if not black_images:
        print("\nNo empty (black) images found.")
        return
    
    # Show images to be deleted
    print(f"\nThe following {len(black_images)} images are completely black and will be deleted:")
    for image_path in black_images:
        print(f"- {os.path.basename(image_path)}")
    
    # Ask for confirmation
    confirm = input("\nDo you want to delete these images? (y/n): ").strip().lower()
    
    if confirm == 'y':
        print("\nDeleting images...")
        for image_path in black_images:
            try:
                os.remove(image_path)
                print(f"Deleted: {os.path.basename(image_path)}")
            except Exception as e:
                print(f"Failed to delete {os.path.basename(image_path)}: {str(e)}")
        print("\nDeletion complete.")
    else:
        print("\nOperation cancelled.")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed()
    # Required for Windows systems
    multiprocessing.freeze_support()
    main()