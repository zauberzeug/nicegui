from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Set, Tuple

import vbuild

from . import __version__
from .helpers import KWONLY_SLOTS

if TYPE_CHECKING:
    from .element import Element


@dataclass(**KWONLY_SLOTS)
class Component:
    key: str
    name: str
    path: Path

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
    pass


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
    :return: registered component
    """
    path, key, name, suffix = deconstruct_location(location, base_path)
    if suffix == '.vue':
        if key in vue_components and vue_components[key].path == path:
            return vue_components[key]
        assert key not in vue_components, f'Duplicate VUE component {key}'
        build = vbuild.VBuild(name, path.read_text())
        vue_components[key] = VueComponent(key=key, name=name, path=path,
                                           html=build.html, script=build.script, style=build.style)
        return vue_components[key]
    if suffix == '.js':
        if key in js_components and js_components[key].path == path:
            return js_components[key]
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
    :return: registered library
    """
    path, key, name, suffix = deconstruct_location(location, base_path)
    if suffix in {'.js', '.mjs'}:
        if key in libraries and libraries[key].path == path:
            return libraries[key]
        assert key not in libraries, f'Duplicate js library {key}'
        libraries[key] = Library(key=key, name=name, path=path, expose=expose)
        return libraries[key]
    raise ValueError(f'Unsupported library type "{suffix}"')


def deconstruct_location(location: Path, base_path: Path) -> Tuple[Path, str, str, str]:
    """Deconstruct a location into its parts: full path, relative path, name, suffix."""
    abs_path = location if location.is_absolute() else base_path / location
    rel_path = location if not location.is_absolute() else location.relative_to(base_path)
    return abs_path, str(rel_path), location.name.split('.', 1)[0], location.suffix.lower()


def generate_resources(prefix: str, elements: List[Element]) -> Tuple[List[str],
                                                                      List[str],
                                                                      List[str],
                                                                      Dict[str, str],
                                                                      List[str]]:
    done_libraries: Set[str] = set()
    done_components: Set[str] = set()
    vue_scripts: List[str] = []
    vue_html: List[str] = []
    vue_styles: List[str] = []
    js_imports: List[str] = []
    imports: Dict[str, str] = {}

    # build the importmap structure for exposed libraries
    for key, library in libraries.items():
        if key not in done_libraries and library.expose:
            imports[library.name] = f'{prefix}/_nicegui/{__version__}/libraries/{key}'
            done_libraries.add(key)

    # build the none-optimized component (i.e. the Vue component)
    for key, component in vue_components.items():
        if key not in done_components:
            vue_html.append(component.html)
            vue_scripts.append(component.script.replace(f"Vue.component('{component.name}',",
                                                        f"app.component('{component.tag}',", 1))
            vue_styles.append(component.style)
            done_components.add(key)

    # build the resources associated with the elements
    for element in elements:
        for library in element.libraries:
            if library.key not in done_libraries:
                if not library.expose:
                    js_imports.append(f'import "{prefix}/_nicegui/{__version__}/libraries/{library.key}";')
                done_libraries.add(library.key)
        for component in element.components:
            if component.key not in done_components and component.path.suffix.lower() == '.js':
                js_imports.extend([
                    f'import {{ default as {component.name} }} from "{prefix}/_nicegui/{__version__}/components/{component.key}";',
                    f'app.component("{component.tag}", {component.name});',
                ])
                done_components.add(component.key)
    return vue_html, vue_styles, vue_scripts, imports, js_imports
