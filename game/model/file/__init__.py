from .file import File


_FILE = File('file.txt')
_BACKUP = File('backup.txt')


def close_all():
    _FILE.get().close()
    _BACKUP.get().close()


def read() -> str:
    return _FILE.read()


def write(msg: str):
    _backup()
    return _FILE.write(msg=msg)


def _backup():
    msg: str = read()
    _BACKUP.write(msg=msg)
