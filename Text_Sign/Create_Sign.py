import cv2
import warnings
import numpy as np
import pandas as pd
import mediapipe as mp
import time
import os

warnings.filterwarnings('ignore')

# MediaPipe
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
        self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, refine_landmarks=True,
                                               min_tracking_confidence=0.5, max_num_faces=1)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.cap = cv2.VideoCapture(0)
        self.data = []

    def collect_data(self, label):
        print(f"Collecting data for: {label}")
        frame_count = 0

        # Create label folder
        label_folder = f'frames/{label}'
        if not os.path.exists(label_folder):
            os.makedirs(label_folder)

        while True:
            ret, image = self.cap.read()
            if not ret:
                print("Ignoring empty camera frame.")
                continue

            # Flip the image horizontally and convert to RGB
            image_rgb = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            hands_results = self.hands.process(image_rgb)
            face_results = self.face_mesh.process(image_rgb)
            pose_results = self.pose.process(image_rgb)

            # Create a white background (blank canvas)
            height, width, _ = image.shape
            white_background = np.ones((height, width, 3), dtype=np.uint8) * 255  # Create a white image

            # Draw landmarks on the white background
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=white_background,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=face_drawing_spec,
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                    )

            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    white_background, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=landmark_color, thickness=3),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                )

            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    self.data.append(self.extract_landmarks(hand_landmarks))
                    mp_drawing.draw_landmarks(
                        white_background, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=hand_drawing_spec,
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                    )

            # Resize for better display and show the image
            white_background = cv2.resize(white_background, (700, 600))
            cv2.imshow('Collecting Data', white_background)

            # Capture frames when 'c' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                print("Starting frame collection. Please wait 4 seconds...")
                time.sleep(4)  # Wait for 4 seconds before starting to collect frames
                frame_count = 0

                # Collect 20 frames
                while frame_count < 20:
                    ret, image = self.cap.read()
                    if not ret:
                        print("Ignoring empty camera frame.")
                        continue

                    # Flip the image horizontally and convert to RGB
                    image_rgb = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                    hands_results = self.hands.process(image_rgb)
                    face_results = self.face_mesh.process(image_rgb)
                    pose_results = self.pose.process(image_rgb)

                    # Create a white background (blank canvas)
                    height, width, _ = image.shape
                    white_background = np.ones((height, width, 3), dtype=np.uint8) * 255  # Create a white image

                    # Draw landmarks on the white background
                    if face_results.multi_face_landmarks:
                        for face_landmarks in face_results.multi_face_landmarks:
                            mp_drawing.draw_landmarks(
                                image=white_background,
                                landmark_list=face_landmarks,
                                connections=mp_face_mesh.FACEMESH_CONTOURS,
                                landmark_drawing_spec=face_drawing_spec,
                                connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                            )

                    if pose_results.pose_landmarks:
                        mp_drawing.draw_landmarks(
                            white_background, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                            landmark_drawing_spec=mp_drawing.DrawingSpec(color=landmark_color, thickness=3),
                            connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                        )

                    if hands_results.multi_hand_landmarks:
                        for hand_landmarks in hands_results.multi_hand_landmarks:
                            self.data.append(self.extract_landmarks(hand_landmarks))
                            mp_drawing.draw_landmarks(
                                white_background, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                landmark_drawing_spec=hand_drawing_spec,
                                connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
                            )

                    # Save the frame after drawing landmarks
                    frame_filename = f'{label_folder}/frame_{frame_count}.jpg'
                    cv2.imwrite(frame_filename, white_background)
                    print(f"Frame {frame_count + 1} saved as: {frame_filename}")
                    frame_count += 1

                # After collecting 20 frames, break out of the loop
                print("20 frames collected.")
                break

            # Quit when 'q' is pressed
            if key == ord('q'):
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
        # Create folder for CSV files if not exists
        csv_folder = 'frames_csv'
        if not os.path.exists(csv_folder):
            os.makedirs(csv_folder)

        # Save data to CSV
        df = pd.DataFrame(self.data)
        df['label'] = label
        csv_path = os.path.join(csv_folder, f'data_{label}.csv')
        df.to_csv(csv_path, mode='a', header=False, index=False)
        print(f"Data saved for: {label} in {csv_path}")


if __name__ == '__main__':
    collector = SignDataCollector()
    label = input("Enter the label for Collect: ")
    collector.collect_data(label)



# import cv2
# import warnings
# import numpy as np
# import pandas as pd
# import mediapipe as mp
# import time
# import os
#
# warnings.filterwarnings('ignore')
#
# # MediaPipe
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
# mp_face_mesh = mp.solutions.face_mesh
# mp_pose = mp.solutions.pose
#
# # specifications
# landmark_color = (0, 0, 255)  #
# connection_color = (0, 255, 0)
# hand_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
# face_drawing_spec = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
#
# class SignDataCollector:
#     def __init__(self):
#         self.hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
#         self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, refine_landmarks=True, min_tracking_confidence=0.5, max_num_faces=1)
#         self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
#         self.cap = cv2.VideoCapture(0)
#         self.data = []
#
#     def collect_data(self, label):
#         print(f"Collecting data for: {label}")
#         start_time = time.time()
#         frame_count = 0
#
#         # Create label
#         label_folder = f'frames/{label}'
#         if not os.path.exists(label_folder):
#             os.makedirs(label_folder)
#
#         while True:
#             ret, image = self.cap.read()
#             if not ret:
#                 print("Ignoring empty camera frame.")
#                 continue
#
#             image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
#             hands_results = self.hands.process(image)
#             face_results = self.face_mesh.process(image)
#             pose_results = self.pose.process(image)
#
#             # Convert the image color
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#
#             # Draw landmarks
#             if hands_results.multi_hand_landmarks:
#                 for hand_landmarks in hands_results.multi_hand_landmarks:
#                     self.data.append(self.extract_landmarks(hand_landmarks))
#                     mp_drawing.draw_landmarks(
#                         image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
#                         landmark_drawing_spec=hand_drawing_spec,
#                         connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
#                     )
#
#             # Draw landmarks
#             if face_results.multi_face_landmarks:
#                 for face_landmarks in face_results.multi_face_landmarks:
#                     mp_drawing.draw_landmarks(
#                         image=image,
#                         landmark_list=face_landmarks,
#                         connections=mp_face_mesh.FACEMESH_CONTOURS,
#                         landmark_drawing_spec=face_drawing_spec,
#                         connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
#                     )
#
#             # Draw pose landmarks
#             if pose_results.pose_landmarks:
#                 mp_drawing.draw_landmarks(
#                     image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                     landmark_drawing_spec=mp_drawing.DrawingSpec(color=landmark_color, thickness=3),
#                     connection_drawing_spec=mp_drawing.DrawingSpec(color=connection_color, thickness=2)
#                 )
#
#             elapsed_time = time.time() - start_time
#             if int(elapsed_time) % 2 == 0:
#                 cv2.putText(image, ' ', (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#             else:
#                 cv2.putText(image, ' ', (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
#
#
#             image = cv2.resize(image, (700, 600))
#             cv2.imshow('Collecting Data', image)
#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('c'):
#                 frame_filename = f'{label_folder}/frame_{frame_count}.jpg'
#                 cv2.imwrite(frame_filename, image)
#                 print(f"Frame saved as: {frame_filename}")
#                 frame_count += 1
#
#
#             if key == ord('q'):
#                 break
#
#         self.save_data(label)
#         self.cap.release()
#         cv2.destroyAllWindows()
#
#     def extract_landmarks(self, hand_landmarks):
#         landmarks = []
#         for landmark in hand_landmarks.landmark:
#             landmarks.append(landmark.x)
#             landmarks.append(landmark.y)
#             landmarks.append(landmark.z)
#         return landmarks
#
#     def save_data(self, label):
#         df = pd.DataFrame(self.data)
#         df['label'] = label
#         df.to_csv(f'data_{label}.csv', mode='a', header=False, index=False)
#         print(f"Data saved for: {label}")
#
# if __name__ == '__main__':
#     collector = SignDataCollector()
#     label = input("Enter the label for  Collect: ")
#     collector.collect_data(label)
