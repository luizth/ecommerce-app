import os

from .path import get_root_path


class Logger:
    PATH: str

    def __init__(self, context: str):
        self.PATH = f'{get_root_path()}/logs/{context}.log'

    def insert(self, msg: str):
        with open(self.PATH, 'a') as log_f:
            log_f.write(msg + '\n')
