from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon
from src.utils import resource_path

class ErrorPopup(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Erreur")
        self.setWindowIcon(QIcon(resource_path('res/sad.png')))

    def exec_with_text(self, text : str):
        self.setText(text)
        self.exec()