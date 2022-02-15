import sys
from cx_Freeze import setup, Executable
setup(name="Practica_1", version="1.0", description="",
       executables=[Executable("main.py", base="Win32GUI")])
