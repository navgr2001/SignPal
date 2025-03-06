from main_imports import MDScreen
from ProjectFiles.applibs import utils
from kivy.clock import Clock
import cv2
import os

utils.load_kv("Text_to_Sign.kv")


class Text_to_Sign_Screen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_frames = []  # To hold all frames from all labels
        self.frame_index = 0  # Index to track the current frame
        self.animation_event = None  # To store scheduled event

    def show_animation(self, labels):
        # Collect frames from all specified labels
        self.all_frames = []

        for label in labels:
            # Directory where frames are stored
            label_folder = f'../Text_Sign/frames/{label}'

            # Check if the folder for the label exists
            if not os.path.exists(label_folder):
                print(f"No data found for label: {label}")
                continue

            # Get all image files in the folder
            frame_files = [os.path.join(label_folder, f) for f in os.listdir(label_folder) if f.endswith('.jpg')]
            frame_files.sort()  # Sort files if needed (e.g., frame_0.jpg, frame_1.jpg, ...)
            self.all_frames.extend(frame_files)  # Add to the main list

        if not self.all_frames:
            print("No frames found for the provided labels.")
            return

        # Initialize the frame index to start from the first frame
        self.frame_index = 0

        # Start the animation by scheduling the update function every 100ms
        self.animation_event = Clock.schedule_interval(self.update_frame, 0.1)

    def update_frame(self, dt):
        # Check if we have more frames to display
        if self.frame_index < len(self.all_frames):
            # Set the image source to the current frame
            self.ids.sign_image.source = self.all_frames[self.frame_index]
            self.frame_index += 1
        else:
            # Stop the animation once all frames have been shown
            Clock.unschedule(self.animation_event)
            print("Animation complete!")

    def on_button_click(self):
        # Get text input value and split into words
        user_input = self.ids.text_input.text.strip()
        if user_input:
            labels = user_input.split()  # Split input into words
            self.show_animation(labels)  # Call the animation function with multiple labels
        else:
            print("Please enter labels for the animation")


# from main_imports import MDScreen
# from ProjectFiles.applibs import utils
# from kivy.clock import Clock
# import cv2
# import os
#
# utils.load_kv("Text_to_Sign.kv")
#
# class Text_to_Sign_Screen(MDScreen):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.frame_files = []  # To hold the frames list
#         self.frame_index = 0  # Index to track the current frame
#         self.animation_event = None  # To store scheduled event
#
#     def show_animation(self, label):
#         # Directory where frames are stored
#         label_folder = f'../Text_Sign/frames/{label}'
#
#         # Check if the folder for the label exists
#         if not os.path.exists(label_folder):
#             print(f"No data found for label: {label}")
#             return
#
#         # Get all image files in the folder
#         self.frame_files = [f for f in os.listdir(label_folder) if f.endswith('.jpg')]
#         self.frame_files.sort()  # Sort files if needed (e.g., frame_0.jpg, frame_1.jpg, ...)
#
#         if not self.frame_files:
#             print(f"No frames found for label: {label}")
#             return
#
#         # Initialize the frame index to start from the first frame
#         self.frame_index = 0
#
#         # Start the animation by scheduling the update function every 100ms
#         self.animation_event = Clock.schedule_interval(self.update_frame, 0.1)
#
#     def update_frame(self, dt):
#         # Check if we have more frames to display
#         if self.frame_index < len(self.frame_files):
#             frame_path = os.path.join(f'../Text_Sign/frames/{self.ids.text_input.text}', self.frame_files[self.frame_index])
#             # Set the image source to the current frame
#             self.ids.sign_image.source = frame_path
#             self.frame_index += 1
#         else:
#             # Stop the animation once all frames have been shown
#             Clock.unschedule(self.animation_event)
#             print("Animation complete!")
#
#     def on_button_click(self):
#         label = self.ids.text_input.text  # Get text input value
#         if label:
#             self.show_animation(label)  # Call the animation function
#         else:
#             print("Please enter a label for the animation")
