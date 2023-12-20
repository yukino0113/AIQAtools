import os
import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog
from PIL import Image, ExifTags

from src.UI.Ui_Dialog import Ui_Window
from src.function.ButtonFunction import ButtonFunction
from src.function.GeneratedImage import GeneratedImage
from src.function.Logging import Logging
from src.function.ReferenceImage import ReferenceImage
from src.function.SaveLoad import SaveLoad


class MainWindowController(QDialog, Ui_Window, ButtonFunction, Logging):
    def __init__(self):
        super().__init__()
        self.genImage = None
        self.refImage = None
        self.sl = None
        self.ui = Ui_Window()
        self.ui.setupUi(self)
        self.setup_control()
        self.showMaximized()
        self.window().setWindowTitle("GAI QA tools")

        self.issueList = [getattr(self.ui, obj_name) for obj_name in dir(self.ui) if obj_name.endswith("CB")]

    def setup_control(self):
        self.ui.importOpenBtn.clicked.connect(self.import_path)
        self.ui.exportOpenBtn.clicked.connect(self.export_path)
        self.ui.loadPath.clicked.connect(self.load_path)
        self.ui.nextPic.clicked.connect(self.next_image)
        self.ui.previousPic.clicked.connect(self.previous_image)

    def import_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, '請選擇輸入路徑')
        if folder_path:
            self.ui.importPath.setText(folder_path)

    def export_path(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, '請選擇輸入路徑')
        if folder_path:
            self.ui.exportPath.setText(folder_path)

    def load_path(self) -> None:
        if not self.ui.importPath.text() or not self.ui.exportPath.text():
            QMessageBox.critical(None, "Error", "請先指定輸入/參考圖路徑")
        else:
            try:
                self.sl = SaveLoad(self.ui.importPath.text())
                self.genImage = GeneratedImage(self.ui.importPath.text())
                self.refImage = ReferenceImage(self.ui.exportPath.text(), self.ui.importPath.text())
                self.load_image()
            except FileNotFoundError:
                QMessageBox.critical(None, "Error", "路徑錯誤，請再檢查一次")
            except IndexError:
                QMessageBox.critical(None, "Error", "路徑為不包含圖片的 Style 資料夾，請再檢查一次")

            for i in [self.ui.nextPic, self.ui.previousPic]:
                i.setEnabled(True)

    def load_image(self):

        def set_scene(path):
            scene = QtWidgets.QGraphicsScene()
            scene.addPixmap(path)
            return scene

        def set_fit(view, scene):
            aspect_ratio = scene.sceneRect().height() / scene.sceneRect().width()

            ratio = 100
            view_width = view.viewport().width() * ratio
            view_height = aspect_ratio * view_width

            while view_height > self.ui.generatedPic.height() or view_width > self.ui.generatedPic.width():
                ratio -= 0.01
                view_width = view.viewport().width() * ratio
                view_height = aspect_ratio * view_width

            view.setTransform(QtGui.QTransform().scale(
                view_width / view.sceneRect().width(),
                view_height / view.sceneRect().height()))

        def set_black_bg(view):
            view.setBackgroundBrush(QColor(0, 0, 0))

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

        if not self.genImage.imagePathList:
            return QMessageBox.critical(None, "Error", "路徑沒有任何圖片")

        def set_file_name_and_progress():
            self.ui.generatedLabel.setText(f'Generated image: '
                                           f'{os.path.basename(self.genImage.currentImage).split(".")[0]}')
            self.ui.referenceImageLabel.setText(f'Reference Image: '
                                                f'{os.path.basename(ref_path).split(".")[0]}')
            self.ui.progressLabel.setText(f'Progress: '
                                          f'{self.genImage.currentImageIndex + 1}/{len(self.genImage.imagePathList)}')

        gen_path = self.genImage.currentImage
        # todo: check base name
        ref_path = \
            f'{self.refImage.imagePathList["_".join(os.path.basename(self.genImage.currentImage).split("_")[:2])]}'

        gen_scene = set_scene(QtGui.QPixmap(gen_path))
        self.ui.generatedPic.setScene(gen_scene)
        set_fit(self.ui.generatedPic, gen_scene)
        set_black_bg(self.ui.generatedPic)

        ref_scene = set_scene(QtGui.QPixmap(reorient_img(ref_path)))
        self.ui.referencePic.setScene(ref_scene)
        set_fit(self.ui.referencePic, ref_scene)
        set_black_bg(self.ui.referencePic)

        set_file_name_and_progress()

    def reset_cb(self):
        [self.ui.issueCBs[issueCB].setChecked(False) for issueCB in self.ui.issueCBs.keys()]

    def previous_image(self):
        if not self.genImage.currentImageIndex > 0:
            # todo: change to disable button?
            return QMessageBox.critical(None, "Error", "目前已經是第一張")

        self.genImage.previous()
        issue_list = self.sl.load(self.genImage.currentImage)
        [self.ui.issueCBs[issueCB].setChecked(True) for issueCB in self.ui.issueCBs.keys()
         if self.ui.issueCBs[issueCB].text() in issue_list]
        self.load_image()

    def next_image(self):

        current_style = self.genImage.currentStyle
        current_image = self.genImage.currentImage

        issue = self.get_checked_checkbox_list()

        if not issue:
            no_issue = QMessageBox.question(self, 'Message', f'請確認圖片是否沒有任何問題',
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if no_issue == QMessageBox.StandardButton.Yes:
                issue.append('正常')
            else:
                return

        delete_list = self.sl.get_delete_list(current_style, issue, current_image)

        if '已完成照片備存' in delete_list:
            delete_list.remove('已完成照片備存')

        if delete_list:

            delete = QMessageBox.question(self, 'Message', f'是否沒有以下問題:\n{", ".join(delete_list)}',
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if delete == QMessageBox.StandardButton.No:
                return

        self.sl.save(current_style, issue, current_image)

        if not self.genImage.currentImageIndex == len(self.genImage.imagePathList) - 1:
            self.genImage.next()
            self.reset_cb()
            self.load_image()
        else:
            QMessageBox.information(None, "Error", "測試結束")
            quit_window = QMessageBox.question(self, 'Message', f'是否要離開本程式',
                                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if quit_window == QMessageBox.StandardButton.Yes:
                self.sl.log_final_summary()
                os.startfile(os.path.join(os.path.dirname(self.ui.importPath.text()), 'result'))
                os.startfile(os.path.join(os.path.dirname(self.ui.importPath.text()), 'result', 'log.txt'))
                sys.exit()
