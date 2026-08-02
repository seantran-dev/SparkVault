from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout

from spark_vault.gui.theme import *
from spark_vault.gui.widgets import *


class DeleteConfirmationDialog(QDialog):

    def __init__(self, service):
        super().__init__()
        self.service = service
        self.setWindowTitle("Delete Credential")
        self.setFixedSize(400, 300)

        self.setStyleSheet(f"""
            QDialog {{
                background: {BACKGROUND};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        dialog_title = TitleLabel("Delete Credential")


        title = TitleLabel("Delete Credential")
        title.setAlignment(Qt.AlignCenter)

        title = QLabel("Are you sure you want to delete")
        title.setFont(BODY_FONT)
        title.setAlignment(Qt.AlignCenter)

        service = QLabel(service)
        service.setFont(HEADING_FONT)
        service.setStyleSheet(f"color: {ACCENT};")
        service.setAlignment(Qt.AlignCenter)

        warning = QLabel("This action cannot be undone.")
        warning.setFont(BODY_FONT)
        warning.setAlignment(Qt.AlignCenter)

        buttons = QHBoxLayout()

        cancel = SecondaryButton("Cancel")
        delete = DangerButton("Delete")

        cancel.clicked.connect(self.reject)
        delete.clicked.connect(self.accept)

        buttons.addStretch()
        buttons.addWidget(cancel)
        buttons.addWidget(delete)

        layout.addStretch()
        layout.addWidget(dialog_title) 
        layout.addWidget(title)
        layout.addWidget(service)
        layout.addWidget(warning)
        layout.addStretch()
        layout.addLayout(buttons)