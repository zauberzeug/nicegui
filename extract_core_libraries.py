#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
STATIC = ROOT / 'nicegui' / 'static'
NODE_MODULES = ROOT / 'node_modules'

shutil.copy2(NODE_MODULES / 'vue' / 'dist' / 'vue.global.js', STATIC / 'vue.global.js')
shutil.copy2(NODE_MODULES / 'vue' / 'dist' / 'vue.global.prod.js', STATIC / 'vue.global.prod.js')
shutil.copy2(NODE_MODULES / 'quasar' / 'dist' / 'quasar.umd.js', STATIC / 'quasar.umd.js')
shutil.copy2(NODE_MODULES / 'quasar' / 'dist' / 'quasar.umd.prod.js', STATIC / 'quasar.umd.prod.js')
shutil.copy2(NODE_MODULES / 'quasar' / 'dist' / 'quasar.css', STATIC / 'quasar.css')
shutil.copy2(NODE_MODULES / 'quasar' / 'dist' / 'quasar.prod.css', STATIC / 'quasar.prod.css')
shutil.copy2(NODE_MODULES / 'socket.io' / 'client-dist' / 'socket.io.min.js', STATIC / 'socket.io.min.js')
shutil.copy2(NODE_MODULES / 'socket.io' / 'client-dist' / 'socket.io.min.js.map', STATIC / 'socket.io.min.js.map')
shutil.copy2(NODE_MODULES / 'es-module-shims' / 'dist' / 'es-module-shims.js', STATIC / 'es-module-shims.js')

for entry in (NODE_MODULES / 'quasar' / 'dist' / 'lang').glob('*.umd.prod.js'):
    shutil.copy2(entry, STATIC / 'lang' / entry.name)

package_json = json.loads((ROOT / 'package.json').read_text(encoding='utf-8'))
tailwind_version = package_json.get('dependencies', {}).get('tailwindcss', '').lstrip('^~')
dest = STATIC / 'tailwindcss.min.js'
tmp = dest.with_suffix(dest.suffix + '.tmp')
with urllib.request.urlopen(f'https://cdn.tailwindcss.com/{tailwind_version}') as response, open(tmp, 'wb') as out:
    shutil.copyfileobj(response, out)
tmp.replace(dest)
