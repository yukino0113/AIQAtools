from PyQt6 import QtWidgets
import sys

from src.Controller import MainWindowController

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowController()
    window.show()
    sys.exit(app.exec())
