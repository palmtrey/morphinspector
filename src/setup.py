import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["scipy.optimize"]}

setup(name = "MyApp",
      version = "0.1",
      description = "My GUI App",
      executables = [Executable("morphinspector.py")])