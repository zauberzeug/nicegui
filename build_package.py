import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

import nicegui

APP_NAME = 'Your App Name'


def remove(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def build_windows():
    return [
        'pyinstaller',
        'main.py',  # your main file with ui.run()
        '--name', APP_NAME,  # name of your app
        '--onedir',
        '--windowed',
        # '--icon', 'AppIcon.ico' # your custom app icon
    ]


def build_macos():
    return [
        'python',
        '-m', 'PyInstaller',
        'main.py',  # your main file with ui.run()
        '--name', APP_NAME,  # name of your app
        '--windowed',
        # '--icon', 'AppIcon.icns' # your custom app icon
    ]


def build_linux():
    return [
        'python',
        '-m', 'PyInstaller',
        'main.py',  # your main file with ui.run()
        '--name', APP_NAME,  # name of your app
        '--windowed'
    ]


build_matrix = {
    'Windows': build_windows,
    'Darwin': build_macos,
    'Linux': build_linux
}

common_data_params = [
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    # '--add-data', f'assets{os.pathsep}assets' # you can add your own additional resources
]

if __name__ == "__main__":
    platform_name = platform.system()

    if platform_name not in build_matrix:
        print(f'Unsupported platform {platform_name}')
        sys.exit(1)

    remove('build')
    remove('dist')

    subprocess.call(build_matrix[platform_name]() + common_data_params)
