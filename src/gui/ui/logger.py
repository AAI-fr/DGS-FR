from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QPlainTextEdit
import sys

class StdoutStream(QObject):
    textWritten = Signal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

class Logger(QPlainTextEdit):
    def __init__(self):
        super().__init__(readOnly=True)
        self.stdout = StdoutStream(textWritten=self.write_log)
        sys.stdout = self.stdout

    def clear(self):
        self.setPlainText('')

    def write_log(self, text):
        self.insertPlainText(text)
        self.ensureCursorVisible()