import cv2
import warnings
import numpy as np
import pandas as pd
import mediapipe as mp
import os
import time

warnings.filterwarnings('ignore')

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose

# Specifications
landmark_color = (0, 255, 0)  # Green for landmarks
connection_color = (80, 44, 121)  # Blue for connections
face_drawing_spec = mp_drawing.DrawingSpec(color=(255, 112, 0), thickness=1)
hand_drawing_spec = mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2)


class SignDataCollector:
    def __init__(self):
        self.hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
        self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, refine_landmarks=True, min_tracking_confidence=0.5, max_num_faces=1)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.cap = cv2.VideoCapture(0)
        self.data = []
        self.output_folder = 'collect_csv'

        # Ensure the collect_csv folder exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def collect_data(self, label):
        collecting = False
        paused = False
        start_time = None
        elapsed_time = 0  # Track elapsed time for the 7-second timer

        while True:
            ret, image = self.cap.read()
            if not ret:
                print("Ignoring empty camera frame.")
                continue

            # Flip the image for a mirror effect
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # Process with MediaPipe Hands, Face Mesh, and Pose
            hands_results = self.hands.process(image)
            face_results = self.face_mesh.process(image)
            pose_results = self.pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw landmarks
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=face_drawing_spec,
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                    )
            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=landmark_color, thickness=3),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                )
            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    if collecting and not paused:
                        self.data.append(self.extract_landmarks(hand_landmarks))
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=hand_drawing_spec,
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                    )

            # Display the video frame
            image = cv2.resize(image, (700, 600))
            cv2.imshow('Sign Data Collector', image)

            # Check for key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c') and not collecting:
                time.sleep(2)  # Short delay before starting collection
                collecting = True
                start_time = time.time()
            elif key == ord('q'):  # Allow early exit with 'q'
                print("Exiting without saving.")
                break
            elif key == ord('h'):  # Pause timer when 'h' is held
                paused = True
            else:  # Resume timer when 'h' is released
                if paused:
                    paused = False
                    start_time = time.time() - elapsed_time  # Adjust start time to preserve elapsed time

            # Update elapsed time if collecting and not paused
            if collecting and not paused:
                elapsed_time = time.time() - start_time

            # Stop collecting data after 10 seconds
            if collecting and elapsed_time >= 10:
                break

        self.save_data(label)
        self.cap.release()
        cv2.destroyAllWindows()

    def extract_landmarks(self, hand_landmarks):
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.append(landmark.x)
            landmarks.append(landmark.y)
            landmarks.append(landmark.z)
        return landmarks

    def save_data(self, label):
        if self.data:
            output_file = os.path.join(self.output_folder, f'data_{label}.csv')
            df = pd.DataFrame(self.data)
            df['label'] = label
            df.to_csv(output_file, mode='a', header=False, index=False)
            print(f"Data saved for: {label} in {output_file}")
        else:
            print("No data collected to save.")


if __name__ == '__main__':
    collector = SignDataCollector()
    label = input("Enter the label for the sign: ")
    collector.collect_data(label)
