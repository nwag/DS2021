import dwdpollen
import datetime


class Pollen:

    def __init__(self, location_id1, location_id2, pollen_list=None):
        if pollen_list is None:
            pollen_list = []
        self.date = str(datetime.datetime.now().date())

        self.location_id1 = location_id1
        self.location_id2 = location_id2
        self.pollen_list = pollen_list

        self.error_flag = False
        try:
            api = dwdpollen.DwdPollenApi()
            self.dwd_data = api.get_pollen(region_id=location_id1, partregion_id=location_id2)
            self.error_flag = False
        except:
            self.error_flag = True

        self.load_dict = {}
        self.speech_output = ""

    def get_specific_load(self):
        dict_load_specific = {}
        pollen_dict = self.dwd_data["pollen"]
        for key in self.pollen_list:
            # print(key)
            # print(pollen_dict[key][time]["human"])
            dict_load_specific[key] = pollen_dict[key][self.date]["human"]
        self.load_dict = dict_load_specific

    # def check_is_there_a_specific_load(self):
    #     for pol in self.pollen_list:
    #         if self.dwd_data[pol] != "keine Belastung":
    #             return True
    #     return False

    def get_load_all(self):
        dict_load_all = {}
        pollen_dict = self.dwd_data["pollen"]
        for key in pollen_dict.keys():
            # print(key)
            # print(pollen_dict[key][time]["human"])
            dict_load_all[key] = pollen_dict[key][self.date]["human"]
        self.load_dict = dict_load_all

    def check_is_there_a_load(self):
        for v in self.load_dict.values():
            if v != "keine Belastung":
                return True
        return False

    def generate_talk_output(self):
        output = "Bezüglich der Pollen gibt es"
        if len(self.load_dict) == 1:
            k = list(self.load_dict.keys())[0]
            if "keine" in self.load_dict[k]:
                load = " nur für " + k + " " + self.load_dict[k] + "."
                output += load
            else:
                load = " nur für " + k + " eine " + self.load_dict[k] + "."
                output += load
        else:
            c = 0
            for key in self.load_dict.keys():
                c += 1
                if self.load_dict[key] != "keine Belastung":
                    if c < len(self.load_dict):
                        if "keine" in self.load_dict[key]:
                            load = ", für " + key + " " + self.load_dict[key]
                            output += load
                        else:
                            load = ", für " + key + " eine " + self.load_dict[key]
                            output += load
                    else:
                        if "keine" in self.load_dict[key]:
                            load = " und für " + key + " " + self.load_dict[key] + "."
                            output += load
                        else:
                            load = " und für " + key + " eine " + self.load_dict[key] + "."
                            output += load
        self.speech_output = output

    def main_all(self):
        if self.error_flag:
            self.speech_output = "Ich habe im Moment Probleme die Pollenflug Daten beim deutschen Wetterdienst abzufragen. Versuche es später noch einmal."
        else:
            self.get_load_all()
            if self.check_is_there_a_load():
                self.generate_talk_output()
            else:
                self.speech_output = "Es gibt im Moment keine Pollenbelastung in deiner Region."

    def main_specific(self):
        if self.error_flag:
            self.speech_output = "Ich habe im Moment Probleme die Pollenflug Daten beim deutschen Wetterdienst abzufragen. Versuche es später noch einmal."
        else:
            self.get_specific_load()
            if self.check_is_there_a_load():
                self.generate_talk_output()
            else:
                self.speech_output = "Es gibt im Moment für dich keine Pollenbelastung in der Region."


if __name__ == '__main__':
    obj1 = Pollen(110, 112)
    obj1.main_all()
    print(obj1.speech_output)
