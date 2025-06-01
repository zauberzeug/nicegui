import inspect
import re
from asyncio import iscoroutine
from typing import Any, Callable, Dict, Optional

from typing_extensions import Self

from .. import background_tasks, ui
from ..element import Element


class SubPages(Element, component='sub_pages.js'):

    def __init__(self, routes: Dict[str, Callable]):
        super().__init__()
        self._routes = routes
        if self._is_root():
            path = ui.context.client.request.url.path if ui.context.client.request else '/'
            if self.show(path):
                ui.run_javascript(f'''
                    if (window.location.pathname !== "{path}") {{
                        history.pushState({{page: "{path}"}}, "", "{path}");
                    }}
                ''')

            self.on('open', lambda e: self.show(e.args))

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route to the sub pages."""
        self._routes[path] = page
        return self

    def show(self, full_path: str) -> bool:
        """Show the page for the given path."""
        segments = full_path.split('/')
        while segments:
            sub_path = '/'.join(segments)
            if not sub_path.startswith('/'):
                sub_path = '/' + sub_path
            for path, builder in self._routes.items():
                params = self._match_path(path, sub_path)
                if params is not None:
                    self._replace_content(path, builder, params)
                    child_sub_pages = find_child_sub_pages(self)
                    if child_sub_pages:
                        child_sub_pages.show(full_path.removeprefix(path))
                    return True
            segments.pop()
        with self:
            ui.label(f'404: sub page "{full_path}" not found')
        return False

    @staticmethod
    def _match_path(pattern: str, path: str) -> Optional[Dict[str, str]]:
        """Match a path pattern against an actual path and extract parameters.

        :return: empty dict for exact matches, parameter dict for parameterized matches, None for no match.
        """
        if '{' not in pattern:
            return {} if pattern == path else None
        regex_pattern = pattern
        for match in re.finditer(r'\{(\w+)\}', pattern):
            param_name = match.group(1)
            regex_pattern = regex_pattern.replace(f'{{{param_name}}}', f'(?P<{param_name}>[^/]+)')
        regex_pattern = f'^{regex_pattern}$'
        regex_match = re.match(regex_pattern, path)
        if regex_match:
            return regex_match.groupdict()
        return None

    def _convert_parameter(self, value: str, param_type: type) -> Any:
        """Convert a string parameter to the specified type."""
        if param_type is str:
            return value
        elif param_type is int:
            return int(value)
        elif param_type is float:
            return float(value)
        elif param_type is bool:
            return value.lower() in ('true', '1', 'yes', 'on')
        else:
            return value

    def _is_root(self) -> bool:
        parent: ui.element = self
        while parent.parent_slot is not None:
            parent = parent.parent_slot.parent
            if isinstance(parent, SubPages):
                return False
        return True

    def _replace_content(self, path: str, builder: Callable, params: Optional[Dict[str, str]] = None):
        self.clear()
        with self:
            if params:
                sig = inspect.signature(builder)
                converted_params = {}
                for param_name, param_value in params.items():
                    if param_name in sig.parameters:
                        param_info = sig.parameters[param_name]
                        param_type = param_info.annotation
                        if param_type != inspect.Parameter.empty:
                            converted_params[param_name] = self._convert_parameter(param_value, param_type)
                        else:
                            converted_params[param_name] = param_value
                result = builder(**converted_params)
            else:
                result = builder()
        if iscoroutine(result):
            async def background_task():
                with self:
                    await result
            background_tasks.create(background_task(), name=f'building sub_page {path}')


def find_child_sub_pages(element: ui.element) -> Optional[SubPages]:
    for child in element.default_slot.children:
        if isinstance(child, SubPages):
            return child
        result = find_child_sub_pages(child)
        if result is not None:
            return result
    return None
