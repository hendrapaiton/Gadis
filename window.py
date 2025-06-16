from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox
from pyvistaqt import QtInteractor

from transform import Transform3D


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize the main window
        self.setWindowTitle("GAMBAR MEDIS | GADIS | DICOM VIEWER")
        self.resize(800, 564)

        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint |
            Qt.WindowTitleHint |
            Qt.CustomizeWindowHint
        )

        # Create the central widget and main layout
        self.central = QWidget()
        self.setCentralWidget(self.central)

        # Set up the main horizontal layout
        self.main_horizontal = QHBoxLayout()
        self.central.setLayout(self.main_horizontal)

        # Create the left layout
        self.left_layout = QVBoxLayout()

        # Create the plotter viewer
        self.dcmViewer = QWidget()
        self.dcmViewer.setMinimumWidth(417)
        self.dcmViewer.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.left_layout.addWidget(self.dcmViewer)

        # Create the bottom layout
        self.bottom_layout = QHBoxLayout()

        # Create the file input
        self.filePath = QLineEdit()
        self.filePath.setPlaceholderText("Dicom File...")
        self.filePath.setReadOnly(True)
        self.filePath.setMinimumHeight(35)

        # Create the browse button
        self.browseButton = QToolButton()
        self.browseButton.setText("...")
        self.browseButton.clicked.connect(self.upload_file)
        self.browseButton.setMinimumHeight(35)

        # Create the process button
        self.processButton = QPushButton("Process")
        self.processButton.setMinimumWidth(120)
        self.processButton.setMinimumHeight(35)

        # Add widgets to the bottom layout
        self.bottom_layout.addWidget(self.filePath)
        self.bottom_layout.addWidget(self.browseButton)
        self.bottom_layout.addWidget(self.processButton)

        # Add the bottom layout to the left layout
        self.left_layout.addLayout(self.bottom_layout)

        # Add the left layout to the main horizontal layout
        self.main_horizontal.addLayout(self.left_layout, stretch=2)

        # Create the right layout
        self.right_layout = QVBoxLayout()

        # Create file list label
        self.files_label = QLabel("DICOM FILE LIST")
        self.right_layout.addWidget(self.files_label)

        # Create file list widget
        self.fileList = QListWidget()
        self.fileList.setMinimumWidth(100)
        self.right_layout.addWidget(self.fileList)

        # Add the right layout to the main horizontal layout
        self.main_horizontal.addLayout(self.right_layout, stretch=1)

        # Connect signals to slots
        self.processButton.clicked.connect(self.process_file)

    def upload_file(self):
        # Open file dialog to select a DICOM series
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select DICOM Series",
            "",
            "7-Zip Files (*.7z);;All Files (*.*)"
        )
        if file_name:
            self.filename = file_name
            self.filePath.setText(self.filename)

    def process_file(self):
        # Connect QtInteractor to the DICOM viewer
        plotter = QtInteractor(self.dcmViewer)
        plotter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Clear the previous content in the DICOM viewer
        if self.dcmViewer.layout():
            while self.dcmViewer.layout().count():
                item = self.dcmViewer.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            layout = QVBoxLayout()
            self.dcmViewer.setLayout(layout)

        # Add the plotter to the DICOM viewer
        self.dcmViewer.layout().addWidget(plotter)
        transform = Transform3D(plotter)
        transform.display_3d_object()

    def closeEvent(self, event):
            """Handle the close event to confirm exit and clean up temporary files"""
            reply = QMessageBox.question(
                self,
                "Exit Confirmation",
                "Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
