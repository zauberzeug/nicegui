from functools import wraps
import inspect
from starlette import routing, requests
from . import globals

def add_route(self, route):
    """
    :param route: starlette route including a path and a function to be called
    :return:
    """
    globals.app.routes.insert(0, route)

def get(self, path: str):
    """
    Use as a decorator for a function like @ui.get('/another/route/{id}').
    :param path: string that starts with a '/'
    :return:
    """
    *_, converters = routing.compile_path(path)

    def decorator(func):
        @wraps(func)
        def decorated(request: requests.Request):
            args = {name: converter.convert(request.path_params.get(name)) for name, converter in converters.items()}
            if 'request' in inspect.signature(func).parameters:
                args['request'] = request
            return func(**args)
        self.add_route(routing.Route(path, decorated))
        return decorated
    return decorator
