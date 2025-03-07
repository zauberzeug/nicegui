# NOTE: run this file like this:
#
# kernprof -l -v profile_imports.py

import os
import sys
from types import ModuleType

from line_profiler import LineProfiler

os.environ['MATPLOTLIB'] = 'false'

profile = LineProfiler()
sys.modules['__main__'].__dict__['profile'] = profile


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


sys.modules['fastapi'] = WhateverModule('fastapi')

if True:
    import nicegui

profile.print_stats()
