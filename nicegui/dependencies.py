from __future__ import annotations

import functools
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from . import core
from .dataclasses import KWONLY_SLOTS
from .helpers import hash_file_path
from .vbuild import VBuild
from .version import __version__

if TYPE_CHECKING:
    from .element import Element


@dataclass(**KWONLY_SLOTS)
class Component:
    key: str
    name: str
    path: Path
    _keys: ClassVar[set[str]] = set()
    _names: ClassVar[set[str]] = set()

    def __post_init__(self) -> None:
        assert self.key not in self._keys, f'Duplicate key "{self.key}" for {self.__class__.__name__} {self.path}'
        assert self.name not in self._names, f'Duplicate name "{self.name}" for {self.__class__.__name__} {self.path}'
        self._keys.add(self.key)
        self._names.add(self.name)

    @property
    def tag(self) -> str:
        """The tag of the component."""
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
class Resource:
    key: str
    path: Path
    _keys: ClassVar[set[str]] = set()

    def __post_init__(self) -> None:
        assert self.key not in self._keys, f'Duplicate key "{self.key}" for {self.__class__.__name__} {self.path}'
        self._keys.add(self.key)


@dataclass(**KWONLY_SLOTS)
class DynamicResource:
    name: str
    function: Callable


@dataclass(**KWONLY_SLOTS)
class Import:
    name: str
    path: Path
    _names: ClassVar[set[str]] = set()

    def __post_init__(self) -> None:
        assert self.name not in self._names, f'Duplicate name "{self.name}" for {self.__class__.__name__} {self.path}'
        self._names.add(self.name)


@dataclass(**KWONLY_SLOTS)
class Library(Import):
    key: str
    _keys: ClassVar[set[str]] = set()

    def __post_init__(self) -> None:
        assert self.key not in self._keys, f'Duplicate key "{self.key}" for {self.__class__.__name__} {self.path}'
        self._keys.add(self.key)


@dataclass(**KWONLY_SLOTS)
class EsmModule(Import):
    pass


vue_components: dict[str, VueComponent] = {}
js_components: dict[str, JsComponent] = {}
libraries: dict[str, Library] = {}
resources: dict[str, Resource] = {}
dynamic_resources: dict[str, DynamicResource] = {}
esm_modules: dict[str, EsmModule] = {}
importmap_overrides: dict[str, str] = {}


def register_vue_component(path: Path, *, max_time: float | None) -> Component:
    """Register a .vue or .js Vue component.

    Single-file components (.vue) are built right away
    to delegate this "long" process to the bootstrap phase
    and to avoid building the component on every single request.
    """
    key = compute_key(path, max_time=max_time)
    name = _get_name(path)
    if path.suffix == '.vue':
        if key in vue_components and vue_components[key].path == path:
            return vue_components[key]
        v = VBuild(path)
        vue_components[key] = VueComponent(key=key, name=name, path=path, html=v.html, script=v.script, style=v.style)
        return vue_components[key]
    if path.suffix == '.js':
        if key in js_components and js_components[key].path == path:
            return js_components[key]
        js_components[key] = JsComponent(key=key, name=name, path=path)
        return js_components[key]
    raise ValueError(f'Unsupported component type "{path.suffix}"')


def register_library(path: Path, *, max_time: float | None) -> Library:
    """Register a *.js library."""
    key = compute_key(path, max_time=max_time)
    name = _get_name(path)
    if path.suffix in {'.js', '.mjs'}:
        if key in libraries and libraries[key].path == path:
            return libraries[key]
        libraries[key] = Library(key=key, name=name, path=path)
        return libraries[key]
    raise ValueError(f'Unsupported library type "{path.suffix}"')


def register_resource(path: Path, *, max_time: float | None) -> Resource:
    """Register a resource."""
    key = compute_key(path, max_time=max_time)
    if key in resources and resources[key].path == path:
        return resources[key]
    resources[key] = Resource(key=key, path=path)
    return resources[key]


def register_dynamic_resource(name: str, function: Callable) -> DynamicResource:
    """Register a dynamic resource which returns the result of a function."""
    dynamic_resources[name] = DynamicResource(name=name, function=function)
    return dynamic_resources[name]


def register_esm(name: str, path: Path, *, max_time: float | None) -> None:
    """Register an ESM module."""
    esm_modules[compute_key(path, max_time=max_time)] = EsmModule(name=name, path=path)


def register_importmap_override(import_name: str, url: str) -> None:
    """Register an importmap override."""
    importmap_overrides[import_name] = url


@functools.cache
def compute_key(path: Path, *, max_time: float | None) -> str:
    """Compute a key for a given path using a hash function.

    If the path is relative to the NiceGUI base directory, the key is computed from the relative path.
    """
    NICEGUI_BASE = Path(__file__).parent
    try:
        rel_path = path.relative_to(NICEGUI_BASE)
    except ValueError:
        rel_path = path
    if path.is_file():
        return f'{hash_file_path(rel_path.parent, max_time=max_time)}/{path.name}'
    return hash_file_path(rel_path, max_time=max_time)


def _get_name(path: Path) -> str:
    return path.name.split('.', 1)[0]


def generate_resources(prefix: str, elements: Iterable[Element]) -> tuple[list[str],
                                                                          list[str],
                                                                          list[str],
                                                                          dict[str, str],
                                                                          list[str],
                                                                          list[str]]:
    """Generate the resources required by the elements to be sent to the client."""
    done_libraries: set[str] = set()
    done_components: set[str] = set()
    vue_scripts: list[str] = []
    vue_html: list[str] = []
    vue_styles: list[str] = []
    imports: dict[str, str] = {
        'vue': f'{prefix}/_nicegui/{__version__}/static/vue.esm-browser{".prod" if core.app.config.prod_js else ""}.js',
        'sass': f'{prefix}/_nicegui/{__version__}/static/sass.default.js',
        'immutable': f'{prefix}/_nicegui/{__version__}/static/immutable.es.js',
        'dompurify': f'{prefix}/_nicegui/{__version__}/static/dompurify.mjs',
    }
    js_imports: list[str] = []
    js_imports_urls: list[str] = [imports['vue']]

    # build the importmap structure for libraries
    for key, library in libraries.items():
        if key not in done_libraries:
            imports[library.name] = f'{prefix}/_nicegui/{__version__}/libraries/{key}'
            done_libraries.add(key)

    # build the importmap structure for ESM modules
    for key, esm_module in esm_modules.items():
        imports[f'{esm_module.name}'] = f'{prefix}/_nicegui/{__version__}/esm/{key}/index.js'
        imports[f'{esm_module.name}/'] = f'{prefix}/_nicegui/{__version__}/esm/{key}/'

    # update the importmap with the overrides
    imports.update(importmap_overrides)

    # build the none-optimized component (i.e. the Vue component)
    for key, vue_component in vue_components.items():
        if key not in done_components:
            vue_html.append(vue_component.html)
            url = f'{prefix}/_nicegui/{__version__}/components/{vue_component.key}'
            js_imports.append(f'import {{ default as {vue_component.name} }} from "{url}";')
            js_imports.append(f"{vue_component.name}.template = '#tpl-{vue_component.name}';")
            js_imports.append(f'app.component("{vue_component.tag}", {vue_component.name});')
            js_imports_urls.append(url)
            vue_styles.append(vue_component.style)
            done_components.add(key)

    # build the resources associated with the elements
    for element in elements:
        if element.component:
            js_component = element.component
            if js_component.key not in done_components and js_component.path.suffix.lower() == '.js':
                url = f'{prefix}/_nicegui/{__version__}/components/{js_component.key}'
                js_imports.append(f'import {{ default as {js_component.name} }} from "{url}";')
                js_imports.append(f'app.component("{js_component.tag}", {js_component.name});')
                js_imports_urls.append(url)
                done_components.add(js_component.key)

    return vue_html, vue_styles, vue_scripts, imports, js_imports, js_imports_urls
