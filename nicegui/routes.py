import inspect
import os.path
from functools import wraps
from typing import List

import justpy as jp
from starlette.requests import Request
from starlette.responses import FileResponse, PlainTextResponse
from starlette.routing import BaseRoute, Mount, Route, compile_path
from starlette.staticfiles import StaticFiles

from . import globals
from .helpers import is_coroutine


def add_route(self, route: BaseRoute) -> None:
    """
    :param route: starlette route including a path and a function to be called
    :return:
    """
    globals.app.routes.insert(0, route)


def add_static_files(self, path: str, directory: str) -> None:
    """
    :param path: string that starts with a '/'
    :param directory: folder with static files to serve under the given path
    """
    add_route(None, Mount(path, app=StaticFiles(directory=directory)))


def get(self, path: str):
    """
    Use as a decorator for a function like @ui.get('/another/route/{id}').
    :param path: string that starts with a '/'
    :return:
    """
    *_, converters = compile_path(path)

    def decorator(func):
        @wraps(func)
        async def decorated(request: Request):
            args = {name: converter.convert(request.path_params.get(name)) for name, converter in converters.items()}
            parameters = inspect.signature(func).parameters
            for key in parameters:
                if parameters[key].annotation.__name__ == 'bool':
                    args[key] = bool(args[key])
                if parameters[key].annotation.__name__ == 'int':
                    args[key] = int(args[key])
                elif parameters[key].annotation.__name__ == 'float':
                    args[key] = float(args[key])
                elif parameters[key].annotation.__name__ == 'complex':
                    args[key] = complex(args[key])
            if 'request' in parameters and 'request' not in args:
                args['request'] = request
            return await func(**args) if is_coroutine(func) else func(**args)
        self.add_route(Route(path, decorated))
        return decorated
    return decorator


def add_dependencies(py_filepath: str, dependencies: List[str] = []) -> None:
    vue_filepath = os.path.splitext(os.path.realpath(py_filepath))[0] + '.js'

    for dependency in dependencies:
        is_remote = dependency.startswith('http://') or dependency.startswith('https://')
        src = dependency if is_remote else f'lib/{dependency}'
        if src not in jp.component_file_list:
            jp.component_file_list += [src]
            if not is_remote:
                filepath = f'{os.path.dirname(vue_filepath)}/{src}'
                route = Route(f'/{src}', lambda _, filepath=filepath: FileResponse(filepath))
                jp.app.routes.insert(0, route)

    if vue_filepath not in jp.component_file_list:
        filename = os.path.basename(vue_filepath)
        jp.app.routes.insert(0, Route(f'/{filename}', lambda _: FileResponse(vue_filepath)))
        jp.component_file_list += [filename]


def create_exclude_routes() -> None:
    def void(_: Request) -> PlainTextResponse:
        return PlainTextResponse()

    if 'chart' in globals.config.excludes:
        add_route(None, Route('/templates/local/highcharts.js', void))
    if 'colors' in globals.config.excludes:
        add_route(None, Route('/colors.js', void))
    if 'custom_example' in globals.config.excludes:
        add_route(None, Route('/custom_example.js', void))
    if 'interactive_image' in globals.config.excludes:
        add_route(None, Route('/interactive_image.js', void))
    if 'keyboard' in globals.config.excludes:
        add_route(None, Route('/keyboard.js', void))
    if 'log' in globals.config.excludes:
        add_route(None, Route('/log.js', void))
    if 'joystick' in globals.config.excludes:
        add_route(None, Route('/joystick.js', void))
        add_route(None, Route('/lib/nipplejs.min.js', void))
    if 'scene' in globals.config.excludes:
        add_route(None, Route('/scene.js', void))
        add_route(None, Route('/lib/CSS2DRenderer.js', void))
        add_route(None, Route('/lib/CSS3DRenderer.js', void))
        add_route(None, Route('/lib/OrbitControls.js', void))
        add_route(None, Route('/lib/STLLoader.js', void))
        add_route(None, Route('/lib/three.min.js', void))
        add_route(None, Route('/lib/tween.umd.min.js', void))
    if 'table' in globals.config.excludes:
        add_route(None, Route('/templates/local/ag-grid-community.js', void))
