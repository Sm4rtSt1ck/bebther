import sys
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
