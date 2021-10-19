import os
import sys
import winreg as reg

option_name = input('Podaj nazwę funkcji')

# Get path of current working directory and python.exe
cwd = os.getcwd()
python_exe = sys.executable

# optional hide python terminal in windows
hidden_terminal = '\\'.join(python_exe.split('\\')[:-1])+"\\pythonw.exe"

# Set the path of the context menu (right-click menu)
key_path = r'SystemFileAssociations\\.txt\\shell\\' + option_name + r'\\' # Change 'Organiser' to the name of your project

# Create outer key
key = reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path)
reg.SetValue(key, '', reg.REG_SZ, '&' + option_name)  # Change 'Organise folder' to the function of your script

# create inner key
key1 = reg.CreateKey(key, r"command")
reg.SetValue(key1, '', reg.REG_SZ, python_exe + f' "{cwd}\\Numeracja.py"' + ' "%1"') # change 'file_organiser.py' to the name of your script
# reg.SetValue(key1, '', reg.REG_SZ, hidden_terminal + f' "{cwd}\\file_organiser.py"')  # use to to hide terminal
# Komputer\HKEY_CLASSES_ROOT\SystemFileAssociations\.txt\shell\Numeracja\command
# C:\Users\Antek\PycharmProjects\pythonProject\venv\Scripts\python.exe "C:\Users\Antek\PycharmProjects\pythonProject\Numeracja.py"
# Komputer\HKEY_CLASSES_ROOT\Directory\Background\shell\Int\command
