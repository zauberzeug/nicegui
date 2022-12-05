from pathlib import Path
from typing import Dict, List, Tuple

import vbuild

from . import globals

vue_components: Dict[str, Path] = {}
js_components: Dict[str, Path] = {}
js_dependencies: Dict[str, List[Path]] = {}


def register_component(name: str, py_filepath: str, component_filepath: str, dependencies: List[str] = []) -> None:
    suffix = Path(component_filepath).suffix.lower()
    assert suffix in ['.vue', '.js'], 'Only VUE and JS components are supported.'
    if suffix == '.vue':
        assert name not in vue_components, f'Duplicate VUE component name {name}'
        vue_components[name] = Path(py_filepath).parent / component_filepath
    elif suffix == '.js':
        assert name not in js_components, f'Duplicate JS component name {name}'
        js_components[name] = Path(py_filepath).parent / component_filepath
    js_dependencies[name] = []
    for dependency in dependencies:
        assert Path(dependency).suffix == '.js', 'Only JS dependencies are supported.'
        js_dependencies[name].append(Path(py_filepath).parent / dependency)


def generate_vue_content() -> Tuple[str]:
    builds = [
        vbuild.VBuild(name, path.read_text())
        for name, path in vue_components.items()
        if name not in globals.excludes
    ]
    return (
        '\n'.join(v.html for v in builds),
        '<style>' + '\n'.join(v.style for v in builds) + '</style>',
        '\n'.join(v.script.replace('Vue.component', 'app.component', 1) for v in builds),
    )


def generate_js_imports(prefix: str) -> str:
    result = ''
    for name, path in vue_components.items():
        if name in globals.excludes:
            continue
        for path in js_dependencies[name]:
            result += f'import "{prefix}/_vue/dependencies/{path}";\n'
    for name, path in js_components.items():
        if name in globals.excludes:
            continue
        for path in js_dependencies[name]:
            result += f'import "{prefix}/_vue/dependencies/{path}";\n'
        result += f'import {{ default as {name} }} from "{prefix}/_vue/components/{name}";\n'
        result += f'app.component("{name}", {name});\n'
    return result
