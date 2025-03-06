# from main_imports import MDScreen
# from ProjectFiles.applibs import utils
# import pyttsx3
#
# utils.load_kv("Text_to_Speech.kv")
#
# class Text_to_Speech_Screen(MDScreen):
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         # Initialize TTS engine
#         self.tts_engine = pyttsx3.init()
#         # Set speech properties (optional)
#         self.tts_engine.setProperty('rate', 150)  # Speed of speech
#         self.tts_engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
#
#     def speak_text(self):
#         # Get the text from the input field
#         user_input = self.ids.text_input.text.strip()
#         if user_input:
#             print(f"Speaking: {user_input}")
#             self.tts_engine.say(user_input)
#             self.tts_engine.runAndWait()
#         else:
#             print("No text provided for Text-to-Speech")
#
#     def on_stop(self):
#         # Stop TTS engine when exiting the screen
#         self.tts_engine.stop()

from main_imports import MDScreen
from ProjectFiles.applibs import utils
import pyttsx3

utils.load_kv("Text_to_Speech.kv")


class Text_to_Speech_Screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        # Set speech properties (optional)
        self.tts_engine.setProperty("rate", 150)  # Speed of speech
        self.tts_engine.setProperty("volume", 1)  # Volume (0.0 to 1.0)

    def speak_text(self, lang):
        # Determine the active text input based on the language
        if lang == "en":
            user_input = self.ids.text_input_english.text.strip()
            voice_name = "english"
        elif lang == "si":
            user_input = self.ids.text_input_sinhala.text.strip()
            voice_name = "si"
        else:
            user_input = None

        if user_input:
            print(f"Speaking in {lang}: {user_input}")
            # Set the voice
            voices = self.tts_engine.getProperty("voices")
            selected_voice = None
            for voice in voices:
                if voice_name in voice.id:  # Match based on voice id or language
                    selected_voice = voice.id
                    break

            if selected_voice:
                self.tts_engine.setProperty("voice", selected_voice)
            else:
                print(f"No voice found for {voice_name}. Defaulting to system voice.")

            # Speak the text
            self.tts_engine.say(user_input)
            self.tts_engine.runAndWait()

    def on_stop(self):
        # Stop TTS engine when exiting the screen
        self.tts_engine.stop()