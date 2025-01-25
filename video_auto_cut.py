import os
import subprocess
import json

def create_output_folder(video_path):
    folder_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = os.path.join(os.path.dirname(video_path), folder_name)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def detect_black_frames(video_path):
    # Normalize Windows paths
    escaped_path = video_path.replace("\\", "/")
    
    ffmpeg_command = [
        "ffmpeg", "-i", escaped_path,
        "-vf", "blackdetect=d=0.5:pic_th=0.98:pix_th=0.1",
        "-an", "-f", "null", "-"
    ]
    
    result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    black_frames = []

    # Parse ffmpeg's stderr for black frame details
    for line in result.stderr.splitlines():
        if "black_start" in line:
            parts = line.split()
            black_start = float([x.split(':')[1] for x in parts if x.startswith("black_start")][0])
            black_end = float([x.split(':')[1] for x in parts if x.startswith("black_end")][0])
            black_frames.append((black_start, black_end))
    
    return black_frames


def split_video(video_path, black_frames, output_folder):
    black_frames = sorted(set(black_frames))
    timestamps = [0] + [end for _, end in black_frames] + [None]  # Add start and end timestamps

    clips = []
    for i in range(len(timestamps) - 1):
        start = timestamps[i]
        end = timestamps[i + 1]

        clip_path = os.path.join(output_folder, f"clip_{i + 1}.mp4")
        
        if end is None:
            ffmpeg_command = [
                "ffmpeg", "-i", video_path, "-ss", str(start),
                "-c", "copy", clip_path
            ]
        else:
            ffmpeg_command = [
                "ffmpeg", "-i", video_path, "-ss", str(start), "-to", str(end),
                "-c", "copy", clip_path
            ]
        
        print(f"Running command: {' '.join(ffmpeg_command)}")  # Debug log
        result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"Error splitting clip {i + 1}: {result.stderr}")
        else:
            clips.append(clip_path)
    
    return clips


def main(video_path):
    if not os.path.isfile(video_path):
        print("Invalid video file path.")
        return

    # Create output folder
    output_folder = create_output_folder(video_path)
    print(f"Output folder: {output_folder}")

    # Detect black frames
    print("Detecting black frames...")
    black_frames = detect_black_frames(video_path)

    if not black_frames:
        print("No black frames detected. Exiting.")
        return

    print(f"Black frames detected at: {black_frames}")

    # Split video
    print("Splitting video into clips...")
    clips = split_video(video_path, black_frames, output_folder)

    print(f"Video successfully split into {len(clips)} clips.")
    print("Clips saved to:")
    for clip in clips:
        print(clip)

if __name__ == "__main__":
    video_path_input = input("Enter the path to the video file: ").strip()
    # video_path_input = video_path_input.replace("\\", "/")  # Normalize Windows paths
    main(video_path_input)
