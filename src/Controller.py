import os
from icecream import ic
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from src.UI.Ui_Dialog import Ui_Dialog


class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.ImportOpenBtn.clicked.connect(self.import_path)
        self.ui.ExportOpenBtn.clicked.connect(self.export_path)
        self.ui.LoadPath.clicked.connect(self.load_path)
        self.ui.nextPic.clicked.connect(self.next_image)

        self.ui.importPath.setText("C:\\Users\\jethro_wang\\Desktop")

    def import_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder_path:
            self.ui.importPath.setText(folder_path)

    def export_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder_path:
            self.ui.ExportPath.setText(folder_path)

    def load_path(self) -> None:
        if not self.ui.importPath.text():
            QMessageBox.critical(None, "Error", "請先指定輸入路徑")
        else:
            image_dict = self.get_generated_path()
            ic(image_dict)

    def get_generated_path(self) -> dict:
        image_dict = {}
        source_path = self.ui.importPath.text()
        for style_folder in [x for x in os.listdir(source_path)
                             if (os.path.isdir(os.path.join(source_path, x)) and 'Design' in x)]:
            image_dict[style_folder] = {}
            for source_folder in style_folder:
                path = os.path.join(source_path, style_folder)
                source_folder = ic(x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x)))
                for folder in source_folder:
                    os.chdir(os.path.join(path, folder))
                    for file in os.listdir(os.path.join(path, folder)):
                        image_dict[style_folder][file.split('.')[0]] = os.path.join(path, folder, file)
        return image_dict

    def next_image(self):
        if not self.ui.ExportPath.text():
            QMessageBox.critical(None, "Error", "請先指定輸出路徑")
