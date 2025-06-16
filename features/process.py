import os
import py7zr
from PySide6.QtWidgets import QMessageBox


class ProcessFile:
    def __init__(self, filename: str):
        self.filename = filename

    def extract_dicom_series(self):
        extract_to = "temp"
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        with py7zr.SevenZipFile(self.filename, mode='r') as archive:
            archive.extractall(path=extract_to)

        dataset = []
        for root, dirs, files in os.walk(extract_to):
            for file in files:
                dataset.append(os.path.join(root, file))
        QMessageBox.information(
            None, "Files mounted", f"{len(dataset)} files have been successfully loaded.")
        return extract_to, dataset
