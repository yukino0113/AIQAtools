from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog

from src.UI.Ui_Dialog import Ui_Dialog


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.ImportOpenBtn.clicked.connect(self.import_path)
        self.ui.ExportOpenBtn.clicked.connect(self.export_path)

    def import_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder_path:
            self.ui.importPath.setText(folder_path)

    def export_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder_path:
            self.ui.ExportPath.setText(folder_path)