from pathlib import Path
from typing import Callable, List

from fastapi import Request

from .context import context
from .elements.sub_pages import SubPages
from .functions.javascript import run_javascript
from .functions.on import on


class SubPagesRouter:
    def __init__(self) -> None:
        from .functions.html import add_head_html
        self.current_path = '/'
        js = (Path(__file__).parent / 'sub_pages_router.js').read_text(encoding='utf-8')
        add_head_html(f'<script>{js}</script>')
        on('open', lambda event: self._handle_open(event.args))
        on('navigate', lambda event: self._handle_navigate(event.args))
        self.on_path_changed: List[Callable[[str], None]] = []

    def set_request(self, request: Request) -> None:
        path = str(request.url.path)
        if request.url.query:
            path += '?' + request.url.query
        if request.url.fragment:
            path += '#' + request.url.fragment
        self.current_path = path

    def _handle_open(self, path: str) -> None:
        """Handle open event from sub pages element."""
        self._update_path(path)

    def _handle_navigate(self, path: str) -> None:
        """Handle navigate event from sub pages element."""
        updated = self._update_path(path)
        if not updated:
            context.client.open(path, new_tab=False)
            return
        run_javascript(f'''
            const fullPath = (window.path_prefix || '') + "{self.current_path}";
            if (window.location.pathname + window.location.search + window.location.hash !== fullPath) {{
                history.pushState({{page: "{self.current_path}"}}, "", fullPath);
            }}
        ''')

    def _update_path(self, path: str) -> bool:
        self.current_path = path
        for callback in self.on_path_changed:
            callback(path)
        updated = False
        for sub_pages in tuple(el for el in context.client.layout.descendants() if isinstance(el, SubPages)):
            try:
                if sub_pages.show() is not None:
                    updated = True
            except ValueError:
                pass
        return updated
