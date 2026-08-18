import importlib
import sys
from types import ModuleType
from typing import TYPE_CHECKING

from . import _lazy

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
_NON_MODULE_LAZY_IMPORTS = {name for name, (_, attr) in _LAZY_IMPORTS.items() if attr}

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
    return sorted(set(__all__) | set(globals()))


def __getattr__(name: str) -> object:
    if name not in _LAZY_IMPORTS and not name.startswith('_'):
        try:
            # import submodules on demand, so that `import nicegui; nicegui.<submodule>` keeps working as on an
            # eagerly initialized package - independently of what has been imported before
            return importlib.import_module(f'.{name}', __name__)
        except ModuleNotFoundError as e:
            if e.name != f'{__name__}.{name}':
                raise  # the submodule exists, but one of its own imports is missing
    return _lazy.resolve(__name__, 'nicegui', _LAZY_IMPORTS, name)


class _PackageModule(ModuleType):
    """Class for the nicegui package module itself.

    Lazy imports of objects rather than modules (``app``, ``context``, ...) can collide with equally named submodules
    (``nicegui.app``, ``nicegui.context``, ...): whenever the import machinery loads such a submodule,
    it binds it as a package attribute, shadowing the object which ``__getattr__`` provides.
    (The eager package init used to win this race by assignment order.)
    Ignoring module bindings for these names keeps them resolvable via ``__getattr__``,
    while non-module assignments (e.g. ``mock.patch``) still work as plain instance attributes.
    """

    def __setattr__(self, name: str, value: object) -> None:
        if name in _NON_MODULE_LAZY_IMPORTS and isinstance(value, ModuleType):
            return  # absorb the import machinery's submodule binding (see class docstring)
        super().__setattr__(name, value)


sys.modules[__name__].__class__ = _PackageModule
