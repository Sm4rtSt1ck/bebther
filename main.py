import sys
from os import walk
from types import CoroutineType
from xml.etree.ElementTree import parse
import Parsers

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

isDebug = True
# References if the debug mode is enabled.
# Controls some behavior such as debug-outputs
currentParser = None
parsers = list()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.updateData()
        self.load_main()
        self.fetchParsers()
        global parsers
        global currentParser
        if len(parsers) > 0:
            currentParser = parsers[0]

    def load_main(self):
        uic.loadUi("main.ui", self)
        self.setting_button.clicked.connect(self.load_settings)
        self.setting_button_3.clicked.connect(self.toggleParser)

    def load_settings(self):
        uic.loadUi("settings.ui", self)
        self.main_button.clicked.connect(self.load_main)
        self.autorun_on.clicked.connect(Settings.autorun_on)

    def toggleParser(self) -> None:
        global parsers, currentParser
        if parsers.index(currentParser) + 1 < len(parsers):
            currentParser = parsers[parsers.index(currentParser) + 1]
        else:
            currentParser = parsers[0]
        self.setting_button_3.setText(currentParser.name)

    def fetchParsers(self):
        files = list()
        for(dirpath, dirname, filenames) in walk("./Parsers/"):
            files.append(filenames)
            break
        print(*files)
        filenames.remove("baseParser.py")
        result = list()
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
        global currentParser
        if currentParser is None:
            return None
        data = currentParser.getData()
        print(*data if data is not None else "NO WEATHER")
        if data is not None:
            self.l_temp.setText(
                f"{'+' if data['Temperature'] > 0 else ''}"
                + f"{data['Temperature']}°"
            )
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
            print(data["Temperature"])


class Settings:
    def autorun_on(self):
        pass

    def autorun_off(self):
        pass

    def theme_light(self):
        pass

    def theme_dark(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
