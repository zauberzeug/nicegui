import os
import sys
from types import ModuleType
from typing import TYPE_CHECKING

from . import _lazy

if os.environ.get('NICEGUI_WORKER_STUBS') == '1':
    import multiprocessing  # cheap here: already imported by the spawn bootstrap in any real worker
    if multiprocessing.current_process().name != 'MainProcess':
        from . import _worker_stubs
        _worker_stubs.install()

_LAZY_IMPORTS = {
    'APIRouter': ('.api_router', 'APIRouter'),
    'App': ('.app.app', 'App'),
    'Client': ('.client', 'Client'),
    'ElementFilter': ('.element_filter', 'ElementFilter'),
    'Event': ('.event', 'Event'),
    'PageArguments': ('.page_arguments', 'PageArguments'),
    '__version__': ('.version', '__version__'),
    'app': ('.nicegui', 'app'),
    'binding': ('.binding', ''),
    'context': ('.context', 'context'),
    'elements': ('.elements', ''),
    'html': ('.html', ''),
    'run': ('.run', ''),
    'storage': ('.storage', ''),
    'ui': ('.ui', ''),
}

if TYPE_CHECKING:
    from . import binding, elements, html, run, storage, ui
    from .api_router import APIRouter
    from .app.app import App
    from .client import Client
    from .context import context
    from .element_filter import ElementFilter
    from .event import Event
    from .nicegui import app
    from .page_arguments import PageArguments
    from .version import __version__

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
    'run',
    'storage',
    'ui',
]


def __dir__() -> list[str]:
    return __all__


def __getattr__(name: str) -> object:
    return _lazy.resolve(__name__, 'nicegui', _LAZY_IMPORTS, name)


class _PackageModule(ModuleType):
    """Class for the nicegui package module itself.

    The attributes ``app`` and ``context`` collide with the submodules ``nicegui.app`` and ``nicegui.context``:
    whenever the import machinery loads those submodules, it binds them as package attributes,
    shadowing the ``App`` and ``Context`` instances which ``__getattr__`` provides.
    (The eager package init used to win this race by assignment order.)
    Ignoring module bindings for these two names keeps them resolvable via ``__getattr__``,
    while non-module assignments (e.g. ``mock.patch``) still work as plain instance attributes.
    """

    def __setattr__(self, name: str, value: object) -> None:
        if name in {'app', 'context'} and isinstance(value, ModuleType):
            return  # absorb the import machinery's submodule binding (see class docstring)
        super().__setattr__(name, value)


sys.modules[__name__].__class__ = _PackageModule
