from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from gui.theme import *
from gui.credential_dialog import CredentialDialog
class Credential:
    def __init__(
        self,
        service,
        username,
        ciphertext,
        nonce,
        created_at,
        updated_at,
        website
    ):
        self.service = service
        self.username = username
        self.ciphertext = ciphertext
        self.nonce = nonce
        self.created_at = created_at
        self.updated_at = updated_at
        self.website = website

class CredentialCard(QFrame):

    def __init__(self, credential, key):
        super().__init__()
        self.credential = credential
        self.key = key
        self.setFixedHeight(110)
        self.setObjectName("CredentialCard")   # <-- Put it here

        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(f"""
            QFrame#CredentialCard {{
                background-color: {PANEL};
                border: 1px solid {BORDER};
                border-radius: {RADIUS}px;
            }}

            QFrame#CredentialCard:hover {{
                background-color: {PANEL_LIGHT};
                border: 1px solid {ACCENT};
            }}

            QLabel {{
                background: transparent;
                border: none;
            }}
        """)


        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 10, 18, 10)


        
        # Title
        self.title_label = QLabel(self.credential.service)
        self.title_label.setFont(HEADING_FONT)

        
        # Website
        self.website_label = QLabel(self.credential.website)
        self.website_label.setFont(BODY_FONT)
        self.website_label.setStyleSheet(f"color: {TEXT_DIM};")


        # Last Updated
        self.updated_label = QLabel(f"Updated {self.credential.updated_at.strftime('%b %d, %Y')}")
        self.updated_label.setFont(LABEL_FONT)
        self.updated_label.setAlignment(Qt.AlignRight)
        self.updated_label.setStyleSheet(f"color: {TEXT_DIM};")



        layout.addWidget(self.title_label)
        layout.addWidget(self.website_label)

        layout.addSpacing(4)
        layout.addStretch()

        layout.addWidget(self.updated_label)

    def mousePressEvent(self, event):
        dialog = CredentialDialog(self.credential, self.key)
        dialog.exec()