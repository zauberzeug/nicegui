#!/usr/bin/env python3
import json
from pathlib import Path

import httpx

FAMILIES = {
    'Material Icons': ('', ''),
    'Material Icons Outlined': ('_outlined', 'o_'),
    'Material Icons Round': ('_round', 'r_'),
    'Material Icons Sharp': ('_sharp', 's_'),
    'Material Symbols Outlined': ('_sym_outlined', 'sym_o_'),
    'Material Symbols Rounded': ('_sym_round', 'sym_r_'),
    'Material Symbols Sharp': ('_sym_sharp', 'sym_s_'),
}
FAMILY_SET = set(FAMILIES)

response = httpx.get('https://fonts.google.com/metadata/icons?incomplete=1&key=material_symbols')
with (Path(__file__).parent / 'nicegui' / 'icon.py').open('w') as f:
    for icon in json.loads(response.text[4:])['icons']:
        for family in FAMILY_SET.difference(icon['unsupported_families']):
            name = f'{icon["name"]}{FAMILIES[family][0]}'.upper()
            if not name.isidentifier():
                name = f'_{name}'
            value = f'{FAMILIES[family][1]}{icon["name"]}'
            f.write(f"{name} = '{value}'\n")
