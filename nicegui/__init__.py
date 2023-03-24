try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version('nicegui')

from . import elements, globals, ui
from .client import Client
from .nicegui import app
