from ..binding import BindTextMixin
from ..element import Element


class Label(Element, BindTextMixin):

    def __init__(self, text: str = '') -> None:
        """Label

        Displays some text.

        :param text: the content of the label
        """
        super().__init__('div')
        self.text = text
