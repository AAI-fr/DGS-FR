from pathlib import Path
from src.utils import run_cli

def build_cia(makerom_path : str, input_dir : str, dist_path : str, rsf_dir : str, log = None):
    logo_command = []
    if Path(input_dir, "logo.bin").is_file():
        logo_command = ["-logo", Path(input_dir, "logo.bin")]
    elif Path(input_dir, 'exefs', 'logo.bin').is_file():
        logo_command = ["-logo", Path(input_dir, 'exefs', 'logo.bin')]
    run_cli([
        makerom_path, "-f", "ncch", "-target", "t",
        "-code", Path(input_dir, 'exefs', 'code.bin'),
        "-banner", Path(input_dir, 'exefs', 'banner.bin'),
        "-icon", Path(input_dir, 'exefs', 'icon.bin'), 
        "-rsf", Path(rsf_dir, 'ncch0.rsf'), 
        "-romfs", Path(input_dir, 'romfs.bin'), 
        "-exheader", Path(input_dir, 'exheader.bin'), 
        "-plainrgn", Path(input_dir, 'plainrgn.bin')
        ] 
        + logo_command 
        + ["-o", Path(input_dir, "c.0000.00000000")]
        , log)
    # emanual_command = []
    # if Path(input_dir, "c.0001.00000001").is_file():
        # emanual_command = ["-i", Path(input_dir, "c.0001.00000001:0001:00000001"),]
    run_cli([
        makerom_path, "-f", "cia", 
        "-i", Path(input_dir, "c.0000.00000000:0000:00000000")]
        # + emanual_command
        + [ "-o", dist_path ], log)
    
def build_dlc_cia(makerom_path : str, input_dir : str, dist_path : str, rsf_dir : str, log = None):
    files = [file for file in Path(input_dir).iterdir() if file.is_file()]
    cia_command = [makerom_path, "-f", "cia", "-o", dist_path, '-rsf', Path(rsf_dir, 'dlc_rom.rsf'), '-dlc']
    for file in files:
        _, ncch_idx, unk = file.name.split('.')
        idx = int(ncch_idx, 16)
        ncch_command = [
            makerom_path, "-f", "ncch", "-target", "t",
            "-rsf", Path(rsf_dir, 'dlc_ncch.rsf'), 
            "-romfs", Path(input_dir, str(idx), 'romfs.bin'),
            "-o", file
            ]
        if idx == 0:
            ncch_command.append("-icon")
            ncch_command.append(Path(input_dir, str(idx), 'exefs', 'icon.bin'))
        run_cli(ncch_command, log)
        cia_command.append('-i')
        cia_command.append(Path(input_dir, f'{file.name}:0x{ncch_idx}:0x{unk}'))
    run_cli(cia_command, log)
