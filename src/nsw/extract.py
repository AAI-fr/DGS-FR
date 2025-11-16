from pathlib import Path
from src.utils import run_cli
from .utils import get_biggest_nca, get_tik

def extract_nsp(nstool_path : str, nsp_path : str, keys_path : str, tmp_path : str, log = None):
    Path(tmp_path).mkdir(exist_ok = True, parents=True)
    run_cli([nstool_path, '-t', 'pfs', '-x', tmp_path, nsp_path], log)
    tik_path = get_tik(tmp_path)
    nca_path = get_biggest_nca(tmp_path)
    run_cli([nstool_path, '-t', 'nca', '-k', keys_path, '--tik', tik_path, '-x', tmp_path, nca_path], log)
