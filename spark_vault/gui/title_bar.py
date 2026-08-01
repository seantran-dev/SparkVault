from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

class TitleBar(QWidget):
    def __init__(self):
        super().__init__()

        self.title = QLabel("SecureDB")

        self.minimize = QPushButton("—")
        self.maximize = QPushButton("□")
        self.close = QPushButton("✕")

        layout = QHBoxLayout(self)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.minimize)
        layout.addWidget(self.maximize)
        layout.addWidget(self.close)