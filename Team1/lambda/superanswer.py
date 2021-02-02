import calendar_custom
import clothing
import pollen
import forgottenlist

from datetime import datetime


class SuperAnswer:
    def __init__(self, pers_dict):
        self.pers_dict = pers_dict
        try:
            cal_dict = pers_dict["calendar"]
        except KeyError:
            cal_dict = {}

        try:
            clothing_loc = pers_dict["settings"]["user_info"]["location_cloth"]
        except KeyError:
            clothing_loc = "10838"

        try:
            pollen_loc = pers_dict["settings"]["user_info"]["location_pol"]
        except KeyError:
            pollen_loc = [110, 112]

        try:
            forgotten_list = pers_dict["ForgottenList"]
        except KeyError:
            forgotten_list = []

        self.calendar_obj = calendar_custom.CalendarCustom(cal_dict)
        self.clothing_obj = clothing.Clothing(clothing_loc)
        self.pollen_obj = pollen.Pollen(pollen_loc[0], pollen_loc[1])
        self.forgottenlist_obj = forgottenlist.ForgottenList(forgotten_list)

        self.calendar_flag = True
        self.pollen_flag = True
        self.clothing_flag = True
        self.forgottenlist_flag = True

        try:
            self.clothing_flag = pers_dict["settings"]["functions"]["clothing"]
        except KeyError:
            pass

        try:
            self.calendar_flag = pers_dict["settings"]["functions"]["calendar"]
        except KeyError:
            pass

        try:
            self.pollen_flag = pers_dict["settings"]["functions"]["pollen"]
        except KeyError:
            pass

        try:
            self.forgottenlist_flag = pers_dict["settings"]["functions"]["forgottenlist"]
        except KeyError:
            pass

        self.forgottenlist_frequence = 1
        self.forgottenlist_frequence_date = 0  # "%Y-%m-%d

        try:
            self.forgottenlist_frequence = pers_dict["settings"]["frequency"]["forgottenlist"][0]
        except KeyError:
            pass

        self.calendar_output = ""
        self.clothing_output = ""
        self.pollen_output = ""
        self.forgottenlist_output = ""

        self.speech_output = ""

    def calendar(self):
        self.calendar_obj.look_for_events_today()
        self.calendar_obj.generate_speech_output()
        self.calendar_output = self.calendar_obj.speech_output

    def clothing(self):
        self.clothing_obj.main_rec()
        self.clothing_output = self.clothing_obj.speech_output

    def pollen(self):
        self.pollen_obj.main_all()
        self.pollen_output = self.pollen_obj.speech_output

    def forgotten_list(self):
        self.forgottenlist_obj.generate_speech_output_forgotten_list()
        self.forgottenlist_output = self.forgottenlist_obj.speech_output

    def todays_functions(self):
        """looks up which functions are activated and which should be outputed now"""
        if self.clothing_flag:
            self.clothing()

        if self.calendar_flag:
            self.calendar()

        if self.pollen():
            self.pollen()

        if self.forgottenlist_flag:
            if self.forgottenlist_frequence == 1:
                self.forgotten_list()
            else:
                if self.forgottenlist_frequence_date == 0:
                    self.forgotten_list()
                else:
                    date_now = datetime.now()
                    date_then = datetime.strptime(self.forgottenlist_frequence_date, "%Y-%m-%d")
                    time_dif = date_now - date_then
                    time_dif_days = time_dif.days
                    mod_dif = time_dif_days % self.forgottenlist_frequence
                    if mod_dif == 0:
                        self.forgotten_list()

    def generate_speech_output(self):
        if self.forgottenlist_output:
            self.speech_output += self.forgottenlist_output + " "
        if self.calendar_output:
            self.speech_output += " Zudem hast du" + self.calendar_output[7:]
        if self.clothing_output:
            self.speech_output += " " + self.clothing_output
        if self.pollen_output:
            self.speech_output += " Und " + self.pollen_output[0].lower() + self.pollen_output[1:]


if __name__ == '__main__':
    obj = SuperAnswer({})
    obj.todays_functions()
    obj.generate_speech_output()
    print(obj.speech_output)
