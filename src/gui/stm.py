from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QPushButton, QHBoxLayout
from .ui import ErrorPopup, FileExplorer, Logger, QImage, Navigation, SuccessPopup
from pathlib import Path
from PySide6.QtCore import Qt
import src.aapatch as aapatch
from src.utils import uprint, resource_path

WIN_DEFAULT_PATH = r'C:\Program Files (x86)\Steam\steamapps\common\TGAAC'

class StmWidget(QWidget):
    game_root : str = ''
    def __init__(self, patch_path : str):
        super().__init__()
        self.patch_path = patch_path
        if Path(WIN_DEFAULT_PATH, 'TGAAC.exe').exists():
            self.game_root = WIN_DEFAULT_PATH
        im = QImage(resource_path('res/logo.png'))
        self.explorer = FileExplorer("Sélectionnez le dossier d'installation du jeu", onPress=self.get_path)
        self.explorer.setText(self.game_root)
        self.button = QPushButton("C'est parti !")
        self.button.setDisabled(self.game_root == '')
        self.button.clicked.connect(self.patch)
        self.logger = Logger()
        self.success = SuccessPopup()
        nav = Navigation()
        layout = QVBoxLayout()
        im_layout = QHBoxLayout()
        im_layout.addWidget(im)
        im_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(im_layout)
        layout.addWidget(self.explorer)
        layout.addWidget(self.button)
        layout.addWidget(self.logger)
        layout.addWidget(nav)
        layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(layout)
        self.error_win = ErrorPopup()

    def get_path(self):
        root_path = QFileDialog.getExistingDirectory(
            caption="Sélectionnez le dossier d'installation du jeu.", 
            )
        if root_path != '': 
            self.game_root = root_path
            self.explorer.setText(root_path)
            self.button.setEnabled(True)

    def patch(self):
        self.logger.clear()
        try:
            patch = aapatch.load(self.patch_path)
            patch.patch_all(self.game_root)
            uprint('Patch terminé !')
            self.success.exec_with_text("Le patch a bien été appliqué.\nBon jeu dans la langue de Molière !")
        except Exception as e:
            self.error_win.exec_with_text(str(e))
