from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QUrl
import transcribe_audio as ta
import os
import time

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.file_path = ""

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.file_label = QLabel("No file selected.")
        self.select_button = QPushButton("Select File")
        self.transcribe_button = QPushButton("Transcribe Selected")
        self.progress = QProgressBar()

        self.select_button.clicked.connect(self.select_file)
        self.transcribe_button.clicked.connect(self.transcribe_and_save_selected)

        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.transcribe_button)
        self.layout.addWidget(self.progress)

        # Enable dropping
        self.setAcceptDrops(True)

    def select_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName()
        if self.file_path:
            self.file_label.setText(self.file_path)

    def transcribe_and_save_selected(self):
        if not self.file_path:
            QMessageBox.critical(self, "No file selected", "Please select a file to transcribe.")
            return
        self.progress.setValue(0)
        QApplication.processEvents()
        transcription = ta.transcribe_audio(self.file_path)
        self.progress.setValue(50)
        QApplication.processEvents()
        transcription_filename = self.save_transcription(self.file_path, transcription)
        self.progress.setValue(100)
        QApplication.processEvents()
        QMessageBox.information(self, "Transcription complete", f"Transcription saved as: {transcription_filename}")

    def save_transcription(self, audio_file, transcription):
        directory, filename = os.path.split(audio_file)
        transcription_filename = os.path.splitext(filename)[0] + "_transcription.txt"
        with open(os.path.join(directory, transcription_filename), "w") as f:
            f.write(transcription)
        return transcription_filename

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            self.file_path = url.toLocalFile()
            self.file_label.setText(self.file_path)

app = QApplication([])
window = Window()
window.show()
app.exec_()
