from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import TYPE_CHECKING

from fastapi import Request
from starlette.routing import Match, Route

from . import core, json
from .context import context
from .elements.sub_pages import SubPages
from .functions.on import on

if TYPE_CHECKING:
    from .client import Client


class SubPagesRouter:

    def __init__(self, request: Request | None) -> None:
        on('sub_pages_open', lambda event: self._handle_open(event.args))
        on('sub_pages_navigate', lambda event: self._handle_navigate(event.args))

        if request is not None:
            forwarded_prefix = request.headers.get('X-Forwarded-Prefix', '')
            root = _normalize(request.scope.get('root_path', ''))
            combined = _normalize(forwarded_prefix or '') + _normalize(root or '')
            path = request.url.path
            for p in (combined, root):
                if p and (path == p or path.startswith(p + '/')):
                    path = path[len(p):] or '/'
                    break
            if request.url.query:
                path += '?' + request.url.query
            # NOTE: we do not use request.url.fragment because browsers do not send it to the server
            self.current_path = path
        else:
            self.current_path = '/'
        self.is_initial_request = True

        self._path_changed_handlers: list[Callable[[str], None]] = []

    def on_path_changed(self, handler: Callable[[str], None]) -> None:
        """Register a callback to be invoked when the path changes.

        :param handler: callback function that receives the new path as its argument
        """
        self._path_changed_handlers.append(handler)

    async def refresh(self) -> None:
        """Refresh the currently shown sub pages.

        This will clear and rebuild the current sub page as if navigating to it again.
        Useful when you want to update the page content based on changes in data or state.

        *Added in version 3.1.0*
        """
        for el in context.client.layout.descendants():
            if isinstance(el, SubPages):
                el._reset_match()  # pylint: disable=protected-access
        await self._handle_open(self.current_path)

    async def _handle_open(self, path: str) -> bool:
        self.current_path = path
        self.is_initial_request = False
        for callback in self._path_changed_handlers:
            callback(path)
        for child in context.client.layout.descendants():
            if isinstance(child, SubPages):
                child._show()  # pylint: disable=protected-access
        return await self._can_resolve_full_path(context.client)

    async def _handle_navigate(self, path: str) -> None:
        # NOTE: keep a reference to the client because _handle_open clears the slots so that context.client does not work anymore
        client = context.client
        await self._handle_open(path)
        if (
            not has_any_unresolved_path(client) or  # path is handled by `ui.sub_pages`
            not self._other_page_builder_matches_path(path, client)  # `ui.sub_pages` is still responsible
        ):
            current_path_string = json.dumps(self.current_path)
            client.run_javascript(f'''
                const fullPath = (window.path_prefix || '') + {current_path_string};
                if (window.location.pathname + window.location.search + window.location.hash !== fullPath) {{
                    history.pushState({{page: {current_path_string}}}, "", fullPath);
                }}
            ''')
        else:
            client.open(path, new_tab=False)

    def _other_page_builder_matches_path(self, path: str, client: Client) -> bool:
        """Check if there is any other matching page builder than the one for this client."""
        client_route = client.request.scope.get('route')
        if client_route is None:
            return False  # NOTE: requests handled by 404 handler (e.g., root pages) have no route key
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

    @staticmethod
    async def _can_resolve_full_path(client: Client) -> bool:
        sub_pages_elements = [el for el in client.layout.descendants() if isinstance(el, SubPages)]
        if any(el._active_tasks for el in sub_pages_elements):  # pylint: disable=protected-access
            await asyncio.sleep(0)
            # NOTE: refresh the list to include newly created nested sub pages in async sub page builders after the event loop tick
            sub_pages_elements = [el for el in client.layout.descendants() if isinstance(el, SubPages)]
        for sub_pages in sub_pages_elements:
            if (
                sub_pages._match is not None and  # pylint: disable=protected-access
                sub_pages._match.remaining_path and  # pylint: disable=protected-access
                not any(isinstance(el, SubPages) for el in sub_pages.descendants())
            ):
                sub_pages._set_match(None)  # pylint: disable=protected-access
        return not has_any_unresolved_path(client, with_404_enabled_only=True)


def has_any_unresolved_path(client: Client, *, with_404_enabled_only: bool = False) -> bool:
    """Check if any sub_pages has an unresolved path.

    :param with_404_enabled_only: whether to only consider sub_pages with show_404 enabled
    """
    return any(
        sub_pages.has_404 and (sub_pages._404_enabled or not with_404_enabled_only)  # pylint: disable=protected-access
        for sub_pages in client.layout.descendants()
        if isinstance(sub_pages, SubPages)
    )


def _normalize(p: str) -> str:
    return p[:-1] if p and p != '/' and p.endswith('/') else p
