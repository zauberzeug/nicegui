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
            if request.url.fragment:
                path += '#' + request.url.fragment
            self.current_path = path
        else:
            self.current_path = '/'

        self._path_changed_handlers: List[Callable[[str], None]] = []

    def on_path_changed(self, handler: Callable[[str], None]) -> None:
        """Register a callback to be invoked when the path changes.

        **This is an experimental feature, and the API is subject to change.**

        :param handler: callback function that receives the new path as its argument
        """
        self._path_changed_handlers.append(handler)

    def _handle_open(self, path: str) -> bool:
        self.current_path = path
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
        if self._handle_open(path):
            client.run_javascript(f'''
                const fullPath = (window.path_prefix || '') + "{self.current_path}";
                if (window.location.pathname + window.location.search + window.location.hash !== fullPath) {{
                    history.pushState({{page: "{self.current_path}"}}, "", fullPath);
                }}
            ''')
        elif self._is_valid_fastapi_route(path, client):
            client.open(path, new_tab=False)

    def _is_valid_fastapi_route(self, path: str, client: Client) -> bool:
        for route in client.page.api_router.routes:
            if isinstance(route, Route):
                match, _ = route.matches({'type': 'http', 'path': path, 'method': 'GET'})
                if match == Match.FULL:
                    return True
        return False
