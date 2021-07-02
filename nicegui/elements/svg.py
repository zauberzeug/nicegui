import justpy as jp
from urllib.parse import urlparse
from .element import Element

class Svg(Element):

    def __init__(self,
                 content: str = '',
                 ):
        """Svg Element

        Displays an svg.

        :param content: the svg definition
        """

        view = jp.Div(style="padding:0;width:100%;height:100%")
        super().__init__(view)
        self.content = content

    @property
    def content(self):

        return self.view.inner_html()

    @content.setter
    def content(self, content: any):

        self.view.components = []
        jp.parse_html(content, a=self.view)

    def set_content(self, content: str):

        self.content = content

    def bind_content_to(self, target, forward=lambda x: x):

        self.content.bind_to(target, forward=forward, nesting=1)
        return self

    def bind_content_from(self, target, backward=lambda x: x):

        self.content.bind_from(target, backward=backward, nesting=1)
        return self

    def bind_content(self, target, forward=lambda x: x, backward=lambda x: x):

        self.content.bind(target, forward=forward, backward=backward, nesting=1)
        return self
