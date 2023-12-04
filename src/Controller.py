import os
import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PIL import Image, ExifTags
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
        folder_path = QFileDialog.getExistingDirectory(self, '請選擇輸入路徑')
        if folder_path:
            self.ui.importPath.setText(folder_path)

    def export_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, '請選擇輸入路徑')
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
                QMessageBox.critical(None, "Error", "路徑為不包含圖片的 Style 資料夾，請再檢查一次")

            for i in [self.ui.nextPic, self.ui.skipPic, self.ui.previousPic]:
                i.setEnabled(True)

    def load_image(self):

        def set_scene(path):
            scene = QtWidgets.QGraphicsScene()
            scene.addPixmap(path)
            return scene

        def set_fit(view, scene):
            aspect_ratio = scene.sceneRect().height() / scene.sceneRect().width()

            ratio = 10
            view_width = view.viewport().width() * ratio
            view_height = aspect_ratio * view_width

            while view_height > self.ui.generatedPic.height() or view_width > self.ui.generatedPic.width():
                ratio -= 0.05
                view_width = view.viewport().width() * ratio
                view_height = aspect_ratio * view_width

            view.setTransform(QtGui.QTransform().scale(
                view_width / view.sceneRect().width(),
                view_height / view.sceneRect().height()))

        def set_black_bg(view):
            view.setBackgroundBrush(QColor(0, 0, 0))

        def set_image(view, path):
            scene = set_scene(QtGui.QPixmap(path))
            view.setScene(scene)
            set_fit(view, scene)
            set_black_bg(view)

        def reorient_img(path):
            try:
                image = Image.open(path)
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())

                if exif[orientation] == 3:
                    image = image.transpose(Image.ROTATE_180)
                elif exif[orientation] == 6:
                    image = image.transpose(Image.ROTATE_270)
                elif exif[orientation] == 8:
                    image = image.transpose(Image.ROTATE_90)
                image.save(path)
                image.close()

            except (AttributeError, KeyError, IndexError):
                # cases: image don't have getexif
                pass

            return path

        if not self.genImage.imagePathDic:
            return QMessageBox.critical(None, "Error", "路徑沒有 Style 資料夾")

        self.ui.fileNameLabel.setText(os.path.basename(self.genImage.currentImage).split('.')[0])

        # this label ui has not been make
        # self.ui.referenceLabel.setText('_'.join(os.path.basename(self.genImage.currentImage).split("_")[:2]))

        gen_path = self.genImage.get_current_image_path()
        ref_path = (f'{os.path.dirname(os.path.realpath(__file__))}/../reference_image/'
                    f'{"_".join(os.path.basename(self.genImage.currentImage).split("_")[:2])}.jpg')

        set_image(self.ui.generatedPic, gen_path)
        set_image(self.ui.referencePic, reorient_img(ref_path))

    def reset_cb(self):
        [checkbox.setChecked(False) for checkbox in self.issueList]

    def previous_image(self):
        if not self.genImage.currentImageIndex > 0:
            # todo: change to disable button?
            return QMessageBox.critical(None, "Error", "目前已經是第一張")

        self.genImage.previous()
        issue_list = self.sl.load(self.genImage.get_current_image_path())
        [checkbox.setChecked(True) for checkbox in self.issueList if checkbox.text() in issue_list]
        self.load_image()

    def skip_image(self):

        if (self.genImage.currentStyleIndex == len(self.genImage.imagePathDic) - 1 and
                self.genImage.currentImageIndex == len(self.genImage.imagePathDic[self.genImage.currentStyle]) - 1):
            QMessageBox.information(None, "Error", "已經是最後一張圖了")
            return

        skip = QMessageBox.question(self, 'Message', f'是否要跳過本張圖片',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if skip == QMessageBox.StandardButton.Yes:
            self.genImage.next()
            self.reset_cb()
            self.load_image()

    def next_image(self):

        current_style = self.genImage.currentStyle
        current_image = self.genImage.get_current_image_path()

        issue = [checkbox.text() for checkbox in self.issueList if checkbox.isChecked()]

        if not issue:
            no_issue = QMessageBox.question(self, 'Message', f'請確認圖片是否沒有任何問題',
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if no_issue == QMessageBox.StandardButton.Yes:
                issue.append('正常')
            else:
                return

        if delete_list := self.sl.get_delete_list(current_style, issue, current_image):
            delete = QMessageBox.question(self, 'Message', f'是否沒有以下問題:\n{", ".join(delete_list)}',
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if delete == QMessageBox.StandardButton.No:
                return

        self.sl.save(current_style, issue, current_image)

        if not self.genImage.currentStyleIndex == len(self.genImage.imagePathDic) - 1 and \
                self.genImage.currentImageIndex == len(self.genImage.imagePathDic[self.genImage.currentStyle]) - 1:
            self.genImage.next()
            self.reset_cb()
            self.load_image()
        else:
            QMessageBox.information(None, "Error", "測試結束")

    def save_modify_image(self):
        pass
