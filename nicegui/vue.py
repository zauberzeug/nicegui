from pathlib import Path
from typing import Dict, List, Tuple

import vbuild
from starlette.responses import FileResponse
from starlette.routing import Route

components: Dict[str, Path] = {}


def register_component(name: str, py_filepath: str, component_filepath: str) -> None:
    assert name not in components
    components[name] = Path(py_filepath).parent / component_filepath


def generate_vue_content() -> Tuple[str]:
    builds = [vbuild.VBuild(p.name, p.read_text()) for p in components.values() if p.suffix == '.vue']
    return (
        '\n'.join(v.html for v in builds),
        '<style>' + '\n'.join(v.style for v in builds) + '</style>',
        '\n'.join(v.script.replace('Vue.component', 'app.component', 1) for v in builds),
    )


def get_js_components() -> Dict[str, str]:
    return {name: filepath for name, filepath in components.items() if filepath.suffix == '.js'}


def generate_js_routes() -> List[Route]:
    return [
        Route(f'/_vue/{name}', lambda _, filepath=filepath: FileResponse(filepath, media_type='text/javascript'))
        for name, filepath in get_js_components().items()
    ]


def generate_js_imports() -> str:
    return '\n'.join(f'''
        import {{ default as {name} }} from "/_vue/{name}";
        app.component("{name}", {name});
    ''' for name in get_js_components().keys())
