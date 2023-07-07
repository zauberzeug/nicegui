from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

import vbuild

from . import __version__
from .element import Element
from .helpers import KWONLY_SLOTS


@dataclass(**KWONLY_SLOTS)
class Component:
    key: str
    name: str

    @property
    def tag(self) -> str:
        return f'nicegui-{self.name}'


@dataclass(**KWONLY_SLOTS)
class VueComponent(Component):
    html: str
    script: str
    style: str


@dataclass(**KWONLY_SLOTS)
class JsComponent(Component):
    path: Path


@dataclass(**KWONLY_SLOTS)
class Library:
    key: str
    name: str
    path: Path
    expose: bool


vue_components: Dict[str, VueComponent] = {}
js_components: Dict[str, JsComponent] = {}
libraries: Dict[str, Library] = {}


def register_vue_component(location: Path, base_path: Path = Path(__file__).parent / 'elements') -> Component:
    """Register a .vue or .js Vue component.

    Single-file components (.vue) are built right away
    to delegate this "long" process to the bootstrap phase
    and to avoid building the component on every single request.

    :param location: location to the library relative to the base_path (used as the resource identifier, must be URL-safe)
    :param base_path: base path where your libraries are located
    :return: resource identifier to be used in element's `use_component`
    """
    path, key, name, suffix = deconstruct_location(location, base_path)
    if suffix == '.vue':
        assert key not in vue_components, f'Duplicate VUE component {key}'
        build = vbuild.VBuild(name, path.read_text())
        vue_components[key] = VueComponent(key=key, name=name, html=build.html, script=build.script, style=build.style)
        return vue_components[key]
    if suffix == '.js':
        assert key not in js_components, f'Duplicate JS component {key}'
        js_components[key] = JsComponent(key=key, name=name, path=path)
        return js_components[key]
    raise ValueError(f'Unsupported component type "{suffix}"')


def register_library(location: Path, base_path: Path = Path(__file__).parent / 'elements' / 'lib', *,
                     expose: bool = False) -> Library:
    """Register a *.js library.

    :param location: location to the library relative to the base_path (used as the resource identifier, must be URL-safe)
    :param base_path: base path where your libraries are located
    :param expose: whether to expose library as an ESM module (exposed modules will NOT be imported)
    :return: resource identifier to be used in element's `use_library`
    """
    path, key, name, suffix = deconstruct_location(location, base_path)
    if suffix in {'.js', '.mjs'}:
        assert key not in libraries, f'Duplicate js library {key}'
        libraries[key] = Library(key=key, name=name, path=path, expose=expose)
        return libraries[key]
    raise ValueError(f'Unsupported library type "{suffix}"')


def deconstruct_location(location: Path, base_path: Path) -> Tuple[Path, str, str, str]:
    """Deconstruct a location into its parts: full path, relative path, name, suffix."""
    return base_path / location, str(location), location.name.split('.', 1)[0], location.suffix.lower()


def generate_resources(prefix: str, elements: List[Element]) -> Tuple[str, str, str, str, str]:
    done_libraries: Set[str] = set()
    done_components: Set[str] = set()
    vue_scripts: str = ''
    vue_html: str = ''
    vue_styles: str = ''
    js_imports: str = ''
    imports: Dict[str, str] = {}

    # build the importmap structure for exposed libraries
    for key, library in libraries.items():
        if key not in done_libraries and library.expose:
            imports[library.name] = f'{prefix}/_nicegui/{__version__}/libraries/{key}'
            done_libraries.add(key)

    # build the none-optimized component (i.e. the Vue component)
    for key, component in vue_components.items():
        if key not in done_components:
            vue_html += f'{component.html}\n'
            vue_scripts += component.script.replace(f"Vue.component('{component.name}',",
                                                    f"app.component('{component.tag}',", 1) + '\n'
            vue_styles += f'{component.style}\n'
            done_components.add(key)

    # build the resources associated with the elements
    for element in elements:
        if key.startswith('nipple'):
            print(key, flush=True)
        for key in element.libraries:
            if key in libraries and key not in done_libraries:
                if not libraries[key].expose:
                    js_imports += f'import "{prefix}/_nicegui/{__version__}/libraries/{key}";\n'
                done_libraries.add(key)
        for key in element.components:
            if key in js_components and key not in done_components:
                component = js_components[key]
                js_imports += f'import {{ default as {component.name} }} from "{prefix}/_nicegui/{__version__}/components/{key}";\n'
                js_imports += f'app.component("{component.tag}", {component.name});\n'
                done_components.add(key)
    vue_styles = f'<style>{vue_styles}</style>'
    return vue_html, vue_styles, vue_scripts, imports, js_imports
