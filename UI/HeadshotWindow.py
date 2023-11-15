from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog
import configparser

configparser = configparser.ConfigParser()
configparser.read('config.ini')


class HeadshotWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.window_setting()
        self.init_ui()
        self.load()

    def window_setting(self) -> None:
        self.setLayout(self.layout)

        # Set window properties
        self.setWindowTitle('AI QA Tools')
        self.setGeometry(100, 100, 1600, 600)

    def init_ui(self) -> None:
        def init_import() -> None:
            self.import_label = QLabel('Import folder:')
            self.layout.addWidget(self.import_label, 0, 0, 1, 1)

            self.import_entry = QLineEdit()
            self.import_entry.setReadOnly(True)
            self.import_entry.setText(configparser['fileIO']['input_path'])
            self.layout.addWidget(self.import_entry, 0, 1, 1, 4)

            self.import_file_button = QPushButton('Open...')
            self.import_file_button.clicked.connect(self._import_open_file_dialog)
            self.layout.addWidget(self.import_file_button, 0, 5, 1, 1)

        def init_export() -> None:
            self.export_label = QLabel('Export folder:')
            self.layout.addWidget(self.export_label, 1, 0, 1, 1)

            self.export_entry = QLineEdit()
            self.export_entry.setReadOnly(True)
            self.export_entry.setText(configparser['fileIO']['output_path'])
            self.layout.addWidget(self.export_entry, 1, 1, 1, 4)

            self.export_file_button = QPushButton('Open...')
            self.export_file_button.clicked.connect(self.export_open_file_dialog)
            self.layout.addWidget(self.export_file_button, 1, 5, 1, 1)

        init_import()
        init_export()

        self.x = QLabel(':')
        self.layout.addWidget(self.x, 10, 10)

    def load(self):
        pass

    def _import_open_file_dialog(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder_path:
            self.import_entry.setText(folder_path)

    def export_open_file_dialog(self) -> None:
        folder_path = QFileDialog.getExistingDirectory(self, 'Select a folder')
        if folder_path:
            self.export_entry.setText(folder_path)
