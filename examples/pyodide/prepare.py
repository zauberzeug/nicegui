#!/usr/bin/env python3
"""Prepare the Pyodide demo directory for local serving.

Copies vendor files (NiceGUI, Quasar, Vue, Tailwind) from the installed
nicegui package, copies component JS files and ESM bundles for browser-side
loading, generates an import map, and builds a stripped-down nicegui wheel
(Python-only, no static/JS assets) for fast loading in the browser.

Usage:
    python prepare.py [--no-build]

Then serve with any static HTTP server:
    python -m http.server 8080
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json as json_mod
import os
import shutil
import subprocess
import sys
import zipfile
from base64 import urlsafe_b64encode
from pathlib import Path

import nicegui

DEMO_DIR = Path(__file__).resolve().parent
REPO_ROOT = DEMO_DIR.parent.parent
NICEGUI_DIR = Path(nicegui.__file__).parent
STATIC_DIR = NICEGUI_DIR / 'static'
ELEMENTS_DIR = NICEGUI_DIR / 'elements'

VENDOR_FILES = [
    'nicegui.js',
    'nicegui.css',
    'quasar.umd.prod.js',
    'quasar.important.prod.css',
    'quasar.unimportant.prod.css',
    'tailwindcss.min.js',
    'vue.esm-browser.prod.js',
]


def prepare_static_files() -> None:
    """Copy vendor files from the installed nicegui package."""
    print(f'Copying static files from {STATIC_DIR}')
    for filename in VENDOR_FILES:
        shutil.copy2(STATIC_DIR / filename, DEMO_DIR / filename)
        print(f'  Copied {filename}')

    # Copy utility JS modules needed by component JS files (relative imports)
    utils_src = STATIC_DIR / 'utils'
    utils_dst = DEMO_DIR / 'static' / 'utils'
    if utils_src.is_dir():
        utils_dst.mkdir(parents=True, exist_ok=True)
        for js_file in utils_src.glob('*.js'):
            shutil.copy2(js_file, utils_dst / js_file.name)
            print(f'  Copied static/utils/{js_file.name}')

    # Copy fonts.css and icon/symbol font files it references
    fonts_css = STATIC_DIR / 'fonts.css'
    if fonts_css.exists():
        shutil.copy2(fonts_css, DEMO_DIR / 'fonts.css')
        print('  Copied fonts.css')
    fonts_src = STATIC_DIR / 'fonts'
    fonts_dst = DEMO_DIR / 'fonts'
    if fonts_src.is_dir():
        fonts_dst.mkdir(parents=True, exist_ok=True)
        for font_file in fonts_src.glob('*.woff2'):
            shutil.copy2(font_file, fonts_dst / font_file.name)
        print(f'  Copied {sum(1 for _ in fonts_dst.glob("*.woff2"))} font files to fonts/')

    # Copy DOMPurify (used by setHTML polyfill for HTML sanitization)
    dompurify_src = STATIC_DIR / 'dompurify.mjs'
    if dompurify_src.exists():
        static_dst = DEMO_DIR / 'static'
        static_dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dompurify_src, static_dst / 'dompurify.mjs')
        print('  Copied static/dompurify.mjs')


def prepare_components() -> None:
    """Copy component JS files and ESM bundles; generate an import map.

    Component JS files (small Vue wrappers) are copied to ``components/``
    preserving subdirectory structure so that their relative imports
    (e.g. ``../../static/utils/resources.js``) still resolve.

    ESM bundles (``dist/`` directories) are copied to ``esm/{module_name}/``
    and an ``importmap.json`` is generated for the browser.
    """
    from nicegui.dependencies import esm_modules, js_components

    components_dir = DEMO_DIR / 'components'
    esm_dir = DEMO_DIR / 'esm'

    # Clean previous output
    for d in [components_dir, esm_dir]:
        if d.exists():
            shutil.rmtree(d)

    # --- Copy component JS files ---
    print('Copying component JS files...')
    for comp in js_components.values():
        if not comp.path.exists():
            continue
        try:
            rel = comp.path.relative_to(ELEMENTS_DIR)
        except ValueError:
            continue
        dst = components_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(comp.path, dst)
        print(f'  components/{rel}')

    # --- Copy ESM dist/ bundles (JS only, skip .map) ---
    print('Copying ESM bundles...')
    imports: dict[str, str] = {}
    for esm in esm_modules.values():
        if not esm.path.is_dir():
            continue
        dest = esm_dir / esm.name
        dest.mkdir(parents=True, exist_ok=True)
        count = 0
        for src_file in esm.path.rglob('*'):
            if not src_file.is_file():
                continue
            if src_file.suffix == '.map':
                continue
            rel = src_file.relative_to(esm.path)
            dst_file = dest / rel
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            count += 1
        print(f'  esm/{esm.name}/ ({count} files)')
        imports[esm.name] = f'./esm/{esm.name}/index.js'
        imports[esm.name + '/'] = f'./esm/{esm.name}/'

    # --- Add library imports needed by component JS files ---
    imports['dompurify'] = './static/dompurify.mjs'

    # --- Inject import map into index.html ---
    importmap = {'imports': imports}
    importmap_tag = f'<script type="importmap">\n{json_mod.dumps(importmap, indent=2)}\n    </script>'
    html_path = DEMO_DIR / 'index.html'
    html = html_path.read_text()
    import re
    html = re.sub(
        r'<!-- BEGIN IMPORTMAP.*?-->.*?<!-- END IMPORTMAP -->',
        f'<!-- BEGIN IMPORTMAP (generated by prepare.py \u2014 do not edit manually) -->\n'
        f'    {importmap_tag}\n'
        f'    <!-- END IMPORTMAP -->',
        html,
        flags=re.DOTALL,
    )
    html_path.write_text(html)
    print(f'Injected import map into index.html ({len(imports)} entries)')


_BUILD_ARTIFACTS = {'package.json', 'package-lock.json', 'rollup.config.mjs', 'vite.config.js'}

# Static files read at import time (must be kept for the wheel to be importable)
_REQUIRED_STATIC = {'nicegui/static/headwind.css', 'nicegui/static/sad_face.svg'}


def _should_keep(name: str) -> bool:
    """Return True if a wheel entry should be kept for Pyodide."""
    # Always keep dist-info metadata
    if '.dist-info/' in name:
        return True
    # Keep static files that are read at import time
    if name in _REQUIRED_STATIC:
        return True
    # Drop everything else under nicegui/static/ (vendor JS/CSS/fonts loaded from HTML)
    if name.startswith('nicegui/static/'):
        return False
    parts = name.split('/')
    if len(parts) >= 3 and parts[1] == 'elements':
        # Drop element JS bundles and source maps (dist/ directories)
        if 'dist' in parts:
            return False
        # Drop build tooling (package.json, rollup configs, src/)
        if parts[-1] in _BUILD_ARTIFACTS:
            return False
        if 'src' in parts:
            return False
    return True


def _strip_wheel(src: Path, dst: Path) -> None:
    """Create a stripped wheel at *dst* keeping only Python source + metadata."""
    kept, dropped = 0, 0
    with zipfile.ZipFile(src, 'r') as zin, zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
        record_path = None
        for item in zin.infolist():
            if item.filename.endswith('/RECORD'):
                record_path = item.filename
                continue  # rebuild RECORD at the end
            if not _should_keep(item.filename):
                dropped += 1
                continue
            data = zin.read(item.filename)
            zout.writestr(item, data)
            kept += 1

        # Rebuild RECORD with correct hashes for kept files
        if record_path:
            record_buf = io.StringIO()
            writer = csv.writer(record_buf)
            for item in zout.infolist():
                data = zout.read(item.filename)
                digest = urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b'=').decode()
                writer.writerow([item.filename, f'sha256={digest}', str(len(data))])
            writer.writerow([record_path, '', ''])
            zout.writestr(record_path, record_buf.getvalue())

    print(f'  Kept {kept} files, dropped {dropped} files')


def prepare_wheel(skip_build: bool = False) -> None:
    """Build the nicegui wheel, strip it, and copy to the demo directory."""
    if not skip_build:
        print('Building nicegui wheel...')
        result = subprocess.run(
            ['uv', 'build', '--wheel'],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            print(f'Wheel build failed:\n{result.stderr}')
            sys.exit(1)
        print('Wheel built successfully')

    # Find the latest wheel
    dist_dir = REPO_ROOT / 'dist'
    wheels = sorted(dist_dir.glob('nicegui-*.whl'), key=os.path.getmtime, reverse=True)
    if not wheels:
        print('No wheel found in dist/. Run without --no-build to build one.')
        sys.exit(1)

    wheel_src = wheels[0]
    orig_size = wheel_src.stat().st_size

    # Remove old wheels from demo dir
    for old_whl in DEMO_DIR.glob('nicegui*.whl'):
        old_whl.unlink()

    # Strip static/JS assets and copy with a fixed valid wheel filename
    wheel_dst = DEMO_DIR / 'nicegui-0.0.0-py3-none-any.whl'
    print(f'Stripping wheel {wheel_src.name} ({orig_size // 1024} KB)...')
    _strip_wheel(wheel_src, wheel_dst)
    new_size = wheel_dst.stat().st_size
    print(f'  {orig_size // 1024} KB -> {new_size // 1024} KB (saved {(orig_size - new_size) // 1024} KB)')


def prepare_dynamic_resources() -> None:
    """Generate dynamic CSS resources that are normally served by the NiceGUI server.

    Uses the same hashing scheme as ``markdown.py`` so that ``markdown.js``
    can load the resource via ``./dynamic_resources/{resource_name}``.
    """
    # Generate codehilite CSS for syntax-highlighted code blocks (e.g. ui.markdown with code)
    try:
        from pygments.formatters import HtmlFormatter  # pylint: disable=import-outside-toplevel
        css = HtmlFormatter(style='default').get_style_defs('.codehilite')
        resource_name = f'codehilite_{hashlib.sha256(css.encode()).hexdigest()[:32]}.css'
        resources_dir = DEMO_DIR / 'dynamic_resources'
        resources_dir.mkdir(parents=True, exist_ok=True)
        (resources_dir / resource_name).write_text(css)
        print(f'Generated {resource_name} ({len(css)} bytes)')
    except ImportError:
        print('  Pygments not installed, skipping codehilite.css')


def main() -> None:
    parser = argparse.ArgumentParser(description='Prepare Pyodide demo files')
    parser.add_argument('--no-build', action='store_true', help='Skip building the wheel (reuse existing)')
    args = parser.parse_args()

    prepare_static_files()
    prepare_components()
    prepare_dynamic_resources()
    prepare_wheel(skip_build=args.no_build)
    print('\nReady! Serve with:  python -m http.server 8080')


if __name__ == '__main__':
    main()
