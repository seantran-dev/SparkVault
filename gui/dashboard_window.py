from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QLabel,
    QPushButton
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation, Signal

from gui.widgets import *
from gui.theme import *
from gui.credential_card import CredentialCard, Credential
from gui.credential_dialog import CredentialDialog
from database.credentials import *

import qtawesome as qta


class DashboardPage(QWidget):
    logout_requested = Signal()

    def __init__(self, user, key):
        super().__init__()
        self.user = user
        self.key = key

        self.setWindowTitle("SecureDB")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.setStyleSheet(f"""
            QWidget {{
                background:{BACKGROUND};
                color:{TEXT};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        #
        # Header
        #

        header_layout = QHBoxLayout()

        self.title = QLabel("SecureDB")
        self.title.setFont(HEADING_FONT)

        self.settings_button = QPushButton("Settings")
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout_requested.emit)

        for button in [self.settings_button, self.logout_button]:
            button.setFont(BODY_FONT)
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {TEXT_DIM};
                    border: none;
                    padding: 6px 12px;
                }}

                QPushButton:hover {{
                    color: {ACCENT};
                }}

                QPushButton:pressed {{
                    color: {TEXT};
                }}
            """)

        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_button)
        header_layout.addWidget(self.logout_button)

        #
        # Toolbar
        #

        toolbar_layout = QHBoxLayout()

        self.search_box = CyberTextBox("Search credentials...")
        self.add_button = CyberButton("+ Add Credential")

        toolbar_layout.addWidget(self.search_box)
        toolbar_layout.addWidget(self.add_button)

        # Scroll Function and Smoothening
        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.NoFrame)
        self.scroll_area.verticalScrollBar().setStyleSheet(SCROLLBAR_STYLE)
        

        self.container = QWidget()

        self.credentials_layout = QVBoxLayout(self.container)
        self.credentials_layout.setSpacing(12)
        self.credentials_layout.addStretch()

        self.scroll_area.setWidget(self.container)

        credentials = get_credentials(self.user)

        cards = []
        for row in credentials:
            credential = Credential(
                service = row[2], # service
                username = row[3], # username
                ciphertext = row[4], # ciphertext
                nonce = row[5], # once
                created_at = row[6], # created at datetime
                updated_at = row[7], # updated at datetime
                website = row[8], # website
            )
            card = CredentialCard(credential, key)
            cards.append(card)
        
        for card in cards:
            self.credentials_layout.insertWidget(
                self.credentials_layout.count() - 1,
                card
            )

        main_layout.addLayout(header_layout)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.scroll_area)

        

    def logout(self):
        from gui.login_window import LoginWindow

        self.login_window = LoginWindow()
        self.login_window.show()

        self.close()

class SmoothScrollArea(QScrollArea):

    def __init__(self):
        super().__init__()

        self.animation = QPropertyAnimation(
            self.verticalScrollBar(),
            b"value"
        )

        self.animation.setDuration(180)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def wheelEvent(self, event):
        bar = self.verticalScrollBar()

        step = 122

        if self.animation.state() == QAbstractAnimation.Running:
            start = self.animation.endValue()
        else:
            start = bar.value()

        target = start - (event.angleDelta().y() / 120) * step

        target = max(bar.minimum(), min(target, bar.maximum()))

        self.animation.stop()
        self.animation.setStartValue(bar.value())
        self.animation.setEndValue(target)
        self.animation.start()