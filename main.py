import sys
from os import walk
import Parsers

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

isDebug = True
# References if the debug mode is enabled.
# Controls some behavior such as debug-outputs
currentParser = None
parsers = list()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("test.ui", self)
        self.fetchParsers()
        global parsers
        global currentParser
        if len(parsers) > 0:
            currentParser = parsers[0]
        self.updateData()

    def fetchParsers(self) -> None:
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

    def updateData(self) -> None:
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
