"""Code that runs in the worker processes of ``run.cpu_bound``.

This module lives outside the ``nicegui`` package on purpose:
everything a worker unpickles is imported there,
and importing any ``nicegui.*`` module would execute ``nicegui/__init__.py`` and load the whole web stack.
Keeping these helpers here lets workers start without NiceGUI if the main module guards its NiceGUI code (#5684).
Therefore this module must only import from the standard library.
"""
import traceback
from collections.abc import Callable
from typing import Any


class SubprocessException(Exception):
    """A picklable exception to represent exceptions raised in subprocesses."""

    def __init__(self, original_type, original_message, original_traceback) -> None:
        self.original_type = original_type
        self.original_message = original_message
        self.original_traceback = original_traceback
        super().__init__(f'{original_type}: {original_message}')

    def __reduce__(self):
        return (SubprocessException, (self.original_type, self.original_message, self.original_traceback))

    def __str__(self):
        return (f'Exception in subprocess:\n'
                f'  Type: {self.original_type}\n'
                f'  Message: {self.original_message}\n'
                f'  {self.original_traceback}')


def safe_callback(callback: Callable, *args, **kwargs) -> Any:
    """Run a callback; catch and wrap any exceptions that might occur."""
    try:
        return callback(*args, **kwargs)
    except Exception as e:
        # we do not want to pass the original exception because it might be unpicklable
        raise SubprocessException(type(e).__name__, str(e), traceback.format_exc()) from None
