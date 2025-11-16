from PySide6.QtWidgets import QHBoxLayout, QWidget, QPushButton, QMessageBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from .qimage import QImage
import webbrowser
from src.utils import resource_path

def callback(url : str):
    webbrowser.open_new_tab(url)

class ImageLink(QImage):
    def __init__(self, im_path : str, url : str):
        super().__init__(resource_path(im_path))
        self.mousePressEvent = lambda e: callback(url)
        self.setCursor(Qt.PointingHandCursor)

class Navigation(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        group_icon_layout = QHBoxLayout()

        text = open(resource_path('res/credits.txt'), encoding='utf-8').read()
        credits = QMessageBox()
        credits.setText(text)
        credits.setWindowTitle('Crédits')
        credits.setWindowIcon(QIcon(resource_path('res/icon.png')))

        discord = ImageLink('res/discord.png', 'https://discord.gg/bye98cMs8S')
        web = ImageLink('res/aaifr.png', 'https://aai-fr.keuf.net/')
        github = ImageLink('res/github.png', 'https://github.com/AAI-fr/DGS-FR')

        button = QPushButton()
        button.setText('Crédits')
        button.clicked.connect(lambda e: credits.exec_())

        group_icon_layout.addWidget(web)
        group_icon_layout.addWidget(discord)
        group_icon_layout.addWidget(github)
        group_icon_layout.setAlignment(Qt.AlignLeft)

        layout.addLayout(group_icon_layout)
        layout.addWidget(button)

        self.setLayout(layout)
