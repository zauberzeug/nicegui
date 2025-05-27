from asyncio import iscoroutine
from typing import Callable, Dict

from typing_extensions import Self

from .. import background_tasks, ui
from ..element import Element


class SubPages(Element, component='sub_pages.js'):

    def __init__(self, routes: Dict[str, Callable]):
        super().__init__()
        self._routes = routes
        self._base_path = self._find_base_path()
        self._current_path = '/'
        self.show(ui.context.client.request.url.path if ui.context.client.request else '/')
        self.on('open', lambda e: self.show(e.args))

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route to the sub pages."""
        self._routes[path] = page
        return self

    def show(self, full_path: str):
        """Show the page for the given path."""
        if full_path.startswith(self._base_path):
            path = full_path[len(self._base_path):]
            if not path.startswith('/'):
                path = '/' + path
        else:
            path = full_path
        if path in self._routes:
            self._current_path = path
            self.clear()
            ui.run_javascript(f'''
                if (window.location.pathname !== "{full_path}") {{
                    history.pushState({{page: "{full_path}"}}, "", "{full_path}");
                }}
            ''')
            with self:
                result = self._routes[path]()
            if iscoroutine(result):
                async def background_task():
                    with self:
                        await result
                background_tasks.create(background_task(), name=f'building sub_page {full_path}')
        else:
            if any(full_path.startswith(route) for route in self._routes):
                return
            with self:
                ui.label(f'404: sub page "{path}" not found on {self._base_path}')

    def _find_base_path(self):
        parent = self
        while True:
            if parent.parent_slot is None:
                return '/'
            parent = parent.parent_slot.parent
            if isinstance(parent, SubPages):
                return parent._current_path
