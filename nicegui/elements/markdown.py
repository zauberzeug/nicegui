import hashlib
import os
from collections.abc import Callable
from functools import lru_cache

import markdown2
from fastapi.responses import PlainTextResponse
from pygments.formatters import HtmlFormatter  # pylint: disable=no-name-in-module

from .. import core
from .mixins.content_element import ContentElement


class Markdown(ContentElement, component='markdown.js', default_classes='nicegui-markdown'):
    # NOTE: The Mermaid ESM is already registered in mermaid.py.

    def __init__(self,
                 content: str = '', *,
                 extras: list[str] = ['fenced-code-blocks', 'tables'],  # noqa: B006
                 sanitize: Callable[[str], str] | bool = True,
                 ) -> None:
        """Markdown Element

        Renders Markdown onto the page.

        :param content: the Markdown content to be displayed
        :param extras: list of `markdown2 extensions <https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras>`_ (default: `['fenced-code-blocks', 'tables']`)
        :param sanitize: sanitization mode:
            ``True`` (default) uses client-side sanitization via setHTML or DOMPurify,
            ``False`` disables sanitization (use only with trusted content),
            or pass a callable to apply server-side sanitization
        """
        self._sanitize = sanitize
        self.extras = extras[:]
        super().__init__(content=content)
        self._props['sanitize'] = sanitize is True
        if 'mermaid' in extras:
            self._props['use-mermaid'] = True

        codehilite = self._generate_codehilite_css()
        self._props['resource-name'] = f'codehilite_{hashlib.sha256(codehilite.encode()).hexdigest()[:32]}.css'
        self.add_dynamic_resource(
            self._props['resource-name'],
            lambda: PlainTextResponse(
                codehilite,
                media_type='text/css',
                headers={'Cache-Control': core.app.config.cache_control_directives},
            ),
        )

        self._props.add_rename('resource_name', 'resource-name')  # DEPRECATED: remove in NiceGUI 4.0
        self._props.add_rename('use_mermaid', 'use-mermaid')  # DEPRECATED: remove in NiceGUI 4.0

    @staticmethod
    @lru_cache(maxsize=1)
    def _generate_codehilite_css() -> str:
        return (
            HtmlFormatter(nobackground=True).get_style_defs('.codehilite') +
            HtmlFormatter(nobackground=True, style='github-dark').get_style_defs('.body--dark .codehilite')
        )

    def _handle_content_change(self, content: str) -> None:
        html = prepare_content(content, extras=' '.join(self.extras))
        if callable(self._sanitize):
            html = self._sanitize(html)
        if self._props.get('innerHTML') != html:
            self._props['innerHTML'] = html


@lru_cache(maxsize=int(os.environ.get('MARKDOWN_CONTENT_CACHE_SIZE', '1000')))
def prepare_content(content: str, extras: str) -> str:
    """Render Markdown content to HTML."""
    return markdown2.markdown(remove_indentation(content), extras=extras.split())


def remove_indentation(text: str) -> str:
    """Remove indentation from a multi-line string based on the indentation of the first non-empty line."""
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ''
    indentation = len(lines[0]) - len(lines[0].lstrip())
    return '\n'.join(line[indentation:] for line in lines)
