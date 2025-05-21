#!/usr/bin/env python3
from pathlib import Path

codes = sorted(path.name.split('.')[0] for path in Path('nicegui/static/lang').glob('*.umd.prod.js'))

with (Path(__file__).parent / 'nicegui' / 'language.py').open('w', encoding='utf-8') as f:
    f.write('from typing import Literal\n')
    f.write('\n')
    f.write('Language = Literal[\n')
    for code in codes:
        f.write(f"    '{code}',\n")
    f.write(']\n')
