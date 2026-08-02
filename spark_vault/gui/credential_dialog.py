from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QMenu
)
from PySide6.QtCore import Qt
from spark_vault.gui.theme import *
from spark_vault.encryption.decrypt import *
from spark_vault.gui.widgets import *
import qtawesome as qta
from spark_vault.gui.delete_confirmation_dialog import DeleteConfirmationDialog
from spark_vault.gui.edit_credential_dialog import EditCredentialDialog
from spark_vault.database.credentials import edit_credentials

class CredentialDialog(QDialog):
    
    def __init__(self, user, credential, key):
        
        super().__init__()
        self.delete_requested = False
        self.edit_requested = False
        self.user = user
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
        

        button_layout = QHBoxLayout()

        self.delete_button = DangerButton("Delete")
        self.delete_button.clicked.connect(self.delete)

        self.edit_button = SecondaryButton("Edit")
        self.edit_button.clicked.connect(self.edit)
        self.close_button = SecondaryButton("Close")


        self.close_button.setDefault(True)
        self.close_button.clicked.connect(self.accept)
        #self.edit_button.clicked.connect(self.enable_edit_mode)



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

        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.edit_button)
        button_layout.setSpacing(12)
        button_layout.addWidget(self.close_button)
        

        main_layout.addLayout(button_layout)

    def toggle_password(self):
        if self.password_visible:
            self.password.setText("••••••••••••••••")
            self.show_button.setIcon(qta.icon("fa6s.eye-slash"))
            self.password_visible = False
        else:
            self.password.setText(self.plaintext_password)
            self.show_button.setIcon(qta.icon("fa6s.eye"))
            self.password_visible = True


    def delete(self):
        dialog = DeleteConfirmationDialog(self.credential.service)

        if dialog.exec():
            self.delete_requested = True
            self.accept()

    def edit(self):
        dialog = EditCredentialDialog(self.credential, self.key)

        if dialog.exec():
            edit_credentials(
                self.user,
                self.key,
                self.credential.credential_id,
                dialog.service.text().strip(),
                dialog.username.text().strip(),
                dialog.password.text(),
                dialog.website.text().strip(),
            )
            self.edit_requested = True
            self.accept()


