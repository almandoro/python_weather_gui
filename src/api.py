from typing import List

import requests
import json

from utils import icon_mapping


class WeatherDay:
    forecast_date: str
    max_temp: str
    min_temp: str
    weather: str
    weather_icon: int
    icon_path: str

    def _find_icon_path(self):
        for map in icon_mapping:
            for item in map.items():
                file = item[0]
                numbers = item[1]
                if str(self.weather_icon) in numbers:
                    return file

        return 'default.jpg'

    def __init__(self, forecast_date, max_temp, min_temp, weather, weather_icon):
        self.forecast_date = forecast_date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.weather = weather
        self.weather_icon = weather_icon
        self.icon_path = self._find_icon_path()

    def __str__(self):
        return f'---\n' \
               f'{self.forecast_date}\n' \
               f'Max: {self.max_temp}\n' \
               f'Min: {self.min_temp}\n' \
               f'Pogoda: {self.weather}\n' \
               f'Numer ikony: {self.weather_icon}\n' \
               f'Sciezka do ikony: {self.icon_path}\n' \
               f'---\n'


class WeatherApi:
    @staticmethod
    def get_weather(id: str) -> List[WeatherDay]:
        r = requests.get(f'http://wwis.imgw.pl/pl/json/{id}_pl.xml')
        parsed_json = json.loads(r.text)

        weather_days = []
        for day in parsed_json['city']['forecast']['forecastDay']:
            if len(weather_days) == 3:
                break

            weather_day = WeatherDay(
                day['forecastDate'],
                day['maxTemp'],
                day['minTemp'],
                day['weather'],
                day['weatherIcon']
            )
            weather_days.append(weather_day)

        return weather_days
