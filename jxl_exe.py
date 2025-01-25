import subprocess
import os


def compress_with_exe(input_file, output_file, quality=50):
    # Path to the executable
    exe_path = os.path.join(os.getcwd(), 'jxl-x64-windows-static', 'cjxl.exe')
    num_threads = os.cpu_count()

    # Run the executable with input, output, and quality parameter
    try:
        result = subprocess.run(
            [exe_path, 
            input_file, 
            output_file, 
            '--quality', str(quality),
            '--effort', str(5),
            '--num_threads', str(num_threads)
            ],  # Add the quality parameter here
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Print the output of the command
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running cjxl.exe: {e.stderr.decode()}")
    except FileNotFoundError:
        print("cjxl.exe not found. Please check the path and try again.")


# compress_with_exe('111.png', '111.jxl', 50)
        

input_folder = input("Input folder: ")
output_folder = input_folder + '_compressed'
os.makedirs(output_folder, exist_ok=True)

def is_image(filename):
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

def find_images(folder):
    return [f for f in os.listdir(folder) if is_image(f)]


image_list = find_images(input_folder)
stats_current = 0
stats_max = len(image_list)

for image in image_list:
    stats_current += 1
    print(f"{image} --- {stats_current}/{stats_max}")
    compress_with_exe(os.path.join(input_folder, image), os.path.join(output_folder, image))