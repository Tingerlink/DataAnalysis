import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
"includes": [],
"packages": [],
"excludes": [
        "collections.sys",
        "collections.abc",
    ],
"include_files": []}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32": base = "Win32GUI"

setup( name = "DataAnalysis",
       version = "0.1",
       description = u"DataAnalysis",
       options = {"build_exe": build_exe_options},
       executables = [Executable("DataAnalysis.py", base=base)])
