import Parsers.baseParser as baseParser
import requests
import json
import datetime
from main import debug


class Parser(baseParser.Parser):
    """Parser object used for parsing the weather data"""
    name = "AccuWeather"
    description = "AccuWeather has local and international weather forecasts\
         from the most accurate weather forecasting technology\
              featuring up to the minute weather reports."
    URL = "https://www.accuweather.com/"
    apikey = "QxpQIeCf2j0G5iVl043GHXgBCxIP5Iry"
    # QxpQIeCf2j0G5iVl043GHXgBCxIP5Iry
    # 2LkBQzbEiYQyUvlWEfSqjg0GSsLERr4c

    def getData(location_key="292712") -> dict:
        """Parse weather data from the resource and
        return as a formatted dictionary."""
        response = requests.get(
            url="https://dataservice.accuweather.com/currentconditions"
            + f"/v1/{location_key}?apikey={Parser.apikey}"
            + "&metric=true&details=true"
        )  # Creating a request for current condition data
        if response.status_code != 200:
            return None
        # Parsing received weather data using JSON
        response = json.loads(response.content)
        forecast_response = requests.get(
            url="http://dataservice.accuweather.com/forecasts/v1/daily"
            + f"/1day/{location_key}?apikey={Parser.apikey}"
            + "&metric=true&details=true"
        )  # Creating a request for weather forecast data
        debug(forecast_response.url)
        data = dict()
        if forecast_response.status_code != 200:
            return None
        else:
            # Parsing received forecast data using JSON
            forecase_response = json.loads(forecast_response.content)
            # Filling the dictionary
            data["SunriseTime"] = (
                datetime.datetime.fromisoformat(
                    forecase_response["DailyForecasts"][0]["Sun"]["Rise"]
                )
                .time()
                .strftime("%H:%M")
            )
            data["SunsetTime"] = (
                datetime.datetime.fromisoformat(
                    forecase_response["DailyForecasts"][0]["Sun"]["Set"]
                )
                .time()
                .strftime("%H:%M")
            )
            data["NightTemperature"] = forecase_response["DailyForecasts"][0][
                "Temperature"
            ]["Minimum"]["Value"]
            data["DayTemperature"] = forecase_response["DailyForecasts"][0][
                "Temperature"
            ]["Maximum"]["Value"]
        data["Temperature"] = response[0]["Temperature"]["Metric"]["Value"]
        data["Humidity"] = response[0]["RelativeHumidity"]
        data["Pressure"] = response[0]["Pressure"]["Metric"]["Value"]
        data["WindSpeed"] = response[0]["Wind"]["Speed"]["Metric"]["Value"]
        data["UVIndex"] = response[0]["UVIndex"]
        return data
