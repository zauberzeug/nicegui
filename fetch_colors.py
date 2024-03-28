#!/usr/bin/env python3
from pathlib import Path
from typing import cast

import webcolors

from nicegui.elements.mixins.color_elements import QUASAR_COLORS, TAILWIND_COLORS

CSS_COLORS = sorted(set([
    *list(webcolors.CSS2_NAMES_TO_HEX),
    *list(webcolors.CSS21_NAMES_TO_HEX),
    *list(webcolors.CSS3_NAMES_TO_HEX),
    *list(webcolors.HTML4_NAMES_TO_HEX),
]))

with open(Path(__file__).parent / 'nicegui' / 'color.py', 'w') as f:
    for color in CSS_COLORS:
        f.write(f"{color.upper()} = '{color}'\n")

    f.write('\n')
    f.write('class quasar:\n')
    for color in QUASAR_COLORS:
        f.write(f"    {color.upper().replace('-', '_')} = '{color}'\n")

    f.write('\n')
    f.write('class tailwind:\n')
    for color in cast(list[str], TAILWIND_COLORS):
        f.write(f"    {color.upper().replace('-', '_')} = '{color}'\n")
