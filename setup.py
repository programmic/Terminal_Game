import sys
from cx_Freeze import setup, Executable

# Abhängigkeiten werden automatisch erkannt, aber es kann nötig sein, sie anzupassen.
build_exe_options = {
   "excludes": ["tkinter", "unittest"],
   "zip_include_packages": ["encodings", "PySide6"],
}

# base="Win32GUI" sollte nur mit der Windows GUI App verwendet werden
base = "Win32GUI" if sys.platform == "win32" else None

setup(
   name="main",
   version="0.1",
   description="Terminal Game v0.3",
   options={"build_exe": build_exe_options},
   executables=[Executable("main.py", base=base)],
)