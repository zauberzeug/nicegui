import importlib
import os
import sys
from types import ModuleType
from typing import TYPE_CHECKING

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
    if name not in _LAZY_IMPORTS:
        raise AttributeError(f"module 'nicegui' has no attribute {name!r}")
    module_path, attr_name = _LAZY_IMPORTS[name]
    module = importlib.import_module(module_path, package='nicegui')
    value = getattr(module, attr_name) if attr_name else module
    setattr(sys.modules[__name__], name, value)
    return value


class _PackageModule(ModuleType):
    """Class for the nicegui package module itself.

    The attributes `app` and `context` collide with the submodules `nicegui.app` and `nicegui.context`:
    whenever the import machinery loads those submodules, it binds them as package attributes, shadowing
    the `App` and `Context` instances which `__getattr__` would provide. (The eager package init used to win
    this race by assignment order.) Data descriptors on the module's class take precedence over instance
    attributes, so these properties always return the instances.
    """

    @property
    def app(self):
        """The global ``App`` instance (shadows the ``nicegui.app`` subpackage; see class docstring)."""
        if '_app_override' in self.__dict__:
            return self.__dict__['_app_override']
        from .nicegui import app  # pylint: disable=import-outside-toplevel,redefined-outer-name
        return app

    @app.setter
    def app(self, value) -> None:
        if not isinstance(value, ModuleType):  # silently absorb the import machinery's submodule binding only
            self.__dict__['_app_override'] = value  # support deliberate assignment, e.g. mock.patch

    @app.deleter
    def app(self) -> None:
        self.__dict__.pop('_app_override', None)

    @property
    def context(self):
        """The global ``Context`` instance (shadows the ``nicegui.context`` submodule; see class docstring)."""
        if '_context_override' in self.__dict__:
            return self.__dict__['_context_override']
        from .context import context  # pylint: disable=import-outside-toplevel,redefined-outer-name
        return context

    @context.setter
    def context(self, value) -> None:
        if not isinstance(value, ModuleType):  # silently absorb the import machinery's submodule binding only
            self.__dict__['_context_override'] = value  # support deliberate assignment, e.g. mock.patch

    @context.deleter
    def context(self) -> None:
        self.__dict__.pop('_context_override', None)


sys.modules[__name__].__class__ = _PackageModule
