import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


install('pandas')
install('regex')
install('pathlib2')
input('Sprawdź czy nie wystąpił błąd!')
