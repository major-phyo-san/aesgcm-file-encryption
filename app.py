import sys

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget
from PyQt6.QtGui import QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt

from pages.KeygenPage import KeygenPage
from pages.EncryptionPage import EncryptionPage
from pages.DecryptionPage import DecryptionPage

class MainPage(QWidget):
    backgroundImage = "assets/background.jpg"

    def __init__(self, stack):
        super().__init__()

        self.stack = stack

        self.set_background_image(self.backgroundImage) 

        # Create and configure buttons
        button1 = QPushButton("Key Generation")
        button2 = QPushButton("Encrypt Files")
        button3 = QPushButton("Decrypt Files")

        button1.setStyleSheet("font-size: 18px; color: #23198c; padding: 10px; background-color: rgba(179, 216, 227, 0.7);")
        button2.setStyleSheet("font-size: 18px; color: #23198c; padding: 10px; background-color: rgba(179, 216, 227, 0.7);")
        button3.setStyleSheet("font-size: 18px; color: #23198c; padding: 10px; background-color: rgba(179, 216, 227, 0.7);")

        button1.clicked.connect(lambda: self.go_to_page(1))
        button2.clicked.connect(lambda: self.go_to_page(2))
        button3.clicked.connect(lambda: self.go_to_page(3))

        # Layout for buttons (horizontal layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)

        # Center the buttons horizontally
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main layout for the page
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.setAlignment(button_layout, Qt.AlignmentFlag.AlignCenter)

        # Set layout
        self.setLayout(main_layout)

    def go_to_page(self, page_index):
        self.stack.setCurrentIndex(page_index)

    def set_background_image(self, image_path):
        # Set background image
        self.setAutoFillBackground(True)
        palette = self.palette()
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def resizeEvent(self, event):
        # Adjust background image on window resize
        self.set_background_image(self.backgroundImage)
        super().resizeEvent(event)

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        # Set main window size
        self.setWindowTitle("AES GCM File Encryption")
        self.setGeometry(0, 0, 1366, 768)

        # Create pages
        self.main_page = MainPage(self)
        self.page1 = KeygenPage(self)
        self.page2 = EncryptionPage(self)
        self.page3 = DecryptionPage(self)

        # Add pages to the stack
        self.addWidget(self.main_page)
        self.addWidget(self.page1)
        self.addWidget(self.page2)
        self.addWidget(self.page3)

        # Set initial page
        self.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
