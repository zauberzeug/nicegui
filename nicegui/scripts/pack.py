#!/usr/bin/env python
import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

import nicegui


def main() -> None:
    parser = argparse.ArgumentParser(description='Build a package of your NiceGUI app')
    parser.add_argument('--name', type=str, help='Name of your app', default='Your App Name')
    parser.add_argument('--add-data', type=str, help='Additional data to include', action='append', default=[
        f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    ])
    parser.add_argument('--dry-run', action='store_true', help='Dry run', default=False)
    parser.add_argument('main', help='Main file with ui.run()', default='main.py')
    args = parser.parse_args()

    for directory in ['build', 'dist']:
        if Path(directory).exists():
            Path(directory).rmdir()

    try:
        command = {
            'Windows': ['pyinstaller', '--onedir'],
            'Darwin': ['python', '-m', 'PyInstaller'],
            'Linux': ['python', '-m', 'PyInstaller'],
        }[platform.system()]
    except KeyError:
        print(f'Unsupported platform {platform.system()}')
        sys.exit(1)

    command.extend(['--name', args.name])
    for data in args.add_data:
        command.extend(['--add-data', data])
    command.extend(['--windowed'])
    command.extend([args.main])

    print('PyInstaller command:')
    print(' ', ' '.join(command))
    if args.dry_run:
        return

    subprocess.call(command)


if __name__ == '__main__':
    main()
