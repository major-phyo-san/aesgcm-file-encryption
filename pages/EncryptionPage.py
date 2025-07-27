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
from helpers.encrypt import encrypt_file, save_encrypted_to_file
from helpers.keygen import generate_key

class EncryptionPage(QWidget):
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

        # QLabel {
        #     font-size: 13px;
        # }
        
        pageLabel = QLabel("Audio File Encryption")
        pageLabel.setFont(QFont("Arial", 40, QFont.Weight.Bold))
        pageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a horizontal line separator below the heading
        heading_separator = QFrame()
        heading_separator.setFrameShape(QFrame.Shape.HLine)
        heading_separator.setFrameShadow(QFrame.Shadow.Sunken)
        heading_separator.setStyleSheet("margin-bottom: 18px; margin-top: 8px;")
        heading_separator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        heading_separator.setMinimumWidth(400)  # Adjust width as needed

        self.docfile_button = QPushButton("Select File")
        self.docfile_button.clicked.connect(self.pick_doc_file)
        self.docfile_label = QLabel("No file selected")
        self.docfile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        docfile_frame = QFrame()
        docfile_layout = QVBoxLayout(docfile_frame)
        docfile_layout.addWidget(self.docfile_button)
        docfile_layout.addWidget(self.docfile_label)

        self.privatekeyfile_button = QPushButton("Select Key File")
        self.privatekeyfile_button.clicked.connect(self.pick_privatekey_file)
        self.privatekeyfile_label = QLabel("No key selected")

        privatekeyfile_frame = QFrame()
        privatekeyfile_layout = QHBoxLayout(privatekeyfile_frame)
        privatekeyfile_layout.addWidget(self.privatekeyfile_button)
        privatekeyfile_layout.addWidget(self.privatekeyfile_label)

        self.analysis_output_label = QLabel("Calculation Analysis:")
        self.analysis_output = QTextEdit()
        self.analysis_output.setReadOnly(True)
        self.analysis_output.setFixedHeight(50)

        encrypt_button = QPushButton("Encrypt")
        encrypt_button.clicked.connect(self.encrypt_btn_clicked)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_btn_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(encrypt_button)
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
        # content_layout.addWidget(self.analysis_output_label, alignment=Qt.AlignmentFlag.AlignCenter)
        # content_layout.addWidget(self.analysis_output, alignment=Qt.AlignmentFlag.AlignCenter)
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
        self.privatekey_file_path = None
        self.encrypted = None
        self.signature = None
        self.key = None

    def go_back(self):
        self.clear()
        self.stack.setCurrentIndex(0)

    def clear(self):
        self.docfile_path = None
        self.privatekey_file_path = None
        self.encrypted = None
        self.signature = None
        self.key = None
        self.analysis_output.clear()
        self.docfile_label.setText("No file selected")
        # self.privatekeyfile_label.setText("No key selected")

    def pick_doc_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.flac *.aac *.ogg *.m4a)")
        if file_path:
            file_size = os.stat(file_path).st_size / 1024
            self.docfile_path = file_path
            file_name = os.path.basename(file_path)  # <-- Get just the file name
            label_text = f"Audio file selected, (Name: {file_name}, Size: {file_size:.2f} KB)"
            self.docfile_label.setText(label_text)

    def pick_privatekey_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Key", "", "Key Files (*.key)")
        if file_path:
            self.privatekey_file_path = file_path
            self.privatekeyfile_label.setText("Key selected")

    def encrypt_btn_clicked(self):
        if not self.docfile_path:
            QMessageBox.warning(self, "Warning", "No audio file selected")
            return

        self.analysis_output.clear()
        try:
            tracemalloc.start()
            start_time = time.time()
            self.key = generate_key()
            self.encrypted = encrypt_file(self.docfile_path, self.key)
            end_time = time.time()
            _, peak = tracemalloc.get_traced_memory()
            time_taken_ms = (end_time - start_time) * 1000

            time_analysis = f"Time taken: {time_taken_ms:.2f} ms\nMemory usage: {peak / 1024:.2f} KB"
            self.analysis_output.setText(time_analysis)

            QMessageBox.information(self, "Success", "Audio file encrypted successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_btn_clicked(self):
        if not self.encrypted:
            QMessageBox.warning(self, "Warning", "No encrypted data to save")
            return

        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        try:
            info = save_encrypted_to_file(self.encrypted, self.key, directory)
            QMessageBox.information(self, "Success", info)
        except Exception as e:
            QMessageBox.critical(self, "Error", "Encrypted file failed to save")

    def monitor_resources(self, interval=1):
        cpu_usage, memory_usage = get_resource_usage(interval)
        return cpu_usage, memory_usage
