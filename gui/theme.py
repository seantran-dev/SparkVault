# Adjust window size here!
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 664


RADIUS = 10

from pathlib import Path
from PySide6.QtGui import QFont, QFontDatabase

FONT_DIR = Path(__file__).parent / "fonts"

def load_fonts():
    font_id = QFontDatabase.addApplicationFont(
        str(FONT_DIR / "blender" / "BlenderPro-Book.ttf")
    )

    if font_id != -1:
        #print(QFontDatabase.applicationFontFamilies(font_id))
        print("", end = "")


TITLE_FONT = QFont("Blender Pro", 26)
HEADING_FONT = QFont("Blender Pro", 22)
BODY_FONT = QFont("Blender Pro", 18)
BUTTON_FONT = QFont("Blender Pro", 14)

LABEL_FONT = QFont("Blender Pro", 14)
SMALL_FONT = QFont("Blender Pro", 12)


# Colors
BACKGROUND = "#111111"
PANEL = "#1A1A1A"
PANEL_LIGHT = "#252525"

ACCENT = "#00FF66"

TEXT = "#FFFFFF"
TEXT_DIM = "#8E8E8E"

BORDER = "#303030"

SCROLLBAR_STYLE = """
    QScrollBar:vertical {
        background: transparent;
        width: 10px;
    }

    QScrollBar::handle:vertical {
        background: #303030;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical:hover {
        background: #00FF66;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical,
    QScrollBar::sub-page:vertical {
        background: transparent;
        height: 0px;
    }
    """




