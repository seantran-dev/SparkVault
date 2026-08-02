from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)

from spark_vault.gui.widgets import *
from spark_vault.gui.theme import *


class AddCredentialDialog(QDialog):

    def __init__(self, credential=None):
        super().__init__()

        self.credential = credential

        self.setWindowTitle(
            "Add Credential" if credential is None else "Edit Credential"
        )
        self.resize(500, 350)

        self.setStyleSheet(f"""
            QDialog {{
                background: {BACKGROUND};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        title = TitleLabel(
            "Add Credential"
            if credential is None
            else "Edit Credential"
        )
    
        self.service = CyberTextBox("Service (Required)")
        self.username = CyberTextBox("Username")
        self.password = CyberTextBox("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.website = CyberTextBox("Website")

        # If editing, pre-fill the fields
        if credential is not None:
            self.service.setText(credential.service)
            self.username.setText(credential.username)
            self.website.setText(credential.website)

            # Password can be filled later once you decrypt it.
            # self.password.setText(...)

        button_layout = QHBoxLayout()

        self.cancel_button = CyberButton("Cancel")
        self.save_button = CyberButton(
            "Save"
            if credential is None
            else "Save Changes"
        )
        self.status_label = QLabel("")
        self.status_label.setFont(BODY_FONT)
        self.status_label.setStyleSheet(f"""
            color: {ERROR};
            font-size: 16pt;
        """)
        self.save_button.setDefault(True)
        self.save_button.setAutoDefault(True)

        self.cancel_button.setDefault(False)
        self.cancel_button.setAutoDefault(False)

        button_layout = QHBoxLayout()


        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.save)
        self.service.textChanged.connect(self.clear_status)
        

        button_layout.addWidget(self.status_label)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        main_layout.addWidget(title)
        main_layout.addWidget(self.service)
        main_layout.addWidget(self.username)
        main_layout.addWidget(self.password)
        main_layout.addWidget(self.website)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def save(self):
        if not self.service.text().strip():
            self.status_label.setText("Service is required.")
            return

        self.accept()

    def clear_status(self):
        self.status_label.clear()