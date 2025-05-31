from asyncio import iscoroutine
from typing import Callable, Dict, Optional

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
                if sub_path == path:
                    self._replace_content(path, builder)
                    child_sub_pages = find_child_sub_pages(self)
                    if child_sub_pages:
                        child_sub_pages.show(full_path.removeprefix(path))
                    return True
            segments.pop()
        with self:
            ui.label(f'404: sub page "{full_path}" not found')
        return False

    def _find_base_path(self):
        parent = self
        while True:
            if parent.parent_slot is None:
                return '/'
            parent = parent.parent_slot.parent
            if isinstance(parent, SubPages):
                return parent._current_path

    def _is_root(self) -> bool:
        parent: ui.element = self
        while parent.parent_slot is not None:
            parent = parent.parent_slot.parent
            if isinstance(parent, SubPages):
                return False
        return True

    def _replace_content(self, path: str, builder: Callable):
        self.clear()
        with self:
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
