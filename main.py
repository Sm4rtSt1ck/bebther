import sys
import datetime
import pathlib
import datetime
import database
import json
import asyncio
from os import walk
import images
import dialogs

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow

isDebug = True  # Controls some behavior such as debug-outputs
currentParser = None  # Contains instance of the selected Parser object
parsers = list()  # List of all available parsers
# Location of this file
directory = pathlib.Path(__file__).parent.resolve()
# Location of .ui files
windows = {  # Windows
    "dark": {  # Dark windows
        "main": f"{directory}\\ui\\main.ui",
        "settings": f"{directory}\\ui\\settings.ui",
        "compare_days": f"{directory}\\ui\\compare_days.ui",
        "compare_sources": f"{directory}\\ui\\compare_sources.ui"},
    "light": {  # Light windows
        "main": f"{directory}\\ui\\main_light.ui",
        "settings": f"{directory}\\ui\\settings_light.ui",
        "compare_days": f"{directory}\\ui\\compare_days_light.ui",
        "compare_sources": f"{directory}\\ui\\compare_sources_light.ui"}}
# Default theme
theme = windows["dark"]
# Autorun
isAutorun = False
# Current city string
currentCity = "Иркутск"
# Default city stored in settings
defaultCity = "Иркутск"
# Last parsed data
last_data = None


def debug(value) -> None:
    """Modified print method. Prints value if the debug mode is enabled"""
    if isDebug:
        if type(value) == list or type(value) == dict:
            print(f"[DEBUG | {datetime.datetime.now()}]: ", end='')
            print(*value)
        else:
            print(f"[DEBUG | {datetime.datetime.now()}]: {value}")


class Windows(QMainWindow):
    """Windows functionality"""
    def __init__(self) -> None:
        """UI Initialization"""
        super().__init__()
        # Connecting and initializing the database
        database.start()
        # Initial UI setup
        self.readSettings()
        global currentCity
        currentCity = defaultCity
        global parsers
        global currentParser
        if len(parsers) > 0:
            currentParser = parsers[0]
        self.init_main()
        self.updateParsers()

    def updateCityName(self) -> None:
        """Update backend cityName variable from UI"""
        global currentCity
        currentCity = self.cityNameField.toPlainText()

    def toggleParser(self, index) -> None:
        """Switching to the next available parser"""
        global parsers, currentParser
        currentParser = parsers[index]
        self.updateData()

    def readSettings(self) -> None:
        """Read settings from the JSON file"""
        try:
            # Opening the file and parsing JSON
            data = json.loads(open(
                f"{directory}\\settings.json", "r").readline())
            global defaultCity, theme, isAutorun
            # Applying to variables
            defaultCity = data["defaultCity"]
            theme = data["theme"]
            isAutorun = data["isAutorun"]
            print(data["defaultCity"])
        except Exception as e:
            debug(f"Couldn't load settings: {e}")

    async def writeSettings(self) -> None:
        """Save settings to the JSON file"""
        try:
            global defaultCity, theme, isAutorun
            sfile = open("settings.json", "w")
            settings = dict()
            # Filling in the dictionary
            settings["defaultCity"] = defaultCity
            settings["theme"] = theme
            settings["isAutorun"] = isAutorun
            # Writing the dumped JSON data to file
            sfile.write(json.dumps(settings))
        except Exception as e:
            debug(f"Couldn't save settings: {e}")

    def updateParsers(self) -> None:
        """Updating list of available parsers"""
        files = list()
        # Getting all files present in the ./Parsers/ folder
        for(dirpath, dirname, filenames) in walk(f"{directory}/Parsers/"):
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
        self.updateParsersUI()

    def updateParsersUI(self) -> None:
        """Updating QComboBox items in UI, adding parsers to select"""
        global parsers
        self.parserBox.clear()
        for i in parsers:
            self.parserBox.addItem(i.name)

    def updateOneParserUI(self, box: QComboBox) -> None:
        """Updating given QComboBox, adding parsers to select"""
        global parsers
        box.clear()
        for i in parsers:
            box.addItem(i.name)

    def getData(self) -> dict:
        """Get data from current parser"""
        global currentParser, last_data
        if currentParser is None:
            return None
        # Getting the parsed data
        data = currentParser.getData(currentParser.getCity(currentCity))
        debug(data if data is not None else "NO WEATHER")
        last_data = data
        if data is None:
            dialogs.NoDataDialog().exec()
        return data

    def updateUI(self, data) -> None:
        """Updating weather data"""
        if data is None:
            return None
        # Filling parsed data into UI labels
        self.l_temp.setText(
            f"{'+' if data['Temperature'] > 0 else ''}"
            + f"{data['Temperature']}°"
        )
        self.l_humidity.setText(f"{data['Humidity']}%")
        self.l_wind_speed.setText(f"{data['WindSpeed']} m/s")
        self.l_pressure.setText(f"{data['Pressure']}")
        self.l_uv_index.setText(f"{data['UVIndex']}")
        self.l_day_temp.setText(
            f"{'+' if data['DayTemperature'] > 0 else ''}"
            + f"{data['DayTemperature']}°"
        )
        self.label_3.setText(
            datetime.datetime.now().time().strftime("%H:%M"))
        self.l_night_temp.setText(
            f"{'+' if data['NightTemperature'] > 0 else ''}"
            + f"{data['NightTemperature']}°"
        )
        self.l_sunrise.setText(f"{data['SunriseTime']}")
        self.l_sunset.setText(f"{data['SunsetTime']}")

    def updateData(self) -> None:
        """Updates data and UI values"""
        data = self.getData()
        if data is not None:
            self.updateUI(data)
        else:
            debug("Error, no data.")

    def pushToDatabase(self) -> None:
        """Writes current weather data to the database."""
        global last_data, currentCity, currentParser
        if last_data is None:
            debug("last_data was None, couldn't write to the db")
            dialogs.DBFailDialog().exec()
            return
        # Formatting dict for database entry
        data = last_data
        data["Date"] = datetime.datetime.now().date()
        data["City"] = currentCity
        data["WeatherSource"] = currentParser.name
        if database.db is None:
            debug("WRITE: database does not exist")
            dialogs.DBFailDialog().exec()
            return
        try:
            database.write(last_data)
            dialogs.DBSavedDialog().exec()
        except Exception as e:
            debug(f"Couldn't write to the database: {e}")
            dialogs.DBFailDialog().exec()

    # Main window
    def init_main(self) -> None:
        """Loads gui of main window,
        defines functions and connects buttons to thems"""
        uic.loadUi(theme["main"], self)
        global last_data
        self.updateParsersUI()  # Updating parsers list in UI
        self.parserBox.currentIndexChanged.connect(self.toggleParser)
        self.updateUI(last_data)  # Updating UI

        def share() -> None:
            """Opens picture with info about weather"""
            global last_data
            if last_data is None:
                dialogs.ShareFailDialog().exec()
                return
            images.Worker.output_image(last_data, theme)

        def buttons() -> None:
            """Connects buttons to functions"""
            self.cityNameField.setPlainText(currentCity)
            self.cityNameField.textChanged.connect(self.updateCityName)
            self.setting_button.clicked.connect(self.init_settings)
            self.reload_button.clicked.connect(self.updateData)
            self.setting_button.clicked.connect(self.init_settings)
            self.compare_days_button.clicked.connect(self.init_compare_days)
            self.compare_sources_button.clicked.connect(
                self.init_compare_sources)
            self.save_button.clicked.connect(self.pushToDatabase)
            self.share_button.clicked.connect(share)
        buttons()

    def changeHometown(self) -> None:
        """Changes local entry of default city and save settings"""
        global defaultCity
        defaultCity = self.hometownField.toPlainText()

    def transitToMain(self) -> None:
        """Transition method from settings to main window"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.writeSettings())
        self.init_main()

    # Settings window
    def init_settings(self) -> None:
        """Loads gui of settings window,
        defines functions and connects buttons to them"""
        uic.loadUi(theme["settings"], self)

        def changeTheme() -> None:
            """Changes theme"""
            def light() -> None:
                """Switches theme to light"""
                global theme
                theme = windows["light"]
                # Reloads current window
                uic.loadUi(theme["settings"], self)

            def dark() -> None:
                """Switches theme to dark"""
                global theme
                theme = windows["dark"]
                # Reloads current window
                uic.loadUi(theme["settings"], self)

            light() if self.theme_light.isChecked() else dark()
            buttons()
            self.writeSettings()

        def autorun() -> None:
            def on() -> None:
                """Turns autorun on"""
                global isAutorun
                import winreg
                keyVal = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
                # Connecting to the registry
                registry = winreg.ConnectRegistry(
                    None, winreg.HKEY_CURRENT_USER)

                # Writing to the registry key or creating a new one
                try:
                    key = winreg.OpenKey(
                        registry, keyVal, 0, winreg.KEY_ALL_ACCESS)
                except OSError:
                    key = winreg.CreateKey(winreg.registry, keyVal)

                # Setting key value
                winreg.SetValueEx(
                    key, "Bebther", 0, winreg.REG_SZ, f"{directory}\\run.lnk")
                # Closing the registry
                winreg.CloseKey(key)
                isAutorun = True

            def off() -> None:
                """Turns autorun off"""
                global isAutorun
                import winreg

                # Connecting to the registry
                keyVal = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
                registry = winreg.ConnectRegistry(
                    None, winreg.HKEY_CURRENT_USER)

                # Removing the registry key
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

        def buttons() -> None:
            """Connects buttons to functions"""
            # Main menu button
            self.main_button.clicked.connect(self.transitToMain)

            # Theme buttons
            self.hometownField.textChanged.connect(self.changeHometown)
            global defaultCity
            self.hometownField.setPlainText(defaultCity)
            self.theme_light.clicked.connect(changeTheme)
            self.theme_dark.clicked.connect(changeTheme)
            self.theme_light.setChecked(
                True if theme == windows["light"] else False)
            self.theme_dark.setChecked(
                True if theme == windows["dark"] else False)

            # Autorun buttons
            self.autorun_on.clicked.connect(autorun)
            self.autorun_off.clicked.connect(autorun)
            self.autorun_on.setChecked(isAutorun)
            self.autorun_off.setChecked(False if isAutorun else True)
        buttons()

    def init_compare_days(self) -> None:
        """Initialize the day comparison UI"""
        uic.loadUi(theme["compare_days"], self)

        self.main_button.clicked.connect(self.init_main)

        def fill_data() -> None:
            """Fill the weather data into UI labels"""
            def today() -> None:
                """Fill today's weather data into UI labels"""
                global last_data
                data = last_data
                if data is None:
                    return False
                # Filling parsed data into UI labels
                self.l_humidity_3.setText(f"{data['Humidity']}%")
                self.l_wind_speed_3.setText(f"{data['WindSpeed']} m/s")
                self.l_pressure_3.setText(f"{data['Pressure']}")
                self.l_uv_index_3.setText(f"{data['UVIndex']}")
                self.l_day_temp_3.setText(
                    f"{'+' if data['DayTemperature'] > 0 else ''}"
                    + f"{data['DayTemperature']}°"
                )
                self.l_night_temp_3.setText(
                    f"{'+' if data['NightTemperature'] > 0 else ''}"
                    + f"{data['NightTemperature']}°"
                )
                self.l_sunrise_3.setText(f"{data['SunriseTime']}")
                self.l_sunset_3.setText(f"{data['SunsetTime']}")

            def yesterday() -> None:
                """Fill yesterday's weather data into UI labels"""
                global last_data
                date = datetime.date.today()
                date = date - datetime.timedelta(days=1)
                data = database.read(date)
                if data is None:
                    return False
                # Filling parsed data into UI labels
                self.l_humidity_2.setText(f"{data['Humidity']}%")
                self.l_wind_speed_2.setText(f"{data['WindSpeed']} m/s")
                self.l_pressure_2.setText(f"{data['Pressure']}")
                self.l_uv_index_2.setText(f"{data['UVIndex']}")
                self.l_day_temp_2.setText(
                    f"{'+' if data['DayTemperature'] > 0 else ''}"
                    + f"{data['DayTemperature']}°"
                )
                self.l_night_temp_2.setText(
                    f"{'+' if data['NightTemperature'] > 0 else ''}"
                    + f"{data['NightTemperature']}°"
                )
                self.l_sunrise_2.setText(f"{data['SunriseTime']}")
                self.l_sunset_2.setText(f"{data['SunsetTime']}")

            def tda() -> None:
                """Fill two-days-ago's weather data into UI labels"""
                global last_data
                date = datetime.date.today()
                date = date - datetime.timedelta(days=2)
                data = database.read(date)
                if data is None:
                    return False
                # Filling parsed data into UI labels
                self.l_humidity.setText(f"{data['Humidity']}%")
                self.l_wind_speed.setText(f"{data['WindSpeed']} m/s")
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

            today()
            yesterday()
            tda()

        fill_data()

    def init_compare_sources(self) -> None:
        """Initialize the source comparison UI"""
        uic.loadUi(theme["compare_sources"], self)
        self.updateOneParserUI(self.parserBox)
        self.updateOneParserUI(self.parserBox_2)
        global parsers
        if len(parsers) > 0:
            self.updateCmpData1(0)
            self.parserBox.setCurrentIndex(0)
            if len(parsers) > 1:
                self.updateCmpData2(1)
                self.parserBox_2.setCurrentIndex(1)
            else:
                self.updateCmpData2(0)
                self.parserBox_2.setCurrentIndex(0)

        self.parserBox.currentIndexChanged.connect(self.updateCmpData1)
        self.parserBox_2.currentIndexChanged.connect(self.updateCmpData2)
        self.main_button.clicked.connect(self.init_main)

    def updateCmpData1(self, index) -> None:
        """Update data for first comparison box"""
        global parsers, currentParser
        currentParser = parsers[index]
        data = self.getData()
        if data is None:
            return False
        # Filling parsed data into UI labels
        self.l_temp.setText(
            f"{'+' if data['Temperature'] > 0 else ''}"
            + f"{data['Temperature']}°"
        )
        self.l_humidity.setText(f"{data['Humidity']}%")
        self.l_wind_speed.setText(f"{data['WindSpeed']} m/s")
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

    def updateCmpData2(self, index) -> None:
        """Update data for second comparison box"""
        global parsers, currentParser
        currentParser = parsers[index]
        data = self.getData()
        if data is None:
            return False
        # Filling parsed data into UI labels
        self.l_temp_2.setText(
            f"{'+' if data['Temperature'] > 0 else ''}"
            + f"{data['Temperature']}°"
        )
        self.l_humidity_2.setText(f"{data['Humidity']}%")
        self.l_wind_speed_2.setText(f"{data['WindSpeed']} m/s")
        self.l_pressure_2.setText(f"{data['Pressure']}")
        self.l_uv_index_2.setText(f"{data['UVIndex']}")
        self.l_day_temp_2.setText(
            f"{'+' if data['DayTemperature'] > 0 else ''}"
            + f"{data['DayTemperature']}°"
        )
        self.l_night_temp_2.setText(
            f"{'+' if data['NightTemperature'] > 0 else ''}"
            + f"{data['NightTemperature']}°"
        )
        self.l_sunrise_2.setText(f"{data['SunriseTime']}")
        self.l_sunset_2.setText(f"{data['SunsetTime']}")


# Program's entry point
# Creating application and window instances


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Windows()
    MainWindow.show()
    sys.exit(app.exec_())
