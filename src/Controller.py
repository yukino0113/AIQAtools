import os

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from icecream import ic

from src.UI.Ui_Dialog import Ui_Dialog
from src.function.GeneratedImage import GeneratedImage
from src.function.SaveLoad import SaveLoad


class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.genImage = None
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_control()

        self.issueList = [getattr(self.ui, obj_name) for obj_name in dir(self.ui) if obj_name.endswith("CB")]

    def setup_control(self):
        self.ui.importOpenBtn.clicked.connect(self.import_path)
        self.ui.exportOpenBtn.clicked.connect(self.export_path)
        self.ui.loadPath.clicked.connect(self.load_path)
        self.ui.nextPic.clicked.connect(self.next_image)
        self.ui.skipPic.clicked.connect(self.skip_image)
        self.ui.previousPic.clicked.connect(self.previous_image)

        for i in [self.ui.nextPic, self.ui.skipPic, self.ui.previousPic]:
            i.setEnabled(False)

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
                self.sl = SaveLoad(self.ui.importPath.text())
            except FileNotFoundError:
                QMessageBox.critical(None, "Error", "路徑錯誤，請再檢查一次")
            except IndexError:
                QMessageBox.critical(None, "Error", "路徑包含無圖片的 Style 資料夾，請再檢查一次")

            for i in [self.ui.nextPic, self.ui.skipPic, self.ui.previousPic]:
                i.setEnabled(True)

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

    def reset_cb(self):
        for cb in self.issueList:
            cb.setChecked(False)

    def previous_image(self):
        if not self.genImage.ImageOrder > 0:
            return QMessageBox.critical(None, "Error", "This is the first image")

        self.genImage.previous()
        issue_list = self.sl.load(self.genImage.get_current_image_path())
        for CB in self.issueList:
            if CB.text() in issue_list:
                CB.setChecked(True)
        self.load_image()

    def skip_image(self):
        skip = QMessageBox.question(self, 'Message', f'請確認圖片是否沒有任何問題',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if skip == QMessageBox.StandardButton.Yes:
            self.genImage.next()
            self.reset_cb()
            self.load_image()

    def next_image(self):

        current_style = self.genImage.currentStyle
        current_image = self.genImage.get_current_image_path()

        issue = [x.text() for x in self.issueList if x.isChecked()]

        if delete_list := self.sl.get_delete_list(current_style, issue, current_image):
            delete = QMessageBox.question(self, 'Message', f'是否刪除以下資料夾?\n{", ".join(delete_list)}',
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if delete == QMessageBox.StandardButton.No:
                return

        if not issue:
            no_issue = QMessageBox.question(self, 'Message', f'請確認圖片是否沒有任何問題',
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if no_issue == QMessageBox.StandardButton.Yes:
                issue.append('正常')
            else:
                return

        self.sl.save(current_style, issue, current_image)

        self.genImage.next()
        self.reset_cb()
        self.load_image()

    def save_modify_image(self):
        pass
