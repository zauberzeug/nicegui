from __future__ import annotations

import asyncio
import inspect
import re
from typing import Any, Callable, Dict, Optional, Set
from urllib.parse import urlparse

from starlette.datastructures import QueryParams
from typing_extensions import Self

from .. import background_tasks
from ..context import context
from ..element import Element
from ..elements.label import Label
from ..functions.javascript import run_javascript
from ..logging import log
from ..page_args import PageArgs, RouteMatch


class SubPages(Element, component='sub_pages.js', default_classes='nicegui-sub-pages'):
    def __init__(
        self,
            routes: Optional[Dict[str, Callable]] = None,
            *,
            root_path: Optional[str] = None,
            data: Optional[Dict[str, Any]] = None,
            show_404: bool = True,
    ) -> None:
        """Create a container for client-side routing within a page.

        Provides URL-based navigation between different views to build single page applications (SPAs).
        Routes are defined as path patterns mapping to page builder functions.
        Path parameters like '/user/{id}' are extracted and passed to the builder function.

        **This is an experimental feature, and the API is subject to change.**

        :param routes: dictionary mapping path patterns to page builder functions
        :param root_path: path prefix to strip from incoming paths (for non-root page mounts)
        :param data: arbitrary data passed to all page builder functions
        :param show_404: whether to show a 404 error message if the full path could not be consumed; this can be useful for dynamically created nested sub pages
        """
        super().__init__()
        assert not context.client.shared, (
            'ui.sub_pages cannot be used with auto-index client or other shared clients. '
            'Please use a function with ui.page decorator instead. See https://nicegui.io/documentation/sub_pages'
        )
        self._router = context.client.sub_pages_router
        self._routes = routes or {}
        parent_sub_pages_element = next((el for el in self.ancestors() if isinstance(el, SubPages)), None)
        self._root_path = parent_sub_pages_element._full_path if parent_sub_pages_element else root_path
        self._data = data or {}
        self._active_tasks: Set[asyncio.Task] = set()
        self._send_update_on_path_change = True
        self._current_match: Optional[RouteMatch] = None
        self._should_show_404 = show_404
        self.show()

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route.

        :param path: path pattern to match (e.g., '/user/{id}' for parameterized routes)
        :param page: function to call when this path is accessed
        :return: self for method chaining
        """
        self._routes[path] = page
        self.show()
        return self

    def show(self) -> Optional[RouteMatch]:
        """Display the page matching the current URL path.

        :return: RouteMatch if a matching route was found and displayed, None for 404
        """
        match_result = self._find_matching_path()

        # NOTE: if path/query params are the same, only update fragment without re-rendering
        if (match_result is not None and
            self._current_match is not None and
            match_result.path == self._current_match.path and
                not self._required_query_params_changed(match_result)):

            # NOTE: if the full path could not be consumed, the last sub pages element must handle a possible 404
            if not any(el for el in self.descendants() if isinstance(el, SubPages)) and match_result.remaining_path:
                if self._should_show_404:
                    self.clear()
                    with self:
                        self._show_404()
                return None
            self._scroll_to_fragment(match_result.fragment)
            return match_result
        self._cancel_active_tasks()
        self.clear()
        with self:
            if match_result is None:
                if self._should_show_404:
                    self._show_404()
                return None
            self._send_update_on_path_change = False
            self._current_match = match_result
            self._send_update_on_path_change = True
            if not self._show_page(match_result):
                return None
        return match_result

    def _show_page(self, match: RouteMatch) -> bool:
        kwargs = PageArgs.build_kwargs(match, self, self._data)
        try:
            result = match.builder(**kwargs)
        except Exception as e:
            self.clear()  # NOTE: clear partial content created before the exception
            self._show_error(e)
            return True
        # NOTE: if the full path could not be consumed, the deepest sub pages element must handle the possible 404
        has_children = any(el for el in self.descendants() if isinstance(el, SubPages))
        if match.remaining_path and not has_children:
            if self._should_show_404:
                self.clear()
                self._show_404()
            if asyncio.iscoroutine(result):
                result.close()
            return False

        self._scroll_to_fragment(match.fragment)
        if asyncio.iscoroutine(result):
            async def background_task():
                with self:
                    await result
            task = background_tasks.create(background_task(), name=f'building sub_page {match.pattern}')
            self._active_tasks.add(task)
            task.add_done_callback(self._active_tasks.discard)
        return True

    def _show_404(self) -> None:
        """Display a 404 error message for unmatched routes."""
        Label(f'404: sub page {self._router.current_path} not found')

    def _show_error(self, _: Exception) -> None:  # NOTE: exception is exposed for debugging scenarios via inheritance
        msg = f'sub page {self._router.current_path} produced an error'
        Label(f'500: {msg}')
        log.error(msg, exc_info=True)

    @property
    def _full_path(self) -> str:
        return f'{self._root_path or ""}{self._current_match.path if self._current_match else ""}'

    def _find_matching_path(self) -> Optional[RouteMatch]:
        match: Optional[RouteMatch] = None
        relative_path = self._router.current_path[len(self._root_path or ''):]
        if not relative_path.startswith('/'):
            relative_path = '/' + relative_path
        segments = relative_path.split('/')
        while segments:
            path = '/'.join(segments)
            if not path:
                path = '/'
            match = self._match_route(path)
            if match is not None:
                match.remaining_path = urlparse(relative_path).path.rstrip('/')[len(match.path):]
                break
            segments.pop()
        return match

    def _match_route(self, path: str) -> Optional[RouteMatch]:
        parsed_url = urlparse(path)
        path_only = parsed_url.path.rstrip('/')
        query_params = QueryParams(parsed_url.query) if parsed_url.query else QueryParams()
        fragment = parsed_url.fragment
        if not path_only.startswith('/'):
            path_only = '/' + path_only

        for route, builder in self._routes.items():
            parameters = self._match_path(route, path_only)
            if parameters is not None:
                return RouteMatch(
                    path=path_only,
                    pattern=route,
                    builder=builder,
                    parameters=parameters,
                    query_params=query_params,
                    fragment=fragment,
                )
        return None

    @staticmethod
    def _match_path(pattern: str, path: str) -> Optional[Dict[str, str]]:
        if '{' not in pattern:
            return {} if pattern == path else None

        regex_pattern = re.escape(pattern)
        for match in re.finditer(r'\\{(\w+)\\}', regex_pattern):
            param_name = match.group(1)
            regex_pattern = regex_pattern.replace(f'\\{{{param_name}\\}}', f'(?P<{param_name}>[^/]+)')

        regex_match = re.match(f'^{regex_pattern}$', path)
        return regex_match.groupdict() if regex_match else None

    def _cancel_active_tasks(self) -> None:
        for task in self._active_tasks:
            if not task.done() and not task.cancelled():
                task.cancel()
        self._active_tasks.clear()

    def _scroll_to_fragment(self, fragment: str) -> None:
        if fragment:
            run_javascript(f'''
                const scrollToFragment = () => {{
                    let target = document.getElementById("{fragment}");
                    if (!target) {{
                        target = document.querySelector('a[name="{fragment}"]');
                    }}
                    if (target) {{
                        target.scrollIntoView({{ behavior: "smooth" }});
                    }} else {{
                        requestAnimationFrame(scrollToFragment);
                    }}
                }};
                requestAnimationFrame(scrollToFragment);
            ''')

    def _required_query_params_changed(self, route_match: RouteMatch) -> bool:
        if not route_match.query_params:
            return False
        parameters = inspect.signature(route_match.builder).parameters
        for name, param in parameters.items():
            if param.annotation is PageArgs:
                return True
            if name in route_match.query_params:
                return True
        return False
