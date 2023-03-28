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
import tarfile
from pathlib import Path
import urllib.request
import re


def delete_folder(path):
    if not path.exists():
        return path
    for sub in path.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()
    path.rmdir()
    return path


def ensure(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


# Create a hidden folder to work in.
tmp = Path('.npm')
delete_folder(tmp).mkdir()

with open('npm.json') as file:
    dependencies = json.load(file)
    for key in dependencies:
        dependency = dependencies[key]

        # Reset destination folder.
        destination = Path('nicegui', dependency['destination'], key)
        delete_folder(destination).mkdir()

        # ---
        # Handle the special case of tailwind. Hopefully remove this soon.
        if 'download' in dependency:
            USER_AGENT = 'Mozilla/5.0'
            request = urllib.request.Request(dependency['download'], headers={'User-Agent': USER_AGENT})
            with urllib.request.urlopen(request) as resource:
                content = resource.read().decode()
                version = resource.geturl().rsplit('/', 1)[-1]
                print(f"tailwind: {version} - https://cdn.tailwindcss.com")
                with Path(destination, dependency['rename']).open('w') as dest:
                    dest.write(content)
            continue
        # ---

        package = dependency['package'] if 'package' in dependency else key
        npm_url = f"https://registry.npmjs.org/{package}"

        with urllib.request.urlopen(npm_url) as npm:
            # Get package info from npm.
            npm_data = json.load(npm)
            npm_version = dependency['version'] if 'version' in dependency else npm_data['dist-tags']['latest']
            npm_tarball = npm_data['versions'][npm_version]['dist']['tarball']
            print(f"{key}: {npm_version} - {npm_tarball}")

            # Download and extract.
            Path(tmp, key).mkdir()
            urllib.request.urlretrieve(npm_tarball, Path(tmp, key, f"{key}.tgz"))
            with tarfile.open(Path(tmp, key, f"{key}.tgz")) as archive:

                to_be_extracted = []
                for tarinfo in archive.getmembers():
                    for keep in dependency['keep']:
                        if re.match(f"^{keep}$", tarinfo.name):
                            to_be_extracted.append(tarinfo)

                archive.extractall(members=to_be_extracted, path=Path(tmp, key))

                for extracted in to_be_extracted:
                    filename = extracted.name
                    for rename in dependency['rename']:
                        filename = filename.replace(rename, dependency['rename'][rename])

                    newfile = Path(destination, filename)
                    if newfile.exists():
                        newfile.unlink()
                    Path(tmp, key, extracted.name).rename(ensure(newfile))

        # Delete destination folder if empty.
        if not any(Path(destination).iterdir()):
            delete_folder(destination)


delete_folder(tmp)
