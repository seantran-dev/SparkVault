from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QLabel,
    QPushButton,
    QDialog,
    QToolButton,
    QMenu
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation, Signal
from PySide6.QtGui import QAction

from gui.widgets import *
from gui.theme import *
from gui.credential_card import CredentialCard, Credential
from gui.credential_dialog import CredentialDialog
from gui.widgets import ToolbarButton
from gui.add_credential_dialog import AddCredentialDialog
from database.settings import *
from database.credentials import delete_credential as db_delete_credential
from gui.account_dialog import AccountDialog
import qtawesome as qta

from database.settings import *


class DashboardPage(QWidget):
    logout_requested = Signal()

    def __init__(self, user, key):
        super().__init__()
        self.user = user
        self.key = key

        self.setWindowTitle("SparkVault")
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

        # Header

        header_layout = QHBoxLayout()

        self.title = QLabel("SparkVault")
        self.title.setFont(HEADING_FONT)

        self.account_button = QPushButton("Account")
        self.account_button.clicked.connect(self.open_account_dialog)
        self.settings_button = QPushButton("Settings")
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout_requested.emit)

        for button in [self.account_button, self.settings_button, self.logout_button]:
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
        header_layout.addWidget(self.account_button)
        # header_layout.addWidget(self.settings_button)
        header_layout.addWidget(self.logout_button)

        #
        # Toolbar
        #

        toolbar_layout = QHBoxLayout()

        # Search bar
        self.search_box = SearchBox("Search credentials...")
        self.search_box.sort_button.clicked.connect(self.show_sort_menu)
        self.search_box.textChanged.connect(self.refresh_credentials)
        
        # Add new credential
        self.add_button = ToolbarButton("Add", None, primary=True)


        #self.search_box.addAction(sort_action, QLineEdit.TrailingPosition)



        self.add_button.setFixedWidth(TOOLBAR_ADD_BUTTON_WIDTH)
        self.add_button.setFixedHeight(TOOLBAR_ADD_BUTTON_HEIGHT)

        toolbar_layout.addWidget(self.search_box)
        toolbar_layout.addWidget(self.add_button)
        
        self.add_button.clicked.connect(self.add_credential)

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
        
        self.refresh_credentials()

        main_layout.addLayout(header_layout)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.scroll_area)

    def open_account_dialog(self):
        dialog = AccountDialog(self.user, self.key)
        if dialog.exec():
            self.user = dialog.user
            self.key = dialog.key

    def show_sort_menu(self):
        menu = QMenu(self)

        menu = QMenu(self)

        menu.setStyleSheet(f"""
        QMenu {{
            background-color: {PANEL};
            color: {TEXT};
            border: 1px solid {BORDER};
            padding: 4px;
        }}

        QMenu::item {{
            padding: 8px 20px;
            border-radius: 4px;
        }}

        QMenu::item:selected {{
            background-color: {ACCENT};
            color: black;
        }}

        QMenu::separator {{
            height: 1px;
            background: {BORDER};
            margin: 4px 8px;
        }}
        """)

        az = menu.addAction("A → Z")
        za = menu.addAction("Z → A")
        menu.addSeparator()

        new_created = menu.addAction("Newest Created")
        old_created = menu.addAction("Oldest Created")
        menu.addSeparator()

        recent_updated = menu.addAction("Recently Updated")
        old_updated = menu.addAction("Least Recently Updated")

        actions = {
            az: "SERVICE_ASC",
            za: "SERVICE_DESC",
            new_created: "CREATED_DESC",
            old_created: "CREATED_ASC",
            recent_updated: "UPDATED_DESC",
            old_updated: "UPDATED_ASC",
        }
        user_settings = load_user_settings(self.user[0])
        # Show checkmark for current selection
        for action, value in actions.items():
            action.setCheckable(True)
            action.setChecked(value == user_settings[4])


        action = menu.exec(
            self.search_box.sort_button.mapToGlobal(
                self.search_box.sort_button.rect().bottomLeft()
            )
        )

        if action in actions:
            update_setting(self.user[0], "default_sort", actions[action])
            self.refresh_credentials()

    def search_credentials(self, credentials):
        query = self.search_box.text().strip().lower()
        
        if not query:
            return credentials

        return [
            credential
            for credential in credentials
            if (
                query in (credential[2] or "").lower()
                or query in (credential[3] or "").lower()
                or query in (credential[8] or "").lower()
            )
        ]

    def refresh_credentials(self):

        settings = load_user_settings(self.user[0])
        sort = settings[4]

        credentials = get_credentials(self.user)

        while self.credentials_layout.count() > 1:
            item = self.credentials_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()


        if not credentials:
            empty = SubtitleLabel('Click "Add" to store a new credential.')
            empty.setAlignment(Qt.AlignCenter)
            self.credentials_layout.insertWidget(
                self.credentials_layout.count() - 1,
                empty
            )
            return
        
        searched_credentials = self.search_credentials(credentials)
        credentials = self.sort_credentials(searched_credentials, sort)

        for row in credentials:
            credential = Credential(
                credential_id=row[0],
                user_id=row[1],
                service=row[2],
                username=row[3],
                ciphertext=row[4],
                nonce=row[5],
                created_at=row[6],
                updated_at=row[7],
                website=row[8]
            )

            card = CredentialCard(self.user, credential, self.key)
            card.delete_requested.connect(self.delete_credential)
            card.edit_requested.connect(self.refresh_credentials)
            self.credentials_layout.insertWidget(
                self.credentials_layout.count() - 1,
                card
            )

    def delete_credential(self, credential_id):
        db_delete_credential(self.user[0], credential_id)
        self.refresh_credentials()

    def sort_credentials(self, credentials, sort):
                if sort == "SERVICE_ASC":
                    credentials.sort(key=lambda c: c[2].lower())
        
                elif sort == "SERVICE_DESC":
                    credentials.sort(key=lambda c: c[2].lower(), reverse=True)
        
                elif sort == "CREATED_DESC":
                    credentials.sort(key=lambda c: c[6], reverse=True)
        
                elif sort == "CREATED_ASC":
                    credentials.sort(key=lambda c: c[6])
        
                elif sort == "UPDATED_DESC":
                    credentials.sort(key=lambda c: c[7], reverse=True)
        
                elif sort == "UPDATED_ASC":
                    credentials.sort(key=lambda c: c[7])
        
                return credentials
    
    def add_credential(self):

        dialog = AddCredentialDialog()

        if dialog.exec():

            service = dialog.service.text().strip()
            username = dialog.username.text().strip()
            password = dialog.password.text()
            website = dialog.website.text().strip()

            add_credentials(
                self.user,
                service,
                username,
                password,
                website,
                self.key
            )

            self.refresh_credentials()

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
