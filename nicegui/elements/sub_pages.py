from asyncio import iscoroutine
from typing import Callable, Dict, Self

from .. import background_tasks, ui
from ..element import Element


class SubPages(Element, component='sub_pages.js'):

    def __init__(self, routes: Dict[str, Callable]):
        super().__init__()
        self._routes = routes
        self.show(ui.context.client.request.url.path if ui.context.client.request else '/')
        self.on('open', lambda e: self.show(e.args))

    def add(self, path: str, page: Callable) -> Self:
        """Add a new route to the sub pages."""
        self._routes[path] = page
        return self

    def show(self, path: str):
        """Show the page for the given path."""
        if path in self._routes:
            self.clear()
            ui.run_javascript(f'''
                if (window.location.pathname !== "{path}") {{
                    history.pushState({{page: "{path}"}}, "", "{path}");
                }}
            ''')
            with self:
                result = self._routes[path]()
            if iscoroutine(result):
                async def background_task():
                    with self:
                        await result
                background_tasks.create(background_task(), name=f'sub_pages {path}')
