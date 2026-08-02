from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QStackedLayout,
    QPushButton,
)


from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt
import qtawesome as qta

from spark_vault.gui.theme import *
from spark_vault.gui.widgets import *
from spark_vault.database.users import update_username, get_user, update_user_password

class AccountDialog(QDialog):

    def __init__(self, user, key):
        super().__init__()
        self.user = user
        self.key = key
        self.username = user[1]

        self.setup_window()
        self.setup_stack()

        self.build_account_page()
        self.build_username_page()
        self.build_password_page()

        self.show_account_page()

    def setup_window(self):

        self.setWindowTitle("Account")
        self.resize(600, 500)

        self.setStyleSheet(f"""
            QDialog {{
                background: {BACKGROUND};
            }}

            QLabel {{
                background: transparent;
                color: {TEXT};
            }}

            QPushButton {{
                background: {PANEL_LIGHT};
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 4px;
            }}

            QPushButton:hover {{
                border: 1px solid {ACCENT};
            }}
        """)

    def setup_stack(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            25, 25, 25, 25
        )

        self.stack = QStackedLayout()

        self.main_layout.addLayout(self.stack)
    
    # helper
    def create_label(self, text):
        label = QLabel(text)
        label.setFont(LABEL_FONT)
        label.setStyleSheet(f"color: {TEXT_DIM};")
        return label

    def create_readonly_box(self, text):
        box = CyberTextBox("")
        box.setText(text)
        box.setReadOnly(True)
        return box

    def build_account_page(self):

        self.account_page = QWidget()

        layout = QVBoxLayout(self.account_page)
        layout.setSpacing(18)

        # Title      
        title = TitleLabel("Your Account")

        # Username
        username_label = self.create_label("Username")
        username_row = QHBoxLayout()

        self.username_box = self.create_readonly_box(self.username)

        self.edit_username_button = SecondaryButton("Edit")
        self.edit_username_button.setFixedWidth(90)

        self.edit_username_button.clicked.connect(self.show_username_page)

        username_row.addWidget(self.username_box)
        username_row.addWidget(self.edit_username_button)

        # Password
        password_label = self.create_label("Password")
        password_row = QHBoxLayout()
        self.password_box = self.create_readonly_box("••••••••••••••••")

        self.edit_password_button = SecondaryButton("Edit")
        self.edit_password_button.setFixedWidth(90)

        self.edit_password_button.clicked.connect(self.show_password_page)

        password_row.addWidget(self.password_box)
        password_row.addWidget(self.edit_password_button)

        # Button

        self.account_status = QLabel("")
        self.account_status.setFont(BODY_FONT)
        self.account_status.setStyleSheet(f"""
            color: {ACCENT};
        """)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.account_status)
        button_layout.addStretch()
        self.close_button = SecondaryButton("Close")
        self.close_button.clicked.connect(self.reject)
        self.close_button.setDefault(True)
        self.close_button.setAutoDefault(True)
        self.edit_username_button.setDefault(False)
        self.edit_username_button.setAutoDefault(False)
        self.edit_password_button.setDefault(False)
        self.edit_password_button.setAutoDefault(False)


        button_layout.addWidget(self.close_button)

        

        
        # Layout
        layout.addWidget(title)

        layout.addSpacing(10)

        layout.addWidget(username_label)
        layout.addLayout(username_row)

        layout.addWidget(password_label)
        layout.addLayout(password_row)

        layout.addStretch()
        layout.addLayout(button_layout)

        self.stack.addWidget(self.account_page)

    def build_username_page(self):

        self.username_page = QWidget()

        layout = QVBoxLayout(self.username_page)
        layout.setSpacing(18)

        # Title
        title = TitleLabel("Change Username")

        # Username
        username_label = self.create_label("Username")

        self.new_username_box = CyberTextBox("")
        self.new_username_box.setText(self.username)

        # Password
        password_label = self.create_label("Retype Password to Confirm")

        self.username_confirm_password_box = CyberTextBox("")
        self.username_confirm_password_box.setEchoMode(QLineEdit.Password)

        # Status
        self.username_status = QLabel("")
        self.username_status.setFont(BODY_FONT)
        self.username_status.setStyleSheet(f"""
            color: {ERROR};
        """)

        # Buttons
        button_layout = QHBoxLayout()

        self.username_cancel = SecondaryButton("Cancel")
        self.username_save = CyberButton("Save")

        self.username_cancel.clicked.connect(self.cancel_username)

        self.username_save.clicked.connect(self.save_username)



        button_layout.addWidget(self.username_status)
        button_layout.addStretch()
        button_layout.addWidget(self.username_cancel)
        button_layout.addWidget(self.username_save)

        #
        # Assemble
        #

        layout.addWidget(title)

        layout.addSpacing(10)

        layout.addWidget(username_label)
        layout.addWidget(self.new_username_box)

        layout.addWidget(password_label)
        layout.addWidget(self.username_confirm_password_box)

        layout.addStretch()

        layout.addLayout(button_layout)

        self.stack.addWidget(self.username_page)

    def show_username_page(self):

        self.new_username_box.setText(self.username)
        self.username_confirm_password_box.clear()
        self.username_status.clear()

        self.stack.setCurrentIndex(1)
    
    def cancel_username(self):
        self.new_username_box.setText(self.username)
        self.username_confirm_password_box.clear()
        self.username_status.clear()

        self.show_account_page()
        

    def save_username(self):
        new_username = self.new_username_box.text().strip()
        current_password = self.username_confirm_password_box.text()

        if not new_username:
            self.username_status.setText("Username cannot be empty.")
            return

        success, message = update_username(self.user, current_password, new_username)

        if not success:
            self.username_status.setText(message)
            return

        # Success
        self.username = new_username
        self.username_box.setText(new_username)
        self.user = get_user(new_username)

        print("Updated Successfully")
        self.show_account_page()

        self.account_status.setText("Username updated successfully.")


    def save_password(self):
        current_password = self.current_password_box.text()
        new_password = self.new_password_box.text()
        confirm_password = self.password_confirm_box.text()

        if not current_password:
            self.password_status.setText("Current password is required.")
            return

        if not new_password:
            self.password_status.setText("New password is required.")
            return

        if new_password != confirm_password:
            self.password_status.setText("Passwords do not match.")
            return
        if current_password == new_password:
            self.password_status.setText("New password must be different.")
            return
            
        success, message, new_user, new_key = update_user_password(self.user, self.key, current_password, new_password)

        if not success:
            self.password_status.setText(message)
            return
        self.user = new_user
        self.key = new_key

        self.current_password_box.clear()
        self.new_password_box.clear()
        self.password_confirm_box.clear()
        self.password_status.clear()

        self.account_status.setText("Password updated successfully.")

        self.current_password_box.clearFocus()
        self.new_password_box.clearFocus()
        self.password_confirm_box.clearFocus()
        self.show_account_page()

        print("Returned from show_account_page")

    def show_account_page(self):

        self.username_box.setText(self.username)
        self.stack.setCurrentIndex(0)


    def build_password_page(self):

        self.password_page = QWidget()

        layout = QVBoxLayout(self.password_page)
        layout.setSpacing(18)

        #Title
        title = TitleLabel("Change Password")

        # Current Password
        current_label = self.create_label("Current Password")

        self.current_password_box = CyberTextBox("")
        self.current_password_box.setEchoMode(QLineEdit.Password)

        # New Password
        new_label = self.create_label("New Password")

        self.new_password_box = CyberTextBox("")
        self.new_password_box.setEchoMode(QLineEdit.Password)

        # Confirm Password
        confirm_label = self.create_label("Confirm Password")

        self.password_confirm_box = CyberTextBox("")
        self.password_confirm_box.setEchoMode(QLineEdit.Password)

        # Status
        self.password_status = QLabel("")
        self.password_status.setFont(BODY_FONT)
        self.password_status.setStyleSheet(f"""
            color: {ERROR};
        """)

        # Buttons
        button_layout = QHBoxLayout()

        self.password_cancel = SecondaryButton("Cancel")
        self.password_save = CyberButton("Save")

        self.password_cancel.clicked.connect(self.cancel_password)

        self.password_save.clicked.connect(self.save_password)

        button_layout.addWidget(self.password_status)
        button_layout.addStretch()
        button_layout.addWidget(self.password_cancel)
        button_layout.addWidget(self.password_save)

        # Assemble

        layout.addWidget(title)

        layout.addSpacing(10)

        layout.addWidget(current_label)
        layout.addWidget(self.current_password_box)

        layout.addWidget(new_label)
        layout.addWidget(self.new_password_box)

        layout.addWidget(confirm_label)
        layout.addWidget(self.password_confirm_box)

        layout.addStretch()

        layout.addLayout(button_layout)

        self.stack.addWidget(self.password_page)

    def show_password_page(self):

        self.current_password_box.clear()
        self.new_password_box.clear()
        self.password_confirm_box.clear()

        self.password_status.clear()

        self.stack.setCurrentIndex(2)
    
    def cancel_password(self):

        self.current_password_box.clear()
        self.new_password_box.clear()
        self.password_confirm_box.clear()

        self.password_status.clear()

        self.show_account_page()

    
    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:

            index = self.stack.currentIndex()

            if index == 1:
                self.save_username()
                return

            elif index == 2:
                self.save_password()
                return

        super().keyPressEvent(event)