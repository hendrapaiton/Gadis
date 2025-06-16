from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from pyvistaqt import QtInteractor

from transform import display_3d_object

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GAMBAR MEDIS | GADIS")
        self.resize(800, 564)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.main_horizontal = QHBoxLayout()
        self.central.setLayout(self.main_horizontal)

        self.left_layout = QVBoxLayout()

        self.dcmViewer = QWidget()
        self.dcmViewer.setMinimumHeight(350)
        self.left_layout.addWidget(self.dcmViewer)

        self.bottom_layout = QHBoxLayout()

        self.filePath = QLineEdit()
        self.filePath.setPlaceholderText("Dicom File...")
        self.filePath.setReadOnly(True)

        self.processButton = QPushButton("Process")
        self.processButton.setMinimumWidth(120)

        self.bottom_layout.addWidget(self.filePath)
        self.bottom_layout.addWidget(self.processButton)

        self.left_layout.addLayout(self.bottom_layout)

        self.main_horizontal.addLayout(self.left_layout, stretch=2)

        self.right_layout = QVBoxLayout()

        self.files_label = QLabel("DICOM FILE LIST")
        self.right_layout.addWidget(self.files_label)

        self.fileList = QListWidget()
        self.fileList.setMinimumWidth(100)
        self.right_layout.addWidget(self.fileList)

        self.main_horizontal.addLayout(self.right_layout, stretch=1)

        self.processButton.clicked.connect(self.process_file)

    def process_file(self):
        plotter = QtInteractor(self.dcmViewer)
        display_3d_object(plotter)
