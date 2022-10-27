import requests
import json
import string    
import random 
from datetime import date
from kivy.properties import ObjectProperty
from kivymd.uix.label import MDLabel
#:import C kivy.utils.get_color_from_hex
from kivy.utils import get_color_from_hex as C
from kivy.uix.image import Image
import time


class UsersFunction():
    users_link = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/users/.json"
    company_link = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/company/.json"
    firebase_url = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/.json"


    def __init__(self):
        pass

    def company_code_generator(self):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
        return code 
    def clear_field_login(self): # CLEAR THE TEXT FIELD OF LOGIN
        self.main.new_sign_in_screen.username.text = ""
        self.main.new_sign_in_screen.password.text = ""
    def bootingScreen(self):
        time.sleep(5)
        self.main.current = "employer_main"
    def login(self):
        data = self.main.new_sign_in_screen
        user_link =  "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/users/"
        response = requests.get(url=user_link+data.username.text+".json")
        user_details = response.json()
        if data.password.text == "":
            data.username.text = ""
        elif user_details == None:
            data.username.text = ""
            data.password.text = ""
        else:
        
            # NEW DATE BREAKS THE OLD ACCOUNTS BECAUSE OF KEY ERROR 
            if data.password.text == user_details["password"]:
                self.state = user_details['type']
                self.current_user = data.username.text
                self.current_user_data = user_details
                self.current_user_url = user_link+data.username.text+".json"
                self.clear_field_login()
            else:
                data.username.text = ""
                data.password.text = ""

        if self.state == 1:
            self.updateDataTables()
            self.main.current = "employer_main"
        elif self.state == 2:
            self.generate_fatigue_status()
            self.hr = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"])/60
            self.min = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"])%60
            self.main.current = "employee_home_screen"
            self.fatigue = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["fatigue"])
            self.sleep = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["sleep"])
            self.work= int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["work"])
            self.apetite = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["apetite"])
            self.hygiene = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["hygiene"])
            

        #user_details["username"] = data.username.text
    
    def logout(self):
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
        self.to_sign_in()
        self.to_nav_1()
        screen = self.main.employer_main.float_2.employer_nav.employer_home.user_box
        screen.clear_widgets()
        self.main.employer_main.float_2.employer_nav.current = "employer_home"

    def company_code(self):
        data = self.main.pre_employee
        res = requests.get(url=self.company_link)
        i = 0
        company_codes = res.json().keys()
        for code in company_codes:
            if code == data.company_code.text:
                i = 1
                self.main.current = "employee_sign_up_screen"
                self.main.employee_sign_up_screen.employee_code.text = code
        if i == 0:
            self.main.current = "new_sign_in_screen"
        self.main.employee_sign_up_screen.full_name.text=""
        self.main.employee_sign_up_screen.username.text=""
        self.main.employee_sign_up_screen.password.text=""
    def sign_up(self, acc_type):
        user_link = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/users/"
        today = date.today()
        if acc_type == 1:
            data = self.main.employer_sign_up_screen
            code = self.company_code_generator()
            user_data = {
                data.username.text: {
                    "full_name": data.full_name.text,
                    "company_code": code,
                    "password": data.password.text,
                    "type": acc_type
                }
            }
            company_data = {code: {data.username.text: today.strftime("%m-%d-%Y")}}
            requests.patch(url=self.company_link, json=json.loads(json.dumps(company_data)))
        elif acc_type == 2:
            data = self.main.employee_sign_up_screen
            user_data = {
                data.username.text: {
                    "full_name": data.full_name.text,
                    "company_code": data.employee_code.text,
                    "password": data.password.text,
                    "type": acc_type,
                    "data": ""
                }
            }
            company_data = {data.username.text: today.strftime("%m-%d-%Y")}
            requests.patch(url="https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/company/"+data.employee_code.text+"/.json", json=json.loads(json.dumps(company_data)))
            
            
            
            #requests.patch(url=self.users_link, json=json.loads(json.dumps(user_data)))
        #M1UMT1DSF7 company code testing
        print(user_data)
        requests.patch(url=self.users_link, json=json.loads(json.dumps(user_data)))
        #init date data
        init_data = {self.today.strftime("%m-%d-%Y"):""}
        requests.patch(url=self.user_link+data.username.text+"/data/.json", json=json.loads(json.dumps(init_data)))
        #init sleep hour
        factors = ("sleep","work","hygiene","apetite","total_sleep","fatigue")
        for factor in factors:
            factor_data = {factor:0}
            requests.patch(url=self.user_link+data.username.text+"/data/"+self.today.strftime("%m-%d-%Y")+"/.json", json=json.loads(json.dumps(factor_data)))
        self.main.current = "new_sign_in_screen"


    def getEmployeeList(self): # # 01TJY1BTLP #eeeeq
        data = self.current_user_data 
        comp_link =  "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/company/"
        user_link =  "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/users/"
        users_list = {}
        response = requests.get(url=comp_link+data['company_code']+".json").json()
        #for user in response:
        for user in response.keys():
            if user != self.current_user:
                #users_list.append(requests.get(url=user_link+user+".json").json())
                users_list[user] = (requests.get(url=user_link+user+".json").json())
                x = int(users_list[user]["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"])
                
                print(x)
        print(users_list)
        #fatigue = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["fatigue"])
        date_today = date.today()
        code = 0
        print(data)
        #Comp_code = users_list[response.keys(0)]['company_code']
        #self.main.employer_main.float_2.employer_nav.employer_menu.company_field.text = Comp_code
        return users_list


    def updateDataTables(self):
        screen = self.main.employer_main.float_2.employer_nav.employer_home
        users_list = self.getEmployeeList()
        #print(users_list)
        for user in users_list:
            Comp_code = users_list[user]['company_code']
            self.main.employer_main.float_2.employer_nav.employer_menu.company_field.text = Comp_code
            fatigue = users_list[user]['data'][date.today().strftime("%m-%d-%Y")]["fatigue"]
            sleep = int(users_list[user]["data"][date.today().strftime("%m-%d-%Y")]["sleep"])
            work= int(users_list[user]["data"][date.today().strftime("%m-%d-%Y")]["work"])
            apetite = int(users_list[user]["data"][date.today().strftime("%m-%d-%Y")]["apetite"])
            hygiene = int(users_list[user]["data"][date.today().strftime("%m-%d-%Y")]["hygiene"])
            name = users_list[user]["full_name"]
            #TOTAL SLEEP TIME FROM DB
            sleep_time=users_list[user]["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"]
            final_level=0
            level=0
            if fatigue > 0 and fatigue <= 28:
                level = 1
            elif fatigue >=29 and fatigue <=56:
                level = 2
            elif fatigue >= 57 and fatigue <= 84:
                level = 3
            elif fatigue >= 85 and fatigue <= 112:
                level = 4
            elif fatigue > 112:
                level = 5
            # THIS WILL WORK ONLY IF BOTH HAS A VALUE
            if level != 0 and sleep_time != 0:
                if level ==1: # COLUMN 1 of the table
                    if sleep_time < (5*60):
                        final_level=2
                    elif sleep_time < 6*60 and sleep_time >= (5*60):
                        final_level=2
                    elif sleep_time < 7*60 and sleep_time >= (6*60):
                        final_level=1
                    elif sleep_time < 8*60 and sleep_time >= (7*60):
                        final_level=1
                    elif sleep_time >= 8*60:
                        final_level=1
                if level == 2: # COLUMN 1 of the table
                    if sleep_time < (5*60):
                        final_level=3
                    elif sleep_time < 6*60 and sleep_time >= (5*60):
                        final_level=3
                    elif sleep_time < 7*60 and sleep_time >= (6*60):
                        final_level=2
                    elif sleep_time < 8*60 and sleep_time >= (7*60):
                        final_level=2
                    elif sleep_time >= 8*60:
                        final_level=1
                if level == 3: # COLUMN 1 of the table
                    if sleep_time < (5*60):
                        final_level=4
                    elif sleep_time < 6*60 and sleep_time >= (5*60):
                        final_level=3
                    elif sleep_time < 7*60 and sleep_time >= (6*60):
                        final_level=3
                    elif sleep_time < 8*60 and sleep_time >= (7*60):
                        final_level=2
                    elif sleep_time >= 8*60:
                        final_level=1
                if level == 4: # COLUMN 1 of the table
                    if sleep_time < (5*60):
                        final_level=4
                    elif sleep_time < 6*60 and sleep_time >= (5*60):
                        final_level=4
                    elif sleep_time < 7*60 and sleep_time >= (6*60):
                        final_level=3
                    elif sleep_time < 8*60 and sleep_time >= (7*60):
                        final_level=3
                    elif sleep_time >= 8*60:
                        final_level=2
                if level == 5: # COLUMN 1 of the table
                    if sleep_time < (5*60):
                        final_level=4
                    elif sleep_time < 6*60 and sleep_time >= (5*60):
                        final_level=4
                    elif sleep_time < 7*60 and sleep_time >= (6*60):
                        final_level=4
                    elif sleep_time < 8*60 and sleep_time >= (7*60):
                        final_level=3
                    elif sleep_time >= 8*60:
                        final_level=2
            if final_level == 0:
                message="Not yet assessed"
                image='images/neutral.png'
            elif final_level == 1:
                message="Low Fatigue"
                image='images/low.png'
            elif final_level == 2:
                message="Moderate Fatigue"
                image='images/moderate.png'
            elif final_level == 3:
                message="High Fatigue"
                image='images/high.png'
            elif final_level == 4:
                message="Extreme Fatigue"
                image='images/extreme.png'


            print(f'Name: {user}\nfatigue: {fatigue}, total sleep: {sleep_time}, fatigue level is: {level} severity level is {final_level}')
            labels = MDLabel(
                text = f"{name} ",
                pos_hint = {'center_x':0.5,'center_y':1},
                theme_text_color="Custom",
                text_color= C("e8e8e8"),
                font_size= 12
            )
            screen.user_box.add_widget(labels)
            labels = MDLabel(
            #if fatigue 
                text = f"{message}",
                pos_hint = {'center_x':0.5,'center_y':1},
                theme_text_color="Custom",
                text_color= C("e8e8e8"),
                font_size= 10,
                padding = (5,5),
                falign = "center"
            )
            screen.user_box.add_widget(labels)
            labels = Image(
                pos_hint = {'center_x':0.5,'center_y':1},
                size_hint = (0.8,0.8),
                source = image
            )
            screen.user_box.add_widget(labels)



            #tables.append(user, int(users_list[user]["data"][date.today().strftime("%m-%d-%Y")]["fatigue"]))
        #screen.ids.data_tables.row_data = tables

    