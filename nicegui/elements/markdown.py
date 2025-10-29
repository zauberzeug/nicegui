import os
from functools import lru_cache

import markdown2
from fastapi.responses import PlainTextResponse
from pygments.formatters import HtmlFormatter  # pylint: disable=no-name-in-module

from .mixins.content_element import ContentElement


class Markdown(ContentElement, component='markdown.js', default_classes='nicegui-markdown'):
    # NOTE: The Mermaid ESM is already registered in mermaid.py.

    def __init__(self,
                 content: str = '', *,
                 extras: list[str] = ['fenced-code-blocks', 'tables'],  # noqa: B006
                 ) -> None:
        """Markdown Element

        Renders Markdown onto the page.

        :param content: the Markdown content to be displayed
        :param extras: list of `markdown2 extensions <https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras>`_ (default: `['fenced-code-blocks', 'tables']`)
        """
        self.extras = extras[:]
        super().__init__(content=content)
        if 'mermaid' in extras:
            self._props['use_mermaid'] = True

        self.add_dynamic_resource(
            'codehilite.css',
            lambda: PlainTextResponse(
                HtmlFormatter(nobackground=True).get_style_defs('.codehilite') +
                HtmlFormatter(nobackground=True, style='github-dark').get_style_defs('.body--dark .codehilite'),
                media_type='text/css',
            ),
        )

    def _handle_content_change(self, content: str) -> None:
        html = prepare_content(content, extras=' '.join(self.extras))
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
