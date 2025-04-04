import os
import time
import tracemalloc

from datetime import datetime

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QTextEdit, QMessageBox, QFileDialog, QDialog
from PyQt6.QtCore import Qt

from helpers.analytics import get_resource_usage
from helpers.keygen import generate_key

class KeygenPage(QWidget):
    def __init__(self,stack):
        super().__init__()

        self.stack = stack
        self.keypair = None

        pageLabel = QLabel("Key Generation")
        pageLabel.setStyleSheet("font-size: 24px; padding: 10px;")

        # Create and configure select box
        self.options = {
            "ed25519",  # default
            "secp224r1",
            "secp256k1",  # Used in Bitcoin & Ethereum
            "secp256r1",  # General-Purpose (Web, TLS, Digital Signatures, Blockchain), (NIST P-256), Same as prime256v1
            "secp384r1",  # Higher Security (Government, Long-Term Security)
            "secp521r1",  # Ultra-Secure (Rare Use Cases, High Computational Power)
            "prime192v1",  # Same as secp192r1
            "prime256v1",  # Same as secp256r1
        }
        self.select_box = QComboBox()
        self.select_box.addItems(self.options)
        self.select_box.setStyleSheet("font-size: 18px; padding: 5px; width: 120px; height: 30px;")

        #  Create and configure buttons
        keygen_button = QPushButton("Generate AES GCM Key")
        keygen_button.setStyleSheet("font-size: 18px; padding: 10px;")
        keygen_button.clicked.connect(self.keygen_btn_clicked)

        # Create and configure the "Save As" button
        save_button = QPushButton("Save Key")
        save_button.setStyleSheet("font-size: 18px; padding: 10px;")
        save_button.clicked.connect(self.save_keys)

        # Layout for button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        # button_layout.addWidget(self.select_box)
        button_layout.addWidget(keygen_button)
        button_layout.addWidget(save_button)
        button_layout.addStretch(1)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 18px; padding: 10px;")
        back_button.clicked.connect(self.go_back)

        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("font-size: 18px; padding: 10px;")
        clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout()
        layout.addWidget(pageLabel)
        layout.addLayout(button_layout)
        layout.addWidget(clear_button)     
        layout.addWidget(back_button)       
        layout.setAlignment(pageLabel, Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(back_button, Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(clear_button, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def go_back(self):
        self.keypair = None
        self.stack.setCurrentIndex(0)     

    def clear(self):
        self.keypair = None
    
    def keygen_btn_clicked(self):
        # selected_label = self.select_box.currentText();
        # print(f"Keygen btn clicked with option {selected_label}")
        tracemalloc.start()
        start_time = time.time()
        self.keypair = generate_key()
        if not self.keypair:
            QMessageBox.warning(self, "Warning", "Key generation failed")
            return
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        time_taken_ms = (end_time - start_time) * 1000
        cpu_usage, memory_usage = self.monitor_resources()
        print(f"Time taken {round(time_taken_ms, 4)} ms")
        print(f"CPU usage {cpu_usage} %")
        print(f"Memory usage {memory_usage} %")
        QMessageBox.information(self, "Success", f"Key generated successfully.")
    
    def save_keys(self):
        """Generate a key pair and save them to the selected directory."""
        # Get a directory from the user
        if not self.keypair:
            QMessageBox.critical(self, "Error", "No key to save.")
            return
        directory = QFileDialog.getExistingDirectory(self, "Select Save Directory")

        if directory:  # Ensure the user selected a valid directory
            key = self.keypair
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            keyname = f"{timestamp}_aes_key.key"
            keypath = os.path.join(directory, keyname)

            try:
                # Save the key
                with open(keypath, "wb") as key_file:
                    key_file.write(key)
                # Show success message
                QMessageBox.information(self, "Success", f"Key saved to:\n{directory}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save key:\n{str(e)}")

    def monitor_resources(self, interval=1):
        cpu_usage, memory_usage = get_resource_usage(interval)
        return cpu_usage, memory_usage