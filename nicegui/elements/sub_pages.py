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
from ..page_arguments import PageArguments, RouteMatch


class SubPages(Element, component='sub_pages.js', default_classes='nicegui-sub-pages'):

    def __init__(self,
                 routes: Optional[Dict[str, Callable]] = None,
                 *,
                 root_path: Optional[str] = None,
                 data: Optional[Dict[str, Any]] = None,
                 show_404: bool = True,
                 ) -> None:
        """Create a container for client-side routing within a page.

        Provides URL-based navigation between different views to build single page applications (SPAs).
        Routes are defined as path patterns mapping to page builder functions.
        Path parameters like "/user/{id}" are extracted and passed to the builder function.

        **This is an experimental feature, and the API is subject to change.**

        *Added in version 2.22.0*

        :param routes: dictionary mapping path patterns to page builder functions
        :param root_path: path prefix to strip from incoming paths (ignored by nested ``ui.sub_pages`` elements)
        :param data: arbitrary data passed to all page builder functions
        :param show_404: whether to show a 404 error message if the full path could not be consumed
            (can be useful for dynamically created nested sub pages) (default: ``True``)
        """
        super().__init__()
        assert not context.client.shared, (
            'ui.sub_pages cannot be used with the auto-index client or other shared clients. '
            'Please use a function with ui.page decorator instead. See https://nicegui.io/documentation/sub_pages.'
        )
        self._router = context.client.sub_pages_router
        self._routes = routes or {}
        parent_sub_pages_element = next((el for el in self.ancestors() if isinstance(el, SubPages)), None)
        self._rendered_path = ''
        self._root_path = parent_sub_pages_element._rendered_path if parent_sub_pages_element else root_path
        self._data = data or {}
        self._match: Optional[RouteMatch] = None
        self._active_tasks: Set[asyncio.Task] = set()
        self._404_enabled = show_404
        self.has_404 = False
        self._show()

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route.

        :param path: path pattern to match (e.g., "/user/{id}" for parameterized routes)
        :param page: function to call when this path is accessed
        :return: self for method chaining
        """
        self._routes[path] = page
        self._show()
        return self

    def _show(self) -> None:
        """Display the page matching the current URL path."""
        self._rendered_path = ''
        match = self._find_matching_path()
        # NOTE: if path and query params are the same, only update fragment without re-rendering
        if (
            match is not None and
            self._match is not None and
            match.path == self._match.path and
            not self._required_query_params_changed(match) and
            not (self.has_404 and self._match.remaining_path == match.remaining_path)
        ):
            # NOTE: Even though our matched path is the same, the remaining path might still require us to handle 404 (if we are the last sub pages element)
            if match.remaining_path and not any(isinstance(el, SubPages) for el in self.descendants()):
                self._set_match(None)
            else:
                self._handle_scrolling(match, behavior='smooth')
                self._set_match(match)
        else:
            self._cancel_active_tasks()
            self.clear()
            with self:
                if match is not None and self._render_page(match):
                    self._set_match(match)
                else:
                    self._set_match(None)

    def _render_page(self, match: RouteMatch) -> bool:
        kwargs = PageArguments.build_kwargs(match, self, self._data)
        self._rendered_path = f'{self._root_path or ""}{match.path}'
        try:
            result = match.builder(**kwargs)
        except Exception as e:
            self.clear()  # NOTE: clear partial content created before the exception
            self._render_error(e)
            return True

        # NOTE: if the full path could not be consumed, the deepest sub pages element must handle the possible 404
        if match.remaining_path and not any(isinstance(el, SubPages) for el in self.descendants()):
            if asyncio.iscoroutine(result):
                result.close()
            return False

        self._handle_scrolling(match, behavior='instant')
        if asyncio.iscoroutine(result):
            async def background_task():
                with self:
                    await result
            task = background_tasks.create(background_task(), name=f'building sub_page {match.pattern}')
            self._active_tasks.add(task)
            task.add_done_callback(self._active_tasks.discard)
        return True

    def _render_404(self) -> None:
        """Display a 404 error message for unmatched routes."""
        Label(f'404: sub page {self._router.current_path} not found')

    def _render_error(self, _: Exception) -> None:  # NOTE: exception is exposed for debugging scenarios via inheritance
        msg = f'sub page {self._router.current_path} produced an error'
        Label(f'500: {msg}')
        log.error(msg, exc_info=True)

    def _set_match(self, match: Optional[RouteMatch]) -> None:
        self._match = match
        if match is None:
            if self._404_enabled:
                self.has_404 = True
                self.clear()
                with self:
                    self._render_404()
        else:
            self.has_404 = False

    def _reset_match(self) -> None:
        self._match = None

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

    def _handle_scrolling(self, match: RouteMatch, *, behavior: str) -> None:
        if match.fragment:
            self._scroll_to_fragment(match.fragment, behavior=behavior)
        elif not self._router.is_initial_request:  # NOTE: the initial path has no fragment; to not interfere with later fragment scrolling, we skip scrolling to top
            self._scroll_to_top(behavior=behavior)

    def _scroll_to_fragment(self, fragment: str, *, behavior: str) -> None:
        run_javascript(f'''
            requestAnimationFrame(() => {{
                document.querySelector('#{fragment}, a[name="{fragment}"]')?.scrollIntoView({{ behavior: "{behavior}" }});
            }});
        ''')

    def _scroll_to_top(self, *, behavior: str) -> None:
        run_javascript(f'''
            requestAnimationFrame(() => {{ window.scrollTo({{top: 0, left: 0, behavior: "{behavior}"}}); }});
        ''')

    def _required_query_params_changed(self, route_match: RouteMatch) -> bool:
        if self._match is None:
            return True
        current_params = route_match.query_params
        previous_params = self._match.query_params
        for name, param in inspect.signature(route_match.builder).parameters.items():
            if param.annotation is PageArguments:
                return current_params != previous_params
            if current_params.get(name) != previous_params.get(name):
                return True
        return False
