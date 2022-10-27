import kivy
from kivymd.app import MDApp
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import requests
import json
from users_functions import UsersFunction
from kivy.properties import ObjectProperty
from kivy.clock import Clock,mainthread
from kivy.animation import Animation
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout

Window.size = (320, 570)


Builder.load_file("nav2.kv") #timespend UI with edit time button
Builder.load_file("edittime.kv")    
Builder.load_file("home.kv")
Builder.load_file("screen1b.kv")
Builder.load_file("loading.kv")
Builder.load_file("screen1.kv") #old login
Builder.load_file("screen2a.kv")
Builder.load_file("screen2b.kv")
Builder.load_file("try.kv")


class main_kv(ScreenManager):
    pass

class NavBar(FakeRectangularElevationBehavior, MDFloatLayout):
    pass
            
class MainApp(MDApp, UsersFunction):
    firebase_url = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/.json"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def push_data(self):
        json_data = """{
            "type": "string",
            "content": "selwyntarr"
        }"""
        requests.patch(url=self.firebase_url, json=json.loads(json_data))
        print('put')
    def total_time(self): #error handling needed 
        if self.screen.ids.am1.state != 'down':
            print(self.screen.ids.hr1.text,":",self.screen.ids.min1.text)
        else:
            self.screen.ids.hr1.text = str(int(self.screen.ids.hr1.text)+12)
            print(self.screen.ids.hr1.text,":",self.screen.ids.min1.text)
        # THE self.screen format is wrong, remake to the right iherit functions.
        # can print out the times in plaintext format. Need math
        self.total = self.screen.ids.total_time.text
        print(self.total)

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
        self.main.current = "sign_up_screen"
    

    def build(self):
        self.theme_cls.material_style = "M3"
        self.main = main_kv()
        return self.main

    def change_color(self, instance):
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            for i in range(4):
                if f"nav_icon{i+1}" == current_id:
                    self.root.ids[f"nav_icon{i+1}"].text_color = "2c4a6e"
                else:
                    self.root.ids[f"nav_icon{i+1}"].text_color = "1c4a6e"

if __name__ == '__main__':
    MainApp().run()