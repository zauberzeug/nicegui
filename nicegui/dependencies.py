import json
import warnings
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import vbuild

from .element import Element
from . import __version__


class Legacy:
    """ @todo remove when register_component is removed. """
    components: List[str] = []
    libraries: List[str] = []


legacy = Legacy()  # @todo remove when register_component is removed.
vue_components: Dict[str, Any] = {}
js_components: Dict[str, Any] = {}
libraries: Dict[str, Any] = {}


def register_vue_component(name: str, path: Path) -> None:
    """Register a .vue or .js vue component.

    :param name: the component's unique machine-name (used in component `use_library`): no space, no special characters
    :param path: the component's local path
    """
    key = f'vue_{name}'
    suffix = path.suffix.lower()
    assert suffix in {'.vue', '.js', '.mjs'}, 'Only VUE and JS components are supported.'
    if suffix == '.vue':
        assert key not in vue_components, f'Duplicate VUE component name {name}'
        # The component (in case of .vue) is built right away to:
        # 1. delegate this "long" process to the bootstrap phase
        # 2. avoid building the component on every single request
        vue_components[key] = vbuild.VBuild(name, path.read_text())
    elif suffix == '.js':
        assert key not in js_components, f'Duplicate JS component name {name}'
        js_components[key] = {'name': name, 'path': path}


def register_library(name: str, path: Path, expose: bool = False) -> None:
    """Register a new external library.

    :param name: the library's unique machine-name (used in component `use_library`): no space, no special characters
    :param path: the library's local path
    :param expose: if True, this will be exposed as an ESM module but NOT imported
    """
    assert path.suffix == '.js' or path.suffix == '.mjs', 'Only JS dependencies are supported.'
    key = f'lib_{name}'
    libraries[key] = {'name': name, 'path': path, 'expose': expose}


def register_component(name: str, py_filepath: str, component_filepath: str, dependencies: List[str] = [],
                       optional_dependencies: List[str] = []) -> None:
    """Deprecated method.

    Use `register_vue_component` or `register_library` library instead.
    """
    url = f'https://github.com/zauberzeug/nicegui/pull/658'
    warnings.warn(DeprecationWarning(
        f'This function is deprecated. Use either register_vue_component or register_library instead, along with `use_component` or `use_library` ({url}).'))

    suffix = Path(component_filepath).suffix.lower()
    if suffix in {'.vue', '.js'}:
        register_vue_component(name, Path(Path(py_filepath).parent, component_filepath).absolute())
        legacy.components.append(f'vue_{name}')

    for idx, dependency in enumerate(dependencies + optional_dependencies):
        path = Path(Path(py_filepath).parent, dependency)
        register_library(name + str(idx), path)
        legacy.libraries.append(f'lib_{name}{idx}')


def generate_resources(prefix: str, elements: List[Element]) -> Tuple[str, str, str, str, str]:
    done: Set[str] = set()
    vue_scripts = ''
    vue_html = ''
    vue_styles = ''
    js_imports = ''
    import_maps = {'imports': {}}

    # Build the importmap structure for exposed libraries.
    for key in libraries:
        if key not in done and libraries[key]['expose']:
            name = libraries[key]['name']
            import_maps['imports'][name] = f'{prefix}/_nicegui/{__version__}/library/{key}/include'
            done.add(key)
    # Build the none optimized component (ie, the vue component).
    for key in vue_components:
        if key not in done:
            vue_html += f'{vue_components[key].html}\n'
            vue_scripts += f'{vue_components[key].script.replace("Vue.component", "app.component", 1)}\n'
            vue_styles += f'{vue_components[key].style}\n'
            done.add(key)

    # Build the resources associated with the elements.
    all_elements = list(elements)  # @todo remove all_elements when legacy support is dropped.
    all_elements.append(legacy)
    for element in all_elements:  # @todo 'in elements' iteration when legacy support is dropped.
        for key in element.libraries:
            if key in libraries and key not in done:
                if not libraries[key]['expose']:
                    js_imports += f'import "{prefix}/_nicegui/{__version__}/library/{key}/include";\n'
                done.add(key)
        for key in element.components:
            if key in js_components and key not in done:
                name = js_components[key]['name']
                js_imports += f'import {{ default as {key} }} from "{prefix}/_nicegui/{__version__}/components/{key}";\n'
                js_imports += f'app.component("{name}", {key});\n'
                done.add(key)

    vue_styles = f'<style>{vue_styles}</style>'
    import_maps = f'<script type="importmap">{json.dumps(import_maps)}</script>'
    return vue_html, vue_styles, vue_scripts, import_maps, js_imports
