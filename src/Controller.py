import os

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QColor
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
        self.ui.skipPic.clicked.connect(self.skip_image)
        self.ui.previousPic.clicked.connect(self.previous_image)

        self.ui.nextPic.setEnabled(False)
        self.ui.skipPic.setEnabled(False)
        self.ui.previousPic.setEnabled(False)

        self.drawing = False
        self.start_point = None
        self.end_point = None

        self.ui.generatedPic.mousePressEvent = self.mousePressEvent
        self.ui.generatedPic.mouseMoveEvent = self.mouseMoveEvent
        self.ui.generatedPic.mouseReleaseEvent = self.mouseReleaseEvent

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
            try:
                self.genImage = GeneratedImage(self.ui.importPath.text())
                self.load_image()
            except FileNotFoundError:
                QMessageBox.critical(None, "Error", "路徑錯誤，請再檢查一次")

            self.ui.nextPic.setEnabled(True)
            self.ui.skipPic.setEnabled(True)
            self.ui.previousPic.setEnabled(True)

    def load_image(self):

        def set_scene(path):
            scene = QtWidgets.QGraphicsScene()
            scene.addPixmap(QtGui.QPixmap(path))
            return scene

        def set_fit(view, scene):
            aspect_ratio = scene.sceneRect().height() / scene.sceneRect().width()
            ratio = 1
            while ratio:
                view_width = view.viewport().width() * ratio
                view_height = aspect_ratio * view_width
                if view_height <= self.ui.generatedPic.height() and view_width <= self.ui.generatedPic.width():
                    break
                ratio -= 0.05
            view.setTransform(
                QtGui.QTransform().scale(
                    view_width / view.sceneRect().width(),
                    view_height / view.sceneRect().height()))

        def set_black_bg(view):
            view.setBackgroundBrush(QColor(0, 0, 0))

        # todo: fit image
        
        if not self.genImage.imagePathDic:
            QMessageBox.critical(None, "Error", "The path doesn't have any style folder")
        else:
            self.gen_scene = set_scene(QtGui.QPixmap(self.genImage.get_current_image_path()))
            self.ui.generatedPic.setScene(self.gen_scene)
            set_fit(self.ui.generatedPic, self.gen_scene)
            set_black_bg(self.ui.generatedPic)

            self.ui.fileNameLabel.setText(self.genImage.currentImage)

            ref_scene = set_scene(f'{os.path.dirname(os.path.realpath(__file__))}\\..\\reference_image\\'
                                  f'{"_".join(self.genImage.currentImage.split("_")[:2])}.jpg')
            self.ui.referencePic.setScene(ref_scene)
            set_fit(self.ui.referencePic, ref_scene)
            set_black_bg(self.ui.referencePic)

    def previous_image(self):
        if self.genImage.ImageOrder > 0:
            self.genImage.previous()
            self.load_image()
        else:
            QMessageBox.critical(None, "Error", "This is the first image")

    def skip_image(self):
        self.genImage.next()
        # todo
        #  will pop hint window?

        self.load_image()

    def next_image(self):
        # todo
        #  if no CB, will pop window to tell user wil save to no issue folder.

        # if not self.ui.exportPath.text():
        #    QMessageBox.critical(None, "Error", "請先指定輸出路徑")
        # else:
        self.genImage.next()
        self.load_image()
