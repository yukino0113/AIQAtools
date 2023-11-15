import sys
from PyQt5.QtWidgets import QApplication

from UI.HeadshotWindow import HeadshotWindow
from UI.startWindow import StartWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # window = StartWindow()
    window = HeadshotWindow()
    window.show()
    sys.exit(app.exec_())
