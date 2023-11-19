from PyQt6 import QtWidgets
import sys

from src.Controller import MainWindow_controller

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow_controller()
    window.show()
    sys.exit(app.exec())
