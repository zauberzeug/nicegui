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
import tempfile
from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List

import httpx

temp_dir = tempfile.TemporaryDirectory()

parser = ArgumentParser()
parser.add_argument('path', default='.', help='path to the root of the repository')
parser.add_argument('--name', nargs='*', help='filter library updates by name')
args = parser.parse_args()
root_path = Path(args.path)
names = args.name or None


def prepare(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def cleanup(path: Path) -> Path:
    shutil.rmtree(path, ignore_errors=True)
    return path


def url_to_filename(url: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '_', url)


def download_buffered(url: str) -> Path:
    filepath = Path(temp_dir.name) / url_to_filename(url)
    if not filepath.exists():
        response = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
        filepath.write_bytes(response.content)
    return filepath


DEPENDENCIES = (root_path / 'DEPENDENCIES.md').open('w', encoding='utf-8')
DEPENDENCIES.write('# Included Web Dependencies\n\n')
KNOWN_LICENSES = {
    'UNKNOWN': 'UNKNOWN',
    'MIT': 'https://opensource.org/licenses/MIT',
    'ISC': 'https://opensource.org/licenses/ISC',
    'Apache-2.0': 'https://opensource.org/licenses/Apache-2.0',
    'BSD-2-Clause': 'https://opensource.org/licenses/BSD-2-Clause',
    'BSD-3-Clause': 'https://opensource.org/licenses/BSD-3-Clause',
}

# Create a hidden folder to work in.
tmp = cleanup(root_path / '.npm')

dependencies: Dict[str, dict] = json.loads((root_path / 'npm.json').read_text(encoding='utf-8'))
for key, dependency in dependencies.items():
    if names is not None and key not in names:
        continue

    # Reset destination folder.
    destination = prepare(root_path / dependency['destination'] / key)

    # Get package info from NPM.
    package_name = dependency.get('package', key)
    npm_data = json.loads(download_buffered(f'https://registry.npmjs.org/{package_name}').read_text(encoding='utf-8'))
    npm_version = dependency.get('version') or dependency.get('version', npm_data['dist-tags']['latest'])
    npm_tarball = npm_data['versions'][npm_version]['dist']['tarball']
    license_ = 'UNKNOWN'
    if 'license' in npm_data['versions'][npm_version]:
        license_ = npm_data['versions'][npm_version]['license']
    elif package_name == 'echarts-gl':
        license_ = 'BSD-3-Clause'
    print(f'{key}: {npm_version} - {npm_tarball} ({license_})')
    DEPENDENCIES.write(f'- {key}: {npm_version} ([{license_}]({KNOWN_LICENSES.get(license_, license_)}))\n')

    # Handle the special case of tailwind. Hopefully remove this soon.
    if 'download' in dependency:
        download_path = download_buffered(dependency['download'])
        content = download_path.read_text(encoding='utf-8')
        MSG = (
            'console.warn("cdn.tailwindcss.com should not be used in production. '
            'To use Tailwind CSS in production, install it as a PostCSS plugin or use the Tailwind CLI: '
            'https://tailwindcss.com/docs/installation");'
        )
        if MSG not in content:
            raise ValueError(f'Expected to find "{MSG}" in {download_path}')
        content = content.replace(MSG, '')
        prepare(destination / dependency['rename']).write_text(content, encoding='utf-8')

    # Download and extract.
    tgz_file = prepare(Path(tmp, key, f'{key}.tgz'))
    tgz_download = download_buffered(npm_tarball)
    shutil.copyfile(tgz_download, tgz_file)
    with tarfile.open(tgz_file) as archive:
        to_be_extracted: List[tarfile.TarInfo] = []
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
            if newfile.exists():
                newfile.unlink()
            Path(tmp, key, extracted.name).rename(newfile)

            if 'GLTFLoader' in filename:
                content = newfile.read_text(encoding='utf-8')
                MSG = '../utils/BufferGeometryUtils.js'
                if MSG not in content:
                    raise ValueError(f'Expected to find "{MSG}" in {filename}')
                content = content.replace(MSG, 'BufferGeometryUtils')
                newfile.write_text(content, encoding='utf-8')

            if 'DragControls.js' in filename:
                content = newfile.read_text(encoding='utf-8')
                MSG = '_selected = findGroup( _intersections[ 0 ].object )'
                if MSG not in content:
                    raise ValueError(f'Expected to find "{MSG}" in {filename}')
                content = content.replace(MSG, MSG + ' || _intersections[ 0 ].object')
                newfile.write_text(content, encoding='utf-8')

            if 'mermaid.esm.min.mjs' in filename:
                content = newfile.read_text(encoding='utf-8')
                content = re.sub(r'"\./chunks/mermaid.esm.min/(.*?)\.mjs"', r'"\1"', content)
                newfile.write_text(content, encoding='utf-8')

    try:
        # Delete destination folder if empty.
        if not any(destination.iterdir()):
            destination.rmdir()
    except Exception:
        pass

temp_dir.cleanup()

cleanup(tmp)
