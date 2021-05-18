import markdown2
from .html import Html

class Markdown(Html):

    def __init__(self, content: str = '', classes: str = ''):

        super().__init__(content, classes=classes)

    def set_content(self, content: str):

        html = markdown2.markdown(content, extras=['fenced-code-blocks'])
        super().set_content(html)
