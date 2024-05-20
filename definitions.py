import os
import sys


def get_root_dir():
    base_path = ''
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)

    if "_internal" in os.listdir(base_path):
        base_path = os.path.join(base_path, '_internal')

    return base_path


OS_SEP = os.sep
ROOT_DIR = get_root_dir()

IPOPT_PATH = os.path.join(ROOT_DIR, f'solvers{OS_SEP}ipopt{OS_SEP}bin', 'ipopt.exe')
CBC_PATH = os.path.join(ROOT_DIR, f'solvers{OS_SEP}cbc{OS_SEP}bin', 'cbc.exe')

LP_ASSETS_PATH = os.path.join(ROOT_DIR, f'Core{OS_SEP}LP{OS_SEP}Assets{OS_SEP}')
