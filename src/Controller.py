from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox

from src.UI.Ui_Dialog import Ui_Dialog
from src.function.GeneratedImage import GeneratedImage


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.genImage = None
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.importOpenBtn.clicked.connect(self.import_path)
        self.ui.exportOpenBtn.clicked.connect(self.export_path)
        self.ui.loadPath.clicked.connect(self.load_path)
        self.ui.nextPic.clicked.connect(self.next_image)

        self.ui.importPath.setText("C:\\Users\\jethro_wang\\Desktop")

    def import_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder_path:
            self.ui.importPath.setText(folder_path)

    def export_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder_path:
            self.ui.exportPath.setText(folder_path)

    def load_path(self) -> None:
        if not self.ui.importPath.text():
            QMessageBox.critical(None, "Error", "請先指定輸入路徑")
        else:
            self.genImage = GeneratedImage(self.ui.importPath.text())

    def load_generated_path(self):
        # todo
        #   create image showing class
        #   can get showing number and can modify
        #   can get the image path from the number and load image
        pass

    def load_reference_image(self):
        # todo
        #  name parser for generated image name
        #  loading image from reference folder (Need class?)
        pass

    def previous_image(self):
        self.genImage.previous()
        pass

    def pass_image(self):
        self.genImage.next()
        # todo
        #  will pop hint window?
        pass

    def next_image(self):
        if not self.ui.exportPath.text():
            QMessageBox.critical(None, "Error", "請先指定輸出路徑")
        else:
            self.genImage.next()
        # todo
        #  if no CB, will pop window to tell user wil save to no issue folder.

