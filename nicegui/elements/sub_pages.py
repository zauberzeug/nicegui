from __future__ import annotations

import asyncio
import re
from typing import Any, Callable, Dict, Optional, Set, cast
from urllib.parse import urlparse

from starlette.datastructures import QueryParams
from typing_extensions import Self

from .. import background_tasks
from ..binding import BindableProperty, bind, bind_from, bind_to
from ..context import context
from ..element import Element
from ..elements.label import Label
from ..functions.javascript import run_javascript
from ..page_args import PageArgs, RouteMatch


class SubPages(Element, component='sub_pages.js', default_classes='nicegui-sub-pages'):
    path = BindableProperty(
        on_change=lambda sender, path: cast(SubPages, sender)._handle_path_change(path))  # pylint: disable=protected-access

    def __init__(self, routes: Optional[Dict[str, Callable]] = None, *, root_path: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> None:
        """Sub Pages

        Create a sub pages element to handle client-side routing within a page.

        :param routes: dictionary mapping sub-page paths to page builder functions
        :param root_path: optional root path to strip from incoming paths (useful for non-root page mounts)
        :param data: optional dictionary with arbitrary data to be passed to sub-page functions
        """
        super().__init__()
        self._routes = routes or {}
        parent_sub_pages_element = next((el for el in self.ancestors() if isinstance(el, SubPages)), None)
        self._root_path = parent_sub_pages_element.full_path \
            if parent_sub_pages_element else root_path
        self._data = data or {}
        self.path = '---'
        self._active_tasks: Set[asyncio.Task] = set()
        self._send_update_on_path_change = True
        self.show(context.client.sub_pages_router.get_path_for(self))

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route to the sub pages.

        :param path: the path pattern to match (can include {param} placeholders)
        :param page: the callable to execute when the path is matched
            ({param} placeholders will be passed to the function parameters with same name)
        :return: self for method chaining
        """
        self._routes[path] = page
        self.show(context.client.sub_pages_router.get_path_for(self))
        return self

    def show(self, full_path: str) -> Optional[RouteMatch]:
        """Show the page for the given path.

        :param full_path: the path to navigate to (can be empty string for root path; trailing slash is ignored)
        :return: the RouteMatch object if a route was found and shown, None otherwise
        """
        if full_path == 'error':
            with self:
                Label(f'404: sub page {full_path} not found')
            return None
        if full_path == self.path:
            return None
        self._cancel_active_tasks()
        self.clear()
        match_result = self._match_route(full_path)
        if match_result is None:
            return None
        self._send_update_on_path_change = False
        self.path = match_result.path
        self._send_update_on_path_change = True

        with self:
            self._place_content(match_result)

        if match_result.fragment:
            run_javascript(f'''
                setTimeout(() => {{
                    let target = document.getElementById("{match_result.fragment}");
                    if (target)
                        target.scrollIntoView({{ behavior: "smooth" }});
                    else
                        if (target = document.querySelector('a[name="{match_result.fragment}"]'))
                            target.scrollIntoView({{ behavior: "smooth" }});
                }}, 100);
            ''')

        return match_result

    @property
    def full_path(self) -> str:
        """Get the full path of this SubPages element."""
        return f'{self._root_path or ""}{self.path}'

    def _cancel_active_tasks(self) -> None:
        """Cancel all active async tasks for this SubPages instance."""
        for task in self._active_tasks:
            if not task.done() and not task.cancelled():
                task.cancel()
        self._active_tasks.clear()

    def _match_route(self, full_path: str) -> Optional[RouteMatch]:
        """Find exact matching route for a full path.

        :return: RouteMatch object if found, None otherwise
        """
        parsed_url = urlparse(full_path)
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

    def _normalize_path(self, path: str) -> str:
        """Normalize the path by trimming root path and handling trailing slashes."""
        if self._root_path and path.startswith(self._root_path):
            path = path[len(self._root_path):]

        if path.endswith('/') and path != '/':
            path = path[:-1]
        if path == '':
            path = '/'

        return path

    @staticmethod
    def _match_path(pattern: str, path: str) -> Optional[Dict[str, str]]:
        """Match a path pattern against an actual path and extract parameters noted with {param} placeholders.

        :return: empty dict for exact matches, parameter dict for parameterized matches, None for no match.
        """
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

        if asyncio.iscoroutine(result):
            async def background_task():
                with self:
                    await result
            task = background_tasks.create(background_task(), name=f'building sub_page {route_match.pattern}')
            self._active_tasks.add(task)
            task.add_done_callback(self._active_tasks.discard)

    @staticmethod
    def find_child(element: Element) -> Optional[SubPages]:
        """Find child ``ui.sub_pages`` element, ensuring only one exists per level.

        :return: the ``ui.sub_pages`` element if found, ``None`` otherwise
        """
        return next((el for el in element.descendants() if isinstance(el, SubPages)), None)

    def bind_path_to(self,
                     target_object: Any,
                     target_name: str = 'path',
                     forward: Callable[..., Any] = lambda x: x,
                     ) -> Self:
        """Bind the path of this element to the target object's target_name property.

        The binding works one way only, from this element to the target.
        The update happens immediately and whenever the path changes.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the path before applying it to the target.
        """
        bind_to(self, 'path', target_object, target_name, forward)
        return self

    def bind_path_from(self,
                       target_object: Any,
                       target_name: str = 'path',
                       backward: Callable[..., Any] = lambda x: x,
                       ) -> Self:
        """Bind the path of this element from the target object's target_name property.

        The binding works one way only, from the target to this element.
        The update happens immediately and whenever the path changes.

        :param target_object: The object to bind from.
        :param target_name: The name of the property to bind from.
        :param backward: A function to apply to the path before applying it to this element.
        """
        bind_from(self, 'path', target_object, target_name, backward)
        return self

    def bind_path(self,
                  target_object: Any,
                  target_name: str = 'path', *,
                  forward: Callable[..., Any] = lambda x: x,
                  backward: Callable[..., Any] = lambda x: x,
                  ) -> Self:
        """Bind the path of this element to the target object's target_name property.

        The binding works both ways, from this element to the target and from the target to this element.
        The update happens immediately and whenever the path changes.
        The backward binding takes precedence for the initial synchronization.

        :param target_object: The object to bind to.
        :param target_name: The name of the property to bind to.
        :param forward: A function to apply to the path before applying it to the target.
        :param backward: A function to apply to the path before applying it to this element.
        """
        bind(self, 'path', target_object, target_name, forward=forward, backward=backward)
        return self

    def set_path(self, path: str) -> None:
        """Set the path of this element.

        :param path: The new path.
        """
        self.path = path

    def _handle_path_change(self, path: str) -> None:
        pass
        # raise NotImplementedError('SubPages.set_path is not implemented')
