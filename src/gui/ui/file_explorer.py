from PySide6.QtWidgets import QHBoxLayout, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class FileExplorer(QWidget):
    def __init__(self, label, onPress):
        super().__init__()
        layout = QVBoxLayout()
        labelW = QLabel(label)
        layout.addWidget(labelW)
        hlayout = QHBoxLayout()
        inp = QLineEdit()
        inp.setReadOnly(True)
        self.setText = inp.setText
        button = QPushButton(text='Parcourir')
        button.clicked.connect(onPress)

        hlayout.addWidget(inp)
        hlayout.addWidget(button)
        layout.addLayout(hlayout)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)