from __future__ import annotations

from typing import TYPE_CHECKING, Callable, List, Optional

from fastapi import Request
from starlette.routing import Match, Route

from . import core
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
        if (
            self._handle_open(path) or  # path is handled by `ui.sub_pages`
            not self._other_page_builder_matches_path(path, client)  # `ui.sub_pages` is still responsible
        ):
            client.run_javascript(f'''
                const fullPath = (window.path_prefix || '') + "{self.current_path}";
                if (window.location.pathname + window.location.search + window.location.hash !== fullPath) {{
                    history.pushState({{page: "{self.current_path}"}}, "", fullPath);
                }}
            ''')
        else:
            client.open(path, new_tab=False)

    def _other_page_builder_matches_path(self, path: str, client: Client) -> bool:
        """Check if there is any other matching page builder than the one for this client."""
        if client.request is None:
            return True  # NOTE: we will remove this in NiceGUI 3.0 where we plan to drop support for auto-index pages

        client_route = client.request.scope['route']
        client_func = getattr(client_route.endpoint, '__func__', client_route.endpoint)

        other_routes = [route for route in core.app.routes if isinstance(route, Route)]
        for other_route in other_routes:
            other_func = getattr(other_route.endpoint, '__func__', other_route.endpoint)
            if (
                getattr(client_func, '__name__', None) == getattr(other_func, '__name__', None) and
                getattr(client_func, '__module__', None) == getattr(other_func, '__module__', None) and
                getattr(client_func, '__qualname__', None) == getattr(other_func, '__qualname__', None)
            ):
                continue  # client route and other route point to the same page builder, so they don't count

            match, _ = other_route.matches({'type': 'http', 'path': path, 'method': 'GET'})
            if match == Match.FULL:
                return True

        return False
