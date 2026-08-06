from __future__ import annotations

import asyncio
import atexit
import importlib
import os
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

from .logging import log

if TYPE_CHECKING:
    from socketio import AsyncServer

    from .air import Air
    from .app import App
    from .client import Client

app: App
sio: AsyncServer
loop: asyncio.AbstractEventLoop | None = None
air: Air | None = None
root: Callable | None = None
script_mode: bool = False
script_client: Client | None = None


def __getattr__(name: str) -> object:
    if name in {'app', 'sio'}:
        # lazily build the App and AsyncServer on first access by importing the nicegui module which assigns them
        module = importlib.import_module('.nicegui', package='nicegui')
        if name in globals():
            return globals()[name]
        # a genuine circular import raises AttributeError with Python's standard "partially initialized" hint
        return getattr(module, name)
    raise AttributeError(f"module 'nicegui.core' has no attribute {name!r}")


def is_loop_running() -> bool:
    """Return whether the NiceGUI event loop is running and tasks can be scheduled."""
    return loop is not None and loop.is_running()


def is_script_mode_preflight() -> bool:
    """Return whether this is the preflight run of the script mode."""
    return script_mode and not app.is_started  # pylint: disable=undefined-variable # noqa: F821


def is_script_mode_re_execution() -> bool:
    """Return whether the script is being re-executed for a per-client connection in script mode."""
    return script_mode and app.is_started  # pylint: disable=undefined-variable # noqa: F821


def stop_and_exit() -> None:
    """Run the app's ``on_shutdown`` callbacks and ``atexit`` handlers, then hard-exit.

    Skips uvicorn's connection drain, which runs before lifespan shutdown and can hang forever on a ghost Windows
    connection (#5443). ``os._exit`` skips normal interpreter teardown, so ``atexit`` handlers are run explicitly first.
    Code after ``ui.run()`` (e.g. a trailing ``finally``) still does not run — a documented limitation.
    """
    from . import run  # pylint: disable=import-outside-toplevel,cyclic-import
    if loop is not None and loop.is_running() and not app.is_stopped:  # pylint: disable=undefined-variable # noqa: F821
        try:
            future = asyncio.run_coroutine_threadsafe(app.stop(), loop)  # pylint: disable=undefined-variable # noqa: F821
            future.result(timeout=30)
        except Exception:
            log.exception('Error or timeout awaiting graceful shutdown before hard exit')
    run.tear_down()  # kill the process/thread pools before atexit, so multiprocessing's atexit join can't block
    atexit._run_exitfuncs()  # pylint: disable=protected-access
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)


def reset() -> None:
    """Reset core variables. (Useful for testing.)"""
    global loop, air, root, script_mode, script_client  # pylint: disable=global-statement # noqa: PLW0603
    loop = None
    air = None
    root = None
    script_mode = False
    script_client = None
