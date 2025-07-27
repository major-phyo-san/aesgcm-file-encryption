import sys

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QLabel
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt

from pages.KeygenPage import KeygenPage
from pages.EncryptionPage import EncryptionPage
from pages.DecryptionPage import DecryptionPage

from MainAppTabs import MainAppTabs

class MainPage(QWidget):
    backgroundImage = "assets/background.jpg"

    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 8px;
                background-color: #0078D7;
                color: white;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #333;
            }
        """)

        self.set_background_image(self.backgroundImage)

        title = QLabel("AES GCM Audio File Encryption")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #001233;")

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.open_main_app)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addSpacing(40)
        main_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)        

    def open_main_app(self):
        self.stack.setCurrentIndex(1)

    def go_to_page(self, page_index):
        self.stack.setCurrentIndex(page_index)

    def set_background_image(self, image_path):
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.set_background_image(self.backgroundImage)
        super().resizeEvent(event)

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AES GCM File Encryption")
        self.setGeometry(0, 0, 400, 600)

        self.setWindowTitle("AES GCM File Encryption")
        self.setGeometry(0, 0, 400, 600)
        # self.setFixedSize(400, 600)

        self.main_page = MainPage(self)
        self.tabs_page = MainAppTabs(self)

        self.addWidget(self.main_page)   # index 0
        self.addWidget(self.tabs_page)   # index 1

        # self.main_page = MainPage(self)
        # self.page1 = KeygenPage(self)
        # self.page2 = EncryptionPage(self)
        # self.page3 = DecryptionPage(self)

        # self.addWidget(self.main_page)
        # self.addWidget(self.page1)
        # self.addWidget(self.page2)
        # self.addWidget(self.page3)

        self.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
