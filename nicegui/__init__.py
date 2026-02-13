from . import binding, elements, html, storage, ui
from .api_router import APIRouter
from .app.app import App
from .client import Client
from .context import context
from .element_filter import ElementFilter
from .event import Event
from .page_arguments import PageArguments
from .pyodide_compat import IS_PYODIDE
from .version import __version__

if not IS_PYODIDE:
    from . import run
    from .nicegui import app
    from .page import page
else:
    run = None  # type: ignore
    from . import core as _core
    from .page_pyodide import page  # type: ignore
    _core.app = App()
    app = _core.app

__all__ = [
    'APIRouter',
    'App',
    'Client',
    'ElementFilter',
    'Event',
    'PageArguments',
    '__version__',
    'app',
    'binding',
    'context',
    'elements',
    'html',
    'page',
    'run',
    'storage',
    'ui',
]
