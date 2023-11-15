import time

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QRadioButton, QButtonGroup, QPushButton

from UI.HeadshotWindow import HeadshotWindow


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.window_setting()

        self.task_label = QLabel('Task:')
        self.task_radio_headshot = QRadioButton('AI Headshot')
        self.task_radio_sketch = QRadioButton('AI Sketch')
        self.done_button = QPushButton('Done', self)
        self.init_ui()

    def window_setting(self):
        self.setLayout(self.layout)

        self.setWindowTitle('AI QA Tools')
        self.setGeometry(100, 100, 160, 120)

    def init_ui(self):
        group_task = QButtonGroup()
        group_task.addButton(self.task_radio_headshot)

        self.layout.addWidget(self.task_label, 0, 0, 1, 1)
        self.layout.addWidget(self.task_radio_headshot, 0, 1, 1, 1)
        self.layout.addWidget(self.task_radio_sketch, 0, 2, 1, 1)
        self.layout.addWidget(self.done_button, 1, 0, 1, 3)

        self.task_radio_headshot.setChecked(True)
        self.task_radio_headshot.setDisabled(True)
        self.task_radio_sketch.setDisabled(True)

        self.done_button.clicked.connect(self.done_pressed)

    def done_pressed(self):
        if self.task_radio_headshot.isChecked():
            self.headshot_window = HeadshotWindow()
            self.headshot_window.show()


