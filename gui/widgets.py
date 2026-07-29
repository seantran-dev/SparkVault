from PySide6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QLabel,
    QFrame,
    QLineEdit
)

from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPainter, QColor

from gui.theme import *


class CyberButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)
        self.progress = 0
        self.animating = False

        self.setFont(BUTTON_FONT)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(f"""
            QPushButton {{
                background:{ACCENT};
                color:black;
                border:none;
                outline: none;
                border-radius:{RADIUS}px;
                padding:12px;
            }}

            QPushButton:hover {{
                background:#4DFF94;
            }}

            QPushButton:pressed {{
                background:#00B84A;
            }}
        """)

    def set_progress(self, value):
        self.progress = value
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        # Background
        painter.setPen(Qt.PenStyle.NoPen)

        if self.progress == 0:
            painter.setBrush(QColor(ACCENT))
        else:
            painter.setBrush(QColor(PANEL_LIGHT))

        painter.drawRoundedRect(rect, RADIUS, RADIUS)

        # Progress fill
        if self.progress > 0:

            fill = QRect(
                0,
                0,
                int(rect.width() * self.progress / 100),
                rect.height()
            )

            painter.setBrush(QColor(ACCENT))
            painter.drawRoundedRect(fill, RADIUS, RADIUS)

        # Border
        painter.setPen(QColor(ACCENT))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(
            rect.adjusted(0, 0, -1, -1),
            RADIUS,
            RADIUS
        )

        # Text
        if self.progress == 0:
            painter.setPen(QColor("black"))
        else:
            painter.setPen(QColor(TEXT))

        painter.setFont(self.font())
        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            self.text()
        )

class CyberTextBox(QLineEdit):

    def __init__(self, placeholder="", password=False):
        super().__init__()

        self.setPlaceholderText(placeholder)
        self.setFont(BODY_FONT)

        if password:
            self.setEchoMode(QLineEdit.EchoMode.Password)

        self.setStyleSheet(f"""
            QLineEdit {{
                background:{PANEL};
                border:2px solid {BORDER};
                border-radius:{RADIUS}px;
                color:{TEXT};
                padding:10px;
            }}

            QLineEdit:focus {{
                border:2px solid {ACCENT};
            }}
        """)

class DimLabel(QLabel):

    def __init__(self, text=""):
        super().__init__(text)

        self.setFont(BODY_FONT)

        self.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_DIM};
                background: transparent;
            }}
        """)
        
class TitleLabel(QLabel):

    def __init__(self, text):

        super().__init__(text)

        self.setAlignment(Qt.AlignCenter)

        self.setFont(TITLE_FONT)

        self.setStyleSheet(f"""

            color:{ACCENT};

        """)

class SubtitleLabel(QLabel):

    def __init__(self, text):

        super().__init__(text)

        self.setAlignment(Qt.AlignCenter)

        self.setFont(BODY_FONT)

        self.setStyleSheet(f"""

            color:{TEXT_DIM};

        """)

class CyberCard(QFrame):

    def __init__(self):

        super().__init__()

        self.setStyleSheet(f"""

            QFrame {{

                background:{PANEL};

                border:1px solid {BORDER};

                border-radius:{RADIUS}px;

            }}

        """)

class LinkLabel(QLabel):

    clicked = Signal()

    def __init__(self, text):
        super().__init__(text)

        self.setAlignment(Qt.AlignCenter)

        self.setTextFormat(Qt.RichText)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(False)

        self.setFont(BODY_FONT)

        self.linkActivated.connect(lambda _: self.clicked.emit())

        self.setStyleSheet(f"""
            QLabel {{
                color:{TEXT_DIM};
            }}

            QLabel a {{
                color:{ACCENT};
                text-decoration:none;
            }}

            QLabel a:hover {{
                text-decoration:underline;
            }}
        """)