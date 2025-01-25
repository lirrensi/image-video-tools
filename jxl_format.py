from imagecodecs import JPEGXL, jpegxl_encode, avif_encode, imread
import os
import platform
from datetime import datetime, timezone
import shutil
import pytz
import ctypes
import numpy as np


def set_file_times(filepath: str, create_time: datetime, modify_time: datetime):
    # Ensure datetime objects are naive and in UTC
    if create_time.tzinfo is not None:
        create_time = create_time.astimezone(timezone.utc).replace(tzinfo=None)
    if modify_time.tzinfo is not None:
        modify_time = modify_time.astimezone(timezone.utc).replace(tzinfo=None)

    # Convert datetime objects to FILETIME format
    def datetime_to_filetime(dt: datetime) -> (int, int):
        # FILETIME structure: 64-bit integer (high and low 32-bit)
        windows_epoch = datetime(1601, 1, 1)
        delta = dt - windows_epoch
        # Convert to 100-nanosecond intervals
        total_100ns_intervals = int(delta.total_seconds() * 10**7)
        low = total_100ns_intervals & 0xFFFFFFFF
        high = (total_100ns_intervals >> 32) & 0xFFFFFFFF
        return low, high

    # Convert datetimes to FILETIME format
    create_time_low, create_time_high = datetime_to_filetime(create_time)
    modify_time_low, modify_time_high = datetime_to_filetime(modify_time)

    # Define FILETIME structure
    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", ctypes.c_uint32),
                    ("dwHighDateTime", ctypes.c_uint32)]

    # Prepare FILETIME structures
    create_time_filetime = FILETIME(dwLowDateTime=create_time_low, dwHighDateTime=create_time_high)
    modify_time_filetime = FILETIME(dwLowDateTime=modify_time_low, dwHighDateTime=modify_time_high)

    # Load Windows API functions
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.CreateFileW(filepath, 0x40000000, 0, None, 3, 0, None)  # GENERIC_WRITE

    if handle == -1:
        raise FileNotFoundError("The file could not be opened")

    # Set file times
    success = kernel32.SetFileTime(handle, ctypes.byref(create_time_filetime), None, ctypes.byref(modify_time_filetime))
    
    if not success:
        raise OSError("Failed to set file times")

    # Close the handle
    kernel32.CloseHandle(handle)



def is_image(filename):
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

def find_images(folder):
    return [f for f in os.listdir(folder) if is_image(f)]

# def get_compressed_image_data(file_path):
#     img_arr = imread(file_path)
#     compressed_arr = jpegxl_encode(img_arr, level=50, effort=5, numthreads=os.cpu_count())
#     # compressed_arr = avif_encode(img_arr, level=50, speed=7, numthreads=os.cpu_count())
    
#     return compressed_arr

def smart_convert_to_24bit(img_arr):
    # Check if we need to convert (if it's higher than 8-bit)
    if img_arr.dtype in (np.uint16, np.float32, np.float64):
        # Normalize to 0-1 range from 16-bit
        img_float = img_arr.astype(np.float32) / np.iinfo(np.uint16).max
        
        # If image has alpha channel (4 channels), keep only RGB
        if img_float.shape[-1] == 4:
            img_float = img_float[..., :3]
        
        # Convert to 8-bit (0-255 range)
        return (img_float * 255).clip(0, 255).astype(np.uint8)
    
    # If already 8-bit, just handle alpha if present
    if img_arr.dtype == np.uint8 and img_arr.shape[-1] == 4:
        return img_arr[..., :3]
    
    # If already 8-bit RGB, return as-is
    return img_arr

def get_compressed_image_data(file_path):
    # Read the image
    img_arr = imread(file_path)
    
    img_arr = smart_convert_to_24bit(img_arr)
        # Standard 24-bit compression
    compressed_arr = jpegxl_encode(
        img_arr,
        level=50,
        effort=5,
        numthreads=os.cpu_count()
    )
    
    return compressed_arr

def generate_new_file_name(original_file_path, gmt_offset=0):
# function to generate a new file name based on the pattern
    # Get the file's modification time
    creation_time = os.path.getmtime(original_file_path)

    # Convert the creation time to a datetime object in UTC
    creation_datetime_utc = datetime.fromtimestamp(creation_time, tz=pytz.utc)
    
    # Adjust the datetime object to the specified GMT offset
    gmt_tz = pytz.FixedOffset(gmt_offset * 60)  # Convert hours to minutes
    creation_datetime_local = creation_datetime_utc.astimezone(gmt_tz)
    
    print('creation_datetime_local', creation_datetime_local)

    # Format the creation datetime as required
    creation_date_str = creation_datetime_local.strftime('%Y_%m_%d__%H_%M_%S')


    # Get the original filename without the extension
    original_filename_no_ext = os.path.splitext(os.path.basename(original_file_path))[0]

    # also limit max symbols
    original_filename_no_ext = original_filename_no_ext[0:48]

    # Generate the new file name based on the pattern
    new_file_name = f"scr__{creation_date_str}__{original_filename_no_ext}.jxl"

    return new_file_name, creation_datetime_local

support = JPEGXL.available
if not support:
    raise RuntimeError("JXL is not available")

target_folder = input("Target folder: ")
utc_correction = int(input("UTC correction (default 0): ") or 0)

if not os.path.isdir(target_folder):
    print("Directory does not exist.")
    exit(1)

compress_folder = target_folder + '_compressed'
os.makedirs(compress_folder, exist_ok=True)


image_list = find_images(target_folder)
stats_current = 0
stats_max = len(image_list)

# Iterate through each image in the list
for image in image_list:
    stats_current += 1
    print(f"{stats_current}/{stats_max} --- {image}")

    original_file_path = os.path.join(target_folder, image)

    # Generate the new file name and path for the compressed image
    new_file_name, creation_datetime = generate_new_file_name(original_file_path, gmt_offset=utc_correction)
    new_file_name = new_file_name.strip().replace(' ', '_')

    new_file_path = os.path.join(compress_folder, new_file_name)

    # check if file exists
    if os.path.exists(new_file_path):
        print(f"File {new_file_name} already exists. Skipping.")
        continue

    # Compress the image and get the compressed data
    image_data = get_compressed_image_data(original_file_path)

    # Write the compressed image data to a new file
    with open(new_file_path, 'wb') as f:
        f.write(image_data)

    # Copy the original file's metadata to the new compressed file
    # shutil.copystat(original_file_path, new_file_path)
    # set created and modified specifically with 'creation_datetime
    set_file_times(new_file_path, creation_datetime, creation_datetime)

print("Compression complete. Compressed files are saved with original metadata.")