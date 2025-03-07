__all__ = [
    'APIRouter',
    'App',
    'Client',
    'ElementFilter',
    'Tailwind',
    '__version__',
    'app',
    'binding',
    'context',
    'elements',
    'html',
    'run',
    'storage',
    'ui',
]


@profile
def import_all():
    global binding, elements, html, run, storage, ui, APIRouter, App, Client, context, ElementFilter, app, Tailwind, __version__
    if True:
        from . import binding
    if True:
        from . import elements
    if True:
        from . import html
    if True:
        from . import run
    if True:
        from . import storage
    if True:
        from . import ui
    from .api_router import APIRouter
    from .app.app import App
    from .client import Client
    from .context import context
    from .element_filter import ElementFilter
    from .nicegui import app
    from .tailwind import Tailwind
    from .version import __version__


import_all()
