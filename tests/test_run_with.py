import gc
import weakref

import pytest
from fastapi import FastAPI

from nicegui import app, ui


def test_run_with_rejects_self_mount():
    """Passing nicegui.app to ui.run_with() would mount it into itself and cause infinite recursion on unmatched paths."""
    with pytest.raises(ValueError, match='must be called with your own FastAPI app'):
        ui.run_with(app)


class _Weak:
    pass


@pytest.mark.asyncio
async def test_get_server_instance_handles_dead_weakref():
    """Iterating gc.get_objects() with isinstance() should handle dead weakref proxies."""
    original = gc.get_objects

    def patched():
        obj = _Weak()
        proxy = weakref.proxy(obj)
        del obj
        return [proxy, *original()]

    gc.get_objects = patched
    fastapi_app = FastAPI()
    ui.run_with(app=fastapi_app)

    # should not fail
    async with fastapi_app.router.lifespan_context(fastapi_app) as _ct:
        pass
