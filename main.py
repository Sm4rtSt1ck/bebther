import sys
from os import walk

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

isDebug = True
# References if the debug mode is enabled.
# Controls some behavior such as debug-outputs
currentParser = None  # Contains instance of the selected Parser object
parsers = list()  # List of all available parsers


def debug(value):
    """Modified print method. Prints value if the debug mode is enabled"""
    if isDebug:
        if type(value) == list or type(value) == dict:
            print("[DEBUG]: ", end='')
            print(*value)
        else:
            print(f"[DEBUG]: {value}")


class MainWindow(QMainWindow):
    """Main program class.
    Contains UI and workflow functions"""
    def __init__(self):
        """UI Initialization"""
        super().__init__()
        # Initial setup
        self.load_main()
        self.updateParsers()
        global parsers
        global currentParser
        if len(parsers) > 0:
            currentParser = parsers[0]
        self.updateData()

    def load_main(self):
        """Loading main UI window and assigning buttons"""
        uic.loadUi("main.ui", self)
        self.setting_button.clicked.connect(self.load_settings)
        self.setting_button_3.clicked.connect(self.toggleParser)

    def load_settings(self):
        """Loading settings windows and assigning buttons"""
        uic.loadUi("settings.ui", self)
        self.main_button.clicked.connect(self.load_main)
        self.autorun_on.clicked.connect(Settings.autorun_on)

    def toggleParser(self) -> None:
        """Switching to the next available parser"""
        global parsers, currentParser
        if parsers.index(currentParser) + 1 < len(parsers):
            currentParser = parsers[parsers.index(currentParser) + 1]
        else:
            currentParser = parsers[0]
        # Setting the weather source button's text
        self.setting_button_3.setText(currentParser.name)

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
        global currentParser
        if currentParser is None:
            return None
        # Getting the parsed data
        data = currentParser.getData()
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


class Settings:
    """Settings UI window workflow"""
    def autorun_on(self):
        """Add the application to autorun"""
        pass

    def autorun_off(self):
        """Remove the application from autorun"""
        pass

    def theme_light(self):
        """Switch UI to light color scheme"""
        pass

    def theme_dark(self):
        """Switch UI to dark color scheme"""
        pass


# Program's entry point
# Creating application and window instances

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
