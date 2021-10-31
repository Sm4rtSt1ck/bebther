import sys
from typing import MutableMapping

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


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
        self.autorun_on.clicked.connect(Settings.autorun)


class Settings:
    def autorun(self):
        print("Bebra")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())