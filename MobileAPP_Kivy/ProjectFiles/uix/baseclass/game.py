import os
from random import shuffle
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from MobileAPP_Kivy.ProjectFiles.applibs import utils

utils.load_kv("game.kv")

class Game_Screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = [
            {'video_frames': 'learn_sign/words/monday', 'answer': 'Monday', 'options': ['Monday', 'B', 'C', 'D']},
            {'video_frames': 'learn_sign/words/tuesday', 'answer': 'Tuesday', 'options': ['A', 'Tuesday', 'C', 'D']},
            {'video_frames': 'learn_sign/words/wednesday', 'answer': 'Wednesday', 'options': ['A', 'B', 'Wednesday', 'D']},
            {'video_frames': 'learn_sign/words/thursday', 'answer': 'Thursday', 'options': ['A', 'B', 'C', 'Thursday']},
            {'video_frames': 'learn_sign/words/friday', 'answer': 'Friday', 'options': ['Friday', 'B', 'C', 'D']},
            {'video_frames': 'learn_sign/words/saturday', 'answer': 'Saturday', 'options': ['A', 'Saturday', 'C', 'D']},
            {'video_frames': 'learn_sign/words/sunday', 'answer': 'Sunday', 'options': ['A', 'B', 'Sunday', 'D']},
        ]
        self.score = 0
        self.current_question = 0
        self.current_frame_index = 0
        self.video_interval = 1 / 30  # 30 FPS for video-like playback
        shuffle(self.questions)  # Randomize the questions
        self.display_question()

    def shuffle_questions_and_answers(self):
        shuffle(self.questions)
        for question in self.questions:
            shuffle(question['options'])

    def display_question(self):
        self.clear_widgets()
        self.current_frame_index = 0

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Video Simulation at the Top
        video_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        self.video_frames_path = self.questions[self.current_question]['video_frames']
        self.video_image = Image(size_hint=(1, None), height=250)
        video_layout.add_widget(self.video_image)
        layout.add_widget(video_layout)

        # Start displaying frames as video
        self.start_video_animation()

        # Shuffle answers
        options = self.questions[self.current_question]['options'][:]
        shuffle(options)

        # Answers Below
        options_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=10, padding=10)
        for option in self.questions[self.current_question]['options']:
            button = Button(
                text=option,
                size_hint=(1, None),
                height=50,
                background_color=(0, 0, 0, 0),
                color=(0, 0, 0, 1),
            )
            button.bind(on_release=self.check_answer)
            options_layout.add_widget(button)
        layout.add_widget(options_layout)

        self.add_widget(layout)

    def start_video_animation(self):
        self.frames = sorted(
            [os.path.join(self.video_frames_path, f) for f in os.listdir(self.video_frames_path) if f.endswith('.jpg')]
        )
        if not self.frames:
            print("No frames found in the directory:", self.video_frames_path)
            return

        Clock.schedule_interval(self.update_video_frame, self.video_interval)

    def update_video_frame(self, dt):
        if self.current_frame_index >= len(self.frames):
            self.current_frame_index = 0

        frame_path = self.frames[self.current_frame_index]
        self.video_image.source = frame_path
        self.current_frame_index += 1

    def stop_video_animation(self):
        Clock.unschedule(self.update_video_frame)

    def check_answer(self, instance):
        self.stop_video_animation()
        selected_answer = instance.text
        correct_answer = self.questions[self.current_question]['answer']

        if selected_answer == correct_answer:
            instance.background_color = (0, 1, 0, 1)
            self.score += 1
        else:
            instance.background_color = (1, 0, 0, 1)

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.schedule_next_question()
        else:
            self.show_score()

    def schedule_next_question(self):
        Clock.schedule_once(lambda dt: self.display_question(), 1)


    def show_score(self):
        self.clear_widgets()
        result_layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
        score_label = Label(text=f'Your Score: {self.score}/{len(self.questions)}', font_size=32,color=(0, 0, 0, 1))
        result_layout.add_widget(score_label)

        if self.score >= len(self.questions) // 2:
            message = Label(text='Congratulations!', font_size=24, color=(0, 1, 0, 1))
        else:
            message = Label(text='Try Again!', font_size=24, color=(1, 0, 0, 1))
        result_layout.add_widget(message)

        retry_button = Button(text='Retry', size_hint=(None, None), size=(200, 50),pos_hint={'center_x': 0.5},background_color=(255/255, 0/255, 0/255, 1))
        retry_button.bind(on_release=self.retry_game)
        result_layout.add_widget(retry_button)

        # Home button
        home_button = Button(text='Home', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5},
                             background_color=(13/255, 65/255, 225/255, 1))
        home_button.bind(on_release=self.go_to_home)
        result_layout.add_widget(home_button)

        self.add_widget(result_layout)

    def retry_game(self, instance):
        self.score = 0
        self.current_question = 0
        self.shuffle_questions_and_answers()
        self.display_question()

    def go_to_home(self, instance):
        self.manager.current = 'Main_Menu'

class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Game_Screen(name='game'))
        return sm

if __name__ == '__main__':
    MyApp().run()