import subprocess
import sys
import os


def install():
    here = os.path.abspath(os.path.dirname(__file__))
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(here, "requirements.txt")])

if __name__ == "__main__":
    install()
    input('Sprawdź czy nie wystąpił błąd!')
