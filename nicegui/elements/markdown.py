import os
import re
from functools import lru_cache
from typing import List

import markdown2
from pygments.formatters import HtmlFormatter

from .mermaid import Mermaid
from .mixins.content_element import ContentElement


class Markdown(ContentElement, component='markdown.js'):

    def __init__(self, content: str = '', *, extras: List[str] = ['fenced-code-blocks', 'tables']) -> None:
        """Markdown Element

        Renders Markdown onto the page.

        :param content: the Markdown content to be displayed
        :param extras: list of `markdown2 extensions <https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras>`_ (default: `['fenced-code-blocks', 'tables']`)
        """
        self.extras = extras
        super().__init__(content=content)
        self._classes = ['nicegui-markdown']
        self._props['codehilite_css'] = HtmlFormatter(nobackground=True).get_style_defs('.codehilite')
        if 'mermaid' in extras:
            self._props['use_mermaid'] = True
            self.libraries.append(Mermaid.exposed_libraries[0])

    def on_content_change(self, content: str) -> None:
        html = prepare_content(content, extras=' '.join(self.extras))
        if self._props.get('innerHTML') != html:
            self._props['innerHTML'] = html
            self.run_method('update', html)


@lru_cache(maxsize=int(os.environ.get('MARKDOWN_CONTENT_CACHE_SIZE', '1000')))
def prepare_content(content: str, extras: str) -> str:
    html = markdown2.markdown(remove_indentation(content), extras=extras.split())
    return apply_tailwind(html)  # we need explicit Markdown styling because tailwind CSS removes all default styles


def apply_tailwind(html: str) -> str:
    rep = {
        '<h1': '<h1 class="text-5xl mb-4 mt-6"',
        '<h2': '<h2 class="text-4xl mb-3 mt-5"',
        '<h3': '<h3 class="text-3xl mb-2 mt-4"',
        '<h4': '<h4 class="text-2xl mb-1 mt-3"',
        '<h5': '<h5 class="text-1xl mb-0.5 mt-2"',
        '<a': '<a class="underline text-blue-600 hover:text-blue-800 visited:text-purple-600"',
        '<ul': '<ul class="list-disc ml-6"',
        '<p>': '<p class="mb-2">',
        r'<div\ class="codehilite">': '<div class="codehilite mb-2 p-2">',
        '<code': '<code style="background-color: transparent"',
    }
    pattern = re.compile('|'.join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], html)


def remove_indentation(text: str) -> str:
    """Remove indentation from a multi-line string based on the indentation of the first non-empty line."""
    lines = text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ''
    indentation = len(lines[0]) - len(lines[0].lstrip())
    return '\n'.join(line[indentation:] for line in lines)
