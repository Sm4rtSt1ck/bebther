from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class NoDataDialog(QDialog):
    """Dialog explaining why the data could not be parsed"""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sorry!")
        btn = QDialogButtonBox.Ok
        self.btn = QDialogButtonBox(btn)
        self.btn.clicked.connect(self.close)
        self.layout = QVBoxLayout()
        msg = QLabel(
            "Seems like we couldn't resolve data from selected source.\n"
            + "This often happens because the provider sets certain"
            + " limits on how many requests you can send a day.\n"
            + "Please, select a different source, "
            + "this one should become available soon"
            )
        self.layout.addWidget(msg)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)


class DBSavedDialog(QDialog):
    """Notification dialog about completing database operation"""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Done")
        btn = QDialogButtonBox.Ok
        self.btn = QDialogButtonBox(btn)
        self.btn.clicked.connect(self.close)
        self.layout = QVBoxLayout()
        msg = QLabel(
            "Current weather was saved to the database."
            )
        self.layout.addWidget(msg)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)


class DBFailDialog(QDialog):
    """Notification dialog about failing database operation"""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sorry!")
        btn = QDialogButtonBox.Ok
        self.btn = QDialogButtonBox(btn)
        self.btn.clicked.connect(self.close)
        self.layout = QVBoxLayout()
        msg = QLabel(
            "Couldn't save weather info to the database"
            )
        self.layout.addWidget(msg)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)


class ShareFailDialog(QDialog):
    """Notification dialog about failing share operation"""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Sorry!")
        btn = QDialogButtonBox.Ok
        self.btn = QDialogButtonBox(btn)
        self.btn.clicked.connect(self.close)
        self.layout = QVBoxLayout()
        msg = QLabel(
            "Can't share because there is no available data.\n"
            + "Please, change the weather source or update the data"
            )
        self.layout.addWidget(msg)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
