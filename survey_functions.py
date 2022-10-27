import requests
import json
from datetime import date
from kivy.properties import ObjectProperty

class SurveyFunctions():
    user_link = "https://fatigueapp-a7ea1-default-rtdb.asia-southeast1.firebasedatabase.app/users/"
    today = date.today()

    def __init__(self):
        pass
    def reset_toggle_time(self):
        screen = self.main.employee_home
    def check_toggle(self):
        screen = self.main.employee_home_screen.float.main_screen.survey_form_one
        if screen.answer_one.state == "down":
            return 1
        if screen.answer_two.state == "down":
            return 2
        if screen.answer_three.state == "down":
            return 3
        if screen.answer_four.state == "down":
            return 4
        if screen.answer_five.state == "down":
            return 5
    
    def reset_toggle(self):
        screen = self.main.employee_home_screen.float.main_screen.survey_form_one
        screen.answer_one.state = "normal"
        screen.answer_two.state = "normal"
        screen.answer_three.state = "normal"
        screen.answer_four.state = "normal"
        screen.answer_five.state = "normal"

    def init_data(self):
        data = {self.today.strftime("%m-%d-%Y"):""}
        requests.patch(url=self.user_link+self.current_user+"/data/.json", json=json.loads(json.dumps(data)))

    def add_data(self, type, data):
        factor_data = {type:data}
        requests.patch(url=self.user_link+self.current_user+"/data/"+self.today.strftime("%m-%d-%Y")+"/.json", json=json.loads(json.dumps(factor_data)))
    
    def check_data(self, date):
        res = requests.get(url=self.user_link+self.current_user+"/data/"+date+".json")
        if res != None:
            return True
        else:
            return False

    def push_survey_data(self, type, data):
        check = self.check_data(self.today.strftime("%m-%d-%Y"))
        if check == True:
            self.add_data(type, data)
        elif check == False:
            self.init_data()
            self.add_data(type, data)

    def compute_fatigue(self):
        self.current_user_data = requests.get(url=self.user_link+self.current_user+"/.json").json()
        self.sleep = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["sleep"])
        self.work= int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["work"])
        self.apetite = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["apetite"])
        self.hygiene = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["hygiene"])
        fatigue_level = (self.sleep)+(self.work)+(self.apetite)+(self.hygiene)
        print(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"])
        if (self.sleep!=0 and self.work!=0 and self.apetite!=0 and self.hygiene!=0 ):
            print("All is well")
            c1t = round((self.sleep*0.6291) + (self.work*0.2809) + (self.apetite*0.09))
            print (f"c1t is: {c1t}")
            c2t = round((self.sleep*0.2809) + (self.work*0.5689) + (self.apetite*0.0912) + (self.hygiene*0.059))
            print (f"c2t is: {c2t}")
            c3t = round((self.sleep*0.09) + (self.work*0.0912) + (self.apetite*0.6914) + (self.hygiene*0.1274))
            print (f"c3t is: {c3t}")
            c4t = round((self.work*0.059) + (self.apetite*0.1274) + (self.hygiene*0.8136))
            print (f"c3t is: {c4t}")
            total = c1t+c2t+c3t+c4t
            print(total)
        else:
            print("All is not well")
        return int(fatigue_level)
        #screen = self.main.employee_home_screen.float.main_screen.home_two.ids



    def questionnaire(self, type, index):
        factor = ({"sleep": ("I experienced headaches.",
                             "I forget things easily.",
                             "I feel less energetic.",
                             "I lose interest in work.",
                             "I feel tired.",
                             "I do not feel alive and alert.",
                             "I feel hard to prepare myself before going to work."),
                   "work": ("I feel less productive.",
                           "I find it hard to concentrate on my tasks.",
                           "I feel like I slowly lose my energy.",
                           "I feel sleepy.",
                           "I feel I am not getting enough rest.",
                           "I feel so tired.",
                           "I feel like I am mentally exhausted."),
                   "apetite": ("I skip my meal to arrive at work on time.",
                               "I eat instantly cooked food to aid my hunger.",
                               "I do not have enough time and energy to prepare my own    meals. ",
                               "I go to work on an empty stomach.",
                               "I eat less than I usually do when I am busy.",
                               "I skip meals.",
                               "I feel sick or nauseated when I eat."),
                   "hygiene": ("I forget to change my clothes before going to bed after work.",
                                "I forget to brush my teeth.",
                                "I forget to groom before going to work.",
                                "I do not take a bath.",
                                "I do not have time to do my skin care routine.",
                                "I do not work out.",
                                "I do not wash my hands before eating")
                           })
        screen = self.main.employee_home_screen.float.main_screen.survey_form_one
        self.type = type

        # change picture
        if self.type == "sleep":
            screen.factor_title.text = "Today,"
            screen.picture.source = "images/theme1.png"
        elif self.type == "work":
            screen.factor_title.text = "Yesterday,"
            screen.picture.source = "images/theme2.png"
        elif self.type == "apetite":
            screen.factor_title.text = "Yesterday,,"
            screen.picture.source = "images/theme3.png"
        elif self.type == "hygiene":
            screen.factor_title.text = "Yesterday,"
            screen.picture.source = "images/theme4.png"

        # move to different pages
        if self.page == 6: # if last page
            self.value.append(self.check_toggle())
            self.push_survey_data(self.type, sum(self.value))
            self.value = []
            self.page = 0
            print(self.compute_fatigue())
            self.push_survey_data("fatigue", self.compute_fatigue())
            print("final:")
            print(self.value)
            print(self.value_storage)

            if (self.sleep!=0 and self.work!=0 and self.apetite!=0 and self.hygiene!=0):
                self.to_nav_1()
            else:
                self.to_nav_4()
        else:
            # change to submit button if last page
            if self.page == 5:
                screen.next.text = "Submit"
            else:
                screen.next.text = "Next"
            # append or delete entry
            if index == 1:
                self.value.append(self.check_toggle())
                print(self.value)
            elif index == -1:
                self.value.pop()
                print(self.value)
            # navigate thru
            self.page = self.page+index
            screen.question.text = factor[type][self.page]
        # show prev button
        if self.page == 0:
            screen.prev.disabled = True
            screen.prev.opacity = 0
        else:
            screen.prev.disabled = False
            screen.prev.opacity = 1
        # reset toggle every page
        self.reset_toggle()

    def return_to_nav(self):
        self.reset_toggle()
        self.value = []
        self.page = 0
        self.main.employee_home_screen.float.main_screen.current = 'input_factor'
    def to_nav_4(self):
        self.main.employee_home_screen.float.main_screen.current = 'input_factor'
    def to_nav_2(self):
        self.current_user_data = requests.get(url=self.user_link+self.current_user+"/.json").json()
        total_sleep=self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"]
        if self.compute_fatigue() != 0:
            self.main.employee_home_screen.float.main_screen.current = 'sleep'
            self.main.employee_home_screen.float.main_screen.sleep.text = f"{int(total_sleep/60)}hrs {total_sleep%60}mins"
        elif self.compute_fatigue() == 0 and int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"]) == 0:
            self.main.employee_home_screen.float.main_screen.current = 'input_factor'
    def to_nav_1(self):
        self.main.employee_home_screen.float.main_screen.current = 'home_two'
    def generate_fatigue_status(self):
        self.current_user_data = requests.get(url=self.user_link+self.current_user+"/.json").json()
        self.sleep = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["sleep"])
        self.work= int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["work"])
        self.apetite = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["apetite"])
        self.hygiene = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["hygiene"])
        #TOTAL SLEEP TIME FROM DB
        total_sleep=self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"]
        print( total_sleep)
        if (self.sleep!=0 and self.work!=0 and self.apetite!=0 and self.hygiene!=0):
            print("All is well")
        else:
            print("All is not well")
        screen = self.main.employee_home_screen.float.main_screen.home_two
        level=0
        final_level=0
        sleep_time = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["total_sleep"])
        fatigue = int(self.current_user_data["data"][date.today().strftime("%m-%d-%Y")]["fatigue"])
        print(f"TOTAL FATIGUE IS: {fatigue}\n TOTAL SLEEP IS: {sleep_time}")
        # 28, 29-56, 57-84, 85-112, 112+
        # DETERMINE THE LEVEL OF FATIGUE BASED ON THE SURVEY
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
        else:
            print("INPUT NOT FINISHED")
        # DETERMINE IF FINAL_LEVEL IS NOT 0
        if final_level == 0:
            screen.home_button.disabled = False
            screen.home_button.opacity =  1
        if final_level != 0:
            screen.home_button.disabled = True
            screen.home_button.opacity = 0
            if final_level == 1 :
                screen.fatigue_message.text= "You have a LOW risk of fatigue. No specific controls necessary."
                screen.fatigue_picture.source= "images/low.png"
            if final_level == 2 :
                screen.fatigue_message.text= "You have a MODERATE risk of fatigue. The actions at this level involve increased monitoring for fatigue-related impairment."
                screen.fatigue_picture.source= "images/moderate.png"
            if final_level == 3 :
                screen.fatigue_message.text= "You have a HIGH level risk of fatigue. This indicates that the fatigue is likely to occur and it should be supervised."
                screen.fatigue_picture.source= "images/high.png"    
            if final_level == 4 :
                screen.fatigue_message.text= "You have a VERY HIGH risk of fatigue. This indicates the risks associated with fatigue are critical and can potential harm you."
                screen.fatigue_picture.source= "images/extreme.png"
        elif sleep_time==0 and final_level>0:
            screen.fatigue_message.text= "You have not yet changed your sleep time"
            screen.fatigue_picture.source= "images/neutral.png"
            screen.home_button.text = "Set sleep."
        elif sleep_time==0 and final_level==0:
            screen.fatigue_message.text= "You have not assessed your fatigue yet."
            screen.fatigue_picture.source= "images/neutral.png"
        print(final_level)
        print(level,(sleep_time/60))