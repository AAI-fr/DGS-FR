from pathlib import Path

def get_biggest_nca(root_folder : str):
    nca_path = None
    biggest_size = 0
    for file in Path(root_folder).iterdir():
        if file.is_file() and file.suffix == '.nca':
            size = file.stat().st_size
            if size > biggest_size:
                biggest_size = size
                nca_path = file
    if not nca_path: raise Exception("Erreur: aucun fichier nca trouvé dans le dossier d'extraction")
    return nca_path

def get_tik(root_folder : str):
    for file in Path(root_folder).iterdir():
        if file.is_file() and file.suffix == '.tik':
            return file
    return 'placeholder'
