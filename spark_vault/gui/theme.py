# Adjust window size here!
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 664


RADIUS = 10

from pathlib import Path
from PySide6.QtGui import QFont, QFontDatabase
from spark_vault.database.initialize import resource_path

FONT_DIR = resource_path("spark_vault/gui/fonts")

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
BUTTON_FONT = QFont("Blender Pro", 16)

LABEL_FONT = QFont("Blender Pro", 14)
SMALL_FONT = QFont("Blender Pro", 12)


TOOLBAR_ADD_BUTTON_WIDTH = 130
TOOLBAR_ADD_BUTTON_HEIGHT = 50

TOOLBAR_SORT_BUTTON_WIDTH = 50
TOOLBAR_SORT_BUTTON_HEIGHT = 50
# Colors
BACKGROUND = "#111111"
PANEL = "#1A1A1A"
PANEL_LIGHT = "#252525"

# ACCENT = "#00FF66"
#ACCENT = "#C9A227" #yellowih gold
ACCENT = "#00E676"
ERROR =  "#FF5252"

# Toolbar Buttons

TOOLBAR = "#2E2E2E"
TOOLBAR_HOVER = "#3A3A3A"
TOOLBAR_PRESSED = "#4A4A4A"

PRIMARY = ACCENT
PRIMARY_HOVER = "#00FF66"
PRIMARY_PRESSED = "#00C348"

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




