from PySide6.QtWidgets import (
    QPushButton,
    QLineEdit,
    QLabel,
    QFrame,
    QLineEdit,
    QToolButton
)

from PySide6.QtCore import Qt, QRect, Signal, QSize
from PySide6.QtGui import QPainter, QColor

from spark_vault.gui.theme import *
import qtawesome as qta


class CyberButton(QPushButton):

    def __init__(self, text, primary=True):
        super().__init__(text)

        if primary:
            background = ACCENT
            hover = "#00E676"
            pressed = "#00A63C"
            text_color = "black"
        else:
            background = PANEL_LIGHT
            hover = PANEL_LIGHT
            pressed = PANEL
            text_color = TEXT

        self.progress = 0
        self.animating = False

        self.setFont(BUTTON_FONT)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(f"""
            QPushButton {{
            background-color: {background};
            color: {text_color};
            border: 2px solid {BORDER};
            border-radius: {RADIUS}px;
            padding: 12px;
        }}

        QPushButton:hover {{
            background-color: {hover};
            border: 2px solid {ACCENT};
        }}

        QPushButton:pressed {{
            background-color: {pressed};
            border: 2px solid {ACCENT};
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
        # Background
        painter.setPen(Qt.PenStyle.NoPen)

        if self.progress == 0:
            if self.isDown():
                color = QColor("#00C348")      # Pressed
            elif self.underMouse():
                color = QColor("#00FF66")      # Hover
            else:
                color = QColor(ACCENT)         # Normal

            painter.setBrush(color)
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

class SecondaryButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)

        self.setFont(BUTTON_FONT)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {PANEL_LIGHT};
                color: {TEXT};
                border: 2px solid {BORDER};
                border-radius: {RADIUS}px;
                padding: 12px;
            }}

            QPushButton:hover {{
                border: 2px solid {ACCENT};
            }}

            QPushButton:pressed {{
                background-color: {PANEL};
                border: 2px solid {ACCENT};
            }}
        """)

class DangerButton(QPushButton):

    def __init__(self, text):
        super().__init__(text)

        self.setFont(BUTTON_FONT)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {PANEL_LIGHT};
                color: {TEXT};
                border: 2px solid {BORDER};
                border-radius: {RADIUS}px;
                padding: 12px;
            }}

            QPushButton:hover {{
                background-color: #8B1E1E;
                border: 2px solid #E53935;
                color: white;
            }}

            QPushButton:pressed {{
                background-color: #6D1515;
                border: 2px solid #E53935;
                color: white;
            }}
        """)
        
class ToolbarButton(QPushButton):

    def __init__(self, text="", icon=None, primary=False):
        super().__init__(text)

        self.setFont(BODY_FONT)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(110, 42)

        self.icon = icon

        if primary:
            self.normal_color = QColor(PRIMARY)
            self.hover_color = QColor(PRIMARY_HOVER)
            self.pressed_color = QColor(PRIMARY_PRESSED)
            self.text_color = QColor(BACKGROUND)
            self.border_color = QColor(PRIMARY)
        else:
            self.normal_color = QColor(TOOLBAR)
            self.hover_color = QColor(TOOLBAR_HOVER)
            self.pressed_color = QColor(TOOLBAR_PRESSED)
            self.text_color = QColor(TEXT)
            self.border_color = QColor(BORDER)

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        # Background
        painter.setPen(Qt.PenStyle.NoPen)

        if self.isDown():
            color = self.pressed_color
        elif self.underMouse():
            color = self.hover_color
        else:
            color = self.normal_color

        painter.setBrush(color)
        painter.drawRoundedRect(rect, RADIUS, RADIUS)

        # Border
        painter.setPen(self.border_color)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(
            rect.adjusted(0, 0, -1, -1),
            RADIUS,
            RADIUS
        )

        # Icon
        if self.icon:
            icon_rect = QRect(12, 0, 18, rect.height())
            self.icon.paint(
                painter,
                icon_rect,
                Qt.AlignmentFlag.AlignCenter
            )

        # Text
        painter.setPen(self.text_color)
        painter.setFont(self.font())

        if self.icon:
            text_rect = rect.adjusted(36, 0, 0, 0)
            alignment = Qt.AlignVCenter | Qt.AlignLeft
        else:
            text_rect = rect
            alignment = Qt.AlignCenter

        painter.drawText(
            text_rect,
            alignment,
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
                padding-right:40px;
            }}

            QLineEdit:focus {{
                border:2px solid {ACCENT};
            }}
        """)




class SearchBox(CyberTextBox):

    def __init__(self, placeholder=""):
        super().__init__(placeholder)

        # Leave room for the sort button
        self.setStyleSheet(self.styleSheet() + """
            QLineEdit {
                padding-right: 42px;
            }
        """)

        self.sort_button = QToolButton(self)
        self.sort_button.setIcon(qta.icon("fa6s.sort", color=TEXT_DIM))
        self.sort_button.setIconSize(QSize(28, 28))
        self.sort_button.setCursor(Qt.PointingHandCursor)
        self.sort_button.setFixedSize(32, 32)

        self.sort_button.setStyleSheet(f"""
            QToolButton {{
                border: none;
                background: transparent;
            }}

            QToolButton:hover {{
                background: {PANEL_LIGHT};
                border-radius: 6px;
            }}
        """)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        margin = 8
        self.sort_button.move(
            self.width() - self.sort_button.width() - margin,
            (self.height() - self.sort_button.height()) // 2
        )

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