from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QFrame
)

from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation
from gui.theme import *
from gui.widgets import *
from authentication.login import *
import sys



class LoginPage(QWidget):
    login_successful = Signal(object, object)
    show_create_account = Signal()
    
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(120, 60, 120, 60)
        layout.setSpacing(18)
        layout.addStretch()
        layout.addWidget(
            TitleLabel("SecureDB")
        )

        layout.addWidget(
            SubtitleLabel("Encrypted Password Vault")
        )
        
        layout.addSpacing(30)

        self.progress = QProgressBar()

        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setFixedHeight(3)
        self.progress.hide()
        self.progress.setStyleSheet(f"""
        QProgressBar {{
            border: none;
            background: {PANEL};
        }}

        QProgressBar::chunk {{
            background: {ACCENT};
        }}
        """)

        self.username = CyberTextBox("Username")

        self.password = CyberTextBox("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addWidget(self.username)
        layout.addWidget(self.password)

        layout.addSpacing(15)

        self.login_button = CyberButton("Unlock Vault")
        self.status = SubtitleLabel("")
        self.status.setAlignment(Qt.AlignCenter)

        

        self.login_button.clicked.connect(self.handle_login)
        self.username.returnPressed.connect(self.handle_login)
        self.password.returnPressed.connect(self.handle_login)
        
        self.create_account = LinkLabel(
            'Don\'t have an account? <a href="#">Create Account</a>'
        )
        self.create_account.clicked.connect(self.show_create_account.emit)

        layout.addWidget(self.login_button)
        layout.addWidget(self.status)

        self.unlock_container = QWidget()
        self.unlock_container.setFixedHeight(3)

        container_layout = QHBoxLayout(self.unlock_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.unlock_line = QFrame()
        self.unlock_line.setMaximumWidth(0)
        self.unlock_line.setFixedHeight(3)

        self.unlock_line.setStyleSheet(f"""
        QFrame {{
            background: {ACCENT};
            border-radius: 1px;
        }}
        """)

        container_layout.addWidget(self.unlock_line)
        container_layout.addStretch()

        self.unlock_container.hide()

        layout.addWidget(self.unlock_container)
        layout.addWidget(self.create_account)

        layout.addStretch()

    def handle_login(self):

        username = self.username.text().strip()
        password = self.password.text()

        user, key = login(username, password)

        if user is None:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password."
            )
            return

        self.login_success(user, key)

    def login_success(self, user, key):
        self.login_button.setEnabled(False)
        self.login_button.setText("Signing In...")

        QTimer.singleShot(
            250,
            lambda: self.start_unlock(user, key)
        )

    def reset(self):
        self.login_button.setEnabled(True)
        self.login_button.setText("Unlock Vault")
        self.login_button.set_progress(0)

        self.status.setText("")

        self.username.clear()
        self.password.clear()
        self.username.setFocus()

    def start_unlock(self, user, key):

        self.login_button.setEnabled(False)
        self.login_button.setText("Unlocking...")

        self.status.setText("Decrypting encrypted vault...")

        self.user = user
        self.key = key

        self.value = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advance_unlock)
        self.timer.start(14)

    def advance_unlock(self):

        if self.value < 50:
            increment = 1.0 + self.value / 20
        else:
            remaining = 100 - self.value
            increment = max(0.5, remaining * 0.08)

        self.value += increment

        if self.value >= 99.5:
            self.value = 100
            self.login_button.set_progress(100)

            self.timer.stop()

            QTimer.singleShot(
                150,
                lambda: self.login_successful.emit(
                    self.user,
                    self.key
                )
            )
        else:
            self.login_button.set_progress(int(self.value))
