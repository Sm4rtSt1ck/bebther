import sys
import datetime
from os import walk
import pathlib
import datetime
import database
import json

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

isDebug = True
# References if the debug mode is enabled.
# Controls some behavior such as debug-outputs
currentParser = None  # Contains instance of the selected Parser object
parsers = list()  # List of all available parsers
# Location of this file
directory = pathlib.Path(__file__).parent.resolve()
# Location of .ui files
windows = {  # Windows
    "dark": {  # Dark windows
        "main": f"{directory}\\ui\\main.ui",
        "settings": f"{directory}\\ui\\settings.ui"},
    "light": {  # Light windows
        "main": f"{directory}\\ui\\main_light.ui",
        "settings": f"{directory}\\ui\\settings_light.ui"}}
# Default theme
theme = windows["dark"]
# Autorun
isAutorun = False
# Current city string
currentCity = "Иркутск"
# Default city stored in settings
defaultCity = "Иркутск"
# Last parsed data
last_data = dict()


def debug(value):
    """Modified print method. Prints value if the debug mode is enabled"""
    if isDebug:
        if type(value) == list or type(value) == dict:
            print(f"[DEBUG | {datetime.datetime.now()}]: ", end='')
            print(*value)
        else:
            print(f"[DEBUG | {datetime.datetime.now()}]: {value}")


class Windows(QMainWindow):
    """Windows functionality"""
    def __init__(self):
        """UI Initialization"""
        super().__init__()
        # Connecting and initializing the database
        database.start()
        # Initial UI setup
        self.readSettings()
        global currentCity
        currentCity = defaultCity
        self.updateParsers()
        global parsers
        global currentParser
        if len(parsers) > 0:
            currentParser = parsers[0]
        self.init_main()
        self.updateData()
        self.pushToDatabase()

    def updateCityName(self):
        """Update backend cityName variable from UI"""
        global currentCity
        currentCity = self.cityNameField.toPlainText()

    def toggleParser(self) -> None:
        """Switching to the next available parser"""
        global parsers, currentParser
        if parsers.index(currentParser) + 1 < len(parsers):
            currentParser = parsers[parsers.index(currentParser) + 1]
        else:
            currentParser = parsers[0]
        # Setting the weather source button's text
        self.setting_button_3.setText(currentParser.name)

    def readSettings(self):
        try:
            data = json.loads(open("settings.json", "r").readline())
            global defaultCity, theme, isAutorun
            defaultCity = data["defaultCity"]
            theme = data["theme"]
            isAutorun = data["isAutorun"]
            print(data["defaultCity"])
        except Exception as e:
            debug(f"Couldn't load settings: {e}")

    def writeSettings(self):
        try:
            global defaultCity, theme, isAutorun
            sfile = open("settings.json", "w")
            settings = dict()
            print(defaultCity)
            settings["defaultCity"] = defaultCity
            settings["theme"] = theme
            settings["isAutorun"] = isAutorun
            sfile.write(json.dumps(settings))
        except Exception as e:
            debug(f"Couldn't save settings: {e}")

    def updateParsers(self):
        """Updating list of available parsers"""
        files = list()
        # Getting all files present in the ./Parsers/ folder
        for(dirpath, dirname, filenames) in walk("./Parsers/"):
            files.append(filenames)
            break
        debug(files)
        filenames.remove("baseParser.py")
        result = list()
        # Importing the modules from files
        for i in filenames:
            if i.endswith("Parser.py"):
                result.append(getattr(__import__(
                    f"Parsers.{i.replace('.py', '')}",
                    fromlist=["Parser"]), "Parser"))
            else:
                filenames.remove(i)
        global parsers
        parsers = result

    def updateData(self):
        """Updating weather data using selected parser"""
        global currentParser, last_data
        if currentParser is None:
            return None
        # Getting the parsed data
        data = currentParser.getData(currentParser.getCity(currentCity))
        debug(data if data is not None else "NO WEATHER")
        if data is not None:
            self.l_temp.setText(
                f"{'+' if data['Temperature'] > 0 else ''}"
                + f"{data['Temperature']}°"
            )
            # Filling the parsed data into UI labels
            self.l_humidity.setText(f"{data['Humidity']}%")
            self.l_wind_speed.setText(f"{data['WindSpeed']}m/s")
            self.l_pressure.setText(f"{data['Pressure']}")
            self.l_uv_index.setText(f"{data['UVIndex']}")
            self.l_day_temp.setText(
                f"{'+' if data['DayTemperature'] > 0 else ''}"
                + f"{data['DayTemperature']}°"
            )
            self.l_night_temp.setText(
                f"{'+' if data['NightTemperature'] > 0 else ''}"
                + f"{data['NightTemperature']}°"
            )
            self.l_sunrise.setText(f"{data['SunriseTime']}")
            self.l_sunset.setText(f"{data['SunsetTime']}")
            last_data = data

    def pushToDatabase(self) -> None:
        """Writes current weather data to the database."""
        global last_data, currentCity, currentParser
        if last_data is None:
            debug("last_data was None, couldn't write to the db")
            return
        data = last_data
        data["Date"] = datetime.datetime.now().date()
        data["City"] = currentCity
        data["WeatherSource"] = currentParser.name
        if database.db is None:
            debug("WRITE: database does not exist")
            return
        try:
            database.write(last_data)
        except Exception as e:
            debug(f"Couldn't write to the database: {e}")

    # Main window
    def init_main(self):
        """Loads gui of main window and connects buttons to functions"""
        uic.loadUi(theme["main"], self)
        self.cityNameField.setPlainText(currentCity)
        self.cityNameField.textChanged.connect(self.updateCityName)
        self.setting_button.clicked.connect(self.init_settings)

    # Settings window
    def init_settings(self):
        """Loads gui of settings window,
        defines functions and connects buttons to them"""
        uic.loadUi(theme["settings"], self)

        def changeTheme():
            def light():
                """Switches theme to light"""
                global theme
                theme = windows["light"]
                uic.loadUi(theme["settings"], self)

            def dark():
                """Switches theme to dark"""
                global theme
                theme = windows["dark"]
                uic.loadUi(theme["settings"], self)

            light() if self.theme_light.isChecked() else dark()
            buttons()
            self.writeSettings()

        def changeHometown(index):
            pass

        def autorun():
            def on():
                """Turns autorun on"""
                global isAutorun
                import winreg

                keyVal = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
                registry = winreg.ConnectRegistry(
                    None, winreg.HKEY_CURRENT_USER)

                try:
                    key = winreg.OpenKey(
                        registry, keyVal, 0, winreg.KEY_ALL_ACCESS)
                except OSError:
                    key = winreg.CreateKey(winreg.registry, keyVal)

                winreg.SetValueEx(
                    key, "Bebther", 0, winreg.REG_SZ, f"{directory}\\run.bat")
                winreg.CloseKey(key)
                isAutorun = True

            def off():
                """Turns autorun off"""
                global isAutorun
                import winreg

                keyVal = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
                registry = winreg.ConnectRegistry(
                    None, winreg.HKEY_CURRENT_USER)

                try:
                    key = winreg.OpenKey(
                        registry, keyVal, 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteValue(key, "Bebther")
                    winreg.CloseKey(key)
                    isAutorun = False
                except OSError:
                    pass

            on() if self.autorun_on.isChecked() else off()
            self.writeSettings()

        def buttons():
            """Connects buttons to functions"""
            # Main menu button
            self.main_button.clicked.connect(self.init_main)

            # Theme buttons
            self.theme_light.clicked.connect(changeTheme)
            self.theme_dark.clicked.connect(changeTheme)
            self.theme_light.setChecked(
                True if theme == windows["light"] else False)
            self.theme_dark.setChecked(
                True if theme == windows["dark"] else False)

            # Hometown combobox
            self.hometown_button.currentIndexChanged.connect(changeHometown)

            # Autorun buttons
            self.autorun_on.clicked.connect(autorun)
            self.autorun_off.clicked.connect(autorun)
            self.autorun_on.setChecked(isAutorun)
            self.autorun_off.setChecked(False if isAutorun else True)
        buttons()

# Program's entry point
# Creating application and window instances


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Windows()
    MainWindow.show()
    sys.exit(app.exec_())
