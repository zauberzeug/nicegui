import inspect
from functools import wraps

import justpy as jp
from starlette import requests, routing
from starlette.routing import BaseRoute, Mount
from starlette.staticfiles import StaticFiles

from nicegui.elements.page import Page

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


def private_page(self, path: str):
    '''
    Use as a decorator for a function like this:

    @ui.private_page('/private')
    def create_private_page():
        ui.label(f'your private page {uuid4()}')
    '''
    def decorator(func):
        @wraps(func)
        async def decorated():
            with Page(None) as page:
                await func() if is_coroutine(func) else func()
            return page
        jp.Route(path, decorated)
        return decorated
    return decorator
