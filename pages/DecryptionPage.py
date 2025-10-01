import os
import time
import tracemalloc

from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit,
    QMessageBox, QFileDialog, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from helpers.analytics import get_resource_usage
from helpers.decrypt import decrypt_file, save_decrypted_to_file

class DecryptionPage(QWidget):
    def __init__(self, stack):
        super().__init__()

        self.stack = stack
        self.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 6px 12px;
                border-radius: 8px;
                background-color: #0078D7;
                color: white;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QTextEdit {
                font-size: 12px;
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
        """)

        pageLabel = QLabel("Audio File Decryption")
        pageLabel.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        pageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a horizontal line separator below the heading
        heading_separator = QFrame()
        heading_separator.setFrameShape(QFrame.Shape.HLine)
        heading_separator.setFrameShadow(QFrame.Shadow.Sunken)
        heading_separator.setStyleSheet("margin-bottom: 18px; margin-top: 8px;")
        heading_separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        heading_separator.setMinimumWidth(400)

        self.docfile_button = QPushButton("Select Encrypted File")
        self.docfile_button.clicked.connect(self.pick_doc_file)
        self.docfile_label = QLabel("No file selected")
        self.docfile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        docfile_frame = QFrame()
        docfile_layout = QVBoxLayout(docfile_frame)
        docfile_layout.addWidget(self.docfile_button)
        docfile_layout.addWidget(self.docfile_label)

        self.publickeyfile_button = QPushButton("Select Key File")
        self.publickeyfile_button.clicked.connect(self.pick_publickey_file)
        self.publickeyfile_label = QLabel("No key selected")
        self.publickeyfile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        publickeyfile_frame = QFrame()
        publickeyfile_layout = QVBoxLayout(publickeyfile_frame)
        publickeyfile_layout.addWidget(self.publickeyfile_button)
        publickeyfile_layout.addWidget(self.publickeyfile_label)

        self.analysis_output_label = QLabel("Calculation Analysis:")
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        self.analysis_output.setFixedHeight(50)

        decrypt_button = QPushButton("Decrypt")
        decrypt_button.clicked.connect(self.decrypt_btn_clicked)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_btn_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(decrypt_button)
        button_layout.addWidget(save_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(12)
        content_layout.addWidget(pageLabel)
        content_layout.addWidget(heading_separator)
        content_layout.addWidget(docfile_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(publickeyfile_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.analysis_output_label, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.analysis_output, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addLayout(button_layout)
        content_layout.addWidget(clear_button, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        wrapper = QWidget()
        wrapper.setLayout(content_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(wrapper)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        wrapper.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

        self.docfile_path = None
        self.publickey_file_path = None
        self.signaturefile_path = None
        self.decrypted = {}

    def go_back(self):
        self.docfile_path = None
        self.publickey_file_path = None
        self.signaturefile_path = None
        self.decrypted = {}
        self.analysis_output.setPlainText("")
        self.docfile_label.setText("No file selected")
        self.publickeyfile_label.setText("No key selected")
        self.stack.setCurrentIndex(0)

    def clear(self):
        self.docfile_path = None
        self.publickey_file_path = None
        self.signaturefile_path = None
        self.decrypted = {}
        self.analysis_output.setPlainText("")
        self.docfile_label.setText("No file selected")
        self.publickeyfile_label.setText("No key selected")

    def pick_doc_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted File", "", "Enc Files (*.enc)")
        if file_path:
            file_size = os.stat(file_path).st_size / 1024
            self.docfile_path = file_path
            file_name = os.path.basename(file_path)  # <-- Get just the file name
            label_text = f"Audio file selected, (Name: {file_name}, Size: {file_size:.2f} KB)"
            self.docfile_label.setText(label_text)

    def pick_publickey_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Key", "", "Key Files (*.key)")
        if file_path:
            self.publickey_file_path = file_path
            file_name = os.path.basename(self.publickey_file_path)  # <-- Get just the file name
            label_text = f"Key selected, (Name: {file_name})"
            self.publickeyfile_label.setText(label_text)

    def decrypt_btn_clicked(self):
        if not self.docfile_path:
            QMessageBox.warning(self, "Warning", "No audio file selected")
            return

        if not self.publickey_file_path:
            QMessageBox.warning(self, "Warning", "No key selected")
            return

        self.analysis_output.setPlainText("")

        try:
            tracemalloc.start()
            start_time = time.time()
            self.decrypted = decrypt_file(self.docfile_path, self.publickey_file_path)
            if not self.decrypted:
                QMessageBox.critical(self, "Error", "Decryption failed")
                return
            end_time = time.time()
            _, peak = tracemalloc.get_traced_memory()
            time_taken_ms = (end_time - start_time) * 1000

            time_analysis = f"Time taken: {time_taken_ms:.6f} ms"
            self.analysis_output.setText(time_analysis)

            QMessageBox.information(self, "Success", "Audio file decrypted successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", repr(e))
            return

    def save_btn_clicked(self):
        if not self.decrypted:
            QMessageBox.warning(self, "Warning", "No decrypted data to save")
            return
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        try:
            info = save_decrypted_to_file(self.decrypted, directory)
            QMessageBox.information(self, "Success", info)
        except Exception as e:
            QMessageBox.critical(self, "Error", "Decrypted file failed to save")

    def monitor_resources(self, interval=1):
        cpu_usage, memory_usage = get_resource_usage(interval)
        return