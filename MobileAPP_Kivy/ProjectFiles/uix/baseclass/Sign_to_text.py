from main_imports import MDScreen
from ProjectFiles.applibs import utils
import warnings
from kivy.graphics.texture import Texture
from kivy.clock import Clock
import cv2
import numpy as np
import mediapipe as mp
import joblib
import tensorflow as tf

warnings.filterwarnings('ignore')
utils.load_kv("Sign_to_text.kv")

# MediaPipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose


class Sign_to_text_Screen(MDScreen):
    def __init__(self, **kwargs):
        super(Sign_to_text_Screen, self).__init__(**kwargs)
        self.hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
        self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, refine_landmarks=True,
                                               min_tracking_confidence=0.5, max_num_faces=1)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.model = joblib.load('../Sign_Text/sign_language_model.pkl')
        self.detected_signs = []  # List to store detected signs

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Camera not initialized.")
            return
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        if not self.cap.isOpened():
            print("Error: Camera not initialized.")
            return

        ret, image = self.cap.read()
        if not ret:
            print("Ignoring empty camera frame.")
            return

        # Process the image
        image = cv2.flip(image, 1)
        original_image = image.copy()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process landmarks
        hands_results = self.hands.process(rgb_image)
        face_results = self.face_mesh.process(rgb_image)
        pose_results = self.pose.process(rgb_image)

        # Draw face landmarks first
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                self.draw_face_landmarks(image, face_landmarks)

        # Draw pose landmarks next
        if pose_results.pose_landmarks:
            self.draw_pose_landmarks(image, pose_results.pose_landmarks)

        # Draw hand landmarks last to ensure they appear on top
        if hands_results.multi_hand_landmarks:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                self.draw_hand_landmarks(image, hand_landmarks)
                features = self.extract_landmarks(hand_landmarks)
                prediction = self.predict_sign_language(features)

                # Add prediction to the list
                if prediction not in self.detected_signs:
                    self.detected_signs.append(prediction)
                if len(self.detected_signs) > 3:  # Limit the list to 3 recent predictions
                    self.detected_signs.pop(0)

                # Update the label with concatenated predictions
                self.ids.prediction_label.text = " ".join(self.detected_signs)

        # Display image in the app
        self.update_camera_texture(image)

    def update_camera_texture(self, image):
        """Update the camera texture."""
        image = cv2.resize(image, (700, 600))
        buf = cv2.flip(image, 0).tobytes()
        texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.ids['camera'].texture = texture

    def extract_landmarks(self, hand_landmarks):
        """Extract landmarks for the model."""
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.append(landmark.x)
            landmarks.append(landmark.y)
            landmarks.append(landmark.z)
        return np.array(landmarks).reshape(1, -1)

    def predict_sign_language(self, features):
        """Predict sign language from features."""
        prediction = self.model.predict(features)
        return prediction[0]

    def draw_hand_landmarks(self, image, hand_landmarks):
        """Draw hand landmarks."""
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )

    def draw_face_landmarks(self, image, face_landmarks):
        """Draw face landmarks."""
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)
        )

    def draw_pose_landmarks(self, image, pose_landmarks):
        """Draw pose landmarks."""
        mp_drawing.draw_landmarks(
            image, pose_landmarks, mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=3),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
        )

    def on_enter(self):
        self.cap = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_leave(self):
        Clock.unschedule(self.update)
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()


# from main_imports import MDScreen
# from ProjectFiles.applibs import utils
# import warnings
# from kivy.graphics.texture import Texture
# from kivy.clock import Clock
# import cv2
# import numpy as np
# import mediapipe as mp
# import tensorflow as tf
#
# warnings.filterwarnings('ignore')
# utils.load_kv("Sign_to_text.kv")
#
# # MediaPipe setup
# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
# mp_face_mesh = mp.solutions.face_mesh
# mp_pose = mp.solutions.pose
#
# # Drawing specifications
# face_landmark_style = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
# face_connection_style = mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=1)
#
#
#
# class Sign_to_text_Screen(MDScreen):
#     def __init__(self, **kwargs):
#         super(Sign_to_text_Screen, self).__init__(**kwargs)
#
#         # Initialize MediaPipe models
#         self.hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2)
#         self.face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, refine_landmarks=True,
#                                                min_tracking_confidence=0.5, max_num_faces=1)
#         self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
#
#         # Load trained model
#         self.model = tf.keras.models.load_model('../Sign_Text/my_model82.h5')
#
#         # Variables for storing predictions
#         self.sequence = []
#         self.detected_signs = []
#         self.frame_limit = 30
#         self.confidence_threshold = 0.70  # Confidence threshold for predictions
#
#         # Start camera
#         self.cap = cv2.VideoCapture(0)
#         if not self.cap.isOpened():
#             print("Error: Camera not initialized.")
#             return
#
#         # Schedule update function
#         Clock.schedule_interval(self.update, 1.0 / 30.0)
#
#     def update(self, dt):
#         if not self.cap.isOpened():
#             print("Error: Camera not initialized.")
#             return
#
#         ret, image = self.cap.read()
#         if not ret:
#             print("Ignoring empty camera frame.")
#             return
#
#         image = cv2.flip(image, 1)  # Flip for correct orientation
#         rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#         # Process frames for landmarks
#         hands_results = self.hands.process(rgb_image)
#         face_results = self.face_mesh.process(rgb_image)
#         pose_results = self.pose.process(rgb_image)
#
#         # Extract features
#         features = self.extract_landmarks(hands_results, face_results, pose_results)
#
#         if features is not None:  # Ensure valid data is present
#             self.sequence.append(features)
#
#             # Maintain a rolling sequence of 30 frames
#             if len(self.sequence) > self.frame_limit:
#                 self.sequence.pop(0)
#
#             # Predict once we have 30 frames
#             if len(self.sequence) == self.frame_limit:
#                 prediction, confidence = self.predict_sign_language(np.array(self.sequence))
#
#                 # Only update detected signs if confidence is above the threshold
#                 if confidence >= self.confidence_threshold:
#                     if prediction not in self.detected_signs:
#                         self.detected_signs.append(prediction)
#                     if len(self.detected_signs) > 3:  # Keep only the last 3 detected words
#                         self.detected_signs.pop(0)
#
#                     # Update the UI label
#                     self.ids.prediction_label.text = " ".join(self.detected_signs) if confidence >= self.confidence_threshold else ""
#
#         # Draw keypoint skeleton
#         self.draw_skeleton(image, hands_results, face_results, pose_results)
#
#         self.update_camera_texture(image)
#
#     def extract_landmarks(self, hands_results, face_results, pose_results):
#         """Ensures feature vector always has 1662 elements."""
#         landmarks = []
#
#         # Hand landmarks (2 hands, 21 points each, 3D = 126)
#         hand_landmarks_list = [[0] * 63] * 2  # Default to zero
#         if hands_results and hands_results.multi_hand_landmarks:
#             for i, hand_landmarks in enumerate(hands_results.multi_hand_landmarks[:2]):
#                 hand_landmarks_list[i] = [coord for landmark in hand_landmarks.landmark for coord in
#                                           (landmark.x, landmark.y, landmark.z)]
#         landmarks.extend(hand_landmarks_list[0] + hand_landmarks_list[1])
#
#         # Face landmarks (468 points, 3D = 1404)
#         face_landmarks_list = [0] * (468 * 3)
#         if face_results and face_results.multi_face_landmarks:
#             face_landmarks = face_results.multi_face_landmarks[0]
#             face_landmarks_list = [coord for landmark in face_landmarks.landmark for coord in
#                                    (landmark.x, landmark.y, landmark.z)]
#         landmarks.extend(face_landmarks_list)
#
#         # Pose landmarks (33 points, 3D = 99)
#         pose_landmarks_list = [0] * (33 * 3)
#         if pose_results and pose_results.pose_landmarks:
#             pose_landmarks_list = [coord for landmark in pose_results.pose_landmarks.landmark for coord in
#                                    (landmark.x, landmark.y, landmark.z)]
#         landmarks.extend(pose_landmarks_list)
#
#         # Ensure exact 1662 elements
#         landmarks.extend([0] * (1662 - len(landmarks)))
#         return np.array(landmarks)
#
#     def predict_sign_language(self, features):
#         """Predicts sign language using the trained LSTM model."""
#         features = features.reshape(1, 30, -1)  # Reshape to match model input
#         prediction = self.model.predict(features)
#         predicted_index = np.argmax(prediction)  # Get index of highest probability
#         confidence = np.max(prediction)  # Get confidence of prediction
#         return self.get_word_from_index(predicted_index), confidence
#
#     def get_word_from_index(self, index):
#         """Maps predicted index to the corresponding word."""
#         word_list = ['1', '2', '3', 'Afternoon', 'Ayubowan', 'Evening', 'Good', 'Month', 'Morning', 'Night','Noon']
#         return word_list[index] if index < len(word_list) else "Unknown"
#
#     def draw_skeleton(self, image, hands_results, face_results, pose_results):
#         """Draws keypoints and connections on the camera feed."""
#         # Convert image to RGB
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#         # Draw hands
#         if hands_results.multi_hand_landmarks:
#             for hand_landmarks in hands_results.multi_hand_landmarks:
#                 mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#
#         # Draw face
#         if face_results.multi_face_landmarks:
#             for face_landmarks in face_results.multi_face_landmarks:
#                 mp_drawing.draw_landmarks(image, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
#                                           landmark_drawing_spec=face_landmark_style,
#                                           connection_drawing_spec=face_connection_style)
#
#         # Draw pose
#         if pose_results.pose_landmarks:
#             mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
#
#     def update_camera_texture(self, image):
#         """Update the camera texture for UI display."""
#         image = cv2.resize(image, (700, 600))
#         buf = cv2.flip(image, 0).tobytes()
#         texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
#         texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
#         self.ids['camera'].texture = texture
#
#     def on_enter(self):
#         """Restart video capture when entering the screen."""
#         self.cap = cv2.VideoCapture(0)
#         Clock.schedule_interval(self.update, 1.0 / 30.0)
#
#     def on_leave(self):
#         """Release resources when leaving the screen."""
#         Clock.unschedule(self.update)
#         if self.cap.isOpened():
#             self.cap.release()
#         cv2.destroyAllWindows()
