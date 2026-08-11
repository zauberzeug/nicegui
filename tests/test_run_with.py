import weakref

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from nicegui import app, ui


def test_run_with_rejects_self_mount():
    """Passing nicegui.app to ui.run_with() would mount it into itself and cause infinite recursion on unmatched paths."""
    with pytest.raises(ValueError, match='must be called with your own FastAPI app'):
        ui.run_with(app)


async def test_run_with_tolerates_dangling_weakref_proxy(nicegui_reset_globals):
    """A dangling weakref.proxy in gc.get_objects() must not crash ui.run_with() startup."""
    _ = weakref.proxy(set())  # referent is unreferenced, proxy is dangling immediately
    fastapi_app = FastAPI()
    ui.run_with(fastapi_app)
    async with fastapi_app.router.lifespan_context(fastapi_app):
        pass


def test_run_with_unknown_path_falls_through_to_root(nicegui_reset_globals):
    """SPA-style subpaths (handled client-side by ui.sub_pages) must render the root page, not JSON 404."""
    fastapi_app = FastAPI()

    def root() -> None:
        ui.sub_pages({'/auth/login': lambda: ui.label('login')})

    ui.run_with(fastapi_app, root=root)
    with TestClient(fastapi_app) as client:
        response = client.get('/auth/login')
    assert response.headers['content-type'].startswith('text/html'), \
        'unmatched path under ui.run_with(root=...) should render the root HTML page, not JSON'


def test_run_with_api_endpoint_404_still_returns_json(nicegui_reset_globals):
    """An @app.get endpoint raising 404 must still get FastAPI's JSON response, even when mounted via ui.run_with()."""
    fastapi_app = FastAPI()

    @app.get('/api/missing')
    def api_missing():
        raise HTTPException(404, 'item not found')

    ui.run_with(fastapi_app)
    with TestClient(fastapi_app) as client:
        response = client.get('/api/missing')
    assert response.status_code == 404
    assert response.headers['content-type'].startswith('application/json'), \
        'API endpoints raising HTTPException(404) should keep getting JSON'
    assert response.json() == {'detail': 'item not found'}
