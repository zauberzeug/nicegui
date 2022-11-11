from ..binding import BindTextMixin
from ..element import Element


class TextElement(Element, BindTextMixin):
    """An element with a bindable text property."""

    def __init__(self, tag: str, text: str) -> None:
        super().__init__(tag)
        self.text = text
        self.bind_text_to(self, '_text')

    def on_text_change(self, _) -> None:
        self.update()
