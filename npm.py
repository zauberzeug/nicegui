#!/usr/bin/env python3
"""
Update dependencies according to npm.json configurations using the NPM packagist.

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
import urllib.request
from pathlib import Path


def prepare(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def cleanup(path: Path) -> Path:
    shutil.rmtree(path, ignore_errors=True)
    return path


# Create a hidden folder to work in.
tmp = cleanup(Path('.npm'))

dependencies: dict[str, dict] = json.loads(Path('npm.json').read_text())
for key, dependency in dependencies.items():
    # Reset destination folder.
    destination = prepare(Path('nicegui', dependency['destination'], key))

    # Handle the special case of tailwind. Hopefully remove this soon.
    if 'download' in dependency:
        USER_AGENT = 'Mozilla/5.0'
        request = urllib.request.Request(dependency['download'], headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(request) as resource:
            content = resource.read().decode()
            version = resource.geturl().rsplit('/', 1)[-1]
            print(f'tailwind: {version} - https://cdn.tailwindcss.com')
            prepare(Path(destination, dependency['rename'])).write_text(content)
        continue

    package_name = dependency.get('package', key)
    with urllib.request.urlopen(f'https://registry.npmjs.org/{package_name}') as npm:
        # Get package info from NPM.
        npm_data = json.load(npm)
        npm_version = dependency.get('version', npm_data['dist-tags']['latest'])
        npm_tarball = npm_data['versions'][npm_version]['dist']['tarball']
        print(f'{key}: {npm_version} - {npm_tarball}')

        # Download and extract.
        tgz_file = prepare(Path(tmp, key, f'{key}.tgz'))
        urllib.request.urlretrieve(npm_tarball, tgz_file)
        with tarfile.open(tgz_file) as archive:
            to_be_extracted = []
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
