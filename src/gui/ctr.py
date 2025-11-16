from PySide6.QtWidgets import QWidget, QFileDialog, QVBoxLayout, QPushButton
from src.ctr import check_rom, extract_rom, extract_dlc_rom, build_cia, build_dlc_cia
from .ui import ErrorPopup, FileExplorer, Logger, QImage, Navigation, SuccessPopup
from pathlib import Path
from src.utils import uprint, resource_path
import src.aapatch as aapatch
import os
import shutil

class DGS1_Info:
    game_id = 0x400000014AD00
    dlc_id =  0x4008C0014AD00
    game_name = 'TCAA_AGE_Aventures_Patch_FR.cia'
    dlc_name = 'TCAA_AGE_Aventures_DLC_Patch_FR.cia'
    logo_path = resource_path('res/logo_dgs1.png')
    rsf_path = resource_path(Path('res', 'ctr', 'dgs1'))
    dlc_files = [
            'c.0000.0000001f', 'c.0001.00000001', 'c.0002.00000011', 
            'c.0003.00000012', 'c.0004.00000013', 'c.0005.00000020', 
            'c.0006.00000021', 'c.0007.00000022', 'c.0008.00000023', 
            'c.0009.00000024', 'c.000a.00000025', 'c.000b.0000001a', 
            'c.000c.0000001b', 'c.000d.0000001c', 'c.000e.0000001d', 
            'c.000f.0000001e']

class DGS2_Info:
    game_id = 0x40000001AE200
    dlc_id =  0x4008C001AE200
    game_name = 'TCAA_AGE_Détermination_Patch_FR.cia'
    dlc_name = 'TCAA_AGE_Détermination_DLC_Patch_FR.cia'
    logo_path = resource_path('res/logo_dgs2.png')
    rsf_path = resource_path(Path('res', 'ctr', 'dgs2'))
    dlc_files = ['c.0000.00000003', 'c.0001.00000004', 'c.0002.00000005']

CTRTOOL = resource_path(Path('cltools', 'ctrtool'))
MAKEROM = resource_path(Path('cltools', 'makerom'))

class CtrWidget(QWidget):
    game_rom_path : str = ''
    dlc_rom_path : str = ''

    def __init__(self, patch_path : str, game : str):
        super().__init__()
        if game == 'DGS1':
            self.info = DGS1_Info()
        elif game == 'DGS2':
            self.info = DGS2_Info()
        self.patch_path = patch_path
        self.game_explorer = FileExplorer('Sélectionnez la ROM japonaise du jeu', self.get_game_path)
        self.dlc_explorer = FileExplorer('Sélectionnez la ROM DLC japonaise du jeu', self.get_dlc_path)
        im = QImage(self.info.logo_path)
        layout = QVBoxLayout()
        self.button = QPushButton("C'est parti !")
        self.button.setDisabled(True)
        self.button.clicked.connect(self.patch)
        self.log = Logger()
        self.success = SuccessPopup()
        nav = Navigation()
        layout.addWidget(im)
        layout.addWidget(self.game_explorer)
        layout.addWidget(self.dlc_explorer)
        layout.addWidget(self.button)
        layout.addWidget(self.log)
        layout.addWidget(nav)
        self.setLayout(layout)
        self.error_win = ErrorPopup()

    def get_game_path(self):
        filepath, _ = QFileDialog.getOpenFileName(
            caption='Sélectionnez la ROM japonaise du jeu.', 
            filter="ROM 3DS (*.cia *.3ds)")
        if filepath == '': return
        try:
            if check_rom(filepath, self.info.game_id):
                self.game_rom_path = filepath
                self.game_explorer.setText(self.game_rom_path)
                self.button.setEnabled(True)
        except Exception as e:
            self.error_win.exec_with_text(str(e))

    def get_dlc_path(self):
        filepath, _ = QFileDialog.getOpenFileName(
            caption='Sélectionnez la ROM DLC japonaise du jeu.', 
            filter="ROM DLC 3DS (*.cia)")
        if filepath == '': return
        try:
            if check_rom(filepath, self.info.dlc_id):
                self.dlc_rom_path = filepath
                self.dlc_explorer.setText(self.dlc_rom_path)
        except Exception as e:
            self.error_win.exec_with_text(str(e))

    def patch(self):
        try:
            tmp_path = 'tmp_' + os.urandom(4).hex()
            f = open('log.txt', mode='w', encoding='utf-8')
            if self.game_rom_path != '':
                uprint('Extraction des fichiers...')
                extract_rom(CTRTOOL, self.game_rom_path, Path(tmp_path, 'Game'), log=f)
                uprint('Extraction  !')
            if self.dlc_rom_path != '':
                uprint('Extraction des fichiers DLC...')
                extract_dlc_rom(CTRTOOL, self.dlc_rom_path, Path(tmp_path, 'DLC'), self.info.dlc_files, log=f)
                uprint('Extraction terminée !')
            uprint('Patch des fichiers...')
            patch = aapatch.load(self.patch_path)
            if self.game_rom_path != '': patch.patch_all(Path(tmp_path, 'Game'), flags=[1])
            if self.dlc_rom_path != '': patch.patch_all(Path(tmp_path), flags=[2])
            if self.game_rom_path != '':
                uprint('Reconstruction de la ROM...')
                build_cia(MAKEROM, Path(tmp_path, 'Game'), self.info.game_name, self.info.rsf_path, log=f)
                uprint('ROM construite avec succès !')
            if self.dlc_rom_path != '':
                uprint('Reconstruction de la ROM DLC...')
                build_dlc_cia(MAKEROM, Path(tmp_path, 'DLC'), self.info.dlc_name, self.info.rsf_path, self.info.dlc_files, log=f)
                uprint('ROM DLC construite avec succès !')
            self.success.exec_with_text('Patch appliqué avec succès.\nVous trouverez la ou les ROMs en français dans le dossier du patcheur.\nBon jeu dans la langue de Molière !')
        except Exception as e:
            self.error_win.exec_with_text(str(e))
        finally:
            f.close()
            if Path(tmp_path).is_dir():
                shutil.rmtree(tmp_path)
        