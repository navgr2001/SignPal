from main_imports import BoxLayout
from ProjectFiles.applibs import utils


utils.load_kv("ui_class.kv")

class OneLineTextDialog(BoxLayout):
    
    def input_text(self):
        return self.ids.dialog_text.text
