from __future__ import annotations

import asyncio
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
from ..page_args import PageArgs, RouteMatch


class SubPages(Element, component='sub_pages.js', default_classes='nicegui-sub-pages'):
    def __init__(
        self,
            routes: Optional[Dict[str, Callable]] = None,
            *,
            root_path: Optional[str] = None,
            data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Sub Pages

        Create a sub pages element to handle client-side routing within a page.

        :param routes: dictionary mapping sub-page paths to page builder functions
        :param root_path: optional root path to strip from incoming paths (useful for non-root page mounts)
        :param data: optional dictionary with arbitrary data to be passed to sub-page functions
        """
        super().__init__()
        self._router = context.client.sub_pages_router
        self._routes = routes or {}
        parent_sub_pages_element = next((el for el in self.ancestors() if isinstance(el, SubPages)), None)
        self._root_path = parent_sub_pages_element.full_path if parent_sub_pages_element else root_path
        self._data = data or {}
        self._active_tasks: Set[asyncio.Task] = set()
        self._send_update_on_path_change = True
        self._path: Optional[str] = None
        self.show()

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route to the sub pages.

        :param path: the path pattern to match (can include {param} placeholders)
        :param page: the callable to execute when the path is matched
            ({param} placeholders will be passed to the function parameters with same name)
        :return: self for method chaining
        """
        self._routes[path] = page
        self.show()
        return self

    def show(self) -> Optional[RouteMatch]:
        """Show the page for the given path.

        :param full_path: the path to navigate to (can be empty string for root path; trailing slash is ignored)
                         If None, the path will be calculated automatically from the current router state
        :return: the RouteMatch object if a route was found and shown, None otherwise
        """
        match_result = self._find_matching_path()
        if match_result is not None and match_result.full_url == self._path:
            self._scroll_to_fragment(match_result.fragment)
            return match_result
        self._cancel_active_tasks()
        self.clear()
        if match_result is None:
            self.show_404()
            return None
        self._send_update_on_path_change = False
        self._path = match_result.full_url
        self._send_update_on_path_change = True

        with self:
            self._place_content(match_result)

        return match_result

    def show_404(self) -> None:
        """Show a 404 error message."""
        with self:
            Label(f'404: sub page {self._router.current_path} not found')

    @property
    def full_path(self) -> str:
        """Get the full path of this SubPages element."""
        return f'{self._root_path or ""}{self._path or ""}'

    def _find_matching_path(self) -> Optional[RouteMatch]:
        match: Optional[RouteMatch] = None
        segments = self._router.current_path.split('/')
        while segments:
            path = '/'.join(segments)
            if not path:
                break
            match = self._match_route(path[len(self._root_path or ''):])
            if match is not None:
                break
            segments.pop()

        return match

    def _cancel_active_tasks(self) -> None:
        for task in self._active_tasks:
            if not task.done() and not task.cancelled():
                task.cancel()
        self._active_tasks.clear()

    def _match_route(self, path: str) -> Optional[RouteMatch]:
        parsed_url = urlparse(path)
        path_only = parsed_url.path.rstrip('/')
        query_params = QueryParams(parsed_url.query) if parsed_url.query else QueryParams()
        fragment = parsed_url.fragment
        if path_only == '':
            path_only = '/'

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

    def _scroll_to_fragment(self, fragment: str) -> None:
        if fragment:
            run_javascript(f'''
                console.log('scrolling to fragment', "{fragment}");
                setTimeout(() => {{
                    console.log('scrolled to fragment', "{fragment}");
                    let target = document.getElementById("{fragment}");
                    if (target)
                        target.scrollIntoView({{ behavior: "smooth" }});
                    else
                        if (target = document.querySelector('a[name="{fragment}"]'))
                            target.scrollIntoView({{ behavior: "smooth" }});
                }}, 100);
            ''')

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

    @property
    def _is_root(self) -> bool:
        """Whether this is a root ``ui.sub_pages`` element."""
        for parent in self.ancestors():
            if isinstance(parent, SubPages):
                return False
        return True

    def _place_content(self, route_match: RouteMatch) -> None:
        kwargs = PageArgs.build_kwargs(route_match, self, self._data)
        result = route_match.builder(**kwargs)
        self._scroll_to_fragment(route_match.fragment)
        if asyncio.iscoroutine(result):
            async def background_task():
                with self:
                    await result
            task = background_tasks.create(background_task(), name=f'building sub_page {route_match.pattern}')
            self._active_tasks.add(task)
            task.add_done_callback(self._active_tasks.discard)
