from datetime import datetime, timedelta
from pytz import timezone

"""{'Kalendar':
                'Datum': 
                        {'event_name': ..., 'event_packlist': ...}
                'Datum2: 
                        {'event_name': ..., 'event_packlist': ...}"""

class CalendarCustom:
    def __init__(self, pers_dict):
        self.pers_dict_calendar = pers_dict
        tz = timezone("Europe/Berlin")
        self.time_today = datetime.now(tz=tz)
        # self.time_new = ""
        self.remove_old_events()
        self.todays_events = []
        self.speech_output = ""

    def add_event(self, event_name, event_date, event_packlist):
        if event_date in self.pers_dict_calendar:
            return 0
        else:
            self.pers_dict_calendar[event_date] = {"event_name": event_name, "event_packlist": event_packlist}
            return 1
    
    def check_if_date_is_valid(self, event_date):
        try:
            d = datetime.strptime(event_date, "%Y-%m-%d %H:%M")
            return 1
        except ValueError:
            return 0
            
    def check_if_date_occupied(self, event_date):
        if event_date in self.pers_dict_calendar:
            return 0
        else:
            return 1

    def remove_event_date(self, event_date):
        try:
            del self.pers_dict_calendar[event_date]
            return 1
        except KeyError:
            return 0

    def remove_event_name(self, event_name):
        for key in self.pers_dict_calendar:
            if self.pers_dict_calendar[key]["event_name"] == event_name:
                del self.pers_dict_calendar[key]
                return 1
        return 0

    def look_for_events_today(self):
        """searches for keys, that matches time_today (first date, then time to sort out past events)"""
        for key in self.pers_dict_calendar.keys():
            d = datetime.strptime(key, "%Y-%m-%d %H:%M")
            delta = d - self.time_today.replace(tzinfo=None)
            if delta.total_seconds() > 0 and d.date() == self.time_today.date():
                self.todays_events.append(key)

    def generate_speech_output(self):
        """concatenates todays events to a text for alexa talk"""
        if not self.todays_events:
            self.speech_output = "Du hast fuer heute keine Termine."
        else:
            if len(self.todays_events) == 1:
                event_data = self.pers_dict_calendar[self.todays_events[0]]
                e_time = datetime.strptime(self.todays_events[0], "%Y-%m-%d %H:%M")

                l_string = ""
                c = 0
                if len(event_data["event_packlist"]) == 1:
                    l_string += event_data["event_packlist"][0] + "."
                else:
                    for element in event_data["event_packlist"]:
                        c += 1
                        if c < len(event_data["event_packlist"]):
                            l_string += element + ", "
                        else:
                            l_string = l_string[:-2] + " und " + element + "."
                if e_time.minute == 0:
                    self.speech_output = "Du hast heute einen Termin. {name} um {h} Uhr. Hierfür brauchst du {l}".format(
                        h=e_time.hour, name=event_data["event_name"], l=l_string)
                else:
                    self.speech_output = "<speak>Du hast heute einen Termin. {name} um {h} Uhr <say-as interpret-as='cardinal'>{minu}</say-as>. Hierfür brauchst du {l}</speak>".format(
                        h=e_time.hour, minu=e_time.minute, name=event_data["event_name"], l=l_string)
            else:
                self.speech_output = "<speak>Du hast heute {} Termine. ".format(str(len(self.todays_events)))
                c_o = 0
                for event_date in self.todays_events:
                    c_o += 1

                    event_data = self.pers_dict_calendar[event_date]
                    e_time = datetime.strptime(event_date, "%Y-%m-%d %H:%M")

                    l_string = ""
                    c = 0
                    if len(event_data["event_packlist"]) == 1:
                        l_string += event_data["event_packlist"][0] + "."
                    else:
                        for element in event_data["event_packlist"]:
                            c += 1
                            if c < len(event_data["event_packlist"]):
                                l_string += element + ", "
                            else:
                                l_string = l_string[:-2] + " und " + element + "."

                    if c_o < len(self.todays_events):
                        if e_time.minute == 0:
                            self.speech_output += " {name} um {h} Uhr. Hierfür brauchst du {l}".format(h=e_time.hour,
                                                                                                       minu=e_time.minute,
                                                                                                       name=
                                                                                                       event_data[
                                                                                                           "event_name"],
                                                                                                       l=l_string)
                        else:
                            self.speech_output += " {name} um {h} Uhr <say-as interpret-as='cardinal'>{minu}</say-as>. Hierfür brauchst du {l}".format(
                                h=e_time.hour,
                                minu=e_time.minute,
                                name=
                                event_data[
                                    "event_name"],
                                l=l_string)
                    else:
                        if e_time.minute == 0:
                            self.speech_output += " Und {name} um {h} Uhr. Hierfür brauchst du {l}</speak>".format(
                                h=e_time.hour,
                                minu=e_time.minute,
                                name=
                                event_data[
                                    "event_name"],
                                l=l_string)
                        else:
                            self.speech_output += " Und {name} um {h} Uhr <say-as interpret-as='cardinal'>{minu}</say-as>. Hierfür brauchst du {l}</speak>".format(
                                h=e_time.hour,
                                minu=e_time.minute,
                                name=
                                event_data[
                                    "event_name"],
                                l=l_string)

    def format_date(self, year, month, day, hour, minute=0):
        # self.time_new = datetime.strptime(
        #     "{}-{}-{} {}:{}".format(str(year), str(month), str(day), str(hour), str(minute)), "%Y-%m-%d %H:%M")
        # self.time_new = "{}-{}-{} {}:{}".format(str(year), str(month), str(day), str(hour), str(minute))
        time_new = "{}-{}-{} {}:{:0>2}".format(str(year), str(month), str(day), str(hour), str(minute))
        return time_new

    def remove_old_events(self):
        """goes through pers_calendar_dict and removes past events"""
        for key in list(self.pers_dict_calendar.keys()):
            d = datetime.strptime(key, "%Y-%m-%d %H:%M")
            delta = d - self.time_today.replace(tzinfo=None)
            if delta.total_seconds() < 0:
                del self.pers_dict_calendar[key]
