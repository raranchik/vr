import os
import sys


def get_root_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


OS_SEP = os.sep
ROOT_DIR = get_root_dir()

IPOPT_PATH = os.path.join(ROOT_DIR, f'solvers{OS_SEP}ipopt{OS_SEP}bin', 'ipopt.exe')
CBC_PATH = os.path.join(ROOT_DIR, f'solvers{OS_SEP}cbc{OS_SEP}bin', 'cbc.exe')
