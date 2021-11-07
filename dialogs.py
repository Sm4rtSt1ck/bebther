from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel


class NoDataDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Ooops...")
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
