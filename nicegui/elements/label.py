from ..binding import BindableProperty, BindTextMixin
from ..element import Element


class Label(Element, BindTextMixin):
    text = BindableProperty()

    def __init__(self, text: str = '') -> None:
        """Label

        Displays some text.

        :param text: the content of the label
        """
        super().__init__('div')
        self.text = text

    @property
    def text(self) -> str:
        return self.content

    @text.setter
    def text(self, value: str) -> None:
        self.content = value
        self.update()

    def set_text(self, text: str) -> None:
        self.text = text
