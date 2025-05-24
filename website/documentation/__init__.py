import asyncio

from fastapi import Request, Response

from nicegui import Client, app, ui
from nicegui.logging import log
from nicegui.page import page
from nicegui.storage import RequestTrackingMiddleware

from .content import overview, redirects, registry
from .custom_restructured_text import CustomRestructuredText
from .intro import create_intro
from .rendering import render_page
from .search import build_search_index
from .tree import build_tree
from .windows import bash_window, browser_window, python_window


async def preload_pages() -> None:
    """Execute demo functions once to register all page routes."""
    async def call_next(_):
        return Response(status_code=200)

    request = Request(scope={'type': 'http', 'method': 'GET', 'path': '/', 'session': {}})
    await RequestTrackingMiddleware(app).dispatch(request, call_next)
    with Client(page(''), request=request) as client:
        client.tab_id = '1'
        await app.storage._create_tab_storage(client.tab_id)  # pylint: disable=protected-access
        for documentation in registry.values():
            for part in documentation.parts:
                if part.demo is not None:
                    with ui.element() as container:
                        try:
                            result = part.demo.function()
                            if asyncio.iscoroutine(result):
                                # NOTE: we are not using helpers.wait_for because it messes up the context and does not need to be cancelled
                                await asyncio.wait_for(result, timeout=1)
                        except TimeoutError:
                            pass
                        except Exception:
                            log.exception('Error in demo function %s in "%s"', part.demo.function.__name__, part.title)
                    container.delete()

__all__ = [
    'CustomRestructuredText',
    'bash_window',
    'browser_window',
    'build_search_index',
    'build_tree',
    'create_intro',
    'overview',  # ensure documentation tree is built
    'preload_pages',
    'python_window',
    'redirects',
    'registry',
    'render_page',
]
