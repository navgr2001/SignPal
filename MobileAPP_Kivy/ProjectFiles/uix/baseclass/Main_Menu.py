from main_imports import MDScreen
from ProjectFiles.applibs import utils
import warnings
from kivy.clock import Clock
from kivy.lang import Builder

from kivymd.uix.picker import MDDatePicker

# libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

warnings.filterwarnings('ignore')
utils.load_kv("Main_Menu.kv")


class Main_Menu_Screen(MDScreen):


    pass
