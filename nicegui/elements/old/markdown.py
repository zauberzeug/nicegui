from __future__ import annotations

import re
from typing import List

import justpy as jp
import markdown2

from ..binding import BindableProperty, BindContentMixin
from .element import Element


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
        '<div\ class="codehilite">': '<div class=" codehilite mb-2 p-2" style="overflow: scroll">',
        '<code': '<code style="background-color: #f8f8f8"',
    }
    pattern = re.compile('|'.join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], html)


def _handle_content_change(sender: Markdown, content: str) -> None:
    html = markdown2.markdown(content, extras=sender.extras)
    html = apply_tailwind(html)  # we need explicit markdown styling because tailwind CSS removes all default styles
    if sender.view.inner_html != html:
        sender.view.inner_html = html
        sender.update()


class Markdown(Element, BindContentMixin):
    content = BindableProperty(on_change=_handle_content_change)

    def __init__(self, content: str = '', *, extras: List[str] = ['fenced-code-blocks', 'tables']):
        """Markdown Element

        Renders markdown onto the page.

        :param content: the markdown content to be displayed
        :param extras: list of `markdown2 extensions <https://github.com/trentm/python-markdown2/wiki/Extras#implemented-extras>`_ (default: `['fenced-code-blocks', 'tables']`)
        """
        self.extras = extras

        view = jp.QDiv(temp=False)
        super().__init__(view)

        self.content = content
        _handle_content_change(self, content)

    def set_content(self, content: str) -> None:
        self.content = content
