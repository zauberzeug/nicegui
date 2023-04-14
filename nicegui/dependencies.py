import json
import warnings
from pathlib import Path
from typing import Any, Dict, List, Tuple

import vbuild

from . import __version__


class Legacy():
    """ @todo remove when register_component is removed. """
    components: List[str] = []
    libraries: List[str] = []


legacy = Legacy()  # @todo remove when register_component is removed.
vue_components: Dict[str, Any] = {}
js_components: Dict[str, Any] = {}
libraries: Dict[str, Any] = {}


def register_vue_component(name: str, path: Path) -> None:
    """
    Register a .vue or .js vue component.
    :param name: the component unique machine-name (used in component `use_library`): no space, no special characters.
    :param path: the component local path.
    """
    index = f'vue_{name}'
    suffix = path.suffix.lower()
    assert suffix in {'.vue', '.js', '.mjs'}, 'Only VUE and JS components are supported.'
    if suffix == '.vue':
        assert index not in vue_components, f'Duplicate VUE component name {name}'
        # The component (in case of .vue) is built right away to:
        #         1. delegate this 'long' process to the bootstrap phase
        #         2. avoid building the component on every single requests
        vue_components[index] = vbuild.VBuild(name, path.read_text())
    elif suffix == '.js':
        assert index not in js_components, f'Duplicate JS component name {name}'
        js_components[index] = {'name': name, 'path': path}


def register_library(name: str, path: Path, expose: bool = False) -> None:
    """
    Register a  new external library.
    :param name: the library unique machine-name (used in component `use_library`): no space, no special characters.
    :param path: the library local path.
    :param expose: if True, this will be exposed as an ESM module but NOT imported.
    """
    assert path.suffix == '.js' or path.suffix == '.mjs', 'Only JS dependencies are supported.'
    index = f'lib_{name}'
    libraries[index] = {'name': name, 'path': path, 'expose': expose}


def register_component(name: str, py_filepath: str, component_filepath: str, dependencies: List[str] = [],
                       optional_dependencies: List[str] = []) -> None:
    """
    Deprecated method. Use `register_vue_component` or `register_library` library instead.
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


def generate_resources(prefix: str, elements) -> Tuple[str, str, str, str, str]:
    done = []
    vue_scripts = ''
    vue_html = ''
    vue_styles = ''
    js_imports = ''
    import_maps = {'imports': {}}

    # Build the resources associated with the elements.
    all_elements = list(elements)  # @todo remove all_elements when legacy support is dropped.
    all_elements.append(legacy)
    for element in all_elements:  # @todo 'in elements' iteration when legacy support is dropped.
        for index in element.libraries:
            if index in libraries and index not in done:
                if libraries[index]['expose']:
                    name = libraries[index]['name']
                    import_maps['imports'][name] = f'{prefix}/_nicegui/{__version__}/library/{index}/include'
                else:
                    js_imports += f'import "{prefix}/_nicegui/{__version__}/library/{index}/include";\n'
                done.append(index)
        for index in element.components:
            if index in vue_components and index not in done:
                vue_html += f'{vue_components[index].html}\n'
                vue_scripts += f'{vue_components[index].script.replace("Vue.component", "app.component", 1)}\n'
                vue_styles += f'{vue_components[index].style}\n'
                done.append(index)
            if index in js_components and index not in done:
                name = js_components[index]['name']
                js_imports += f'import {{ default as {index} }} from "{prefix}/_nicegui/{__version__}/components/{index}";\n'
                js_imports += f'app.component("{name}", {index});\n'
                done.append(index)

    vue_styles = f'<style>{vue_styles}</style>'
    import_maps = f'<script type="importmap">{json.dumps(import_maps)}</script>'
    return vue_html, vue_styles, vue_scripts, import_maps, js_imports
