from cx_Freeze import setup, Executable
import os
os.environ['TCL_LIBRARY'] = r'C:\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Python36\tcl\tk8.6'
base = "Win32GUI"
#base=None
#E:\_PYTHON_\VibHub-WoW\src
executables = [Executable("main_ui.py", base=base)]

packages = ["idna","multiprocessing"]
options = {
    'build_exe': {
        'packages':packages,
        'include_files':[
            r"C:\Python36\DLLs\tcl86t.dll",
            r"C:\Python36\DLLs\tk86t.dll"]
    },

}

setup(
    name = "VibHub WoW Connector",
    options = options,
    version = "0.1",
    description = 'VibHub Connector for World of Warcraft',
    executables = executables
)
