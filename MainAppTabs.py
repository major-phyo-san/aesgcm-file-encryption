from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout

from pages.EncryptionPage import EncryptionPage
from pages.DecryptionPage import DecryptionPage

class MainAppTabs(QWidget):
    def __init__(self, stack):
        super().__init__()
        tabs = QTabWidget()
        tabs.addTab(EncryptionPage(stack), "Encrypt")
        tabs.addTab(DecryptionPage(stack), "Decrypt")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)