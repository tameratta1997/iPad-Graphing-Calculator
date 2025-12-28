"""
Setup script for creating a macOS application bundle from the Calculator GUI.
Usage: python3 setup.py py2app
"""

from setuptools import setup

APP = ['gui_calculator.py']
DATA_FILES = ['calculator.py']  # Include the calculator module
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'Calculator.icns',  # Custom calculator icon
    'plist': {
        'CFBundleName': 'Calculator',
        'CFBundleDisplayName': 'Calculator',
        'CFBundleGetInfoString': "Scientific Calculator",
        'CFBundleIdentifier': "com.calculator.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2025",
        'LSMinimumSystemVersion': '10.13.0',
    },
    'packages': ['tkinter'],
    'includes': ['math', 'calculator'],
}

setup(
    name='Calculator',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
