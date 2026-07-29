from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Qt
from gui.theme import *
from encryption.decrypt import *
import qtawesome as qta

class CredentialDialog(QDialog):

    def __init__(self, credential, key):
        super().__init__()

        self.credential = credential
        self.key = key

        self.plaintext_password = decrypt_password(key, self.credential.ciphertext, self.credential.nonce)

        self.setWindowTitle("Credential")
        self.resize(500, 550)

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BACKGROUND};
            }}

            QLabel {{
                background: transparent;
                color: {TEXT};
            }}
            QPushButton {{
                background-color: {PANEL_LIGHT};
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 4px;
            }}

            QPushButton:hover {{
                border: 1px solid #00FF66;
            }}

            QPushButton:pressed {{
                background-color: #252525;
                border: 1px solid #00FF66;
            }}
        """)
        
        # Main Layout
        
        self.title_label = QLabel(self.credential.service)
        self.title_label.setFont(TITLE_FONT)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(30)

        website_layout = QVBoxLayout()
        website_layout.setSpacing(6)

        website_heading = QLabel("Website")
        website_heading.setFont(LABEL_FONT)
        website_heading.setStyleSheet(f"color: {TEXT_DIM};")

        website = QLabel(self.credential.website)
        website.setFont(BODY_FONT)
        
        website_layout.addWidget(website_heading)
        website_layout.addWidget(website)

        # Username

        username_layout = QVBoxLayout()
        username_layout.setSpacing(6)

        username_heading = QLabel("Username")
        username_heading.setFont(LABEL_FONT)
        username_heading.setStyleSheet(f"color: {TEXT_DIM};")

        username = QLabel(self.credential.username)
        username.setFont(BODY_FONT)

        username_layout.addWidget(username_heading)
        username_layout.addWidget(username)

        # Password Section

        password_layout = QVBoxLayout()
        password_layout.setSpacing(2)

        password_heading = QLabel("Password")
        password_heading.setFont(LABEL_FONT)
        password_heading.setStyleSheet(f"color: {TEXT_DIM};")

        password_row = QHBoxLayout()
        password_row.setSpacing(10)

        self.password = QLabel("••••••••••••••••")
        self.password.setFont(BODY_FONT)
        self.password_visible = False

        self.show_button = QPushButton("")
        self.show_button.setIcon(qta.icon("fa6s.eye-slash"))
        self.show_button.setFixedSize(32, 32)
        self.show_button.clicked.connect(self.toggle_password)
        self.show_button.setFocusPolicy(Qt.NoFocus)

        copy_button = QPushButton("")
        copy_button.setIcon(qta.icon("fa6s.copy"))
        copy_button.setFixedSize(32, 32)
        copy_button.setFocusPolicy(Qt.NoFocus)
        

        
        
        password_row.addWidget(self.password)

        password_row.addStretch()

        password_row.addWidget(self.show_button)
        password_row.addWidget(copy_button)

        password_layout.addWidget(password_heading)
        password_layout.addLayout(password_row)

        

        main_layout.addWidget(self.title_label)
        main_layout.addLayout(website_layout)
        main_layout.addLayout(username_layout)
        main_layout.addLayout(password_layout)
        main_layout.addStretch()

    def toggle_password(self):
        if self.password_visible:
            self.password.setText("••••••••••••••••")
            self.show_button.setIcon(qta.icon("fa6s.eye-slash"))
            self.password_visible = False
        else:
            self.password.setText(self.plaintext_password)
            self.show_button.setIcon(qta.icon("fa6s.eye"))
            self.password_visible = True