from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List, Optional

from fastapi import Request
from starlette.routing import Match, Route

from .context import context
from .elements.sub_pages import SubPages
from .functions.on import on

if TYPE_CHECKING:
    from .client import Client


class SubPagesRouter:

    def __init__(self, request: Optional[Request]) -> None:
        on('sub_pages_open', lambda event: self._handle_open(event.args))
        on('sub_pages_navigate', lambda event: self._handle_navigate(event.args))

        if request is not None:
            path = request.url.path
            if request.url.query:
                path += '?' + request.url.query
            # NOTE: we do not use request.url.fragment because browsers do not send it to the server
            self.current_path = path
        else:
            self.current_path = '/'
        self.is_initial_request = True

        self._path_changed_handlers: List[Callable[[str], None]] = []

    def on_path_changed(self, handler: Callable[[str], None]) -> None:
        """Register a callback to be invoked when the path changes.

        **This is an experimental feature, and the API is subject to change.**

        :param handler: callback function that receives the new path as its argument
        """
        self._path_changed_handlers.append(handler)

    def _handle_open(self, path: str) -> bool:
        self.current_path = path
        self.is_initial_request = False
        for callback in self._path_changed_handlers:
            callback(path)
        updated = False
        for child in context.client.layout.descendants():
            if isinstance(child, SubPages):
                try:
                    if child.show() is not None:
                        updated = True
                except ValueError:
                    pass
        return updated

    def _handle_navigate(self, path: str) -> None:
        # NOTE: keep a reference to the client because _handle_open clears the slots so that context.client does not work anymore
        client = context.client
        self._handle_open(path)

        if self._is_other_fastapi_page(path, client):
            client.open(path, new_tab=False)
        else:
            client.run_javascript(f'''
                const fullPath = (window.path_prefix || '') + "{self.current_path}";
                if (window.location.pathname + window.location.search + window.location.hash !== fullPath) {{
                    history.pushState({{page: "{self.current_path}"}}, "", fullPath);
                }}
            ''')

    def _is_other_fastapi_page(self, path: str, client: Client) -> bool:
        assert client.request is not None
        current_route = client.request.scope['route']
        for route in client.page.api_router.routes:
            if isinstance(route, Route):
                match, _ = route.matches({'type': 'http', 'path': path, 'method': 'GET'})
                if match == Match.FULL:
                    current_func = getattr(current_route.endpoint, '__func__', current_route.endpoint)
                    route_func = getattr(route.endpoint, '__func__', route.endpoint)
                    # NOTE: we must check if they're the same function by comparing name and module, because multiple routes can point to the same page builder
                    if not (getattr(current_func, '__name__', None) == getattr(route_func, '__name__', None) and
                            getattr(current_func, '__module__', None) == getattr(route_func, '__module__', None)):
                        return True
        return False
