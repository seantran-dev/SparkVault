import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from gui.login_window import LoginPage
from gui.dashboard_window import DashboardPage
from gui.credential_card import CredentialCard
from gui.theme import load_fonts
from gui.main_window import MainWindow

def main():

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("gui/assets/spark.ico"))
    
    load_fonts()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())




if __name__ ==  "__main__":
    main()