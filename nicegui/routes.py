import asyncio
import inspect
import os.path
from functools import wraps
from typing import List

import justpy as jp
from starlette import requests, routing
from starlette.responses import FileResponse
from starlette.routing import BaseRoute, Mount, Route
from starlette.staticfiles import StaticFiles

from . import globals
from .helpers import is_coroutine
from .page import Page, get_current_view
from .task_logger import create_task


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
    *_, converters = routing.compile_path(path)

    def decorator(func):
        @wraps(func)
        async def decorated(request: requests.Request):
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
        self.add_route(routing.Route(path, decorated))
        return decorated
    return decorator


def add_dependencies(py_filepath: str, dependencies: List[str] = []) -> None:
    if py_filepath in globals.dependencies:
        return
    globals.dependencies[py_filepath] = dependencies

    new_dependencies: List[str] = []

    vue_filepath = os.path.splitext(os.path.realpath(py_filepath))[0] + '.js'
    if vue_filepath not in jp.component_file_list:
        filename = os.path.basename(vue_filepath)
        jp.app.routes.insert(0, Route(f'/{filename}', lambda _: FileResponse(vue_filepath)))
        jp.component_file_list += [filename]
        new_dependencies.append(filename)

    for dependency in dependencies:
        is_remote = dependency.startswith('http://') or dependency.startswith('https://')
        src = dependency if is_remote else f'lib/{dependency}'
        if src not in jp.component_file_list:
            jp.component_file_list += [src]
            if not is_remote:
                filepath = f'{os.path.dirname(vue_filepath)}/{src}'
                route = Route(f'/{src}', lambda _, filepath=filepath: FileResponse(filepath))
                jp.app.routes.insert(0, route)
            new_dependencies.append(src)

    if asyncio.get_event_loop().is_running():
        create_task(inject_dependencies(new_dependencies))


async def inject_dependencies(dependencies: List[str]) -> None:
    for page in get_current_view().pages.values():
        assert isinstance(page, Page)
        for src in dependencies:
            await page.await_javascript(f'''
            let script = document.createElement("script");
            script.src = "{src}";
            document.body.append(script);
            ''')
        await page.update()
