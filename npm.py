#!/usr/bin/env python3
"""Update dependencies according to npm.json configurations using jsDelivr CDN.

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
import tempfile
from argparse import ArgumentParser
from pathlib import Path

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


def url_to_filename(url: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '_', url)


def download_buffered(url: str) -> Path:
    filepath = Path(temp_dir.name) / url_to_filename(url)
    if not filepath.exists():
        response = httpx.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
        filepath.write_bytes(response.content)
    return filepath


def get_package_info_from_jsdelivr(pkg_name: str) -> dict:
    path = download_buffered(f'https://data.jsdelivr.com/v1/package/npm/{pkg_name}')
    return json.loads(path.read_text(encoding='utf-8'))


def get_package_files_from_jsdelivr(pkg_name: str, version: str) -> dict:
    path = download_buffered(f'https://data.jsdelivr.com/v1/package/npm/{pkg_name}@{version}')
    return json.loads(path.read_text(encoding='utf-8'))


def download_file_from_jsdelivr(pkg_name: str, version: str, filepath: str) -> bytes:
    return download_buffered(f'https://cdn.jsdelivr.net/npm/{pkg_name}@{version}/{filepath}').read_bytes()


def find_matching_files(files_dict: dict, pattern: str) -> list[str]:
    matches = []

    def traverse(files_list, current_path=''):
        for file_info in files_list:
            if file_info['type'] == 'file':
                full_path = f"{current_path}/{file_info['name']}" if current_path else file_info['name']
                if re.match(f'^{pattern}$', full_path):
                    matches.append(full_path)
            elif file_info['type'] == 'directory':
                new_path = f"{current_path}/{file_info['name']}" if current_path else file_info['name']
                if 'files' in file_info:
                    traverse(file_info['files'], new_path)

    if 'files' in files_dict:
        traverse(files_dict['files'])

    return matches


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

dependencies: dict[str, dict] = json.loads((root_path / 'npm.json').read_text(encoding='utf-8'))
for key, dependency in dependencies.items():
    if names is not None and key not in names:
        continue

    destination = prepare(root_path / dependency['destination'] / key)

    try:
        package_name = dependency.get('package', key)
        package_info = get_package_info_from_jsdelivr(package_name)
        npm_version = dependency.get('version') or package_info['tags']['latest']
        files_info = get_package_files_from_jsdelivr(package_name, npm_version)

        license_ = 'UNKNOWN'
        try:
            package_json_content = download_file_from_jsdelivr(package_name, npm_version, 'package.json')
            package_json = json.loads(package_json_content.decode('utf-8'))
            if 'license' in package_json:
                license_ = package_json['license']
            elif package_name == 'echarts-gl':
                license_ = 'BSD-3-Clause'
        except Exception:
            if package_name == 'echarts-gl':
                license_ = 'BSD-3-Clause'

        jsdelivr_url = f'https://cdn.jsdelivr.net/npm/{package_name}@{npm_version}/'
        print(f'{key}: {npm_version} - {jsdelivr_url} ({license_})')
        DEPENDENCIES.write(f'- {key}: {npm_version} ([{license_}]({KNOWN_LICENSES.get(license_, license_)}))\n')

        for keep_pattern in dependency['keep']:
            matching_files = find_matching_files(files_info, keep_pattern)

            for file_path in matching_files:
                try:
                    file_content = download_file_from_jsdelivr(package_name, npm_version, file_path)

                    filename = file_path
                    for rename_from, rename_to in dependency.get('rename', {}).items():
                        filename = filename.replace(rename_from, rename_to)

                    newfile = prepare(Path(destination, filename))
                    if newfile.exists():
                        newfile.unlink()

                    newfile.write_bytes(file_content)

                    if 'GLTFLoader' in filename:
                        content = newfile.read_text(encoding='utf-8')
                        MSG = '../utils/BufferGeometryUtils.js'
                        if MSG in content:
                            content = content.replace(MSG, 'BufferGeometryUtils')
                            newfile.write_text(content, encoding='utf-8')

                    if 'DragControls.js' in filename:
                        content = newfile.read_text(encoding='utf-8')
                        MSG = '_selected = findGroup( _intersections[ 0 ].object )'
                        if MSG in content:
                            content = content.replace(MSG, MSG + ' || _intersections[ 0 ].object')
                            newfile.write_text(content, encoding='utf-8')

                    if 'mermaid.esm.min.mjs' in filename:
                        content = newfile.read_text(encoding='utf-8')
                        content = re.sub(r'"\./chunks/mermaid.esm.min/(.*?)\.mjs"', r'"\1"', content)
                        newfile.write_text(content, encoding='utf-8')

                except Exception as e:
                    print(f'Warning: Failed to download {file_path} for {package_name}: {e}')

    except Exception as e:
        print(f'Error processing package {package_name}: {e}')
        continue

    try:
        if not any(destination.iterdir()):
            destination.rmdir()
    except Exception:
        pass

temp_dir.cleanup()
