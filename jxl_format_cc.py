from imagecodecs import JPEGXL, jpegxl_encode, imread
import os
import concurrent.futures
import sys

support = JPEGXL.available
if not support:
    raise RuntimeError("JXL is not available")

target_folder = input("Target folder: ")

if not os.path.isdir(target_folder):
    print("Directory does not exist.")
    exit(1)

compress_folder = target_folder + '_compressed'
os.makedirs(compress_folder, exist_ok=True)

def is_image(filename):
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

def find_images(folder):
    return [f for f in os.listdir(folder) if is_image(f)]

def process_file(filename):
    img_path = os.path.join(target_folder, filename)
    compressed_path = os.path.join(compress_folder, f"{filename}.jxl")
    
    img_arr = imread(img_path)
    jxl_arr = jpegxl_encode(img_arr, level=50, effort=5, numthreads=os.cpu_count())
    
    with open(compressed_path, "wb") as f:
        f.write(jxl_arr)

def main():
    image_list = find_images(target_folder)
    stats_max = len(image_list)

    if stats_max == 0:
        print("No images found to process.")
        return

    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        # Use map to apply process_file function to each filename
        futures = {executor.submit(process_file, image): image for image in image_list}
        
        for future in concurrent.futures.as_completed(futures):
            filename = futures[future]
            try:
                future.result()  # To catch any exceptions raised during processing
                stats_current = image_list.index(filename) + 1
                print(f"{stats_current}/{stats_max} processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
