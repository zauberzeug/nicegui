import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import vbuild

from . import __version__
from .element import Element

vue_components: Dict[str, Any] = {}
js_components: Dict[str, Any] = {}
libraries: Dict[str, Any] = {}


def register_vue_component(name: str, path: Path) -> None:
    """Register a .vue or .js Vue component.

    :param name: unique machine-name (used in element's `use_library`): no space, no special characters
    :param path: local path
    """
    suffix = path.suffix.lower()
    assert suffix in {'.vue', '.js', '.mjs'}, 'Only VUE and JS components are supported.'
    if suffix == '.vue':
        assert name not in vue_components, f'Duplicate VUE component name {name}'
        # The component (in case of .vue) is built right away to:
        # 1. delegate this "long" process to the bootstrap phase
        # 2. avoid building the component on every single request
        vue_components[name] = vbuild.VBuild(name, path.read_text())
    elif suffix == '.js':
        assert name not in js_components, f'Duplicate JS component name {name}'
        js_components[name] = {'name': name, 'path': path}


def register_library(name: str, path: Path, *, expose: bool = False) -> None:
    """Register a new external library.

    :param name: unique machine-name (used in element's `use_library`): no space, no special characters
    :param path: local path
    :param expose: if True, this will be exposed as an ESM module but NOT imported
    """
    assert path.suffix == '.js' or path.suffix == '.mjs', 'Only JS dependencies are supported.'
    libraries[name] = {'name': name, 'path': path, 'expose': expose}


def generate_resources(prefix: str, elements: List[Element]) -> Tuple[str, str, str, str, str]:
    done_libraries: Set[str] = set()
    done_components: Set[str] = set()
    vue_scripts = ''
    vue_html = ''
    vue_styles = ''
    js_imports = ''
    import_maps = {'imports': {}}

    # Build the importmap structure for exposed libraries.
    for key in libraries:
        if key not in done_libraries and libraries[key]['expose']:
            name = libraries[key]['name']
            import_maps['imports'][name] = f'{prefix}/_nicegui/{__version__}/library/{key}/include'
            done_libraries.add(key)
    # Build the none optimized component (ie, the vue component).
    for key in vue_components:
        if key not in done_components:
            vue_html += f'{vue_components[key].html}\n'
            vue_scripts += f'{vue_components[key].script.replace("Vue.component", "app.component", 1)}\n'
            vue_styles += f'{vue_components[key].style}\n'
            done_components.add(key)

    # Build the resources associated with the elements.
    for element in elements:
        for key in element.libraries:
            if key in libraries and key not in done_libraries:
                if not libraries[key]['expose']:
                    js_imports += f'import "{prefix}/_nicegui/{__version__}/library/{key}/include";\n'
                done_libraries.add(key)
        for key in element.components:
            if key in js_components and key not in done_components:
                name = js_components[key]['name']
                js_imports += f'import {{ default as {key} }} from "{prefix}/_nicegui/{__version__}/components/{key}";\n'
                js_imports += f'app.component("{name}", {key});\n'
                done_components.add(key)

    vue_styles = f'<style>{vue_styles}</style>'
    import_maps = f'<script type="importmap">{json.dumps(import_maps)}</script>'
    return vue_html, vue_styles, vue_scripts, import_maps, js_imports
