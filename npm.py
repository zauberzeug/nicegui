#!/usr/bin/env python3
"""Update dependencies according to npm.json configurations using the NPM packagist.

npm.json file is a JSON object key => dependency.

- key: is the key name of the dependency. It will be the folder name where the dependency will be stored.
- dependency: a JSON object key-pair value with the following meaning full keys:
    - package (optional): if provided, this is the NPM package name. Otherwise, key is used as an NPM package name.
    - version (optional): if provided, this will fix the version to use. Otherwise, the latest available NPM package version will be used.
    - destination: the destination folder where the dependency should end up.
    - keep: an array of regexp of files to keep within the downloaded NPM package.
    - rename: an array of rename rules (string replace). Used to change the package structure after download to match NiceGUI expectations.
"""
import json
import re
import shutil
import tarfile
from argparse import ArgumentParser
from pathlib import Path

import requests

parser = ArgumentParser()
parser.add_argument('path', default='.', help='path to the root of the repository')
parser.add_argument('--name', nargs='*', help='filter library updates by name')
args = parser.parse_args()
root_path = Path(args.path)
names = args.name or None


def prepare(path: Path) -> Path:
    """
    Create the parent directory for the given path if it doesn't exist.

    Args:
        path (Path): The path for which the parent directory needs to be created.

    Returns:
        Path: The input path with the parent directory created.

    Raises:
        None

    Example:
        >>> prepare(Path('/d:/Alejandro/Projects/Python/Otros/NiceGUI/nicegui/npm.py'))
        Path('/d:/Alejandro/Projects/Python/Otros/NiceGUI/nicegui')
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def cleanup(path: Path) -> Path:
    """
    Recursively removes a directory and its contents.

    Args:
        path (Path): The path to the directory to be removed.

    Returns:
        Path: The path of the removed directory.

    Raises:
        FileNotFoundError: If the specified directory does not exist.
        PermissionError: If the user does not have permission to remove the directory.

    Example:
        >>> cleanup(Path('/path/to/directory'))
        Path('/path/to/directory')
    """
    shutil.rmtree(path, ignore_errors=True)
    return path


def url_to_filename(url: str) -> str:
    """
    Convert a URL to a valid filename by replacing non-alphanumeric characters with underscores.

    Args:
        url (str): The URL to be converted.

    Returns:
        str: The converted filename.

    Example:
        >>> url_to_filename('https://example.com/file?param=value')
        'https_example_com_file_param_value'
    """
    return re.sub(r'[^a-zA-Z0-9]', '_', url)


def download_buffered(url: str) -> Path:
    """
    Downloads a file from the given URL and saves it to a temporary directory.

    Args:
        url (str): The URL of the file to be downloaded.

    Returns:
        Path: The path to the downloaded file.

    Raises:
        requests.exceptions.RequestException: If there is an error while making the request.

    Notes:
        - The function creates a temporary directory at '/tmp/nicegui_dependencies' if it doesn't exist.
        - The downloaded file is saved with the same name as the file in the URL.
        - If the file already exists in the temporary directory, it will not be downloaded again.
        - The function uses the 'User-Agent' header 'Mozilla/5.0' for the request.
        - The function has a timeout of 3 seconds for the request.
    """
    path = Path('/tmp/nicegui_dependencies')
    path.mkdir(exist_ok=True)
    filepath = path / url_to_filename(url)
    if not filepath.exists():
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
        filepath.write_bytes(response.content)
    return filepath


DEPENDENCIES = (root_path / 'DEPENDENCIES.md').open('w')
DEPENDENCIES.write('# Included Web Dependencies\n\n')
KNOWN_LICENSES = {
    'MIT': 'https://opensource.org/licenses/MIT',
    'ISC': 'https://opensource.org/licenses/ISC',
    'Apache-2.0': 'https://opensource.org/licenses/Apache-2.0',
    'BSD-2-Clause': 'https://opensource.org/licenses/BSD-2-Clause',
}

# Create a hidden folder to work in.
tmp = cleanup(root_path / '.npm')

dependencies: dict[str, dict] = json.loads((root_path / 'npm.json').read_text())
for key, dependency in dependencies.items():
    if names is not None and key not in names:
        continue

    # Reset destination folder.
    destination = prepare(root_path / dependency['destination'] / key)

    # Get package info from NPM.
    package_name = dependency.get('package', key)
    npm_data = json.loads(download_buffered(f'https://registry.npmjs.org/{package_name}').read_text())
    npm_version = dependency.get('version') or dependency.get('version', npm_data['dist-tags']['latest'])
    npm_tarball = npm_data['versions'][npm_version]['dist']['tarball']
    license_ = npm_data['versions'][npm_version]['license']
    print(f'{key}: {npm_version} - {npm_tarball} ({license_})')
    DEPENDENCIES.write(f'- {key}: {npm_version} ([{license_}]({KNOWN_LICENSES.get(license_, license_)}))\n')

    # Handle the special case of tailwind. Hopefully remove this soon.
    if 'download' in dependency:
        download_path = download_buffered(dependency['download'])
        content = download_path.read_text()
        MSG = (
            'console.warn("cdn.tailwindcss.com should not be used in production. '
            'To use Tailwind CSS in production, install it as a PostCSS plugin or use the Tailwind CLI: '
            'https://tailwindcss.com/docs/installation");'
        )
        if MSG not in content:
            raise ValueError(f'Expected to find "{MSG}" in {download_path}')
        content = content.replace(MSG, '')
        prepare(destination / dependency['rename']).write_text(content)

    # Download and extract.
    tgz_file = prepare(Path(tmp, key, f'{key}.tgz'))
    tgz_download = download_buffered(npm_tarball)
    shutil.copyfile(tgz_download, tgz_file)
    with tarfile.open(tgz_file) as archive:
        to_be_extracted: list[tarfile.TarInfo] = []
        for tarinfo in archive.getmembers():
            for keep in dependency['keep']:
                if re.match(f'^{keep}$', tarinfo.name):
                    to_be_extracted.append(tarinfo)  # TODO: simpler?

        archive.extractall(members=to_be_extracted, path=Path(tmp, key))

        for extracted in to_be_extracted:
            filename: str = extracted.name
            for rename in dependency['rename']:
                filename = filename.replace(rename, dependency['rename'][rename])

            newfile = prepare(Path(destination, filename))
            Path(tmp, key, extracted.name).rename(newfile)

    # Delete destination folder if empty.
    if not any(destination.iterdir()):
        destination.rmdir()

cleanup(tmp)
