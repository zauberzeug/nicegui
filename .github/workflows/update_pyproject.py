#!/usr/bin/env python3
import re
import sys
from pathlib import Path

if __name__ == '__main__':
    path = Path('pyproject.toml')
    content = path.read_text(encoding='utf-8')
    version = sys.argv[1].removeprefix('v')
    content = re.sub(r'version = "[0-9]+\.[0-9]+\.[0-9]+-dev"', f'version = "{version}-dev"', content)
    path.write_text(content, encoding='utf-8')
