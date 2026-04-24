import weakref

import pytest
from fastapi import FastAPI

from nicegui import app, ui


def test_run_with_rejects_self_mount():
    """Passing nicegui.app to ui.run_with() would mount it into itself and cause infinite recursion on unmatched paths."""
    with pytest.raises(ValueError, match='must be called with your own FastAPI app'):
        ui.run_with(app)


async def test_run_with_tolerates_dangling_weakref_proxy():
    """A dangling weakref.proxy in gc.get_objects() must not crash ui.run_with() startup."""
    _ = weakref.proxy(set())  # referent is unreferenced, proxy is dangling immediately
    fastapi_app = FastAPI()
    ui.run_with(fastapi_app)
    async with fastapi_app.router.lifespan_context(fastapi_app):
        pass
