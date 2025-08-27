import runpy
import sys
from multiprocessing import current_process

from . import core
from .page import page
from .ui_run import run


def run_nicegui_script() -> None:
    """Run a NiceGUI script."""
    if core.script_mode:
        return  # already triggered once; avoid multiple calls

    @page('/')
    def root():
        runpy.run_path(sys.argv[0])

    run(root)

    core.script_mode = True

    if current_process().name == 'MainProcess':
        sys.exit(0)  # stop further execution after the first element in the launcher
