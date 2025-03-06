import cv2
import os

# Path to the directory containing videos
video_dir = r"C:\Users\MSI\OneDrive\Desktop\FINAL V10 Submitted\MobileAPP_Kivy\Asset\videos\words"
# Path to save extracted frames
output_dir = "words"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate through all video files in the directory
for video_file in os.listdir(video_dir):
    # Check if the file is a video file
    if video_file.endswith(".mp4"):
        video_path = os.path.join(video_dir, video_file)

        # Create a folder for the video's frames
        label = os.path.splitext(video_file)[0]  # Use the video name as the label
        frame_dir = os.path.join(output_dir, label)
        os.makedirs(frame_dir, exist_ok=True)

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = total_frames // 20  # Extract 20 frames evenly spaced

        count = 0
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Save the frame if it matches the frame rate
            if count % frame_rate == 0 and frame_count < 20:
                frame_name = f"frame_{frame_count + 1}.jpg"
                frame_path = os.path.join(frame_dir, frame_name)
                cv2.imwrite(frame_path, frame)
                frame_count += 1

            count += 1

        cap.release()
        print(f"Extracted {frame_count} frames from {video_file} into {frame_dir}")

print("Frame extraction complete!")
