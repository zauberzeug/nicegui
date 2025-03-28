# fmt: off
# ruff: noqa: E402
# pylint: disable=C0413
import os
import sys
from types import ModuleType


class WhateverModule(ModuleType):

    def __getattr__(self, name):
        return Whatever()

class Whatever:

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        return Whatever()

    def __call__(self, *args, **kwargs):
        return Whatever()

    def __mro_entries__(self, *args, **kwargs):
        return (Whatever, )

    def __add__(self, other):
        return Whatever()

if os.environ.get('NICEGUI_HOST'):
    sys.modules['nicegui.binding'] = WhateverModule('nicegui.binding')
    sys.modules['nicegui.elements'] = WhateverModule('nicegui.elements')
    sys.modules['nicegui.html'] = WhateverModule('nicegui.html')
    # NOTE: keep importing the run module
    sys.modules['nicegui.storage'] = WhateverModule('nicegui.storage')
    sys.modules['nicegui.ui'] = WhateverModule('nicegui.ui')
    sys.modules['nicegui.api_router'] = WhateverModule('nicegui.api_router')
    sys.modules['nicegui.app.app'] = WhateverModule('nicegui.app.app')
    sys.modules['nicegui.client'] = WhateverModule('nicegui.client')
    sys.modules['nicegui.context'] = WhateverModule('nicegui.context')
    sys.modules['nicegui.element_filter'] = WhateverModule('nicegui.element_filter')
    sys.modules['nicegui.nicegui'] = WhateverModule('nicegui.nicegui')
    sys.modules['nicegui.tailwind'] = WhateverModule('nicegui.tailwind')
    sys.modules['nicegui.version'] = WhateverModule('nicegui.version')

from . import binding, elements, html, run, storage, ui
from .api_router import APIRouter
from .app.app import App
from .client import Client
from .context import context
from .element_filter import ElementFilter
from .nicegui import app
from .tailwind import Tailwind
from .version import __version__

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
