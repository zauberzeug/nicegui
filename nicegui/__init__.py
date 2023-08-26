import importlib.metadata

__version__: str = importlib.metadata.version('nicegui')

from . import elements, globals, ui  # pylint: disable=redefined-builtin
from .api_router import APIRouter
from .client import Client
from .nicegui import app
from .tailwind import Tailwind

__all__ = [
    'APIRouter',
    'app',
    'Client',
    'elements',
    'globals',
    'Tailwind',
    'ui',
    '__version__',
]
