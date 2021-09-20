from starlette.routing import Route
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
    def decorator(func):
        self.add_route(Route(path, func))
        return func
    return decorator
