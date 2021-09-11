from . import globals

def add_route(self, route):
    globals.app.routes.insert(0, route)
