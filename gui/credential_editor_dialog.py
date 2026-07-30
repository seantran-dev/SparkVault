from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)

from gui.widgets import *
from gui.theme import *


class CredentialEditorDialog(QDialog):

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

        self.service = CyberTextBox("Service")
        self.username = CyberTextBox("Username")
        self.password = CyberTextBox("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.website = CyberTextBox("Website (Optional)")

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

        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.accept)

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