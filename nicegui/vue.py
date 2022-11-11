from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import vbuild
from starlette.responses import FileResponse
from starlette.routing import Route

components: Dict[str, Component] = {}


@dataclass
class Component:
    name: str
    path: Path
    dependencies: List[str]


def register_component(name: str, py_filepath: str, component_filepath: str, dependencies: List[str] = []) -> None:
    assert name not in components
    components[name] = Component(
        name=name,
        path=Path(py_filepath).parent / component_filepath,
        dependencies=[Path(py_filepath).parent / dependency for dependency in dependencies],
    )


def generate_vue_content() -> Tuple[str]:
    builds = [vbuild.VBuild(c.name, c.path.read_text()) for c in components.values() if c.path.suffix == '.vue']
    return (
        '\n'.join(v.html for v in builds),
        '<style>' + '\n'.join(v.style for v in builds) + '</style>',
        '\n'.join(v.script.replace('Vue.component', 'app.component', 1) for v in builds),
    )


def get_js_components() -> List[Component]:
    return [c for c in components.values() if c.path.suffix == '.js']


def generate_js_routes() -> List[Route]:
    routes: List[Route] = []
    for component in components.values():
        for dependency in component.dependencies:
            print(dependency, flush=True)
            routes.append(Route(f'/_vue/{component.name}/{dependency}',
                                lambda _, path=dependency: FileResponse(path, media_type='text/javascript')))
    for component in get_js_components():
        routes.append(Route(f'/_vue/{component.name}',
                            lambda _, path=component.path: FileResponse(path, media_type='text/javascript')))
    return routes


def generate_js_imports() -> str:
    result = ''
    for component in components.values():
        for dependency in component.dependencies:
            result += f'''
                import "/_vue/{component.name}/{dependency}";
            '''
    for component in get_js_components():
        result += f'''
            import {{ default as {component.name} }} from "/_vue/{component.name}";
            app.component("{component.name}", {component.name});
        '''
    return result
