from src.utils import EndianBinaryFileReader
from pathlib import Path

class RomIsEncrypted(Exception):
    pass

class InvalidRomId(Exception):
    pass

CTR_ALIGN = 0x40

def check_rom(rom_path : str, id : int):
    with EndianBinaryFileReader(rom_path) as f:
        if Path(rom_path).suffix == '.cia':
            header_size = f.read_UInt32()
            f.seek(8)
            certificate_size = f.read_UInt32()
            ticket_size = f.read_UInt32()
            tmd_size = f.read_UInt32()
            f.seek(header_size)
            f.seek(certificate_size, 1)
            f.align(CTR_ALIGN)
            f.seek(ticket_size, 1)
            f.align(CTR_ALIGN)
            f.seek(tmd_size, 1)
            f.align(CTR_ALIGN)

        else:
            f.seek(0x120)
            ncch_offset = f.read_UInt32() * 0x200
            f.seek(ncch_offset)

        # ncch
        f.seek(0x100, 1)
        magic = f.read(4)
        if magic != b'NCCH':
            raise RomIsEncrypted('Erreur : la rom du jeu est chiffrée. Une 3DS hackée est requise pour la déchiffrer.')
        f.seek(0x4, 1)
        rom_id = f.read_UInt64()
        if rom_id != id:
            raise InvalidRomId(f"Erreur : l'id de la rom n'est pas bonne. Assurez-vous d'avoir sélectionné la bonne rom.\nId de la rom : {hex(rom_id)}\nAttendu : {hex(id)}")
        return True
    
def get_correct_cci_apps(root_dir : str):
    main_app = None
    manual_app = None
    for file in Path(root_dir).iterdir():
        if file.is_file() and file.suffix == '.app' and file.name.startswith('00_'): 
            main_app = file.name
        if file.is_file() and file.suffix == '.app' and file.name.startswith('01_'): 
            manual_app = file.name
    if not main_app:
        raise Exception("Erreur lors de l'extraction de la ROM : le ncch0 n'a pas pu être localisé")
    return main_app, manual_app