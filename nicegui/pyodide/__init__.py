"""NiceGUI Pyodide runtime package.

Provides the bridge, outbox, and runtime needed to run NiceGUI
entirely in the browser via Pyodide/PyScript.
"""
from .runtime import PyodideRuntime

__all__ = ['PyodideRuntime']
