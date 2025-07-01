from __future__ import annotations

import asyncio
import re
from typing import Any, Callable, Dict, List, Optional, Set, cast
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
        self._root_path = parent_sub_pages_element.path if parent_sub_pages_element else root_path
        self._data = data or {}
        self.path = '/'
        self._active_tasks: Set[asyncio.Task] = set()
        self._send_update_on_path_change = True  # standard pattern like for other elements
        self._handle_routes_change()
        self.on('open', lambda e: self._show_page_and_update_browser_url(e.args))
        self.on('navigate', lambda e: self._handle_navigate(e.args))

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route to the sub pages.

        :param path: the path pattern to match (can include {param} placeholders)
        :param page: the callable to execute when the path is matched
            ({param} placeholders will be passed to the function parameters with same name)
        :return: self for method chaining
        """
        self._routes[path] = page
        self._handle_routes_change()
        return self

    def show(self, full_path: str) -> Optional[RouteMatch]:
        """Show the page for the given path.

        :param full_path: the path to navigate to (can be empty string for root path; trailing slash is ignored)
        :return: the RouteMatch object if a route was found and shown, None otherwise
        """
        self._cancel_active_tasks()
        self.clear()

        match_result = self._match_route(full_path)
        if match_result is None:
            with self:
                Label(f'404: sub page {full_path} not found')
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

    def _cancel_active_tasks(self) -> None:
        """Cancel all active async tasks for this SubPages instance."""
        for task in self._active_tasks:
            if not task.done() and not task.cancelled():
                task.cancel()
        self._active_tasks.clear()

    def _show_page_and_update_browser_url(self, path: str) -> Optional[RouteMatch]:
        """Show the page and update browser URL.

        :param path: the path to navigate to
        :return: the RouteMatch object if successful, None if no route was found
        """
        match_result = self.show(path)
        if match_result is None:
            return None

        new_path = f'{self._root_path or ""}{match_result.path}'
        run_javascript(f'''
            const fullPath = (window.path_prefix || '') + "{new_path}";
            if (window.location.pathname + window.location.search + window.location.hash !== fullPath) {{
                history.pushState({{page: "{path}"}}, "", fullPath);
            }}
        ''')
        return match_result

    def _match_route(self, full_path: str) -> Optional[RouteMatch]:
        """Find the first matching route for a full path (including query params and fragments) with segment dropping.

        :return: RouteMatch object if found, None otherwise
        """
        parsed_url = urlparse(full_path)
        path_only = parsed_url.path
        query_params = QueryParams(parsed_url.query) if parsed_url.query else QueryParams()
        fragment = parsed_url.fragment
        normalized_path = self._normalize_path(path_only)
        segments = normalized_path.split('/')
        while segments:
            sub_path = '/'.join(segments)
            for route, builder in self._routes.items():
                matches = self._match_path(route, sub_path)
                if matches is not None:
                    return RouteMatch(
                        path=sub_path,
                        pattern=route,
                        builder=builder,
                        parameters=matches,
                        query_params=query_params,
                        fragment=fragment
                    )
            segments.pop()
        return None

    def _handle_navigate(self, navigation_data) -> None:
        """Handle navigate event from link clicks."""
        old_path = navigation_data.get('from', '')
        new_path = navigation_data.get('to', navigation_data)

        if self._should_handle_navigation(old_path, new_path):
            if not self._try_navigate_to(new_path):
                context.client.open(new_path)

    def _should_handle_navigation(self, old_path: str, new_path: str) -> bool:
        """Determine if this SubPages should handle the navigation.

        Rule: Handle if the route resolution within this SubPages' own route table changes,
        OR if paths differ only by query parameters or trailing slashes.
        """
        # Check if this element can route both paths
        old_normalized = self._normalize_path(old_path)
        new_normalized = self._normalize_path(new_path)

        old_route = self._match_route(old_normalized)
        new_route = self._match_route(new_normalized)

        # Both paths must be routable by this element
        if old_route is None or new_route is None:
            return False

        # Handle if the route resolution changes within our route table
        if old_route.pattern != new_route.pattern:
            return True

        # Also handle if paths differ only by query parameters or trailing slashes
        # (these cases normalize to the same path but should still trigger navigation)
        old_base = old_path.split('?')[0].rstrip('/')
        new_base = new_path.split('?')[0].rstrip('/')

        # If base paths are the same but full paths differ, handle it
        if old_base == new_base and old_path != new_path:
            return True

        return False

    def _normalize_path(self, path: str) -> str:
        """Normalize the path by trimming root path and handling trailing slashes."""
        # For nested SubPages, dynamically get the parent's current path
        if not self._is_root:
            parent_sub_pages = next((el for el in self.ancestors() if isinstance(el, SubPages)), None)
            if parent_sub_pages is not None:
                parent_path = parent_sub_pages.path
                if parent_path != '/' and path.startswith(parent_path):
                    path = path[len(parent_path):]
        elif self._root_path is not None:
            # For root SubPages, use the static _root_path
            root = self._root_path.rstrip('/')
            if path.startswith(root):
                path = path[len(root):]

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

    def _try_navigate_to(self, path: str) -> bool:
        """Try to handle navigation through ``ui.sub_pages`` system.

        :param path: the path to navigate to
        :return: ``True`` if handled by ``ui.sub_pages``, ``False`` otherwise
        """
        return self._show_page_and_update_browser_url(path) is not None

    @staticmethod
    def try_navigate_to(path: str) -> bool:
        """Try to handle navigation through ``ui.sub_pages`` system.

        :param path: the path to navigate to
        :return: ``True`` if handled by ``ui.sub_pages``, ``False`` otherwise
        """
        handled_by_sub_pages = False
        for sub_page in SubPages.find_roots(context.client.content):
            if sub_page._try_navigate_to(path):  # pylint: disable=protected-access
                handled_by_sub_pages = True
        return handled_by_sub_pages

    @staticmethod
    def find_roots(element: Element) -> List[SubPages]:
        """Find all root ``ui.sub_pages`` elements in an element tree.

        :param element: the element to search from
        :return: list of all root ``ui.sub_pages`` elements found
        """
        return [el for el in element.descendants(include_self=True) if isinstance(el, SubPages) and el._is_root]  # pylint: disable=protected-access

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

    def _handle_routes_change(self) -> None:
        assert context.client.request
        path = str(context.client.request.url.path)
        if context.client.request.url.query:
            path += '?' + context.client.request.url.query
        if context.client.request.url.fragment:
            path += '#' + context.client.request.url.fragment
        self._show_page_and_update_browser_url(path)

    def _handle_path_change(self, path: str) -> None:
        if self._is_root and self._send_update_on_path_change:
            self._show_page_and_update_browser_url(f'{self._root_path or ""}{path}')
