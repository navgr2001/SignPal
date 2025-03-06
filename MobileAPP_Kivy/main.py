import os
from kivy.uix.image import Image


from kivy.uix.popup import Popup
from kivy.uix.video import Video
from kivy.utils import platform
if platform != 'android':
    from kivy.config import Config

    Config.set("graphics", "width", 360)
    Config.set("graphics", "height", 740)
    Config.set('graphics', 'borderless', 'True')

from kivy.core.window import Window
Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"


from ProjectFiles.uix.baseclass.root import Root

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from ProjectFiles.uix.baseclass.Main_Menu import Main_Menu_Screen
from ProjectFiles.uix.baseclass.Sign_to_text import Sign_to_text_Screen
from ProjectFiles.uix.baseclass.Text_to_Sign import Text_to_Sign_Screen
from ProjectFiles.uix.baseclass.Text_to_Speech import Text_to_Speech_Screen
from ProjectFiles.uix.baseclass.Learn_Sign import Learn_Sign_Screen
from ProjectFiles.uix.baseclass.Alphabet import Alphabet_Screen
from ProjectFiles.uix.baseclass.Numbers import Numbers_Screen
from ProjectFiles.uix.baseclass.Words import Words_Screen
from ProjectFiles.uix.baseclass.game import Game_Screen
from main_imports import ImageLeftWidget, MDApp, TwoLineAvatarListItem
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.toolbar import MDToolbar




if platform != 'android':
    from kivy.config import Config
    Config.set("graphics", "width", 360)
    Config.set("graphics", "height", 740)
    Config.set('graphics', 'borderless', 'True')

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"

# Preloader screen
class PreloaderScreen(MDScreen):
    pass

class TabContent(BoxLayout, MDTabsBase):
    """Class to define content for each tab."""
    pass
class Sign2024(MDApp):
    def __init__(self, **kwargs):
        super(Sign2024, self).__init__(**kwargs)

        self.APP_NAME = "apk "
        self.COMPANY_NAME = "apk"

    def all_chats(self):
        # self.change_screen("profile")
        twolineW = TwoLineAvatarListItem(text=f"SignApp",
                                         secondary_text="@username",
                                         on_touch_up=self.chat_room)

        self.screen_manager.get_screen("login").ids.chat_tab.add_widget(twolineW)

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.accent_palette = "Indigo"
        self.theme_cls.accent_hue = "500"
        self.theme_cls.theme_style = "Light"
        self.screen_manager = Root()

        self.screen_manager.add_widget(PreloaderScreen(name='preloader'))
        self.screen_manager.add_widget(Text_to_Sign_Screen())
        self.screen_manager.add_widget(Main_Menu_Screen())
        self.screen_manager.add_widget(Sign_to_text_Screen())
        self.screen_manager.add_widget(Text_to_Speech_Screen())
        self.screen_manager.add_widget(Learn_Sign_Screen())
        self.screen_manager.add_widget(Game_Screen())
        self.screen_manager.add_widget(Alphabet_Screen(name="Alphabet"))
        self.screen_manager.add_widget(Numbers_Screen(name="Numbers"))
        self.screen_manager.add_widget(Words_Screen(name="Words"))
        # Set initial screen to preloader
        Clock.schedule_once(self.load_main_menu, 5)  # Show preloader for 3 seconds
        return self.screen_manager

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """
        Handle the tab switching event.

        :param instance_tabs: MDTabs instance
        :param instance_tab: The currently active tab
        :param instance_tab_label: Tab label instance
        :param tab_text: The text of the selected tab
        """
        print(f"Switched to tab: {tab_text}")

    def open_frames_popup(self, frames_folder):
        """
        Opens a popup window to play frames as a video.
        :param frames_folder: Path to the folder containing extracted frames
        """
        layout = BoxLayout(orientation='vertical')
        image_widget = Image()
        layout.add_widget(image_widget)

        popup = Popup(
            title="Video Playback",
            content=layout,
            size_hint=(0.8, 0.8),
            auto_dismiss = False
        )
        popup.open()

        # Get all frame files sorted
        frame_files = sorted(
            [os.path.join(frames_folder, f) for f in os.listdir(frames_folder) if f.endswith(".jpg")]
        )

        # Play frames
        def update_frame(dt):
            if frame_files:
                frame = frame_files.pop(0)
                image_widget.source = frame
            else:
                Clock.unschedule(update_frame)  # Stop playback when all frames are shown
                popup.dismiss()

        Clock.schedule_interval(update_frame, 1 / 30)  # Update at ~30 FPS


    def load_main_menu(self, *args):
        self.screen_manager.current = 'Main_Menu'

    def on_start(self):
        self.screen_manager.change_screen("Main_Menu")

if __name__ == "__main__":
    Sign2024().run()
