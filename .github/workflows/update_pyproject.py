#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

VERSION_PATTERN = re.compile(r'v[0-9]+\.[0-9]+\.[0-9]+')

if __name__ == '__main__':
    command = 'git describe --tags $(git rev-list --tags --max-count=100)'
    tags = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, check=True) \
        .stdout.strip().splitlines()
    version = next(tag for tag in tags if VERSION_PATTERN.fullmatch(tag)).removeprefix('v')

    path = Path('pyproject.toml')
    content = path.read_text(encoding='utf-8')
    content = re.sub(r'version = "[0-9]+\.[0-9]+\.[0-9]+-dev"', f'version = "{version}-dev"', content)
    path.write_text(content, encoding='utf-8')
