#!/usr/bin/env python3
import hashlib
import re
from pathlib import Path

import requests

AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
FONTS_DIRECTORY = Path('nicegui/static/fonts')

for file in FONTS_DIRECTORY.glob('*'):
    file.unlink()

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
    filepath = FONTS_DIRECTORY.joinpath(font_url.split('/')[-1])
    filepath = filepath.with_stem(hashlib.sha256(filepath.stem.encode()).hexdigest()[:16])
    if filepath.exists():
        # check if the content is the same between the existing file and the new one
        with open(filepath, 'rb') as existing_file:
            existing_content = existing_file.read()
        if existing_content != font:
            raise RuntimeError(f'Content mismatch for {filepath}.')
    filepath.write_bytes(font)
    css = css.replace(font_url, f'fonts/{filepath.name}')
css = css.replace('https://fonts.gstatic.com/s/materialicons/v140', 'fonts')
css = css.replace('https://fonts.gstatic.com/s/roboto/v30', 'fonts')
css = css.replace("'", '"')
Path('nicegui/static/fonts.css').write_text(css, encoding='utf-8')
