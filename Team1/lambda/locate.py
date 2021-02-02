import csv
from datetime import datetime
from simple_dwd_weatherforecast import dwdforecast
from random import choice


# Find nearest Station-ID automatically
# id = dwdforecast.get_nearest_station_id(50.1109221, 8.6821267)

class Locate:
    region_partregion_ids_dict = {"Baden-Württemberg": [110, {"Oberrhein und unteres Neckartal": 111,
                                                              "Hohenlohe/mittlerer Neckar/Oberschwaben": 112,
                                                              "Mittelgebirge Baden-Württemberg": 113}],
                                  "Bayern": [110, {"Allgäu/Oberbayern/Bay. Wald": 121,
                                                   "Donauniederungen": 122,
                                                   "Bayern n. der Donau, o. Bayr. Wald, o. Mainfranken": 123,
                                                   "Mainfranken": 124}],
                                  "Rheinland-Pfalz": [100, {"Saarland": 103,
                                                            "Rhein, Pfalz, Nahe und Mosel": 101,
                                                            "Mittelgebirgsbereich Rheinland-Pfalz": 102}],
                                  "Saarland": [100, {"Saarland": 103,
                                                     "Rhein, Pfalz, Nahe und Mosel": 101,
                                                     "Mittelgebirgsbereich Rheinland-Pfalz": 102}],

                                  "Hessen": [90, {"Nordhessen und hess. Mittelgebirge": 91,
                                                  "Rhein-Main": 92}],
                                  "Sachsen": [80, {"Tiefland Sachsen": 81,
                                                   "Mittelgebirge Sachsen": 82}],
                                  "Thüringen": [70, {"Tiefland Thüringen": 71,
                                                     "Mittelgebirge Thüringen": 72}],
                                  "Sachsen-Anhalt": [60, {"Tiefland Sachsen-Anhalt": 61,
                                                          "Harz": 62}],
                                  "Berlin": [50, {"Brandenburg und Berlin": -1}],
                                  "Brandenburg": [50, {"Brandenburg und Berlin": -1}],
                                  "Nordrhein-Westfalen": [40, {"Rhein.-Westfäl. Tiefland": 41,
                                                               "Ostwestfalen": 42,
                                                               "Mittelgebirge NRW": 43}],
                                  "Bremen": [30, {"Westl. Niedersachsen/Bremen": 31,
                                                  "Östl. Niedersachsen": 32}],
                                  "Niedersachsen": [30, {"Westl. Niedersachsen/Bremen": 31,
                                                         "Östl. Niedersachsen": 32}],
                                  "Mecklenburg-Vorpommern": [20, {"Mecklenburg-Vorpommern": -1}],
                                  "Hamburg": [10, {"Inseln und Marschen": 11,
                                                   "Geest": 12}],
                                  "Schleswig-Holstein": [10, {"Inseln und Marschen": 11,
                                                              "Geest": 12}]
                                  }

    def __init__(self, plz):
        self.plz_dict_csv = {}
        self.plz_state_dict = {}
        self.plz = str(plz)

        self.result_lat = 0
        self.result_lon = 0
        self.result_town = 0
        # self.result = {"lat": 0, "lon": 0, "town": ""}

        self.result_weatherstation_id = ""
        self.result_weatherstation_town = ""

        self.region_id = 0
        self.partregion_id = 0
        self.state = ""

        self.load_using_csv()
        self.load_plz_state_from_csv()

    def load_using_csv(self):
        with open("PLZ.tab", newline="", encoding='utf-8') as plz_file:
            csv_reader = csv.DictReader(plz_file, delimiter="\t")
            c = 0
            for row in csv_reader:
                self.plz_dict_csv[c] = row
                c += 1

    def load_plz_state_from_csv(self):
        with open("zuordnung_plz_ort.csv", newline="", encoding='utf-8') as state_file:
            csv_reader = csv.DictReader(state_file, delimiter=",")
            for row in csv_reader:
                self.plz_state_dict[row["plz"]] = row["bundesland"]

    def __load_plz(self, plz):
        self.plz = str(plz)

    def look_up_coord(self):
        self.result_lon = 0
        self.result_lat = 0
        self.result_town = "not found"
        for key in self.plz_dict_csv.keys():
            if self.plz_dict_csv[key]["plz"] == self.plz:
                self.result_lon = float(self.plz_dict_csv[key]["lon"])
                self.result_lat = float(self.plz_dict_csv[key]["lat"])
                self.result_town = self.plz_dict_csv[key]["Ort"]

    def look_up_state(self):
        self.state = self.plz_state_dict[self.plz]
        self.region_id = Locate.region_partregion_ids_dict[self.state][0]
        if self.region_id == 110:
            self.partregion_id = 112
        else:
            part_region_ids_list = list(Locate.region_partregion_ids_dict[self.state][1].values())
            self.partregion_id = choice(part_region_ids_list)

    def find_nearest_wheater_station(self):
        self.result_weatherstation_id = dwdforecast.get_nearest_station_id(lat=self.result_lat, lon=self.result_lon)
        dwd_weather_data = dwdforecast.Weather(self.result_weatherstation_id)
        self.result_weatherstation_town = dwd_weather_data.get_station_name().capitalize()

    def main_loc_cloth(self):
        self.look_up_coord()
        self.find_nearest_wheater_station()
