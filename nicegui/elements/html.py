from ..element import Element
from .binding_mixins import BindContentMixin


class Html(Element, BindContentMixin):

    def __init__(self, content: str = '') -> None:
        """HTML Element

        Renders arbitrary HTML onto the page.
        `Tailwind <https://tailwindcss.com/>`_ can be used for styling.
        You can also use `ui.add_head_html` to add html code into the head of the document and `ui.add_body_html`
        to add it into the body.

        :param content: the HTML code to be displayed
        """
        super().__init__('div')
        self.content = content
        self.on_content_change(content)

    def on_content_change(self, content: str) -> None:
        if '</script>' in content:
            raise ValueError('HTML elements must not contain <script> tags. Use ui.add_body_html() instead.')
        self._text = content
        self.update()
