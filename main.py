import sys
from datetime import datetime, date
import pathlib
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

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


class Windows(QMainWindow):
    """Windows functionality"""
    def __init__(self):
        super().__init__()
        # Home window is main
        self.init_main()

    # Main window
    def init_main(self):
        """Loads gui of main window and connects buttons to functions"""
        uic.loadUi(theme["main"], self)

        def share():
            """Opens picture with info about weather"""
            from PIL import Image, ImageDraw, ImageFont
            # Opens icons
            clr = "_black" if theme == windows["light"] else ""
            images = f"{directory}\\ui\\images\\highres"
            humidity = Image.open(
                f"{images}\\drop{clr}.png").resize((100, 100))
            barometer = Image.open(
                f"{images}\\barometer{clr}.png").resize((100, 100))
            wind = Image.open(f"{images}\\wind{clr}.png").resize((100, 100))
            ultraviolet = Image.open(
                f"{images}\\ultraviolet{clr}.png").resize((100, 100))
            day = Image.open(
                f"{images}\\sunny{clr}.png").resize((100, 100))
            night = Image.open(
                f"{images}\\night-mode{clr}.png").resize((100, 100))
            sunrise = Image.open(
                f"{images}\\sunrise{clr}.png").resize((100, 100))
            sunset = Image.open(
                f"{images}\\sunset{clr}.png").resize(
                    (100, 100)).convert("RGBA")
            # Opens background
            background = Image.open(
                f"{directory}\\ui\\images\\\
{'' if theme == windows['dark'] else 'light/'}"
                + "share_background.jpeg").convert("RGBA")
            txt = Image.new("RGBA", background.size, (255, 255, 255, 0))
            font = ImageFont.truetype(
                f"{directory}\\ui\\Bahnschrift.ttf", 63)
            draw = ImageDraw.Draw(txt)
            textColor = (
                200, 200, 200, 255) if theme == windows["dark"] else (
                    0, 0, 0, 200)
            # Humidity
            background.paste(humidity, (20, 20), humidity)
            draw.text((150, 40), "007%", font=font, fill=textColor)
            # Barometer
            background.paste(barometer, (20, 175), barometer)
            draw.text((150, 195), "228", font=font, fill=textColor)
            # Wind
            background.paste(wind, (20, 330), wind)
            draw.text((150, 350), "1488", font=font, fill=textColor)
            # Ultraviolet
            background.paste(ultraviolet, (20, 485), ultraviolet)
            draw.text((150, 505), "1488", font=font, fill=textColor)
            # Day temp
            background.paste(day, (330, 330), day)
            draw.text((450, 350), "10°", font=font, fill=textColor)
            # Night temp
            background.paste(night, (630, 330), night)
            draw.text((740, 350), "10°", font=font, fill=textColor)
            # Sunrise time
            background.paste(sunrise, (330, 485), sunrise)
            draw.text((450, 505), "6:00", font=font, fill=textColor)
            # Sunset time
            background.paste(sunset, (630, 485), sunset)
            draw.text((740, 505), "19:00", font=font, fill=textColor)
            # Current time
            time = datetime.now()
            font = ImageFont.truetype(
                f"{directory}\\ui\\Bahnschrift.ttf", 30)
            draw.text(
                (800, 20), time.time().strftime("%H:%M"),
                font=font, fill=textColor)
            font = ImageFont.truetype(
                f"{directory}\\ui\\Bahnschrift.ttf", 200)
            temp = 0
            temp = f"{'+' if temp > 0 else ''}{temp}°"
            draw.text(
                (550 - len(str(temp)) * 30, 75), temp,
                font=font, fill=textColor)

            out = Image.alpha_composite(background, txt)
            out.show()

            humidity.close()
            barometer.close()
            wind.close()
            ultraviolet.close()
            day.close()
            night.close()
            sunrise.close()
            sunset.close()
            background.close()

        def buttons():
            self.setting_button.clicked.connect(self.init_settings)
            self.share_button.clicked.connect(share)
        buttons()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Windows()
    MainWindow.show()
    sys.exit(app.exec_())
