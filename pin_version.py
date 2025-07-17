#!/usr/bin/env python3
"""Pins version of dependencies in npm.json according to package.json"""
import json
from pathlib import Path
from typing import Dict, Set

PATH = Path(__file__).parent
NPM_FILE = PATH / 'npm.json'
PACKAGE_FILE = PATH / 'package.json'

npm: Dict[str, Dict] = json.loads(NPM_FILE.read_text(encoding='utf-8'))
package: Dict[str, Dict] = json.loads(PACKAGE_FILE.read_text(encoding='utf-8'))
npm_pinned_entries: Set[str] = set()

for package_name, package_version in package['dependencies'].items():
    stripped_version = package_version.strip('^~')
    for key, value in npm.items():
        if key == package_name or value.get('package') == package_name:
            existing_version = value.get('version', 'N/A')
            if existing_version != stripped_version:
                print(f'Changing {package_name} from {existing_version} to {stripped_version}')
                npm[key]['version'] = stripped_version.strip('^~')
            else:
                print(f'Keeping  {package_name} at {stripped_version}')
            npm_pinned_entries.add(key)
            break
    else:
        print(f'Warning: {package_name} not found in npm.json!')

for key in npm:
    if key not in npm_pinned_entries:
        print(f'Warning: {key} not found in package.json!')


NPM_FILE.write_text(json.dumps(npm, indent=2) + '\n', encoding='utf-8')
