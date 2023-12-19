# Form implementation generated from reading ui file 'QAtool.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import os

from PyQt6.QtGui import QFont


class Ui_Window(object):
    def setupUi(self, Window):

        def _get_issue():
            issue = {}
            with open(f'{os.path.dirname(os.path.realpath(__file__))}/../../issue_list.txt', 'r', encoding='utf-8') as f:
                for line in f.read().split('\n'):
                    if ':' in line and not line.startswith('#'):
                        key, value = line.split(":")
                        issue[key] = value
                issue['正常'] = '正常'
                return issue

        Window.setObjectName("Window")
        Window.resize(1200, 600)
        self.gridLayout = QtWidgets.QGridLayout(Window)
        self.gridLayout.setObjectName("gridLayout")
        self.pathLayout = QtWidgets.QSplitter(parent=Window)
        self.pathLayout.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pathLayout.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.pathLayout.setObjectName("pathLayout")
        self.layoutWidget = QtWidgets.QWidget(parent=self.pathLayout)
        self.layoutWidget.setObjectName("layoutWidget")
        self.stylePathLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.stylePathLayout.setContentsMargins(0, 0, 0, 0)
        self.stylePathLayout.setObjectName("stylePathLayout")
        self.importLable = QtWidgets.QLabel(parent=self.layoutWidget)
        self.importLable.setObjectName("importLable")
        self.stylePathLayout.addWidget(self.importLable)
        self.importPath = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.importPath.setObjectName("importPath")
        self.stylePathLayout.addWidget(self.importPath)
        self.importOpenBtn = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.importOpenBtn.setObjectName("importOpenBtn")
        self.stylePathLayout.addWidget(self.importOpenBtn)
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.pathLayout)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.refrencePathLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.refrencePathLayout.setContentsMargins(0, 0, 0, 0)
        self.refrencePathLayout.setObjectName("refrencePathLayout")
        self.referenceLabel = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.referenceLabel.setObjectName("referenceLabel")
        self.refrencePathLayout.addWidget(self.referenceLabel)
        self.exportPath = QtWidgets.QLineEdit(parent=self.layoutWidget1)
        self.exportPath.setObjectName("exportPath")
        self.refrencePathLayout.addWidget(self.exportPath)
        self.exportOpenBtn = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.exportOpenBtn.setObjectName("exportOpenBtn")
        self.refrencePathLayout.addWidget(self.exportOpenBtn)
        self.loadPath = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.loadPath.setObjectName("loadPath")
        self.refrencePathLayout.addWidget(self.loadPath)
        self.gridLayout.addWidget(self.pathLayout, 0, 0, 1, 1)
        self.belowLayout = QtWidgets.QHBoxLayout()
        self.belowLayout.setObjectName("belowLayout")
        self.referenceLayout = QtWidgets.QVBoxLayout()
        self.referenceLayout.setObjectName("referenceLayout")
        self.referenceImageLabel = QtWidgets.QLabel(parent=Window)
        self.referenceImageLabel.setObjectName("referenceImageLabel")
        self.referenceLayout.addWidget(self.referenceImageLabel)
        self.referencePic = QtWidgets.QGraphicsView(parent=Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.referencePic.sizePolicy().hasHeightForWidth())
        self.referencePic.setSizePolicy(sizePolicy)
        self.referencePic.setMinimumSize(QtCore.QSize(500, 500))
        self.referencePic.setObjectName("referencePic")
        self.referenceLayout.addWidget(self.referencePic)
        self.belowLayout.addLayout(self.referenceLayout)
        self.generatedLayout = QtWidgets.QVBoxLayout()
        self.generatedLayout.setObjectName("generatedLayout")
        self.generatedLabel = QtWidgets.QLabel(parent=Window)
        self.generatedLabel.setObjectName("generatedLabel")
        self.generatedLayout.addWidget(self.generatedLabel)
        self.generatedPic = QtWidgets.QGraphicsView(parent=Window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.generatedPic.sizePolicy().hasHeightForWidth())
        self.generatedPic.setSizePolicy(sizePolicy)
        self.generatedPic.setMinimumSize(QtCore.QSize(500, 500))
        self.generatedPic.setObjectName("generatedPic")
        self.generatedLayout.addWidget(self.generatedPic)
        self.belowLayout.addLayout(self.generatedLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(parent=Window)
        self.widget.setObjectName("widget")
        self.widget.setMaximumWidth(169)
        self.progressCB = QtWidgets.QVBoxLayout(self.widget)
        self.progressCB.setObjectName("progressCB")
        self.progressLabel = QtWidgets.QLabel(parent=Window)
        self.progressLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        self.progressLabel.setObjectName("progressLabel")
        self.progressLabel.setFont(QFont('Arial', 12))
        self.progressCB.addWidget(self.progressLabel)
        self.verticalLayout_3.addLayout(self.progressCB)
        self.verticalLayout_3.addWidget(self.widget)
        self.belowLayout.addLayout(self.verticalLayout_3)
        self.gridLayout.addLayout(self.belowLayout, 1, 0, 1, 1)

        self.issueCBs = {}
        for issue in _get_issue():
            self.issueCBs[issue] = QtWidgets.QCheckBox(parent=Window)
            self.issueCBs[issue].setMinimumSize(QtCore.QSize(155, 0))
            self.issueCBs[issue].setObjectName("exampleCB")
            self.issueCBs[issue].setText(QtCore.QCoreApplication.translate("Window", f"{issue}"))
            self.issueCBs[issue].setFont(QFont('Arial', 10))

            self.progressCB.addWidget(self.issueCBs[issue])

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        self.progressCB.addItem(spacerItem)

        self.buttonsLayout = QtWidgets.QWidget(parent=Window)
        self.buttonsLayout.setMinimumSize(QtCore.QSize(0, 23))
        self.buttonsLayout.setMaximumSize(QtCore.QSize(16777215, 23))
        self.buttonsLayout.setObjectName("buttonsLayout")
        self.formLayout_2 = QtWidgets.QFormLayout(self.buttonsLayout)
        self.formLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTop|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.formLayout_2.setContentsMargins(1, -1, 10, -1)
        self.formLayout_2.setObjectName("formLayout_2")
        self.previousPic = QtWidgets.QPushButton(parent=self.buttonsLayout)
        self.previousPic.setEnabled(False)
        self.previousPic.setMinimumSize(QtCore.QSize(75, 23))
        self.previousPic.setMaximumSize(QtCore.QSize(75, 23))
        self.previousPic.setObjectName("previousPic")

        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.previousPic)
        self.nextPic = QtWidgets.QPushButton(parent=self.buttonsLayout)
        self.nextPic.setEnabled(False)
        self.nextPic.setMinimumSize(QtCore.QSize(75, 23))
        self.nextPic.setMaximumSize(QtCore.QSize(75, 23))
        self.nextPic.setObjectName("nextPic")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.nextPic)
        self.progressCB.addWidget(self.buttonsLayout)


        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)
        
    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Dialog"))

        # Path related string
        self.importLable.setText(_translate("Window", "Style Path:"))
        self.importOpenBtn.setText(_translate("Window", "Open"))
        self.referenceLabel.setText(_translate("Window", "Reference Path:"))
        self.exportOpenBtn.setText(_translate("Window", "Open"))
        self.loadPath.setText(_translate("Window", "Load All Path"))

        # File name related string
        self.referenceImageLabel.setText(_translate("Window", "Reference Image: "))
        self.generatedLabel.setText(_translate("Window", "Generated image:"))

        # Progress string
        self.progressLabel.setText(_translate("Window", "Progress:"))

        # Buttons
        self.previousPic.setText(_translate("Window", "Previous"))
        self.nextPic.setText(_translate("Window", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QDialog()
    ui = Ui_Window()
    ui.setupUi(Window)
    Window.show()
    sys.exit(app.exec())
