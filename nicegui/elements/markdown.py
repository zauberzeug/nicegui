import markdown2
import justpy as jp
from typing import Union, List
from .element import Element
from icecream import ic

class Markdown(Element):

    def __init__(self,
                 content: str = ''):

        view = jp.Div()
        view.inner_html = markdown2.markdown(content, extras=['fenced-code-blocks'])
        super().__init__(view, '')

    @property
    def text(self):

        return self.view.text

    @text.setter
    def text(self, text: any):

        self.view.text = text

    def set_text(self, text: str):

        self.text = text
