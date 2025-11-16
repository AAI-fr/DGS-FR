from PySide6.QtWidgets import QApplication
from src.window import MainWindow

def main():
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()

if __name__ == '__main__':
    main()