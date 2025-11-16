from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QPushButton, QHBoxLayout
from .ui import ErrorPopup, FileExplorer, Logger, QImage, Navigation, SuccessPopup
from PySide6.QtCore import Qt
from src.nsw import extract_nsp
from src.utils import uprint, resource_path
from pathlib import Path
import src.aapatch as aapatch
import os
import shutil

NSTOOL = resource_path(Path('cltools', 'nstool'))

class NswWidget(QWidget):
    rom_path : str = ''
    keys_path : str = ''
    def __init__(self, patch_path : str):
        super().__init__()
        self.patch_path = patch_path
        self.keys_explorer = FileExplorer("Sélectionnez le fichier prod.keys", onPress=self.get_keys_path)
        self.rom_explorer = FileExplorer("Sélectionnez la ROM du jeu", onPress=self.get_rom_path)
        self.button = QPushButton("C'est parti !")
        self.button.setDisabled(True)
        self.button.clicked.connect(self.patch)
        self.logger = Logger()
        self.success = SuccessPopup()
        im = QImage(resource_path('res/logo.png'))
        nav = Navigation()
        layout = QVBoxLayout()
        im_layout = QHBoxLayout()
        im_layout.addWidget(im)
        im_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(im_layout)
        layout.addWidget(self.keys_explorer)
        layout.addWidget(self.rom_explorer)
        layout.addWidget(self.button)
        layout.addWidget(self.logger)
        layout.addWidget(nav)
        self.setLayout(layout)
        self.error_win = ErrorPopup()

    def get_keys_path(self):
        keys_path, _ = QFileDialog.getOpenFileName(
            caption='Sélectionnez le fichier prod.keys.', 
            filter="Clefs de déchiffrement Switch (*.keys)")
        if keys_path != '': 
            self.keys_path = keys_path
            self.keys_explorer.setText(keys_path)
        self.update_button_state()

    def get_rom_path(self):
        rom_path, _ = QFileDialog.getOpenFileName(
            caption='Sélectionnez la ROM du jeu.', 
            filter="ROM Switch (*.nsp)")
        if rom_path != '': 
            self.rom_path = rom_path
            self.rom_explorer.setText(rom_path)
        self.update_button_state()

    def update_button_state(self):
        if self.rom_path != '' and self.keys_path != '':
            self.button.setEnabled(True)
        else:
            self.button.setDisabled(True)

    def patch(self):
        try:
            uprint('Extraction des fichiers (cela peut prendre quelques minutes)...')
            tmp_path = 'tmp_' + os.urandom(4).hex()
            f = open('log.txt', mode='w', encoding='utf-8')
            extract_nsp(NSTOOL, self.rom_path, self.keys_path, tmp_path, log=f)
            patch = aapatch.load(self.patch_path)
            patch.patch_all(Path(tmp_path, '1'), new_path=Path('010036e00fb20000', 'romfs'))
            uprint('Patch terminé !')
            self.success.exec_with_text('Le patch a bien été appliqué.\nCopiez le dossier 010036e00fb20000 dans le dossier atmosphere/contents de la carte SD de votre Switch.\nSi vous avez la version japonaise, renommez ce dossier en 0100d7f00fb1a000.\nBon jeu dans la langue de Molière !')
        except Exception as e:
            self.error_win.exec_with_text(str(e))
        finally:
            f.close()
            if Path(tmp_path).is_dir():
                shutil.rmtree(tmp_path)
