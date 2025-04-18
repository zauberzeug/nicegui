#!/usr/bin/env python3
"""Pins version of dependencies in npm.json according to package.json"""

import json
npm_pinned_entries = set()


with open('npm.json', 'r', encoding='utf-8') as f:
    npm = json.load(f)

with open('package.json', 'r', encoding='utf-8') as f:
    package = json.load(f)

for package_name, package_version in package['dependencies'].items():
    stripped_version = package_version.strip("^~")
    # for each key, value pair in npm.json, either key is the package name, or value['package'] is the package name
    for key, value in npm.items():
        if key == package_name or value.get('package') == package_name:
            # check for existing version in npm.json
            existing_version = value.get("version", "N/A")
            if existing_version != stripped_version:
                print(f"  Changing: {package_name} from {existing_version} to {stripped_version}")
                npm[key]['version'] = stripped_version.strip("^~")
            else:
                print(f"  Keeping:  {package_name} pinned to {stripped_version}")
            # add to set of pinned entries
            npm_pinned_entries.add(key)
            break
    else:  # no break, so no match found
        print(f"!!!Warning: {package_name} not found in npm.json !!!")

for key, value in npm.items():
    if key not in npm_pinned_entries:
        print(f"!!!Warning: {key} not found in package.json !!!")

# save the updated npm.json file
with open('npm.json', 'w', encoding='utf-8') as f:
    json.dump(npm, f, indent=2)
