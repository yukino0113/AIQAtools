from PIL import Image, ExifTags
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QFileDialog


from src.UI.Ui_Dialog import Ui_Window


class ButtonFunction:

    def __init__(self):
        self.ui = self.ui = Ui_Window()

    def import_file_picker(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path:
            self.ui.importPath.setText(folder_path)

    def reference_file_picker(self):
        folder_path = QFileDialog.getExistingDirectory()
        if folder_path:
            self.ui.exportPath.setText(folder_path)

    def reset_cb(self):
        [self.ui.issueCBs[issueCB].setChecked(False) for issueCB in self.ui.issueCBs.keys()]

    def get_checked_checkbox_list(self):
        return [self.ui.issueCBs[issueCB].text() for issueCB in self.ui.issueCBs.keys()
                if self.ui.issueCBs[issueCB].isChecked()]

    def set_checkbox(self, issue_list):
        [self.ui.issueCBs[issueCB].setChecked(True) for issueCB in self.ui.issueCBs.keys()
         if self.ui.issueCBs[issueCB].text() in issue_list]

