from kivy.utils import get_color_from_hex as C
import time
import kivy
import requests
import json
from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from users_functions import UsersFunction
from kivy.properties import ObjectProperty
from kivy.clock import Clock,mainthread
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from survey_functions import SurveyFunctions
from datetime import date
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable, TableHeader, TableData, TablePagination
from kivymd.uix.dialog import BaseDialog
from kivy.uix.stacklayout import StackLayout

#x = [1,5,3,2,4,5,2]
#y = [1,2,3,4,5,6,7]
#plt.plot(x,y)
#plt.ylabel("Y Axis")
#plt.xlabel("X Axis")
#box = self.root.box #THIS IS TO PUT THE content of plt into box id widget in 
#box.add_widget(FigureCanvasKivyAgg(plt.gcf())) #kv file nav3.kv
Window.size = (320, 570)

Builder.load_file("login.kv")
Builder.load_file("home.kv") #landing page (employee)
Builder.load_file("presignup.kv")
Builder.load_file("preemployee.kv") # before employee signup
Builder.load_file("employee.kv")
Builder.load_file("employer.kv")
Builder.load_file("nav2.kv") #timespend UI with edit time button
Builder.load_file("nav3.kv") #input UI with the 4 factors
Builder.load_file("nav4.kv") #input UI with the 4 factors
Builder.load_file("navigationTwo.kv") # 3/4
Builder.load_file("employer_nav.kv")
Builder.load_file("edittime.kv")
Builder.load_file("loading.kv")
Builder.load_file("screen1.kv") #old login
Builder.load_file("screen2a.kv")
Builder.load_file("survey1.kv") #survey questionaire for factor 1 (sleep)


class main_kv(ScreenManager):
    pass

class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass

class MainApp(MDApp, UsersFunction, SurveyFunctions):
    firebase_url = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/.json"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # for current user
        self.state = 0
        self.current_user = None
        self.current_user_data = None
        self.current_user_url = None
        # for survey navigation
        self.page = 0
        self.type = None
        self.value = []
        self.value_storage = []
        self.total = 0
        # time sleep
        self.hr = 0
        self.min = 0
        # fatigue level
        self.fatigue = 0
        self.sleep = 0
        self.work = 0
        self.apetite = 0
        self.hygiene = 0

    def get_sleep_hour(self):
        screen = self.main.employee_home_screen.float.main_screen.sleep.ids
        screen.hour_sleep.text = f"{int(self.hr)}hrs {self.min}mins"

    def total_time(self): #error handling needed 
        screen = self.main.employee_home_screen.float.main_screen.edit_time.ids
        total_sleep_hours = 0
        sleep_time, wake_time = 0, 0
        hr1 = int(screen.hr1.text) if screen.hr1.text != '' else 0 
        min1 = int(screen.min1.text) if screen.min1.text != '' else 0
        hr2 = int(screen.hr2.text) if screen.hr2.text != '' else 0
        min2 = int(screen.min2.text) if screen.min2.text != '' else 0
        if screen.am1.state == "down" and screen.pm1.state == "normal":
            sleep_time = hr1*60+min1
        elif screen.am1.state == "normal" and screen.pm1.state == "down":
            sleep_time = (hr1+12)*60+min1
        if screen.am2.state == "down" and screen.pm2.state == "normal":
            wake_time = hr2*60+min2
        elif screen.am2.state == "normal" and screen.pm2.state == "down":
            wake_time = (hr2+12)*60+min2
        if screen.am2.state == "down" or screen.pm2.state == "down" and screen.am1.state == "down" or screen.pm1.state == "down":
            total_sleep_hours = abs(wake_time - sleep_time)
            screen.total_time.text = f"{int(total_sleep_hours/60)}hrs {total_sleep_hours%60}mins"
            self.hr = int(total_sleep_hours/60)
            self.min = total_sleep_hours%60
            self.push_survey_data("total_sleep", total_sleep_hours)


        #print(f"{int(total_sleep_hours/60)}:{total_sleep_hours%60}")

            

    def push_data(self):
        json_data = """{
            "type": "string",
            "content": "selwyntarr"
        }"""
        requests.patch(url=self.firebase_url, json=json.loads(json_data))
        print('put')

    def get_data(self):
        res = requests.get(url=self.firebase_url)
        print('get')
        print(res.json())

    def delete_data(self):
        delete_url = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/"
        requests.delete(url=delete_url+'content/'+'.json')
        print('delete')
    
    def replace_data(self):
        replace_url = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/"
        replace_input = "type/.json"
        new_json_data = "char"
        requests.put(url=replace_url+replace_input, json=new_json_data)
        print('replace')

    def create_account(self):
        self.main.current = "pre_sign_up_screen"

    def to_pre_employee(self):
        self.main.current = "pre_employee"

    def to_sign_up_employee(self):
        self.main.current = "employee_sign_up_screen"
    
    def to_sign_up_employer(self):
        self.main.current = "employer_sign_up_screen"

    def to_sign_in(self):
        self.main.current = "new_sign_in_screen"
    
    def change_color(self, instance):
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            for i in range(4):
                if f"nav_icon{i+1}" == current_id:
                    self.root.ids[f"nav_icon{i+1}"].background_color = "2c4a6e"
                else:
                    self.root.ids[f"nav_icon{i+1}"].background_color = "1c4a6e"
    def toggle_color(self,):
        pass


    def build(self):
        self.main = main_kv()
        return self.main
    
    

if __name__ == '__main__':
    MainApp().run()