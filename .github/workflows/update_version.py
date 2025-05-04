#!/usr/bin/env python3
import sys
from datetime import datetime, timezone
from pathlib import Path

if __name__ == '__main__':
    version = sys.argv[1].lstrip('v')

    path = Path('pyproject.toml')
    lines = path.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines):
        if line.startswith('version = '):
            lines[i] = f'version = "{version}-dev"'
            break
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    path = Path('CITATION.cff')
    lines = path.read_text(encoding='utf-8').splitlines()
    for i, line in enumerate(lines):
        if line.startswith('version: '):
            lines[i] = f'version: {version}'
        if line.startswith('date-released: '):
            lines[i] = f'date-released: "{datetime.now(timezone.utc).strftime(r"%Y-%m-%d")}"'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
