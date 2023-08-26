#!/usr/bin/env python3
import re
from pathlib import Path

import requests

AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

url = 'https://fonts.googleapis.com/css2?family=Material+Icons&family=Roboto:wght@100;300;400;500;700;900'
css = requests.get(url, headers={'User-Agent': AGENT}, timeout=5).content.decode()
for font_url in re.findall(r'url\((.*?)\)', css):
    font = requests.get(font_url, timeout=5).content
    (Path('nicegui/static/fonts') / font_url.split('/')[-1]).write_bytes(font)
css = css.replace('https://fonts.gstatic.com/s/materialicons/v140', 'fonts')
css = css.replace('https://fonts.gstatic.com/s/roboto/v30', 'fonts')
css = css.replace(' U+2122', '\n    U+2122')
css = css.replace("'", '"')
Path('nicegui/static/fonts.css').write_text(css)
