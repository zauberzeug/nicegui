#!/usr/bin/env python
import argparse
import os
import platform
import subprocess
from contextlib import suppress
from pathlib import Path

import nicegui

DESCRIPTION = '''
Build a package of your NiceGUI app
-----------------------------------

NiceGUI apps can be bundled into an executable with PyInstaller.
This allows you to distribute your app as a single file that can be executed on any computer.
Use this script as a starting point to create a package for your app.

Important: Make sure to run your main script with

    ui.run(reload=False, port=native.find_open_port(), ...)

to disable the reload server and to automatically find an open port.

For more information and packaging tips, have a look into the NiceGUI documentation:
https://nicegui.io/documentation/section_configuration_deployment#package_for_installation.
'''.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--name', type=str, default='Your App Name', help='Name of your app.')
    parser.add_argument('--windowed', action='store_true', default=False, help=(
        'Prevent a terminal console from appearing.\n'
        'Only use with `ui.run(native=True, ...)`.\n'
        'It will create an `.app` file on Mac which runs without showing any console output.'
    ))
    parser.add_argument('--onefile', action='store_true', default=False, help=(
        'Create a single executable file.\n'
        'Whilst convenient for distribution, it will be slower to start up.'
    ))
    parser.add_argument('--onedir', action='store_true', default=False, help=(
        'Create an executable with all supporting files in a directory.\n'
        'This starts faster than "--onefile" because it skips the unpacking step.\n'
        'For distribution, package the directory into an archive file (e.g., .zip or .7z).'
    ))
    parser.add_argument('--add-data', type=str, action='append', default=[
        f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    ], help='Include additional data.')
    parser.add_argument('--icon', type=str, help='Path to an icon file.')
    parser.add_argument('--osx-bundle-identifier', type=str, help='Mac OS .app bundle identifier.')
    parser.add_argument('--dry-run', action='store_true', help='Dry run.', default=False)
    parser.add_argument('--clean', action='store_true', default=False, help=(
        'Clean PyInstaller cache (in ./build folder) and remove temporary files before building.'
    ))
    parser.add_argument('--noconfirm', action='store_true', default=False, help=(
        'Replace output directory (./dist/SPECNAME) without asking for confirmation.'
    ))
    parser.add_argument('main', default='main.py', help='Main file which calls `ui.run()`.')
    args = parser.parse_args()

    command = ['pyinstaller'] if platform.system() == 'Windows' else ['python', '-m', 'PyInstaller']
    command.extend(['--name', args.name])
    if args.clean:
        command.append('--clean')
    if args.noconfirm:
        command.append('--noconfirm')
    if args.windowed:
        command.append('--windowed')
    if args.onefile:
        command.append('--onefile')
    if args.onedir:
        command.append('--onedir')
    for data in args.add_data:
        command.extend(['--add-data', data])
    if args.icon:
        command.extend(['--icon', args.icon])
    if args.osx_bundle_identifier:
        command.extend(['--osx-bundle-identifier', args.osx_bundle_identifier])

    with suppress(ImportError):
        import pyecharts  # pylint: disable=import-outside-toplevel
        command.extend(['--add-data', f'{Path(pyecharts.__file__).parent}{os.pathsep}pyecharts'])

    command.extend([args.main])

    print('PyInstaller command:')
    print(' ', ' '.join(command))
    if args.dry_run:
        return

    subprocess.call(command)


if __name__ == '__main__':
    main()
