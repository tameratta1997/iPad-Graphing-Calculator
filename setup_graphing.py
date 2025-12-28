"""
Setup script for creating a macOS application bundle from the Graphing Calculator GUI.
Usage: python3 setup_graphing.py py2app
"""

from setuptools import setup

APP = ['gui_calculator_graphing.py']
DATA_FILES = ['calculator.py']  # Include the calculator module
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'Calculator.icns',  # Custom calculator icon
    'plist': {
        'CFBundleName': 'Graphing Calculator',
        'CFBundleDisplayName': 'Graphing Calculator',
        'CFBundleGetInfoString': "Scientific & Graphing Calculator",
        'CFBundleIdentifier': "com.graphingcalculator.app",
        'CFBundleVersion': "2.0.0",
        'CFBundleShortVersionString': "2.0.0",
        'NSHumanReadableCopyright': "Copyright © 2025",
        'LSMinimumSystemVersion': '10.13.0',
    },
    'packages': ['numpy', 'matplotlib'],
    'includes': ['math', 'calculator', 'numpy', 'matplotlib.backends.backend_tkagg'],
    'excludes': ['PyInstaller', 'gi', 'gtk', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6'],
    'frameworks': [],
    'matplotlib_backends': ['TkAgg'],
}

setup(
    name='Graphing Calculator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
