import requests
import json
from main import debug
import datetime


class Parser:
    """Basic parser object's structure.
    Used for reference"""
    name = "OpenWeatherMap"
    description = "60 calls a minute"
    URL = "https://openweathermap.org/"
    apikey = "c000d489291afdc8c6b578c2c79d2e5f"

    def getData(location_key="292712") -> dict:
        """Parse the data and return as a formatted dict"""
        result = dict()
        rlk = requests.get(
            url="https://api.openweathermap.org/data/2.5/weather?"
            + f"q={location_key}&appid={Parser.apikey}&units=metric"
        )
        if rlk.status_code != 200:
            debug("Couldn't get OWM data, SC != 200")
            return None
        rlk = json.loads(rlk.content)["coord"]
        response = requests.get(
            url="https://api.openweathermap.org/data/2.5/onecall?"
            + f"lat={rlk['lat']}&lon={rlk['lon']}&appid={Parser.apikey}"
            + "&units=metric"
        )
        if response.status_code != 200:
            debug("Couldn't get OWM2 data, SC != 200")
        response = json.loads(response.content)["current"]
        result["Temperature"] = round(float(response["temp"]), 1)
        result["Humidity"] = response["humidity"]
        result["WindSpeed"] = response["wind_speed"]
        result["Pressure"] = response["pressure"]
        result["UVIndex"] = response["uvi"]
        result["SunriseTime"] = datetime.datetime.fromtimestamp(
            int(response["sunrise"])).time().strftime("%H:%M")
        result["SunsetTime"] = datetime.datetime.fromtimestamp(
            int(response["sunset"])).time().strftime("%H:%M")
        response = requests.get(
            url="https://api.openweathermap.org/data/2.5/forecast?"
            + f"q={location_key}&appid={Parser.apikey}&units=metric"
        )
        if response.status_code != 200:
            debug("Couldn't get OWM3 data, SC != 200")
        response = json.loads(response.content)["list"][0]["main"]
        result["DayTemperature"] = round(float(response["temp_max"]), 1)
        result["NightTemperature"] = round(float(response["temp_min"]), 1)
        return result

    def getCity(cityName="Irkutsk") -> str:
        """Get the city id from name"""
        return cityName  # As simple as that, ty OWM :)
