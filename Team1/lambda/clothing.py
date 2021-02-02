import random

from simple_dwd_weatherforecast import dwdforecast
from datetime import datetime, timezone


class Clothing:
    weather_dict = {"fog": ["Außerdem wird es heute nebelig. Pass auf dich auf."],
                    "lightning-rainy": ["Außerdem kann es heute zu Gewitter kommen. Denke an deine Regensachen."],
                    "pouring": ["Außerdem ist für heute heftiger Regen vorher gesagt. Nimm besser einen Regenschirm mit."],
                    "rainy": [
                        "Außerdem soll heute ein regnerischer Tag werden. Nimm eventuell einen Regenschirm mit."],
                    "snowy": ["Außerdem kann es heute zu Schnee kommen."],
                    "snowy-rainy": ["Außerdem sind heute Regen und Schnee angekündigt. Denke daran, wenn du dir heute eine Jacke "
                                    "aussuchst."]
                    }

    condition_dict = {"fog": "nebelig",
                      "lightning-rainy": "gewittrig",
                      "pouring": "sehr regnerisch",
                      "rainy": "regnerisch",
                      "snowy": "schneien",
                      "snowy-rainy": "Schneeregen geben",
                      "cloudy": "bewölkt",
                      "partlycloudy": "teilweise bewölkt",
                      "sunny": "sonnig"
                      }
    
    clothing_level_dict = {1: "<speak>Also ich würde alle Winterjacken anziehen die ich habe. Draußen ist es <say-as interpret-as='bleep'>beep</say-as> kalt.</speak>",
                      2: "Ziehe dir besser eine Winterjacke an.",
                      3: "Ziehe dir deshalb heute etwas warmes an.",
                      4: "Bei diesen Temperaturen sollte eine leichte Jacke reichen.",
                      5: "Also kannst du deine Sommerklamotten anziehen."}

    condition_level_influence = {"fog": -1,
                                 "lightning-rainy": -1,
                                 "pouring": -1,
                                 "rainy": -1,
                                 "snowy": 0,
                                 "snowy-rainy": 0,
                                 "cloudy": 0,
                                 "partlycloudy": 0,
                                 "sunny": +1
                                 }

    def __init__(self, location_id):
        self.time = datetime.now(timezone.utc)
        self.dwd_weather_data = dwdforecast.Weather(location_id)

        self.min_temp_day_k = self.dwd_weather_data.get_daily_min(dwdforecast.WeatherDataType.TEMPERATURE, self.time)
        self.max_temp_day_k = self.dwd_weather_data.get_daily_max(dwdforecast.WeatherDataType.TEMPERATURE, self.time,
                                                                shouldUpdate=False)
        self.avg_temp_day_k = (self.min_temp_day_k + self.max_temp_day_k) / 2

        self.min_temp_day = round(self.min_temp_day_k - 273.15)
        self.max_temp_day = round(self.max_temp_day_k - 273.15)
        self.avg_temp_day = round(self.avg_temp_day_k - 273.15)
        self.temp_level = 0

        self.worst_condition_day = self.dwd_weather_data.get_daily_condition(self.time, shouldUpdate=False)

        self.recommendation_cond = ""
        self.recommendation_temp = ""

        self.speech_output = ""

    def recommended_clothing_cond(self):
        # temp = average_temp_day(time)
        # cond = worst_condition_day(time)

        if self.worst_condition_day in Clothing.weather_dict.keys():
            self.recommendation_cond = random.choice(Clothing.weather_dict[self.worst_condition_day])
        else:
            self.recommendation_cond = "Im schlimmsten Fall wird es heute {}.".format(
                Clothing.condition_dict[self.worst_condition_day])

    def recommended_clothing_temp(self):
        if self.min_temp_day == self.max_temp_day:
            self.recommendation_temp = "Die Temperaturen liegen heute um die {}".format(str(self.max_temp_day))
        else:
            self.recommendation_temp = "Die Temperaturen liegen heute zwischen {} und {} Grad.".format(
                str(self.min_temp_day), str(self.max_temp_day))

        # if self.max_temp_day <= -26:
        #     self.temp_level = 1
        # elif -26 < self.max_temp_day <= -13:
        #     self.temp_level = 2
        # elif -13 < self.max_temp_day <= 0:
        #     self.temp_level = 3
        # elif 0 < self.max_temp_day <= 10:
        #     self.temp_level = 4
        # elif 10 < self.max_temp_day <= 20:
        #     self.temp_level = 5
        # elif 20 < self.max_temp_day <= 26:
        #     self.temp_level = 6
        # elif 26 < self.max_temp_day:
        #     self.temp_level = 7
        
        if self.avg_temp_day <= -26:
            self.temp_level = 1
        elif -26 < self.avg_temp_day <= 0:
            self.temp_level = 2
        elif 0 < self.avg_temp_day <= 10:
            self.temp_level = 3
        elif 10 < self.avg_temp_day <= 20:
            self.temp_level = 4
        elif 20 < self.avg_temp_day:
            self.temp_level = 5

        cond_infl = Clothing.condition_level_influence[self.worst_condition_day]
        self.temp_level += cond_infl
        if self.temp_level < 1:
            self.temp_level = 1
        if self.temp_level > 5:
            self.temp_level = 5

        self.recommendation_temp += " " + Clothing.clothing_level_dict[self.temp_level]

    def main_rec(self):
        self.recommended_clothing_cond()
        self.recommended_clothing_temp()
        self.speech_output = self.recommendation_temp + " " + self.recommendation_cond


if __name__ == '__main__':
    # Find nearest Station-ID automatically
    # id = dwdforecast.get_nearest_station_id(50.1109221, 8.6821267)

    # dwd_weather = dwdforecast.Weather("10385")  # Station-ID For BERLIN-SCHOENEFELD

    obj1 = Clothing("10385")
    obj1.main_rec()
    print(obj1.speech_output)