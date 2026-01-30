import asyncio
import inspect
import re
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse

from starlette.datastructures import QueryParams
from typing_extensions import Self

from .. import background_tasks, json
from ..context import context
from ..element import Element
from ..elements.label import Label
from ..functions.javascript import run_javascript
from ..logging import log
from ..page_arguments import PageArguments, RouteMatch


class SubPages(Element, component='sub_pages.js', default_classes='nicegui-sub-pages'):

    def __init__(self,
                 routes: dict[str, Callable] | None = None,
                 *,
                 root_path: str | None = None,
                 data: dict[str, Any] | None = None,
                 show_404: bool = True,
                 ) -> None:
        """Create a container for client-side routing within a page.

        Provides URL-based navigation between different views to build single page applications (SPAs).
        Routes are defined as path patterns mapping to page builder functions.
        Path parameters like "/user/{id}" are extracted and passed to the builder function.

        *Added in version 2.22.0*

        :param routes: dictionary mapping path patterns to page builder functions
        :param root_path: path prefix to strip from incoming paths (ignored by nested ``ui.sub_pages`` elements)
        :param data: arbitrary data passed to all page builder functions
        :param show_404: whether to show a 404 error message if the full path could not be consumed
            (can be useful for dynamically created nested sub pages) (default: ``True``)
        """
        super().__init__()
        self._router = context.client.sub_pages_router
        self._routes = routes or {}
        parent_sub_pages_element = next((el for el in self.ancestors() if isinstance(el, SubPages)), None)
        self._rendered_path = ''
        self._root_path = parent_sub_pages_element._rendered_path if parent_sub_pages_element else root_path
        self._data = data or {}
        self._match: RouteMatch | None = None
        self._active_tasks: set[asyncio.Task] = set()
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

    def refresh(self) -> None:
        """Rebuild this sub pages element.

        *Added in version 3.1.0*
        """
        self._reset_match()
        self._show()

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
            with self.clear():
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
            self.client.handle_exception(e)
            return True

        self._handle_scrolling(match, behavior='instant')
        if asyncio.iscoroutine(result):
            async def background_task():
                with self:
                    try:
                        await result
                    except Exception as e:
                        self.client.handle_exception(e)
                        raise

            task = background_tasks.create(background_task(), name=f'building sub_page {match.pattern}')
            self._active_tasks.add(task)

            def _close_if_canceled(t: asyncio.Task) -> None:
                if t.cancelled():
                    result.close()
                self._active_tasks.discard(t)

            task.add_done_callback(_close_if_canceled)
        return True

    def _render_404(self) -> None:
        """Display a 404 error message for unmatched routes."""
        Label(f'404: sub page {self._router.current_path} not found')

    def _render_error(self, _: Exception) -> None:  # NOTE: exception is exposed for debugging scenarios via inheritance
        msg = f'sub page {self._router.current_path} produced an error'
        Label(f'500: {msg}')
        log.error(msg, exc_info=True)

    def _set_match(self, match: RouteMatch | None) -> None:
        self._match = match
        self.has_404 = match is None
        if self.has_404 and self._404_enabled:
            with self.clear():
                self._render_404()

    def _reset_match(self) -> None:
        self._match = None

    def _find_matching_path(self) -> RouteMatch | None:
        match: RouteMatch | None = None
        relative_path = self._router.current_path[len(self._root_path or ''):]
        if not relative_path.startswith('/'):
            relative_path = '/' + relative_path
        segments = relative_path.split('/')
        query_params: QueryParams | None = None
        while segments:
            path = '/'.join(segments)
            if not path:
                path = '/'
            match, query_params = self._match_route(path, query_params)
            if match is not None:
                match.remaining_path = urlparse(relative_path).path.rstrip('/')[len(match.path):]
                break
            segments.pop()
        return match

    def _match_route(self, path: str, query_params: QueryParams | None) -> tuple[RouteMatch | None, QueryParams | None]:
        parsed_url = urlparse(path)
        path_only = parsed_url.path.rstrip('/')
        query_params = query_params or QueryParams(parsed_url.query)
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
                ), query_params
        return None, query_params

    @staticmethod
    def _match_path(pattern: str, path: str) -> dict[str, str] | None:
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
                const frag = {json.dumps(fragment)};
                const el = document.getElementById(frag) || document.querySelector("a[name=" + JSON.stringify(frag) + "]");
                el?.scrollIntoView({{ behavior: "{behavior}" }});
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
