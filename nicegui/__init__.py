import importlib.metadata

__version__: str = importlib.metadata.version('nicegui')

from . import elements, globals, ui
from .api_router import APIRouter
from .client import Client
from .nicegui import app
from .tailwind import Tailwind

__all__ = [
    'app',
    'Client',
    'elements',
    'globals',
    'Tailwind',
    'ui',
    '__version__',
]
