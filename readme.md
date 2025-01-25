# Repository README

## Overview

This repository contains a collection of utilities and scripts focused on image and video processing tasks. These include tools for file sorting, video editing, image format conversion, metadata manipulation, and other file management operations. Below is a detailed description of the key components and their functionalities.

---

## File Descriptions

### 1. `ym+sort/`

-   **Purpose**: Sort files by year and month based on their metadata (e.g., EXIF date for images).
-   **Functionality**:
    -   Organizes files into a directory structure of `Year/Month/`.
    -   Supports custom file type filtering (e.g., images, videos).
-   **Usage**:
    1. Place files within a designated folder.
    2. Run the script to auto-sort files into subdirectories based on timestamps.

---

### 2. `video_auto_cut/`

-   **Purpose**: Automatically trim videos based on predefined criteria.
-   **Functionality**:
    -   Cuts specific segments of video using start and end time markers.
    -   Supports batch processing of multiple videos.
-   **Features**:
    -   Configuration for time markers per file.
    -   Output videos saved in the same directory as the originals or in a custom directory.
-   **Usage**:
    1. Specify time markers in a configuration file or as command-line inputs.
    2. Run the script to process videos.

---

### 3. `jxl_format/`

-   **Purpose**: Convert image files to the JPEG XL (JXL) format.
-   **Functionality**:
    -   Accepts common image formats as input (JPEG, PNG, etc.).
    -   Compresses and converts to the high-efficiency JPEG XL format.
-   **Features**:
    -   Configurable compression quality.
    -   Batch processing of multiple images.
-   **Usage**:
    1. Provide a list or folder of input images.
    2. Run the script to convert images, which will be saved in the same or a specified directory.

---

### 4. `back_empty_cull/`

-   **Purpose**: Identify and remove background-empty images.
-   **Functionality**:
    -   Detects images with minimal content (e.g., blank or predominantly one-color backgrounds) using pixel intensity thresholds.
    -   Removes or moves "empty" images to a specified folder.
-   **Usage**:
    1. Provide a folder of images to scan.
    2. Run the script to process and clean up the folder.

---

### 5. `img_rename_only_exif/`

-   **Purpose**: Rename image files based on their EXIF metadata.
-   **Functionality**:
    -   Uses EXIF data (e.g., creation date) to generate file names.
    -   Example: Renames `IMG_1234.jpg` to `2023-01-01_12-00-00.jpg`.
-   **Features**:
    -   Supports customizable naming conventions.
    -   Skips files with missing EXIF data or allows fallback handling.
-   **Usage**:
    1. Provide a folder of images.
    2. Run the script to rename files automatically.

---

### 6. `percentage_cull/`

-   **Purpose**: Remove a specified percentage of files based on a random selection.
-   **Functionality**:
    -   Randomly selects a percentage of files within a folder for removal or relocation.
    -   Useful for downscaling datasets or cleaning up large collections.
-   **Features**:
    -   Configurable percentage value.
    -   Dry-run mode to preview selected files before deletion.
-   **Usage**:
    1. Specify the folder and percentage (e.g., 20%).
    2. Run the script to cull files.

---

## Getting Started

1. **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2. **Setup and Dependencies**
   Make sure you have Python and the required libraries installed. Use the following command to install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run Individual Modules**
   Execute specific scripts based on the functionality you need. Each script has a `--help` flag for guidance on usage.

---

## Author and Contributions

-   **Author**: [Your Name or Organization]  
    Contributions and feedback are welcome. Please open issues or submit pull requests for any suggestions or improvements.

---

## License

This repository is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the included code.
