

class File:

    def __init__(self, name):
        from ...constants import ASSETS_PATH
        from typing import TextIO
        self._name = ASSETS_PATH + 'txt/' + name
        try:
            self._file: TextIO = open(file=self._name, mode='r')
        except FileNotFoundError:
            self._file: TextIO = open(file=self._name, mode='w')

    def read(self):
        if self._file.readable() and not self._file.closed:
            self._file.seek(0)
        else:
            if not self._file.closed:
                self._file.close()
            self._file = open(file=self._name, mode='r')
        return self._file.read().rstrip()

    def write(self, msg: str):
        if self._file.closed:
            self._file = open(file=self._name, mode='w')
        if not self._file.writable():
            if not self._file.closed:
                self._file.close()
            self._file = open(file=self._name, mode='w')
        return self._file.write(msg)

    def get(self):
        return self._file
