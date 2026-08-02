from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
)

from spark_vault.gui.widgets import *
from spark_vault.gui.theme import *
from spark_vault.encryption.decrypt import decrypt_password


class EditCredentialDialog(QDialog):

    def __init__(self, credential, key):
        super().__init__()

        self.credential = credential
        self.key = key

        self.setWindowTitle("Edit Credential")
        self.resize(500, 550)

        self.setStyleSheet(f"""
            QDialog {{
                background: {BACKGROUND};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        title = TitleLabel("Edit Credential")

        self.service = CyberTextBox("Service (Required)")
        self.username = CyberTextBox("Username")
        self.password = CyberTextBox("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.website = CyberTextBox("Website")


        service_label = QLabel("Service")
        service_label.setFont(LABEL_FONT)
        service_label.setStyleSheet(f"color: {TEXT_DIM};")

        username_label = QLabel("Username")
        username_label.setFont(LABEL_FONT)
        username_label.setStyleSheet(f"color: {TEXT_DIM};")

        password_label = QLabel("Password")
        password_label.setFont(LABEL_FONT)
        password_label.setStyleSheet(f"color: {TEXT_DIM};")

        website_label = QLabel("Website")
        website_label.setFont(LABEL_FONT)
        website_label.setStyleSheet(f"color: {TEXT_DIM};")

        # Pre-fill fields
        self.service.setText(credential.service)
        self.username.setText(credential.username)
        self.website.setText(credential.website)

        self.password.setText(
            decrypt_password(
                key,
                credential.ciphertext,
                credential.nonce
            )
        )

        self.status_label = QLabel("")
        self.status_label.setFont(BODY_FONT)
        self.status_label.setStyleSheet(f"""
            color: {ERROR};
            font-size: 16pt;
        """)

        self.cancel_button = CyberButton("Cancel")
        self.save_button = CyberButton("Save Changes")

        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.save)
        self.service.textChanged.connect(self.clear_status)
        
        self.save_button.setDefault(True)
        self.save_button.setAutoDefault(True)

        self.cancel_button.setDefault(False)
        self.cancel_button.setAutoDefault(False)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.status_label)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        main_layout.addWidget(title)
        main_layout.addWidget(service_label)
        main_layout.addWidget(self.service)
        
        main_layout.addWidget(website_label)
        main_layout.addWidget(self.website)

        main_layout.addWidget(username_label)
        main_layout.addWidget(self.username)

        main_layout.addWidget(password_label)
        main_layout.addWidget(self.password)

        
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def save(self):
        if not self.service.text().strip():
            self.status_label.setText("Service is required.")
            return

        self.accept()

    def clear_status(self):
        self.status_label.clear()