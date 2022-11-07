import justpy as jp

from ..binding import BindableProperty, BindTextMixin
from .element import Element


class Badge(Element, BindTextMixin):
    text = BindableProperty()

    def __init__(self, text: str = '', *,
                 color: str = 'blue', text_color: str = 'white', outline: bool = False) -> None:
        """Badge

        A badge element wrapping Quasar's
        `QBadge <https://v1.quasar.dev/vue-components/badge>`_ component.

        :param text: the initial value of the text field
        :param color: the color name for component from the Quasar Color Palette (default: "blue")
        :param text_color: overrides text color (if needed); color name from the Quasar Color Palette (default: "white")
        :param outline: use 'outline' design (colored text and borders only) (default: False)
        """
        view = jp.QBadge(label=text, color=color, text_color=text_color, outline=outline, temp=True)
        super().__init__(view)

        self.text = text
        self.bind_text_to(self.view, 'label')

    def set_text(self, text: str) -> None:
        self.text = text
