#!/usr/bin/env python3
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import nicegui.elements.chart as highcharts

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
PATH = Path('/tmp/nicegui_dependencies')
PATH.mkdir(exist_ok=True)


def url_to_filename(url: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '_', url)


def request_buffered_str(url: str) -> str:
    filepath = PATH / url_to_filename(url)
    if filepath.exists():
        return filepath.read_text()
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    filepath.write_text(response.text)
    return response.text


def request_buffered(url: str) -> bytes:
    filepath = PATH / url_to_filename(url)
    if filepath.exists():
        return filepath.read_bytes()
    response = requests.get(url, headers={'User-Agent': USER_AGENT})
    filepath.write_bytes(response.content)
    return response.content


# Google fonts
url = 'https://fonts.googleapis.com/css2?family=Material+Icons&family=Roboto:wght@100;300;400;500;700;900'
css = request_buffered_str(url)
for font_url in re.findall(r'url\((.*?)\)', css):
    font = request_buffered(font_url)
    (Path('nicegui/static/fonts') / font_url.split('/')[-1]).write_bytes(font)
css = css.replace('https://fonts.gstatic.com/s/materialicons/v140', 'fonts')
css = css.replace('https://fonts.gstatic.com/s/roboto/v30', 'fonts')
css = css.replace(' U+2122', '\n    U+2122')
css = css.replace("'", '"')
Path('nicegui/static/fonts.css').write_text(css)

# quasar.js
url = 'https://cdn.jsdelivr.net/npm/quasar/dist/quasar.umd.prod.js'
js = request_buffered_str(url)
Path('nicegui/static/quasar.umd.prod.js').write_text(js)
version = re.search(r'Quasar Framework v(\d+\.\d+\.\d+)', js).group(1)
url = 'https://cdn.jsdelivr.net/npm/quasar/dist/quasar.prod.css'
css = request_buffered_str(url)
Path('nicegui/static/quasar.prod.css').write_text(css)
print('Quasar:', version)

# Quasar language packs
url = 'https://cdn.jsdelivr.net/npm/quasar@2/dist/lang/'
html = request_buffered_str(url)
soup = BeautifulSoup(html, 'html.parser')
languages = []
for link in soup.find_all('a', href=re.compile(r'\.umd\.prod\.js$')):
    name = link.get('href').split('/')[-1]
    languages.append(name.split('.')[0])
    js = request_buffered_str(url + name)
    Path(f'nicegui/static/quasar.{name}').write_text(js)
with open(Path(__file__).parent / 'nicegui' / 'language.py', 'w') as f:
    f.write(f'from typing_extensions import Literal\n\n')
    f.write(f'Language = Literal[\n')
    for language in languages:
        f.write(f"    '{language}',\n")
    f.write(f']\n')

# vue.js
url = 'https://unpkg.com/vue@3/anything'
info = request_buffered_str(url)
version = re.search(r'Cannot find "/anything" in vue@(\d+\.\d+\.\d+)', info).group(1)
url = 'https://unpkg.com/vue@3/dist/vue.global.prod.js'
js = request_buffered_str(url)
Path('nicegui/static/vue.global.prod.js').write_text(js)
print('Vue:', version)

# socket.io.js
url = 'https://cdn.jsdelivr.net/npm/socket.io-client/dist/socket.io.min.js'
js = request_buffered_str(url)
Path('nicegui/static/socket.io.min.js').write_text(js)
version = re.search(r'Socket.IO v(\d+\.\d+\.\d+)', js).group(1)
print('Socket.io:', version)

# tailwind.js
url = 'https://cdn.tailwindcss.com/'
js = request_buffered_str(url)
Path('nicegui/static/tailwindcss.min.js').write_text(js)
version = re.search(r'{name:"tailwindcss",version:"(\d+\.\d+\.\d+)"', js).group(1)
print('Tailwind CSS:', version)

# tween.js
url = 'https://cdnjs.com/libraries/tween.js'
html = request_buffered_str(url)
soup = BeautifulSoup(html, 'html.parser')
version = soup.find('span', class_='vs__selected').text.strip()
url = f'https://cdnjs.cloudflare.com/ajax/libs/tween.js/{version}/tween.umd.min.js'
js = request_buffered_str(url)
Path('nicegui/elements/lib/tween.umd.min.js').write_text(js)
print('Tween.js:', version)

# plotly.js
url = 'https://cdnjs.com/libraries/plotly.js'
html = request_buffered_str(url)
soup = BeautifulSoup(html, 'html.parser')
version = soup.find('span', class_='vs__selected').text.strip()
url = f'https://cdnjs.cloudflare.com/ajax/libs/plotly.js/{version}/plotly.min.js'
js = request_buffered_str(url)
Path('nicegui/elements/lib/plotly.min.js').write_text(js)
print('Plotly.js:', version)

# ag-grid.js
url = 'https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.js'
js = request_buffered_str(url)
Path('nicegui/elements/lib/ag-grid-community.min.js').write_text(js)
version = re.search(r'@version v(\d+\.\d+\.\d+)', js).group(1)
print('AG Grid:', version)

# nipplejs.js
url = 'https://www.npmjs.com/package/nipplejs'
html = request_buffered_str(url)
soup = BeautifulSoup(html, 'html.parser')
version = soup.find('h3', string='Version').find_next_sibling('div').text.strip()
url = f'https://cdn.jsdelivr.net/npm/nipplejs@{version}/dist/nipplejs.min.js'
js = request_buffered_str(url)
Path('nicegui/elements/lib/nipplejs.min.js').write_text(js)
print('NippleJS:', version)

# mermaid.min.js
url = 'https://cdn.jsdelivr.net/npm/mermaid@9/dist/'
html = request_buffered_str(url)
soup = BeautifulSoup(html, 'html.parser')
# find a with href starting with /npm/mermaid@
version = soup.find('a', href=re.compile(r'^/npm/mermaid@')).text.strip().removeprefix('mermaid@')
url = f'https://cdn.jsdelivr.net/npm/mermaid@{version}/dist/mermaid.min.js'
js = request_buffered_str(url)
Path('nicegui/elements/lib/mermaid.min.js').write_text(js)
print('Mermaid:', version)
# TODO: upgrade to Mermaid 10.0.x? (ESM only and potentially breaking changes)

# highcharts.js
for dependency in highcharts.dependencies:
    name = dependency.split('/')[-1]
    url = f'https://code.highcharts.com/{name}'
    js = request_buffered_str(url)
    Path(f'nicegui/elements/lib/{name}').write_text(js)
    v = re.search(r'Highcharts JS v(\d+\.\d+\.\d+)', js).group(1)
    if name == 'highcharts.js':
        version = v
        print('Highcharts:', version)
    else:
        assert version == v
for dependency in highcharts.optional_dependencies:
    name = dependency.split('/')[-1]
    url = f'https://code.highcharts.com/modules/{name}'
    js = request_buffered_str(url)
    Path(f'nicegui/elements/lib/highcharts_modules/{name}').write_text(js)
    v = re.search(r'JS v(\d+\.\d+\.\d+)', js).group(1)
    assert version == v

# three.js
url = 'https://www.npmjs.com/package/three'
html = request_buffered_str(url)
soup = BeautifulSoup(html, 'html.parser')
version = soup.find('h3', string='Version').find_next_sibling('div').text.strip()
url = f'https://cdn.jsdelivr.net/npm/three@{version}/build/three.min.js'
js = request_buffered_str(url)
Path('nicegui/elements/lib/three.min.js').write_text(js)
print('Three.js:', version)
# TODO: using script JS files is not supported after version 0.160.0 --> use ES module instead
# TODO: CSS2DRenderer.js, CSS3DRenderer.js, OrbitControls.js, STLLoader.js (require ES modules)
