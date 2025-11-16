from xxhash import xxh32_digest
from PySide6.QtCore import QCoreApplication
from pathlib import Path
import subprocess
import platform
import sys
import os

def get_file_hash(filepath : str):
    return xxh32_digest(get_file_data(filepath))

def get_file_data(filepath : str):
    with open(filepath, 'rb') as fr:
        data = fr.read()
    return data

def write_file_data(filepath : str, data : bytes):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, mode='wb') as fw:
        fw.write(data)

def uprint(text : str):
    print(text)
    QCoreApplication.processEvents()

def run_cli(command : list, stdout):
    if platform.system() == 'Windows':
        subprocess.check_call(command, stdout=stdout, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        subprocess.check_call(command, stdout=stdout)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    