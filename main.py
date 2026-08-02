import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from spark_vault.gui.login_window import LoginPage
from spark_vault.gui.dashboard_window import DashboardPage
from spark_vault.gui.credential_card import CredentialCard
from spark_vault.gui.theme import load_fonts
from spark_vault.gui.main_window import MainWindow
from spark_vault.database.initialize import initialize_database
from spark_vault.database.initialize import resource_path
def main():
    initialize_database()

    app = QApplication(sys.argv)

    app.setWindowIcon(QIcon(str(resource_path("spark_vault/gui/assets/spark.ico"))))
    
    load_fonts()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ ==  "__main__":
    main()