from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
)

from spark_vault.gui.widgets import CyberButton, LinkLabel
from spark_vault.gui.theme import *
from spark_vault.authentication.register import register
from spark_vault.database.users import *

class CreateAccountPage(QWidget):

    account_created = Signal()
    back_requested = Signal()

    def __init__(self):
        super().__init__()

        title = QLabel("Create SecureDB Account")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(TITLE_FONT)
        title.setStyleSheet(f"color:{ACCENT};")

        subtitle = QLabel("Create a new encrypted vault.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(BODY_FONT)
        subtitle.setStyleSheet(f"color:{TEXT_DIM};")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Master Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Confirm Password")
        self.confirm.setEchoMode(QLineEdit.Password)

        for box in (self.username, self.password, self.confirm):
            box.setFont(BODY_FONT)
            box.setFixedHeight(42)

            box.setStyleSheet(f"""
                QLineEdit {{
                    background:{PANEL};
                    color:{TEXT};
                    border:2px solid {BORDER};
                    border-radius:8px;
                    padding-left:12px;
                }}

                QLineEdit:focus {{
                    border:2px solid {ACCENT};
                }}
            """)

        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(BODY_FONT)
        self.status.setStyleSheet(f"color:{ACCENT};")

        self.create_button = CyberButton("Create Account")

        self.back = LinkLabel(
            'Already have an account? <a href="#">Login</a>'
        )
        self.back.clicked.connect(self.back_requested.emit)
        

        self.create_button.clicked.connect(self.create_account)
        self.username.returnPressed.connect(self.create_account)
        self.password.returnPressed.connect(self.create_account)
        self.confirm.returnPressed.connect(self.create_account)

        self.username.textChanged.connect(self.clear_status)
        self.password.textChanged.connect(self.clear_status)
        self.confirm.textChanged.connect(self.clear_status)

        self.username.editingFinished.connect(self.check_username)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(150, 80, 150, 80)
        layout.setSpacing(18)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.confirm)

        
        layout.addSpacing(0)
        layout.addWidget(self.create_button)
        layout.addWidget(self.status)
        layout.addWidget(self.back)

        layout.addStretch()

    def check_username(self):
        username = self.username.text().strip()

        if not username:
            self.status.clear()
            return

        if get_user(username) is not None:
            self.status.setStyleSheet(f"color: {ERROR};")
            self.status.setText("Username is already taken.")
        else:
            self.status.setStyleSheet(f"color: {ACCENT};")
            self.status.setText("Username is available.")

    def create_account(self):

        username = self.username.text().strip()
        password = self.password.text()
        confirm = self.confirm.text()

        if not username:
            self.status.setText("Please enter a username.")
            return
        elif get_user(username) is not None:
            self.status.setStyleSheet(f"""color: {ERROR};""")
            self.status.setText("Username is already taken.")
            return
        
        if not password:
            self.status.setStyleSheet(f"""color: {ACCENT};""")
            self.status.setText("Please enter a password.")
            return
        elif not confirm:
            self.status.setStyleSheet(f"""color: {ACCENT};""")
            self.status.setText("Please confirm your password.")
            return
        if password != confirm:
            self.status.setStyleSheet(f"""color: {ERROR};""")
            self.status.setText("Passwords do not match.")
            return

        
        
        register(username, "", password)

        self.account_created.emit()
        
            
    def clear_status(self):
        self.status.clear()

    def reset(self):

        self.username.clear()
        self.password.clear()
        self.confirm.clear()
        self.status.clear()

