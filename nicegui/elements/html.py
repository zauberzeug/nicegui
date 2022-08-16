from typing import Any

import justpy as jp

from .element import Element


class Html(Element):

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

    @property
    def content(self) -> str:
        return self.view.inner_html

    @content.setter
    def content(self, content: str) -> None:
        self.set_content(content)

    def set_content(self, content: str) -> None:
        if '</script>' in content:
            raise ValueError('HTML elements must not contain <script> tags. Use ui.add_body_html() instead.')
        self.view.inner_html = content
        self.update()
