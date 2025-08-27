import runpy
import sys

from .page import page
from .ui_run import run


def run_nicegui_script() -> None:
    """Run a NiceGUI script."""
    @page('/')
    def root():
        runpy.run_path(sys.argv[0])

    run(root, reload=False)
