from pathlib import Path
from src.utils import run_cli
from io import StringIO

def extract_cia(ctrtool_path : str, cia_path : str, tmp_path : str, log : StringIO = None):
    Path(tmp_path).mkdir(parents = True, exist_ok = True)
    run_cli([ctrtool_path, '-t', 'cia', f'--contents={Path(tmp_path, 'c')}', cia_path], log)
    run_cli([ctrtool_path, '-t', 'ncch', 
                f'--exheader={Path(tmp_path, 'exheader.bin')}',
                f'--exefs={Path(tmp_path, 'exefs.bin')}', 
                f'--romfs={Path(tmp_path, 'romfs.bin')}',
                f'{Path(tmp_path, 'c.0000.00000000')}'
                ], log)
    run_cli([ctrtool_path, '-t', 'exefs',
                f'--exefsdir={Path(tmp_path, 'exefs')}',
                f'{Path(tmp_path, 'exefs.bin')}'
                ], log)
    
def extract_cci(ctrtool_path : str, cci_path : str, tmp_path : str, log = None):
    Path(tmp_path).mkdir(exist_ok = True)
    run_cli([ctrtool_path, '-t', 'cci', f'--contents={tmp_path}', cci_path], log)
    run_cli([ctrtool_path, '-t', 'ncch', 
               f'--exheader={Path(tmp_path, 'exheader.bin')}',
                f'--exefs={Path(tmp_path, 'exefs.bin')}', 
                f'--romfs={Path(tmp_path, 'romfs.bin')}',
                f'{Path(tmp_path, '00_000400000014ad00.app')}'
                ], log)
    run_cli([ctrtool_path, '-t', 'exefs',
                f'--exefsdir={Path(tmp_path, 'exefs')}',
                f'{Path(tmp_path, 'exefs.bin')}'
                ], log)
    
def extract_rom(ctrtool_path : str, rom_path : str, tmp_path : str, log = None):
    if Path(rom_path).suffix == '.cia':
        extract_cia(ctrtool_path, rom_path, tmp_path, log)
    else:
        extract_cci(ctrtool_path, rom_path, tmp_path, log)
    
def extract_dlc_rom(ctrtool_path : str, cia_path : str, tmp_path : str, files : list[str], log = None):
    Path(tmp_path).mkdir(parents=True, exist_ok = True)
    run_cli([ctrtool_path, '-t', 'cia', f'--contents={Path(tmp_path, 'c')}', cia_path], log)
    for i, file in enumerate(files):
        Path(tmp_path, str(i)).mkdir(exist_ok=True)
        run_cli([ctrtool_path, '-t', 'ncch', 
                f'--exefs={Path(tmp_path, str(i), 'exefs.bin')}', 
                f'--romfs={Path(tmp_path, str(i), 'romfs.bin')}',
                Path(tmp_path, file)
                ], log)
    run_cli([ctrtool_path, '-t', 'exefs',
            f'--exefsdir={Path(tmp_path, '0', 'exefs')}',
            Path(tmp_path, '0', 'exefs.bin')
            ], log)