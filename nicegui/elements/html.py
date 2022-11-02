from typing import Any

import justpy as jp

from ..binding import BindableProperty, BindContentMixin
from .element import Element


class Html(Element, BindContentMixin):
    content = BindableProperty()

    def __init__(self, content: str = ''):
        """HTML Element

        Renders arbitrary HTML onto the page. `Tailwind <https://tailwindcss.com/>`_ can be used for styling.
        You can also use `ui.add_head_html` to add html code into the head of the document and `ui.add_body_html`
        to add it into the body.

        :param content: the HTML code to be displayed
        """
        view = jp.QDiv(temp=False)
        super().__init__(view)

        self.content = content
        self.bind_content_to(self.view, 'inner_html')

    def set_content(self, content: str) -> None:
        if '</script>' in content:
            # TODO: should also be checked if content is set directly
            raise ValueError('HTML elements must not contain <script> tags. Use ui.add_body_html() instead.')
        self.content = content
