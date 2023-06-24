from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

import vbuild

from . import __version__, globals
from .helpers import KWONLY_SLOTS
from .ids import IncrementingStringIds


@dataclass(**KWONLY_SLOTS)
class Component:
    name: str
    path: Path

    @property
    def import_path(self) -> str:
        return f'/_nicegui/{__version__}/components/{self.name}'


@dataclass(**KWONLY_SLOTS)
class Dependency:
    id: int
    path: Path
    dependents: Set[str]
    optional: bool

    @property
    def import_path(self) -> str:
        return f'/_nicegui/{__version__}/dependencies/{self.id}/{self.path.name}'


dependency_ids = IncrementingStringIds()

vue_components: Dict[str, Component] = {}
js_components: Dict[str, Component] = {}
js_dependencies: Dict[int, Dependency] = {}


def register_component(name: str, py_filepath: str, component_filepath: str, dependencies: List[str] = [],
                       optional_dependencies: List[str] = []) -> None:
    suffix = Path(component_filepath).suffix.lower()
    assert suffix in {'.vue', '.js'}, 'Only VUE and JS components are supported.'
    if suffix == '.vue':
        assert name not in vue_components, f'Duplicate VUE component name {name}'
        vue_components[name] = Component(name=name, path=Path(py_filepath).parent / component_filepath)
    elif suffix == '.js':
        assert name not in js_components, f'Duplicate JS component name {name}'
        js_components[name] = Component(name=name, path=Path(py_filepath).parent / component_filepath)
    for dependency in dependencies + optional_dependencies:
        path = Path(py_filepath).parent / dependency
        assert path.suffix == '.js', 'Only JS dependencies are supported.'
        id = dependency_ids.get(str(path.resolve()))
        if id not in js_dependencies:
            optional = dependency in optional_dependencies
            js_dependencies[id] = Dependency(id=id, path=path, dependents=set(), optional=optional)
        js_dependencies[id].dependents.add(name)


def generate_vue_content() -> Tuple[str, str, str]:
    builds = [
        vbuild.VBuild(name, component.path.read_text())
        for name, component in vue_components.items()
        if name not in globals.excludes
    ]
    return (
        '\n'.join(v.html for v in builds),
        '<style>' + '\n'.join(v.style for v in builds) + '</style>',
        '\n'.join(v.script.replace('Vue.component', 'app.component', 1) for v in builds),
    )


def generate_js_imports(prefix: str) -> str:
    result = ''
    for dependency in js_dependencies.values():
        if dependency.optional:
            continue
        if not dependency.dependents.difference(globals.excludes):
            continue
        result += f'import "{prefix}{dependency.import_path}";\n'
    for name, component in js_components.items():
        if name in globals.excludes:
            continue
        var_name = name.replace('-', '_')
        result += f'import {{ default as {var_name} }} from "{prefix}{component.import_path}";\n'
        result += f'app.component("{name}", {var_name});\n'
    return result
