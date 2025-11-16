from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap

class QImage(QLabel):
    def __init__(self, im_path : str):
        super().__init__()
        pixmap = QPixmap(im_path)
        self.setPixmap(pixmap)
