#!/usr/bin/env python3
from __future__ import annotations

import shutil
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
for entry in (NODE_MODULES / 'quasar' / 'dist' / 'lang').glob('*.umd.prod.js'):
    shutil.copy2(entry, STATIC / 'lang' / entry.name)

shutil.copy2(NODE_MODULES / '@tailwindcss' / 'browser' / 'dist' / 'index.global.js', STATIC / 'tailwindcss.min.js')
WARNING = (
    'console.warn("The browser build of Tailwind CSS should not be used in production. '
    'To use Tailwind CSS in production, use the Tailwind CLI, Vite plugin, or PostCSS plugin: '
    'https://tailwindcss.com/docs/installation");'
)
(STATIC / 'tailwindcss.min.js').write_text((STATIC / 'tailwindcss.min.js').read_text().replace(WARNING, ''))

shutil.copy2(NODE_MODULES / 'socket.io' / 'client-dist' / 'socket.io.min.js', STATIC / 'socket.io.min.js')
shutil.copy2(NODE_MODULES / 'socket.io' / 'client-dist' / 'socket.io.min.js.map', STATIC / 'socket.io.min.js.map')

shutil.copy2(NODE_MODULES / 'es-module-shims' / 'dist' / 'es-module-shims.js', STATIC / 'es-module-shims.js')
