from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFileDialog, QPushButton
from PySide6.QtGui import QIcon
from .gui import CtrWidget, StmWidget, NswWidget, FileExplorer, ErrorPopup, Navigation
import src.aapatch as aapatch
from src.utils import resource_path

class MainWindow(QMainWindow):
    patch_path : str
    patch_flag : int
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Patch FR The Chronicles of Ace Attorney - A Great Era')
        self.setWindowIcon(QIcon(resource_path('res/icon.png')))
        self.setMinimumWidth(350)

        self.explorer = FileExplorer('Veuillez sélectionner un patch.', onPress=self.loadPatch)
        self.button = QPushButton('Valider')
        self.button.clicked.connect(self.onValidate)
        self.button.setDisabled(True)

        nav = Navigation()

        layout = QVBoxLayout()
        layout.addWidget(self.explorer)
        layout.addWidget(self.button)
        layout.addWidget(nav)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.error_win = ErrorPopup()

    def loadPatch(self):
        filepath, _ = QFileDialog.getOpenFileName(
            caption='Sélectionnez un patch.', 
            filter="AA Patch (*.aapatch)")
        if filepath == '': return
        try:
            patch = aapatch.load(filepath)
            self.patch_flag = patch.flag
            self.patch_path = filepath
            self.button.setEnabled(True)
            self.explorer.setText(filepath)
        except Exception as e:
            self.error_win.exec_with_text(str(e))

    def onValidate(self):
        match self.patch_flag:
            case 0:
                self.setCentralWidget(CtrWidget(self.patch_path, 'DGS1'))
            case 1:
                self.setCentralWidget(CtrWidget(self.patch_path, 'DGS2'))
            case 2:
                self.setMinimumWidth(475)
                self.setCentralWidget(StmWidget(self.patch_path))
            case 3:
                self.setMinimumWidth(475)
                self.setCentralWidget(NswWidget(self.patch_path))
            
            case _:
                self.error_win.exec_with_text("Ce patch n'est pas supporté avec cette version du patcheur")

