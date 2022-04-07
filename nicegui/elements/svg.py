from typing import Any

import justpy as jp

from .element import Element


class Svg(Element):

    def __init__(self, content: str = ''):
        """Svg Element

        Displays an svg.

        :param content: the svg definition
        """
        view = jp.Div(style='padding:0;width:100%;height:100%', temp=False)
        super().__init__(view)
        self.content = content

    @property
    def content(self):
        return self.view.inner_html()

    @content.setter
    def content(self, content: Any):
        self.view.components = []
        jp.parse_html(content, a=self.view)

    def set_content(self, content: str):
        self.content = content
