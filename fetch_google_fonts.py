#!/usr/bin/env python3
import re
from pathlib import Path

import requests

AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

css_families = [
    'Roboto:100,300,400,500,700,900',
    'Material+Icons',
    'Material+Icons+Outlined',
    'Material+Icons+Round',
    'Material+Icons+Sharp',
]
css2_families = [
    'Material+Symbols+Outlined',
    'Material+Symbols+Rounded',
    'Material+Symbols+Sharp',
]
css = '/* prettier-ignore */'
css += '\n' + requests.get(f'https://fonts.googleapis.com/css?family={"|".join(css_families)}',
                           headers={'User-Agent': AGENT}, timeout=5).content.decode()
css += '\n' + requests.get(f'https://fonts.googleapis.com/css?family={"|".join(css2_families)}',
                           headers={'User-Agent': AGENT}, timeout=5).content.decode()
for font_url in re.findall(r'url\((.*?)\)', css):
    font = requests.get(font_url, timeout=5).content
    filepath = Path('nicegui/static/fonts').joinpath(font_url.split('/')[-1])
    filepath.write_bytes(font)
    css = css.replace(font_url, f'fonts/{filepath.name}')
css = css.replace('https://fonts.gstatic.com/s/materialicons/v140', 'fonts')
css = css.replace('https://fonts.gstatic.com/s/roboto/v30', 'fonts')
css = css.replace("'", '"')
Path('nicegui/static/fonts.css').write_text(css)
