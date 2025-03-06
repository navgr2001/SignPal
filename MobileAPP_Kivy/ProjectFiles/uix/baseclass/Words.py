# from main_imports import MDScreen
# from ProjectFiles.applibs import utils
# from kivy.clock import Clock
# from kivy.resources import resource_find
# import cv2
# import os
#
# utils.load_kv("Words.kv")
#
#
# class Words_Screen(MDScreen):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.all_frames = []  # To hold all frames from all labels
#         self.frame_index = 0  # Index to track the current frame
#         self.animation_event = None  # To store scheduled event
#
#     def show_animation(self, labels):
#         # Collect frames from all specified labels
#         self.all_frames = []
#
#         for label in labels:
#             # Directory where frames are stored
#             # label_folder = os.path.join("C:/Users/MSI/OneDrive/Desktop/FINAL V10 Submitted/MobileAPP_Kivy/learn_sign/words", label)
#             label_folder = resource_find(f"learn_sign/words/{label}")
#
#             # Check if the folder for the label exists
#             if not os.path.exists(label_folder):
#                 print(f"No data found for label: {label}")
#                 continue
#
#             # Get all image files in the folder
#             frame_files = [os.path.join(label_folder, f) for f in os.listdir(label_folder) if f.endswith('.jpg')]
#             frame_files.sort()  # Sort files if needed (e.g., frame_0.jpg, frame_1.jpg, ...)
#             self.all_frames.extend(frame_files)  # Add to the main list
#
#         if not self.all_frames:
#             print("No frames found for the provided labels.")
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
#         if self.frame_index < len(self.all_frames):
#             # Set the image source to the current frame
#             self.ids.sign_image.source = self.all_frames[self.frame_index]
#             self.frame_index += 1
#         else:
#             # Stop the animation once all frames have been shown
#             Clock.unschedule(self.animation_event)
#             print("Animation complete!")
#
#     def on_button_click(self):
#         # Get text input value and split into words
#         user_input = self.ids.text_input.text.strip()
#         if user_input:
#             labels = user_input.split()  # Split input into words
#             self.show_animation(labels)  # Call the animation function with multiple labels
#         else:
#             print("Please enter labels for the animation")
from main_imports import MDScreen
from ProjectFiles.applibs import utils
from kivy.lang import Builder
from kivy.uix.video import Video
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
import warnings

utils.load_kv("Words.kv")


class Words_Screen(MDScreen):
    def on_enter(self):
        # Ensure that the layout has been fully loaded before accessing children
        grid = self.ids.button_grid  # Accessing button_grid using the id defined in words.kv
        if grid:
            # Example: Access the first button (Monday button)
            first_button = grid.children[0]
            print(f"First button text: {first_button.text}")  # Just an example action

    def filter_buttons(self, search_text):
        grid = self.ids.button_grid  # Accessing button_grid
        if grid:
            # Filter the buttons based on the search text
            for button in grid.children:
                button_text = button.text.lower()
                if search_text.lower() in button_text:
                    button.disabled = False  # Show the button if it matches
                else:
                    button.disabled = True  # Hide the button if it doesn't match

    def open_frames_popup(self, label):
        # Sample method to open popup when a button is pressed
        content = BoxLayout(orientation='vertical')
        video = Video(source=f'{label}.mp4', state='play')
        content.add_widget(video)

        popup = Popup(title=label, content=content, size_hint=(0.8, 0.8))
        popup.open()

class MyApp(MDApp):
    def build(self):
        return Builder.load_file("Words.kv")  # Load the KV file for the screen

    def on_start(self):
        # Example to demonstrate the filter functionality
        screen = self.root.ids.words_screen
        screen.filter_buttons("monday")  # You can test by typing "monday" in the search bar

# Run the app
if __name__ == '__main__':
    MyApp().run()