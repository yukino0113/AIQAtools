from PyQt6 import QtWidgets
import sys

from src.Controller import MainWindowController
from src.function.Logging import Logging

Logging().clear_log()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowController()
    window.show()
    sys.exit(app.exec())
