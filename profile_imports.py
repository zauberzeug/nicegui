# NOTE: run this file like this:
#
# kernprof -l -v profile_imports.py

import os
import sys

from line_profiler import LineProfiler

os.environ['MATPLOTLIB'] = 'false'

profile = LineProfiler()
sys.modules['__main__'].__dict__['profile'] = profile

if True:
    from nicegui import ui

profile.print_stats()
