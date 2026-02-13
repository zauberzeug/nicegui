"""Pyodide environment detection for NiceGUI."""
from __future__ import annotations

import sys


def is_pyodide() -> bool:
    """Check if running in a Pyodide (WebAssembly/Emscripten) environment."""
    return 'pyodide' in sys.modules or hasattr(sys, '_emscripten_info')


IS_PYODIDE: bool = is_pyodide()
