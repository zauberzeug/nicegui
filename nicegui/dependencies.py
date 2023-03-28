import warnings
from pathlib import Path
from typing import Any, Dict, List, Tuple

import vbuild

from . import __version__

js_dependencies: Dict[str, Any] = {}  # @todo remove when unused in elements.
vue_components: Dict[str, Any] = {}
js_components: Dict[str, Path] = {}
libraries: Dict[str, Any] = {}


def register_vue_component(name: str, path: Path) -> None:
    """
    Register a .vue or .js vue component.
    The component (in case of .vue) is built right away to:
        1. delegate this 'long' process to the bootstrap phase
        2. avoid building the component on every single requests
    """
    suffix = path.suffix.lower()
    assert suffix in {'.vue', '.js'}, 'Only VUE and JS components are supported.'
    if suffix == '.vue':
        assert name not in vue_components, f'Duplicate VUE component name {name}'
        vue_components[name] = vbuild.VBuild(name, path.read_text())
    elif suffix == '.js':
        assert name not in js_components, f'Duplicate JS component name {name}'
        js_components[name] = path


def register_library(name: str, path: Path) -> None:
    """
    Register a  new external library.
    :param name: the library unique name (used in component `use_library`).
    :param path: the library local path.
    """
    assert path.suffix == '.js', 'Only JS dependencies are supported.'
    libraries[name] = {'path': path}


def register_component(name: str, py_filepath: str, component_filepath: str, dependencies: List[str] = [],
                       optional_dependencies: List[str] = []) -> None:
    """
    Deprecated method. Use `register_vue_component` or `register_library` library instead.
    """

    url = f'https://github.com/zauberzeug/nicegui/pull/xxx'  # @todo to be defined.
    warnings.warn(DeprecationWarning(
        f'This function is deprecated. Use either register_vue_component or register_library instead, along with `use_component` or `use_library` ({url}).'))

    suffix = Path(component_filepath).suffix.lower()
    if suffix in {'.vue', '.js'}:
        register_vue_component(name, Path(Path(py_filepath).parent, component_filepath).absolute())

    for dependency in dependencies + optional_dependencies:
        path = Path(Path(py_filepath).parent, dependency)
        register_library(name, path)


def generate_resources(prefix: str, elements) -> Tuple[str, str, str, str, str]:
    vue_scripts = ''
    vue_html = ''
    vue_styles = ''
    js_imports = ''
    es5_exposes = ''

    # Build the resources associated with the elements.
    for element in elements:
        for name in element.components:
            if name in vue_components:
                vue_html += f'{vue_components[name].html}\n'
                vue_scripts += f'{vue_components[name].script.replace("Vue.component", "app.component", 1)}\n'
                vue_styles += f'{vue_components[name].style}\n'
            if name in js_components:
                js_imports += f'import {{ default as {name} }} "{prefix}{js_components[name]}";\n'
                js_imports += f'app.component("{name}", {name});\n'
        for name in element.libraries:
            if name in libraries:
                js_imports += f'import "{prefix}/_nicegui/{__version__}/library/{name}";\n'

    vue_styles = f'<style>{vue_styles}</style>'
    return vue_html, vue_styles, vue_scripts, es5_exposes, js_imports
