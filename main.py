import sys
import Parsers.accuweather as AccuWeather

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

isDebug = True
# References if the debug mode is enabled.
# Controls some behavior such as debug-outputs


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_main()
    
    def load_main(self):
        uic.loadUi("main.ui", self)
        self.setting_button.clicked.connect(self.load_settings)
    
    def load_settings(self):
        uic.loadUi("settings.ui", self)
        self.main_button.clicked.connect(self.load_main)
        self.autorun_on.clicked.connect(Settings.autorun_on)

    def updateData(self):
        data = AccuWeather.Parser.getData()
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
