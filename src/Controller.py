import os

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from icecream import ic

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
            self.load_image()

    def load_image(self):
        gen_scene = QtWidgets.QGraphicsScene()
        gen_scene.addPixmap(QtGui.QPixmap(self.genImage.get_current_image_path()))
        self.ui.generatedPic.setScene(gen_scene)

        self.ui.fileNameLabel.setText(self.genImage.currentImage)

        ic(os.path.dirname(os.path.realpath(__file__)))
        ref_file_path = ic(f'{os.path.dirname(os.path.realpath(__file__))}\\..\\reference_image\\'
                           f'{"_".join(self.genImage.currentImage.split("_")[:2])}.jpg')
        ref_scene = QtWidgets.QGraphicsScene()
        ref_scene.addPixmap(QtGui.QPixmap(ref_file_path))
        self.ui.referencePic.setScene(ref_scene)

    def previous_image(self):
        self.genImage.previous()

        self.load_image()
        pass

    def pass_image(self):
        self.genImage.next()
        # todo
        #  will pop hint window?

        self.load_image()

    def next_image(self):
        # todo
        #  if no CB, will pop window to tell user wil save to no issue folder.

        #if not self.ui.exportPath.text():
        #    QMessageBox.critical(None, "Error", "請先指定輸出路徑")
        #else:
            self.genImage.next()
            self.load_image()

