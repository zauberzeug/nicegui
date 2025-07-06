from pathlib import Path
from typing import List, Tuple

from fastapi import Request

from .context import context
from .elements.sub_pages import SubPages
from .events import GenericEventArguments
from .functions.javascript import run_javascript
from .functions.on import on


class SubPagesRouter:
    def __init__(self) -> None:
        from .functions.html import add_head_html
        self.current_path = '/'
        js = (Path(__file__).parent / 'sub_pages_router.js').read_text(encoding='utf-8')
        add_head_html(f'<script>{js}</script>')
        on('open', self._handle_open)
        on('navigate', self._handle_navigate)

    def set_request(self, request: Request) -> None:
        path = str(request.url.path)
        if request.url.query:
            path += '?' + request.url.query
        if request.url.fragment:
            path += '#' + request.url.fragment
        self.current_path = path

    def get_path_for(self, sub_pages: SubPages) -> str:
        candidates = self._get_sub_pages()
        segments = self.current_path.split('/')
        while segments:
            path = '/'.join(segments) or '/'
            relative_path = path
            for candidate in candidates:
                if sub_pages is candidate:
                    if sub_pages._match_route(relative_path):
                        return relative_path
                relative_path = relative_path[len(candidate.path):]
            segments.pop()
        raise ValueError(f'No path found for {sub_pages}')

    def _get_sub_pages(self) -> Tuple[SubPages, ...]:
        return tuple(el for el in context.client.layout.descendants() if isinstance(el, SubPages))

    def _handle_open(self, event: GenericEventArguments) -> None:
        """Handle open event from sub pages element."""

    def _handle_navigate(self, event: GenericEventArguments) -> None:
        """Handle navigate event from sub pages element."""
        target = event.args['to']
        self.current_path = target
        for sub_pages in self._get_sub_pages():
            try:
                sub_pages.show(self.get_path_for(sub_pages))
            except ValueError:
                pass

        run_javascript(f'''
            const fullPath = (window.path_prefix || '') + "{target}";
            if (window.location.pathname + window.location.search + window.location.hash !== fullPath) {{
                history.pushState({{page: "{target}"}}, "", fullPath);
            }}
        ''')

    def _find_roots(self) -> List[SubPages]:
        """Find all root ``ui.sub_pages`` elements in an element tree.

        :param element: the element to search from
        :return: list of all root ``ui.sub_pages`` elements found
        """
        return [el for el in context.client.layout.descendants(include_self=True) if isinstance(el, SubPages) and el._is_root]  # pylint: disable=protected-access
